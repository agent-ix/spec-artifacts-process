"""FR-007-AC-17: the criterion obligation sources read the document's rating."""

from __future__ import annotations

import json

import pytest
from conftest import MANIFEST_PATH, REPO_ROOT, run_quire
from support.strict_yaml import load_yaml_strict

SCOPE = REPO_ROOT / "tests" / "fixtures" / "criticality"


def sources() -> dict[str, dict]:
    manifest = load_yaml_strict(MANIFEST_PATH.read_text())
    return {s["name"]: s for s in manifest["traceability"]["obligations"]}


@pytest.mark.trace("TC-226", "FR-007-AC-17")
def test_requirement_criterion_sources_declare_the_criticality_field() -> None:
    declared = sources()
    for name in ("acceptance-criterion", "nfr-acceptance-criterion"):
        assert declared[name]["criticality_field"] == "criticality"
    for name in ("constraint", "nfr-metric", "configuration-matrix"):
        assert "criticality_field" not in declared[name]


@pytest.mark.trace("TC-226", "FR-007-AC-17")
def test_coverage_obligations_carry_the_document_rating_and_never_default() -> None:
    result = run_quire(
        "coverage", "--scope", str(SCOPE), "--json", siblings=("spec-artifacts-iso",)
    )
    assert result.returncode == 0, result.stderr
    rated = {
        o["id"]: o.get("criticality") for o in json.loads(result.stdout)["obligations"]
    }
    assert rated["FR-001-AC-1"] == "high"
    assert rated["NFR-001-AC-1"] == "low"
    assert rated["FR-002-AC-1"] is None
