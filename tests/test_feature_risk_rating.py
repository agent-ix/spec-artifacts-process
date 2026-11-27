"""Feature-risk archetypes and the supplier/adopter distinction (FR-024–026)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
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


EA_RELEASE = "0.11.0"


def engineering_assurance_binary() -> str:
    """Require the released EA binary used by this cross-repository contract."""
    configured = os.environ.get("EA_TEST_BINARY")
    binary = configured or shutil.which("engineering-assurance")
    assert binary, (
        "EA_TEST_BINARY must name the released Engineering Assurance binary "
        "used by the FR-027 Process integration tests."
    )
    version = subprocess.run(
        [binary, "--version"], capture_output=True, text=True, check=False
    )
    assert version.returncode == 0, version.stderr
    assert version.stdout.strip() == f"engineering-assurance {EA_RELEASE}", (
        f"FR-027 integration tests require released EA {EA_RELEASE}; "
        f"got {version.stdout.strip()!r} from {binary}"
    )
    return binary


def run_git(repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run one Git operation in a fixture repository and retain its output."""
    environment = os.environ.copy()
    environment.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
    environment.pop("GIT_DIR", None)
    return subprocess.run(
        ["git", *args],
        cwd=repository,
        capture_output=True,
        text=True,
        env=environment,
        check=False,
    )


def rating_markdown(*, rating_id: str, scope: str, status: str, rated_by: str) -> str:
    """Render the minimal schema-valid rating record used by the CLI fixtures."""
    document = rating(scope, "rates_feature" if scope == "supplier" else "re_rates")
    document["id"] = rating_id
    document["status"] = status
    document["rated_by"] = rated_by
    return f"---\n{json.dumps(document, indent=2)}\n---\n\n# Rating\n"


