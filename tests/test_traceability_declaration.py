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

import spec_artifacts_process as pack

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
LANGUAGES = ["rust", "python", "typescript"]


@pytest.fixture(scope="module")
def traceability() -> dict:
    return yaml.safe_load(pack.MANIFEST_PATH.read_text())["traceability"]


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
    assert criteria == {"FR", "NFR"}, criteria


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
            assert entry["archetype"] in ("FR", "NFR"), entry["name"]


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
        if e["section"] in ("Test Case Summary", "Functional Requirement Coverage")
    ]
    expected = ["functional-coverage", "test-case", "traces-to"]
    assert (
        sorted(matrix_entries) == expected
    ), f"one entry per table kind, not per filename: {matrix_entries}"


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
    and stops at the comma, so the rest of the line is never read — 205 ids
    across 17 repos. The engine splits capture group 1 (quire-rs FR-051-AC-16);
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


def test_test_name_form_binds_both_spellings_of_its_token(
    traceability: dict,
) -> None:
    """TC-071 (FR-004-AC-11, CR-034): the declared form had no separator between
    `tc` and the digits, so `fn tc_744_…` bound nothing — 1,292 sites in
    `agent-ix/filament-ide-rs` against 0 of the `fn tc744_…` spelling, and two
    thirds of what that repository's coverage reported as missing tests was the
    tool failing to read a tag that was present.

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


def test_implements_forms_require_the_keyword(traceability: dict) -> None:
    """TC-066 (FR-004-AC-10, CR-028): the `implements` forms bind PRODUCTION
    code to the requirement it is about (quire-rs FR-062) — a separate list from
    `markers`, because `markers` mint evidence and these mint scope.

    The literal `Implements:` keyword is the prose guard. The legacy
    `*-comment-id` forms bind a bare id after `//` and need a trailing-delimiter
    rule to stop a sentence flowing through the id; here the keyword carries
    that weight, so a line that merely names a requirement matches nothing.
    """
    forms = traceability["trace_tags"]["implements"]
    by_language = {f["language"]: f for f in forms}

    assert sorted(by_language) == sorted(LANGUAGES)
    assert len(forms) == len(by_language), "one form per language"

    listed = ["FR-001", "FR-002-AC-3"]
    for form in forms:
        assert form.get("template"), form["name"]
        assert "{ids}" in form["template"], form["name"]
        pattern = re.compile(form["pattern"])

        match = pattern.search("/// Implements: " + ", ".join(listed))
        assert match, f"{form['name']} does not match a keyword line"
        ids = [part.strip() for part in match.group(1).split(",") if part.strip()]
        assert ids == listed, f"{form['name']} captured {ids}"

        # Prose naming a requirement is not a declaration of scope. Without the
        # keyword there is nothing to match, which is the whole reason these
        # forms need no trailing delimiter.
        assert not pattern.search(
            "// FR-001 is the manifest activation requirement."
        ), f"{form['name']} binds prose"


def test_implements_is_a_separate_list_from_markers(traceability: dict) -> None:
    """TC-066 (FR-004-AC-10, CR-028): no name is shared between the two lists.

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

    128 rows in one repository named a means the vocabulary had no word for
    (`Inspection` 112, `Analysis` 11, `Demonstration` 5). Because they were
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
    pattern admitted nothing valid to write. 16 of 16 rows carrying `-` in one
    repository were retired; none was a live row with a missing trace.
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
    # pinned as rejected since CR-017 and no measured row uses it.
    for form in ("see the other matrix", "none", "n/a", "—", "FR-", "-FR-001"):
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


def _testmatrix_extraction() -> dict:
    """The TestMatrix `test_cases` assert block, from the shipped manifest."""
    manifest = yaml.safe_load(pack.MANIFEST_PATH.read_text())
    for entry in manifest["artifact_types"]:
        if entry["name"] == "TestMatrix":
            return entry["body_extraction"]["yield_pattern"]["match"]["test_cases"][
                "assert"
            ]
    raise AssertionError("TestMatrix archetype not declared")
