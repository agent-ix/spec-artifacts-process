"""The Anomaly archetype, its record schema and its fixtures.

Requirements FR-014, FR-015 and NFR-001 (user story US-003).

Three layers are exercised, each through the real artifact it ships:

* **document** — `quire validate` against this module's manifest (vocabularies,
  required sections, table shape);
* **record** — the document mapped by `mappings.yaml` and validated against the
  emitted `Anomaly.json` (the status-conditional checks the `assert` facet
  cannot express);
* **reference** — whether an assessment `Target` resolves, and to what kind. The
  module owns none of that text: it is the engine's reference diagnostic.

The fixtures live under `tests/fixtures/anomaly/` and are read in place by
quoin's tests; quoin holds no copy.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest
from conftest import (
    EXAMPLES_DIR,
    PACKAGE_ROOT,
    REPO_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    frontmatter,
)

FIXTURES = REPO_ROOT / "tests" / "fixtures" / "anomaly"
CORPUS = FIXTURES / "corpus"
VALID = sorted((FIXTURES / "valid").glob("*.md"))
INVALID = {p.stem: p for p in sorted((FIXTURES / "invalid").glob("*.md"))}
INSTALLED = Path.home() / ".ix" / "filament" / "modules"

PLACEHOLDERS = [
    "TBD",
    "tbd",
    "Unknown",
    "unknown",
    "n/a",
    "N/A",
    "None",
    "none",
    "-",
    "",
]


def quire_validate(*paths: Path, scope: Path = FIXTURES) -> subprocess.CompletedProcess:
    """`quire validate` against this module only: it replaces ambient discovery."""
    return subprocess.run(
        [
            "quire",
            "validate",
            "--module",
            str(PACKAGE_ROOT),
            "--scope",
            str(scope),
            *map(str, paths),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def diagnostics(result: subprocess.CompletedProcess) -> list[str]:
    """The located diagnostics of a run; engine registry warnings are not documents'."""
    return [
        line for line in result.stderr.splitlines() if ": line " in line and "[" in line
    ]


def record_errors(mapper, schema_registry, path: Path) -> list:
    record = mapper.build("Anomaly", path.read_text(), path.name)
    return list(schema_registry("Anomaly").iter_errors(record))


def locator(manifest, name: str) -> dict:
    anomaly = next(a for a in manifest["artifact_types"] if a["name"] == "Anomaly")
    return anomaly["body_extraction"]["yield_pattern"]["match"][name]


# -- FR-014 -------------------------------------------------------------------


@pytest.mark.trace("FR-014-AC-1")
def test_the_manifest_declares_anomaly_with_both_vocabularies(manifest):
    assert locator(manifest, "status")["assert"]["choices"] == [
        "identified",
        "assessed",
        "resolved",
        "closed",
    ]
    assert locator(manifest, "resolution")["assert"]["choices"] == [
        "fixed",
        "not-a-defect",
        "duplicate",
        "wont-fix",
    ]
    description = locator(manifest, "description")
    assert description["after_heading"] == "Description"
    assert description["required"] is True


@pytest.mark.trace("FR-014-AC-2")
def test_the_skeleton_validates_as_authored_and_the_schema_is_emitted():
    result = quire_validate(SKELETONS_DIR / "Anomaly.md", scope=REPO_ROOT)
    assert result.returncode == 0, result.stderr
    assert diagnostics(result) == []
    assert (SCHEMAS_DIR / "Anomaly.json").is_file()


@pytest.mark.parametrize("path", VALID, ids=lambda p: p.stem)
@pytest.mark.trace("FR-014-AC-3")
def test_every_valid_fixture_validates_at_document_and_record_layer(
    mapper, schema_registry, path: Path
):
    result = quire_validate(path)
    assert result.returncode == 0, result.stderr
    assert diagnostics(result) == []
    assert record_errors(mapper, schema_registry, path) == []


