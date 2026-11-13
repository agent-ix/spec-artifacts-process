"""FR-017: the ADR archetype lists the design-realization verb."""

from __future__ import annotations

import json
import os
import pathlib
import subprocess

import pytest
from conftest import MANIFEST_PATH, PACKAGE_ROOT, REPO_ROOT
from support.strict_yaml import load_yaml_strict

FIXTURES = REPO_ROOT / "tests" / "fixtures" / "adr"


def validate(name: str) -> str:
    result = subprocess.run(
        [
            "quire",
            "validate",
            "--module",
            str(PACKAGE_ROOT),
            "--scope",
            str(FIXTURES),
            str(FIXTURES / f"adr-{name}.md"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout + result.stderr


def adr_links() -> dict[str, list[str]]:
    manifest = load_yaml_strict(MANIFEST_PATH.read_text())
    return next(a for a in manifest["artifact_types"] if a["name"] == "ADR")[
        "allowed_links"
    ]


@pytest.mark.trace("FR-017-AC-1", "TC-217")
def test_adr_may_author_realizes_requirement() -> None:
    assert "realizes_requirement" in adr_links()
    assert "disallowed-edge-type" not in validate("realizes_requirement")


@pytest.mark.trace("FR-017-AC-2", "TC-218")
def test_adr_may_not_author_the_inverse_verb() -> None:
    assert "requirement_realized_by" not in adr_links()
    assert "disallowed-edge-type" in validate("requirement_realized_by")


@pytest.mark.trace("FR-017-AC-3", "TC-219")
def test_adr_unlisted_verb_still_draws_the_finding() -> None:
    assert "disallowed-edge-type" in validate("bogus_verb")


@pytest.mark.trace("FR-017-AC-4", "TC-220")
def test_adr_keeps_its_previous_verbs() -> None:
    links = adr_links()
    for verb in ("supersedes", "superseded_by", "relates_to", "depends_on"):
        assert links[verb] == ["*"]


# The realizing verb and the design relations are declared by
# spec-objects-architecture; the FR and NFR archetypes by spec-artifacts-iso.
# Both are resolved from the installed filament modules.
MODULES_ROOT = pathlib.Path(
    os.environ.get("IX_FILAMENT_MODULES_PATH")
    or pathlib.Path.home() / ".ix" / "filament" / "modules"
)
CORPUS = REPO_ROOT / "tests" / "fixtures" / "design_edges"
MEMBER = "agent-ix/design-fixture"


def quire(*args: str) -> subprocess.CompletedProcess:
    modules = []
    for name in ("spec-artifacts-iso", "spec-objects-architecture"):
        assert (MODULES_ROOT / name / "manifest.yaml").is_file(), (
            f"{name} is not installed under {MODULES_ROOT}; the rows that load "
            "it fail rather than skip, because a skipped row is not coverage"
        )
        modules += ["--module", str(MODULES_ROOT / name)]
    modules += ["--module", str(PACKAGE_ROOT)]
    return subprocess.run(
        ["quire", *args, *modules],
        capture_output=True,
        text=True,
        check=False,
    )


def bundle(kind: str, *extra: str) -> list[str]:
    result = quire("validate", "--okf", *extra, "--repo", f"{MEMBER}={CORPUS / kind}")
    return result.stderr.splitlines()


@pytest.mark.trace("FR-017-AC-5", "TC-221")
def test_realizes_requirement_targets_are_fr_and_nfr() -> None:
    assert adr_links()["realizes_requirement"] == ["FR", "NFR"]


@pytest.mark.trace("FR-017-AC-6", "TC-222")
def test_adr_realizing_fr_and_nfr_draws_no_disallowed_edge() -> None:
    lines = bundle("valid")
    for doc in ("ADR-001", "ADR-002"):
        assert not [ln for ln in lines if doc in ln and "disallowed-edge" in ln]


@pytest.mark.trace("FR-017-AC-7", "TC-223")
def test_adr_realizing_a_part_names_source_target_and_type() -> None:
    wrong = [
        ln for ln in bundle("invalid", "--strict") if "disallowed-edge-target" in ln
    ]
    assert len(wrong) == 1
    assert "ADR-004" in wrong[0]
    assert "scoring_engine" in wrong[0]
    assert "'part'" in wrong[0]


@pytest.mark.trace("FR-017-AC-8", "TC-224")
def test_adr_realizing_a_missing_id_is_a_located_dangling_reference() -> None:
    dangling = [
        ln
        for ln in bundle("invalid", "--strict")
        if "dangling-reference" in ln and "'realizes_requirement'" in ln
    ]
    assert len(dangling) == 1
    assert "ADR-003.md" in dangling[0]
    assert "FR-999" in dangling[0]


@pytest.mark.trace("FR-017-AC-9", "TC-225")
def test_relations_report_the_adr_as_realizing_fr_and_nfr() -> None:
    result = quire("relations", "--json", "--repo", f"{MEMBER}={CORPUS / 'valid'}")
    assert result.returncode == 0, result.stderr
    rows = {
        (rel["name"], row["document"]["id"]): row
        for rel in json.loads(result.stdout)["relations"]
        for row in rel["rows"]
    }
    for relation, requirement, adr in (
        ("fr-has-design-element", "FR-001", "ADR-001"),
        ("nfr-has-design-element", "NFR-001", "ADR-002"),
    ):
        row = rows[(relation, requirement)]
        assert row["state"] == "covered"
        assert [(e["id"], e["archetype"]) for e in row["linked"]] == [(adr, "ADR")]
