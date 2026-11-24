"""Feature-risk archetypes and the supplier/adopter distinction (FR-024–026)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from conftest import (
    EXAMPLES_DIR,
    MANIFEST_PATH,
    REPO_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    quire_validate,
)
from jsonschema import Draft202012Validator
from support.strict_yaml import load_yaml_strict


def frontmatter_schema(name: str) -> dict:
    """Load one authored frontmatter schema from the module."""
    return json.loads((SCHEMAS_DIR / name).read_text())


def rating(scope: str, verb: str) -> dict:
    """Build minimal valid metadata for one scope and its relationship verb."""
    return {
        "id": "FRR-001",
        "title": "Feature rating",
        "type": "FeatureRiskRating",
        "scope": scope,
        "rating": "not_high_process_risk",
        "rated_by": "Named Reviewer",
        "intended_use": "IU-001",
        "relationships": [{"target": "ix://agent-ix/example/FR-001", "type": verb}],
    }


class TestFeatureRiskRating:
    """Tests for IntendedUse and FeatureRiskRating module contracts."""

    @pytest.mark.trace("FR-025-AC-1", "FR-025-AC-4", "FR-026-AC-5")
    @pytest.mark.parametrize(
        ("scope", "verb"),
        [("supplier", "rates_feature"), ("adopter", "re_rates")],
    )
    def test_valid_relationships_match_rating_scope(
        self, scope: str, verb: str
    ) -> None:
        """Accept only each rating scope's relationship kind.

        Assumptions:
            Each fixture has all required fields and one well-formed edge.
        Criteria:
            Supplier `rates_feature` and adopter `re_rates` metadata validate.

        Trace: FR-025-AC-1, FR-025-AC-4, FR-026-AC-5
        """
        validator = Draft202012Validator(
            frontmatter_schema("feature-risk-rating-frontmatter.schema.json")
        )
        assert list(validator.iter_errors(rating(scope, verb))) == []

    @pytest.mark.trace("FR-025-AC-4", "FR-026-AC-5")
    @pytest.mark.parametrize(
        ("scope", "verb"),
        [("supplier", "re_rates"), ("adopter", "rates_feature")],
    )
    def test_rejects_relationships_from_the_other_scope(
        self, scope: str, verb: str
    ) -> None:
        """Reject a supplier/adopter edge used by the opposite scope.

        Assumptions:
            The input is otherwise valid feature-rating metadata.
        Criteria:
            Scope mismatch produces at least one schema error.

        Trace: FR-025-AC-4, FR-026-AC-5
        """
        validator = Draft202012Validator(
            frontmatter_schema("feature-risk-rating-frontmatter.schema.json")
        )
        assert list(validator.iter_errors(rating(scope, verb)))

    @pytest.mark.trace("FR-025-AC-6", "NFR-002")
    def test_rating_is_human_authored_without_computed_fields(self) -> None:
        """Keep risk values person-authored and reject undeclared fields.

        Assumptions:
            The frontmatter schema defines the complete rating field set.
        Criteria:
            Rating has no default, computed-risk fields are absent, and extra
            properties are rejected.

        Trace: FR-025-AC-6, NFR-002
        """
        schema = frontmatter_schema("feature-risk-rating-frontmatter.schema.json")
        assert "default" not in schema["properties"]["rating"]
        assert schema["additionalProperties"] is False
        names = set(schema["properties"])
        assert not names & {
            "score",
            "risk_score",
            "threshold",
            "product_criticality",
            "software_safety_class",
            "risk_acceptability",
        }

    @pytest.mark.trace("FR-025-AC-2")
    def test_invalid_rating_missing_rater_and_extra_fields_fail(self) -> None:
        """Reject invalid enum values, missing identity and computed fields.

        Assumptions:
            Each candidate begins as otherwise-valid supplier metadata.
        Criteria:
            Invalid rating, absent named rater, and extra score each fail
            frontmatter validation.

        Trace: FR-025-AC-2
        """
        validator = Draft202012Validator(
            frontmatter_schema("feature-risk-rating-frontmatter.schema.json")
        )
        invalid_value = rating("supplier", "rates_feature")
        invalid_value["rating"] = "medium"
        missing_rater = rating("supplier", "rates_feature")
        del missing_rater["rated_by"]
        computed_value = rating("supplier", "rates_feature")
        computed_value["score"] = 3

        assert list(validator.iter_errors(invalid_value))
        assert list(validator.iter_errors(missing_rater))
        assert list(validator.iter_errors(computed_value))

    @pytest.mark.trace("FR-024-AC-4")
    @pytest.mark.parametrize(
        "tool",
        ["quoin", "quire-rs", "quire-cli", "engineering-assurance", "filament-analyze"],
    )
    def test_intended_use_schema_admits_initial_tool_set(self, tool: str) -> None:
        """Admit every package in the initial intended-use validation scope.

        Assumptions:
            The document contains all required IntendedUse fields.
        Criteria:
            Every named package validates against the tool vocabulary.

        Trace: FR-024-AC-4
        """
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
    def test_skeletons_and_examples_validate(self, path: Path) -> None:
        """Validate each shipped authoring example with quire.

        Assumptions:
            The module manifest and local requirement documents are loaded.
        Criteria:
            Both archetypes' skeletons and examples pass quire validation.

        Trace: FR-024-AC-1, FR-025-AC-1
        """
        result = quire_validate(path, scope=REPO_ROOT)
        assert result.returncode == 0, result.stderr

    @pytest.mark.trace("FR-026-AC-1", "FR-026-AC-5")
    def test_required_relation_uses_only_supplier_feature_edges(self) -> None:
        """Declare FR completeness over supplier-only `rates_feature` edges.

        Assumptions:
            Adopter ratings use `re_rates` and do not introduce FR edges.
        Criteria:
            The incoming required relation to a FeatureRiskRating uses the
            supplier edge verb and feature-without-risk-rating check.

        Trace: FR-026-AC-1, FR-026-AC-5
        """
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
        assert (
            manifest["grammar_severity"]["trace:feature-without-risk-rating"] is False
        )
