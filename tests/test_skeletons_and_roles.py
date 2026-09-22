"""Executable skeletons, packaging, and the definition/occurrence split.

Requirements FR-012 and FR-013; rows TC-111..TC-114, TC-116, TC-119..TC-126, TC-130.

The skeletons are validated through the ENGINE against this module's own
manifest, so the contract is asserted as an author experiences it rather than as
a YAML shape.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest
from conftest import (
    EXAMPLES_DIR,
    PACKAGE_ROOT,
    REPO_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    artifact_type_names,
    frontmatter,
)

# Per FR-013 each model carries one role. `definition` is authored intent;
# `evidence-act`
# records that a human or a named command was declared as the source of
# evidence. Neither is a run.
EXPECTED_ROLES = {
    "ADR": "definition",
    "Plan": "definition",
    "Task": "definition",
    "Review": "definition",
    "SpecReview": "definition",
    "Finding": "definition",
    "Feedback": "definition",
    "TestMatrixIndex": "definition",
    "TestMatrix": "definition",
    "Standard": "definition",
    "SuiteRegistry": "evidence-act",
    "Inspections": "evidence-act",
}

# Whole words that name an execution outcome. A property matching one of these
# would make a definition carry an occurrence, which is what FR-013 forbids.
RUN_LEXICON = (
    "run",
    "runId",
    "startedAt",
    "finishedAt",
    "duration",
    "passed",
    "failed",
    "log",
    "artifact",
    "elapsed",
    "exitCode",
)

# One property matches the lexicon and is not a run record. It is listed here,
# with its reason, rather than removed from the lexicon: narrowing the words to
# make a check pass is how a check stops catching the thing it was written for.
LEXICON_EXCEPTIONS = {
    # The spec document a feedback thread is anchored IN — a repo-relative path
    # or an ix:// reference to an authored artifact. Not an artefact a run
    # produced; the word is the same and the concept is not.
    "FeedbackAnchor.json.artifact",
}


def skeleton_for(model: str) -> Path:
    return SKELETONS_DIR / f"{model}.md"


@pytest.mark.trace("TC-111")
def test_every_declared_type_has_exactly_one_skeleton():
    present = {p.name for p in SKELETONS_DIR.glob("*.md")}
    expected = {f"{name}.md" for name in artifact_type_names()} | {"Standard.sysml.md"}
    assert present == expected


@pytest.mark.parametrize(
    "path", sorted(SKELETONS_DIR.glob("*.md")), ids=lambda p: p.name
)
@pytest.mark.trace("TC-112")
def test_every_skeleton_validates_against_its_own_archetype(quire_engine, path: Path):
    """A skeleton that does not validate sends every author who copies it into a
    failure, which is why this runs the engine rather than re-reading the YAML."""
    model = frontmatter(path.read_text())["type"]
    result = quire_engine.validate_document(model, str(PACKAGE_ROOT), path.read_text())
    assert result["errors"] == [], result["errors"]
    assert result["is_valid"] is True


@pytest.mark.parametrize(
    "path", sorted(SKELETONS_DIR.glob("*.md")), ids=lambda p: p.name
)
@pytest.mark.trace("TC-130")
def test_every_skeleton_validates_under_0_2_0_with_zero_errors(
    quire_engine, path: Path
):
    """NFR-001-AC-4. Same engine call as TC-112, asserted as the compatibility
    claim rather than as the authoring claim: the two rows would be deleted for
    different reasons."""
    model = frontmatter(path.read_text())["type"]
    assert quire_engine.validate_document(model, str(PACKAGE_ROOT), path.read_text())[
        "is_valid"
    ]


@pytest.mark.parametrize("model", sorted(artifact_type_names()))
@pytest.mark.trace("TC-114")
def test_every_required_section_is_present_in_its_skeleton(manifest, model: str):
    entry = next(a for a in manifest["artifact_types"] if a["name"] == model)
    locators = ((entry.get("body_extraction") or {}).get("yield_pattern") or {}).get(
        "match"
    ) or {}
    text = skeleton_for(model).read_text()
    headings = {
        line.lstrip("#").strip() for line in text.split("\n") if line.startswith("#")
    }
    for name, locator in locators.items():
        if not locator.get("required"):
            continue
        heading = locator.get("under_section") or locator.get("after_heading")
        assert (
            heading in headings
        ), f"{model}.md is missing the required section {heading!r}"


@pytest.mark.trace("TC-116")
def test_the_added_standard_locators_are_optional_and_omittable(quire_engine, manifest):
    entry = next(a for a in manifest["artifact_types"] if a["name"] == "Standard")
    locators = entry["body_extraction"]["yield_pattern"]["match"]
    assert set(locators) == {"properties", "invariants"}
    for locator in locators.values():
        assert locator["required"] is False
    bare = (
        '---\nid: Standard-200\ntitle: "a standard with neither section"\n'
        "type: Standard\ncode: bare\n---\n"
        "# Standard-200: a standard with neither section\n\n"
        "## Description\n\nNothing typed here.\n"
    )
    assert quire_engine.validate_document("Standard", str(PACKAGE_ROOT), bare)[
        "is_valid"
    ]


def _assert_no_fixtures_packaged(names: list[str]) -> None:
    assert not [n for n in names if "tests/fixtures" in n]


@pytest.mark.integration
@pytest.mark.trace("TC-119")
def test_no_fixture_reaches_the_wheel():
    """No file under `tests/fixtures/` is packaged into the built wheel. Needs
    no engine — `make build` is Poetry, so this half runs with no `quire` CLI
    on PATH."""
    subprocess.run(
        ["make", "build"], cwd=str(REPO_ROOT), check=True, capture_output=True
    )
    wheel = sorted((REPO_ROOT / "dist").glob("*.whl"))[-1]
    with zipfile.ZipFile(wheel) as archive:
        _assert_no_fixtures_packaged(archive.namelist())


def test_the_wheel_fixture_check_can_fail():
    """Proves `test_no_fixture_reaches_the_wheel` is not vacuous: a namelist
    carrying a `tests/fixtures/...` entry must fail the same assertion."""
    with pytest.raises(AssertionError):
        _assert_no_fixtures_packaged(
            [
                "spec_artifacts_process/manifest.yaml",
                "tests/fixtures/negative/some-fixture.md",
            ]
        )


@pytest.mark.integration
@pytest.mark.trace("TC-119")
def test_no_fixture_mints_an_id():
    """`quire coverage` is an engine behaviour over the whole repository, so this
    is an integration row rather than a unit one."""
    if shutil.which("quire") is None:
        pytest.skip("the `quire` CLI is required for `quire coverage`")
    coverage = subprocess.run(
        ["quire", "coverage", "--scope", str(REPO_ROOT)],
        capture_output=True,
        text=True,
    )
    assert coverage.returncode == 0, coverage.stderr
    assert "tests/fixtures" not in coverage.stdout


@pytest.mark.trace("TC-120")
def test_every_model_carries_exactly_one_role(mappings):
    roles = {model: spec["role"] for model, spec in mappings["models"].items()}
    assert roles == EXPECTED_ROLES


@pytest.mark.parametrize("model", sorted(artifact_type_names()))
@pytest.mark.trace("TC-121")
def test_no_model_declares_a_run_property(model: str):
    """Walks the model and everything it `$ref`s, so a run property cannot hide
    one level down in a row type."""
    seen: set[str] = set()
    frontier = [f"{model}.json"]
    offenders: list[str] = []
    while frontier:
        name = frontier.pop()
        if name in seen:
            continue
        seen.add(name)
        path = SCHEMAS_DIR / name
        if not path.is_file():
            continue
        schema = json.loads(path.read_text())
        for prop in schema.get("properties", {}):
            for word in RUN_LEXICON:
                if re.fullmatch(word, prop) or re.fullmatch(rf"{word}[A-Z]\w*", prop):
                    offenders.append(f"{name}.{prop}")
        for ref in re.findall(r'"\$ref":\s*"([^"]+)"', json.dumps(schema)):
            frontier.append(ref.rsplit("/", 1)[-1])
    unexplained = [o for o in offenders if o not in LEXICON_EXCEPTIONS]
    assert unexplained == [], unexplained


@pytest.mark.trace("TC-122")
def test_plan_and_task_declare_no_execution_property(mappings):
    for model in ("Plan", "Task"):
        properties = set(mappings["models"][model]["properties"])
        assert "status" in properties, "the authored lifecycle word stays"
        assert not properties & {
            "startedAt",
            "finishedAt",
            "duration",
            "outcome",
            "runId",
        }
    assert "track" in mappings["models"]["Task"]["properties"]
    task = json.loads((SCHEMAS_DIR / "Task.json").read_text())
    assert "track" not in task["required"], "FR-005: `track` is optional"


@pytest.mark.trace("TC-123")
def test_the_finding_document_and_the_findings_row_keep_distinct_namespaces(manifest):
    row = json.loads((SCHEMAS_DIR / "FindingRow.json").read_text())
    assert set(row["required"]) == {"id", "severity", "summary", "refs", "line"}
    assert "escapeCause" in row["properties"] and "escapeCause" not in row["required"]
    row_id = json.loads((SCHEMAS_DIR / "FindingRowId.json").read_text())
    assert row_id["pattern"] == r"^FND-[0-9]+$"
    document = next(a for a in manifest["artifact_types"] if a["name"] == "Finding")
    assert document["defaults"]["id_pattern"].startswith("FIND-")


@pytest.mark.trace("TC-124")
def test_matrix_rows_carry_their_trace_tokens_as_a_list(mapper):
    record = mapper.build(
        "TestMatrix", skeleton_for("TestMatrix").read_text(), "skeletons/TestMatrix.md"
    )
    rows = {row["id"]: row for row in record["testCases"]}
    assert rows["TC-001"]["tracesTo"]["tokens"] == ["FR-001-AC-1"]
    assert rows["TC-004"]["tracesTo"] == {"tokens": [], "noTrace": True}
    # The question a matrix record must answer without re-parsing a cell.
    claimed = {t for row in record["testCases"] for t in row["tracesTo"]["tokens"]}
    assert "FR-001-AC-1" in claimed


@pytest.mark.trace("TC-125")
def test_the_unmodelled_concepts_name_their_owner(mappings):
    entries = mappings["not_modelled"]
    assert len(entries) >= 3
    for entry in entries:
        assert entry["owner"].startswith("agent-ix/")
        assert entry["reason"].strip()
    concepts = " ".join(e["concept"].lower() for e in entries)
    assert "run" in concepts and "baseline" in concepts


@pytest.mark.parametrize("model", sorted(artifact_type_names()))
@pytest.mark.trace("TC-113")
def test_a_golden_record_exists_for_every_declared_type(model: str):
    assert (EXAMPLES_DIR / f"{model}.record.json").is_file()
