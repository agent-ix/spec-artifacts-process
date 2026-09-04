"""The two-consumer measurement (NFR-001-AC-5, TC-131).

A green local suite is not evidence for a module every repository in the
programme validates against. This runs `quire validate` over two real consumer
repositories twice — once with this module at 0.1.0 and once at 0.2.0 — and
compares the finding sets as a **difference**, so a consumer that is already red
for its own reasons contributes to both sides and therefore to neither.

It is an integration row: it drives the real CLI over trees this repository does
not own. It **fails** rather than skips when a consumer is absent, because a
skipped row is not coverage — the whole point of the measurement is that it
happened.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest
from conftest import BASELINE_MANIFEST, PACKAGE_ROOT

# The two consumers NFR-001 names. Both validate their `spec/**` against this
# module's archetypes, and both are read-only here.
CONSUMERS = ("spec-objects-business", "filament-core-data")

DEV_ROOT = Path(os.environ.get("IX_DEV_ROOT", Path.home() / "dev"))

# Loader-level lines: identical on both sides of the comparison and not a
# document finding. Everything else that is not a warning is one.
LOADER_NOISE = (
    "DuplicateArchetype",
    "UnknownEdgeType",
    "DuplicateInverseEdge",
    "DuplicateModuleName",
)

INSTALLED_MODULES = Path.home() / ".ix" / "filament" / "modules"

# `--summary` prints one line per run naming how many documents were graded.
# Without it a run that read nothing looks exactly like a run that found
# nothing, and the comparison of two empty sets reports success.
GRADED = re.compile(r"^(?P<graded>\d+)/(?P<total>\d+) docs grammar-clean")

# The other `--summary` rollup line. Not a finding, and identical on both sides.
SUMMARY_ROLLUP = re.compile(r"^\d+/\d+ criteria property-extractable")


def consumer_path(name: str) -> Path:
    return DEV_ROOT / name


def staged_modules(tmp_path: Path, manifest: Path, label: str) -> Path:
    """A module SEARCH PATH holding every installed module except this one, plus
    this module at the version under test.

    `--module <dir>` cannot be used: it loads that module *alone*, so every FR,
    US and index document in the consumer becomes `unknown type`, and the two
    sides of the comparison would then be equal for the wrong reason — a
    vacuously green measurement is the exact failure this test exists to avoid.
    """
    root = tmp_path / label
    root.mkdir(parents=True)
    for installed in sorted(INSTALLED_MODULES.iterdir()):
        if installed.name == "spec-artifacts-process":
            continue
        # Copied, not symlinked. A symlinked module makes the loader emit
        # `SymlinkLoop broken at …` once per module — nine lines that appear
        # identically on both sides of the comparison and would satisfy the
        # "did anything happen" guard below without a single document having
        # been read.
        shutil.copytree(installed, root / installed.name)
    module = root / "spec-artifacts-process"
    module.mkdir()
    shutil.copy(manifest, module / "manifest.yaml")
    shutil.copytree(PACKAGE_ROOT / "schemas", module / "schemas")
    shutil.copytree(PACKAGE_ROOT / "skeletons", module / "skeletons")
    return root


def findings(consumer: Path, modules: Path) -> set[str]:
    """Error-severity findings of one consumer, normalised for comparison.

    Warnings are excluded deliberately: `legacy_forms: warning` is the declared
    posture, so a new warning is the contract working. A new **error** is the
    regression this measurement exists to catch.
    """
    environment = dict(os.environ)
    environment["IX_FILAMENT_MODULES_PATH"] = str(modules)
    result = subprocess.run(
        ["quire", "validate", "--scope", str(consumer), "--summary", "spec/**/*.md"],
        capture_output=True,
        text=True,
        env=environment,
    )
    out = set()
    documents = 0
    for line in (result.stdout + result.stderr).split("\n"):
        text = line.strip()
        if not text or text.startswith("warning:"):
            continue
        if any(text.startswith(prefix) for prefix in LOADER_NOISE):
            continue
        match = GRADED.match(text)
        if match:
            documents = int(match.group("total"))
            continue
        if SUMMARY_ROLLUP.match(text):
            continue
        out.add(text.replace(str(consumer) + "/", ""))
    return documents, out


@pytest.mark.integration
@pytest.mark.trace("TC-131")
@pytest.mark.parametrize("name", CONSUMERS)
def test_a_consumer_gains_no_error_finding_under_0_2_0(tmp_path: Path, name: str):
    consumer = consumer_path(name)
    if not (consumer / "spec").is_dir():
        pytest.fail(
            f"the consumer repository {consumer} is not present, so "
            "NFR-001-AC-5 could not be measured. Set IX_DEV_ROOT or check it "
            "out. This fails rather than skips: a measurement that did not "
            "happen is not a measurement that passed."
        )
    commit = subprocess.run(
        ["git", "-C", str(consumer), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert commit, f"{name} has no resolvable commit"

    read_before, before = findings(
        consumer, staged_modules(tmp_path, BASELINE_MANIFEST, "v0_1_0")
    )
    read_after, after = findings(
        consumer, staged_modules(tmp_path, PACKAGE_ROOT / "manifest.yaml", "v0_2_0")
    )
    regressions = sorted(after - before)

    # Recorded so the run is reproducible and a later failure is attributable.
    (tmp_path / f"{name}.measurement.json").write_text(
        json.dumps(
            {
                "consumer": name,
                "commit": commit,
                "documents_graded": read_before,
                "findings_under_0_1_0": len(before),
                "findings_under_0_2_0": len(after),
                "regressions": regressions,
            },
            indent=2,
        )
    )
    # The measurement must have measured something. Comparing the findings of
    # two runs that read no document is a comparison of two empty sets, and it
    # reports success — the vacuous green this whole file exists to avoid.
    assert read_before > 0 and read_after > 0, (
        f"{name}: the validator graded {read_before} documents at 0.1.0 and "
        f"{read_after} at 0.2.0; nothing was measured"
    )
    assert read_before == read_after, (
        f"{name}: {read_before} documents graded at 0.1.0 and {read_after} at 0.2.0 — "
        "the two runs did not see the same corpus, so the difference is not comparable"
    )
    assert regressions == [], (
        f"{name} @ {commit} gains {len(regressions)} error finding(s) under "
        f"0.2.0 that 0.1.0 did not report:\n" + "\n".join(regressions)
    )


@pytest.mark.integration
@pytest.mark.trace("TC-131")
def test_the_measurement_can_fail(tmp_path: Path):
    """A green measurement is worth nothing unless a red one is reachable.

    A module whose `Status` pattern is tightened to admit only `✅` is exactly
    the class of change NFR-001 forbids — a narrowed vocabulary that turns green
    consumers red. It must show up as a regression on a real consumer, or the
    passing run above is a comparison of two empty sets in disguise.
    """
    consumer = consumer_path(CONSUMERS[0])
    if not (consumer / "spec").is_dir():  # pragma: no cover - environment guard
        pytest.fail(f"the consumer repository {consumer} is not present")
    tightened = tmp_path / "tightened.yaml"
    source = (PACKAGE_ROOT / "manifest.yaml").read_text()
    narrowed = source.replace(
        r"Status: '^(✅|❌|🚧|⛔)(\s+.*)?$'", r"Status: '^(✅)(\s+.*)?$'"
    )
    assert narrowed != source, "the Status pattern moved; this guard must be re-aimed"
    tightened.write_text(narrowed)

    _, before = findings(consumer, staged_modules(tmp_path, BASELINE_MANIFEST, "base"))
    _, after = findings(consumer, staged_modules(tmp_path, tightened, "narrowed"))
    regressions = after - before
    assert (
        regressions
    ), "a narrowed Status vocabulary produced no regression — the measurement is blind"
    assert any("Status" in line for line in regressions)
