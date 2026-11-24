"""The RoleSpec and Rubric archetypes and their fixtures (FR-020 to FR-023).

Every negative fixture under `tests/fixtures/roles/invalid/` is one failing
case, so each case is checked for the cell, field or id that names it rather than
for a bare nonzero exit. The corpus fixtures under `tests/fixtures/roles/corpus/`
are whole repositories, because reference resolution and minting read a corpus.

Not covered here, because the engine cannot express them yet (FR-021): criteria
parented through a column, the unused-metric and all-judgement warnings
(SWM-247), and the cross-table distinctness and id-uniqueness asserts (SWM-248).
"""

from __future__ import annotations

import json
import re
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


def fails_naming(name: str, needle: str) -> None:
    path = INVALID / f"{name}.md"
    result = validate(path)
    assert result.returncode != 0, result.stderr
    found = messages(result, path)
    assert found, result.stderr
    assert any(needle in m for m in found), found


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


def bundle_findings(corpus: Path, kind: str) -> list[str]:
    """The `kind` findings of `quire validate --okf` over a corpus.

    `--okf` reports a reference to an undefined id as a warning, so a clean exit
    does not mean there is no finding.
    """
    result = subprocess.run(
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
    return [line for line in result.stderr.splitlines() if f"[{kind}]" in line]


def dangling(corpus: Path) -> list[str]:
    return bundle_findings(corpus, "dangling-trace-reference")


def manifest_type(manifest: dict, name: str) -> dict:
    return next(t for t in manifest["artifact_types"] if t["name"] == name)


# Each case: fixture name and the text the diagnostic must carry.
ROLE_SPEC_CASES: dict[str, list[tuple[str, str]]] = {
    "FR-020-AC-1": [
        ("missing-evaluations", "evaluations"),
        ("missing-metrics", "metrics"),
        ("missing-column", "Metrics"),
        ("missing-version", "version"),
        ("missing-role", "role"),
        ("empty-table", "objectives"),
    ],
    "FR-020-AC-2": [
        ("bad-eval-evidence-source", "telepathy"),
        ("bad-metric-evidence-source", "telepathy"),
        ("bad-direction", "sideways"),
        ("bad-cadence", "hourly"),
        ("bad-method", "heuristic"),
    ],
    "FR-020-AC-3": [
        ("deterministic-empty-query", "MIND-R06-E1"),
        ("deterministic-rubric-ref", "MIND-R06-E1"),
        ("deterministic-free-text", "MIND-R06-E1"),
        ("judgement-not-rubric-ref", "MIND-R02-E2"),
        ("empty-trigger", "'Trigger'"),
        ("free-text-trigger", "when the loop is removed"),
        ("free-text-metric-query", "p90 of latency"),
    ],
    "FR-020-AC-4": [("judgement-tick", "MIND-R02-E2")],
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
        ("judgement-wrong-evaluator", "MIND-R02-E2"),
        ("deterministic-wrong-evaluator", "MIND-R01-E1"),
    ],
    "FR-020-AC-8": [
        ("version-zero", "version"),
        ("version-not-integer", "version"),
        ("id-lower-case", "at id"),
        ("id-too-long", "at id"),
    ],
    "FR-021-AC-4": [("objective-empty-metrics", "MIND-O02")],
}

RUBRIC_CASES: dict[str, list[tuple[str, str]]] = {
    "FR-023-AC-1": [
        ("rubric-missing-version", "version"),
        ("rubric-missing-checks", "checks"),
        ("rubric-missing-column", "Scale"),
        ("rubric-empty-table", "checks"),
        ("rubric-bad-id", "at id"),
        ("rubric-version-zero", "version"),
    ],
    "FR-023-AC-2": [
        ("rubric-check-wrong-name", "rubric-other@1#failed-probe"),
        ("rubric-check-wrong-version", "rubric-minder@1#failed-probe"),
        ("rubric-check-bad-slug", "rubric-minder@1#Failed_Probe"),
    ],
}


def _params(cases: dict[str, list[tuple[str, str]]], ac: str):
    return [pytest.param(n, needle, id=n) for n, needle in cases[ac]]


