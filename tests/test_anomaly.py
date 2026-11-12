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


def signature(errors) -> list[tuple]:
    """(validator, path) of each error, in schema order."""
    return [(e.validator, list(e.absolute_path)) for e in errors]


def rule_index(error) -> int:
    """Which top-level conditional (`allOf` entry) raised the error."""
    path = list(error.relative_schema_path)
    return path[path.index("allOf") + 1]


def locator(manifest, name: str) -> dict:
    anomaly = next(a for a in manifest["artifact_types"] if a["name"] == "Anomaly")
    return anomaly["body_extraction"]["yield_pattern"]["match"][name]


# -- FR-014 -------------------------------------------------------------------


@pytest.mark.trace("FR-014-AC-1", "TC-168")
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


@pytest.mark.trace("FR-014-AC-2", "TC-169")
def test_the_skeleton_validates_as_authored_and_the_schema_is_emitted():
    result = quire_validate(SKELETONS_DIR / "Anomaly.md", scope=REPO_ROOT)
    assert result.returncode == 0, result.stderr
    assert diagnostics(result) == []
    assert (SCHEMAS_DIR / "Anomaly.json").is_file()


@pytest.mark.parametrize("path", VALID, ids=lambda p: p.stem)
@pytest.mark.trace("FR-014-AC-3", "TC-170")
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


@pytest.mark.trace("FR-014-AC-4", "TC-171")
def test_a_closed_anomaly_with_no_closed_by_fails(mapper, schema_registry):
    errors = record_errors(mapper, schema_registry, INVALID["closed-no-closed-by"])
    assert [e.validator for e in errors] == ["required"]
    assert "closedBy" in errors[0].message


@pytest.mark.parametrize(
    "name",
    [n for n in INVALID if n.startswith("closed-closed-by-")],
)
@pytest.mark.trace("FR-014-AC-4", "TC-171")
def test_a_placeholder_closed_by_fails_in_any_letter_case(
    mapper, schema_registry, name: str
):
    errors = record_errors(mapper, schema_registry, INVALID[name])
    assert [list(e.absolute_path) for e in errors] == [["closedBy"]]


@pytest.mark.parametrize("value", PLACEHOLDERS)
@pytest.mark.trace("FR-014-AC-4", "TC-171")
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


@pytest.mark.parametrize("name", ["resolved-no-resolution", "closed-no-resolution"])
@pytest.mark.trace("FR-014-AC-5", "TC-172")
def test_a_resolved_or_closed_anomaly_needs_a_resolution(
    mapper, schema_registry, name: str
):
    errors = record_errors(mapper, schema_registry, INVALID[name])
    assert signature(errors) == [("required", [])]
    assert "'resolution'" in errors[0].message


@pytest.mark.trace("FR-014-AC-5", "TC-172")
def test_a_resolved_anomaly_must_be_fixed(mapper, schema_registry):
    errors = record_errors(mapper, schema_registry, INVALID["resolved-not-fixed"])
    assert signature(errors) == [("const", ["resolution"])]


@pytest.mark.parametrize(
    "name", ["identified-with-resolution", "assessed-with-resolution"]
)
@pytest.mark.trace("FR-014-AC-5", "TC-172")
def test_an_identified_or_assessed_anomaly_carries_no_resolution(
    mapper, schema_registry, name: str
):
    errors = record_errors(mapper, schema_registry, INVALID[name])
    assert [(e.validator, rule_index(e)) for e in errors] == [("not", 0)]


@pytest.mark.parametrize(
    "name", ["identified-with-closed-by", "assessed-with-closed-by"]
)
@pytest.mark.trace("FR-014-AC-6", "TC-173")
def test_closed_by_on_a_non_closed_anomaly_fails(mapper, schema_registry, name: str):
    errors = record_errors(mapper, schema_registry, INVALID[name])
    assert [(e.validator, rule_index(e)) for e in errors] == [("not", 2)]


@pytest.mark.trace("FR-014-AC-7", "FR-015-AC-9", "TC-174", "TC-184")
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


