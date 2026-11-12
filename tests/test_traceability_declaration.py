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


@pytest.mark.trace("TC-028", "FR-004-AC-1")
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


@pytest.mark.trace("TC-147", "FR-004-AC-19")
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


@pytest.mark.trace("TC-148", "FR-004-AC-20")
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


@pytest.mark.trace("TC-148", "FR-004-AC-20")
def test_constraint_is_a_traces_to_and_inspection_target(traceability: dict) -> None:
    """TC-148 (FR-004-AC-20): declaring the target alone mints the id but
    resolves no existing `-CON-` reference in a `Traces To` cell and
    discharges no constraint through an `Inspections` record, so both
    reference declarations widen alongside it."""
    refs = {r["name"]: r for r in traceability["document_references"]}
    assert "constraint" in refs["traces-to"]["targets"]
    assert "constraint" in refs["inspection-obligation"]["targets"]


@pytest.mark.trace("TC-148", "FR-004-AC-20")
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


@pytest.mark.trace("TC-029", "FR-004-AC-2")
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


@pytest.mark.trace("TC-039", "FR-004-AC-2")
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


@pytest.mark.trace("TC-030", "FR-004-AC-3")
def test_one_templated_marker_per_language(traceability: dict) -> None:
    """TC-030 (FR-004-AC-3): a marker without a `template` yields no migration
    suggestion — FR-051 emits one only "where the equivalent marker is
    derivable", and the template is what makes it derivable."""
    markers = traceability["trace_tags"]["markers"]
    by_language = {m["language"]: m for m in markers}

    assert sorted(by_language) == sorted([*LANGUAGES, "shell"])
    assert len(markers) == len(by_language), "one canonical marker per language"
    for marker in markers:
        assert marker.get("template"), marker["name"]
        assert "{ids}" in marker["template"], marker["name"]
        re.compile(marker["pattern"])


@pytest.mark.trace("FR-004-AC-3")
def test_shell_marker_is_a_comment_form_gated_by_entry_paths(
    traceability: dict,
) -> None:
    """FR-004-AC-3 (quire-rs FR-051-AC-38, AC-42, AC-43): shell has no attribute
    syntax, so its canonical marker is a `#` comment, and only a script under an
    `entry_paths` glob may bind."""
    (form,) = [
        m for m in traceability["trace_tags"]["markers"] if m["language"] == "shell"
    ]
    assert form["syntax"] == "comment"
    assert form["entry_paths"] == ["scripts/audits/**/*.sh"]
    match = re.search(form["pattern"], "# trace: FR-024-AC-9, TC-502")
    assert match and match.group(1) == "FR-024-AC-9, TC-502"
    assert not re.search(form["pattern"], "# trace is not a tag")


@pytest.mark.trace("TC-032", "FR-004-AC-5")
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


@pytest.mark.trace("TC-033", "FR-004-AC-6")
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


@pytest.mark.trace("TC-036", "FR-004-AC-9")
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


@pytest.mark.trace("TC-034", "FR-004-AC-7")
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


@pytest.mark.trace("FR-004-AC-23")
def test_withdrawn_is_declared_retirement_not_a_verification_method(
    manifest: dict,
) -> None:
    """Keep withdrawal separate from live verification and status markers."""
    traceability = manifest["traceability"]
    vocabularies = traceability["vocabularies"]
    assert vocabularies["retired"] == ["Withdrawn"]
    assert traceability["status"]["retired"] == ["⛔"]
    assert set(vocabularies["retired"]).isdisjoint(manifest["verification_catalog"])
    for live_vocabulary in ("test_type", "no_source_symbol"):
        assert set(vocabularies["retired"]).isdisjoint(vocabularies[live_vocabulary])
    for live_method in ("Test", "Planned", "Inspection", "Analysis"):
        assert live_method not in vocabularies["retired"]


def _implements_forms(traceability: dict) -> dict[str, dict]:
    return {f["name"]: f for f in traceability["trace_tags"]["implements"]}


