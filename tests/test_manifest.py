"""Manifest validity + pack entrypoint tests."""

from __future__ import annotations

import json
import pathlib
import re
import shutil
import subprocess

import pytest
import yaml

import spec_artifacts_process as pack

MANIFEST_PATH = pack.MANIFEST_PATH


def test_pack_exposes_manifest_path() -> None:
    assert MANIFEST_PATH == pack.PACK_ROOT / "manifest.yaml"
    assert MANIFEST_PATH.is_file()


def test_manifest_loads() -> None:
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert manifest["manifest_version"] == "1.0.0"
    assert manifest["name"] == "spec-artifacts-process"
    assert manifest["version"]


def test_spec_review_archetype_registered_with_findings_validation() -> None:
    """SpecReview is the per-analysis review archetype: a Summary section plus a
    Findings table whose Severity column is constrained to low/medium/high
    (quire CR-010 `column_choices`)."""
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())

    names = {a["name"] for a in manifest["archetypes"]}
    assert "SpecReview" in names, "SpecReview archetype must be registered"

    sr = next(t for t in manifest["artifact_types"] if t["name"] == "SpecReview")
    assert sr["frontmatter_schema_ref"] == "schemas/spec-review-frontmatter.schema.json"

    findings = sr["body_extraction"]["yield_pattern"]["match"]["findings"]
    assert findings["from"] == "table_row"
    assert findings["under_section"] == "Findings"
    assert findings["assert"]["columns"] == ["ID", "Severity", "Summary", "Refs"]
    assert findings["assert"]["column_choices"]["Severity"] == [
        "low",
        "medium",
        "high",
    ]
    assert findings["assert"]["id_pattern"] == r"^FND-\d+$"

    schema_path = pack.PACK_ROOT / "schemas" / "spec-review-frontmatter.schema.json"
    assert schema_path.is_file()
    schema = json.loads(schema_path.read_text())
    assert schema["properties"]["type"]["const"] == "SpecReview"

    # An authoring skeleton must exist so `quoin write --types SpecReview`
    # emits the authoritative template (catalog resolves skeletons/<Name>.md).
    skeleton = pack.PACK_ROOT / "skeletons" / "SpecReview.md"
    assert skeleton.is_file()
    body = skeleton.read_text()
    assert "type: SpecReview" in body
    header = next(line for line in body.splitlines() if line.strip().startswith("| ID"))
    assert [c.strip() for c in header.strip().strip("|").split("|")] == [
        "ID",
        "Severity",
        "Summary",
        "Refs",
    ]


def test_spec_review_analysis_admits_both_review_families() -> None:
    """TC-027 (FR-002-AC-6): the `analysis` enum covers analyses *of a spec* and
    reviews of an *implementation against its spec*. A review with no fitting
    value does not become a smaller review — it becomes an unvalidated file
    outside the system, or no artifact at all (see #11)."""
    schema = json.loads(
        (pack.PACK_ROOT / "schemas" / "spec-review-frontmatter.schema.json").read_text()
    )
    analysis = schema["properties"]["analysis"]["enum"]

    spec_analyses = [
        "base",
        "failure-domain",
        "integrity",
        "dependency",
        "evidence",
        "risk-complexity",
        "scope-boundary",
        "gap-analysis",
        "ears-conformance",
    ]
    implementation_reviews = ["code-review", "spec-correctness"]

    assert analysis == spec_analyses + implementation_reviews
    assert len(analysis) == len(set(analysis)), "enum values must be unique"


def test_manifest_validates_against_fr035_schema() -> None:
    """Skip if jsonschema lacks draft 2020-12 (use CI check-jsonschema instead)."""
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        pytest.skip("jsonschema lib missing draft 2020-12 support")
    schema_path = (
        pathlib.Path(__file__).resolve().parent / "module-manifest.schema.json"
    )
    if not schema_path.exists():
        pytest.skip("FR-035 schema not bundled with tests")
    schema = json.loads(schema_path.read_text())
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    errors = list(Draft202012Validator(schema).iter_errors(manifest))
    assert not errors, [
        f"{'.'.join(str(p) for p in e.absolute_path)}: {e.message}" for e in errors
    ]