@pytest.mark.trace("FR-015-AC-9", "TC-184")
def test_assessment_entries_carry_the_target_as_authored(mapper):
    path = FIXTURES / "valid" / "assessed.md"
    rows = mapper.build("Anomaly", path.read_text(), path.name)["assessment"]
    assert [r["target"] for r in rows] == ["FR-001", "FR-001-AC-1", "HAZ-001"]
    none = FIXTURES / "valid" / "none.md"
    row = mapper.build("Anomaly", none.read_text(), none.name)["assessment"][0]
    assert row["kind"] == "None" and "target" not in row


@pytest.mark.trace("FR-014-AC-8", "TC-175")
def test_a_repository_with_no_anomaly_is_unaffected(manifest):
    anomaly = next(a for a in manifest["artifact_types"] if a["name"] == "Anomaly")
    assert "required" not in anomaly
    traceability = manifest.get("traceability", {})
    for declaration in traceability.get("trace_targets", []):
        assert declaration.get("archetype") != "Anomaly"
    other = quire_validate(SKELETONS_DIR / "Feedback.md", scope=REPO_ROOT)
    assert other.returncode == 0, other.stderr


# -- FR-015 -------------------------------------------------------------------


@pytest.mark.trace("FR-015-AC-1", "TC-176")
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


@pytest.mark.trace("FR-015-AC-2", "TC-177")
def test_an_identified_unassessed_anomaly_without_a_section_validates(
    mapper, schema_registry
):
    path = FIXTURES / "valid" / "identified.md"
    assert "Safety Impact Assessment" not in path.read_text()
    assert quire_validate(path).returncode == 0
    assert record_errors(mapper, schema_registry, path) == []


@pytest.mark.parametrize("status", ["assessed", "resolved", "closed"])
@pytest.mark.trace("FR-015-AC-3", "TC-178")
def test_assessed_or_later_needs_a_section_and_a_judged_impact(
    mapper, schema_registry, status: str
):
    no_section = record_errors(mapper, schema_registry, INVALID[f"{status}-no-section"])
    assert signature(no_section) == [("required", [])], "one defect, one diagnostic"
    assert "'assessment'" in no_section[0].message
    unassessed = record_errors(mapper, schema_registry, INVALID[f"{status}-unassessed"])
    assert [list(e.absolute_path) for e in unassessed] == [["safetyImpact"]]


@pytest.mark.parametrize(
    "name", ["identified-impacting-no-section", "identified-none-no-section"]
)
@pytest.mark.trace("FR-015-AC-3", "FR-015-AC-7", "TC-178", "TC-182")
def test_an_identified_none_or_impacting_anomaly_still_needs_its_table(
    mapper, schema_registry, name: str
):
    errors = record_errors(mapper, schema_registry, INVALID[name])
    assert signature(errors) == [("required", [])]
    assert "'assessment'" in errors[0].message


@pytest.mark.parametrize(
    "name",
    ["impacting-only-unaffected", "impacting-only-impact-none"],
)
@pytest.mark.trace("FR-015-AC-7", "TC-182")
def test_an_impacting_anomaly_needs_a_row_that_is_not_unaffected(
    mapper, schema_registry, name: str
):
    errors = record_errors(mapper, schema_registry, INVALID[name])
    assert signature(errors) == [("contains", ["assessment"])]


@pytest.mark.trace("FR-015-AC-7", "TC-182")
def test_impact_none_is_admitted_only_on_a_none_row(mapper, schema_registry):
    errors = record_errors(
        mapper, schema_registry, INVALID["impacting-row-impact-none"]
    )
    assert ("not", ["assessment", 0, "impact"]) in signature(errors)


@pytest.mark.trace("FR-015-AC-7", "TC-182")
def test_a_none_anomaly_row_must_carry_impact_none(mapper, schema_registry):
    errors = record_errors(mapper, schema_registry, INVALID["none-with-affects"])
    assert signature(errors) == [("const", ["assessment", 0, "impact"])]


@pytest.mark.trace("FR-015-AC-7", "TC-182")
def test_a_none_anomaly_holds_exactly_one_row(mapper, schema_registry):
    errors = record_errors(mapper, schema_registry, INVALID["none-with-hazard-row"])
    assert ("maxItems", ["assessment"]) in signature(errors)


@pytest.mark.trace("FR-015-AC-7", "TC-182")
def test_a_none_anomaly_with_one_none_row_validates(mapper, schema_registry):
    path = FIXTURES / "valid" / "none.md"
    assert record_errors(mapper, schema_registry, path) == []