def test_there_is_a_valid_fixture_per_status_and_closed_resolution():
    seen = {
        (fm["status"], fm.get("resolution"))
        for fm in (frontmatter(p.read_text()) for p in VALID)
    }
    assert {
        ("identified", None),
        ("assessed", None),
        ("resolved", "fixed"),
        ("closed", "fixed"),
        ("closed", "not-a-defect"),
    } <= seen


@pytest.mark.trace("FR-014-AC-4")
def test_a_closed_anomaly_with_no_closed_by_fails(mapper, schema_registry):
    errors = record_errors(mapper, schema_registry, INVALID["closed-no-closed-by"])
    assert [e.validator for e in errors] == ["required"]
    assert "closedBy" in errors[0].message


@pytest.mark.parametrize(
    "name",
    [n for n in INVALID if n.startswith("closed-closed-by-")],
)
@pytest.mark.trace("FR-014-AC-4")
def test_a_placeholder_closed_by_fails_in_any_letter_case(
    mapper, schema_registry, name: str
):
    errors = record_errors(mapper, schema_registry, INVALID[name])
    assert [list(e.absolute_path) for e in errors] == [["closedBy"]]


@pytest.mark.parametrize("value", PLACEHOLDERS)
@pytest.mark.trace("FR-014-AC-4")
def test_the_placeholder_set_is_rejected_and_a_name_is_accepted(
    schema_registry, value: str
):
    record = json.loads((EXAMPLES_DIR / "Anomaly.record.json").read_text())
    record |= {"status": "closed", "resolution": "fixed", "closedBy": value}
    validator = schema_registry("Anomaly")
    assert any(
        list(e.absolute_path) == ["closedBy"] for e in validator.iter_errors(record)
    )
    record["closedBy"] = f" {value}x "
    assert list(validator.iter_errors(record)) == []


@pytest.mark.parametrize(
    "name",
    [
        "resolved-no-resolution",
        "closed-no-resolution",
        "resolved-not-fixed",
        "identified-with-resolution",
    ],
)
@pytest.mark.trace("FR-014-AC-5")
def test_resolution_presence_and_pairing_fail(mapper, schema_registry, name: str):
    assert record_errors(mapper, schema_registry, INVALID[name]) != []


@pytest.mark.parametrize(
    "name", ["identified-with-closed-by", "assessed-with-closed-by"]
)
@pytest.mark.trace("FR-014-AC-6")
def test_closed_by_on_a_non_closed_anomaly_fails(mapper, schema_registry, name: str):
    errors = record_errors(mapper, schema_registry, INVALID[name])
    assert errors != []
    assert all("closedBy" in e.message or e.validator == "not" for e in errors)


@pytest.mark.trace("FR-014-AC-7", "FR-015-AC-9")
def test_the_mapping_names_each_key_once_and_the_golden_record_validates(
    mappings, schema_registry
):
    properties = mappings["models"]["Anomaly"]["properties"]
    for key in ("status", "resolution", "closedBy", "safetyImpact", "assessment"):
        assert key in properties
    assert "statusHistory" not in properties
    assert properties["closedBy"]["path"] == ["closed_by"]
    golden = json.loads((EXAMPLES_DIR / "Anomaly.record.json").read_text())
    assert list(schema_registry("Anomaly").iter_errors(golden)) == []


@pytest.mark.trace("FR-015-AC-9")
def test_assessment_entries_carry_the_target_as_authored(mapper):
    path = FIXTURES / "valid" / "assessed.md"
    rows = mapper.build("Anomaly", path.read_text(), path.name)["assessment"]
    assert [r["target"] for r in rows] == ["FR-001", "FR-001-AC-1", "HAZ-001"]
    none = FIXTURES / "valid" / "none.md"
    row = mapper.build("Anomaly", none.read_text(), none.name)["assessment"][0]
    assert row["kind"] == "None" and "target" not in row


