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
    run_quire,
)
from jsonschema import Draft202012Validator
from support.strict_yaml import load_yaml_strict


def frontmatter_schema(name: str) -> dict:
    """Load one authored frontmatter schema from the module."""
    return json.loads((SCHEMAS_DIR / name).read_text())


def rating(scope: str, verb: str) -> dict:
    """Build minimal valid metadata for one scope and its relationship verb."""
    document = {
        "id": "FRR-001",
        "title": "Feature rating",
        "type": "FeatureRiskRating",
        "scope": scope,
        "rating": "not_high_process_risk",
        "rated_by": "Named Reviewer",
        "relationships": [],
    }
    if scope == "supplier":
        document["relationships"] = [
            {
                "target": "ix://agent-ix/spec-artifacts-process/IU-001",
                "type": "uses_intended_use",
            },
            {"target": "ix://agent-ix/example/FR-001", "type": verb},
        ]
    else:
        document["intended_use"] = "Adopter integrator package intended use"
        document["relationships"] = [
            {"target": "ix://agent-ix/example/FRR-001", "type": verb}
        ]
    return document


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

    @pytest.mark.trace("FR-025-AC-8", "FR-025-AC-9", "FR-025-AC-11", "FR-025-AC-16")
    def test_supplier_intended_use_is_one_typed_relationship(self) -> None:
        """Require a supplier rating to link to its IntendedUse artifact.

        Assumptions:
            Supplier ratings use a local `IU-NNN` relationship target.
        Criteria:
            One typed IntendedUse edge validates; a missing or foreign-kind
            edge does not.

        Trace: FR-025-AC-8, FR-025-AC-9, FR-025-AC-11, FR-025-AC-16
        """
        validator = Draft202012Validator(
            frontmatter_schema("feature-risk-rating-frontmatter.schema.json")
        )
        valid = rating("supplier", "rates_feature")
        assert list(validator.iter_errors(valid)) == []

        missing = rating("supplier", "rates_feature")
        missing["relationships"] = [
            edge for edge in missing["relationships"] if edge["type"] != "uses_intended_use"
        ]
        foreign = rating("supplier", "rates_feature")
        foreign["relationships"][0]["target"] = (
            "ix://agent-ix/spec-artifacts-process/FR-024"
        )
        duplicate = rating("supplier", "rates_feature")
        duplicate["relationships"].insert(1, duplicate["relationships"][0].copy())

        assert list(validator.iter_errors(missing))
        assert list(validator.iter_errors(foreign))
        assert list(validator.iter_errors(duplicate))

    @pytest.mark.trace("FR-025-AC-3")
    def test_supplier_rating_covers_two_existing_feature_targets(self, tmp_path: Path) -> None:
        """Accept one assessment row for each of two existing feature targets.

        Assumptions:
            FR-009 and FR-024 exist in the loaded specification corpus.
        Criteria:
            Two `rates_feature` edges and their two typed row references validate.

        Trace: FR-025-AC-3
        """
        content = (EXAMPLES_DIR / "FeatureRiskRating.md").read_text()
        content = content.replace(
            "    type: rates_feature\n---",
            "    type: rates_feature\n"
            "  - target: ix://agent-ix/spec-artifacts-process/FR-024\n"
            "    type: rates_feature\n---",
        ).replace(
            "| FR-009 | An invalid schema may allow malformed records to appear valid. | Run schema validation against invalid and valid fixtures and inspect diagnostics. |",
            "| FR-009 | An invalid schema may allow malformed records to appear valid. | Run schema validation against invalid and valid fixtures and inspect diagnostics. |\n"
            "| FR-024 | An intended-use omission can hide a material operating limit. | Review the intended-use record and confirm the limit is stated. |",
        )
        path = tmp_path / "two-feature-rating.md"
        path.write_text(content)

        result = quire_validate(path, scope=REPO_ROOT)
        assert result.returncode == 0, result.stderr

    @pytest.mark.trace("FR-024-AC-8", "FR-025-AC-12")
    @pytest.mark.parametrize(
        ("artifact", "identifier"),
        [("IntendedUse", "IU-1"), ("FeatureRiskRating", "FRR-1")],
    )
    def test_artifact_identifiers_require_exactly_three_digits(
        self, artifact: str, identifier: str
    ) -> None:
        """Reject identifiers shorter than the authored three-digit form.

        Assumptions:
            Each candidate otherwise matches its artifact frontmatter shape.
        Criteria:
            `IU-1` and `FRR-1` fail validation.

        Trace: FR-024-AC-8, FR-025-AC-12
        """
        schema_name = (
            "intended-use-frontmatter.schema.json"
            if artifact == "IntendedUse"
            else "feature-risk-rating-frontmatter.schema.json"
        )
        document = (
            {
                "id": identifier,
                "title": "Tool purpose",
                "type": "IntendedUse",
                "tool": "quoin",
                "relationships": [],
            }
            if artifact == "IntendedUse"
            else rating("supplier", "rates_feature")
        )
        if artifact == "FeatureRiskRating":
            document["id"] = identifier

        validator = Draft202012Validator(frontmatter_schema(schema_name))
        assert list(validator.iter_errors(document))

    @pytest.mark.trace("FR-025-AC-6", "FR-025-AC-7", "NFR-003-AC-1")
    def test_rating_is_human_authored_without_computed_fields(self) -> None:
        """Keep risk values person-authored and reject undeclared fields.

        Assumptions:
            The frontmatter schema defines the complete rating field set.
        Criteria:
            Rating has no default, computed-risk fields are absent, and extra
            properties are rejected.

        Trace: FR-025-AC-6, FR-025-AC-7, NFR-003-AC-1
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
        row_schema = frontmatter_schema("FeatureAssessmentRow.json")
        assert set(row_schema["properties"]) == {
            "requirement",
            "failureMode",
            "detection",
            "line",
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

    @pytest.mark.trace("FR-024-AC-4", "FR-024-AC-6")
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

        Trace: FR-024-AC-4, FR-024-AC-6
        """
        schema = frontmatter_schema("intended-use-frontmatter.schema.json")
        assert schema["properties"]["tool"]["enum"] == [
            "quoin",
            "quire-rs",
            "quire-cli",
            "engineering-assurance",
            "filament-analyze",
        ]
        document = {
            "id": "IU-001",
            "title": "Package intended use",
            "type": "IntendedUse",
            "tool": tool,
            "relationships": [],
        }
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(document)) == []
        document["tool"] = "unlisted-tool"
        assert list(validator.iter_errors(document))

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

    @pytest.mark.trace("FR-026-AC-2", "FR-026-AC-17")
    def test_required_relation_uses_only_supplier_feature_edges(self) -> None:
        """Declare FR completeness over supplier-only `rates_feature` edges.

        Assumptions:
            Adopter ratings use `re_rates` and do not introduce FR edges.
        Criteria:
            The incoming required relation to a FeatureRiskRating uses the
            supplier edge verb and feature-without-risk-rating check.

        Trace: FR-026-AC-2, FR-026-AC-17
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

    @pytest.mark.trace("FR-026-AC-1", "FR-026-AC-2", "FR-026-AC-5")
    def test_supplier_completeness_is_opt_in_and_excludes_adopter_reratings(
        self, tmp_path: Path
    ) -> None:
        """Report only the missing supplier rating when explicitly enabled.

        Assumptions:
            Three FR records exist, two supplier ratings cover two FRs, and an
            adopter re-rates one supplier rating.
        Criteria:
            Default validation is clean; error severity reports only the
            unrated third FR and does not count the adopter relationship.

        Trace: FR-026-AC-1, FR-026-AC-2, FR-026-AC-5
        """
        functional = tmp_path / "spec" / "functional"
        functional.mkdir(parents=True)
        source_fr = (REPO_ROOT / "spec/functional/FR-024-intended-use-archetype.md").read_text()
        for number in range(1, 4):
            identifier = f"FR-{number:03d}"
            target = functional / f"{identifier}-feature.md"
            target.write_text(source_fr.replace("FR-024", identifier))

        intended_use = tmp_path / "spec" / "IntendedUse.md"
        intended_use.write_text((EXAMPLES_DIR / "IntendedUse.md").read_text())
        rating_dir = tmp_path / "spec" / "ratings"
        rating_dir.mkdir()
        rating_template = (EXAMPLES_DIR / "FeatureRiskRating.md").read_text()
        for number in (1, 2):
            identifier = f"FR-{number:03d}"
            record_id = f"FRR-{number:03d}"
            body = rating_template.replace("FRR-001", record_id).replace(
                "FR-009", identifier
            )
            (rating_dir / f"{record_id}.md").write_text(body)

        adopter = rating_template.replace("FRR-001", "FRR-003").replace(
            "scope: supplier", "scope: adopter\nintended_use: Integrator production context"
        )
        adopter = adopter.replace(
            "  - target: ix://agent-ix/spec-artifacts-process/IU-001\n    type: uses_intended_use\n",
            "",
        ).replace(
            "ix://agent-ix/spec-artifacts-process/FR-009\n    type: rates_feature",
            "ix://agent-ix/spec-artifacts-process/FRR-001\n    type: re_rates",
        ).replace("FR-009", "FR-001")
        (rating_dir / "adopter-rerating.md").write_text(adopter)

        default = run_quire(
            "validate", "--scope", str(tmp_path), siblings=("spec-artifacts-iso",)
        )
        enabled = run_quire(
            "validate",
            "--severity",
            "trace:feature-without-risk-rating=error",
            "--scope",
            str(tmp_path),
            siblings=("spec-artifacts-iso",),
        )

        assert default.returncode == 0, default.stderr
        assert enabled.returncode != 0
        findings = [
            line
            for line in enabled.stderr.splitlines()
            if "feature-without-risk-rating" in line
        ]
        assert len(findings) == 1
        assert "FR-003" in findings[0]
        assert "FR-001" not in findings[0]

    @pytest.mark.trace("FR-024-AC-2", "FR-024-AC-3")
    def test_intended_use_requires_sections_and_rejects_unknown_frontmatter(
        self, tmp_path: Path
    ) -> None:
        """Reject missing IntendedUse sections and undeclared metadata.

        Assumptions:
            Each candidate starts from the valid shipped example.
        Criteria:
            Missing `Limits` and an unknown frontmatter key each produce a
            located Quire validation error.

        Trace: FR-024-AC-2, FR-024-AC-3
        """
        valid = (EXAMPLES_DIR / "IntendedUse.md").read_text()
        missing_section = valid.replace(
            "## Limits\n\nThe tool is not a compliance oracle and does not decide product or clinical safety.\n\n",
            "",
        )
        missing_path = tmp_path / "missing-limits.md"
        missing_path.write_text(missing_section)
        missing_result = quire_validate(missing_path, scope=REPO_ROOT)

        unknown_path = tmp_path / "unknown-field.md"
        unknown_path.write_text(valid.replace("type: IntendedUse\n", "type: IntendedUse\nunknown: true\n"))
        unknown_result = quire_validate(unknown_path, scope=REPO_ROOT)

        assert missing_result.returncode != 0
        assert "Limits" in missing_result.stderr
        assert unknown_result.returncode != 0
        assert "unknown" in unknown_result.stderr

    @pytest.mark.trace("FR-025-AC-10", "FR-025-AC-13")
    def test_assessment_requirement_is_typed_as_an_existing_fr(self, tmp_path: Path) -> None:
        """Reject a table requirement reference that names no FR.

        Assumptions:
            The fixture retains a valid supplier IntendedUse edge and all
            required sections.
        Criteria:
            An existing FR reference validates and an unresolved FR reference
            reports a dangling-reference diagnostic.

        Trace: FR-025-AC-10, FR-025-AC-13
        """
        valid = (EXAMPLES_DIR / "FeatureRiskRating.md").read_text()
        invalid = valid.replace("| FR-009 |", "| FR-999 |")
        path = tmp_path / "dangling-assessment-target.md"
        path.write_text(invalid)

        result = quire_validate(path, scope=REPO_ROOT)
        assert result.returncode != 0
        assert "FR-999" in result.stderr

    @pytest.mark.trace("FR-025-AC-11", "FR-025-AC-15")
    def test_intended_use_relationship_rejects_an_existing_non_intended_use(
        self, tmp_path: Path
    ) -> None:
        """Reject a typed IntendedUse edge that resolves to an FR document.

        Assumptions:
            FR-024 is a known FR in the loaded scope and the rating is otherwise
            a valid copy of the shipped supplier example.
        Criteria:
            A target with the FR id form fails schema validation; an unresolved
            IU id fails typed-reference validation.

        Trace: FR-025-AC-11, FR-025-AC-15
        """
        content = (EXAMPLES_DIR / "FeatureRiskRating.md").read_text().replace(
            "ix://agent-ix/spec-artifacts-process/IU-001",
            "ix://agent-ix/spec-artifacts-process/FR-024",
        )
        path = tmp_path / "foreign-intended-use.md"
        path.write_text(content)

        result = quire_validate(path, scope=REPO_ROOT)
        assert result.returncode != 0
        assert "FR-024" in result.stderr

        missing_intended_use = content.replace("/FR-024", "/IU-999")
        missing_path = tmp_path / "missing-intended-use.md"
        missing_path.write_text(missing_intended_use)
        missing_result = run_quire(
            "validate", "--strict", "--scope", str(REPO_ROOT), str(missing_path)
        )
        assert missing_result.returncode != 0
        assert "IU-999" in missing_result.stderr

    @pytest.mark.trace("FR-025-AC-4", "FR-025-AC-5")
    def test_adopter_rerating_is_separate_and_read_only(self, tmp_path: Path) -> None:
        """Keep adopter re-ratings separate from the supplier record.

        Assumptions:
            The adopter document points to the supplier rating id and has a
            distinct rating and rationale.
        Criteria:
            Both records validate without modifying supplier bytes.

        Trace: FR-025-AC-4, FR-025-AC-5
        """
        supplier_text = (EXAMPLES_DIR / "FeatureRiskRating.md").read_text().replace(
            "FRR-001", "FRR-700"
        )
        adopter_text = supplier_text.replace("FRR-700", "FRR-701").replace(
            "scope: supplier", "scope: adopter\nintended_use: Integrator production context"
        )
        adopter_text = adopter_text.replace(
            "  - target: ix://agent-ix/spec-artifacts-process/IU-001\n    type: uses_intended_use\n",
            "",
        ).replace(
            "ix://agent-ix/spec-artifacts-process/FR-009\n    type: rates_feature",
            "ix://agent-ix/spec-artifacts-process/FRR-700\n    type: re_rates",
        )
        adopter_text = adopter_text.replace(
            "rating: not_high_process_risk", "rating: high_process_risk"
        ).replace(
            "The named reviewer selected this rating for the stated repository-validation use.",
            "The adopter reviewer selected a different rating for its integration use.",
        )
        supplier_path = tmp_path / "supplier.md"
        adopter_path = tmp_path / "adopter.md"
        supplier_path.write_text(supplier_text)
        adopter_path.write_text(adopter_text)
        before = supplier_path.read_bytes()

        result = quire_validate(supplier_path, adopter_path, scope=REPO_ROOT)

        assert result.returncode == 0, result.stderr
        assert supplier_path.read_bytes() == before
        assert "rating: not_high_process_risk" in supplier_path.read_text()
        assert "rating: high_process_risk" in adopter_path.read_text()

    @pytest.mark.trace(
        "FR-024-AC-7",
        "FR-027-AC-13",
        "FR-026-AC-7",
        "FR-026-AC-8",
        "FR-026-AC-9",
        "FR-026-AC-10",
        "FR-026-AC-11",
        "FR-026-AC-12",
        "FR-026-AC-13",
        "FR-026-AC-14",
        "FR-026-AC-15",
        "FR-026-AC-16",
    )
    def test_ratings_command_contract_names_output_and_failure_behavior(self) -> None:
        """Keep the ratings command contract explicit for its Quoin owner.

        Assumptions:
            FR-026 is the producer-facing interface contract implemented by
            Quoin PR #1053.
        Criteria:
            Command, human output, JSON envelope, unreadable diagnostics,
            duplicate failure and read-only behavior remain specified.

        Trace: FR-024-AC-7, FR-027-AC-13, FR-026-AC-7, FR-026-AC-8, FR-026-AC-9, FR-026-AC-10, FR-026-AC-11, FR-026-AC-12, FR-026-AC-13, FR-026-AC-14, FR-026-AC-15, FR-026-AC-16
        """
        spec = (REPO_ROOT / "spec/functional/FR-026-feature-rating-completeness.md").read_text()
        for contract in (
            "quoin validation ratings --repo DIR --repo-id ORG/REPO [--json]",
            "The command SHALL NOT inspect Git remotes or require a Git repository.",
            "FR-ID: STATUS (rating IDs: ID[, ID…])",
            'exactly the top-level members `features` and `unreadable`',
            'Each object in `features` SHALL contain exactly `feature_id`',
            'status` (one of `unrated`, `rated`, `rated_more_than_once`)',
            'exactly `path` (repository-relative path using `/`) and `reason`',
            "unreadable: PATH: REASON",
            "A `rated_more_than_once` status SHALL make the result partial",
            "The command SHALL NOT create repository files.",
            "The command SHALL NOT edit repository files.",
            "The command SHALL NOT delete repository files.",
            "The command SHALL NOT normalize repository files.",
            "leaves every repository path and file byte unchanged",
            "A missing or non-directory `DIR/spec/` returns a command error",
            "The command SHALL order functional requirement results by `feature_id`.",
            "The command SHALL order each `rating_ids` array lexically by rating id.",
            "An unreadable input SHALL make the result partial.",
            "A partial result due to unreadable input SHALL exit with status 1.",
            "A partial result due to duplicate supplier ratings SHALL exit with status 1.",
            "A duplicate supplier rating identifies the FR and every conflicting rating id and exits with status 1.",
            "A `rated_more_than_once` status",
            "A missing or non-directory `DIR/spec/` returns a command error",
            "Quoin's [FR-217](ix://agent-ix/quoin/FR-217) validation-report command",
            "Quoin's [FR-220](ix://agent-ix/quoin/FR-220) external-tools configuration index",
        ):
            assert contract in spec

    @pytest.mark.trace("NFR-002-AC-1", "NFR-003-AC-1", "FR-027-AC-6")
    def test_authorship_and_computed_decision_boundaries_are_schema_visible(self) -> None:
        """Keep human authorship and the absence of computed decisions explicit.

        Assumptions:
            The schemas and TypeSpec output are committed module data.
        Criteria:
            `rated_by` is required; generated decision fields are absent; and
            the record model contains no commit identity for acceptance.

        Trace: NFR-002-AC-1, NFR-003-AC-1, FR-027-AC-6
        """
        schema = frontmatter_schema("feature-risk-rating-frontmatter.schema.json")
        assert "rated_by" in schema["required"]
        assert schema["additionalProperties"] is False
        assert not set(schema["properties"]) & {
            "score",
            "risk_score",
            "threshold",
            "product_criticality",
            "software_safety_class",
            "risk_acceptability",
            "commit_id",
            "digest",
        }
