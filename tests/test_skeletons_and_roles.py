"""Executable skeletons, packaging, and the definition/occurrence split.

Requirements FR-012 and FR-013; rows TC-111..TC-114, TC-116, TC-119..TC-126.

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
    "IntendedUse": "definition",
    "FeatureRiskRating": "definition",
    "ADR": "definition",
    "Plan": "definition",
    "DossierDocument": "definition",
    "Task": "definition",
    "Review": "definition",
    "SpecReview": "definition",
    "Finding": "definition",
    "Feedback": "definition",
    "Anomaly": "definition",
    "TestMatrixIndex": "definition",
    "TestMatrix": "definition",
    "Standard": "definition",
    "RoleSpec": "definition",
    "Rubric": "definition",
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


def validate_with_quire_cli(model: str, text: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "quire",
            "validate",
            "--module",
            str(PACKAGE_ROOT),
            "--archetype",
            model,
            "-",
        ],
        input=text,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.trace("TC-111", "FR-012-AC-1")
def test_each_declared_type_has_its_canonical_skeleton():
    for model in artifact_type_names():
        assert skeleton_for(model).is_file(), f"missing {model}.md"
    assert (SKELETONS_DIR / "Standard.sysml.md").is_file()


@pytest.mark.parametrize(
    "model",
    [*sorted(artifact_type_names()), "Standard.sysml"],
    ids=lambda model: f"{model}.md",
)
@pytest.mark.trace("TC-112", "FR-012-AC-2", "FR-012-AC-4", "FR-012-CON-1")
def test_every_skeleton_validates_against_its_own_archetype(model: str):
    """A skeleton that does not validate sends every author who copies it into a
    failure, which is why this runs the engine rather than re-reading the YAML."""
    path = SKELETONS_DIR / f"{model}.md"
    model = frontmatter(path.read_text())["type"]
    result = validate_with_quire_cli(model, path.read_text())
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("model", sorted(artifact_type_names()))
@pytest.mark.trace("TC-114", "FR-012-AC-4")
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
        if not locator.get("required") or locator.get("from") == "frontmatter_field":
            continue
        heading = locator.get("under_section") or locator.get("after_heading")
        assert (
            heading in headings
        ), f"{model}.md is missing the required section {heading!r}"


@pytest.mark.trace("TC-116", "FR-012-AC-6", "FR-012-CON-2")
def test_the_added_standard_locators_are_optional_and_omittable(manifest):
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
    result = validate_with_quire_cli("Standard", bare)
    assert result.returncode == 0, result.stdout + result.stderr


def _assert_no_fixtures_packaged(names: list[str]) -> None:
    assert not [n for n in names if "tests/fixtures" in n]


@pytest.mark.integration
@pytest.mark.trace("TC-119", "TC-022", "FR-002-AC-4")
def test_no_fixture_reaches_the_wheel():
    """The valid SpecReview skeleton is included in the wheel, not test fixtures."""
    result = subprocess.run(
        [
            "quire",
            "validate",
            "--module",
            str(PACKAGE_ROOT),
            str(SKELETONS_DIR / "SpecReview.md"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    subprocess.run(
        ["make", "build"], cwd=str(REPO_ROOT), check=True, capture_output=True
    )
    wheel = sorted((REPO_ROOT / "dist").glob("*.whl"))[-1]
    with zipfile.ZipFile(wheel) as archive:
        _assert_no_fixtures_packaged(archive.namelist())
        assert "spec_artifacts_process/skeletons/SpecReview.md" in archive.namelist()


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
        [
            "quire",
            "coverage",
            "--scope",
            str(REPO_ROOT),
            "--module",
            str(PACKAGE_ROOT),
        ],
        capture_output=True,
        text=True,
    )
    assert coverage.returncode == 0, coverage.stderr
    assert "tests/fixtures" not in coverage.stdout


@pytest.mark.trace("TC-120", "FR-013-AC-1", "FR-013-CON-1", "FR-018-AC-7", "TC-236")
def test_every_model_carries_exactly_one_role(mappings):
    roles = {model: spec["role"] for model, spec in mappings["models"].items()}
    assert roles == EXPECTED_ROLES


@pytest.mark.parametrize("model", sorted(artifact_type_names()))
@pytest.mark.trace("TC-121", "FR-013-AC-2")
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


@pytest.mark.trace("TC-122", "FR-013-AC-3")
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


@pytest.mark.trace("TC-123", "FR-013-AC-4")
def test_the_finding_document_and_the_findings_row_keep_distinct_namespaces(manifest):
    row = json.loads((SCHEMAS_DIR / "FindingRow.json").read_text())
    assert set(row["required"]) == {"id", "severity", "summary", "refs", "line"}
    assert "escapeCause" in row["properties"] and "escapeCause" not in row["required"]
    row_id = json.loads((SCHEMAS_DIR / "FindingRowId.json").read_text())
    assert row_id["pattern"] == r"^FND-[0-9]+$"
    document = next(a for a in manifest["artifact_types"] if a["name"] == "Finding")
    assert document["defaults"]["id_pattern"].startswith("FIND-")


@pytest.mark.trace("TC-124", "FR-013-AC-5")
def test_matrix_rows_carry_their_trace_tokens_as_a_list(mapper):
    text = skeleton_for("TestMatrix").read_text()
    text = text.replace(
        "FR-001-AC-1",
        "FR-001-AC-1, -AC-2, -AC-3",
        1,
    )
    record = mapper.build("TestMatrix", text, "skeletons/TestMatrix.md")
    rows = {row["id"]: row for row in record["testCases"]}
    assert rows["TC-001"]["tracesTo"]["tokens"] == [
        "FR-001-AC-1",
        "FR-001-AC-2",
        "FR-001-AC-3",
    ]
    assert rows["TC-004"]["tracesTo"] == {"tokens": [], "noTrace": True}
    # The question a matrix record must answer without re-parsing a cell.
    claimed = {t for row in record["testCases"] for t in row["tracesTo"]["tokens"]}
    assert "FR-001-AC-1" in claimed


@pytest.mark.trace("TC-125", "FR-013-AC-6")
def test_the_unmodelled_concepts_name_their_owner(mappings):
    owners_by_concept = {
        entry["concept"].lower(): entry["owner"] for entry in mappings["not_modelled"]
    }
    expected_owners = {
        "verification run records (runs/**)": "agent-ix/engineering-assurance FR-004",
        "binding records (bindings.json)": "agent-ix/quoin",
        "coverage baselines (baseline.json)": "agent-ix/quoin",
        "evidence freshness": "agent-ix/engineering-assurance FR-004",
    }
    for concept, owner in expected_owners.items():
        assert owners_by_concept.get(concept) == owner


@pytest.mark.parametrize("model", sorted(artifact_type_names()))
@pytest.mark.trace("TC-113")
def test_a_golden_record_exists_for_every_declared_type(model: str):
    assert (EXAMPLES_DIR / f"{model}.record.json").is_file()


@pytest.mark.trace("FR-006-AC-21")
def test_every_legacy_process_example_remains_valid(schema_registry):
    models = sorted(artifact_type_names())
    records = [
        json.loads(path.read_text())
        for path in sorted(EXAMPLES_DIR.glob("*.record.json"))
    ]

    assert {record["type"] for record in records} == set(models)
    for record in records:
        errors = list(schema_registry(record["type"]).iter_errors(record))
        assert errors == [], f"{record['type']} legacy example is invalid: {errors}"
