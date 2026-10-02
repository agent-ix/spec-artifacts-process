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
  acceptance-criterion ids from `FR`, `NFR` and `interface` documents. An
  acceptance-criterion target bound to an archetype whose template does not
  guarantee the minting section on every document **SHALL** declare
  `required: false`, so an ordinary document of that archetype without the
  section is healthy rather than a false `section-matches-nothing`.
- `trace_targets` **SHALL** mint a `constraint` target from the `FR` `##
  Constraints` section's `ID` column, the same archetype-bound, `exclude`-scoped
  shape as `acceptance-criterion` — a `-CON-` id is minted by the same
  mechanism a criterion id already is, because the section is a table with an
  `ID` column exactly like `## Acceptance Criteria` (PLAT-1079). The `constraint`
  target **SHALL** declare no `evidence: reference_only`: a constraint is a
  criterion, and it enters the same evidence-bearing denominator
  `acceptance-criterion` does. An `Inspection`-verified `-CON-` row is handled
  by its declared method, not by excluding the row — the computed matrix
  reports it under `method-without-symbol` the same way an `Inspection`-verified
  acceptance criterion already is, never as an unbacked test-case claim.
  `constraint` **SHALL** be added to the `targets` of both `traces-to`
  (`manifest.yaml:948`) and `inspection-obligation` (`manifest.yaml:896-899`):
  declaring the target alone mints the id but resolves no existing `-CON-`
  reference in a `Traces To` cell and discharges no constraint through an
  `Inspections` record, so both reference declarations widen alongside it.
