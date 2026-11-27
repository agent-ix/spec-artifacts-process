"""Command-level supplier rating reports for FR-026."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from conftest import EXAMPLES_DIR, REPO_ROOT


def rating_text(rating_id: str, feature_id: str) -> str:
    """Build a supplier rating that targets one local functional requirement."""
    return (
        (EXAMPLES_DIR / "FeatureRiskRating.md")
        .read_text()
        .replace("FRR-001", rating_id)
        .replace("FR-009", feature_id)
    )


def command_repo(tmp_path: Path, feature_ids: tuple[str, ...]) -> Path:
    """Create a non-Git spec bundle for the installed Quoin command."""
    spec = tmp_path / "repo" / "spec"
    functional = spec / "functional"
    ratings = spec / "ratings"
    functional.mkdir(parents=True)
    ratings.mkdir()
    template = (
        REPO_ROOT / "spec/functional/FR-024-intended-use-archetype.md"
    ).read_text()
    for feature_id in feature_ids:
        source_id = template.splitlines()[1].split(":", 1)[1].strip().strip('"')
        (functional / f"{feature_id}-feature.md").write_text(
            template.replace(source_id, feature_id)
        )
    return tmp_path / "repo"


def run_ratings(
    repo: Path, tmp_path: Path, *args: str
) -> subprocess.CompletedProcess[str]:
    """Run the published command with isolated config and no project config."""
    return subprocess.run(
        [
            "quoin",
            "validation",
            "ratings",
            "--repo",
            str(repo),
            "--repo-id",
            "agent-ix/spec-artifacts-process",
            "--config-root",
            str(tmp_path / "config"),
            "--no-project-config",
            *args,
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )


class TestFeatureRiskRatingCommand:
    """Exercise the report command against isolated repository bundles."""

    @pytest.mark.trace("FR-026-AC-4")
    @pytest.mark.trace("FR-026-AC-8")
    @pytest.mark.trace("FR-026-AC-9")
    @pytest.mark.trace("FR-026-AC-10")
    @pytest.mark.trace("FR-026-AC-13")
    @pytest.mark.trace("FR-026-AC-14")
    @pytest.mark.trace("FR-026-AC-16")
    def test_duplicate_report_shape_sorting_and_read_only_behavior(
        self, tmp_path: Path
    ) -> None:
        """Report all duplicate supplier ratings in deterministic, read-only output.

        Assumptions:
            FR-002 has two supplier ratings and FR-001 has one; files are
            deliberately created in an order different from lexical order.
        Criteria:
            Human and JSON output identify duplicates, preserve exact report
            shapes, sort ids, and leave every input path and byte unchanged.
        Trace: FR-026-AC-4, FR-026-AC-8, FR-026-AC-9, FR-026-AC-10,
        FR-026-AC-13, FR-026-AC-14, FR-026-AC-16
        """
        repo = command_repo(tmp_path, ("FR-002", "FR-003", "FR-001"))
        ratings = repo / "spec" / "ratings"
        (ratings / "z-rating.md").write_text(rating_text("FRR-902", "FR-002"))
        (ratings / "a-rating.md").write_text(rating_text("FRR-901", "FR-002"))
        (ratings / "single.md").write_text(rating_text("FRR-100", "FR-001"))

        def snapshot() -> dict[str, bytes | None]:
            """Record all repository paths and file bytes."""
            return {
                path.relative_to(repo).as_posix(): (
                    path.read_bytes() if path.is_file() else None
                )
                for path in repo.rglob("*")
            }

        before = snapshot()

        json_result = run_ratings(repo, tmp_path, "--json")
        human_result = run_ratings(repo, tmp_path)

        assert json_result.returncode == 1
        report = json.loads(json_result.stdout)
        assert set(report) == {"features", "unreadable"}
        assert report["unreadable"] == []
        assert report["features"] == [
            {"feature_id": "FR-001", "status": "rated", "rating_ids": ["FRR-100"]},
            {
                "feature_id": "FR-002",
                "status": "rated_more_than_once",
                "rating_ids": ["FRR-901", "FRR-902"],
            },
            {
                "feature_id": "FR-003",
                "status": "unrated",
                "rating_ids": [],
            },
        ]
        assert all(
            set(row) == {"feature_id", "status", "rating_ids"}
            for row in report["features"]
        )
        assert "FR-001: rated (rating IDs: FRR-100)" in human_result.stdout
        assert (
            "FR-002: rated_more_than_once (rating IDs: FRR-901, FRR-902)"
            in human_result.stdout
        )
        assert "FR-003: unrated (rating IDs: none)" in human_result.stdout
        assert human_result.returncode == 1
        after = snapshot()
        assert after == before

    @pytest.mark.trace("FR-026-AC-6", "FR-026-AC-7")
    def test_non_git_bundle_counts_supplier_and_excludes_adopter(
        self, tmp_path: Path
    ) -> None:
        """Count supplier ratings in a plain directory and ignore adopter reratings.

        Assumptions:
            The repository has no Git metadata and contains one supplier and
            one adopter rating for the same FR.
        Criteria:
            The command reads the spec bundle without a remote and reports one
            supplier rating rather than a duplicate.
        Trace: FR-026-AC-6, FR-026-AC-7
        """
        repo = command_repo(tmp_path, ("FR-001",))
        ratings = repo / "spec" / "ratings"
        ratings.joinpath("supplier.md").write_text(rating_text("FRR-100", "FR-001"))
        adopter = rating_text("FRR-200", "FR-001").replace(
            "scope: supplier", "scope: adopter\nintended_use: Integration context"
        )
        adopter = adopter.replace(
            "  - target: ix://agent-ix/spec-artifacts-process/IU-001\n"
            "    type: uses_intended_use\n",
            "",
        ).replace(
            "ix://agent-ix/spec-artifacts-process/FR-001\n    type: rates_feature",
            "ix://agent-ix/spec-artifacts-process/FRR-100\n    type: re_rates",
        )
        ratings.joinpath("adopter.md").write_text(adopter)

        result = run_ratings(repo, tmp_path, "--json")

        assert not (repo / ".git").exists()
        assert result.returncode == 0, result.stderr
        assert json.loads(result.stdout)["features"] == [
            {"feature_id": "FR-001", "status": "rated", "rating_ids": ["FRR-100"]}
        ]

    @pytest.mark.trace("FR-026-AC-8")
    def test_human_output_describes_empty_feature_set(self, tmp_path: Path) -> None:
        """Emit the specified human message when the bundle has no FRs.

        Assumptions:
            The spec directory exists but its functional directory is empty.
        Criteria:
            Human output says no functional requirements were found.
        Trace: FR-026-AC-8
        """
        repo = command_repo(tmp_path, ())

        result = run_ratings(repo, tmp_path)

        assert result.returncode == 0, result.stderr
        assert (
            "supplier feature ratings: no functional requirements found"
            in result.stdout
        )

    @pytest.mark.trace("FR-026-AC-12")
    @pytest.mark.trace("FR-026-AC-11")
    def test_unreadable_inputs_make_both_output_modes_partial(
        self, tmp_path: Path
    ) -> None:
        """Surface malformed FR and rating documents in both output formats.

        Assumptions:
            One valid FR is present alongside malformed Markdown in both input
            classes, so the command can return a partial report.
        Criteria:
            Both output modes report repository-relative paths and nonempty
            reasons; the command exits with status one for the partial report.
        Trace: FR-026-AC-11, FR-026-AC-12
        """
        repo = command_repo(tmp_path, ("FR-001",))
        (repo / "spec" / "functional" / "FR-000-broken.md").write_text(
            "---\nid: [\n---\n"
        )
        (repo / "spec" / "ratings" / "broken.md").write_text("---\nid: [\n---\n")

        json_result = run_ratings(repo, tmp_path, "--json")
        human_result = run_ratings(repo, tmp_path)

        assert json_result.returncode == 1
        unreadable = json.loads(json_result.stdout)["unreadable"]
        assert {item["path"] for item in unreadable} == {
            "spec/functional/FR-000-broken.md",
            "spec/ratings/broken.md",
        }
        assert all(
            set(item) == {"path", "reason"} and item["reason"].strip()
            for item in unreadable
        )
        assert human_result.returncode == 1
        human_unreadable = {}
        for line in human_result.stdout.splitlines():
            if line.startswith("unreadable: "):
                path, separator, reason = line.removeprefix("unreadable: ").partition(
                    ": "
                )
                assert separator and reason.strip(), line
                human_unreadable[path] = reason
        assert set(human_unreadable) == {
            "spec/functional/FR-000-broken.md",
            "spec/ratings/broken.md",
        }
        assert all(reason.strip() for reason in human_unreadable.values())

    @pytest.mark.trace("FR-026-AC-3")
    def test_wrong_kind_rates_feature_target_is_reported(self, tmp_path: Path) -> None:
        """Reject a resolved rates_feature edge to a non-FR artifact.

        Assumptions:
            The bundle has one valid FR, one IntendedUse target, and a supplier
            rating whose rates_feature edge points at that IntendedUse.
        Criteria:
            The ratings command exits partial and reports target-kind-mismatch
            with the invalid target and its actual kind.
        Trace: FR-026-AC-3
        """
        repo = command_repo(tmp_path, ("FR-001",))
        intended_use = repo / "spec" / "intended-use" / "IU-001.md"
        intended_use.parent.mkdir(parents=True)
        intended_use.write_text(
            "---\nid: IU-001\ntype: IntendedUse\n---\nIntended use.\n"
        )
        rating = rating_text("FRR-100", "FR-001").replace(
            "ix://agent-ix/spec-artifacts-process/FR-001\n    type: rates_feature",
            "ix://agent-ix/spec-artifacts-process/IU-001\n    type: rates_feature",
        )
        (repo / "spec" / "ratings" / "wrong-kind.md").write_text(rating)

        result = run_ratings(repo, tmp_path)

        assert result.returncode == 1
        diagnostics = json.loads(result.stderr)
        assert isinstance(diagnostics, list), diagnostics
        assert len(diagnostics) == 1, result.stderr
        finding = diagnostics[0]
        assert finding["code"] == "target-kind-mismatch"
        assert finding["context"]["target"] == (
            "ix://agent-ix/spec-artifacts-process/IU-001"
        )
        assert finding["context"]["actual_kind"] == "IntendedUse"

    @pytest.mark.trace("FR-026-AC-15")
    @pytest.mark.parametrize("spec_is_file", [False, True])
    def test_missing_or_non_directory_spec_is_command_error_without_report(
        self, tmp_path: Path, spec_is_file: bool
    ) -> None:
        """Reject a missing or non-directory spec bundle before reporting rows.

        Assumptions:
            The requested repository exists, but `spec/` is absent or a file.
        Criteria:
            The command returns a nonzero CLI error and emits no partial report.
        Trace: FR-026-AC-15
        """
        repo = tmp_path / "repo"
        repo.mkdir()
        if spec_is_file:
            (repo / "spec").write_text("not a directory")

        result = run_ratings(repo, tmp_path, "--json")

        assert result.returncode != 0
        assert result.stdout.strip() == ""
        assert result.stderr.strip()
