"""The RoleSpec and Rubric archetypes and their fixtures (FR-020 to FR-023).

Every negative fixture under `tests/fixtures/roles/invalid/` is one failing
case, so each case is checked for the cell, field or id that names it rather than
for a bare nonzero exit. The corpus fixtures under `tests/fixtures/roles/corpus/`
are whole repositories, because reference resolution and minting read a corpus.

The tests below exercise the public Quire commands for FR-021's parented
criteria, unused-metric and all-judgement warnings, and cross-table/id
uniqueness assertions. The module declares the data model; Quire implements the
checks.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest
from conftest import PACKAGE_ROOT, SKELETONS_DIR, quire_validate

FIXTURES = PACKAGE_ROOT.parent / "tests" / "fixtures" / "roles"
VALID = FIXTURES / "valid"
INVALID = FIXTURES / "invalid"
CORPUS = FIXTURES / "corpus"

MINDER = VALID / "spec" / "roles" / "minder.md"
RUBRIC = VALID / "spec" / "rubrics" / "rubric-minder.md"

EVALUATIONS = [
    "MIND-R01-E1",
    "MIND-R02-E1",
    "MIND-R02-E2",
    "MIND-R03-E1",
    "MIND-R04-E1",
    "MIND-R05-E1",
    "MIND-R06-E1",
]
RULES = [f"MIND-R0{n}" for n in range(1, 7)]
METRICS = ["MIND-M01", "MIND-M02"]


def validate(path: Path, scope: Path = INVALID) -> subprocess.CompletedProcess:
    return quire_validate(path, scope=scope)


def messages(result: subprocess.CompletedProcess, path: Path) -> list[str]:
    """The diagnostics of one document with its path removed.

    A fixture's file name can contain the cell under test, so a substring check
    on the whole line would hold whatever the diagnostic says.
    """
    prefix = f"{path}: "
    return [
        line[len(prefix) :]
        for line in result.stderr.splitlines()
        if line.startswith(prefix)
    ]


def fails_naming(name: str, needle: str | tuple[str, ...]) -> None:
    """The fixture fails, and one diagnostic carries every text in `needle`."""
    needles = (needle,) if isinstance(needle, str) else needle
    path = INVALID / f"{name}.md"
    result = validate(path)
    assert result.returncode != 0, result.stderr
    found = messages(result, path)
    assert found, result.stderr
    assert any(all(n in m for n in needles) for m in found), found


def validates(path: Path, scope: Path) -> None:
    result = validate(path, scope)
    assert result.returncode == 0, result.stderr
    assert messages(result, path) == [], result.stderr


def coverage(corpus: Path) -> dict:
    result = subprocess.run(
        [
            "quire",
            "coverage",
            "--scope",
            str(corpus),
            "--module",
            str(PACKAGE_ROOT),
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return json.loads(result.stdout)


def bundle(corpus: Path) -> subprocess.CompletedProcess:
    """`quire validate --okf` over a corpus: the run that resolves references."""
    return subprocess.run(
        [
            "quire",
            "validate",
            "--okf",
            "--scope",
            str(corpus),
            "--module",
            str(PACKAGE_ROOT),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def matrix(corpus: Path) -> subprocess.CompletedProcess:
    """Run the public matrix JSON command over one consuming fixture."""
    return subprocess.run(
        [
            "quire",
            "matrix",
            "--scope",
            str(corpus),
            "--module",
            str(PACKAGE_ROOT),
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def valid_consumer(tmp_path: Path) -> Path:
    """Copy the valid RoleSpec bundle into an isolated consuming repository."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    consumer = tmp_path / "consumer"
    shutil.copytree(VALID, consumer)
    return consumer


def dangling(corpus: Path) -> list[str]:
    return [
        line
        for line in bundle(corpus).stderr.splitlines()
        if "[dangling-trace-reference]" in line
    ]


