---
id: FR-004
title: "Traceability declaration: what mints trace ids, what references them, how a test carries one"
type: FR
relationships:
  - target: "ix://agent-ix/quire-rs/spec/functional/FR-050"
    type: "requires"
    cardinality: "1:1"
  - target: "ix://agent-ix/quire-rs/spec/functional/FR-051"
    type: "requires"
    cardinality: "1:1"
---
# FR-004: Traceability declaration: what mints trace ids, what references them, how a test carries one

## Description

The module **SHALL** declare a complete `traceability:` model — trace targets,
document references, and the trace-tag grammar — so `quire coverage` can
reconcile a Test Matrix claim against a real test.

Coverage is not an engine concept: quire knows nothing of "FR", "AC" or "TC",
and `trace_tags` and `document_references` are the two registries with **no
engine fallback** (unlike `observable_verbs` and `vacuous_predicates`, which
modules only extend). Undeclared means an empty registry, which means no
`verifies` relation can ever be minted, which means every row in the ecosystem
is unbacked. [FR-051](ix://agent-ix/quire-rs/spec/functional/FR-051) specified
the three marker forms and deferred the production declaration to "a follow-up
change in `spec-artifacts-iso`"; this requirement is that follow-up, landing
here because the rest of the model is already here and a model split across two
modules can version apart.

## Inputs

- The module manifest's `traceability:` block
- A repository scope: a spec bundle plus the source tree its trace tags live in

## Outputs

- A `TraceabilityModel` that loads and validates (quire-rs `traceability.rs`)
- A non-empty `quire coverage` rollup over any repo in the ecosystem

## Behavior

- `trace_targets` **SHALL** mint test-case ids from the Test Matrix and
  acceptance-criterion ids from `FR` and `NFR` documents.
- **Every** target and reference **SHALL** be bound by `archetype`, the Test
  Matrix included, and **SHALL NOT** declare a `document` path — quire-rs
  deleted that form (CR-062) and rejects the key outright.
- There **SHALL** be one entry per *kind* of table, never one per filename. The
  retired form needed three near-identical entries — `spec/tests.md`,
  `spec/matrix.md`, `spec/evals.md` — and still reached nothing nested, so a
  matrix at `spec/<module>/matrix/tests.md` minted zero ids however correctly it
  was authored. A matrix is reached by what it *is*, not by what it is called.
- Every target and reference **SHALL** declare an `exclude` covering every
  test-tree convention in the ecosystem — `tests/**`, `tests_integration/**` and
  `fixtures/**`.
  Archetype binding admits fixtures, because a fixture exercising the
  `FR` contract *is* typed `FR` — that is what makes it a fixture. Scope
  exclusion, not the absence of typed fixtures, is what keeps a phantom id out
  of the rollup.
- `trace_tags.markers` **SHALL** declare one canonical marker per supported
  language — Python `@pytest.mark.trace(...)`, Rust `#[trace(...)]`, TypeScript
  `trace(...)` — each carrying an authoring `template`, which is what makes a
  migration suggestion derivable.
- Every `legacy` form **SHALL** declare a `language` and a `rewrite_to` naming a
  marker of that **same** language. A form spanning languages can name only one
  target marker, so it would suggest Rust attribute syntax inside a `.py` file.
- `trace_tags.implements` **SHALL** declare one comment form per supported
  language, each carrying a `template`, and each **SHALL** require the literal
  keyword `Implements:` before the id list. The keyword is the prose guard: the
  `legacy` `*-comment-id` forms bind a bare id after `//` and need a
  trailing-delimiter rule to stop a sentence flowing through, whereas here a
  sentence that merely names a requirement matches nothing.
- The module **SHALL** declare those forms as a list separate from `markers`,
  never as a flag on one. `markers` mint `verifies` — evidence, which may back an
  acceptance criterion — and `implements` mints scope, which may not. A shared
  list with a discriminator field would put one typo between the two.
- Every `document_references` entry **SHALL** name only declared `targets`, and
  **SHALL** opt into `expand_ranges` and `strip_annotations` where the corpus
  authors ranges (`FR-001-AC-1 .. FR-001-AC-4`) or qualifiers
  (`TC-024 (blocked: …)`) — both default off (FR-050-AC-12).

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-004-AC-1 | The model declares trace targets minting test-case ids from the Test Matrix and acceptance-criterion ids from `FR` and `NFR`, and loads without a validation error | Test (TC-028) |
| FR-004-AC-2 | Every trace target and document reference is bound by `archetype` and declares no `document` path, the Test Matrix included; matrix entries additionally declare an `exclude` covering test data; and there is exactly one entry per kind of table (`test-case`, `traces-to`, `functional-coverage`), never one per matrix filename | Test (TC-029, TC-039) |
| FR-004-AC-3 | `trace_tags.markers` declares exactly one marker for each of rust, python and typescript, and each declares a `template` | Test (TC-030) |
| FR-004-AC-4 | Every `legacy` form declares a `language`, and its `rewrite_to` names a marker of that same language | Test (TC-031) |
| FR-004-AC-5 | Every `document_references.targets` name is a declared trace target, and every `pattern` compiles with at least one capture group | Test (TC-032) |
| FR-004-AC-6 | `quire coverage` over this repo reports a non-zero backed count and mints no rows from `tests/fixtures/` | Test (TC-033) |
| FR-004-AC-7 | The model declares `vocabularies.test_type_column` and a `no_source_symbol` list naming only test-type values whose verification method mints no source symbol. | Test (TC-034) |
| FR-004-AC-8 | Every `legacy` form without an `id_format` declares its id as a comma-separated list, so a match carries every id the line names; a form declaring `id_format` declares a single id; and the `*-comment-id` delimiter still rejects prose flowing through an id. | Test (TC-035) |
| FR-004-AC-9 | Every `trace_targets` entry and every `document_references` entry declares a non-empty `exclude` covering every test-tree convention (`tests/**`, `tests_integration/**`, `fixtures/**`), so a typed fixture mints no id in any consuming repository. Since CR-062 this covers the matrix entries too, and is what makes archetype binding safe for them. | Test (TC-036) |
| FR-004-AC-10 | `trace_tags.implements` declares exactly one templated form for each of rust, python and typescript; every pattern requires the literal `Implements:` before the id list and captures a comma-separated list; and a sentence naming a requirement in prose matches none of them. | Test (TC-066) |

> **CR-031 note (2026-08-20):** cross-reference only — the status **vocabulary
> declared here is unchanged**. What changed is that FR-003's `column_patterns`
> contract has stopped admitting `⚠️`, a marker this model never classed.
>
> Recorded here because this file owns the `traceability:` block that was the
> source of truth all along, and because the divergence ran in the direction
> nothing checked: the contract admitted a superset. The guard in
> `test_column_vocabularies_have_one_source` is now bidirectional, so a future
> marker added to either side without the other fails at test time rather than
> becoming invisible at rollup time.

> **CR-028 note (2026-08-19):** the module declares `trace_tags.implements`
> (quire-rs FR-062) — the marker forms that bind **production** code to the
> requirement it is about.
>
> **What was missing.** `verifies` links an evidence symbol to a trace id.
> Nothing linked a requirement to the code that implements it, so mutation
> scoping (quoin FR-039) had no file set to mutate. **[RAN]** across quire-rs's
> 52 functional requirements: **38 had at least one mutable target, 14 had
> none** — and the fourteen fail for one reason, that every symbol verifying
> them lives in `tests/`. Reach correlated with **test placement**, not with
> requirement quality (quire-rs CR-071).
>
> **Why a second list and not a flag.** quire-rs CR-061 stopped `verifies`
> binding production symbols precisely because a doc comment in `src/foo.rs`
> that merely *cites* `FR-053-AC-1` would otherwise count as evidence backing
> it. Widening `verifies` was the wrong fix and so is a shared list with a
> discriminator, which puts one typo between scope and evidence. Two lists, two
> relation types, and complementary symbol kinds — `markers` bind only
> test/benchmark/fuzz symbols, `implements` only functions and containers — so a
> mis-declared form binds **nothing** rather than the wrong thing.
>
> **A comment form, not an attribute.** `#[implements("…")]` would need a proc
> macro in every consuming crate, and the point is to annotate production code
> that already exists. `attached_source` spans the leading comment block, so a
> line above the item binds to it. Comma lists, same grammar as the `Trace:`
> forms, because authors already write them that way (CR-024 measured 98 lines
> carrying 205 ids across `~/dev`).
>
> **Criterion ids are admitted** (`FR-001-AC-1`, not only `FR-001`). Scoping
> truncates to the requirement trivially, whereas rejecting the shape would make
> a plausibly-authored marker bind nothing silently — the failure this whole
> programme keeps finding.
>
> **Ordering, and the defect it exposed.** This cannot ship against an engine
> older than quire-rs **v0.38.0**. v0.36.0 minted the relation and v0.37.0
> carried it into `coverage --json`, but the forms a *module* declared were
> dropped between the manifest and the binding — `merge_traceability` and
> `TraceabilityModel::is_empty` are hand-maintained per-field functions and
> neither listed the key. Declaring this block is what surfaced it (quire-rs
> CR-081); against v0.37.0 the declaration loads and mints nothing.

> **CR-062 note (2026-08-17):** FR-004-AC-2 **reverses**: every entry is now
> archetype-bound and `document:` is gone, because quire-rs deleted the form
> (agent-ix/quire-rs#74). Both halves of the original justification changed.
>
> The first half is simply void: the corpus walk no longer skips `tests.md`
> (type-driven membership, quire-rs#73, v0.26.0), so archetype binding sees the
> canonical matrix. The second half — archetype binding admits matrices that are
> test data — is still true, and is answered by `exclude:` rather than by path
> enumeration. That is why AC-9 now covers the matrix entries as well, and why
> the exclusion is asserted rather than assumed: dropping it readmits the 67
> phantom ids from `tests/fixtures/testmatrix/*.md` that this declaration
> recorded, 50 of them reported "backed".
>
> Enumeration was the cost nobody had priced. Three entries per table kind, one
> per filename the ecosystem happens to use, reaching nothing nested. **[RAN]**
> `scripts/sweep_coverage.py` over `~/dev`, 238 repositories, worktrees deduped:
> collapsing nine declarations to three takes ecosystem dead trace tags from
> **1,401 occurrences / 1,052 distinct ids to 1,207 / 873**, and
> `filament-ide-rs` — the one repository authoring nested module matrices — from
> **214 dead tags to 20**, its rollup going 17/850 to **473/2,184** rows backed.
> Rebinding only `test-case` leaves 49 there: `traces-to` and
> `functional-coverage` were path-bound too and could not read the nested
> matrices they describe, which is why all three collapse together.
>
> One ecosystem precondition had to land first, and it is the reason this is not
> a pure win on its own: a **mistyped** matrix now mints nothing, where under
> path binding frontmatter was irrelevant. 6 matrices in the ecosystem declared
> `type: index` while carrying a Test Case Summary; uncorrected, this change took
> repositories minting zero test-case ids from 154 to **159**. All six were
> corrected first and the sweep re-run: **153**.

> **CR-025 note (2026-08-15):** FR-004-AC-6 was already the right gate and this
> declaration failed it — outside this repository. TC-033 measures `quire
> coverage` over **this** repo, whose fixtures are Test Matrices, and matrix
> targets are path-bound, so nothing typed `FR`/`NFR` was ever in reach here.
>
> **The claim that justified the omission was false.** The manifest and this
> requirement both stated that no fixture in the ecosystem is typed `FR`/`NFR`.
> **[RAN]** `quire coverage --scope . --json` in `quire-cli` against the
> pre-change and post-change manifests: 6 fixture documents minted criterion
> ids — `tests/fixtures/validate-mod/docs/{valid,placeholder,missing-section,
> unknown-object}-fr.md` and `tests/fixtures/lint-mod/docs/{clean,warn}.md` —
> putting **9 phantom criteria** in the denominator (total 215 → 206). Backed
> stayed 27 and no group's ratio moved, so nothing real was excluded and, in
> that repo, nothing was falsely *backed*; the damage was denominator
> inflation, not a false green.
>
> **[RAN]** Ecosystem sweep for typed `FR`/`NFR` under any test tree:
> `quire-cli` (13 corpus docs — an earlier grep said 15 by counting two `.rs`
> hits), `filament-parser-lib` (2), `cloudmanager-local-sync` (1). All
> fixtures; no repository authors a real requirement under a test tree. Two of
> them sit under `tests_integration/`, which `tests/**` alone never covers —
> `cloudmanager-local-sync/tests_integration/fixtures/fastapi-service/spec/FR-001-test.md`
> and `filament-parser-lib/tests_integration/fixtures/FR-001.md`, both typed
> `FR` and both colliding with a real `FR-001` in their repo. Neither mints AC
> rows today, so no phantom is live, but the first Acceptance Criteria table
> added to one would mint silently; the declared exclusion covers both
> conventions so it cannot.
>
> AC-9 exists because AC-6 is only checkable where the phantom happens to
> land. A declaration-level assertion holds in every consuming repository,
> including ones this suite never runs in.

> **CR-024 note (2026-08-14):** A legacy form declaring a single id matches once
> and stops at the comma, so `// Trace: FR-001-AC-1, FR-001-AC-2` bound the
> first id and the rest was never *read*. **[RAN]** 98 such lines across `~/dev`,
> worktrees and `-task<N>` copies excluded, carried **205 ids that bound to
> nothing across 17 repos** — every shape declared here and all three languages.
>
> **Both halves are required, and the filing said otherwise.**
> agent-ix/quire-rs#68 stated that no module needs to re-declare anything.
> Verified against real input, that is false: capture group 1 is *already* a
> single id, so splitting it in the engine converts nothing. The engine splits
> group 1 the way `marker_ids` splits a marker's argument list (quire-rs
> FR-051-AC-16, shipped in v0.21.0); this declaration widens the group so there
> is something to split.
>
> **`rust-test-name-id` is not widened.** It declares `id_format`, and `TC-{1}`
> renders over a function name, which cannot carry a list. The engine leaves the
> template path unsplit for the same reason, so widening it here would be a
> declaration the engine ignores.
>
> **The delimiter still holds.** The `*-comment-id` forms admit `,` as an id
> terminator, so a greedy list consumes the separators and the delimiter falls
> through to the real terminator. Verified against `// TC-033, TC-034`,
> `// TC-033, TC-034: why`, `// TC-033 - prose`, `// TC-033, TC-034,` and the
> quire-rs `// TC-480 / FR-025-AC-1: …` convention, which is `/`-separated and
> still binds `TC-480` alone. The prose guard CR-002's predecessor measured is
> intact: `# FR-003-CON-1 sweep found in real matrices` still matches nothing.
>
> **Ordering:** this cannot ship against an engine older than quire-rs v0.21.0.
> A widened group there yields a single id of literally `"A, B"`, which resolves
> to nothing — strictly worse than today.

> **CR-002 note (2026-08-14):** A status lie is a row claiming evidence it does
> not have. A row verified by an agent-behaviour eval or by a manual step cannot
> have that evidence — neither produces a symbol a trace tag could attach to —
> so reporting it as a lie asserts something its own declared method makes
> impossible. Measured in `quoin`: 40 of its 55 status lies were eval rows
> (agent-ix/quoin#65).
>
> `no_source_symbol` names the values that are exempt, and `test_type_column`
> names the column they are read from. The engine withdraws the lie and nothing
> else: the row stays in `unbacked_rows` and the backed/total counts are
> untouched (quire-rs FR-050-AC-16).
>
> `Static`, `Benchmark` and `Compile` are deliberately **not** exempt. Each is
> usually asserted by real code — this repo's own static boundary audit is a
> test — so exempting them would hide overclaims rather than explain them.
>
> **Ordering:** this could not ship before quire-rs v0.20.0 / quire-cli v0.14.0.
> `ColumnVocabularies` is `deny_unknown_fields`, so declaring the keys against an
> older engine fails module load outright and took 31 of this repo's own tests
> with it.

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md),
  [FR-003](./FR-003-testmatrix-body-extraction.md), quire-rs
  [FR-050](ix://agent-ix/quire-rs/spec/functional/FR-050) (coverage rollup) and
  [FR-051](ix://agent-ix/quire-rs/spec/functional/FR-051) (source symbol
  extraction + trace tags)
- **Downstream**: the quoin `gap-analysis` wiring, which reads the rollup rather
  than grepping for tags

## Known Limits

Recorded rather than papered over:

- `US` acceptance criteria are authored as a bullet list and `declared_tables`
  reads tables only; `StR` criteria are validated by review, not by a test.
  Neither is minted — a denominator nothing can satisfy is noise, not rigour.
- The two CR-017 authoring shorthands the shape contract admits — continuation
  (`FR-001-AC-2, -AC-3`) and slash enumeration (`FR-016-AC-1/2/3`) — are not
  expanded by the engine, so such a cell contributes its first token only.
- Most `Verification` cells carry no test id: a sweep over quire-rs, quoin and
  this repo found 285 bare `Test` against 99 `Test (TC-nnn)`. Those rows are
  answerable for their own criterion id instead.