@pytest.mark.trace("FR-014-AC-8")
def test_a_repository_with_no_anomaly_is_unaffected(manifest):
    anomaly = next(a for a in manifest["artifact_types"] if a["name"] == "Anomaly")
    assert "required" not in anomaly
    traceability = manifest.get("traceability", {})
    for declaration in traceability.get("trace_targets", []):
        assert declaration.get("archetype") != "Anomaly"
    other = quire_validate(SKELETONS_DIR / "Feedback.md", scope=REPO_ROOT)
    assert other.returncode == 0, other.stderr


# -- FR-015 -------------------------------------------------------------------


@pytest.mark.trace("FR-015-AC-1")
def test_the_manifest_declares_safety_impact_and_the_assessment_table(manifest):
    assert locator(manifest, "safety_impact")["assert"]["choices"] == [
        "unassessed",
        "none",
        "impacting",
    ]
    assert locator(manifest, "safety_impact")["required"] is True
    table = locator(manifest, "assessment")["assert"]
    assert table["columns"] == ["Kind", "Target", "Impact", "Rationale"]
    assert table["min_rows"] == 1
    assert table["column_choices"] == {
        "Kind": ["Requirement", "Hazard", "None"],
        "Impact": ["Affects", "Mitigates", "Introduces", "Unaffected", "None"],
    }


@pytest.mark.trace("FR-015-AC-2")
def test_an_identified_unassessed_anomaly_without_a_section_validates(
    mapper, schema_registry
):
    path = FIXTURES / "valid" / "identified.md"
    assert "Safety Impact Assessment" not in path.read_text()
    assert quire_validate(path).returncode == 0
    assert record_errors(mapper, schema_registry, path) == []


@pytest.mark.parametrize("status", ["assessed", "resolved", "closed"])
@pytest.mark.trace("FR-015-AC-3")
def test_assessed_or_later_needs_a_section_and_a_judged_impact(
    mapper, schema_registry, status: str
):
    no_section = record_errors(mapper, schema_registry, INVALID[f"{status}-no-section"])
    assert [e.message for e in no_section if "assessment" in e.message]
    unassessed = record_errors(mapper, schema_registry, INVALID[f"{status}-unassessed"])
    assert [list(e.absolute_path) for e in unassessed] == [["safetyImpact"]]


@pytest.mark.parametrize(
    "name",
    [
        "impacting-only-unaffected",
        "impacting-only-impact-none",
        "impacting-row-impact-none",
        "none-with-affects",
        "none-with-hazard-row",
    ],
)
@pytest.mark.trace("FR-015-AC-7")
def test_the_none_and_impacting_table_shapes_fail(mapper, schema_registry, name: str):
    assert record_errors(mapper, schema_registry, INVALID[name]) != []


@pytest.mark.trace("FR-015-AC-7")
def test_a_none_anomaly_with_one_none_row_validates(mapper, schema_registry):
    path = FIXTURES / "valid" / "none.md"
    assert record_errors(mapper, schema_registry, path) == []


@pytest.mark.trace("FR-015-AC-8")
def test_an_empty_rationale_and_an_impact_outside_the_vocabulary_fail_validation():
    rationale = quire_validate(INVALID["empty-rationale"])
    assert rationale.returncode != 0
    assert "Rationale" in rationale.stderr
    impact = quire_validate(INVALID["impact-outside-vocabulary"])
    assert impact.returncode != 0
    assert "Impact" in impact.stderr


