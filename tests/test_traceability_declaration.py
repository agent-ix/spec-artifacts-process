"""FR-004: the `traceability:` declaration — what mints trace ids, what
references them, and how a test carries one.

`trace_tags` and `document_references` have no engine fallback: undeclared means
an empty registry, which means no `verifies` relation is ever minted and every
row in the ecosystem reads as unbacked. These tests are what keep the
declaration from silently regressing to that state.
"""

from __future__ import annotations

import json
import pathlib
import re
import shutil
import subprocess

import pytest
import yaml
from support.strict_yaml import load_yaml_strict

import spec_artifacts_process as pack

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
LANGUAGES = ["rust", "python", "typescript"]


@pytest.fixture(scope="module")
def traceability() -> dict:
    return load_yaml_strict(pack.MANIFEST_PATH.read_text())["traceability"]


def test_strict_manifest_loader_rejects_duplicate_trace_target_keys() -> None:
    duplicate = (
        "traceability:\n  trace_targets:\n    - name: suite\n"
        "      required: false\n      required: false\n"
    )
    with pytest.raises(
        yaml.constructor.ConstructorError, match="duplicate key 'required'"
    ):
        load_yaml_strict(duplicate)


def test_targets_mint_test_cases_and_criteria(traceability: dict) -> None:
    """TC-028 (FR-004-AC-1): the two id families the rollup reconciles."""
    targets = {t["name"]: t for t in traceability["trace_targets"]}

    matrices = [t for t in targets.values() if t["section"] == "Test Case Summary"]
    assert matrices, "no target mints test-case ids"
    for target in matrices:
        assert target["id_column"] == "Test ID"

    criteria = {
        t.get("archetype")
        for t in targets.values()
        if t["section"] == "Acceptance Criteria"
    }
    # quire-rs#460: `interface` joins FR/NFR as a third Acceptance Criteria
    # source — an `object_types` archetype declared in a different module
    # (spec-objects-architecture). The real cross-module precedent is
    # `FR`/`NFR`/`StR` above, declared by spec-artifacts-iso, not this
    # module — not `suite`/`inspection`, which this module declares itself,
    # so binding them is same-module and proves nothing about binding across
    # a module boundary.
    assert criteria == {"FR", "NFR", "interface"}, criteria


def test_interface_acceptance_criterion_is_optional(traceability: dict) -> None:
    """TC-147 (FR-004-AC-19): consumers may omit interface docs or their
    Acceptance Criteria sections. `required:` defaults to `true` (quire-rs
    `traceability.rs`), so the optional target must pin `false`.
    """
    targets = {t["name"]: t for t in traceability["trace_targets"]}
    assert targets["interface-acceptance-criterion"]["required"] is False


def test_interface_archetype_string_is_exact(traceability: dict) -> None:
    """quire-rs#460: the archetype match is a raw frontmatter `type:` string
    compare (quire-rs `src/corpus/declared_tables.rs::scan`), not a
    registry lookup — a typo here silently mints nothing rather than
    failing loudly, so pin the exact string.
    """
    targets = {t["name"]: t for t in traceability["trace_targets"]}
    assert targets["interface-acceptance-criterion"]["archetype"] == "interface"

    refs = {r["name"]: r for r in traceability["document_references"]}
    assert refs["interface-verification"]["archetype"] == "interface"


def test_constraint_target_mirrors_acceptance_criterion(traceability: dict) -> None:
    """TC-148 (FR-004-AC-20): a `-CON-` id is minted by the same section +
    `id_column` mechanism `acceptance-criterion` already mints from — `##
    Constraints` is a table with an `ID` column exactly like `## Acceptance
    Criteria` is.

    `required: false`: spec-artifacts-iso's own FR skeleton lists
    `Constraints` among its OPTIONAL level-2 sections ("Omit the section
    rather than inventing filler constraints"), unlike `Acceptance Criteria`,
    which is required on every FR — the same condition that already makes
    `interface-acceptance-criterion` declare `required: false`. In
    this repository, some FR documents carry no `## Constraints` section.
    """
    targets = {t["name"]: t for t in traceability["trace_targets"]}
    acceptance = targets["acceptance-criterion"]
    constraint = targets["constraint"]

    assert constraint["archetype"] == "FR"
    assert constraint["section"] == "Constraints"
    assert constraint["id_column"] == "ID"
    assert constraint["exclude"] == acceptance["exclude"]
    # No `evidence: reference_only` — a constraint enters the same
    # evidence-bearing denominator `acceptance-criterion` does. Omitted is the
    # default `source` posture, so neither declares the key at all.
    assert "evidence" not in constraint
    assert "evidence" not in acceptance
    assert constraint["required"] is False


def test_constraint_is_a_traces_to_and_inspection_target(traceability: dict) -> None:
    """TC-148 (FR-004-AC-20): declaring the target alone mints the id but
    resolves no existing `-CON-` reference in a `Traces To` cell and
    discharges no constraint through an `Inspections` record, so both
    reference declarations widen alongside it."""
    refs = {r["name"]: r for r in traceability["document_references"]}
    assert "constraint" in refs["traces-to"]["targets"]
    assert "constraint" in refs["inspection-obligation"]["targets"]