def strict(path: Path, scope: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            "quire",
            "validate",
            "--strict",
            "--module",
            str(PACKAGE_ROOT),
            "--scope",
            str(scope),
            str(path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def manifest_type(manifest: dict, name: str) -> dict:
    return next(t for t in manifest["artifact_types"] if t["name"] == name)


# Each case: fixture name and the text the diagnostic must carry.
ROLE_SPEC_CASES: dict[str, list[tuple[str, str | tuple[str, ...]]]] = {
    "FR-020-AC-1": [
        ("missing-evaluations", "evaluations"),
        ("missing-metrics", "metrics"),
        ("missing-objectives", "objectives"),
        ("missing-rules", "rules"),
        ("missing-column", "Metrics"),
        ("metrics-missing-column", "Direction"),
        ("rules-missing-column", "Source"),
        ("evaluations-missing-column", "Cadence"),
        ("metrics-misordered-columns", "do not match asserted columns"),
        ("objectives-misordered-columns", "do not match asserted columns"),
        ("rules-misordered-columns", "do not match asserted columns"),
        ("evaluations-misordered-columns", "do not match asserted columns"),
        ("missing-version", "version"),
        ("missing-role", "role"),
        ("missing-id", '"id" is a required property'),
        ("empty-table", "at least 1"),
        ("empty-metrics", "at least 1"),
        ("empty-rules", "at least 1"),
        ("empty-evaluations", "at least 1"),
        ("metric-empty-name", ("MIND-M01", "'Name'")),
        ("metric-empty-unit", ("MIND-M01", "'Unit'")),
        ("metric-empty-target", ("MIND-M01", "'Target'")),
        ("objective-empty-objective", ("MIND-O01", "'Objective'")),
        ("rule-empty-rule", ("MIND-R01", "'Rule'")),
        ("rule-empty-objective", ("MIND-R01", "'Objective'")),
        ("rule-empty-class", ("MIND-R01", "'Class'")),
        ("rule-empty-source", ("MIND-R01", "'Source'")),
        ("evaluation-empty-rule", ("MIND-R06-E1", "'Rule'")),
    ],
    "FR-020-AC-2": [
        ("bad-eval-evidence-source", "telepathy"),
        ("bad-metric-evidence-source", "telepathy"),
        ("bad-direction", "sideways"),
        ("bad-cadence", "hourly"),
        ("bad-method", "heuristic"),
    ],
    "FR-020-AC-3": [
        ("deterministic-empty-query", ("MIND-R06-E1", "allOf/0/then")),
        ("deterministic-rubric-ref", ("MIND-R06-E1", "allOf/0/then")),
        ("deterministic-free-text", ("MIND-R06-E1", "allOf/0/then")),
        ("judgement-not-rubric-ref", ("MIND-R02-E2", "allOf/1/then/pattern")),
        ("empty-trigger", "'Trigger'"),
        ("free-text-trigger", "when the loop is removed"),
        ("free-text-metric-query", "p90 of latency"),
    ],
    "FR-020-AC-4": [("judgement-tick", ("MIND-R02-E2", "allOf/1/then/not"))],
    "FR-020-AC-5": [
        ("metric-id-wrong-prefix", "OTHR-M02"),
        ("rule-id-bad-shape", "MIND-R6"),
        ("evaluation-id-bad-shape", "MIND-R06-X1"),
        ("objective-id-bad-shape", "MIND-M02"),
    ],
    "FR-020-AC-6": [
        ("bad-comparator", "'=='"),
        ("non-numeric-value", "'none'"),
        ("empty-unit", "'Unit'"),
    ],
    "FR-020-AC-7": [
        ("judgement-wrong-evaluator", ("MIND-R02-E2", "allOf/1/then/pattern")),
        ("deterministic-wrong-evaluator", ("MIND-R01-E1", "allOf/0/then")),
    ],
    "FR-020-AC-8": [
        ("version-zero", "version"),
        ("version-not-integer", "version"),
        ("id-lower-case", "at id"),
        ("id-too-long", "at id"),
    ],
    "FR-021-AC-4": [("objective-empty-metrics", "MIND-O02")],
}

RUBRIC_CASES: dict[str, list[tuple[str, str | tuple[str, ...]]]] = {
    "FR-023-AC-1": [
        ("rubric-missing-version", "version"),
        ("rubric-missing-id", '"id" is a required property'),
        ("rubric-missing-checks", "checks"),
        ("rubric-missing-column", "Scale"),
        ("rubric-empty-table", "at least 1"),
        ("rubric-empty-check", ("rubric-minder@1#failed-probe", "'Check'")),
        ("rubric-empty-scale", ("rubric-minder@1#failed-probe", "'Scale'")),
        ("rubric-bad-id", "at id"),
        ("rubric-version-zero", "version"),
    ],
    "FR-023-AC-2": [
        ("rubric-check-wrong-name", "rubric-other@1#failed-probe"),
        ("rubric-check-wrong-version", "rubric-minder@1#failed-probe"),
        ("rubric-check-bad-slug", "rubric-minder@1#Failed_Probe"),
    ],
}


def _params(cases, ac: str):
    return [pytest.param(n, needle, id=n) for n, needle in cases[ac]]


@pytest.mark.trace("FR-020-AC-1")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-1"))
def test_missing_table_column_or_member_fails_naming_it(name: str, needle):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-1", "FR-022-AC-4")
def test_the_worked_minder_spec_validates():
    validates(MINDER, VALID)


@pytest.mark.trace("FR-020-AC-2")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-2"))
def test_a_value_outside_a_closed_enum_fails_naming_the_cell(name: str, needle):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-3")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-3"))
def test_query_references_and_rubric_references_are_checked_by_method(
    name: str, needle
):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-4")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-4"))
def test_a_judgement_evaluation_never_runs_every_tick(name: str, needle):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-11")
def test_a_role_spec_may_carry_a_purpose_section():
    text = MINDER.read_text()
    assert "\n## Purpose\n" in text
    validates(MINDER, VALID)