@pytest.mark.trace("FR-015-AC-8", "TC-183")
def test_an_empty_rationale_and_an_impact_outside_the_vocabulary_fail_validation():
    rationale = quire_validate(INVALID["empty-rationale"])
    assert rationale.returncode != 0
    assert "Rationale" in rationale.stderr
    impact = quire_validate(INVALID["impact-outside-vocabulary"])
    assert impact.returncode != 0
    assert "Impact" in impact.stderr


def bundle_validate(tmp_path: Path, anomaly: Path) -> subprocess.CompletedProcess:
    """Validate the fixture corpus plus one anomaly as a bundle.

    Reference resolution (quire-rs FR-049) runs over the bundle, so the anomaly
    is placed in a copy of the corpus. `--okf` is the posture that reports the
    finding as a warning, so a clean exit does not mean no finding: callers read
    the `[dangling-trace-reference]` lines.
    """
    modules = [INSTALLED / "spec-artifacts-iso", INSTALLED / "spec-objects-safety"]
    for module in modules:
        assert module.is_dir(), f"{module} is not installed"
    corpus = tmp_path / "corpus"
    shutil.copytree(CORPUS, corpus)
    (corpus / "spec" / "anomalies").mkdir()
    shutil.copy(anomaly, corpus / "spec" / "anomalies" / "AN-001.md")
    return subprocess.run(
        [
            "quire",
            "validate",
            "--okf",
            "--scope",
            str(corpus),
            "--module",
            str(PACKAGE_ROOT),
            *[arg for m in modules for arg in ("--module", str(m))],
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def reference_findings(result: subprocess.CompletedProcess, kind: str) -> list[str]:
    return [
        line
        for line in result.stderr.splitlines()
        if f"[{kind}]" in line and "AN-001.md" in line
    ]


def dangling_findings(result: subprocess.CompletedProcess) -> list[str]:
    return reference_findings(result, "dangling-trace-reference")


@pytest.mark.trace("FR-015-AC-4", "TC-179")
def test_the_impacting_anomaly_validates_in_a_corpus_that_supplies_its_links(
    tmp_path: Path, mapper, schema_registry
):
    path = FIXTURES / "valid" / "impacting-all-targets.md"
    rows = [
        r["target"]
        for r in mapper.build("Anomaly", path.read_text(), "x")["assessment"]
    ]
    assert rows == ["FR-001", "FR-001-AC-1", "HAZ-001"]
    result = bundle_validate(tmp_path, path)
    assert result.returncode == 0, result.stderr
    assert dangling_findings(result) == [], result.stderr
    assert quire_validate(path).returncode == 0
    assert record_errors(mapper, schema_registry, path) == []


@pytest.mark.parametrize(
    "name,target,kind",
    [
        ("dangling-requirement", "FR-999", "Requirement"),
        ("dangling-criterion", "FR-001-AC-99", "Requirement"),
        ("dangling-hazard", "HAZ-999", "Hazard"),
    ],
)
@pytest.mark.trace("FR-015-AC-5", "TC-180")
def test_a_dangling_target_is_reported_naming_the_id_and_its_row(
    tmp_path: Path, name: str, target: str, kind: str
):
    # Only the diagnostic is asserted: bundle validation under `--okf` reports
    # it as a warning and exits 0. FR-015 names the Strict posture as the one
    # that fails, and no quire command here runs a bundle under Strict.
    found = dangling_findings(bundle_validate(tmp_path, INVALID[name]))
    assert len(found) == 1, found
    assert f"'{target}'" in found[0]
    assert f"(row '{kind}')" in found[0]


@pytest.mark.parametrize(
    "name,target,kind",
    [
        ("requirement-row-names-hazard", "HAZ-001", "Requirement"),
        ("hazard-row-names-requirement", "FR-001", "Hazard"),
    ],
)
@pytest.mark.trace("FR-015-AC-6", "TC-181")
def test_a_target_of_the_wrong_kind_is_reported_as_a_kind_mismatch(
    tmp_path: Path, name: str, target: str, kind: str
):
    found = reference_findings(
        bundle_validate(tmp_path, INVALID[name]), "reference-kind-mismatch"
    )
    assert len(found) == 1, found
    assert f"'{target}'" in found[0]
    assert f"(row '{kind}')" in found[0]


@pytest.mark.trace("FR-015-AC-4", "FR-015-AC-6", "TC-179", "TC-181")
def test_a_requirement_row_may_name_an_nfr_and_its_criterion(tmp_path: Path):
    result = bundle_validate(
        tmp_path, FIXTURES / "valid" / "requirement-rows-name-nfr.md"
    )
    assert result.returncode == 0, result.stderr
    assert dangling_findings(result) == [], result.stderr
    assert reference_findings(result, "reference-kind-mismatch") == [], result.stderr


@pytest.mark.trace("FR-015-AC-6", "TC-181")
def test_a_hazard_row_naming_an_nfr_or_its_criterion_is_a_kind_mismatch(
    tmp_path: Path,
):
    result = bundle_validate(tmp_path, INVALID["hazard-row-names-nfr"])
    found = reference_findings(result, "reference-kind-mismatch")
    assert len(found) == 2, result.stderr
    assert dangling_findings(result) == []
    for target in ("NFR-002", "NFR-002-AC-1"):
        assert sum(f"'{target}'" in line for line in found) == 1, found
    assert all("(row 'Hazard')" in line for line in found), found


@pytest.mark.trace("FR-015-AC-10", "FR-014-AC-2", "TC-169", "TC-185")
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


@pytest.mark.trace("NFR-001-AC-1", "TC-186")
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


@pytest.mark.trace("NFR-001-AC-1", "TC-186")
def test_fixture_b_reports_both_coexisting_record_defects_in_one_pass(
    mapper, schema_registry
):
    errors = record_errors(
        mapper, schema_registry, INVALID["nfr1-b-assessed-unassessed-no-section"]
    )
    assert signature(errors) == [("required", []), ("not", ["safetyImpact"])]


def fixture_c_reported(tmp_path: Path) -> list[str]:
    path = INVALID["nfr1-c-dangling-mismatch-empty-rationale"]
    located = diagnostics(quire_validate(path))
    bundle = bundle_validate(tmp_path, path)
    return located + [
        line
        for line in bundle.stderr.splitlines()
        if "AN-001.md" in line
        and ("[dangling-trace-reference]" in line or "mismatch" in line.lower())
    ]


@pytest.mark.trace("NFR-001-AC-1", "TC-186")
def test_fixture_c_reports_all_three_defects(tmp_path: Path):
    assert len(fixture_c_reported(tmp_path)) == 3, fixture_c_reported(tmp_path)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "the engine locates the dangling and kind-mismatched rows "
        "(BundleFinding.line, quire-rs 0.58.0) but the quire CLI's bundle "
        "output (0.42.0) prints no line for a bundle finding. Owned by "
        "quire-cli; turns green when `quire validate --okf` prints it."
    ),
)
@pytest.mark.trace("NFR-001-AC-2", "TC-187")
def test_fixture_c_every_defect_carries_a_line(tmp_path: Path):
    reported = fixture_c_reported(tmp_path)
    assert all(": line " in line for line in reported), reported


@pytest.mark.parametrize(
    "name,at_status,at_safety_impact",
    [
        ("nfr1-a-closed-no-closed-by-no-resolution", 2, 0),
        ("nfr1-b-assessed-unassessed-no-section", 1, 1),
    ],
)
@pytest.mark.trace("NFR-001-AC-1", "NFR-001-AC-2", "TC-186", "TC-187")
def test_record_layer_defects_are_located(
    name: str, at_status: int, at_safety_impact: int
):
    """An absence is reported at the `status` line (`locate_absence_at`); a
    present-but-invalid value, such as `safety_impact: unassessed`, at its own."""
    path = INVALID[name]
    lines = path.read_text().splitlines()

    def line_of(key: str) -> int:
        return next(i for i, text in enumerate(lines, 1) if text.startswith(f"{key}:"))

    found = diagnostics(quire_validate(path))

    def at(key: str) -> list[str]:
        return [d for d in found if f": line {line_of(key)}:" in d]

    assert len(at("status")) == at_status, found
    assert len(at("safety_impact")) == at_safety_impact, found
    assert len(found) == at_status + at_safety_impact, found
