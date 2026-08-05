"""FR-003 — TestMatrix `body_extraction` contract (TC-001..TC-016, TC-018).

The harness drives the real `quire validate` against this module's manifest, so
the tests assert the contract as an author experiences it rather than as a YAML
shape. `test_manifest.py` covers the manifest-data side (TC-017).

Requires the `quire` CLI on PATH; the whole module is skipped when it is
absent, so a checkout without the toolchain still runs the rest of the suite.
"""

from __future__ import annotations

import pathlib
import shutil
import subprocess

import pytest

import spec_artifacts_process as pack

FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "testmatrix"

pytestmark = pytest.mark.skipif(
    shutil.which("quire") is None,
    reason="the `quire` CLI is required to validate against the module manifest",
)


def validate(fixture: str) -> subprocess.CompletedProcess[str]:
    """Validate one fixture against this module. Returns the finished process;
    exit code 0 means the document satisfies the contract."""
    return subprocess.run(
        [
            "quire",
            "validate",
            "--module",
            str(pack.PACK_ROOT),
            str(FIXTURES / fixture),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def assert_valid(fixture: str) -> None:
    result = validate(fixture)
    assert (
        result.returncode == 0
    ), f"{fixture} must satisfy the contract\n{result.stdout}\n{result.stderr}"


def assert_invalid(fixture: str, *, reason: str, mentions: str = "") -> None:
    """Assert the fixture fails, for the documented reason. `reason` is quire's
    bracketed reason token (`missing` for an absent required extraction,
    `assert` for a satisfied locator whose assert failed)."""
    result = validate(fixture)
    output = result.stdout + result.stderr
    assert result.returncode != 0, f"{fixture} must fail the contract\n{output}"
    assert (
        f"[{reason}]" in output
    ), f"{fixture} must fail with reason `{reason}`\n{output}"
    if mentions:
        assert (
            mentions in output
        ), f"{fixture} diagnostic must mention {mentions!r}\n{output}"


# ── TC-001 / TC-016: required tables present, records extracted ──


def test_conforming_matrix_validates() -> None:
    """TC-001 (FR-003-AC-1, FR-003-AC-8): a full matrix with every coverage
    table, a mixed vocabulary, and several test-case rows validates."""
    assert_valid("conforming.md")


def test_optional_tables_omitted_still_validates() -> None:
    """TC-014 (FR-003-AC-7): the StR/US/NFR coverage tables are optional."""
    assert_valid("optional-tables-omitted.md")


def test_optional_table_with_renamed_column_fails() -> None:
    """TC-015 (FR-003-AC-7): optional means "absent is fine", not "anything
    goes" — a present optional table still has its columns asserted."""
    assert_invalid("optional-table-renamed-column.md", reason="assert")


# ── TC-002 / TC-003 / TC-016: structural drift ──


def test_missing_test_case_summary_fails() -> None:
    """TC-002 (FR-003-AC-2)."""
    assert_invalid("missing-test-case-summary.md", reason="missing")


def test_missing_functional_coverage_fails() -> None:
    """TC-003 (FR-003-AC-1)."""
    assert_invalid("missing-fr-coverage.md", reason="missing")


@pytest.mark.parametrize(
    "fixture", ["header-only-summary.md", "header-only-fr-coverage.md"]
)
def test_header_only_table_fails_min_rows(fixture: str) -> None:
    """TC-016 (FR-003-AC-1, FR-003-AC-2): a header-only table is not a table —
    both required extractions demand at least one row."""
    assert_invalid(fixture, reason="assert")


# ── TC-004 / TC-005: Type vocabulary ──


def test_type_vocabulary_permutation_validates() -> None:
    """TC-004 (FR-003-AC-3): Unit, Integration, E2E, Property all accepted."""
    assert_valid("type-vocabulary.md")


def test_type_outside_vocabulary_fails() -> None:
    """TC-005 (FR-003-AC-3): `Manual` is not a Type."""
    assert_invalid("type-invalid.md", reason="assert", mentions="Type")


# ── TC-006 / TC-007: Test ID shapes ──


def test_test_id_shapes_validate() -> None:
    """TC-006 (FR-003-AC-4): `TC-001`, `TC-INT-010`, `TC-INT-010a`."""
    assert_valid("test-id-shapes.md")


@pytest.mark.parametrize(
    "fixture",
    [
        "test-id-no-dash.md",
        "test-id-lowercase.md",
        "test-id-truncated.md",
        "test-id-wrong-prefix.md",
    ],
)
def test_malformed_test_id_fails(fixture: str) -> None:
    """TC-007 (FR-003-AC-4)."""
    assert_invalid(fixture, reason="assert")


# ── TC-008 / TC-009: Status markers ──


def test_status_marker_permutation_validates() -> None:
    """TC-008 (FR-003-AC-5): the four bare markers."""
    assert_valid("status-vocabulary.md")


@pytest.mark.parametrize("fixture", ["status-word.md", "status-decorated.md"])
def test_status_outside_vocabulary_fails(fixture: str) -> None:
    """TC-009 (FR-003-AC-5): `Done` and a decorated `✅ Complete` are both out
    — the marker vocabulary is bare markers only."""
    assert_invalid(fixture, reason="assert", mentions="Status")


# ── TC-010 / TC-011: Priority vocabulary ──


def test_priority_vocabulary_permutation_validates() -> None:
    """TC-010 (FR-003-AC-10): P0..P4."""
    assert_valid("priority-vocabulary.md")


@pytest.mark.parametrize("fixture", ["priority-invalid.md", "priority-word.md"])
def test_priority_outside_vocabulary_fails(fixture: str) -> None:
    """TC-011 (FR-003-AC-10): `P5` and `High` are both out."""
    assert_invalid(fixture, reason="assert", mentions="Priority")


# ── TC-012 / TC-013 / TC-018: Traces To tokens ──


def test_traces_to_token_permutation_validates() -> None:
    """TC-012 (FR-003-AC-6): every token kind alone and in a comma list."""
    assert_valid("traces-to-tokens.md")


@pytest.mark.parametrize(
    "fixture",
    [
        "traces-to-semicolon.md",
        "traces-to-space-before-comma.md",
        "traces-to-test-case-token.md",
        "traces-to-truncated.md",
        "traces-to-trailing-comma.md",
    ],
)
def test_malformed_traces_to_fails(fixture: str) -> None:
    """TC-013 (FR-003-AC-6)."""
    assert_invalid(fixture, reason="assert", mentions="Traces To")


def test_empty_traces_to_fails() -> None:
    """TC-018 (FR-003-AC-6): an empty cell traces to nothing, which the
    pattern rejects — a row with no trace is the drift the matrix exists to
    catch."""
    assert_invalid("traces-to-empty.md", reason="assert")


# ── TC-024: blocked on an engine capability ──


@pytest.mark.xfail(
    reason=(
        "FR-003-AC-11 / TC-024: quire-rs exposes no id-uniqueness table assert "
        "(LocatorAssert has columns/min_rows/id_pattern/choices/column_choices/"
        "column_patterns only), so a duplicate Test ID cannot be machine-"
        "enforced yet. Kept executable so the day the engine capability lands, "
        "this turns green and the xfail is removed."
    ),
    strict=True,
)
def test_duplicate_test_id_fails() -> None:
    """TC-024 (FR-003-AC-11) — ⚠️ blocked, see the xfail reason."""
    assert_invalid("duplicate-test-id.md", reason="assert")