@pytest.mark.trace("FR-020-AC-12")
def test_the_role_spec_links_are_exactly_two_verbs_and_both_are_registered(manifest):
    assert manifest_type(manifest, "RoleSpec")["allowed_links"] == [
        "satisfies",
        "depends_on",
    ]
    assert {"satisfies", "depends_on"} <= set(manifest["edge_types"])


@pytest.mark.trace("FR-020-AC-12")
def test_another_relationship_verb_fails_under_strict_and_valid_specs_pass():
    # Without `--strict` the engine reports an unlisted verb as a warning
    # (`disallowed-edge-type`, exit 0); that is a quire-rs gap (SWM-248), so the
    # failure is pinned under `--strict`.
    path = INVALID / "bad-link-verb.md"
    result = strict(path, INVALID)
    assert result.returncode == 3, result.stderr
    assert any(
        str(path) in line
        and "[disallowed-edge-type]" in line
        and "'supersedes'" in line
        for line in result.stderr.splitlines()
    ), result.stderr
    ok = strict(MINDER, VALID)
    assert ok.returncode == 0, ok.stderr


@pytest.mark.trace("FR-020-AC-5")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-5"))
def test_a_row_id_with_the_wrong_prefix_or_shape_fails_naming_the_id(name: str, needle):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-6")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-6"))
def test_a_threshold_is_a_known_comparator_a_number_and_a_unit(name: str, needle):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-7")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-7"))
def test_the_evaluator_follows_the_method(name: str, needle):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-8")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-8"))
def test_version_and_id_have_their_declared_shape(name: str, needle):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-10")
def test_the_role_spec_skeleton_validates():
    validates(SKELETONS_DIR / "RoleSpec.md", SKELETONS_DIR)


@pytest.mark.trace("FR-020-AC-10", "FR-023-AC-5")
def test_every_negative_fixture_is_one_declared_case():
    declared = {
        name
        for cases in (ROLE_SPEC_CASES, RUBRIC_CASES)
        for group in cases.values()
        for name, _ in group
    } | {"bad-link-verb", "rubric-bad-link-verb", "shape-and-record-defect"}
    assert {p.stem for p in INVALID.glob("*.md")} == declared


@pytest.mark.trace("FR-021-AC-4")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-021-AC-4"))
def test_an_objective_with_no_metric_fails_naming_the_objective(name: str, needle):
    fails_naming(name, needle)


@pytest.mark.trace("FR-021-AC-2")
def test_matrix_json_reports_a_rule_without_any_evaluation(tmp_path: Path):
    """Show an evaluation-free rule as a parent with no criterion.

    Assumptions:
        The consumer fixture is valid except that MIND-R06 has no evaluation.
    Criteria:
        Quire matrix JSON reports MIND-R06 with an empty criterion list.

    Trace: FR-021-AC-2
    """
    consumer = valid_consumer(tmp_path)
    role_spec = consumer / "spec" / "roles" / "minder.md"
    source = role_spec.read_text()
    evaluation = (
        "| MIND-R06-E1 | MIND-R06 | hook-events | "
        "hooks.minder_loop_removal_events | deterministic | "
        "hooks.minder_loop_removed_without_owner_instruction | evaluator | = | "
        "0 | events | session-end |"
    )
    assert source.count(evaluation) == 1
    role_spec.write_text(source.replace(evaluation + "\n", ""))

    result = matrix(consumer)

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    groups = report.get("parented_target_groups")
    assert isinstance(groups, list), report
    group = next(
        (
            item
            for item in groups
            if item.get("parent_target") == "role-rule"
            and item.get("parent_id") == "MIND-R06"
        ),
        None,
    )
    assert group is not None, report
    assert group.get("child_target") == "role-evaluation", group
    assert group.get("child_ids") == [], group


