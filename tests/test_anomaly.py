"""The Anomaly archetype, its record schema and its fixtures.

Requirements FR-014, FR-015, FR-016 and NFR-001 (user story US-003).

Three layers are exercised, each through the real artifact it ships:

* **document** — `quire validate` against this module's manifest (vocabularies,
  required sections, table shape);
* **extracted record** — the YAML record `yield_pattern.match` extracts, validated
  by the engine against `schemas/AnomalyFields.json` (`record_validation`): the
  status-conditional and row checks the `assert` facet cannot express, reported
  by `quire validate` as `semantic.record-invalid`, an absence at the `status`
  line and a present value at its own;
* **mapped record** — the document mapped by `mappings.yaml` and validated against
  the emitted `Anomaly.json` (the same rules over the camelCase record);
* **reference** — whether an assessment or fix-verification `Target` resolves, and
  to what kind. The module owns none of that text: it is the engine's reference
  diagnostic.

The fixtures live under `tests/fixtures/anomaly/` and are read in place by
quoin's tests; quoin holds no copy.
"""

from __future__ import annotations

import importlib.util
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
VALID_BY_NAME = {p.stem: p for p in VALID}

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


def line_of(path: Path, key: str) -> int:
    """The line of a frontmatter key."""
    return next(
        i
        for i, text in enumerate(path.read_text().splitlines(), 1)
        if text.startswith(f"{key}:")
    )


def table_line(path: Path) -> int:
    """The line of the assessment table header."""
    return next(
        i
        for i, text in enumerate(path.read_text().splitlines(), 1)
        if text.startswith("| Kind")
    )


def heading_line(path: Path, heading: str) -> int:
    """The line of a level-2 heading."""
    return next(
        i
        for i, text in enumerate(path.read_text().splitlines(), 1)
        if text == f"## {heading}"
    )


def row_line(path: Path, prefix: str) -> int:
    """The line of the first table row that starts with `prefix`."""
    return next(
        i
        for i, text in enumerate(path.read_text().splitlines(), 1)
        if text.startswith(prefix)
    )


def keys_named(node, name: str) -> list:
    """Every value stored under the key `name`, anywhere in a JSON-like tree."""
    found = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == name:
                found.append(value)
            found += keys_named(value, name)
    elif isinstance(node, list):
        for item in node:
            found += keys_named(item, name)
    return found


def variant(tmp_path: Path, source: Path, old: str, new: str) -> Path:
    """A copy of a fixture with one substring replaced, as `AN-001.md` in `tmp_path`."""
    text = source.read_text()
    assert old in text, f"{old!r} not in {source.name}"
    path = tmp_path / "AN-001.md"
    path.write_text(text.replace(old, new, 1))
    return path


def record_findings(path: Path) -> list[str]:
    """The `semantic.record-invalid` findings `quire validate` reports on a document."""
    return [
        d for d in diagnostics(quire_validate(path)) if "semantic.record-invalid" in d
    ]


def finding_lines(findings: list[str]) -> list[int]:
    return [int(f.split(": line ", 1)[1].split(":", 1)[0]) for f in findings]


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
    record |= {
        "status": "closed",
        "resolution": "fixed",
        "closedBy": value,
        "verification": [
            {"kind": "Test", "target": "TC-001", "rationale": "Passes.", "line": 1}
        ],
    }
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
    for key in (
        "status",
        "resolution",
        "closedBy",
        "severity",
        "safetyImpact",
        "assessment",
        "verification",
        "releaseRationale",
    ):
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


def installed_module(package: str) -> Path:
    """The module tree of an installed Python package (a dev dependency)."""
    spec = importlib.util.find_spec(package)
    assert spec is not None and spec.origin, (
        f"{package} is not installed: it is a dev dependency of this repo "
        "(`poetry install`), not something to install into the home directory"
    )
    return Path(spec.origin).parent


def bundle_validate(tmp_path: Path, anomaly: Path) -> subprocess.CompletedProcess:
    """Validate the fixture corpus plus one anomaly as a bundle.

    Reference resolution (quire-rs FR-049) runs over the bundle, so the anomaly
    is placed in a copy of the corpus. `--okf` is the posture that reports the
    finding as a warning, so a clean exit does not mean no finding: callers read
    the `[dangling-trace-reference]` lines.
    """
    modules = [
        installed_module("spec_artifacts_iso"),
        installed_module("spec_objects_safety"),
    ]
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
        # FR-014 severity, FR-015 fix verification, FR-016 release rationale
        "assessed-no-severity",
        "severity-outside-high",
        "resolved-fixed-no-verification",
        "verification-dangling-criterion",
        "rationale-closed-fixed",
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