@pytest.mark.trace("TC-066", "FR-004-AC-10")
def test_rust_implements_forms_are_line_and_attribute(traceability: dict) -> None:
    """TC-066 (FR-004-AC-10): Rust keeps the comment form and adds the attribute."""
    rust = [
        f for f in traceability["trace_tags"]["implements"] if f["language"] == "rust"
    ]
    assert [f["name"] for f in rust] == [
        "rust-implements-line",
        "rust-implements-attribute",
    ]
    assert all("{ids}" in f["template"] for f in rust)


@pytest.mark.trace("TC-166", "FR-004-AC-37")
def test_implements_forms_are_rust_plus_structural_python_typescript(
    traceability: dict,
) -> None:
    """TC-166 (FR-004-AC-37): Python and TypeScript declare only structural
    forms, in the pinned order, with the pinned templates."""
    forms = traceability["trace_tags"]["implements"]
    by_language = {
        language: [form for form in forms if form["language"] == language]
        for language in LANGUAGES
    }

    assert len(forms) == 5
    assert [f["name"] for f in by_language["rust"]] == [
        "rust-implements-line",
        "rust-implements-attribute",
    ]
    assert [(f["name"], f["syntax"], f["template"]) for f in by_language["python"]] == [
        ("python-implements-decorator", "python_decorator", "@implements({ids})")
    ]
    assert [
        (f["name"], f["syntax"], f["template"]) for f in by_language["typescript"]
    ] == [
        (
            "typescript-implements-decorator",
            "typescript_decorator",
            "@implementing({ids})",
        ),
        (
            "typescript-implements-wrapper",
            "typescript_wrapper",
            "implementing({ids})",
        ),
    ]
    assert not [
        f for f in forms if f["name"].endswith("-line") and f["language"] != "rust"
    ]
    for form in by_language["python"] + by_language["typescript"]:
        assert form["pattern"].startswith("\\A"), form["name"]


@pytest.mark.trace("TC-165", "FR-004-AC-36")
def test_rust_line_form_requires_keyword_and_rejects_prose(traceability: dict) -> None:
    """TC-165 (FR-004-AC-36): the Rust line form binds ids only after `Implements:`."""
    form = _implements_forms(traceability)["rust-implements-line"]
    pattern = re.compile(form["pattern"])
    match = pattern.search("/// Implements: FR-001, FR-002-AC-3")
    assert match
    assert match.group(1) == "FR-001, FR-002-AC-3"
    assert not pattern.search("/// FR-001 is the manifest activation requirement.")
    assert not pattern.search("/// FR-001-AC-1 is implemented here")


_REJECTED_ARGS = [
    "FR-001",
    "'FR-001'",
    '"""FR-001"""',
    '"FR-001" + "-AC-1"',
    "",
    '"not an id"',
    '"sha_256"',
    '""',
]


def _structural_cases(
    fn: str, qualifier: str, prefix: str
) -> tuple[list[str], list[str]]:
    ok = [
        f'{prefix}{fn}("FR-001")',
        f'{prefix}{fn}("FR-001-AC-1", "FR-001-AC-2",)',
        f'{prefix}{fn}(\n    "FR-001-AC-1",\n    "interface_004-AC-1",\n)',
        f'{prefix}{qualifier}.{fn}("FR-001")',
        f'{prefix}{qualifier}.{fn}(\n    "FR-001",\n    "FR-002",\n)',
    ]
    bad = [f"{prefix}{fn}({arg})" for arg in _REJECTED_ARGS]
    bad += [
        f'{prefix}{fn}_all("FR-001")',
        f'{prefix}t.{fn}("FR-001")',
        f'{prefix}other.{fn}("FR-001")',
        f"{prefix}{fn}",
        f'{prefix}{fn}("FR-001") extra',
        f'x {prefix}{fn}("FR-001")',
    ]
    return ok, bad