@pytest.mark.trace("FR-021-AC-5")
def test_unreferenced_metric_warns_without_changing_validation_status(
    tmp_path: Path,
):
    """Warn about a metric that no objective names without failing validation.

    Assumptions:
        MIND-M02 remains a declared metric but both objectives name MIND-M01.
    Criteria:
        Quire emits the unused-target warning naming MIND-M02 and exits zero.

    Trace: FR-021-AC-5
    """
    consumer = valid_consumer(tmp_path)
    role_spec = consumer / "spec" / "roles" / "minder.md"
    source = role_spec.read_text()
    reference = "| MIND-O02 | Every detected problem is acted on quickly | MIND-M02 |"
    assert source.count(reference) == 1
    role_spec.write_text(
        source.replace(reference, reference.replace("MIND-M02", "MIND-M01"))
    )

    result = bundle(consumer)

    assert result.returncode == 0, result.stderr
    assert "target-id-unreferenced" in result.stderr, result.stderr
    warning = next(
        (
            line
            for line in result.stderr.splitlines()
            if "target-id-unreferenced" in line and "MIND-M02" in line
        ),
        None,
    )
    assert warning is not None, result.stderr


@pytest.mark.trace("FR-021-AC-6")
def test_metric_query_must_differ_from_evaluation_query_but_may_match_trigger(
    tmp_path: Path,
):
    """Reject query equality while allowing equality with an evaluation trigger.

    Assumptions:
        Both variants retain the valid RoleSpec and rubric reference structure.
    Criteria:
        Query equality fails naming MIND-M01 and MIND-R01-E1; Trigger-only
        equality validates successfully.

    Trace: FR-021-AC-6
    """
    query_consumer = valid_consumer(tmp_path / "query")
    query_spec = query_consumer / "spec" / "roles" / "minder.md"
    query_source = query_spec.read_text()
    metric_query = "ledger.idle_capacity_minutes_with_ready_work"
    evaluation_query = "ledger.unknown_lane_not_acted_ticks"
    assert query_source.count(metric_query) == 1
    query_spec.write_text(query_source.replace(metric_query, evaluation_query))

    query_result = bundle(query_consumer)

    assert query_result.returncode != 0, query_result.stderr
    mismatch = next(
        (
            line
            for line in query_result.stderr.splitlines()
            if "MIND-M01" in line and "MIND-R01-E1" in line
        ),
        None,
    )
    assert mismatch is not None, query_result.stderr

    trigger_consumer = valid_consumer(tmp_path / "trigger")
    trigger_spec = trigger_consumer / "spec" / "roles" / "minder.md"
    trigger_source = trigger_spec.read_text()
    trigger_query = "ledger.unknown_lane_ticks"
    assert trigger_source.count(metric_query) == 1
    trigger_spec.write_text(trigger_source.replace(metric_query, trigger_query))

    trigger_result = bundle(trigger_consumer)

    assert trigger_result.returncode == 0, trigger_result.stderr


@pytest.mark.trace("FR-021-AC-7")
def test_duplicate_id_in_one_role_spec_table_fails_naming_the_id(
    tmp_path: Path,
):
    """Reject duplicate metric ids within the same RoleSpec table.

    Assumptions:
        MIND-M01 and MIND-M02 are valid ids before the second id is changed.
    Criteria:
        Quire validation fails with a duplicate-id diagnostic naming MIND-M01.

    Trace: FR-021-AC-7
    """
    consumer = valid_consumer(tmp_path)
    role_spec = consumer / "spec" / "roles" / "minder.md"
    source = role_spec.read_text()
    duplicate_row = "| MIND-M02 | Detection-to-action latency, p90 |"
    assert source.count(duplicate_row) == 1
    role_spec.write_text(
        source.replace(duplicate_row, duplicate_row.replace("MIND-M02", "MIND-M01"))
    )

    result = bundle(consumer)

    assert result.returncode != 0, result.stderr
    duplicate = next(
        (
            line
            for line in result.stderr.splitlines()
            if "MIND-M01" in line and "duplicate" in line.lower()
        ),
        None,
    )
    assert duplicate is not None, result.stderr