@pytest.mark.trace("NFR-001-AC-1", "NFR-001-AC-2", "TC-186", "TC-187")
def test_fixture_c_empty_rationale_is_reported_once_with_its_line():
    path = INVALID["nfr1-c-dangling-mismatch-empty-rationale"]
    found = diagnostics(quire_validate(path))
    assert len(found) == 1, found
    assert "Rationale" in found[0]
    row = next(
        i
        for i, text in enumerate(path.read_text().splitlines(), 1)
        if text.endswith("| Affects |  |")
    )
    assert f": line {row}:" in found[0]


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


# -- extracted-record layer (`record_validation`, AnomalyFields.json) ---------


def anomaly_type(manifest) -> dict:
    return next(a for a in manifest["artifact_types"] if a["name"] == "Anomaly")


@pytest.mark.trace("FR-014-AC-9", "TC-188")
def test_the_anomaly_archetype_declares_record_validation(manifest):
    assert anomaly_type(manifest)["record_validation"] == {
        "schema": "schemas/AnomalyFields.json",
        "locate_absence_at": "status",
    }
    assert "locate_absence_at" in anomaly_type(manifest)["record_validation"]
    assert (
        "status" in anomaly_type(manifest)["body_extraction"]["yield_pattern"]["match"]
    )


@pytest.mark.trace("FR-014-AC-10", "TC-189")
def test_the_closed_by_locator_is_optional_frontmatter(manifest):
    assert locator(manifest, "closed_by") == {
        "from": "frontmatter_field",
        "path": ["closed_by"],
        "required": False,
    }


