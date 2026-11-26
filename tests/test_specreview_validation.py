"""Behavior checks for the SpecReview extraction contract (TC-019..TC-021)."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest
from conftest import EXAMPLES_DIR, NEGATIVE_DIR, PACKAGE_ROOT

QUIRE = shutil.which("quire")


def validate(document: Path) -> subprocess.CompletedProcess[str]:
    assert QUIRE, "the `quire` CLI is required to exercise the SpecReview contract"
    return subprocess.run(
        [QUIRE, "validate", "--module", str(PACKAGE_ROOT), str(document)],
        capture_output=True,
        text=True,
        check=False,
    )


def validate_text(tmp_path: Path, text: str) -> subprocess.CompletedProcess[str]:
    document = tmp_path / "review.md"
    document.write_text(text)
    return validate(document)


@pytest.mark.trace("TC-019", "FR-002-AC-1")
def test_well_formed_spec_review_passes_and_missing_findings_fails() -> None:
    valid = validate(EXAMPLES_DIR / "spec-review.md")
    assert valid.returncode == 0, valid.stdout + valid.stderr

    missing = validate(NEGATIVE_DIR / "specreview-missing-findings.md")
    output = missing.stdout + missing.stderr
    assert missing.returncode != 0, "a SpecReview without Findings must fail"
    assert "[missing]" in output, output


@pytest.mark.trace("TC-020", "FR-002-AC-2")
def test_spec_review_severity_choices_are_enforced(tmp_path: Path) -> None:
    example = (EXAMPLES_DIR / "spec-review.md").read_text()
    assert example.count("| medium |") == 1
    for severity in ("low", "medium", "high"):
        valid = validate_text(
            tmp_path, example.replace("| medium |", f"| {severity} |")
        )
        assert valid.returncode == 0, valid.stdout + valid.stderr

    result = validate(NEGATIVE_DIR / "specreview-bad-severity.md")
    output = result.stdout + result.stderr
    assert result.returncode != 0, "critical is not an admitted Severity value"
    assert "[assert]" in output and "Severity" in output, output


@pytest.mark.trace("TC-021", "FR-002-AC-3")
def test_spec_review_finding_id_pattern_is_enforced(tmp_path: Path) -> None:
    valid = validate(EXAMPLES_DIR / "spec-review.md")
    assert valid.returncode == 0, valid.stdout + valid.stderr

    example = (EXAMPLES_DIR / "spec-review.md").read_text()
    assert example.count("FND-001") == 1
    for invalid_id in ("FND-", "fnd-1", "F-001", "FIND-001"):
        result = validate_text(tmp_path, example.replace("FND-001", invalid_id, 1))
        output = result.stdout + result.stderr
        assert result.returncode != 0, f"{invalid_id} must fail the findings id pattern"
        assert "[assert]" in output and "does not match pattern" in output, output