@pytest.mark.trace("FR-021-AC-11")
def test_all_judgement_evaluations_warn_without_changing_validation_status(
    tmp_path: Path,
):
    """Warn when every evaluation under a rule uses judgement.

    Assumptions:
        MIND-R02's deterministic evaluation becomes judgement with a valid
        rubric reference, leaving its existing judgement evaluation unchanged.
    Criteria:
        Quire emits the all-judgement warning naming MIND-R02 and exits zero.

    Trace: FR-021-AC-11
    """
    consumer = valid_consumer(tmp_path)
    role_spec = consumer / "spec" / "roles" / "minder.md"
    source = role_spec.read_text()
    deterministic = (
        "| MIND-R02-E1 | MIND-R02 | ledger | ledger.failed_probe_ticks | "
        "deterministic | ledger.probe_failure_without_defect_row | evaluator | "
        "= | 0 | ticks | tick |"
    )
    judgement = (
        "| MIND-R02-E1 | MIND-R02 | ledger | ledger.failed_probe_ticks | "
        "judgement | rubric-minder@1#failed-probe | director | >= | 2 | score | "
        "daily |"
    )
    assert source.count(deterministic) == 1
    role_spec.write_text(source.replace(deterministic, judgement))

    result = bundle(consumer)

    assert result.returncode == 0, result.stderr
    warning = next(
        (
            line
            for line in result.stderr.splitlines()
            if "parent-children-all-match" in line and "MIND-R02" in line
        ),
        None,
    )
    assert warning is not None, result.stderr


@pytest.mark.trace("FR-021-AC-1")
def test_the_trace_targets_are_declared_over_the_role_spec(manifest):
    targets = {t["name"]: t for t in manifest["traceability"]["trace_targets"]}
    sections = {
        "role-metric": "Metrics",
        "role-objective": "Objectives",
        "role-rule": "Rules",
        "role-evaluation": "Evaluations",
    }
    for name, section in sections.items():
        assert targets[name]["archetype"] == "RoleSpec"
        assert targets[name]["section"] == section
        assert targets[name]["id_column"] == "ID"
        assert {"tests/**", "tests_integration/**", "fixtures/**"} <= set(
            targets[name]["exclude"]
        )
    for name in ("role-metric", "role-objective", "role-rule"):
        assert targets[name]["evidence"] == "reference-only"
    assert "evidence" not in targets["role-evaluation"]


@pytest.mark.trace("FR-021-AC-1")
def test_the_minder_spec_mints_every_evaluation_and_references_every_rule():
    report = coverage(VALID)
    assert [m["id"] for m in report["minted_targets"]] == EVALUATIONS
    referenced = {t for row in report["unbacked_rows"] for t in row["target_ids"]}
    assert set(RULES) <= referenced


@pytest.mark.trace("FR-021-AC-12")
def test_a_metric_is_never_a_criterion():
    report = coverage(VALID)
    ids = {m["id"] for m in report["minted_targets"]}
    assert not set(METRICS) & ids
    assert not {i for i in ids if re.search(r"-[OR]\d{2}$", i)}


@pytest.mark.trace("FR-021-AC-3")
@pytest.mark.parametrize(
    "case,referencing,missing",
    [
        ("dangling-rule", "MIND-R03-E1", "MIND-R09"),
        ("dangling-objective", "MIND-R02", "MIND-O09"),
        ("dangling-metric", "MIND-O02", "MIND-M07"),
    ],
)
def test_a_reference_to_an_undefined_row_dangles(
    case: str, referencing: str, missing: str
):
    found = dangling(CORPUS / case)
    assert len(found) == 1, found
    assert f"'{missing}'" in found[0] and f"row '{referencing}'" in found[0]
    assert bundle(CORPUS / case).returncode == 3


@pytest.mark.trace("FR-021-AC-8")
def test_a_role_spec_outside_spec_mints_nothing_and_still_validates_its_shape():
    corpus = CORPUS / "outside-spec"
    report = coverage(corpus)
    assert not report.get("minted_targets")
    assert report["totals"]["total"] == 0
    path = corpus / "roles" / "minder.md"
    validates(path, corpus)


@pytest.mark.trace("FR-021-AC-10", "FR-023-AC-4")
@pytest.mark.parametrize(
    "case", ["rubric-missing", "rubric-version-stale", "rubric-slug-undefined"]
)
def test_a_rubric_reference_that_resolves_to_no_check_dangles(case: str):
    found = dangling(CORPUS / case)
    assert len(found) == 1, found
    assert "'rubric-minder@1#failed-probe'" in found[0]
    assert "row 'MIND-R02-E2'" in found[0]
    assert bundle(CORPUS / case).returncode == 3


