"""Feature-risk archetypes and the supplier/adopter distinction (FR-024–026)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from conftest import (
    EXAMPLES_DIR,
    MANIFEST_PATH,
    REPO_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    diagnostics,
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
        "status": "proposed",
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


def acceptance_result(
    status: str,
    rated_by: str | None,
    verifier_result: dict,
    trailer: str,
) -> str:
    """Evaluate the signed-acceptance contract used by the spec examples."""
    signer = verifier_result.get("signer", {})
    meaning = verifier_result.get("signed_off_meaning", {})
    if (
        status == "accepted"
        and verifier_result.get("protocol")
        == "engineering-assurance.signature-verify-result/v1"
        and verifier_result.get("status") == "signed_valid"
        and signer.get("mapping") == "mapped"
        and signer.get("principal") == rated_by
        and meaning.get("presence") == "present"
        and "feature-risk-rating-accepted" in meaning.get("values", [])
        and trailer == "Signed-off-meaning: feature-risk-rating-accepted"
    ):
        return "accepted"
    return "not_accepted"


def signed_commit_evidence(tmp_path: Path) -> tuple[dict, str]:
    """Create and verify a temporary SSH-signed commit with the exact trailer."""
    key = tmp_path / "signing-key"
    subprocess.run(
        ["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)],
        check=True,
        capture_output=True,
        text=True,
    )
    public_key = key.with_suffix(".pub").read_text().split()
    principal = "allowed-principal@example.invalid"
    allowed_signers = tmp_path / "allowed_signers"
    allowed_signers.write_text(
        f'{principal} namespaces="git" {public_key[0]} {public_key[1]}\n'
    )
    repository = tmp_path / "signed-repo"
    repository.mkdir()

    def git(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args],
            cwd=repository,
            check=True,
            capture_output=True,
            text=True,
        )

    git("init", "-q")
    git("config", "user.name", "Spec Test Signer")
    git("config", "user.email", "spec-test@example.invalid")
    git("config", "gpg.format", "ssh")
    git("config", "user.signingkey", str(key))
    git("config", "gpg.ssh.allowedSignersFile", str(allowed_signers))
    (repository / "rating.md").write_text("proposal\n")
    git("add", "rating.md")
    git(
        "-c",
        "commit.gpgsign=true",
        "commit",
        "-S",
        "-m",
        "rating proposal",
        "-m",
        "Signed-off-meaning: feature-risk-rating-accepted",
    )
    git("verify-commit", "HEAD")
    message = git("show", "-s", "--format=%B", "HEAD").stdout
    trailer = next(
        (
            line
            for line in message.splitlines()
            if line.startswith("Signed-off-meaning:")
        ),
        "",
    )
    return {
        "protocol": "engineering-assurance.signature-verify-result/v1",
        "status": "signed_valid",
        "kind": "commit",
        "signer": {
            "mapping": "mapped",
            "principal": "allowed-principal@example.invalid",
        },
        "signed_off_meaning": {
            "presence": "present",
            "values": ["feature-risk-rating-accepted"],
        },
    }, trailer


class TestFeatureRiskRating:
    """Tests for IntendedUse and FeatureRiskRating module contracts."""

    @pytest.mark.trace("FR-025-AC-1", "FR-025-AC-4", "FR-025-AC-17", "FR-026-AC-5")
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

        Trace: FR-025-AC-1, FR-025-AC-4, FR-025-AC-17, FR-026-AC-5
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

    @pytest.mark.trace("FR-025-AC-17")
    def test_proposed_and_accepted_ratings_have_consistent_authorship(self) -> None:
        """Reject named proposals and require identity for accepted ratings.

        Assumptions:
            Scope and relationships are otherwise valid supplier metadata.
        Criteria:
            Proposed ratings reject `rated_by`; accepted ratings require it.

        Trace: FR-025-AC-17, FR-027-AC-14, FR-027-AC-15
        """
        validator = Draft202012Validator(
            frontmatter_schema("feature-risk-rating-frontmatter.schema.json")
        )
        proposed = rating("supplier", "rates_feature")
        assert list(validator.iter_errors(proposed)) == []

        proposed_with_rater = rating("supplier", "rates_feature")
        proposed_with_rater["rated_by"] = "Allowed Principal"
        assert list(validator.iter_errors(proposed_with_rater))

        accepted_without_rater = rating("supplier", "rates_feature")
        accepted_without_rater["status"] = "accepted"
        assert list(validator.iter_errors(accepted_without_rater))

        accepted = rating("supplier", "rates_feature")
        accepted["status"] = "accepted"
        accepted["rated_by"] = "Allowed Principal"
        assert list(validator.iter_errors(accepted)) == []

    @pytest.mark.trace("FR-027-AC-14")
    def test_signed_valid_commit_does_not_accept_a_proposed_rating(
        self, tmp_path: Path
    ) -> None:
        """A valid mapped signature and exact trailer cannot accept a proposal.

        Assumptions:
            The verifier result represents a signed-valid commit by the named
            principal, and its exact acceptance trailer is present.
        Criteria:
            A proposal is reported not_accepted even with otherwise valid
            acceptance evidence.

        Trace: FR-027-AC-14
        """
        acceptance_spec = (
            REPO_ROOT / "spec/functional/FR-027-human-acceptance-of-risk-ratings.md"
        ).read_text()
        assert (
            "| FR-027-AC-14 | A rating marked `proposed` is reported `not_accepted`, "
            "including when its commit is otherwise signed-valid. | Test |"
        ) in acceptance_spec
        verifier_result, trailer = signed_commit_evidence(tmp_path)
        assert verifier_result["status"] == "signed_valid"
        assert trailer == "Signed-off-meaning: feature-risk-rating-accepted"
        assert (
            acceptance_result(
                "proposed",
                "allowed-principal@example.invalid",
                verifier_result,
                trailer,
            )
            == "not_accepted"
        )

    @pytest.mark.trace("FR-027-AC-15")
    def test_accepted_rating_requires_matching_signer_and_exact_trailer(
        self, tmp_path: Path
    ) -> None:
        """Accept only matching mapped identity and the exact trailer.

        Assumptions:
            The verifier result is from the versioned FR-036 protocol.
        Criteria:
            Matching accepted record/signature/trailer succeeds; signer or
            trailer mismatch is not accepted.

        Trace: FR-027-AC-15
        """
        acceptance_spec = (
            REPO_ROOT / "spec/functional/FR-027-human-acceptance-of-risk-ratings.md"
        ).read_text()
        assert (
            "| FR-027-AC-15 | An accepted rating requires a `rated_by` principal "
            "matching the verified signer and the exact acceptance trailer. | Test |"
        ) in acceptance_spec
        valid_result, exact_trailer = signed_commit_evidence(tmp_path)
        assert valid_result["status"] == "signed_valid"
        assert exact_trailer == "Signed-off-meaning: feature-risk-rating-accepted"
        assert (
            acceptance_result(
                "accepted",
                "allowed-principal@example.invalid",
                valid_result,
                exact_trailer,
            )
            == "accepted"
        )

        mismatched_signer = dict(valid_result)
        mismatched_signer["signer"] = {
            "mapping": "mapped",
            "principal": "Different Principal",
        }
        assert (
            acceptance_result(
                "accepted",
                "allowed-principal@example.invalid",
                mismatched_signer,
                exact_trailer,
            )
            == "not_accepted"
        )
        assert (
            acceptance_result(
                "accepted",
                "allowed-principal@example.invalid",
                valid_result,
                "Signed-off-meaning: feature-risk-rating-approved",
            )
            == "not_accepted"
        )

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
            edge
            for edge in missing["relationships"]
            if edge["type"] != "uses_intended_use"
        ]
        foreign = rating("supplier", "rates_feature")
        foreign["relationships"][0][
            "target"
        ] = "ix://agent-ix/spec-artifacts-process/FR-024"
        duplicate = rating("supplier", "rates_feature")
        duplicate["relationships"].insert(1, duplicate["relationships"][0].copy())

        assert list(validator.iter_errors(missing))
        assert list(validator.iter_errors(foreign))
        assert list(validator.iter_errors(duplicate))

    @pytest.mark.trace("FR-025-AC-3")
    def test_supplier_rating_covers_two_existing_feature_targets(
        self, tmp_path: Path
    ) -> None:
        """Accept two existing feature targets without per-target tables.

        Assumptions:
            FR-009 and FR-024 exist in the loaded specification corpus.
        Criteria:
            Two `rates_feature` edges validate without a Feature assessments section.

        Trace: FR-025-AC-3
        """
        content = (EXAMPLES_DIR / "FeatureRiskRating.md").read_text()
        assert "## Feature assessments" not in content
        content = content.replace(
            "    type: rates_feature\n---",
            "    type: rates_feature\n"
            "  - target: ix://agent-ix/spec-artifacts-process/FR-024\n"
            "    type: rates_feature\n---",
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

    @pytest.mark.trace(
        "FR-025-AC-6", "FR-025-AC-7", "FR-025-AC-14", "NFR-003-AC-1", "NFR-003-M-1"
    )
    def test_rating_is_human_authored_without_computed_fields(self) -> None:
        """Keep risk values person-authored and reject undeclared fields.

        Assumptions:
            The frontmatter schema defines the complete rating field set.
        Criteria:
            Rating has no default, computed-risk fields are absent, and extra
            properties are rejected.

        Trace: FR-025-AC-6, FR-025-AC-7, NFR-003-AC-1, NFR-003-M-1
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
        mappings = load_yaml_strict(
            (REPO_ROOT / "spec_artifacts_process/mappings.yaml").read_text()
        )
        rating_mapping = mappings["models"]["FeatureRiskRating"]["properties"]
        assert set(rating_mapping) == {
            "id",
            "title",
            "type",
            "scope",
            "rating",
            "status",
            "ratedBy",
            "intendedUse",
            "relationships",
            "provenance",
            "rationale",
            "assuranceActivities",
        }
        assert "riskScore" not in rating_mapping
        artifact = next(
            item
            for item in load_yaml_strict(MANIFEST_PATH.read_text())["artifact_types"]
            if item["name"] == "FeatureRiskRating"
        )
        assert artifact["lint_rules_ref"] == []
        assert set(artifact["body_extraction"]["yield_pattern"]["match"]) == {
            "rationale",
            "assurance_activities",
        }
        record_schema = json.loads((SCHEMAS_DIR / "FeatureRiskRating.json").read_text())
        assert "featureAssessments" not in record_schema["properties"]
        assert "failureMode" not in record_schema["properties"]
        assert "detection" not in record_schema["properties"]
        assert record_schema["unevaluatedProperties"] == {"not": {}}
        assert "featureAssessments" not in json.loads(
            (EXAMPLES_DIR / "FeatureRiskRating.record.json").read_text()
        )
        assert (
            "## Feature assessments"
            not in (SKELETONS_DIR / "FeatureRiskRating.md").read_text()
        )

    @pytest.mark.trace("FR-025-AC-2", "FR-025-AC-17")
    def test_invalid_rating_missing_status_and_extra_fields_fail(self) -> None:
        """Reject invalid enum values, missing status and computed fields.

        Assumptions:
            Each candidate begins as otherwise-valid supplier metadata.
        Criteria:
            Invalid rating, absent status, and extra score each fail
            frontmatter validation.

        Trace: FR-025-AC-2
        """
        validator = Draft202012Validator(
            frontmatter_schema("feature-risk-rating-frontmatter.schema.json")
        )
        invalid_value = rating("supplier", "rates_feature")
        invalid_value["rating"] = "medium"
        missing_status = rating("supplier", "rates_feature")
        del missing_status["status"]
        computed_value = rating("supplier", "rates_feature")
        computed_value["score"] = 3

        assert list(validator.iter_errors(invalid_value))
        assert list(validator.iter_errors(missing_status))
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
        source_fr = (
            REPO_ROOT / "spec/functional/FR-024-intended-use-archetype.md"
        ).read_text()
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
            "scope: supplier",
            "scope: adopter\nintended_use: Integrator production context",
        )
        adopter = (
            adopter.replace(
                "  - target: ix://agent-ix/spec-artifacts-process/IU-001\n"
                "    type: uses_intended_use\n",
                "",
            )
            .replace(
                "ix://agent-ix/spec-artifacts-process/FR-009\n    type: rates_feature",
                "ix://agent-ix/spec-artifacts-process/FRR-001\n    type: re_rates",
            )
            .replace("FR-009", "FR-001")
        )
        (rating_dir / "adopter-rerating.md").write_text(adopter)

        documents = tuple(
            str(path) for path in sorted((tmp_path / "spec").rglob("*.md"))
        )

        default = run_quire(
            "validate",
            "--scope",
            str(tmp_path),
            *documents,
            siblings=("spec-artifacts-iso",),
        )
        enabled = run_quire(
            "validate",
            "--severity",
            "trace:feature-without-risk-rating=error",
            "--scope",
            str(tmp_path),
            *documents,
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
            "## Limits\n\nThe tool is not a compliance oracle and does not "
            "decide product or clinical safety.\n\n",
            "",
        )
        missing_path = tmp_path / "missing-limits.md"
        missing_path.write_text(missing_section)
        missing_result = quire_validate(missing_path, scope=REPO_ROOT)

        unknown_path = tmp_path / "unknown-field.md"
        unknown_path.write_text(
            valid.replace("type: IntendedUse\n", "type: IntendedUse\nunknown: true\n")
        )
        unknown_result = quire_validate(unknown_path, scope=REPO_ROOT)

        assert missing_result.returncode != 0
        assert "Limits" in missing_result.stderr
        assert unknown_result.returncode != 0
        assert "unknown" in unknown_result.stderr

    @pytest.mark.trace("FR-025-AC-10", "FR-025-AC-13")
    def test_rates_feature_relationship_is_typed_as_an_existing_fr(
        self, tmp_path: Path
    ) -> None:
        """Reject a rating relationship that names no FR.

        Assumptions:
            The fixture retains a valid supplier IntendedUse edge and all
            required sections.
        Criteria:
            An existing FR reference validates and an unresolved FR reference
            reports a dangling-reference diagnostic.

        Trace: FR-025-AC-10, FR-025-AC-13
        """
        valid = (EXAMPLES_DIR / "FeatureRiskRating.md").read_text()
        invalid = valid.replace(
            "ix://agent-ix/spec-artifacts-process/FR-009",
            "ix://agent-ix/spec-artifacts-process/FR-999",
        )
        path = tmp_path / "dangling-rating-target.md"
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
        content = (
            (EXAMPLES_DIR / "FeatureRiskRating.md")
            .read_text()
            .replace(
                "ix://agent-ix/spec-artifacts-process/IU-001",
                "ix://agent-ix/spec-artifacts-process/FR-024",
            )
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
        supplier_text = (
            (EXAMPLES_DIR / "FeatureRiskRating.md")
            .read_text()
            .replace("FRR-001", "FRR-700")
        )
        adopter_text = supplier_text.replace("FRR-700", "FRR-701").replace(
            "scope: supplier",
            "scope: adopter\nintended_use: Integrator production context",
        )
        adopter_text = adopter_text.replace(
            "  - target: ix://agent-ix/spec-artifacts-process/IU-001\n"
            "    type: uses_intended_use\n",
            "",
        ).replace(
            "ix://agent-ix/spec-artifacts-process/FR-009\n    type: rates_feature",
            "ix://agent-ix/spec-artifacts-process/FRR-700\n    type: re_rates",
        )
        adopter_text = adopter_text.replace(
            "rating: not_high_process_risk", "rating: high_process_risk"
        ).replace(
            "The named reviewer selected this rating for the stated "
            "repository-validation use.",
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

    @pytest.mark.trace("FR-026-AC-3")
    def test_a_feature_rating_to_an_intended_use_is_a_target_kind_mismatch(
        self, tmp_path: Path
    ) -> None:
        """Reject a `rates_feature` edge that resolves to an IntendedUse.

        Assumptions:
            The rating otherwise validates and IU-001 exists in the same corpus.
        Criteria:
            Quire identifies the relationship's target kind as invalid.

        Trace: FR-026-AC-3
        """
        rating_path = tmp_path / "FRR-001.md"
        rating_path.write_text(
            (EXAMPLES_DIR / "FeatureRiskRating.md")
            .read_text()
            .replace(
                "ix://agent-ix/spec-artifacts-process/FR-009\n    type: rates_feature",
                "ix://agent-ix/spec-artifacts-process/IU-001\n    type: rates_feature",
            )
        )
        intended_use = tmp_path / "IU-001.md"
        intended_use.write_text((EXAMPLES_DIR / "IntendedUse.md").read_text())

        result = quire_validate(rating_path, intended_use, scope=tmp_path)
        found = diagnostics(result)
        assert result.returncode != 0, result.stdout
        assert len(found) == 1, result.stderr
        assert "target-kind-mismatch" in found[0], found
        assert "IU-001" in found[0], found

    def test_ratings_command_contract_names_output_and_failure_behavior(self) -> None:
        """Keep the ratings command contract explicit for its Quoin owner.

        Assumptions:
            FR-026 is the producer-facing interface contract implemented by
            Quoin PR #1053.
        Criteria:
            Command, human output, JSON envelope, unreadable diagnostics,
            duplicate failure and read-only behavior remain specified.

        """
        spec = "\n".join(
            (REPO_ROOT / f"spec/functional/{name}").read_text()
            for name in (
                "FR-024-intended-use-archetype.md",
                "FR-026-feature-rating-completeness.md",
                "FR-027-human-acceptance-of-risk-ratings.md",
            )
        )
        for contract in (
            "quoin validation ratings --repo DIR --repo-id ORG/REPO [--json]",
            "The command SHALL NOT inspect Git remotes or require a Git repository.",
            "FR-ID: STATUS (rating IDs: ID[, ID…])",
            "exactly the top-level members `features` and `unreadable`",
            "Each object in `features` SHALL contain exactly `feature_id`",
            "status` (one of `unrated`, `rated`, `rated_more_than_once`)",
            "exactly `path` (repository-relative path using `/`) and `reason`",
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
            "A partial result due to duplicate supplier ratings SHALL exit "
            "with status 1.",
            "A duplicate supplier rating identifies the FR and every "
            "conflicting rating id and exits with status 1.",
            "A `rated_more_than_once` status",
            "A missing or non-directory `DIR/spec/` returns a command error",
        ):
            assert contract in spec

    @pytest.mark.trace("FR-027-AC-13")
    def test_validation_report_requires_tool_versions_and_configuration_entries(
        self,
    ) -> None:
        """Bind the external-tool report criterion to its named contracts.

        Assumptions:
            Quoin FR-217 and FR-220 own the report and configuration index.
        Criteria:
            FR-027 assigns report production and version-index entries to those
            requirements.

        Trace: FR-027-AC-13
        """
        acceptance_spec = (
            REPO_ROOT / "spec/functional/FR-027-human-acceptance-of-risk-ratings.md"
        ).read_text()
        intended_use_spec = (
            REPO_ROOT / "spec/functional/FR-024-intended-use-archetype.md"
        ).read_text()
        assert (
            "| FR-027-AC-13 | The Quoin validation report identifies the versions "
            "of external tools and references their FR-220 configuration-index "
            "entries. | Test |"
        ) in acceptance_spec
        assert "Quoin [FR-217](ix://agent-ix/quoin/FR-217)" in acceptance_spec
        assert "Quoin [FR-220](ix://agent-ix/quoin/FR-220)" in acceptance_spec
        assert "| FR-024-AC-7 |" not in intended_use_spec
        assert (
            "External-tool report requirements are owned by [FR-027-AC-13]"
            in intended_use_spec
        )

    @pytest.mark.trace("NFR-002-AC-1", "NFR-002-M-1", "NFR-003-AC-1", "FR-027-AC-6")
    def test_authorship_and_computed_decision_boundaries_are_schema_visible(
        self,
    ) -> None:
        """Keep human authorship and the absence of computed decisions explicit.

        Assumptions:
            The schemas and TypeSpec output are committed module data.
        Criteria:
            `status` is required; generated decision fields are absent; and
            the record model contains no commit identity for acceptance.

        Trace: NFR-002-AC-1, NFR-002-M-1, NFR-003-AC-1, FR-027-AC-6
        """
        schema = frontmatter_schema("feature-risk-rating-frontmatter.schema.json")
        assert "status" in schema["required"]
        assert "rated_by" not in schema["required"]
        assert schema["additionalProperties"] is False

        validator = Draft202012Validator(schema)
        valid_supplier = rating("supplier", "rates_feature")
        valid_adopter = rating("adopter", "re_rates")
        valid_accepted_supplier = rating("supplier", "rates_feature")
        valid_accepted_supplier["status"] = "accepted"
        valid_accepted_supplier["rated_by"] = "Allowed Principal"
        valid_accepted_adopter = rating("adopter", "re_rates")
        valid_accepted_adopter["status"] = "accepted"
        valid_accepted_adopter["rated_by"] = "Allowed Principal"
        assert list(validator.iter_errors(valid_supplier)) == []
        assert list(validator.iter_errors(valid_adopter)) == []
        assert list(validator.iter_errors(valid_accepted_supplier)) == []
        assert list(validator.iter_errors(valid_accepted_adopter)) == []

        supplier = rating("supplier", "rates_feature")
        supplier["relationships"] = [
            edge
            for edge in supplier["relationships"]
            if edge["type"] != "uses_intended_use"
        ]
        assert list(validator.iter_errors(supplier))

        adopter = rating("adopter", "re_rates")
        adopter.pop("intended_use")
        assert list(validator.iter_errors(adopter))

        accepted_without_identity = rating("adopter", "re_rates")
        accepted_without_identity["status"] = "accepted"
        assert list(validator.iter_errors(accepted_without_identity))
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