def _check_structural(form: dict, fn: str, qualifier: str, prefix: str) -> None:
    pattern = re.compile(form["pattern"])
    assert form["pattern"].startswith("\\A")
    ok, bad = _structural_cases(fn, qualifier, prefix)
    for text in ok:
        match = pattern.fullmatch(text)
        assert match, f"{form['name']} rejects {text!r}"
        ids = re.findall(r'"([^"]+)"', match.group(1))
        assert ids == re.findall(r'"([^"]+)"', text), (text, ids)
    for text in bad:
        assert not pattern.fullmatch(text), f"{form['name']} fully matches {text!r}"
    # A renamed import contains nothing a search can match.
    assert not pattern.search(f'{prefix}t.{fn}("X-1")')
    assert not pattern.search(f'{prefix}t.{fn}("FR-001")')


@pytest.mark.trace("TC-160", "FR-004-AC-31")
def test_python_decorator_form_matches_whole_node(traceability: dict) -> None:
    """TC-160 (FR-004-AC-31): `python_decorator` pattern is anchored and full-match."""
    form = _implements_forms(traceability)["python-implements-decorator"]
    _check_structural(form, "implements", "ix_trace_py", "@")


@pytest.mark.trace("TC-161", "FR-004-AC-32")
def test_typescript_decorator_and_wrapper_forms(traceability: dict) -> None:
    """TC-161 (FR-004-AC-32): decorator and wrapper, qualified and not."""
    forms = _implements_forms(traceability)
    _check_structural(
        forms["typescript-implements-decorator"], "implementing", "ixTrace", "@"
    )
    _check_structural(
        forms["typescript-implements-wrapper"], "implementing", "ixTrace", ""
    )
    # The wrapper is the inner call: it must not claim the decorator `@`.
    wrapper = re.compile(forms["typescript-implements-wrapper"]["pattern"])
    assert not wrapper.fullmatch('@implementing("FR-001")')