@pytest.mark.trace("FR-021-AC-10", "FR-023-AC-3")
def test_the_rubric_reference_in_the_minder_spec_resolves():
    assert dangling(VALID) == []
    assert bundle(VALID).returncode == 0
    resolved = [
        row
        for row in coverage(VALID)["unbacked_rows"]
        if row["reference"] == "role-evaluation-rubric"
        and row["row_id"] == "MIND-R02-E2"
    ]
    assert resolved and "rubric-minder@1#failed-probe" in resolved[0]["target_ids"]


@pytest.mark.trace("FR-022-AC-3")
def test_the_role_spec_documentation_names_the_lint_owner_and_the_version_field():
    text = (SKELETONS_DIR / "RoleSpec.md").read_text()
    assert "Quoin" in text and "`version`" in text


@pytest.mark.trace("FR-023-AC-1")
def test_the_fixture_rubric_validates():
    validates(RUBRIC, VALID)


@pytest.mark.trace("FR-023-AC-1")
@pytest.mark.parametrize("name,needle", _params(RUBRIC_CASES, "FR-023-AC-1"))
def test_a_rubric_missing_a_member_table_or_column_fails_naming_it(name: str, needle):
    fails_naming(name, needle)


@pytest.mark.trace("FR-023-AC-2")
@pytest.mark.parametrize("name,needle", _params(RUBRIC_CASES, "FR-023-AC-2"))
def test_a_check_id_must_carry_the_rubric_name_version_and_a_slug(name: str, needle):
    fails_naming(name, needle)


@pytest.mark.trace("FR-023-AC-4")
def test_a_rubric_version_bump_without_renumbering_its_checks_fails():
    # `rubric-check-wrong-version` is the fixture rubric at `version: 2` with its
    # check ids untouched.
    text = (INVALID / "rubric-check-wrong-version.md").read_text()
    assert "version: 2" in text and "rubric-minder@1#" in text
    fails_naming("rubric-check-wrong-version", "rubric-minder@1#failed-probe")


@pytest.mark.trace("FR-023-AC-5")
def test_the_rubric_skeleton_validates():
    validates(SKELETONS_DIR / "Rubric.md", SKELETONS_DIR)


@pytest.mark.trace("FR-023-AC-5")
def test_another_relationship_verb_fails_a_rubric_under_strict():
    path = INVALID / "rubric-bad-link-verb.md"
    result = strict(path, INVALID)
    assert result.returncode == 3, result.stderr
    assert any(
        str(path) in line
        and "[disallowed-edge-type]" in line
        and "'supersedes'" in line
        for line in result.stderr.splitlines()
    ), result.stderr
    ok = strict(RUBRIC, VALID)
    assert ok.returncode == 0, ok.stderr


@pytest.mark.trace("FR-023-AC-1")
def test_the_rubric_manifest_entry_declares_its_check_target_and_links(manifest):
    entry = manifest_type(manifest, "Rubric")
    assert entry["allowed_links"] == ["satisfies", "depends_on"]
    targets = {t["name"]: t for t in manifest["traceability"]["trace_targets"]}
    check = targets["rubric-check"]
    assert (check["archetype"], check["section"], check["id_column"]) == (
        "Rubric",
        "Checks",
        "ID",
    )
    assert check["evidence"] == "reference-only"


@pytest.mark.trace("FR-021-AC-3")
def test_a_dangling_reference_is_an_error_by_module_declaration(manifest):
    assert manifest["grammar_severity"]["trace:dangling-trace-reference"] == "error"


def test_shape_and_record_defects_are_reported_in_two_passes():
    """The engine runs `record_validation` only after every `assert` passes, so a
    fixture with a bad cadence (assert) and a wrong evaluator (record) reports
    only the cadence until it is fixed. FR-020 asks for one run; that is a
    quire-rs gap (SWM-248), pinned here so a change in the engine is noticed."""
    path = INVALID / "shape-and-record-defect.md"
    found = messages(validate(path), path)
    assert any("'Cadence'" in m for m in found), found
    assert not any("record-invalid" in m for m in found), found


def test_each_vocabulary_and_query_pattern_is_written_once_in_the_manifest():
    text = (PACKAGE_ROOT / "manifest.yaml").read_text()
    assert text.count("relay-receipts") == 1
    assert text.count("session-end") == 1
    assert text.count("^[a-z][a-z0-9-]*\\.[a-z][a-z0-9_]*$") == 1
