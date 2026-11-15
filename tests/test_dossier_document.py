"""The DossierDocument archetype and its fixtures (FR-018)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from conftest import PACKAGE_ROOT, REPO_ROOT, SKELETONS_DIR

FIXTURES = REPO_ROOT / "tests" / "fixtures" / "dossier"
VALID = sorted((FIXTURES / "valid").glob("*.md"))


def quire_validate(*paths: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            "quire",
            "validate",
            "--module",
            str(PACKAGE_ROOT),
            "--scope",
            str(FIXTURES),
            *map(str, paths),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.trace("FR-018-AC-1")
@pytest.mark.parametrize("path", VALID, ids=lambda p: p.stem)
def test_valid_fixture_validates(path: Path):
    result = quire_validate(path)
    assert result.returncode == 0, result.stderr


@pytest.mark.trace("FR-018-AC-2")
@pytest.mark.parametrize("name", ["missing-version", "empty-version"])
def test_missing_or_empty_version_fails(name: str):
    result = quire_validate(FIXTURES / "invalid" / f"{name}.md")
    assert result.returncode != 0
    assert "version" in result.stderr


@pytest.mark.trace("FR-018-AC-3")
def test_document_kind_outside_enum_fails():
    result = quire_validate(FIXTURES / "invalid" / "bad-kind.md")
    assert result.returncode != 0
    assert "document_kind" in result.stderr


@pytest.mark.trace("FR-018-AC-4")
@pytest.mark.parametrize("name", ["bad-generator", "missing-generator"])
def test_generated_by_must_be_quoin_dossier(name: str):
    result = quire_validate(FIXTURES / "invalid" / f"{name}.md")
    assert result.returncode != 0
    assert "generated_by" in result.stderr


@pytest.mark.trace("FR-018-AC-6")
def test_skeleton_validates():
    result = quire_validate(SKELETONS_DIR / "DossierDocument.md")
    assert result.returncode == 0, result.stderr