@pytest.mark.trace("FR-015-AC-4")
def test_the_corpus_validates_so_the_links_have_something_to_resolve_to():
    modules = [INSTALLED / "spec-artifacts-iso", INSTALLED / "spec-objects-safety"]
    for module in modules:
        assert module.is_dir(), f"{module} is not installed"
    result = subprocess.run(
        [
            "quire",
            "validate",
            "--scope",
            str(CORPUS),
            "--module",
            str(PACKAGE_ROOT),
            *[arg for m in modules for arg in ("--module", str(m))],
            "spec/**/*.md",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    ids = {frontmatter(p.read_text())["id"] for p in CORPUS.glob("spec/**/*.md")}
    assert {"FR-001", "HAZ-001", "HAZ-002", "HAZ-003"} <= ids
    assert (
        "FR-001-AC-1"
        in (CORPUS / "spec/functional/FR-001-verify-checksums.md").read_text()
    )


@pytest.mark.xfail(
    strict=True,
    reason=(
        "quire 0.56 does not resolve a table-cell reference to a document id or "
        "type it by the row's Kind (quire-rs FR-026/FR-040): `quire validate` "
        "reports no dangling-reference or kind-mismatch diagnostic for an "
        "assessment Target. Turns green when the engine reports them."
    ),
)
@pytest.mark.parametrize(
    "name",
    [
        "dangling-requirement",
        "dangling-criterion",
        "dangling-hazard",
        "requirement-row-names-hazard",
        "hazard-row-names-requirement",
    ],
)
@pytest.mark.trace("FR-015-AC-5", "FR-015-AC-6")
def test_dangling_and_mismatched_targets_fail_validation_in_the_corpus(
    tmp_path: Path, name: str
):
    corpus = tmp_path / "corpus"
    shutil.copytree(CORPUS, corpus)
    (corpus / "spec" / "anomalies").mkdir()
    shutil.copy(INVALID[name], corpus / "spec" / "anomalies" / "AN-001.md")
    modules = [INSTALLED / "spec-artifacts-iso", INSTALLED / "spec-objects-safety"]
    result = subprocess.run(
        [
            "quire",
            "validate",
            "--scope",
            str(corpus),
            "--module",
            str(PACKAGE_ROOT),
            *[arg for m in modules for arg in ("--module", str(m))],
            "spec/anomalies/AN-001.md",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0, "the engine accepted an unresolvable Target"


@pytest.mark.trace("FR-015-AC-10", "FR-014-AC-2")
def test_the_negative_counterparts_exist_for_every_named_defect():
    required = {
        # FR-014
        "closed-no-closed-by",
        "closed-closed-by-tbd",
        "resolved-no-resolution",
        "identified-with-closed-by",
        # FR-015
        "assessed-no-section",
        "dangling-requirement",
        "dangling-hazard",
        "requirement-row-names-hazard",
        "hazard-row-names-requirement",
    }
    assert required <= set(INVALID)
    assert (FIXTURES / "valid" / "two-hazards.md").is_file()
    hazards = {p.stem for p in (CORPUS / "spec" / "hazard").glob("*.md")}
    named = {
        row.split("|")[2].strip()
        for p in VALID
        for row in p.read_text().splitlines()
        if row.startswith("| Hazard")
    }
    assert hazards - named == {"HAZ-003"}


# -- NFR-001 ------------------------------------------------------------------


@pytest.mark.trace("NFR-001-AC-1")
def test_fixture_a_reports_both_coexisting_record_defects_in_one_pass(
    mapper, schema_registry
):
    errors = record_errors(
        mapper, schema_registry, INVALID["nfr1-a-closed-no-closed-by-no-resolution"]
    )
    assert sorted(e.message for e in errors) == [
        "'closedBy' is a required property",
        "'resolution' is a required property",
    ]


@pytest.mark.trace("NFR-001-AC-1")
def test_fixture_b_reports_both_coexisting_record_defects_in_one_pass(
    mapper, schema_registry
):
    errors = record_errors(
        mapper, schema_registry, INVALID["nfr1-b-assessed-unassessed-no-section"]
    )
    assert len(errors) == 2
    assert {e.validator for e in errors} == {"required", "not"}


@pytest.mark.trace("NFR-001-AC-1", "NFR-001-AC-2")
def test_fixture_c_document_layer_defect_is_reported_with_its_line():
    result = quire_validate(INVALID["nfr1-c-dangling-mismatch-empty-rationale"])
    found = diagnostics(result)
    assert len(found) == 1, result.stderr
    assert "Rationale" in found[0]
    assert ": line 20:" in found[0]