@pytest.mark.trace("FR-020-AC-1")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-1"))
def test_missing_table_column_or_member_fails_naming_it(name: str, needle: str):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-1", "FR-022-AC-4")
def test_the_worked_minder_spec_validates():
    validates(MINDER, VALID)


@pytest.mark.trace("FR-020-AC-2")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-2"))
def test_a_value_outside_a_closed_enum_fails_naming_the_cell(name: str, needle: str):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-3")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-3"))
def test_query_references_and_rubric_references_are_checked_by_method(
    name: str, needle: str
):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-4")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-4"))
def test_a_judgement_evaluation_never_runs_every_tick(name: str, needle: str):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-11")
def test_a_role_spec_may_carry_a_purpose_section():
    text = MINDER.read_text()
    assert "\n## Purpose\n" in text
    validates(MINDER, VALID)


@pytest.mark.trace("FR-020-AC-12")
def test_the_role_spec_links_are_exactly_three_verbs(manifest):
    assert manifest_type(manifest, "RoleSpec")["allowed_links"] == [
        "satisfies",
        "depends_on",
        "implements",
    ]


@pytest.mark.trace("FR-020-AC-12")
def test_another_relationship_verb_is_reported_on_a_role_spec():
    # The engine reports an unlisted verb as a warning (`disallowed-edge-type`),
    # the same severity it gives every archetype's `allowed_links` miss.
    path = INVALID / "bad-link-verb.md"
    found = [
        line
        for line in validate(path).stderr.splitlines()
        if str(path) in line and "[disallowed-edge-type]" in line
    ]
    assert any("'supersedes'" in line for line in found)


@pytest.mark.trace("FR-020-AC-5")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-5"))
def test_a_row_id_with_the_wrong_prefix_or_shape_fails_naming_the_id(
    name: str, needle: str
):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-6")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-6"))
def test_a_threshold_is_a_known_comparator_a_number_and_a_unit(name: str, needle: str):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-7")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-7"))
def test_the_evaluator_follows_the_method(name: str, needle: str):
    fails_naming(name, needle)


@pytest.mark.trace("FR-020-AC-8")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-020-AC-8"))
def test_version_and_id_have_their_declared_shape(name: str, needle: str):
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
    } | {"bad-link-verb", "rubric-bad-link-verb"}
    assert {p.stem for p in INVALID.glob("*.md")} == declared


@pytest.mark.trace("FR-021-AC-4")
@pytest.mark.parametrize("name,needle", _params(ROLE_SPEC_CASES, "FR-021-AC-4"))
def test_an_objective_with_no_metric_fails_naming_the_objective(name: str, needle: str):
    fails_naming(name, needle)


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


@pytest.mark.trace("FR-021-AC-10", "FR-023-AC-3")
def test_the_rubric_reference_in_the_minder_spec_resolves():
    assert dangling(VALID) == []
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
def test_a_rubric_missing_a_member_table_or_column_fails_naming_it(
    name: str, needle: str
):
    fails_naming(name, needle)


@pytest.mark.trace("FR-023-AC-2")
@pytest.mark.parametrize("name,needle", _params(RUBRIC_CASES, "FR-023-AC-2"))
def test_a_check_id_must_carry_the_rubric_name_version_and_a_slug(
    name: str, needle: str
):
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
def test_another_relationship_verb_is_reported_on_a_rubric():
    path = INVALID / "rubric-bad-link-verb.md"
    found = [
        line
        for line in validate(path).stderr.splitlines()
        if str(path) in line and "[disallowed-edge-type]" in line
    ]
    assert any("'supersedes'" in line for line in found)


@pytest.mark.trace("FR-023-AC-1")
def test_the_rubric_manifest_entry_declares_its_check_target_and_links(manifest):
    entry = manifest_type(manifest, "Rubric")
    assert entry["allowed_links"] == ["satisfies", "depends_on", "implements"]
    targets = {t["name"]: t for t in manifest["traceability"]["trace_targets"]}
    check = targets["rubric-check"]
    assert (check["archetype"], check["section"], check["id_column"]) == (
        "Rubric",
        "Checks",
        "ID",
    )
    assert check["evidence"] == "reference-only"