@pytest.mark.trace("FR-014-AC-11", "FR-009-AC-14", "TC-190", "TC-193")
def test_the_record_schema_ships_and_the_generator_leaves_it_alone():
    schema = json.loads((SCHEMAS_DIR / "AnomalyFields.json").read_text())
    assert schema["$id"].endswith("/spec-artifacts-process/AnomalyFields.json")
    assert (
        "spec_artifacts_process/schemas/**/*.json"
        in (REPO_ROOT / "pyproject.toml").read_text()
    )
    probe = (
        'import("./projection.mjs").then(m => console.log(JSON.stringify('
        '["AnomalyFields.json", "Anomaly.json", "Stale.json"].map(m.isProjection))))'
    )
    result = subprocess.run(
        ["node", "-e", probe],
        cwd=PACKAGE_ROOT / "semantic" / "scripts",
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == [False, True, True]


@pytest.mark.parametrize(
    "name,at",
    [
        ("closed-no-closed-by", "status"),
        ("closed-no-resolution", "status"),
        ("resolved-no-resolution", "status"),
        ("identified-with-resolution", "status"),
        ("assessed-with-resolution", "status"),
        ("identified-with-closed-by", "status"),
        ("assessed-with-closed-by", "status"),
        ("resolved-not-fixed", "resolution"),
        ("closed-closed-by-tbd", "closed_by"),
        ("closed-closed-by-unknown-lower", "closed_by"),
        ("closed-closed-by-na", "closed_by"),
        ("closed-closed-by-none-upper", "closed_by"),
        ("closed-closed-by-dash", "closed_by"),
        ("closed-closed-by-empty", "closed_by"),
    ],
)
@pytest.mark.trace(
    "FR-014-AC-4", "FR-014-AC-5", "FR-014-AC-6", "TC-171", "TC-172", "TC-173"
)
def test_quire_validate_reports_each_status_conditional_defect_once_located(
    name: str, at: str
):
    path = INVALID[name]
    found = record_findings(path)
    assert finding_lines(found) == [line_of(path, at)], found


@pytest.mark.parametrize(
    "name",
    [
        "closed-no-section",
        "resolved-no-section",
        "identified-impacting-no-section",
        "identified-none-no-section",
    ],
)
@pytest.mark.trace("FR-015-AC-3", "FR-015-AC-7", "TC-178", "TC-182")
def test_quire_validate_reports_a_missing_section_at_the_status_line(name: str):
    path = INVALID[name]
    assert finding_lines(record_findings(path)) == [line_of(path, "status")]


@pytest.mark.parametrize(
    "name", ["closed-unassessed", "resolved-unassessed", "assessed-unassessed"]
)
@pytest.mark.trace("FR-015-AC-3", "TC-178")
def test_quire_validate_reports_unassessed_at_the_safety_impact_line(name: str):
    path = INVALID[name]
    assert finding_lines(record_findings(path)) == [line_of(path, "safety_impact")]


@pytest.mark.parametrize(
    "name,count",
    [
        ("impacting-only-unaffected", 1),
        ("impacting-only-impact-none", 1),
        ("impacting-row-impact-none", 2),
        ("none-with-affects", 1),
        ("none-with-target", 1),
        ("none-with-hazard-row", 2),
    ],
)
@pytest.mark.trace("FR-015-AC-7", "TC-182")
def test_quire_validate_reports_the_assessment_row_rules_inside_the_table(
    name: str, count: int
):
    path = INVALID[name]
    lines = finding_lines(record_findings(path))
    assert len(lines) == count, lines
    assert all(line > table_line(path) for line in lines), lines


@pytest.mark.parametrize("name", ["none", "impacting-all-targets", "two-hazards"])
@pytest.mark.trace("FR-015-AC-7", "TC-182")
def test_quire_validate_accepts_the_valid_assessment_shapes(name: str):
    assert record_findings(FIXTURES / "valid" / f"{name}.md") == []


@pytest.mark.trace("FR-014-AC-13", "TC-192")
def test_a_mistyped_status_is_one_defect_not_three(tmp_path: Path):
    source = VALID_BY_NAME["closed-fixed"]
    path = tmp_path / "AN-001.md"
    path.write_text(source.read_text().replace("status: closed", "status: open"))
    found = diagnostics(quire_validate(path, scope=tmp_path))
    assert len(found) == 1, found
    assert "[assert]" in found[0] and "status" in found[0]
    assert finding_lines(found) == [line_of(path, "status")]


@pytest.mark.trace("FR-014-AC-12", "TC-191")
def test_a_closed_anomaly_missing_both_fields_is_reported_once_per_field():
    path = INVALID["nfr1-a-closed-no-closed-by-no-resolution"]
    found = record_findings(path)
    assert sorted(finding_lines(found)) == [line_of(path, "status")] * 2, found
    assert any("closed_by" in f for f in found)
    assert any("resolution" in f for f in found)


# -- FR-014: severity (PLAT-1581) ----------------------------------------------


@pytest.mark.trace("FR-014-AC-14", "TC-195")
def test_the_severity_locator_is_optional_with_the_three_member_vocabulary(manifest):
    assert locator(manifest, "severity") == {
        "from": "frontmatter_field",
        "path": ["severity"],
        "required": False,
        "assert": {"choices": ["minor", "major", "critical"]},
    }
    fields = json.loads((SCHEMAS_DIR / "AnomalyFields.json").read_text())
    assert fields["properties"]["severity"] == {"enum": ["minor", "major", "critical"]}
    assert keys_named(anomaly_type(manifest), "default") == []
    assert keys_named(fields, "default") == []


@pytest.mark.parametrize("status", ["assessed", "resolved", "closed"])
@pytest.mark.trace("FR-014-AC-15", "TC-196")
def test_assessed_or_later_without_severity_fails_at_the_status_line(
    mapper, schema_registry, status: str
):
    path = INVALID[f"{status}-no-severity"]
    found = record_findings(path)
    assert finding_lines(found) == [line_of(path, "status")], found
    assert "severity" in found[0]
    errors = record_errors(mapper, schema_registry, path)
    assert signature(errors) == [("required", [])]
    assert "'severity'" in errors[0].message


@pytest.mark.trace("FR-014-AC-15", "TC-196")
def test_an_identified_anomaly_may_omit_severity_or_carry_one():
    omitted = VALID_BY_NAME["identified"]
    assert "severity" not in omitted.read_text()
    assert quire_validate(omitted).returncode == 0
    carried = VALID_BY_NAME["identified-severity"]
    assert "severity: minor" in carried.read_text()
    assert quire_validate(carried).returncode == 0


@pytest.mark.parametrize(
    "name",
    ["severity-outside-high", "severity-outside-capitalised", "severity-outside-empty"],
)
@pytest.mark.trace("FR-014-AC-16", "TC-197")
def test_a_severity_outside_the_vocabulary_is_one_finding_at_the_severity_line(
    mapper, schema_registry, name: str
):
    path = INVALID[name]
    found = diagnostics(quire_validate(path))
    assert len(found) == 1, found
    assert finding_lines(found) == [line_of(path, "severity")]
    assert "severity" in found[0]
    assert ("enum", ["severity"]) in signature(
        record_errors(mapper, schema_registry, path)
    )


@pytest.mark.trace("FR-014-AC-17", "TC-198")
def test_severity_is_not_computed_from_another_field(tmp_path: Path, mapper, mappings):
    source = VALID_BY_NAME["assessed"]
    table = source.read_text().index("| Requirement | FR-001 |")
    # `safety_impact` differs (and, as the rules require, the rows with it)
    by_impact = tmp_path / "AN-001.md"
    by_impact.write_text(
        source.read_text()[:table].replace("impacting", "none")
        + "| None | - | None | Cosmetic message only; no safety function involved. |\n"
    )
    # the assessment rows differ, `safety_impact` does not
    by_rows = VALID_BY_NAME["two-hazards"]
    assert "safety_impact: impacting" in by_rows.read_text()
    for other in (by_impact, by_rows):
        assert quire_validate(other, scope=other.parent).returncode == 0
    for path in (source, by_impact, by_rows):
        assert mapper.build("Anomaly", path.read_text(), "x")["severity"] == "major"
    # and no rule sets severity: the schemas only ever require it
    for name in ("AnomalyFields.json", "Anomaly.json"):
        schema = json.loads((SCHEMAS_DIR / name).read_text())
        for rule in schema["allOf"]:
            assert "severity" not in rule.get("then", {}).get("properties", {})
    assert mappings["models"]["Anomaly"]["properties"]["severity"] == {
        "kind": "frontmatter",
        "path": ["severity"],
    }


# -- FR-015: fix verification (PLAT-1583) --------------------------------------


def fix_verification_reference(manifest) -> dict:
    return next(
        t
        for t in manifest["traceability"]["document_references"]
        if t["name"] == "anomaly-fix-verification"
    )


@pytest.mark.trace("FR-015-AC-11", "TC-199")
def test_the_manifest_declares_the_fix_verification_table_and_its_reference(manifest):
    assert locator(manifest, "fix_verification") == {
        "from": "table_row",
        "under_section": "Fix Verification",
        "required": False,
        "multiple": True,
        "assert": {
            "columns": ["Kind", "Target", "Rationale"],
            "min_rows": 1,
            "column_choices": {"Kind": ["Criterion", "Test"]},
            "column_patterns": {"Target": "^[A-Za-z0-9]", "Rationale": "\\S"},
        },
    }
    reference = fix_verification_reference(manifest)
    assert reference["archetype"] == "Anomaly"
    assert reference["section"] == "Fix Verification"
    assert reference["column"] == "Target"
    assert reference["kind_column"] == "Kind"
    assert sorted(reference["targets"]) == sorted(
        [
            "acceptance-criterion",
            "nfr-acceptance-criterion",
            "test-case",
            "requirement-document",
            "nfr-document",
            "hazard-document",
        ]
    )
    assert reference["kind_targets"] == {
        "Criterion": ["acceptance-criterion", "nfr-acceptance-criterion"],
        "Test": ["test-case"],
    }


@pytest.mark.parametrize("status", ["resolved", "closed"])
@pytest.mark.trace("FR-015-AC-12", "TC-200")
def test_a_fixed_anomaly_without_a_fix_verification_fails_at_the_status_line(
    mapper, schema_registry, status: str
):
    path = INVALID[f"{status}-fixed-no-verification"]
    found = record_findings(path)
    assert finding_lines(found) == [line_of(path, "status")], found
    assert "fix_verification" in found[0]
    errors = record_errors(mapper, schema_registry, path)
    assert signature(errors) == [("required", [])]
    assert "'verification'" in errors[0].message


@pytest.mark.parametrize(
    "name", ["closed-not-a-defect", "closed-duplicate", "closed-wont-fix"]
)
@pytest.mark.trace("FR-015-AC-12", "TC-200")
def test_a_closed_anomaly_that_is_not_fixed_needs_no_fix_verification(name: str):
    path = VALID_BY_NAME[name]
    assert "Fix Verification" not in path.read_text()
    assert quire_validate(path).returncode == 0


@pytest.mark.parametrize(
    "name",
    [
        "resolved-fixed",
        "closed-fixed",
        "closed-fixed-test-only",
        "closed-fixed-criterion-only",
    ],
)
@pytest.mark.trace("FR-015-AC-13", "TC-201")
def test_a_fixed_anomaly_linking_a_criterion_and_a_test_validates(
    tmp_path: Path, mapper, schema_registry, name: str
):
    path = VALID_BY_NAME[name]
    result = bundle_validate(tmp_path, path)
    assert result.returncode == 0, result.stderr
    assert dangling_findings(result) == [], result.stderr
    assert reference_findings(result, "reference-kind-mismatch") == [], result.stderr
    assert record_errors(mapper, schema_registry, path) == []


@pytest.mark.parametrize(
    "name,target,kind",
    [
        ("verification-dangling-criterion", "FR-001-AC-99", "Criterion"),
        ("verification-dangling-test", "TC-999", "Test"),
    ],
)
@pytest.mark.trace("FR-015-AC-14", "TC-202")
def test_a_dangling_verification_target_names_the_id_and_its_row(
    tmp_path: Path, name: str, target: str, kind: str
):
    found = dangling_findings(bundle_validate(tmp_path, INVALID[name]))
    assert len(found) == 1, found
    assert f"'{target}'" in found[0]
    assert f"(row '{kind}')" in found[0]


@pytest.mark.parametrize(
    "name,target,kind",
    [
        pytest.param(
            "verification-criterion-names-requirement",
            "FR-001",
            "Criterion",
            marks=pytest.mark.xfail(
                strict=True,
                reason=(
                    "engine (quire-rs FR-049, engine 0.58/0.59): the id of a "
                    "requirement document resolves under every target bound to "
                    "its archetype, `acceptance-criterion` included, so a "
                    "`Criterion` row naming `FR-001` raises no kind mismatch. "
                    "The manifest declares exactly the targets FR-015-AC-11 "
                    "names; turns green when the engine types document ids."
                ),
            ),
        ),
        ("verification-criterion-names-hazard", "HAZ-001", "Criterion"),
        ("verification-test-names-criterion", "FR-001-AC-1", "Test"),
    ],
)
@pytest.mark.trace("FR-015-AC-15", "TC-203")
def test_a_verification_target_of_the_wrong_kind_is_a_kind_mismatch(
    tmp_path: Path, name: str, target: str, kind: str
):
    result = bundle_validate(tmp_path, INVALID[name])
    found = reference_findings(result, "reference-kind-mismatch")
    assert len(found) == 1, found
    assert f"'{target}'" in found[0]
    assert f"(row '{kind}')" in found[0]
    assert dangling_findings(result) == []


@pytest.mark.parametrize(
    "name,message,row",
    [
        ("verification-empty-rationale", "Rationale", "| Test |"),
        ("verification-kind-outside", "Kind", "| Review |"),
    ],
)
@pytest.mark.trace("FR-015-AC-16", "TC-204")
def test_a_verification_row_with_no_rationale_or_a_foreign_kind_fails_at_the_row(
    name: str, message: str, row: str
):
    path = INVALID[name]
    found = diagnostics(quire_validate(path))
    assert len(found) == 1, found
    assert message in found[0]
    assert finding_lines(found) == [row_line(path, row)]


@pytest.mark.trace("FR-015-AC-17", "TC-205")
def test_verification_entries_carry_kind_target_and_rationale_as_authored(mapper):
    path = VALID_BY_NAME["closed-fixed"]
    rows = mapper.build("Anomaly", path.read_text(), path.name)["verification"]
    assert [(r["kind"], r["target"], r["rationale"]) for r in rows] == [
        (
            "Criterion",
            "FR-001-AC-1",
            "The criterion now rejects a mismatching checksum.",
        ),
        (
            "Test",
            "TC-001",
            "The regression test fails without the fix and passes with it.",
        ),
    ]
    assert (
        mapper.build("Anomaly", VALID_BY_NAME["assessed"].read_text(), "x").get(
            "verification"
        )
        is None
    )


@pytest.mark.parametrize(
    "name", ["verification-target-dash", "verification-target-empty"]
)
@pytest.mark.trace("FR-015-AC-19", "TC-206")
def test_a_verification_row_with_no_id_token_fails_at_the_row(name: str):
    path = INVALID[name]
    found = diagnostics(quire_validate(path))
    assert len(found) == 1, found
    assert "Target" in found[0]
    assert finding_lines(found) == [row_line(path, "| Test |")]


# -- FR-016: release rationale (PLAT-1584) -------------------------------------

RATIONALE_PLACEHOLDERS = [*PLACEHOLDERS, "Tbd", "UNKNOWN", "N/a"]
RATIONALE_PAIRS = ["identified", "assessed", "resolved"]


@pytest.mark.parametrize("status", RATIONALE_PAIRS)
@pytest.mark.trace("FR-016-AC-1", "TC-207")
def test_an_impacting_anomaly_validates_with_and_without_the_release_rationale(
    mapper, schema_registry, status: str
):
    for name in (f"rationale-{status}-with", f"rationale-{status}-without"):
        path = VALID_BY_NAME[name]
        result = quire_validate(path)
        assert result.returncode == 0, result.stderr
        assert diagnostics(result) == []
        assert record_errors(mapper, schema_registry, path) == []
    with_section = VALID_BY_NAME[f"rationale-{status}-with"].read_text()
    assert "safety_impact: impacting" in with_section
    assert "## Release Rationale" in with_section


@pytest.mark.parametrize("resolution", ["fixed", "duplicate", "not-a-defect"])
@pytest.mark.trace("FR-016-AC-2", "TC-208")
def test_a_closed_anomaly_that_was_not_shipped_unfixed_refuses_the_section(
    mapper, schema_registry, resolution: str
):
    path = INVALID[f"rationale-closed-{resolution}"]
    found = record_findings(path)
    assert finding_lines(found) == [heading_line(path, "Release Rationale")], found
    assert "release_rationale_section" in found[0]
    assert diagnostics(quire_validate(path)) == found
    # the emitted schema states the same rule on the mapped record
    emitted = json.loads((SCHEMAS_DIR / "Anomaly.json").read_text())
    rule = next(
        i for i, r in enumerate(emitted["allOf"]) if "releaseRationale" in json.dumps(r)
    )
    errors = record_errors(mapper, schema_registry, path)
    assert [(e.validator, rule_index(e)) for e in errors] == [("not", rule)]


@pytest.mark.trace("FR-016-AC-2", "TC-208")
def test_a_closed_wont_fix_anomaly_with_a_closer_may_carry_the_section(
    mapper, schema_registry
):
    path = VALID_BY_NAME["closed-wont-fix-rationale"]
    assert quire_validate(path).returncode == 0
    assert record_errors(mapper, schema_registry, path) == []
    text = path.read_text()
    closer = frontmatter(text)["closed_by"]
    authors = [
        row.split("|")[1].strip()
        for row in text.split("## Release Rationale", 1)[1].splitlines()
        if row.startswith("|") and not row.startswith(("| Author", "|--"))
    ]
    assert authors and closer not in authors


@pytest.mark.parametrize(
    "name,at",
    [
        ("rationale-closed-no-resolution", "status"),
        ("rationale-closed-bad-resolution", "resolution"),
    ],
)
@pytest.mark.trace("FR-016-AC-2", "TC-208")
def test_a_closed_anomaly_with_no_usable_resolution_yields_only_the_fr014_finding(
    name: str, at: str
):
    path = INVALID[name]
    found = diagnostics(quire_validate(path))
    assert finding_lines(found) == [line_of(path, at)], found
    assert all("release_rationale" not in f for f in found)


def rationale_row_variant(tmp_path: Path, author: str, rationale: str) -> Path:
    """The assessed-with-section fixture with its one row's cells replaced."""
    source = VALID_BY_NAME["rationale-assessed-with"]
    row = next(
        r for r in source.read_text().splitlines() if r.startswith("| Morgan Reyes |")
    )
    return variant(tmp_path, source, row, f"| {author} | {rationale} |")


@pytest.mark.parametrize("value", RATIONALE_PLACEHOLDERS)
@pytest.mark.trace("FR-016-AC-3", "TC-209")
def test_a_placeholder_or_empty_author_fails_at_the_row_and_a_name_passes(
    tmp_path: Path, value: str
):
    path = rationale_row_variant(tmp_path, value, "A written reason.")
    found = diagnostics(quire_validate(path, scope=tmp_path))
    assert finding_lines(found) == [row_line(path, f"| {value} |")], found
    named = rationale_row_variant(tmp_path, f"{value}x", "A written reason.")
    assert quire_validate(named, scope=tmp_path).returncode == 0


@pytest.mark.parametrize("value", RATIONALE_PLACEHOLDERS)
@pytest.mark.trace("FR-016-AC-4", "TC-210")
def test_a_placeholder_or_empty_rationale_fails_at_the_row_and_text_passes(
    tmp_path: Path, value: str
):
    path = rationale_row_variant(tmp_path, "Morgan Reyes", value)
    found = diagnostics(quire_validate(path, scope=tmp_path))
    assert finding_lines(found) == [row_line(path, "| Morgan Reyes")], found
    texted = rationale_row_variant(tmp_path, "Morgan Reyes", f"{value} x")
    assert quire_validate(texted, scope=tmp_path).returncode == 0


@pytest.mark.parametrize(
    "name", ["rationale-author-empty", "rationale-author-placeholder"]
)
@pytest.mark.trace("FR-016-AC-3", "TC-209")
def test_the_author_fixtures_fail_at_the_row(name: str):
    path = INVALID[name]
    assert finding_lines(diagnostics(quire_validate(path))) == [
        row_line(path, "| TBD |" if "placeholder" in name else "|  |")
    ]


@pytest.mark.parametrize(
    "name", ["rationale-rationale-empty", "rationale-rationale-placeholder"]
)
@pytest.mark.trace("FR-016-AC-4", "TC-210")
def test_the_rationale_fixtures_fail_at_the_row(name: str):
    path = INVALID[name]
    assert finding_lines(diagnostics(quire_validate(path))) == [
        row_line(path, "| Morgan Reyes |")
    ]


@pytest.mark.parametrize("name", ["rationale-bad-headers", "rationale-no-rows"])
@pytest.mark.trace("FR-016-AC-5", "TC-211")
def test_a_section_with_other_headers_or_no_row_fails_at_the_table(name: str):
    path = INVALID[name]
    found = diagnostics(quire_validate(path))
    assert found, "the section must fail validation"
    assert set(finding_lines(found)) == {heading_line(path, "Release Rationale")}, found
    assert all("release_rationale" in f for f in found)


@pytest.mark.trace(
    "NFR-001-AC-1", "NFR-001-AC-2", "FR-016-AC-6", "TC-186", "TC-187", "TC-212"
)
def test_fixture_d_reports_the_section_the_author_and_the_rationale_in_one_run():
    path = INVALID["nfr1-d-closed-fixed-rationale-placeholder-author-empty-rationale"]
    found = diagnostics(quire_validate(path))
    assert len(found) == 3, found
    by_line = {}
    for f in found:
        by_line.setdefault(finding_lines([f])[0], []).append(f)
    heading, row = heading_line(path, "Release Rationale"), row_line(path, "| TBD |")
    assert sorted(by_line) == [heading, row]
    assert (
        len(by_line[heading]) == 1
        and "release_rationale_section" in by_line[heading][0]
    )
    assert len(by_line[row]) == 2
    assert sum("/allOf/0/not" in f for f in by_line[row]) == 1  # the author
    assert sum("/allOf/1/not" in f for f in by_line[row]) == 1  # the rationale


@pytest.mark.trace("FR-016-AC-7", "TC-213")
def test_the_mapping_and_the_emitted_schema_carry_the_release_rationale(
    mapper, mappings, schema_registry
):
    entry = mappings["models"]["Anomaly"]["properties"]["releaseRationale"]
    assert entry["kind"] == "typed-table" and entry["heading"] == "Release Rationale"
    assert entry["fields"] == {
        "Author": {"property": "author", "parse": "text"},
        "Rationale": {"property": "rationale", "parse": "text"},
    }
    with_section = VALID_BY_NAME["rationale-assessed-with"]
    rows = mapper.build("Anomaly", with_section.read_text(), "x")["releaseRationale"]
    assert [(r["author"], r["rationale"].startswith("The checksum")) for r in rows] == [
        ("Morgan Reyes", True)
    ]
    without = VALID_BY_NAME["rationale-assessed-without"]
    assert "releaseRationale" not in mapper.build("Anomaly", without.read_text(), "x")
    validator = schema_registry("Anomaly")
    assert (
        "releaseRationale"
        in json.loads((SCHEMAS_DIR / "Anomaly.json").read_text())["properties"]
    )
    record = mapper.build("Anomaly", with_section.read_text(), "x")
    for author, rationale in [
        ("TBD", "Reason."),
        ("", "Reason."),
        ("Morgan", "n/a"),
        ("Morgan", ""),
    ]:
        bad = record | {
            "releaseRationale": [{**rows[0], "author": author, "rationale": rationale}]
        }
        assert any(
            list(e.absolute_path)[:1] == ["releaseRationale"]
            for e in validator.iter_errors(bad)
        ), (author, rationale)
    closed = mapper.build("Anomaly", INVALID["rationale-closed-fixed"].read_text(), "x")
    assert any(
        e.validator == "not" for e in validator.iter_errors(closed)
    ), "a releaseRationale on a closed `fixed` anomaly is rejected"


@pytest.mark.trace("FR-016-AC-8", "FR-014-AC-14", "TC-214")
def test_the_skeleton_has_no_release_rationale_and_nothing_defaults_or_computes_it(
    manifest, mappings
):
    skeleton = (SKELETONS_DIR / "Anomaly.md").read_text()
    assert not any(
        line.startswith("## Release") for line in skeleton.splitlines()
    ), "the skeleton carries no Release Rationale section"
    fields = json.loads((SCHEMAS_DIR / "AnomalyFields.json").read_text())
    emitted = json.loads((SCHEMAS_DIR / "Anomaly.json").read_text())
    for tree in (
        anomaly_type(manifest),
        mappings["models"]["Anomaly"],
        fields,
        emitted,
        json.loads((SCHEMAS_DIR / "ReleaseRationaleRow.json").read_text()),
    ):
        assert keys_named(tree, "default") == []
    for rule in fields["allOf"]:
        assert "release_rationale" not in rule.get("then", {}).get(
            "properties", {}
        ) or (rule["then"]["properties"].get("release_rationale_section") is False)


@pytest.mark.parametrize("status", RATIONALE_PAIRS)
@pytest.mark.trace("FR-016-AC-10", "TC-215")
def test_the_section_changes_no_other_finding(tmp_path: Path, status: str):
    """Two documents identical but for the section report the same other findings:
    each carries one unrelated defect (a `closed_by` on an open anomaly)."""

    def report(name: str) -> list[tuple[int, str]]:
        source = VALID_BY_NAME[name]
        path = variant(
            tmp_path,
            source,
            "type: Anomaly\n",
            'type: Anomaly\nclosed_by: "Dana Lee"\n',
        )
        found = diagnostics(quire_validate(path, scope=tmp_path))
        # the line and the schema rule; the message echoes the whole record
        return [
            (finding_lines([f])[0], f.split(" (/", 1)[1].split("):", 1)[0])
            for f in found
        ]

    assert report(f"rationale-{status}-without") == report(f"rationale-{status}-with")
    assert len(report(f"rationale-{status}-with")) == 1


@pytest.mark.trace("FR-016-AC-11", "TC-216")
def test_the_release_rationale_locator_is_optional_and_named_in_the_record_schema(
    manifest,
):
    found = locator(manifest, "release_rationale")
    assert found["from"] == "table_row"
    assert found["under_section"] == "Release Rationale"
    assert found["required"] is False
    assert found["assert"]["columns"] == ["Author", "Rationale"]
    assert found["assert"]["min_rows"] == 1
    fields = json.loads((SCHEMAS_DIR / "AnomalyFields.json").read_text())
    assert "release_rationale" in fields["properties"]


@pytest.mark.trace("FR-014-AC-18", "FR-015-AC-18", "FR-016-AC-9")
def test_the_type_holds_no_who_when_or_verdict_field():
    emitted = json.loads((SCHEMAS_DIR / "Anomaly.json").read_text())
    assert sorted(emitted["properties"]) == sorted(
        [
            "id",
            "title",
            "type",
            "status",
            "resolution",
            "closedBy",
            "severity",
            "safetyImpact",
            "object",
            "relationships",
            "provenance",
            "description",
            "assessment",
            "verification",
            "releaseRationale",
        ]
    )
    for row in ("VerificationRow", "ReleaseRationaleRow"):
        schema = json.loads((SCHEMAS_DIR / f"{row}.json").read_text())
        assert sorted(schema["properties"]) == sorted(
            ["kind", "target", "rationale", "line"]
            if row == "VerificationRow"
            else ["author", "rationale", "line"]
        )