def test_testmatrix_body_extraction_contract() -> None:
    """FR-003: the TestMatrix contract is manifest data — required coverage +
    summary tables, the Test ID pattern, and the Type/Priority/Status/Traces To
    cell vocabularies. The behavioural side is
    `test_testmatrix_body_extraction.py`, which drives `quire validate`."""
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    tm = next(t for t in manifest["artifact_types"] if t["name"] == "TestMatrix")
    match = tm["body_extraction"]["yield_pattern"]["match"]

    coverage = match["functional_coverage"]
    assert coverage["from"] == "table_row"
    assert coverage["under_section"] == "Functional Requirement Coverage"
    assert coverage["required"] is True
    assert coverage["assert"]["columns"] == [
        "Functional Req",
        "Acceptance Criteria",
        "Test Cases",
        "Coverage Status",
    ]
    assert coverage["assert"]["min_rows"] == 1

    cases = match["test_cases"]
    assert cases["required"] is True
    assert cases["multiple"] is True, "one record per test-case row (FR-003-AC-8)"
    assert cases["assert"]["columns"] == [
        "Test ID",
        "Title",
        "Type",
        "Priority",
        "Traces To",
        "Status",
    ]
    assert cases["assert"]["id_column"] == "Test ID"
    # CR-019: the prefix set mirrors the declared evidence archetypes (`TC`,
    # `IT`) — not a list of test kinds, which is the `Type` column's job.
    assert (
        cases["assert"]["id_pattern"]
        == r"^(TC|IT)(-[A-Za-z0-9]+)*-\d+[A-Za-z0-9]*(-[A-Za-z0-9]+)*$"
    )
    choices = cases["assert"]["column_choices"]
    assert choices["Type"] == [
        "Unit",
        "Integration",
        "E2E",
        "Property",
        "Fuzz",
        "Benchmark",
        "Static",
        "Compile",
        "Snapshot",
        "Manual",
    ]
    assert choices["Priority"] == ["P0", "P1", "P2", "P3", "P4"]
    # CR-016: Status moved from an enum to a pattern, because the marker heads
    # the cell and the note that says *why* follows it.
    assert "Status" not in choices
    patterns = cases["assert"]["column_patterns"]
    assert patterns["Status"] == r"^(✅|⚠️|❌|🚧|⛔)(\s+.*)?$"
    assert "Traces To" in patterns

    # CR-017: the `Traces To` pattern admits two authoring shorthands the
    # FR-003-CON-1 sweep found in real matrices, and keeps rejecting a cell that
    # traces to nothing — which is exactly what a traceability matrix exists to
    # surface. (agent-ix/spec-artifacts-process#12)
    traces = re.compile(patterns["Traces To"])
    for cell in [
        "FR-001",
        "FR-001-AC-2",
        "FR-001-AC-1, FR-002-AC-2",
        "FR-012-AC-1..FR-012-AC-3",
        "FR-001 (note)",
        # continuation — the parent id is elided on following tokens
        "FR-001-AC-2, -AC-3, -AC-4",
        "FR-004-AC-4, -CON-2",
        # slash enumeration of sub-ids
        "FR-016-AC-1/2/3/6/7/8",
        "FR-005-AC-5/6/7, FR-016-AC-1/2/3, NFR-007-AC-1, US-009",
    ]:
        assert traces.match(cell), f"CR-017 should admit {cell!r}"
    for cell in ["", "—", "Future Task 13", "FR-002 error path", "-AC-1"]:
        assert not traces.match(cell), f"should stay rejected: {cell!r}"

    # The three optional coverage tables: absent is fine, present is asserted.
    for key, section in [
        ("stakeholder_coverage", "Stakeholder Requirement Coverage"),
        ("user_story_coverage", "User Story Coverage"),
        ("non_functional_coverage", "Non-Functional Requirement Coverage"),
    ]:
        assert match[key]["required"] is False
        assert match[key]["under_section"] == section
        assert match[key]["assert"]["columns"]
        assert "min_rows" not in match[key]["assert"], (
            "an optional table must not require rows — a bundle without those "
            "artifacts would have to fabricate them (FR-003-AC-7)"
        )


def test_testmatrix_contract_does_not_widen_the_manifest() -> None:
    """TC-017 (FR-003-AC-9): the contract is additive. The TestMatrix
    frontmatter schema is untouched, and no other archetype gained or lost a
    `body_extraction`."""
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())

    schema = json.loads(
        (pack.PACK_ROOT / "schemas" / "testmatrix-frontmatter.schema.json").read_text()
    )
    assert schema["required"] == ["id", "title", "type"]
    assert schema["properties"]["type"]["const"] == "TestMatrix"
    assert set(schema["properties"]) == {
        "id",
        "title",
        "type",
        "object",
        "relationships",
    }

    with_contract = {
        t["name"] for t in manifest["artifact_types"] if "body_extraction" in t
    }
    assert with_contract == {"Feedback", "SpecReview", "TestMatrix"}, (
        "FR-003 adds the TestMatrix contract only; Feedback and SpecReview keep "
        "the body_extraction they already had, and nothing else gains one"
    )

    tm = next(t for t in manifest["artifact_types"] if t["name"] == "TestMatrix")
    assert tm["frontmatter_schema_ref"] == "schemas/testmatrix-frontmatter.schema.json"
    assert tm["allowed_links"] == ["covers", "references"]
    assert tm["defaults"]["id_pattern"] == "TestMatrix-{next:03d}"


def test_column_vocabularies_have_one_source() -> None:
    """CR-015/CR-016: the traceability model owns the column vocabularies, and
    the body_extraction contract must not drift from it. Until quire grows a
    `from_vocabulary` reference, the contract restates the list and this test is
    what keeps the two honest."""
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    traceability = manifest["traceability"]
    tm = next(t for t in manifest["artifact_types"] if t["name"] == "TestMatrix")
    cases = tm["body_extraction"]["yield_pattern"]["match"]["test_cases"]

    assert (
        cases["assert"]["column_choices"]["Type"]
        == traceability["vocabularies"]["test_type"]
    ), "the Type enum must equal the declared test_type vocabulary"

    status = traceability["status"]
    assert status["column"] == "Status"
    declared_markers = (
        status["complete"] + status["pending"] + status["failed"] + status["retired"]
    )
    pattern = cases["assert"]["column_patterns"]["Status"]
    for marker in declared_markers:
        assert marker in pattern, f"{marker} is classed but not admitted by the pattern"


def test_repo_test_matrix_self_validates() -> None:
    """Gate (contract green): this repo's own `spec/tests.md` satisfies the
    candidate contract — the module does not ship a shape it violates."""
    if shutil.which("quire") is None:
        pytest.skip("the `quire` CLI is required for self-validation")
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    result = subprocess.run(
        [
            "quire",
            "validate",
            "--module",
            str(pack.PACK_ROOT),
            str(repo_root / "spec" / "tests.md"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