@pytest.mark.trace("TC-154", "FR-004-AC-25")
def test_rust_implements_attribute_matches_ix_trace_syntax(traceability: dict) -> None:
    """TC-154 (FR-004-AC-25): Rust's form captures separate id literals."""
    tags = traceability["trace_tags"]
    forms = [
        form
        for form in tags["implements"]
        if form["name"] == "rust-implements-attribute"
    ]
    assert len(forms) == 1, forms
    attribute = forms[0]
    assert attribute["name"] == "rust-implements-attribute"
    assert attribute["syntax"] == "rust_attribute"
    assert attribute["template"] == "#[implements({ids})]"
    pattern = re.compile(attribute["pattern"])
    for syntax, expected in (
        ('#[implements("FR-001")]', ["FR-001"]),
        ('#[implements("FR-001" ,)]', ["FR-001"]),
        ('#[implements("FR-001"\n,)]', ["FR-001"]),
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


@pytest.mark.trace("TC-159", "FR-004-AC-30")
def test_rust_implements_attribute_rejects_malformed_forms(
    traceability: dict,
) -> None:
    """TC-159 (FR-004-AC-30): malformed attributes and prose bind nothing."""
    form = next(
        form
        for form in traceability["trace_tags"]["implements"]
        if form["name"] == "rust-implements-attribute"
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
@pytest.mark.trace("TC-157", "FR-004-AC-28")
def test_quire_credits_ix_trace_implements_attribute_on_production(
    tmp_path: pathlib.Path,
) -> None:
    """The installed engine loads this module and credits Rust production scope."""
    assert shutil.which("quire") is not None, "a guard-capable quire CLI is required"

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
    assert {
        (edge["path"], edge["symbol"], edge["trace_id"], edge["form"])
        for edge in report["implements"]
    } == {
        ("src/lib.rs", "handle_input", "FR-001-AC-1", "rust-implements-attribute"),
        ("src/lib.rs", "handle_input", "FR-001-AC-2", "rust-implements-attribute"),
        ("src/lib.rs", "comment_only", "FR-001-AC-1", "rust-implements-line"),
    }
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
@pytest.mark.trace("TC-156", "FR-004-AC-27")
def test_quire_does_not_credit_attributes_in_rust_text(tmp_path: pathlib.Path) -> None:
    """A comment and a raw-string example must not mint implementation scope."""
    assert shutil.which("quire") is not None, "a guard-capable quire CLI is required"
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
    assert ids == {"FR-001-AC-3"}, ids


@pytest.mark.integration
@pytest.mark.trace("TC-158", "FR-004-AC-29")
def test_quire_credits_valid_trailing_attribute_forms(tmp_path: pathlib.Path) -> None:
    """TC-158 (FR-004-AC-29): valid trailing forms still bind scope."""
    assert shutil.which("quire") is not None, "a guard-capable quire CLI is required"
    ids = _quire_rust_implements_ids(
        tmp_path,
        '#[implements("FR-001-AC-1")] // why\n'
        "pub fn trailing_comment() {}\n"
        '#[implements("FR-001-AC-2")] pub fn same_line() {}\n'
        '#[implements("FR-001-AC-3" ,)]\n'
        "pub fn spaced_comma() {}\n"
        '#[implements("FR-001-AC-4"\n,)]\n'
        "pub fn newline_comma() {}\n",
    )
    assert ids == {"FR-001-AC-1", "FR-001-AC-2", "FR-001-AC-3", "FR-001-AC-4"}, ids


_STRUCTURAL_SPEC = (
    "---\nid: FR-001\ntype: FR\ntitle: Structural cases\n---\n\n"
    "## Acceptance Criteria\n\n"
    "| ID | Criteria | Verification |\n| --- | --- | --- |\n"
    "| FR-001-AC-1 | First case. | Unit |\n"
    "| FR-001-AC-2 | Second case. | Unit |\n"
)


def _quire_coverage(tmp_path: pathlib.Path, files: dict[str, str]) -> dict:
    assert shutil.which("quire") is not None, "a guard-capable quire CLI is required"
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec" / "FR-001.md").write_text(_STRUCTURAL_SPEC)
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
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
    return json.loads(result.stdout)


def _edges(report: dict) -> set[tuple[str, str, str, str]]:
    return {
        (e["path"], e["symbol"], e["trace_id"], e["form"])
        for e in report.get("implements", [])
    }


_PY_PRODUCTION = (
    "from ix_trace_py import implements\n"
    "import ix_trace_py\n"
    "import ix_trace_py as t\n\n"
    '@implements("FR-001-AC-1")\ndef plain():\n    pass\n\n'
    '@ix_trace_py.implements("FR-001-AC-2")\ndef qualified():\n    pass\n\n'
    '@t.implements("FR-001-AC-1")\ndef renamed():\n    pass\n'
)
_TS_PRODUCTION = (
    'import * as ixTrace from "@agent-ix/ix-trace-ts";\n'
    'import { implementing } from "@agent-ix/ix-trace-ts";\n'
    'import * as t from "@agent-ix/ix-trace-ts";\n\n'
    '@implementing("FR-001-AC-1")\nexport class Decorated {\n'
    '  @ixTrace.implementing("FR-001-AC-2")\n  method(): void {}\n}\n\n'
    'export const wrapped = implementing("FR-001-AC-1")(() => 1);\n'
    'export const qualified = ixTrace.implementing("FR-001-AC-2")(() => 2);\n'
    'export const renamed = t.implementing("FR-001-AC-1")(() => 3);\n'
)


@pytest.mark.integration
@pytest.mark.trace("TC-162", "FR-004-AC-33")
def test_quire_credits_structural_python_typescript_implements(
    tmp_path: pathlib.Path,
) -> None:
    """TC-162 (FR-004-AC-33): each accepted spelling mints production scope,
    never backed evidence; a renamed import binds nothing."""
    report = _quire_coverage(
        tmp_path, {"src/mod.py": _PY_PRODUCTION, "src/mod.ts": _TS_PRODUCTION}
    )
    edges = _edges(report)
    assert {e for e in edges if e[0] == "src/mod.py"} == {
        ("src/mod.py", "plain", "FR-001-AC-1", "python-implements-decorator"),
        ("src/mod.py", "qualified", "FR-001-AC-2", "python-implements-decorator"),
    }
    ts = {e for e in edges if e[0] == "src/mod.ts"}
    assert {(e[1], e[2], e[3]) for e in ts} == {
        ("Decorated", "FR-001-AC-1", "typescript-implements-decorator"),
        ("Decorated.method", "FR-001-AC-2", "typescript-implements-decorator"),
        ("wrapped", "FR-001-AC-1", "typescript-implements-wrapper"),
        ("qualified", "FR-001-AC-2", "typescript-implements-wrapper"),
    }
    assert not any(e[1] in ("renamed",) for e in edges), edges
    assert report["totals"]["backed"] == 0


@pytest.mark.integration
@pytest.mark.trace("TC-163", "FR-004-AC-34")
def test_quire_binds_nothing_from_python_typescript_implements_comments(
    tmp_path: pathlib.Path,
) -> None:
    """TC-163 (FR-004-AC-34): the removed line-comment forms mint no relation."""
    report = _quire_coverage(
        tmp_path,
        {
            "src/mod.py": "# Implements: FR-001\ndef f():\n    pass\n",
            "src/mod.ts": "// Implements: FR-001\nexport function f(): void {}\n",
        },
    )
    assert _edges(report) == set()


@pytest.mark.integration
@pytest.mark.trace("TC-164", "FR-004-AC-35")
def test_quire_binds_nothing_for_misplaced_structural_markers(
    tmp_path: pathlib.Path,
) -> None:
    """TC-164 (FR-004-AC-35): `implements` on a test symbol and `trace` on a
    production symbol bind nothing, for Python and TypeScript."""
    report = _quire_coverage(
        tmp_path,
        {
            "tests/test_mod.py": (
                "from ix_trace_py import implements\n\n"
                '@implements("FR-001-AC-1")\ndef test_x():\n    pass\n'
            ),
            "src/mod.py": (
                "import pytest\n\n"
                '@pytest.mark.trace("FR-001-AC-1")\ndef production():\n    pass\n'
            ),
            "tests/mod.test.ts": (
                'import { implementing } from "@agent-ix/ix-trace-ts";\n'
                'it("x", implementing("FR-001-AC-1")(() => {}));\n'
            ),
            "src/ctl.py": (
                "from ix_trace_py import implements\n\n"
                '@implements("FR-001-AC-2")\ndef ctl():\n    pass\n'
            ),
            "src/ctl.ts": (
                'import { implementing } from "@agent-ix/ix-trace-ts";\n'
                'export const ctl = implementing("FR-001-AC-2")(() => 1);\n'
            ),
            "src/mod.ts": (
                'import { trace } from "@agent-ix/ix-trace-ts";\n'
                'export const production = trace("FR-001-AC-1")(() => 1);\n'
            ),
        },
    )
    # TypeScript test symbols are `it`/`test` calls, which no decorator can
    # attach to, so the wrapper nested in one binds nothing (FR-062-AC-24). The
    # controls prove the engine binds the same markers on production symbols.
    assert _edges(report) == {
        ("src/ctl.py", "ctl", "FR-001-AC-2", "python-implements-decorator"),
        ("src/ctl.ts", "ctl", "FR-001-AC-2", "typescript-implements-wrapper"),
    }
    assert report["totals"]["backed"] == 0


@pytest.mark.trace("TC-157")
def test_implements_is_a_separate_list_from_markers(traceability: dict) -> None:
    """TC-157 (FR-004-AC-28, CR-028): the form sets stay separate.

    quire-rs CR-061 stopped `verifies` binding production symbols because a doc
    comment citing `FR-053-AC-1` would otherwise count as evidence backing it.
    Two lists is what keeps one typo from moving a form across that line.
    """
    tags = traceability["trace_tags"]
    marker_names = {m["name"] for m in tags["markers"]}
    implements_names = {f["name"] for f in tags["implements"]}

    assert not marker_names & implements_names, marker_names & implements_names


@pytest.mark.trace("TC-072", "FR-004-AC-12")
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


@pytest.mark.trace("TC-073", "FR-004-AC-13")
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


@pytest.mark.trace("TC-074", "FR-004-AC-14")
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


def _verification_lint_rule() -> dict:
    manifest = load_yaml_strict(pack.MANIFEST_PATH.read_text())
    rules = [r for r in manifest["lint_rules"] if r.get("column") == "Verification"]
    assert len(rules) == 1, rules
    return rules[0]


@pytest.mark.trace("TC-149", "FR-004-AC-21")
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


@pytest.mark.trace("TC-149", "FR-004-AC-21", "FR-004-AC-23")
def test_verification_lint_accepts_withdrawn_and_flags_invalid_values(tmp_path) -> None:
    """TC-149 (FR-004-AC-21): the behavioural half — `quire lint` against a
    fixture document. A `Verification` cell reading `Test (TC-999)` reports a
    `acceptance-criterion-verification-method` finding at `warning` severity
    naming the id. A bare class, catalog method or declared withdrawal token
    raises nothing; Planned and a misspelled withdrawal remain invalid.

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
        pytest.fail("the `quire` CLI is required for lint")

    fixture = tmp_path / "lint-verification-column.md"
    fixture.write_text(
        "---\nid: FR-999\ntype: FR\ntitle: Fixture\n---\n\n"
        "## Acceptance Criteria\n\n"
        "| ID | Criteria | Verification |\n|----|----------|--------------|\n"
        "| FR-999-AC-1 | bare class | Test |\n"
        "| FR-999-AC-2 | catalog method | property-based-testing |\n"
        "| FR-999-AC-3 | withdrawn tombstone | Withdrawn |\n"
        "| FR-999-AC-4 | stale TC id | Test (TC-999) |\n"
        "| FR-999-AC-5 | stale IT id | Inspection (IT-3) |\n"
        "| FR-999-AC-6 | live future behavior | Planned |\n"
        "| FR-999-AC-7 | misspelled retirement | Withdrawnn |\n"
    )
    result = subprocess.run(
        ["quire", "lint", "--module", str(pack.PACK_ROOT), str(fixture)],
        capture_output=True,
        text=True,
        check=False,
    )
    findings = result.stdout + result.stderr
    assert result.returncode == 0, findings
    assert all(f"row {row}:" not in findings for row in (1, 2, 3)), findings
    for row, needle in ((4, "TC-999"), (5, "IT-3"), (6, "Planned"), (7, "Withdrawnn")):
        line = (
            "warning: acceptance-criterion-verification-method: section "
            f"'Acceptance Criteria' column 'Verification' row {row}:"
        )
        assert line in findings, findings
        assert needle in findings, findings


@pytest.mark.trace("FR-004-AC-22", "TC-151")
def test_verification_lint_rule_allowed_set_is_classes_union_catalog(
    manifest: dict,
) -> None:
    """TC-151 (FR-004-AC-22): the `allowed` set equals the four IADT classes
    union every `verification_catalog` key and retirement token, exactly —
    derived-by-assertion rather than hand-maintained, so an entry added to the
    catalog and the lint rule cannot silently drift apart. `Eval` and
    `Manual` remain test types, not methods or retirement tokens."""
    rule = _verification_lint_rule()
    classes = {"Test", "Inspection", "Analysis", "Demonstration"}
    catalog_keys = set(manifest["verification_catalog"])

    retirement = set(manifest["traceability"]["vocabularies"]["retired"])
    assert set(rule["allowed"]) == classes | catalog_keys | retirement
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
