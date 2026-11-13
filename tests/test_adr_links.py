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


def adr_links() -> list[str]:
    manifest = load_yaml_strict(MANIFEST_PATH.read_text())
    return next(a for a in manifest["artifact_types"] if a["name"] == "ADR")[
        "allowed_links"
    ]


@pytest.mark.trace("FR-017-AC-1", "TC-217")
def test_adr_may_author_realizes_requirement() -> None:
    assert "realizes_requirement" in adr_links()
    assert "disallowed-edge-type" not in validate("realizes_requirement")


@pytest.mark.trace("FR-017-AC-2", "TC-218")
def test_adr_may_not_author_the_inverse_verb() -> None:
    assert "requirement_realized_by" not in adr_links()
    assert "disallowed-edge-type" in validate("requirement_realized_by")


@pytest.mark.trace("FR-017-AC-3", "TC-219")
def test_adr_unlisted_verb_still_draws_the_finding() -> None:
    assert "disallowed-edge-type" in validate("bogus_verb")


@pytest.mark.trace("FR-017-AC-4", "TC-220")
def test_adr_keeps_its_previous_verbs() -> None:
    assert {"supersedes", "superseded_by", "relates_to", "depends_on"} <= set(
        adr_links()
    )
