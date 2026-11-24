"""Feature-risk archetypes and their supplier/adopter distinction (FR-024–026)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from conftest import EXAMPLES_DIR, MANIFEST_PATH, REPO_ROOT, SCHEMAS_DIR, SKELETONS_DIR, quire_validate
from jsonschema import Draft202012Validator
from support.strict_yaml import load_yaml_strict


def frontmatter_schema(name: str) -> dict:
    return json.loads((SCHEMAS_DIR / name).read_text())


def rating(scope: str, verb: str) -> dict:
    return {
        "id": "FRR-001",
        "title": "Feature rating",
        "type": "FeatureRiskRating",
        "scope": scope,
        "rating": "not_high_process_risk",
        "rated_by": "Named Reviewer",
        "intended_use": "IU-001",
        "relationships": [
            {"target": "ix://agent-ix/example/FR-001", "type": verb}
        ],
    }


@pytest.mark.trace("FR-025-AC-1", "FR-025-AC-4", "FR-026-AC-5")
@pytest.mark.parametrize(
    ("scope", "verb"), [("supplier", "rates_feature"), ("adopter", "re_rates")]
)
def test_rating_relationships_match_scope(scope: str, verb: str) -> None:
    validator = Draft202012Validator(
        frontmatter_schema("feature-risk-rating-frontmatter.schema.json")
    )
    assert list(validator.iter_errors(rating(scope, verb))) == []


@pytest.mark.trace("FR-025-AC-4", "FR-026-AC-5")
@pytest.mark.parametrize(
    ("scope", "verb"), [("supplier", "re_rates"), ("adopter", "rates_feature")]
)
def test_rating_rejects_relationships_from_the_other_scope(scope: str, verb: str) -> None:
    validator = Draft202012Validator(
        frontmatter_schema("feature-risk-rating-frontmatter.schema.json")
    )
    assert list(validator.iter_errors(rating(scope, verb)))


@pytest.mark.trace("FR-024-AC-4")
@pytest.mark.parametrize(
    "tool", ["quoin", "quire-rs", "quire-cli", "engineering-assurance", "filament-analyze"]
)
def test_intended_use_schema_admits_the_initial_tool_set(tool: str) -> None:
    schema = frontmatter_schema("intended-use-frontmatter.schema.json")
    document = {
        "id": "IU-001",
        "title": "Package intended use",
        "type": "IntendedUse",
        "tool": tool,
        "relationships": [],
    }
    assert list(Draft202012Validator(schema).iter_errors(document)) == []


@pytest.mark.trace("FR-024-AC-1", "FR-025-AC-1")
@pytest.mark.parametrize(
    "path",
    [
        SKELETONS_DIR / "IntendedUse.md",
        SKELETONS_DIR / "FeatureRiskRating.md",
        EXAMPLES_DIR / "IntendedUse.md",
        EXAMPLES_DIR / "FeatureRiskRating.md",
    ],
)
def test_authored_skeletons_and_examples_validate(path: Path) -> None:
    result = quire_validate(path, scope=REPO_ROOT)
    assert result.returncode == 0, result.stderr


@pytest.mark.trace("FR-026-AC-1", "FR-026-AC-5")
def test_supplier_completeness_rule_counts_only_supplier_rating_edges() -> None:
    manifest = load_yaml_strict(MANIFEST_PATH.read_text())
    rule = next(
        relation
        for relation in manifest["traceability"]["required_relations"]
        if relation["name"] == "fr-has-risk-rating"
    )
    assert rule == {
        "name": "fr-has-risk-rating",
        "from": "FR",
        "edges": ["rates_feature"],
        "to": ["FeatureRiskRating"],
        "direction": "incoming",
        "check": "feature-without-risk-rating",
    }