def signed_rating_repository(
    tmp_path: Path,
    *,
    status: str = "accepted",
    signed: bool = True,
    include_trailer: bool = True,
    allowed_principal: str = "alice@example.test",
    map_signing_key: bool = True,
    scopes: tuple[str, ...] = ("supplier",),
) -> tuple[Path, Path]:
    """Create a repository whose rating commit exercises EA's real CLI path."""
    repository = tmp_path / "rating-repo"
    (repository / "spec/validation").mkdir(parents=True)
    key = tmp_path / "signing-key"
    other_key = tmp_path / "other-key"
    for key_path in (key, other_key):
        generated = subprocess.run(
            ["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert generated.returncode == 0, generated.stderr

    allowed_signers = tmp_path / "allowed_signers"
    mapped_key = key if map_signing_key else other_key
    public_key = mapped_key.with_suffix(".pub").read_text().split()
    allowed_signers.write_text(
        f'{allowed_principal} namespaces="git" {public_key[0]} {public_key[1]}\n'
    )

    initialized = run_git(repository, "init", "-q", "-b", "main")
    assert initialized.returncode == 0, initialized.stderr
    for name, value in (
        ("user.name", "Rating Test"),
        ("user.email", "rating@example.test"),
        ("gpg.format", "ssh"),
        ("user.signingkey", str(key)),
        ("gpg.ssh.allowedSignersFile", str(allowed_signers)),
    ):
        configured = run_git(repository, "config", name, value)
        assert configured.returncode == 0, configured.stderr

    for index, scope in enumerate(scopes, start=1):
        rating_path = repository / f"spec/validation/FRR-{index:03}.md"
        rating_path.write_text(
            rating_markdown(
                rating_id=f"FRR-{index:03}",
                scope=scope,
                status=status,
                rated_by="alice@example.test",
            )
        )
    staged = run_git(repository, "add", "spec/validation")
    assert staged.returncode == 0, staged.stderr

    commit_args = ["commit", "--quiet", "-m", "rating proposal"]
    if signed:
        commit_args.insert(2, "-S")
    if include_trailer:
        commit_args.extend(["-m", "Signed-off-meaning: feature-risk-rating-accepted"])
    committed = run_git(repository, *commit_args)
    assert committed.returncode == 0, committed.stderr
    return repository, allowed_signers


def run_rating_acceptance(
    repository: Path, allowed_signers: Path
) -> tuple[subprocess.CompletedProcess[str], dict]:
    """Invoke released EA and return its command status and protocol result."""
    request = {
        "protocol": "engineering-assurance.rating-acceptance-request/v1",
        "repository": str(repository.resolve()),
        "allowed_signers": str(allowed_signers.resolve()),
    }
    output = subprocess.run(
        [
            engineering_assurance_binary(),
            "rating-acceptance",
            "--request",
            json.dumps(request),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    result = json.loads(output.stdout)
    assert result["protocol"] == "engineering-assurance.rating-acceptance-result/v1"
    return output, result


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

        Trace: FR-025-AC-17
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

    @pytest.mark.trace("FR-027-AC-1")
    def test_released_ea_accepts_a_mapped_signed_rating_with_exact_meaning(
        self, tmp_path: Path
    ) -> None:
        """Accept an accepted rating through the released EA command.

        Assumptions:
            The fixture commit is SSH-signed by the principal named in the
            allowed-signers file and carries the exact acceptance trailer.
        Criteria:
            EA reports accepted only for the matching mapped signer and exact
            trailer, using the versioned rating-acceptance result protocol.

        Trace: FR-027-AC-1
        """
        repository, allowed_signers = signed_rating_repository(tmp_path)
        output, result = run_rating_acceptance(repository, allowed_signers)

        assert output.returncode == 0, output.stderr
        assert len(result["results"]) == 1
        assert result["results"][0]["status"] == "accepted"
        assert result["results"][0]["reason"] is None
        assert result["results"][0]["commit"]

    @pytest.mark.trace("FR-027-AC-15")
    def test_released_ea_acceptance_requires_matching_signer_and_exact_trailer(
        self, tmp_path: Path
    ) -> None:
        """Require matching signer identity and meaning for an accepted rating.

        Assumptions:
            The positive case is accepted; each negative case changes only the
            verified principal or the commit's meaning trailer.
        Criteria:
            A mismatched signer or a non-exact trailer makes an accepted
            rating not_accepted.

        Trace: FR-027-AC-15
        """
        valid_repo, valid_signers = signed_rating_repository(tmp_path / "valid")
        valid_output, valid_result = run_rating_acceptance(valid_repo, valid_signers)
        assert valid_output.returncode == 0, valid_output.stderr
        assert valid_result["results"][0]["status"] == "accepted"

        mismatch_repo, mismatch_signers = signed_rating_repository(
            tmp_path / "mismatch", allowed_principal="bob@example.test"
        )
        mismatch_output, mismatch_result = run_rating_acceptance(
            mismatch_repo, mismatch_signers
        )
        assert mismatch_output.returncode == 1, mismatch_output.stderr
        assert mismatch_result["results"][0]["status"] == "not_accepted"
        assert mismatch_result["results"][0]["reason"] == "principal_mismatch"

        trailer_repo, trailer_signers = signed_rating_repository(
            tmp_path / "trailer", include_trailer=False
        )
        trailer_output, trailer_result = run_rating_acceptance(
            trailer_repo, trailer_signers
        )
        assert trailer_output.returncode == 1, trailer_output.stderr
        assert trailer_result["results"][0]["status"] == "not_accepted"
        assert trailer_result["results"][0]["reason"] == "meaning_missing"

    @pytest.mark.trace("FR-027-AC-2")
    def test_released_ea_refuses_an_unsigned_rating_commit(
        self, tmp_path: Path
    ) -> None:
        """Report an unsigned rating commit as not accepted.

        Assumptions:
            The rating is committed without an SSH signature.
        Criteria:
            The released command exits 1 and names the unsigned condition.

        Trace: FR-027-AC-2
        """
        repository, allowed_signers = signed_rating_repository(tmp_path, signed=False)
        output, result = run_rating_acceptance(repository, allowed_signers)

        assert output.returncode == 1, output.stderr
        assert result["results"][0]["status"] == "not_accepted"
        assert result["results"][0]["reason"] == "unsigned"

    @pytest.mark.trace("FR-027-AC-3")
    def test_released_ea_refuses_a_signature_without_a_mapped_principal(
        self, tmp_path: Path
    ) -> None:
        """Report a valid signature from an unmapped key as not accepted.

        Assumptions:
            Allowed-signers maps a different key from the one that signed the
            rating commit.
        Criteria:
            The released command names the signer mapping failure.

        Trace: FR-027-AC-3
        """
        repository, allowed_signers = signed_rating_repository(
            tmp_path, map_signing_key=False
        )
        output, result = run_rating_acceptance(repository, allowed_signers)

        assert output.returncode == 1, output.stderr
        assert result["results"][0]["status"] == "not_accepted"
        assert result["results"][0]["reason"] == "signer_unmapped"

    @pytest.mark.trace("FR-027-AC-4")
    def test_released_ea_refuses_a_mapped_principal_that_differs_from_rated_by(
        self, tmp_path: Path
    ) -> None:
        """Refuse a valid signature mapped to the wrong named principal.

        Assumptions:
            The signature key is trusted but allowed-signers maps it to Bob;
            the rating names Alice in `rated_by`.
        Criteria:
            EA reports not_accepted with the principal mismatch reason.

        Trace: FR-027-AC-4
        """
        repository, allowed_signers = signed_rating_repository(
            tmp_path, allowed_principal="bob@example.test"
        )
        output, result = run_rating_acceptance(repository, allowed_signers)

        assert output.returncode == 1, output.stderr
        assert result["results"][0]["status"] == "not_accepted"
        assert result["results"][0]["reason"] == "principal_mismatch"

    @pytest.mark.trace("FR-027-AC-5")
    def test_released_ea_refuses_a_signed_rating_without_the_exact_trailer(
        self, tmp_path: Path
    ) -> None:
        """Refuse an otherwise valid signed rating without its meaning trailer.

        Assumptions:
            The rating commit is signed by the mapped `rated_by` principal.
        Criteria:
            EA reports not_accepted with reason `meaning_missing`.

        Trace: FR-027-AC-5
        """
        repository, allowed_signers = signed_rating_repository(
            tmp_path, include_trailer=False
        )
        output, result = run_rating_acceptance(repository, allowed_signers)

        assert output.returncode == 1, output.stderr
        assert result["results"][0]["status"] == "not_accepted"
        assert result["results"][0]["reason"] == "meaning_missing"

    @pytest.mark.trace("FR-027-AC-6")
    def test_released_ea_uses_the_same_signature_conditions_for_both_scopes(
        self, tmp_path: Path
    ) -> None:
        """Apply one mapped signed commit to supplier and adopter ratings.

        Assumptions:
            Both rating records are in one commit signed by the shared named
            principal with the required trailer.
        Criteria:
            EA accepts both scopes, and the schema stores no commit identity.

        Trace: FR-027-AC-6
        """
        repository, allowed_signers = signed_rating_repository(
            tmp_path, scopes=("supplier", "adopter")
        )
        output, result = run_rating_acceptance(repository, allowed_signers)
        schema = frontmatter_schema("feature-risk-rating-frontmatter.schema.json")

        assert output.returncode == 0, output.stderr
        assert [item["status"] for item in result["results"]] == [
            "accepted",
            "accepted",
        ]
        assert not {"commit_id", "digest"} & set(schema["properties"])

        adopter_path = repository / "spec/validation/FRR-002.md"
        adopter_path.write_text(
            adopter_path.read_text().replace(
                '"rated_by": "alice@example.test"',
                '"rated_by": "bob@example.test"',
            )
        )
        staged = run_git(repository, "add", "spec/validation/FRR-002.md")
        assert staged.returncode == 0, staged.stderr
        committed = run_git(
            repository,
            "commit",
            "--quiet",
            "-S",
            "-m",
            "update adopter rating",
            "-m",
            "Signed-off-meaning: feature-risk-rating-accepted",
        )
        assert committed.returncode == 0, committed.stderr
        output, result = run_rating_acceptance(repository, allowed_signers)

        assert output.returncode == 1, output.stderr
        assert [item["status"] for item in result["results"]] == [
            "accepted",
            "not_accepted",
        ]
        assert result["results"][1]["reason"] == "principal_mismatch"

    @pytest.mark.trace("FR-027-AC-11")
    def test_released_ea_fails_closed_for_unavailable_and_malformed_signers(
        self, tmp_path: Path
    ) -> None:
        """Never accept when allowed-signers input is missing or malformed.

        Assumptions:
            The rating itself is signed-valid and carries the exact trailer.
        Criteria:
            Missing and malformed allowed-signers inputs both produce
            not_accepted, never a successful FR-037 invalid-input response.

        Trace: FR-027-AC-11
        """
        for malformed in (False, True):
            case = tmp_path / ("malformed" if malformed else "missing")
            case.mkdir()
            repository, allowed_signers = signed_rating_repository(case)
            allowed_signers.unlink()
            if malformed:
                allowed_signers.mkdir()

            output, result = run_rating_acceptance(repository, allowed_signers)

            assert output.returncode == 1, output.stderr
            assert result["results"][0]["status"] == "not_accepted"
            assert result["results"][0]["reason"] == "unverifiable"

        unreadable_case = tmp_path / "unreadable"
        repository, allowed_signers = signed_rating_repository(unreadable_case)
        allowed_signers.chmod(0)
        unreadable = allowed_signers
        if os.access(unreadable, os.R_OK):
            unreadable = Path("/proc/kcore")
        assert (
            unreadable.is_file()
        ), "no unreadable allowed-signers fixture is available"
        assert not os.access(
            unreadable, os.R_OK
        ), "the unreadable allowed-signers fixture is readable in this environment"
        output, result = run_rating_acceptance(repository, unreadable)

        assert output.returncode == 1, output.stderr
        assert result["results"][0]["status"] == "not_accepted"
        assert result["results"][0]["reason"] == "unverifiable"

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

    def test_validation_report_owner_is_named_in_the_requirements(self) -> None:
        """Keep the Quoin report ownership references explicit in the requirements.

        Assumptions:
            Quoin FR-217 and FR-220 own the report and configuration index.
        Criteria:
            FR-027 assigns report production and version-index entries to those
            requirements.

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

    @pytest.mark.trace("NFR-002-AC-1", "NFR-002-M-1", "NFR-003-AC-1")
    def test_authorship_and_computed_decision_boundaries_are_schema_visible(
        self,
    ) -> None:
        """Keep human authorship and the absence of computed decisions explicit.

        Assumptions:
            The schemas and TypeSpec output are committed module data.
        Criteria:
            `status` is required; generated decision fields are absent; and
            the record model contains no commit identity for acceptance.

        Trace: NFR-002-AC-1, NFR-002-M-1, NFR-003-AC-1
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