- A `Verification` cell in an `FR`, `NFR` or `interface` Acceptance Criteria
  table **SHALL** name a method only, with no `TC-…`/`IT-…` id. TC ids are
  retired ecosystem-wide (epic PLAT-1076): a criterion is now bound to its
  evidence directly by trace tag, so a lingering test-case id in that cell is
  stale data. This is enforced as a declarative `lint_rules` entry (quire-rs
  FR-036, `table_column_values`), not a `document_references`/`trace_targets`
  change — quire-rs rejects a `document_references` entry that declares an
  empty `targets` at module load (confirmed against
  the pinned engine, so an earlier draft of this requirement that emptied
  `verification`/`nfr-verification`'s `targets` would have failed module load
  for every consumer). The existing `verification`, `nfr-verification` and
  `interface-verification` document references are **unchanged** by this
  requirement — they stay `targets: [test-case]` and keep resolving a `TC-…`
  id exactly as before, and are retired later, with the Test Matrix itself,
  not by this ticket.
  - The rule's `allowed` set **SHALL** be the four IADT classes
    (`Test`/`Inspection`/`Analysis`/`Demonstration`) **union** every method id
    the manifest's `verification_catalog` declares — `unit-testing`,
    `property-based-testing`, `fuzzing`, `agent-behaviour-eval`, and every
    other catalog key — derived from the manifest, not hand-maintained
    as a second list. A `Verification` cell is also the `acceptance-criterion`
    obligation's `method_column`, and quire-rs FR-054-AC-11 accepts either a
    class or a catalog method id there; restricting the lint rule to the four
    classes alone would warn on an author who follows FR-007's own CR-005
    guidance and writes the precise method (`property-based-testing`) instead
    of the class (`Test`). `Eval` and `Manual` **SHALL NOT** be added: they
    are `traceability.vocabularies.test_type` (Test Matrix) values, not
    catalog method ids, and this column is never populated from that
    vocabulary.
  - The lint rule **SHALL** declare `severity: warning`. This SHALL is
    already violated by existing `Test (TC-…)`/`Inspection
    (TC-…)` cells across this repository's own FR/NFR Acceptance Criteria
    tables — an error-severity rule would fail
    every one of them the moment it shipped. **PLAT-1081** sweeps and clears
    that existing population; **PLAT-1082** promotes the rule from `warning`
    to `error` once the sweep clears it. Neither is this ticket's job.
  - This requirement's own new rows — FR-004-AC-20, FR-004-AC-21 and
    [FR-007-AC-15](./FR-007-verification-method-catalog.md) — **SHALL** name a
    bare method in their own `Verification` cell (no `TC-148`/`TC-149`/`TC-150`
    in the cell), so the criteria that mint this rule do not themselves
    violate it. `spec/tests.md` still traces each to its TC row through the
    Functional Requirement Coverage table, which is a different column and
    is not affected.
  - **This module owns the `FR`/`NFR`/`interface` `Verification`-column
    contract**, because it already owns the `verification_catalog` (FR-007)
    and the obligation sources that read the cell (FR-007-AC-8/AC-15) — the
    lint rule is a third thing reading a cell this module already governs
    two ways, not a new cross-module reach. `spec-artifacts-iso` declares a
    duplicate, conflicting rule today (`ac-verification-method`,
    `manifest.yaml:795-803`) that admits a `TC-\d+` annotation the rule above
    rejects; since `lint_rules` merge across every loaded module, the two
    contradict for the same column. **PLAT-1085** removes `iso`'s rule and
    drops the `TC-…` annotation from its StR sibling rule. PLAT-1085 and this
    module's release **SHALL** ship together — a released default module set
    **SHALL NOT** carry both contracts at once.
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
| FR-004-AC-1 | The model declares trace targets minting test-case ids from the Test Matrix and acceptance-criterion ids from `FR`, `NFR` and `interface`, and loads without a validation error | Test (TC-028) |
| FR-004-AC-2 | Every trace target and document reference is bound by `archetype` and declares no `document` path, the Test Matrix included; matrix entries additionally declare an `exclude` covering test data; and there is exactly one entry per kind of table (`test-case`, `traces-to`, `functional-coverage`), never one per matrix filename | Test (TC-029, TC-039) |
| FR-004-AC-3 | `trace_tags.markers` declares exactly one marker for each of rust, python and typescript, and each declares a `template` | Test (TC-030) |
| FR-004-AC-4 | Every `legacy` form declares a `language`, and its `rewrite_to` names a marker of that same language | Test (TC-031) |
| FR-004-AC-5 | Every `document_references.targets` name is a declared trace target, and every `pattern` compiles with at least one capture group | Test (TC-032) |
| FR-004-AC-6 | `quire coverage` over this repo reports a non-zero backed count and mints no rows from `tests/fixtures/` | Test (TC-033) |
| FR-004-AC-7 | The model declares `vocabularies.test_type_column` and a `no_source_symbol` list naming only test-type values whose verification method mints no source symbol. | Test (TC-034) |
| FR-004-AC-8 | Every `legacy` form without an `id_format` declares its id as a comma-separated list, so a match carries every id the line names; a form declaring `id_format` declares a single id; and the `*-comment-id` delimiter still rejects prose flowing through an id. | Test (TC-035) |
| FR-004-AC-9 | Every `trace_targets` entry and every `document_references` entry declares a non-empty `exclude` covering every test-tree convention (`tests/**`, `tests_integration/**`, `fixtures/**`), so a typed fixture mints no id in any consuming repository. Since CR-062 this covers the matrix entries too, and is what makes archetype binding safe for them. | Test (TC-036) |
| FR-004-AC-10 | `trace_tags.implements` declares exactly one templated form for each of rust, python and typescript; every pattern requires the literal `Implements:` before the id list and captures a comma-separated list; and a sentence naming a requirement in prose matches none of them. | Test (TC-066) |
| FR-004-AC-11 | `rust-test-name-id` binds both spellings of its token — `fn tc744_x` and `fn tc_744_x` render the same `TC-744` — while the separator stays optional, adds no capture group, and admits nothing new: a bare `fn tc_x`, an unanchored `tc_744_` outside a `fn` position, and a digit run with no trailing `_` all still match nothing. | Test (TC-071) |
| FR-004-AC-12 | `vocabularies.test_type` declares the three ISO 29148 verification methods — `Inspection`, `Analysis`, `Demonstration` — alongside the harness kinds, and `no_source_symbol` carries the two that mint no symbol (`Inspection`, `Analysis`) but not `Demonstration`, which is observed running. | Test (TC-072) |
| FR-004-AC-13 | The `Traces To` column pattern admits a lone `-` as the explicit no-trace form for a row that traces to nothing, and still rejects prose, a bare word, and a malformed id. | Test (TC-073) |
| FR-004-AC-14 | `trace_targets` declares a target minting StR validation-criterion ids from the `Validation Criteria` table, and declares none for IT or US — whose criteria are list items and headings, which a `section`+`id_column` target cannot mint. | Test (TC-074) |
| FR-004-AC-15 | Every doc-comment form (`rust-doc-comment-id`, `python-docstring-id`, `typescript-doc-comment-id`) requires a trailing delimiter after the id list, so a sentence beginning with an id is not read as a tag; the authored forms — trailing colon, parenthesis, slash, dash, period, and end of line — all still bind. | Test (TC-075) |
| FR-004-AC-19 | The `interface-acceptance-criterion` target declares `required: false`, so an `interface` document with no Acceptance Criteria section is healthy; and an `interface_NNN-AC-N` id resolves everywhere an `FR`/`NFR` acceptance-criterion id already does — `inspection-obligation`, `traces-to`, the `Traces To` column check, every `legacy`/`implements` comment form, and a new `interface-verification` reference covering its own `Verification` column. | Test (TC-147) |
| FR-004-AC-20 | A `constraint` trace target is declared: archetype `FR`, section `Constraints`, `id_column: ID`, the same `exclude` glob set and evidence posture (`source`, not `reference_only`) as `acceptance-criterion`. `constraint` is added to the `targets` of `traces-to` and `inspection-obligation`. `quire coverage --json` over this repository mints `FR-NNN-CON-N` rows among `minted_targets`, and every `-CON-` reference already authored in `spec/tests.md`'s `Traces To` column resolves rather than reporting `dangling-trace-reference`. | Test |
| FR-004-AC-21 | A `lint_rules` entry (`table_column_values`, `severity: warning`) scoped to `FR`/`NFR`/`interface` requires the `Acceptance Criteria` table's `Verification` column to hold one of the four IADT classes (`Test`/`Inspection`/`Analysis`/`Demonstration`) or a `verification_catalog` method id, with no trailing `TC-…`/`IT-…` id. `quire lint --module <this module>` over a fixture document whose `Verification` cell reads `Test (TC-999)` reports a warning-severity finding naming the id; a cell naming a bare class or a bare catalog method id (e.g. `property-based-testing`) raises nothing; the rule is advisory, evaluated only by `quire lint`, and `quire validate` does not evaluate `lint_rules` at all. The `verification`/`nfr-verification`/`interface-verification` document references are unchanged. | Test |
| FR-004-AC-22 | The lint rule's `allowed` set is exactly the four IADT classes union every key of the manifest's `verification_catalog` — derived, not hand-maintained: a test loads both and asserts set equality, so an entry added to the catalog and the lint rule's `allowed` list cannot drift apart. `Eval` and `Manual` (`traceability.vocabularies.test_type` values, not catalog keys) are absent from `allowed`. | Test |

