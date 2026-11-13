"""FR-017: the ADR archetype lists the design-realization verb."""

from __future__ import annotations

import json
import subprocess

import pytest
from conftest import MANIFEST_PATH, PACKAGE_ROOT, REPO_ROOT, run_quire
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


def adr_links() -> dict[str, list[str]]:
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
    links = adr_links()
    for verb in ("supersedes", "superseded_by", "relates_to", "depends_on"):
        assert links[verb] == ["*"]


CORPUS = REPO_ROOT / "tests" / "fixtures" / "design_edges"
MEMBER = "agent-ix/design-fixture"
SIBLINGS = ("spec-artifacts-iso", "spec-objects-architecture")


def bundle(kind: str, *extra: str) -> subprocess.CompletedProcess:
    return run_quire(
        "validate",
        "--okf",
        *extra,
        "--repo",
        f"{MEMBER}={CORPUS / kind}",
        siblings=SIBLINGS,
    )


@pytest.mark.trace("FR-017-AC-5", "TC-221")
def test_realizes_requirement_targets_are_fr_and_nfr() -> None:
    assert adr_links()["realizes_requirement"] == ["FR", "NFR"]


@pytest.mark.trace("FR-017-AC-6", "TC-222")
def test_adr_realizing_fr_and_nfr_draws_no_disallowed_edge() -> None:
    # The engine does not check an artifact-type target's kind (PLAT-1689), so
    # this row cannot fail through the target list; TC-221 guards the list.
    lines = bundle("valid").stderr.splitlines()
    for doc in ("ADR-001", "ADR-002"):
        assert not [ln for ln in lines if doc in ln and "disallowed-edge" in ln]


@pytest.mark.trace("FR-017-AC-7", "TC-223")
def test_adr_realizing_a_part_draws_the_advisory_finding_naming_the_ids() -> None:
    result = bundle("invalid", "--strict")
    wrong = [ln for ln in result.stderr.splitlines() if "disallowed-edge-target" in ln]
    assert len(wrong) == 1
    assert wrong[0].startswith("warning:")
    assert "ADR-004" in wrong[0]
    assert "scoring_engine" in wrong[0]
    assert "'part'" in wrong[0]


@pytest.mark.trace("FR-017-AC-8", "TC-224")
def test_adr_realizing_a_missing_id_fails_strict_with_a_located_error() -> None:
    result = bundle(
        "invalid", "--strict", "--severity", "trace:unowned-quality-characteristic=off"
    )
    assert result.returncode == 3, result.stderr
    errors = [
        ln
        for ln in result.stderr.splitlines()
        if ln.startswith("[") and "[dangling-reference]" in ln
    ]
    assert errors
    assert all("ADR-003.md" in ln and "FR-999" in ln for ln in errors)
    assert any("'realizes_requirement'" in ln for ln in errors)
    assert f"{len(errors)} OKF bundle validation error(s)" in result.stderr


@pytest.mark.trace("FR-017-AC-9", "TC-225")
def test_relations_report_the_adr_as_realizing_fr_and_nfr() -> None:
    result = run_quire(
        "relations",
        "--json",
        "--repo",
        f"{MEMBER}={CORPUS / 'valid'}",
        siblings=SIBLINGS,
    )
    assert result.returncode == 0, result.stderr
    rows = {
        (rel["name"], row["document"]["id"]): row
        for rel in json.loads(result.stdout)["relations"]
        for row in rel["rows"]
    }
    for relation, requirement, adr in (
        ("fr-has-design-element", "FR-001", "ADR-001"),
        ("nfr-has-design-element", "NFR-001", "ADR-002"),
    ):
        row = rows[(relation, requirement)]
        assert row["state"] == "covered"
        assert [(e["id"], e["archetype"]) for e in row["linked"]] == [(adr, "ADR")]