def test_constraint_target_mints_and_dangling_con_references_resolve() -> None:
    """TC-148 (FR-004-AC-20): the end-to-end measurement. `quire coverage
    --json` mints `FR-NNN-CON-N` rows among `minted_targets`, and `quire
    validate --okf` reports zero `dangling-trace-reference` warnings naming a
    `-CON-` id (PLAT-1079 CR-064)."""
    if shutil.which("quire") is None:
        pytest.skip("the `quire` CLI is required for the rollup")

    coverage = subprocess.run(
        [
            "quire",
            "coverage",
            "--module",
            str(pack.PACK_ROOT),
            "--scope",
            str(REPO_ROOT),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert coverage.returncode == 0, coverage.stderr
    report = json.loads(coverage.stdout)
    minted_constraints = [
        row for row in report["minted_targets"] if row["target"] == "constraint"
    ]
    assert minted_constraints, "no `-CON-` row minted — has the target regressed?"
    assert all(re.match(r"^FR-\d+-CON-\d+$", row["id"]) for row in minted_constraints)

    validation = subprocess.run(
        ["quire", "validate", "--okf", "--scope", str(REPO_ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    output = validation.stdout + validation.stderr
    con_dangling = [
        line
        for line in output.splitlines()
        if "dangling-trace-reference" in line and "CON-" in line
    ]
    assert not con_dangling, con_dangling


def test_every_entry_binds_by_archetype_and_matrices_exclude_test_data(
    traceability: dict,
) -> None:
    """TC-029 (FR-004-AC-2): `archetype:` is the only origin (quire-rs CR-062),
    and the matrix entries carry `exclude:` — which is what makes archetype
    binding safe.

    This reverses the earlier rule. Path binding existed because the corpus walk
    skipped `tests.md` outright; type-driven membership (quire-rs #73) removed
    that skip, and quire-rs #74 deleted the `document:` form. What survives is
    the *second* half of the original finding: archetype binding admits matrices
    that are test data, where a fixture reusing a real test id reports that id as
    backed. `exclude:` answers it, so the exclusion is asserted rather than
    assumed — dropping it silently readmits 67 phantom ids from
    `tests/fixtures/testmatrix/*.md`.
    """
    entries = traceability["trace_targets"] + traceability["document_references"]

    for entry in entries:
        assert "document" not in entry, (
            f"{entry['name']} uses the retired `document:` form; quire-rs "
            "rejects the key outright since CR-062"
        )
        assert entry.get("archetype"), f"{entry['name']} declares no archetype"

        if entry["section"] in ("Test Case Summary", "Functional Requirement Coverage"):
            assert entry["archetype"] == "TestMatrix", entry["name"]
            excluded = entry.get("exclude") or []
            assert any(pattern.startswith("tests/") for pattern in excluded), (
                f"{entry['name']} binds TestMatrix by archetype without excluding "
                "test data — a fixture matrix would mint phantom ids"
            )
        elif entry["section"] == "Acceptance Criteria":
            assert entry["archetype"] in ("FR", "NFR", "interface"), entry["name"]


@pytest.mark.trace("TC-039")
def test_matrix_entries_are_not_enumerated_per_filename(traceability: dict) -> None:
    """TC-039 (FR-004-AC-2, quire-rs CR-062): one entry per *kind* of table, not
    one per filename the ecosystem happens to use.

    The retired form needed three near-identical entries — `spec/tests.md`,
    `spec/matrix.md`, `spec/evals.md` — and still reached nothing nested, so a
    matrix at `spec/<module>/matrix/tests.md` minted zero ids. A matrix is
    reached by what it *is*, not by what it is called.
    """
    entries = traceability["trace_targets"] + traceability["document_references"]
    matrix_entries = [
        e["name"]
        for e in entries
        if e["section"]
        in (
            "Test Case Summary",
            "Functional Requirement Coverage",
            "Nonfunctional and Stakeholder Coverage",
        )
    ]
    expected = [
        "functional-coverage",
        "nonfunctional-stakeholder-coverage",
        "test-case",
        "traces-to",
    ]
    assert (
        sorted(matrix_entries) == expected
    ), f"one entry per table kind, not per filename: {matrix_entries}"


def test_combined_table_extraction_declaration() -> None:
    """Check the optional combined-table declaration pending validator support."""
    manifest = load_yaml_strict(pack.MANIFEST_PATH.read_text())
    matrix = next(
        artifact
        for artifact in manifest["artifact_types"]
        if artifact["name"] == "TestMatrix"
    )
    shape = matrix["body_extraction"]["yield_pattern"]["match"][
        "nonfunctional_stakeholder_coverage"
    ]
    assert shape["under_section"] == "Nonfunctional and Stakeholder Coverage"
    assert shape["required"] is False
    assert shape["assert"]["columns"] == [
        "Requirement",
        "Acceptance Criteria",
        "Test Cases",
        "Status",
    ]


@pytest.mark.integration
@pytest.mark.trace("TC-153")
def test_analyze_matrix_false_complete_is_a_status_lie(tmp_path: pathlib.Path) -> None:
    """Both Analyze coverage tables make Complete claims visible to Quire."""
    if shutil.which("quire") is None:
        pytest.skip("the `quire` CLI is required for the coverage integration")

    spec_dir = tmp_path / "spec"
    tests_dir = tmp_path / "tests"
    spec_dir.mkdir()
    tests_dir.mkdir()
    (spec_dir / "test-matrix.md").write_text(
        "---\nid: TM-001\ntype: TestMatrix\ntitle: Analyze matrix\n---\n\n"
        "## Functional Requirement Coverage\n\n"
        "| Functional Req | Acceptance Criteria | Test Cases | Status |\n"
        "| --- | --- | --- | --- |\n"
        "| FR-001 | FR-001-AC-1 | TC-999 | ✅ Complete |\n\n"
        "## Nonfunctional and Stakeholder Coverage\n\n"
        "| Requirement | Acceptance Criteria | Test Cases | Status |\n"
        "| --- | --- | --- | --- |\n"
        "| StR-001 | StR-001-VC-1 | TC-998 | ✅ Complete |\n"
        "| StR-002 | StR-002-VC-1 | TC-996 | ✅ Complete |\n"
        "| NFR-001 | NFR-001-AC-1 | TC-997 | ✅ Complete |\n"
        "| NFR-002 | NFR-002-AC-1 | TC-995 | 🚧 Planned |\n\n"
        "## Test Case Summary\n\n"
        "| Test ID | Title | Type | Priority | Traces To | Status |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| TC-001 | Existing test | Unit | P0 | FR-001 | 🚧 Planned |\n"
        "| TC-996 | Backed test | Unit | P0 | StR-002 | ✅ Complete |\n"
    )
    (tests_dir / "evidence.rs").write_text(
        '#[trace("TC-996")]\n#[test]\nfn backed_case() {}\n'
    )
    result = subprocess.run(
        [
            "quire",
            "coverage",
            "--scope",
            str(tmp_path),
            "--module",
            str(pack.PACK_ROOT),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    lies = report["status_lies"]
    assert {(lie["reference"], lie["row_id"]) for lie in lies} == {
        ("functional-coverage", "FR-001"),
        ("nonfunctional-stakeholder-coverage", "StR-001"),
        ("nonfunctional-stakeholder-coverage", "NFR-001"),
    }
    assert all(lie["status"] == "✅ Complete" for lie in lies)
    assert any(
        row["reference"] == "nonfunctional-stakeholder-coverage"
        and row["row_id"] == "NFR-002"
        for row in report["unbacked_rows"]
    ), "the Planned control must be scanned even though it is not a lie"
    assert any(
        row["id"] == "TC-996" and row["backed"] for row in report["minted_targets"]
    ), "the Complete control must have real bound evidence"


def test_one_templated_marker_per_language(traceability: dict) -> None:
    """TC-030 (FR-004-AC-3): a marker without a `template` yields no migration
    suggestion — FR-051 emits one only "where the equivalent marker is
    derivable", and the template is what makes it derivable."""
    markers = traceability["trace_tags"]["markers"]
    by_language = {m["language"]: m for m in markers}

    assert sorted(by_language) == sorted(LANGUAGES)
    assert len(markers) == len(by_language), "one canonical marker per language"
    for marker in markers:
        assert marker.get("template"), marker["name"]
        assert "{ids}" in marker["template"], marker["name"]
        re.compile(marker["pattern"])


def test_legacy_forms_rewrite_within_their_own_language(traceability: dict) -> None:
    """TC-031 (FR-004-AC-4): `rewrite_to` names exactly one marker, so a form
    spanning languages can only ever suggest the wrong syntax for the others —
    a Rust attribute offered inside a `.py` file."""
    tags = traceability["trace_tags"]
    marker_language = {m["name"]: m["language"] for m in tags["markers"]}

    for legacy in tags["legacy"]:
        assert legacy.get("language"), f"{legacy['name']} spans languages"
        target = legacy.get("rewrite_to")
        assert target in marker_language, f"{legacy['name']} -> {target}"
        assert marker_language[target] == legacy["language"], (
            f"{legacy['name']} is {legacy['language']} but suggests "
            f"{marker_language[target]} syntax"
        )
        re.compile(legacy["pattern"])


def test_legacy_forms_capture_every_id_the_line_names(traceability: dict) -> None:
    """TC-035 (FR-004-AC-8, CR-024): a form declaring a single id matches once
    and stops at the comma, so the rest of the line is never read. The engine
    splits capture group 1 (quire-rs FR-051-AC-16);
    this asserts the declaration gives it something to split.

    `rust-test-name-id` is deliberately excluded **from list widening**:
    `TC-{1}` renders over a function name, which cannot carry a list, so the
    engine leaves the `id_format` path unsplit and list-widening it here would
    be inert. Its separator is a different axis — see TC-071.
    """
    legacy = {f["name"]: f for f in traceability["trace_tags"]["legacy"]}

    listed = ["FR-001-AC-1", "FR-001-AC-2", "FR-001-AC-4"]
    lines = {
        "rust-trace-line": "// Trace: " + ", ".join(listed),
        "python-trace-line": "# Trace: " + ", ".join(listed),
        "typescript-trace-line": " * Trace: " + ", ".join(listed),
        "rust-comment-id": "// TC-033, TC-034",
        "python-comment-id": "# TC-033, TC-034",
        "typescript-comment-id": "// TC-033, TC-034",
        "python-docstring-id": '    """FR-007-AC-1, FR-005-AC-1',
        "rust-doc-comment-id": "/// TC-058, TC-198",
        "typescript-doc-comment-id": " * TC-058, TC-198",
    }
    assert set(lines) | {"rust-test-name-id"} == set(legacy), set(legacy)

    for name, line in lines.items():
        form = legacy[name]
        assert "id_format" not in form, f"{name} renders a template"
        match = re.search(form["pattern"], line)
        assert match, f"{name} does not match {line!r}"
        ids = [part.strip() for part in match.group(1).split(",") if part.strip()]
        assert len(ids) > 1, f"{name} captured only {ids} from {line!r}"

    # The template path stays single-id, exactly as the engine reads it.
    assert legacy["rust-test-name-id"]["id_format"] == "TC-{1}"
    assert re.search(legacy["rust-test-name-id"]["pattern"], "fn tc753_legacy()")

    # The delimiter that separates a tag from prose is unchanged: quire-rs
    # writes `// TC-480 / FR-025-AC-1: …` and that is one id, not a list, while
    # a sentence flowing through an id still matches nothing.
    comment = legacy["rust-comment-id"]["pattern"]
    slashed = re.search(comment, "// TC-480 / FR-025-AC-1: len == n")
    assert slashed and slashed.group(1) == "TC-480"
    assert not re.search(
        legacy["python-comment-id"]["pattern"],
        "# FR-003-CON-1 sweep found in real matrices",
    )
    for line, expected in (
        ("// TC-033, TC-034: why", ["TC-033", "TC-034"]),
        ("// TC-033 - prose", ["TC-033"]),
        ("// TC-033,  TC-034 ,", ["TC-033", "TC-034"]),
    ):
        match = re.search(comment, line)
        assert match, line
        assert [p.strip() for p in match.group(1).split(",") if p.strip()] == expected

    # quire-rs#460: the underscore-object-id shape (`interface_004`) binds
    # through the same comment forms, same trailing delimiter.
    accepted = re.search(comment, "// interface_004-AC-1: why")
    assert accepted and accepted.group(1) == "interface_004-AC-1"

    # CR-063 finding 3: closed to the literal KIND (`interface`), not a
    # generic `\w+_\d+` — a malformed id, a missing KIND prefix, a leading
    # digit, and the two ordinary identifiers that merely share the
    # `word_number` shape all still bind nothing.
    for rejected in (
        "// interface_004-AC: why",
        "// _004-AC-1: why",
        "// 4_004-AC-1: why",
        "// interface_004_AC_1: why",
        "// sha_256: digest",
        "# retry_3: backoff",
    ):
        opener_pattern = (
            legacy["python-comment-id"]["pattern"]
            if rejected.startswith("#")
            else comment
        )
        assert not re.search(opener_pattern, rejected), rejected


def test_test_name_form_binds_both_spellings_of_its_token(
    traceability: dict,
) -> None:
    """TC-071 (FR-004-AC-11, CR-034): the declared form had no separator between
    `tc` and the digits, so `fn tc_744_…` bound nothing, and most of what
    `agent-ix/filament-ide-rs` coverage reported as missing tests was the tool
    failing to read a tag that was present.

    Both spellings are the same token under this convention — `tc`, the number,
    then the name — and `(?i:tc)` already admits four spellings of `tc`. The
    separator is the same class of variation, so it must not buy recall by
    giving up the anchors.
    """
    form = {f["name"]: f for f in traceability["trace_tags"]["legacy"]}[
        "rust-test-name-id"
    ]
    pattern = form["pattern"]
    assert form["id_format"] == "TC-{1}"

    # Both spellings bind, and to the same id.
    for line in ("fn tc744_legacy()", "fn tc_744_legacy()"):
        match = re.search(pattern, line)
        assert match, f"{line!r} binds nothing"
        assert form["id_format"].replace("{1}", match.group(1)) == "TC-744", line

    # Case variation of the token is unchanged by the separator.
    for line in ("fn TC_744_x()", "fn Tc744_x()", "fn tC_744_x()"):
        match = re.search(pattern, line)
        assert match and match.group(1) == "744", line

    # One capture group, so the engine's template path stays single-id.
    assert re.compile(pattern).groups == 1

    # The anchors still hold on both sides: precision does not move.
    for rejected in (
        "fn tc_legacy()",  # no digits
        "fn tc_744()",  # no trailing separator
        "let tc_744_x = 1;",  # not a fn position
        "// tc_744_x",  # not a fn position
        "fn atc_744_x()",  # \b defeats the prefixed spelling
    ):
        assert not re.search(pattern, rejected), rejected


def test_references_resolve_against_declared_targets(traceability: dict) -> None:
    """TC-032 (FR-004-AC-5): a reference naming an undeclared target resolves
    against nothing, which reads identically to a row nothing backs."""
    declared = {t["name"] for t in traceability["trace_targets"]}

    for reference in traceability["document_references"]:
        assert reference["targets"], reference["name"]
        unknown = set(reference["targets"]) - declared
        assert not unknown, f"{reference['name']} names undeclared {unknown}"
        assert (
            re.compile(reference["pattern"]).groups >= 1
        ), f"{reference['name']}: capture group 1 is the referenced id"


def test_rollup_backs_rows_and_ignores_fixtures() -> None:
    """TC-033 (FR-004-AC-6): the end-to-end gate. A zero backed count is the
    failure this whole declaration exists to fix, and a row minted from
    `tests/fixtures/` is a phantom — those documents are deliberately malformed
    test data that reuse real test ids."""
    if shutil.which("quire") is None:
        pytest.skip("the `quire` CLI is required for the rollup")
    result = subprocess.run(
        [
            "quire",
            "coverage",
            "--module",
            str(pack.PACK_ROOT),
            "--scope",
            str(REPO_ROOT),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)

    assert report["totals"]["total"] > 0, "no rows scanned — nothing to reconcile"
    assert report["totals"]["backed"] > 0, "no row backed by any tagged test"

    from_fixtures = [g for g in report["groups"] if g["document"].startswith("tests/")]
    assert not from_fixtures, from_fixtures


def test_archetype_bound_entries_exclude_the_test_tree(traceability: dict) -> None:
    """TC-036 (FR-004-AC-9, CR-025, widened CR-062): archetype binding admits
    fixtures, because a fixture exercising a contract *is* typed as that contract.
    The phantom lands in consuming repos:
    `quire-cli/tests/fixtures/validate-mod/docs/valid-fr.md` is `type: FR,
    id: FR-001` and put 9 phantom criteria in that repo's denominator. Only a
    declaration-level assertion holds everywhere this module is installed.

    The test tree is not one glob: `cloudmanager-local-sync` and
    `filament-parser-lib` keep typed-`FR` fixtures under `tests_integration/`,
    each colliding with a real `FR-001`, which `tests/**` alone never covers.

    CR-062 makes this cover **every** entry rather than a subset. Matrix entries
    used to be path-bound and so out of reach of the fixture problem; now they are
    archetype-bound like the rest, and `tests/fixtures/testmatrix/*.md` in this
    very repo is the 67-phantom-id population this exclusion keeps out. `exclude:`
    went from a safeguard on some entries to the thing that makes the whole model
    safe."""
    entries = traceability["trace_targets"] + traceability["document_references"]
    archetype_bound = [e for e in entries if e.get("archetype")]
    assert archetype_bound, "no archetype-bound entry — has the model changed?"

    for entry in archetype_bound:
        excludes = entry.get("exclude") or []
        assert excludes, (
            f"{entry['name']} binds by archetype {entry['archetype']!r} with no "
            "exclude — a typed fixture mints ids into the rollup"
        )
        for prefix in ("tests/", "tests_integration/", "fixtures/"):
            assert any(glob.startswith(prefix) for glob in excludes), (
                f"{entry['name']}: exclude {excludes} does not cover "
                f"{prefix}** — a typed fixture there mints ids into the rollup"
            )


def test_no_source_symbol_names_only_methods_that_cannot_be_tagged(
    traceability: dict,
) -> None:
    """TC-034 (FR-004-AC-7, CR-002): the exemption vocabulary is declared, names
    the column it is read from, and lists only values in the test-type
    vocabulary.

    Scope matters more than presence here. `Eval` is an agent driven against a
    live scenario and `Manual` is a person — neither produces a symbol a trace
    tag could attach to. `Static`, `Benchmark` and `Compile` are usually
    asserted by real code (this repo's own static boundary audit is a test), so
    exempting them would hide overclaims instead of explaining them.

    CR-035 adds `Inspection` and `Analysis` on exactly that reasoning — a CI
    lane running a script against a tree, and an argument — and deliberately
    holds `Demonstration` to the `Static`/`Benchmark` line, because a
    demonstration is observed running and can carry a symbol. TC-072 asserts
    that split; this test keeps the list itself pinned so any further change is
    a conscious diff.
    """
    vocab = traceability["vocabularies"]
    assert vocab["test_type_column"] == "Type"

    exempt = vocab["no_source_symbol"]
    assert exempt == ["Eval", "Manual", "Inspection", "Analysis"], exempt
    for value in exempt:
        assert value in vocab["test_type"], f"{value} is not a declared test type"
    for still_bindable in ("Static", "Benchmark", "Compile", "Unit"):
        assert still_bindable not in exempt


@pytest.mark.trace("TC-066")
def test_one_templated_implements_form_per_language(traceability: dict) -> None:
    """TC-066 (FR-004-AC-10): exactly one form per language."""
    forms = traceability["trace_tags"]["implements"]
    by_language = {f["language"]: f for f in forms}

    assert sorted(by_language) == sorted(LANGUAGES)
    assert len(forms) == len(by_language), "one form per language"
    assert all("{ids}" in form.get("template", "") for form in forms)


@pytest.mark.trace("TC-155")
def test_comment_implements_forms_match_language_syntax(traceability: dict) -> None:
    """TC-155 (FR-004-AC-26): comments bind ids only after `Implements:`."""
    forms = traceability["trace_tags"]["implements"]
    by_language = {f["language"]: f for f in forms}

    listed = ["FR-001", "FR-002-AC-3"]
    for language, prefix in (("python", "# "), ("typescript", "// ")):
        form = by_language[language]
        assert form["name"] == f"{language}-implements-line"
        assert form.get("template"), form["name"]
        assert "{ids}" in form["template"], form["name"]
        pattern = re.compile(form["pattern"])

        match = pattern.search(prefix + "Implements: " + ", ".join(listed))
        assert match, f"{form['name']} does not match a keyword line"
        ids = [part.strip() for part in match.group(1).split(",") if part.strip()]
        assert ids == listed, f"{form['name']} captured {ids}"

        # Prose naming a requirement is not a declaration of scope. Without the
        # keyword there is nothing to match, which is the whole reason these
        # forms need no trailing delimiter.
        assert not pattern.search(
            "// FR-001 is the manifest activation requirement."
        ), f"{form['name']} binds prose"

        # quire-rs#460: the underscore-object-id shape scopes the same way.
        scoped = pattern.search(prefix + "Implements: interface_004-AC-1")
        assert scoped, f"{form['name']} does not scope interface_004-AC-1"
        assert (
            scoped.group(1) == "interface_004-AC-1"
        ), f"{form['name']} captured {scoped.group(1)!r}"

        # CR-063 finding 3: closed to the literal KIND. A malformed AC suffix
        # truncates to the requirement id, exactly as an `FR-001-AC` already
        # would — this form has no trailing-delimiter to enforce, so
        # "scoping truncates to the requirement trivially" is documented,
        # intentional behaviour, not a partial bind of the malformed tail.
        for malformed, truncated in (
            ("interface_004-AC", "interface_004"),
            ("interface_004_AC_1", "interface_004"),
        ):
            trunc_match = pattern.search(prefix + f"Implements: {malformed}")
            assert trunc_match, f"{form['name']} lost the base id in {malformed!r}"
            assert (
                trunc_match.group(1) == truncated
            ), f"{form['name']}: {malformed!r} -> {trunc_match.group(1)!r}"

        # No KIND prefix, a leading digit, and an ordinary identifier that
        # merely shares the `word_number` shape still bind nothing.
        for rejected in ("_004-AC-1", "4_004-AC-1", "sha_256", "retry_3"):
            assert not pattern.search(
                prefix + f"Implements: {rejected}"
            ), f"{form['name']} binds {rejected!r}"


@pytest.mark.trace("TC-154")
def test_rust_implements_attribute_matches_ix_trace_syntax(traceability: dict) -> None:
    """TC-154 (FR-004-AC-25): Rust's form captures separate id literals."""
    tags = traceability["trace_tags"]
    forms = [form for form in tags["implements"] if form["language"] == "rust"]
    assert len(forms) == 1, forms
    attribute = forms[0]
    assert attribute["name"] == "rust-implements-attribute"
    assert attribute["template"] == "#[implements({ids})]"
    pattern = re.compile(attribute["pattern"])
    for syntax, expected in (
        ('#[implements("FR-001")]', ["FR-001"]),
        ('#[implements("FR-001", "FR-002-AC-3")]', ["FR-001", "FR-002-AC-3"]),
        (
            '    #[implements("interface_004-AC-1", "TC-CB-01",)]',
            ["interface_004-AC-1", "TC-CB-01"],
        ),
    ):
        match = pattern.search(syntax)
        assert match, syntax
        assert re.findall(r'"([^"]+)"', match.group(1)) == expected
    assert "rust-implements-attribute" not in {form["name"] for form in tags["markers"]}


@pytest.mark.trace("TC-159")
def test_rust_implements_attribute_rejects_malformed_forms(
    traceability: dict,
) -> None:
    """TC-159 (FR-004-AC-30): malformed attributes and prose bind nothing."""
    form = next(
        form
        for form in traceability["trace_tags"]["implements"]
        if form["language"] == "rust"
    )
    pattern = re.compile(form["pattern"])
    for malformed in (
        "/// FR-001 implements this behavior.",
        "/// Implements: FR-001",
        '/// #[implements("FR-001")]',
        'let example = "#[implements(\\"FR-001\\")]";',
        "#[implements(FR-001)]",
        '#[implements("FR-001, FR-002-AC-3")]',
        '#[implements("FR-001" extra)]',
        '#[implements("not an id")]',
        '#[implements("sha_256")]',
        '#[implements("")]',
        "#[implements()]",
    ):
        assert not pattern.search(malformed), malformed


@pytest.mark.integration
@pytest.mark.trace("TC-154")
@pytest.mark.trace("TC-157")
def test_quire_credits_ix_trace_implements_attribute_on_production(
    tmp_path: pathlib.Path,
) -> None:
    """The installed engine loads this module and credits Rust production scope."""
    if shutil.which("quire") is None:
        pytest.skip("the `quire` CLI is required for the coverage integration")

    spec_dir = tmp_path / "spec"
    src_dir = tmp_path / "src"
    spec_dir.mkdir()
    src_dir.mkdir()
    (spec_dir / "FR-001.md").write_text(
        "---\nid: FR-001\ntype: FR\ntitle: Test requirement\n---\n\n"
        "## Acceptance Criteria\n\n"
        "| ID | Criteria | Verification |\n| --- | --- | --- |\n"
        "| FR-001-AC-1 | The function handles an input. | Unit |\n"
        "| FR-001-AC-2 | The function handles another input. | Unit |\n"
    )
    (src_dir / "lib.rs").write_text(
        "use ix_trace_rs::implements;\n\n"
        '#[implements("FR-001-AC-1", "FR-001-AC-2")]\n'
        "pub fn handle_input(value: &str) -> usize { value.len() }\n\n"
        "/// Implements: FR-001-AC-1\n"
        "pub fn comment_only(value: &str) -> usize { value.len() }\n"
    )

    result = subprocess.run(
        [
            "quire",
            "coverage",
            "--scope",
            str(tmp_path),
            "--module",
            str(pack.PACK_ROOT),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["implements"] == [
        {
            "path": "src/lib.rs",
            "symbol": "handle_input",
            "trace_id": trace_id,
            "form": "rust-implements-attribute",
        }
        for trace_id in ("FR-001-AC-1", "FR-001-AC-2")
    ]
    assert report["totals"]["backed"] == 0


def _quire_rust_implements_ids(tmp_path: pathlib.Path, source: str) -> set[str]:
    spec_dir = tmp_path / "spec"
    src_dir = tmp_path / "src"
    spec_dir.mkdir()
    src_dir.mkdir()
    (spec_dir / "FR-001.md").write_text(
        "---\nid: FR-001\ntype: FR\ntitle: Attribute cases\n---\n\n"
        "## Acceptance Criteria\n\n"
        "| ID | Criteria | Verification |\n| --- | --- | --- |\n"
        "| FR-001-AC-1 | First case. | Unit |\n"
        "| FR-001-AC-2 | Second case. | Unit |\n"
        "| FR-001-AC-3 | Third case. | Unit |\n"
    )
    (src_dir / "lib.rs").write_text(source)
    result = subprocess.run(
        [
            "quire",
            "coverage",
            "--scope",
            str(tmp_path),
            "--module",
            str(pack.PACK_ROOT),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return {
        edge["trace_id"] for edge in json.loads(result.stdout).get("implements", [])
    }


@pytest.mark.integration
def test_quire_does_not_credit_attributes_in_rust_text(tmp_path: pathlib.Path) -> None:
    """A comment and a raw-string example must not mint implementation scope."""
    if shutil.which("quire") is None:
        pytest.skip("the `quire` CLI is required for the coverage integration")
    ids = _quire_rust_implements_ids(
        tmp_path,
        "pub fn block_comment_example() {\n"
        '/*\n#[implements("FR-001-AC-1")]\n*/\n}\n'
        "pub fn raw_string_example() {\n"
        'let _example = r#"\n#[implements("FR-001-AC-2")]\n"#;\n}\n'
        '#[implements("FR-001-AC-3")]\n'
        "pub fn real_attribute() {}\n",
    )
    assert "FR-001-AC-3" in ids, "the real-attribute control must bind"
    if ids == {"FR-001-AC-1", "FR-001-AC-2", "FR-001-AC-3"}:
        pytest.xfail(
            "Quire 0.36.2 reads Rust comment and raw-string text as attributes"
        )
    assert ids == {"FR-001-AC-3"}, ids


@pytest.mark.integration
@pytest.mark.trace("TC-158")
def test_quire_credits_valid_trailing_attribute_forms(tmp_path: pathlib.Path) -> None:
    """TC-158 (FR-004-AC-29): valid trailing forms still bind scope."""
    if shutil.which("quire") is None:
        pytest.skip("the `quire` CLI is required for the coverage integration")
    ids = _quire_rust_implements_ids(
        tmp_path,
        '#[implements("FR-001-AC-1")] // why\n'
        "pub fn trailing_comment() {}\n"
        '#[implements("FR-001-AC-2")] pub fn same_line() {}\n',
    )
    assert ids == {"FR-001-AC-1", "FR-001-AC-2"}, ids


@pytest.mark.trace("TC-157")
def test_implements_is_a_separate_list_from_markers(traceability: dict) -> None:
    """TC-157 (FR-004-AC-28, CR-028): the form sets stay separate.

    quire-rs CR-061 stopped `verifies` binding production symbols because a doc
    comment citing `FR-053-AC-1` would otherwise count as evidence backing it.
    Two lists is what keeps one typo from moving a form across that line.
    """
    tags = traceability["trace_tags"]
    marker_names = {m["name"] for m in tags["markers"]} | {
        legacy["name"] for legacy in tags["legacy"]
    }
    implements_names = {f["name"] for f in tags["implements"]}

    assert not marker_names & implements_names, marker_names & implements_names


def test_verification_methods_are_declared_test_types(traceability: dict) -> None:
    """TC-072 (FR-004-AC-12, CR-035): every other `test_type` value names a
    harness kind; a 29148-aligned corpus also authors verification by
    inspection, analysis and demonstration, and had no declared value for any.

    Rows naming a means the vocabulary had no word for (`Inspection`,
    `Analysis`, `Demonstration`) were rejected. Because they were
    undeclared, those rows were typed as something that demands a source symbol
    and coverage reported them as status lies.
    """
    vocab = traceability["vocabularies"]
    types = vocab["test_type"]
    for method in ("Inspection", "Analysis", "Demonstration"):
        assert method in types, f"{method} is a 29148 verification method"

    exempt = vocab["no_source_symbol"]
    # An inspection is a CI lane running a script; an analysis is an argument.
    assert "Inspection" in exempt
    assert "Analysis" in exempt
    # A demonstration is *observed running*, so it can carry a symbol —
    # exempting it would hide an overclaim rather than explain one.
    assert "Demonstration" not in exempt, exempt
    # The pre-existing exemptions are untouched.
    assert {"Eval", "Manual"} <= set(exempt)
    # And the guard the module already holds: nothing that executes is exempt.
    assert not ({"Static", "Benchmark", "Compile", "Unit"} & set(exempt))


def test_traces_to_admits_an_explicit_no_trace_form(traceability: dict) -> None:
    """TC-073 (FR-004-AC-13, CR-036): a retired row has no live requirement to
    trace to — withdrawing it is the act of severing that edge — and the
    pattern admitted nothing valid to write. Every row carrying `-` was
    retired; none was a live row with a missing trace.
    """
    matrix = _testmatrix_extraction()
    pattern = matrix["column_patterns"]["Traces To"]

    assert re.match(pattern, "-"), "the lone hyphen is the no-trace form"

    # Live forms are unchanged.
    for form in (
        "FR-001-AC-1",
        "TC-001, TC-002",
        "FR-001-AC-1 (superseded)",
        "FR-001..FR-003",
    ):
        assert re.match(pattern, form), form

    # …and the loosening buys nothing else: prose, a bare word and a malformed
    # id still fail, so a live row cannot smuggle a non-reference through.
    # Deliberately NOT widened past the form the corpus writes: `—` has been
    # pinned as rejected since CR-017 and no row uses it.
    for form in ("see the other matrix", "none", "n/a", "—", "FR-", "-FR-001"):
        assert not re.match(pattern, form), form

    # quire-rs#460: the underscore-object-id shape (`interface_004`) traces
    # the same way an `FR`/`NFR` acceptance criterion does.
    assert re.match(pattern, "interface_004-AC-1"), "interface_004-AC-1"

    # CR-063 finding 3: the BASE alternative names the literal KIND
    # (`interface`), not a generic `\w+_\d+` — a malformed id, a missing
    # KIND prefix, and a leading digit all still fail, and so do the two
    # false positives an unclosed class would have read as trace tags.
    for form in (
        "interface_004-AC",  # AC suffix has no trailing number
        "_004-AC-1",  # no KIND prefix
        "4_004-AC-1",  # leading digit, not a word
        "interface_004_AC_1",  # AC suffix uses underscores, not hyphens
        "sha_256",  # ordinary code identifier, not a KIND
        "retry_3",  # ordinary code identifier, not a KIND
    ):
        assert not re.match(pattern, form), form


def test_stakeholder_validation_criteria_are_a_trace_target(traceability: dict) -> None:
    """TC-074 (FR-004-AC-14, CR-037): `StR-NNN-VC-N` ids are minted and a tag
    naming one reconciled against nothing.

    IT and US are deliberately absent and the reason is an engine limit: a
    `TraceTarget` mints from `section` + `id_column`, i.e. a table column.
    `IT-NNN-SC-NN` are bullet items under `## Test Procedure` and
    `US-NNN-EX-N` are H3 headings, so declaring either would be a declaration
    the engine cannot honour (agent-ix/quire-rs#244).
    """
    targets = {t["name"]: t for t in traceability["trace_targets"]}
    stakeholder = targets["stakeholder-validation-criterion"]
    assert stakeholder["archetype"] == "StR"
    assert stakeholder["section"] == "Validation Criteria"
    assert stakeholder["id_column"] == "ID"
    # Archetype-bound targets need scope exclusion, like every other one.
    assert stakeholder["exclude"], stakeholder

    declared = {t["archetype"] for t in traceability["trace_targets"]}
    assert not ({"IT", "US"} & declared), (
        "a section+id_column target cannot mint list items or headings; "
        f"declared: {sorted(declared)}"
    )


def test_doc_comment_forms_require_a_trailing_delimiter(traceability: dict) -> None:
    """TC-075 (FR-004-AC-15, CR-038): the anchor stops an id binding from the
    middle of a sentence and never stopped a sentence that *begins* with one.

    `/// TC-1059 used to assert that …` — a note recording that TC-1059 was
    retired — was read as a tag. The dangerous mirror image is
    `/// FR-069-AC-8 is not covered here`, which marks a criterion backed by a
    test that says it does not verify it.
    """
    legacy = {f["name"]: f for f in traceability["trace_tags"]["legacy"]}
    forms = {
        "rust-doc-comment-id": "/// ",
        "typescript-doc-comment-id": " * ",
        "python-docstring-id": '    """',
    }
    for name, opener in forms.items():
        pattern = legacy[name]["pattern"]

        # Prose beginning with an id is not a tag.
        for prose in (
            "TC-1059 used to assert that the CLI and MCP each reached the rule",
            "FR-069-AC-8 is not covered here; see the sibling suite",
            "NFR-026 guarantee is directly observable",
        ):
            assert not re.search(pattern, opener + prose), f"{name}: {prose!r}"

        # Every authored delimiter still binds — including the trailing period,
        # which #64's proposal omitted and four real tags in the corpus use.
        for tag, expected in (
            ("TC-541 (FR-048-AC-1) — why", "TC-541"),
            ("TC-480 / FR-025-AC-1: len == n", "TC-480"),
            ("NFR-035.", "NFR-035"),
            ("FR-087-AC-5", "FR-087-AC-5"),
            ("TC-033, TC-034: why", "TC-033, TC-034"),
        ):
            match = re.search(pattern, opener + tag)
            assert match, f"{name} lost an authored form: {tag!r}"
            assert match.group(1) == expected, f"{name}: {tag!r} -> {match.group(1)!r}"

        # quire-rs#460: the underscore-object-id shape binds through the same
        # trailing-delimiter rule as the hyphenated shape.
        match = re.search(pattern, opener + "interface_004-AC-1: why")
        assert match, f"{name} does not bind interface_004-AC-1"
        assert match.group(1) == "interface_004-AC-1", f"{name}: {match.group(1)!r}"

        # CR-063 finding 3: closed to the literal KIND, so a malformed id, a
        # missing KIND prefix, a leading digit, and an ordinary identifier
        # that merely shares the `word_number` shape all still bind nothing.
        for rejected in (
            "interface_004-AC: why",
            "_004-AC-1: why",
            "4_004-AC-1: why",
            "interface_004_AC_1: why",
            "sha_256: digest",
            "retry_3: backoff",
        ):
            assert not re.search(pattern, opener + rejected), f"{name}: {rejected!r}"


def _verification_lint_rule() -> dict:
    manifest = load_yaml_strict(pack.MANIFEST_PATH.read_text())
    rules = [r for r in manifest["lint_rules"] if r.get("column") == "Verification"]
    assert len(rules) == 1, rules
    return rules[0]


def test_verification_lint_rule_is_scoped_and_advisory() -> None:
    """TC-149 (FR-004-AC-21): a `table_column_values` rule scoped to
    `FR`/`NFR`/`interface` requires the Acceptance Criteria `Verification`
    column to hold a class or catalog method id, with no trailing `TC-…`/
    `IT-…` id, at `severity: warning`."""
    rule = _verification_lint_rule()
    assert rule["type"] == "table_column_values"
    assert set(rule["archetypes"]) == {"FR", "NFR", "interface"}
    assert rule["section"] == "Acceptance Criteria"
    assert rule["severity"] == "warning"
    # No `annotation_pattern`: admitting one would re-admit the very
    # `TC-…`/`IT-…` suffix this rule exists to reject.
    assert not rule.get("annotation_pattern")


def test_verification_lint_rule_flags_stale_test_ids_only(tmp_path) -> None:
    """TC-149 (FR-004-AC-21): the behavioural half — `quire lint` against a
    fixture document. A `Verification` cell reading `Test (TC-999)` reports a
    `acceptance-criterion-verification-method` finding at `warning` severity
    naming the id; a cell naming a bare class or a bare catalog method id
    raises nothing.

    The fixture is written under `tmp_path`, never the repo's own
    `tests/fixtures/` (SR-020 FND-003) — the exclude globs on every trace
    target and document reference cover `fixtures/**` precisely so a
    throwaway document never mints or resolves a real id, and a fixture
    that outlives the test would do exactly that. There is no `quire
    validate --okf` assertion here: `validate` never evaluates `lint_rules`
    (0 rule diagnostics appear in its output), so an exit-code check on it
    would still pass at any severity and asserts nothing about this rule.
    """
    if shutil.which("quire") is None:
        pytest.skip("the `quire` CLI is required for lint")

    fixture = tmp_path / "lint-verification-column.md"
    fixture.write_text(
        "---\nid: FR-999\ntype: FR\ntitle: Fixture\n---\n\n"
        "## Acceptance Criteria\n\n"
        "| ID | Criteria | Verification |\n|----|----------|--------------|\n"
        "| FR-999-AC-1 | bare class | Test |\n"
        "| FR-999-AC-2 | catalog method | property-based-testing |\n"
        "| FR-999-AC-3 | stale TC id | Test (TC-999) |\n"
        "| FR-999-AC-4 | stale IT id | Inspection (IT-3) |\n"
    )
    result = subprocess.run(
        ["quire", "lint", "--module", str(pack.PACK_ROOT), str(fixture)],
        capture_output=True,
        text=True,
        check=False,
    )
    findings = result.stdout + result.stderr
    assert "row 1" not in findings and "row 2" not in findings, findings
    for row, needle in ((3, "TC-999"), (4, "IT-3")):
        line = (
            "warning: acceptance-criterion-verification-method: section "
            f"'Acceptance Criteria' column 'Verification' row {row}:"
        )
        assert line in findings, findings
        assert needle in findings, findings


def test_verification_lint_rule_allowed_set_is_classes_union_catalog(
    manifest: dict,
) -> None:
    """TC-151 (FR-004-AC-22): the `allowed` set equals the four IADT classes
    union every `verification_catalog` key, exactly — derived-by-assertion
    rather than hand-maintained, so an entry added to the catalog and this
    rule's `allowed` list cannot silently drift apart. `Eval`/`Manual` are
    `traceability.vocabularies.test_type` values, not catalog keys, and stay
    absent."""
    rule = _verification_lint_rule()
    classes = {"Test", "Inspection", "Analysis", "Demonstration"}
    catalog_keys = set(manifest["verification_catalog"])

    assert set(rule["allowed"]) == classes | catalog_keys
    assert len(rule["allowed"]) == len(set(rule["allowed"])), "no duplicate entry"
    assert "Eval" not in rule["allowed"]
    assert "Manual" not in rule["allowed"]


def _testmatrix_extraction() -> dict:
    """The TestMatrix `test_cases` assert block, from the shipped manifest."""
    manifest = load_yaml_strict(pack.MANIFEST_PATH.read_text())
    for entry in manifest["artifact_types"]:
        if entry["name"] == "TestMatrix":
            return entry["body_extraction"]["yield_pattern"]["match"]["test_cases"][
                "assert"
            ]
    raise AssertionError("TestMatrix archetype not declared")