> **CR-064 note (PLAT-1079, 2026-09-27):** measured against this repository
> before authoring the above, not assumed from the ticket that asked for it.
>
> **The ticket's own premise was wrong in one place, and re-measuring is why
> that matters.** PLAT-1079 states constraints "are a trace target but not an
> obligation source." `manifest.yaml`'s `trace_targets` list carries no
> `constraint`/`-CON-` entry at all — and
> `-CON-` ids named in this repository's own `spec/tests.md` raised
> `dangling-trace-reference` warnings. Constraints were neither a trace target nor an obligation source;
> AC-20 here mints the target and FR-007-AC-15 declares the obligation source
> against it, and both are needed — an obligation source with no matching
> target has no id namespace to mint into (the same "declare both or load
> fails" shape `ObligationSource::target` already requires).
>
> **The other two asks resolve without a new declaration here, ruled
> 2026-09-27.** `-M-` ids need no `trace_targets` entry: quire-rs's computed
> CoverageMatrix (FR-050-AC-47, `agent-ix/quire-rs#494`) reconciles binders
> against every derived obligation as well as every trace target, and
> `nfr-metric` is already a declared obligation source — a second mint path
> for the same id would be the same namespace declared twice. `US` acceptance
> criteria need no declaration at all: the archetype's own template calls its
> only structured section illustrative, not verification criteria, so there
> is nothing normative to mint — a design fact recorded in Known Limits, not
> a gap awaiting an upstream change.

> **CR-065 note (fix round, PLAT-1079, 2026-09-27):** SR-018 and SR-019
> reviewed the draft and found AC-21 as originally drafted unshippable — a
> `document_references` entry with `targets: []` fails module load
> (confirmed against the pinned engine) rather than
> reporting a dangling reference (SR-018 FND-001). The mechanism above
> replaces it: a `lint_rules` `table_column_values` entry, advisory by
> construction, which is also how the severity SR-018 FND-002 asked for is
> stated directly rather than inherited from `dangling-trace-reference`'s
> fixed warning tier. FND-003's count of existing violations is why the rule ships at
> `warning`, not `error` (see Behavior above); FND-004 is why `constraint`
> is now named explicitly in `traces-to`/`inspection-obligation`'s `targets`,
> not left implied; FND-005's contradiction over `interface-verification` is
> resolved by leaving all three verification references untouched and scoping
> the new lint rule to `FR`/`NFR`/`interface` uniformly, rather than
> special-casing one of the three. FND-006 (LOW) is answered in AC-20's own
> wording: `constraint` is evidence-bearing (`source`), not
> `reference_only`.

> **CR-066 note (fix round 2, PLAT-1079, 2026-09-27):** SR-018's disposition
> pass 1 found the fixed rule's `allowed` list still wrong.
> Restricting it to the four IADT classes contradicts FR-007's own CR-005
> guidance to write the precise catalog method (`property-based-testing`,
> `fuzzing`) rather than the class, and quire-rs FR-054-AC-11 already accepts
> either in this same cell for the `acceptance-criterion` obligation's
> `method_column` — an author following FR-007 would have been warned by
> FR-004 for doing exactly what FR-007 asked (FND-007). AC-21/AC-22 above fix
> it: `allowed` is classes ∪ catalog keys, asserted equal by a test rather than
> re-typed as a second list, and `Eval`/`Manual` stay out because they are
> `test_type` values, not catalog method ids.
>
> **FND-008: this was never only this module's rule to add.**
> `spec-artifacts-iso` already declares `ac-verification-method` over the same
> archetypes, section and column, with an admitted `TC-\d+` annotation the
> rule above rejects — `lint_rules` merge across every loaded module, so a
> released default module set carrying both contracts is not two opinions, it
> is one column two modules disagree about. This module owns the correction
> because it already owns the two other things reading that cell — the
> `verification_catalog` (FR-007) and the obligation sources over it
> (FR-007-AC-8/AC-15) — so the lint rule is a third read of a cell this module
> already governs, not new territory. **PLAT-1085** removes `iso`'s rule and
> the `TC-…` annotation from its StR sibling rule; PLAT-1085 and this module's
> release ship together, so no released default module set ever carries both.
>
> **FND-009 (LOW):** the sweep and the promotion now have names —
> **PLAT-1081** (sweep) and **PLAT-1082** (promotion) — in place of "the
> epic's own sweep ticket."

> **CR-034 note (2026-08-22):** `rust-test-name-id` gains an optional separator
> — `'\bfn (?i:tc)(\d+)_'` becomes `'\bfn (?i:tc)_?(\d+)_'`
> (`agent-ix/spec-artifacts-process#59`, epic `agent-ix/quoin#197`).
>
> **Why:** every tracking tag written in `agent-ix/filament-ide-rs`'s dominant
> convention (`fn tc_NNN_`, with an underscore) bound nothing against the
> declared spelling (`fn tcNNN_`), so most of its Test Matrix rows read as
> unbacked. The justification does not depend on a count: **`fn tc744_x` and
> `fn tc_744_x` are the same token under the declared convention** — `tc`, the
> number, then the name — and `(?i:tc)` already admits four spellings of that
> token, so the separator is the same class of variation. `_?` is anchored on
> both sides and adds no capture group and no list, so precision does not move.
>
> **The comment that appeared to forbid this** said `rust-test-name-id` is
> "deliberately not widened". That is CR-024, and it is about **list support** —
> the comma-separated-group widening applied to the `*-trace-line` and
> `*-comment-id` forms, which cannot apply to a form rendering `TC-{1}` over a
> function name. Orthogonal to the separator. Both notes now say which axis they
> mean.
>
> **Deliberately not fixed here:** the same repository writes `/// Tracing:` against
> a declared `rust-trace-line` keyword of `Trace:`. **That one is bad corpus.**
> Widening to `Trac(?:e|ing):` would read semicolon-separated lines carrying
> `Task-NNN` ids, so the comma form would read ids that are not test-case
> declarations: precision loss for marginal recall. The corpus is swept onto the
> declared form instead (`agent-ix/filament-ide-rs#460`). FR-004-AC-11, TC-071.

> **CR-032 note (2026-08-20):** this module now **declares**
> `traceability.source_exclude` (quire-rs FR-050-AC-22 / CR-085,
> `agent-ix/quire-rs#199`).
>
> Three globs, all anchored at a fixture directory:
> `tests/fixtures/**`, `tests_integration/fixtures/**`, `fixtures/**`.
>
> **`tests/**` must never appear on this key**, and the distinction is the whole
> reason it is a separate key from `exclude`. The `exclude:` globs on the trace
> targets below *do* cover `tests/**`, because that is where **documents** must
> not be read from. `source_exclude` is the other root, and the majority of any
> repository's trace markers live under `tests/` — 194 of quire-rs's own ~458. A
> well-meaning harmonisation of the two lists would delete the evidence tree and
> read as an ecosystem-wide coverage collapse.
>
> **The release ordering is a hard edge, and it demonstrated itself.**
> `TraceabilityModel` is `#[serde(deny_unknown_fields)]`, so an engine that does
> not know the key does not ignore it — **module load fails**, for every command
> that loads the module set. Declaring it against the previously-installed
> toolchain turned 38 of this repository's 81 tests red with
> `unknown field 'source_exclude'`. The chain is therefore engine → **every**
> consumer → module, and it has four hops rather than the three the plan
> assumed: `quire-rs`, then **both** `quire-cli` (the binary
> `subprocess` tests shell out to) and the `quire` **Python wheel** (which
> `testmatrix_sweep.py` imports), then `spec-artifacts-iso` for the
> `additionalProperties: false` schema gate, and only then this module.

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
> scoping (quoin FR-039) had no file set to mutate. Some
> functional requirements had no mutable target, for one reason: every symbol
> verifying them lives in `tests/`. Reach correlated with **test placement**, not with
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
> forms, because authors already write them that way (CR-024).
>
> **Criterion ids are admitted** (`FR-001-AC-1`, not only `FR-001`). Scoping
> truncates to the requirement trivially, whereas rejecting the shape would make
> a plausibly-authored marker bind nothing silently — the failure this whole
> programme keeps finding.
>
> **Ordering, and the defect it exposed.** This cannot ship against an engine
> that predates the fix: the engine minted the relation and
> carried it into `coverage --json`, but the forms a *module* declared were
> dropped between the manifest and the binding — `merge_traceability` and
> `TraceabilityModel::is_empty` are hand-maintained per-field functions and
> neither listed the key. Declaring this block is what surfaced it (quire-rs
> CR-081); against such an engine the declaration loads and mints nothing.

> **CR-062 note (2026-08-17):** FR-004-AC-2 **reverses**: every entry is now
> archetype-bound and `document:` is gone, because quire-rs deleted the form
> (agent-ix/quire-rs#74). Both halves of the original justification changed.
>
> The first half is simply void: the corpus walk no longer skips `tests.md`
> (type-driven membership, quire-rs#73), so archetype binding sees the
> canonical matrix. The second half — archetype binding admits matrices that are
> test data — is still true, and is answered by `exclude:` rather than by path
> enumeration. That is why AC-9 now covers the matrix entries as well, and why
> the exclusion is asserted rather than assumed: dropping it readmits the
> phantom ids from `tests/fixtures/testmatrix/*.md`, which would be reported
> "backed".
>
> Enumeration was the cost nobody had priced. Three entries per table kind, one
> per filename the ecosystem happens to use, reaching nothing nested. Collapsing
> nine declarations to three removes the dead trace tags that nested module
> matrices produced. Rebinding only `test-case` would leave some: `traces-to`
> and `functional-coverage` were path-bound too and could not read the nested
> matrices they describe, which is why all three collapse together.
>
> One ecosystem precondition had to land first, and it is the reason this is not
> a pure win on its own: a **mistyped** matrix now mints nothing, where under
> path binding frontmatter was irrelevant. Matrices declaring `type: index`
> while carrying a Test Case Summary had to be corrected first.

> **CR-025 note (2026-08-15):** FR-004-AC-6 was already the right gate and this
> declaration failed it — outside this repository. TC-033 measures `quire
> coverage` over **this** repo, whose fixtures are Test Matrices, and matrix
> targets are path-bound, so nothing typed `FR`/`NFR` was ever in reach here.
>
> **The claim that justified the omission was false.** The manifest and this
> requirement both stated that no fixture in the ecosystem is typed `FR`/`NFR`.
> Fixtures typed `FR`/`NFR` under a test tree minted phantom criterion ids
> into the denominator; nothing real was excluded, and the damage was
> denominator inflation, not a false green. Some such fixtures sit under
> `tests_integration/`, which `tests/**` alone never covers; the declared
> exclusion covers both conventions so a later Acceptance Criteria table in one
> cannot mint silently.
>
> AC-9 exists because AC-6 is only checkable where the phantom happens to
> land. A declaration-level assertion holds in every consuming repository,
> including ones this suite never runs in.

> **CR-024 note (2026-08-14):** A legacy form declaring a single id matches once
> and stops at the comma, so `// Trace: FR-001-AC-1, FR-001-AC-2` bound the
> first id and the rest was never *read*. Ids written that way
> bound to nothing under every shape declared here and all three languages.
>
> **Both halves are required, and the filing said otherwise.**
> agent-ix/quire-rs#68 stated that no module needs to re-declare anything.
> Verified against real input, that is false: capture group 1 is *already* a
> single id, so splitting it in the engine converts nothing. The engine splits
> group 1 the way `marker_ids` splits a marker's argument list (quire-rs
> FR-051-AC-16); this declaration widens the group so there
> is something to split.
>
> **`rust-test-name-id` is not list-widened.** It declares `id_format`, and
> `TC-{1}` renders over a function name, which cannot carry a list. The engine
> leaves the template path unsplit for the same reason, so list-widening it here
> would be a declaration the engine ignores. This is a statement about **lists
> only** — see CR-034, which changes the separator on a different axis.
>
> **The delimiter still holds.** The `*-comment-id` forms admit `,` as an id
> terminator, so a greedy list consumes the separators and the delimiter falls
> through to the real terminator. Verified against `// TC-033, TC-034`,
> `// TC-033, TC-034: why`, `// TC-033 - prose`, `// TC-033, TC-034,` and the
> quire-rs `// TC-480 / FR-025-AC-1: …` convention, which is `/`-separated and
> still binds `TC-480` alone. The prose guard CR-002's predecessor measured is
> intact: `# FR-003-CON-1 sweep found in real matrices` still matches nothing.
>
> **Ordering:** this cannot ship against an older engine.
> A widened group there yields a single id of literally `"A, B"`, which resolves
> to nothing — strictly worse than today.

> **CR-002 note (2026-08-14):** A status lie is a row claiming evidence it does
> not have. A row verified by an agent-behaviour eval or by a manual step cannot
> have that evidence — neither produces a symbol a trace tag could attach to —
> so reporting it as a lie asserts something its own declared method makes
> impossible. In `quoin`, most status lies were eval rows
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
> **Ordering:** this could not ship before the engine learned the keys.
> `ColumnVocabularies` is `deny_unknown_fields`, so declaring the keys against an
> older engine fails module load outright and took this repo's own tests
> with it.

> **CR-063 note (2026-09-18):** `interface-acceptance-criterion` (quire-rs#460)
> shipped in one PR and this follow-up review round closes it out in the same
> PR, rather than a second one, per the finding rather than the plan.
>
> **`required: false`, BLOCKING.** `required` defaults to `true`
> (quire-rs `traceability.rs`), and the SOA `interface` template has no
> Acceptance Criteria section on most interface documents — so the declared
> (implicit) default raised a false `section-matches-nothing` on every
> ordinary interface doc. With `required: false`
> that false diagnostic is gone.
>
> The two `interface_004-AC-*` ids kept minting throughout — `required` gates
> the section-absent diagnostic, not the target itself.
>
> **The comment above the target cited the wrong mechanism and the wrong
> precedent**, corrected in place rather than left to mislead the next reader:
> the archetype match is a raw frontmatter `type:` string compare
> (quire-rs `src/corpus/declared_tables.rs::scan`), not a merged-registry
> lookup, and the real cross-module precedent is `FR`/`NFR`/`StR` — declared by
> `spec-artifacts-iso`, a different module — not `suite`/`inspection`, which
> this module declares itself and so binds same-module.
>
> **The underscore-object-id shape (`interface_004-AC-1`) now works everywhere
> an `FR`/`NFR` acceptance-criterion id already does**, proven with
> `quire coverage --module <scratch copy>` over a throwaway fixture rather than
> ~/.ix/filament/modules:
>
> - `inspection-obligation` and `traces-to` matched only the trailing `AC-1`
>   before — a wrong partial bind — because their KIND class admitted only
>   2–4 letters followed by a hyphen. Both now alternate that BASE token with
>   a generic underscore-object shape and add
>   `interface-acceptance-criterion` to `targets`.
> - The TestMatrix `Traces To` `column_patterns` check rejected
>   `interface_004-AC-1` outright (anchored, hyphen-only KIND); widened the
>   same way.
> - The `legacy`/`implements` comment, docstring and `Implements:` forms admit
>   it too — the open forms (`*-trace-line`) by the same BASE alternation, the
>   closed-enum forms (`*-comment-id`, `*-docstring-id`, `*-doc-comment-id`,
>   `*-implements-line`) by adding the same alternative alongside their
>   `TC|IT|FR|NFR|StR|US` enum, since those forms already bind `FR` ids today.
> - `interface-verification` is new, mirroring `verification`/
>   `nfr-verification`, so a stale `TC` id in an interface document's
>   `Verification` cell is reported rather than silently unchecked.
>
> **The PR's own "unbacked" claim was wrong.** QSpec already tags
> `tests/checked_package_v2.rs:5642` with `#[trace("TC-233",
> "interface-004-AC-1")]` — hyphenated, not the declared underscore shape —
> which the engine's near-miss diagnostic (`untracked-id-near-miss`) flags as
> the same id written twice, differing only in separator. It does not bind:
> `backed_trace_ids()` is an exact string match, and `interface-004-AC-1` !=
> `interface_004-AC-1`. QSpec#110 retags it to the underscore spelling, which
> then binds by exact match.
>
> FR-004-AC-19, TC-147.

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md),
  [FR-003](./FR-003-testmatrix-body-extraction.md), quire-rs
  [FR-050](ix://agent-ix/quire-rs/spec/functional/FR-050) (coverage rollup),
  [FR-051](ix://agent-ix/quire-rs/spec/functional/FR-051) (source symbol
  extraction + trace tags) and quire-rs FR-036 (declarative `lint_rules`,
  `table_column_values`) for AC-21
- **Ships with (PLAT-1085, spec-artifacts-iso)**: removal of `iso`'s
  conflicting `ac-verification-method` lint rule and the `TC-…` annotation on
  its StR sibling rule. Neither module releases this contract alone.
- **Downstream**: the quoin `gap-analysis` wiring, which reads the rollup rather
  than grepping for tags

## Known Limits

Recorded rather than papered over:

- `US` acceptance criteria are authored as a bullet list and `declared_tables`
  reads tables only; `StR` criteria are validated by review, not by a test.
  Neither is minted — a denominator nothing can satisfy is noise, not rigour.
  **Ruled on PLAT-1079** (2026-09-27), not merely deferred: `US`'s only
  structured content is `## Acceptance Examples (Illustrative)`
  (`spec-artifacts-iso`, `section_body` under that heading — unstructured
  prose carrying `### [US-NNN-EX-N] …` H3 headings, not a table). Both that
  archetype's own comment and this repository's own `US-001`/`US-002`
  (`spec/usecase/`) state the examples are **"illustrative only — not test
  cases and not verification criteria."** There is therefore nothing
  normative to mint: `US` gets no `trace_targets` entry and no obligation
  source, by design, not as a gap awaiting an upstream capability. If a
  future `US` archetype revision ever adds a normative acceptance-criteria
  table distinct from the illustrative examples, that is a
  `spec-artifacts-iso` decision to make first; nothing here depends on it or
  requests it.
- NFR metric rows (the `## Measurement and Evaluation` table `nfr-metric`
  obligation source mints, `{document}-M-{row}`) are an obligation source and
  **stay** that way — they are not also declared as a `trace_targets` entry,
  and PLAT-1079's ask for one is not needed. **Ruled on PLAT-1079**
  (2026-09-27): quire-rs's computed CoverageMatrix (FR-050-AC-47,
  `agent-ix/quire-rs#494`) reconciles binders against every declared
  **trace target and every derived obligation** — the obligation set already
  includes `nfr-metric`, so a test tagging `NFR-012-M-1` binds to the
  obligation id the same way any other criterion's trace tag binds to its
  obligation. `TraceTarget` needing no `id_format` synthetic-id mode of its
  own is the reason a second mint path was never required: the obligation
  *is* the referenceable id here, and a trace target would have minted the
  same id space twice under two names.
- The two CR-017 authoring shorthands the shape contract admits — continuation
  (`FR-001-AC-2, -AC-3`) and slash enumeration (`FR-016-AC-1/2/3`) — are not
  expanded by the engine, so such a cell contributes its first token only.
- Most `Verification` cells carry no test id: a sweep over quire-rs, quoin and
  this repo found 285 bare `Test` against 99 `Test (TC-nnn)`. Those rows are
  answerable for their own criterion id instead.
