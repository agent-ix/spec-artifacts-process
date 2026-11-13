"""FR-017: the ADR archetype lists the design-realization verb."""

from __future__ import annotations

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


@pytest.mark.trace("FR-017-AC-1", "TC-217")
def test_adr_may_author_realizes_requirement_but_not_unlisted_verbs() -> None:
    adr = next(
        a
        for a in load_yaml_strict(MANIFEST_PATH.read_text())["artifact_types"]
        if a["name"] == "ADR"
    )
    assert "realizes_requirement" in adr["allowed_links"]
    assert "requirement_realized_by" not in adr["allowed_links"]

    assert "disallowed-edge-type" not in validate("realizes_requirement")
    assert "disallowed-edge-type" in validate("requirement_realized_by")
    assert "disallowed-edge-type" in validate("bogus_verb")
