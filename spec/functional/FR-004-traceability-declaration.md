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
- `trace_targets` **SHALL** mint an id class from a section **only where the
  shape contract declares that section**, and **SHALL NOT** invent one. A target
  on a heading no archetype admits declares the corpus's mistake into the model,
  and a target missing from a section the contract already validates leaves the
  two halves disagreeing — which is what `FR-nnn-CON-n` is until
  `agent-ix/quire-rs#327` lands.
- Every minting target whose rows carry a verification column **SHALL** ship with
  a `document_references` entry reading that column. `unbacked_rows` is built by
  walking document references, so a target with none contributes to the
  denominator and can never name which of its rows is unbacked.
- An id class a tag can name and no target mints **SHALL** carry a written
  decision in the manifest naming either the target that mints it or the reason
  it is not minted, and where that reason is an engine limit, the ticket that
  owns it. An absence is not a decision: it reads to an author exactly like a
  typo, and the report cannot tell them apart either.

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
| FR-004-AC-11 | `rust-test-name-id` binds both spellings of its token — `fn tc744_x` and `fn tc_744_x` render the same `TC-744` — while the separator stays optional, adds no capture group, and admits nothing new: a bare `fn tc_x`, an unanchored `tc_744_` outside a `fn` position, and a digit run with no trailing `_` all still match nothing. | Test (TC-071) |
| FR-004-AC-12 | `vocabularies.test_type` declares the three ISO 29148 verification methods — `Inspection`, `Analysis`, `Demonstration` — alongside the harness kinds, and `no_source_symbol` carries the two that mint no symbol (`Inspection`, `Analysis`) but not `Demonstration`, which is observed running. | Test (TC-072) |
| FR-004-AC-13 | The `Traces To` column pattern admits a lone `-` as the explicit no-trace form for a row that traces to nothing, and still rejects prose, a bare word, and a malformed id. | Test (TC-073) |
| FR-004-AC-14 | `trace_targets` declares a target minting StR validation-criterion ids from the `Validation Criteria` table, and declares none for IT or US — whose criteria are list items and headings, which a `section`+`id_column` target cannot mint. | Test (TC-074) |
| FR-004-AC-15 | Every doc-comment form (`rust-doc-comment-id`, `python-docstring-id`, `typescript-doc-comment-id`) requires a trailing delimiter after the id list, so a sentence beginning with an id is not read as a tag; the authored forms — trailing colon, parenthesis, slash, dash, period, and end of line — all still bind. | Test (TC-075) |
| FR-004-AC-16 | `typescript-test-name-id` reads a trace id from a test registration's own title — `it`/`test` and their `.modifier` chains, in either quote or a template literal, with or without `await`, and on a wrapped title — and renders it through `id_format` with one capture group. It binds **no suite header** in any spelling (`describe(`, `suite(`, `test.describe(`, `it.describe(`, `test.describe.only(`), because the modifier chain is an allowlist rather than a `\w+` window; it binds nothing that is not a registration at the start of a line; and its trailing delimiter terminates the id rather than truncating it, so a suffixed id (`TC-092a`) and a dashed sub-id (`TC-008-LIST`) bind nothing rather than binding their base row. | Test (TC-077) |
| FR-004-AC-17 | `trace_targets` declares no target minting from a section no archetype's `body_extraction` declares — no entry names `Invariants` in any spelling, and no `NFR`-bound entry names `Constraints` — and the manifest carries the written decision for each id class `#69` names, each naming the ticket that owns it: `agent-ix/quire-rs#244` for `SC`, `agent-ix/quire-rs#327` for the blocked `CON` target, `agent-ix/quire-rs#328` for the bare-`FR-nnn` diagnostic. | Test (TC-078) |

> **CR-041 note (2026-08-24):** the written decision for the five id classes
> `agent-ix/spec-artifacts-process#69` names — `CON`, `INV`, `SC`, `VC` and bare
> `FR-nnn` (EPIC `agent-ix/quire-rs#264` Wave 3). Four are settled here; the
> fifth is settled as **mint** and blocked, and the blocker is measured rather
> than asserted.
>
> **What the numbers count.** Unit: entries in `coverage.untracked_symbols`, one
> per `verifies` relation whose id is neither declared, referenced by a cell, nor
> any row's own id (quire-rs `coverage.rs:1247-1254`) — **not** deduplicated by
> id, so three tests naming `FR-030-CON-1` are three entries. Population: the
> **241** repositories `quire-rs/scripts/corpus.py` enumerates under `~/dev`.
> Instrument: **one** `quire` binary built from `quire-cli` at its pinned rev,
> engine `e06f121` (quire-rs `epic/264-detection-minting-integrity` HEAD),
> release profile, self-reported by every payload. Declaration:
> `qa-corpus/modules/ecosystem` @ `79398fc`, copies differing in exactly one
> declaration. Method: `quire coverage --scope <repo> --json` per repository,
> reading the payload — nothing re-implemented, which is the lesson of
> `agent-ix/quire-rs#309`.
>
> **The ticket's table was stale in three of five rows**, and the three figures
> in circulation for it — 572, 322, 687 — disagreed with each other; none had
> been produced by the engine. Against a baseline of **5,309 / 20,030 rows backed
> = 26.51%** and **1,195** `untracked_symbols` entries:
>
> | class | entries | repos | decision |
> |---|---|---|---|
> | `CON` | 155 | 28 | **mint**, blocked on `agent-ix/quire-rs#327` |
> | `SC` | 124 | 7 | unreachable — `agent-ix/quire-rs#244` |
> | bare `FR-nnn` | 212 | 30 | **explicitly non-minting** |
> | `INV` | 1 | 1 | **explicitly non-minting** |
> | `VC` | 0 | 0 | already minted, CR-037 |
>
> **`CON` — mint it, and the two halves of the model already say so.**
> `spec-artifacts-iso` declares the FR `Constraints` table in `body_extraction`
> with `id_column: ID` and `id_pattern: '^{id}-CON-\d+$'`, so the *shape*
> contract validates `FR-001-CON-1` while the *traceability* model mints nothing
> for it, and a test carrying that id binds perfectly and joins to nothing.
> Resolved per id against each repository's `spec/`: **102 of the tagged
> `CON`/`INV` ids are defined by an `ID` row in an `## Constraints` table on an
> `FR` document**, 4 on an `NFR`, 1 under `## Invariants`, 1 in a matrix section
> only, and **19 name no row anywhere** — a real authoring error the engine is
> right to report. **Bad rule or bad corpus**, settled by opening files: sampled
> 12 of the 202 `CON`-in-test-file sites, one per repository across 12 of the 33
> — **12 of 12 are genuine authored tags**, each asserting exactly the constraint
> its id names
> (`filament-parser-lib/tests/filament/tier1/test_frontmatter_extraction.py:109`
> over a test asserting `result.nodes[0].data == {}`;
> `identity/tests/test_mfa_model.py:148`;
> `platform-test-kit/tests/unit/test_capture.py:113`;
> `ts-auth-sdk/tests/AuthClient.device.test.ts:133`). Not one is a prose citation.
> Declaring the target and its reference is measured at rows minted
> **20,030 → 23,059 (+3,029)**, rows backed **5,309 → 5,452 (+143)**, `-CON-`
> untracked symbols **155 → 34 (−121)**, **2,693** constraint rows gaining a
> locus in `unbacked_rows`, `binding_census` **byte-identical** in all three
> languages and status lies unchanged at **904**. An independent script counts
> **3,225** `ID` rows in `FR`/`NFR` `## Constraints` tables and the engine mints
> exactly 3,225 — instrument and script agree to the row.
>
> **Why it does not ship yet.** Backing **26.51% → 23.64%** and unbacked rows
> **13,889 → 16,582** are the denominator becoming honest and are not the
> objection. The objection is **`section-matches-nothing` 512 → 1,672
> (+1,160)**: `## Constraints` is *optional* in the FR contract ("Constraints is
> optional (no filler rows)") and a `TraceTarget` has no way to say so — quire-rs
> states the opposite outright, that "a trace target's section is not optional"
> (`corpus/declared_tables.rs:69-73`). **Sampled 11 of the 1,160 across 11
> repositories: 10 rule, 1 real.** Ten are FR documents legitimately without the
> section and without any `CON` id
> (`quire-rs/spec/functional/FR-003-archetype-schema-surface.md`,
> `ix-cli/spec/functional/core/FR-023-ix-logout.md`,
> `cloud-manager/spec/functional/FR-006-observability.md` among them); the one
> real find is
> `platform-test-kit/spec/functional/FR-009_isolated_deployment.md`, which writes
> `FR-009.2-CON-1` as an **H4 heading** rather than a table row.
>
> **The controlled corpus caught it, which is what it is for.** Vendoring the two
> entries into `agent-ix/qa-corpus` and running it: **19 of 75 cases fail, 34
> mismatches, 100% of them `section-matches-nothing`.** Thirteen assert a silence
> that is no longer true; six assert `diagnostic_paths` and receive the wrong
> finding, because a reason token is not scoped to the declaration that raised it
> — including `section-name-mismatch` and `section-and-id-column`, the flagship
> `#270` pair. Neither is repairable without **lowering** those assertions, and
> authoring a `## Constraints` table into 19 fixtures to dodge the finding is the
> corpus-side workaround CR-036 refused on principle. Filed as
> `agent-ix/quire-rs#327` — one key, `required: false`, mirroring the
> `body_extraction` key on the very table the target would mint from.
>
> **The other four are decisions in the manifest, not absences**, under one rule:
> *the traceability model mints from sections the shape contract declares, and
> does not invent sections.*
>
> - **`FR-nnn-INV-n` — not minted.** `## Invariants` is declared by neither
>   module. 15 repositories author it anyway (129 rows) and its table is literally
>   `| ID | Constraint | Type | Rationale |`. **One tag in the whole corpus names
>   one of those ids** (`identity/tests/test_tenant_auth_policy.py:195`).
>   Measured rather than assumed free: `section: [Constraints, Invariants]` moves
>   23,059/5,452 → 23,387/5,453 — 328 denominator rows to reach one tag, under a
>   heading no archetype admits. `NFR` `## Constraints` (4 tagged ids) is refused
>   for the same reason; declaring the section upstream in `spec-artifacts-iso` is
>   its fix.
> - **`IT-nnn-SC-nn` — unreachable, an engine limit rather than a decision.** 124
>   entries in 7 repositories. Those ids are list items: **1,356 occurrences
>   across 28 repositories, 243 directly under `## Test Procedure`**, against 148
>   table occurrences — and all 148 of those are *references* from a matrix, not a
>   minting table. `agent-ix/quire-rs#244` owns it, as this file has recorded
>   since CR-037.
> - **`StR-nnn-VC-n` — already minted**, by CR-037 (#63, closed 2026-08-22,
>   before #69 was filed), and the class has **no population at all**: 36 rows
>   minted in `filament-ide-rs`, 22 in `quire-rs`, 18 in `ix-cli`, backed **0** in
>   every one, because not one `StR-nnn-VC-n` tag exists anywhere in any declared
>   form. A fixture for it would have landed GREEN and taught nobody anything.
> - **Bare `FR-nnn` — not minted, deliberately.** 212 entries across 30
>   repositories. A rule joining `FR-006` to `FR-006-AC-1..7` would back **every**
>   criterion of a requirement from one test naming the requirement. Not a `#307`
>   near miss either: that ticket pairs ids differing by zero padding, case or
>   separator, and these differ by a whole id segment. The *diagnostic* that
>   should say "`FR-006` is not a trace target; use `FR-006-AC-n`" is not
>   expressible by a module and is filed as `agent-ix/quire-rs#328`.
>
> **None of these tags vanishes for `agent-ix/quire-rs#312`'s reason when it sits
> on a test function** — the census counts every one and counts it as bound. The
> 275 `CON` sites reaching neither channel are that separate population: 229 in
> **non-test files**, where every enclosing symbol is production, and 46 at module
> scope or on a helper. #312 keeps its fix.
>
> **Deliberately not bundled, measured first:** adding `constraint` to
> `traces-to.targets`. **313 `Test Case Summary` rows across 18 repositories**
> already write a `CON` id in `Traces To`, so the population is real — but with
> that one list changed and nothing else, every field of the payload is identical
> across all 241 repositories. Zero movement, so it waits for a reason true
> independent of the count. FR-004-AC-17, TC-078.

> **CR-040 note (2026-08-24):** TypeScript gains `typescript-test-name-id`, the
> analogue of `rust-test-name-id` (`agent-ix/spec-artifacts-process#68`, EPIC
> `agent-ix/quire-rs#264` Wave 3). TypeScript declared four trace forms and none
> of them read a test's name.
>
> **What the numbers count.** Population: the **241** repositories
> `quire-rs/scripts/corpus.py` enumerates under `~/dev` — non-hidden top-level
> directories carrying `spec/`, minus `SKIP_DIRS`, `SUPERSEDED` and verified
> `-task<N>` worktree siblings. Instrument: **one** `quire` binary built from
> `quire-cli` at its pinned rev, engine `08e5ed4`, self-reported by all 482
> payloads. Variable: the module path — two copies differing in exactly one file
> and exactly one declared form.
>
> Registration census over `.ts`/`.tsx` in that corpus:
>
> | chain | sites | id at the head of the title |
> |---|---|---|
> | `it(` | 5,106 | 496 |
> | `test(` | 1,167 | 363 |
> | `describe(` | 1,512 | 77 |
> | `test.describe(` | 120 | 33 |
> | `it.each(` | 33 | 0 |
>
> **860 test registrations carry an id at the head of their title**, and all 860
> spell the separator `-` — so `[-_]?` admits **zero** extra sites today and is
> there for the reason CR-034's `_?` is: `tc-503` and `tc_503` are one token.
>
> **Measured effect** — same binary, only the declaration changed; unit: Test
> Matrix rows and evidence symbols; population as above:
>
> | metric | declared | + one form | delta |
> |---|---|---|---|
> | rows minted | 20,028 | 20,028 | **0** |
> | rows backed | 5,044 | 5,308 | **+264** |
> | row backing | 25.18% | 26.50% | **+1.32pt** |
> | unbacked rows | 14,403 | 13,889 | **−514** |
> | status lies | 1,104 | 904 | **−200** |
> | typescript bound | 1,043/6,199 | 1,685/6,199 | **+642** |
> | rust bound | 2,804/6,307 | 2,804/6,307 | **0** |
> | python bound | 2,050/12,741 | 2,050/12,741 | **0** |
> | untracked symbols | 1,086 | 1,196 | **+110** |
>
> Rust and Python being byte-identical is the half that says the change is the
> one declared. **7 of 241 repositories change their backed-row count**, and **12** change on at least one
> published metric — three of the six gaining untracked symbols gain no backed row. An
> earlier draft said "move at all", which the `+110 untracked in 6 repositories` figure in
> this same note refutes. `filament-ide-rs` goes
> backed **1,354/2,540 (53%) → 1,529/2,540 (60%)**, typescript bound
> **10/408 (2.5%) → 363/408 (89.0%)**, unbacked **468 → 182**, status lies
> **209 → 55**, untracked symbols **25 → 25**.
>
> **The ticket's own baseline differs, and `agent-ix/quire-rs#322` is why.** #68
> measured `ts 19/524 → 465/524` on an engine where `test.describe(` registered
> a `TestFunction` — 116 suite headers in that denominator, ~102 of them binding
> a header tag as evidence. #322 made them `Container`s. Both readings land on
> 89%; the honest one is over the corrected pool.
>
> **The number that gets worse: untracked symbols +110**, in 6 repositories —
> and it is settled by opening them. **Sampled 12 sites across all 6: 0 invented
> bindings.** `ui-workflow-pane` `TC-048`…`TC-056` are real tests whose Test Case
> Summary stops at `TC-047`; `ix-cli` `TC-421` and `filament-editor-gateway`
> `TC-030` are named only in a *Functional Coverage* table; `ts-observability`
> declares `TC-006`/`TC-007` under an id column spelled `` `ID` `` rather than
> `Test ID`; `user-admin-ui` — 49 of the 110 — has **no `## Test Case Summary`
> at all**. Every one is a real tag the binder previously could not read.
>
> **Bad rule or bad corpus, recall direction: sampled 12 of the 154
> `filament-ide-rs` rows that stopped being status lies, 12 rule, 0 real** —
> TC-974, TC-454, TC-1031, TC-1176, TC-1018, TC-844, TC-1351, TC-664, TC-657,
> TC-1094, TC-965, TC-845, each with a real test whose title matches the row's
> stated claim.
>
> **The anchors are the design, and they are not what #68 sketched.** That sketch
> named `describe` outright and reached `test.describe(` through its
> `(?:\.\w+)?` window; measured, it matches **148 sites this form refuses — 110
> suite headers and 38 suffixed or dashed sub-ids**. A suite header is not
> evidence (quire-rs CR-119/#322) and **226 real corpus suite headers carry an
> id** — 148 bare `describe(` and 78 `test.describe(`, matching this module's own
> manifest census, which an earlier draft of this note contradicted with 224/146 inside
> one change. The bare half is method-sensitive (a predicate over every `.ts`/`.tsx`
> rather than test files gives 176); the 78 is stable, and the claim rests on the measured
> zero below rather than on the count, so — `regex` having no lookaround — the modifier chain is an
> **allowlist** and `describe`/`suite` are structurally unable to appear.
> **[RAN]** those headers verbatim into one scope with a matrix declaring
> all 188 ids: backed **0/189**, typescript bound **0/225**, while a
> positive-control `it("tc-503: …")` in the same tree backs exactly 1 — the zero
> is a measurement, not an absent harness. A second scope closes the
> container-span route: `test.describe("tc-888: …")` wrapping
> `test("tc-999: …")` backs `TC-999` and leaves `TC-888` unbacked.
>
> **The `id_format` hazard is inherited and stated, not discovered later.**
> `TC-{1}` renders captured digits verbatim exactly as the Rust form does, so
> `it("tc-1: …")` mints `TC-1` against a row declaring `TC-001` — that is
> `agent-ix/quire-rs#307`, unchanged in either direction, and zero-padding is not
> expressible in `id_format`. It produced **0** short ids in this sweep.
>
> **Deliberately out of reach:** the curried `it.each([…])("tc-503: …")` title
> (**0 of 37 `.each` sites carry an id**), and the 61 ids in attached comments
> and 45 in file-level docblocks #68 counts — those need
> `agent-ix/quire-rs#273`'s symbol, not a title form.

> **CR-034 note (2026-08-22):** `rust-test-name-id` gains an optional separator
> — `'\bfn (?i:tc)(\d+)_'` becomes `'\bfn (?i:tc)_?(\d+)_'`
> (`agent-ix/spec-artifacts-process#59`, epic `agent-ix/quoin#197`).
>
> **What the number counts:** function-definition sites in
> `agent-ix/filament-ide-rs` @ `3349cf8` (24 crates, ~143k LOC), counted by
> spelling, under `quire 0.29.0` / engine `quire-rs v0.42.0` /
> `spec-artifacts-process v0.23.0`. `fn tc_NNN_` (underscore): **1,292**.
> `fn tcNNN_` (the declared spelling): **0**. Every tracking tag written in that
> repository's dominant convention bound nothing.
>
> **Measured effect** of changing this one pattern in a copy of the module and
> re-running `quire coverage --scope .` with `--module <copy>` — unit: Test
> Matrix rows; population: 2,389 rows in that repository:
>
> | metric | declared | with separator | delta |
> |---|---|---|---|
> | backed | 555 | 1158 | **+603** |
> | backed % | 23% | 48% | **+25pt** |
> | unbacked rows | 1538 | 528 | **−1010 (−66%)** |
> | status lies | 761 | 265 | **−496 (−65%)** |
> | untracked symbols | 19 | 32 | +13 |
>
> **Bad rule, not bad corpus** — settled by opening documents, not by the delta.
> **Sampled 10 flipped rows: 10 rule, 0 real.** Every one has a real test
> carrying its id — TC-914 at
> `crates/filament-backend/tests/reindex_code_postgres.rs:1081`, TC-1341 at
> `crates/filament-backend-client/src/liveness.rs:360`, TC-216 at
> `crates/filament-retrieval/src/fusion.rs:454`, TC-113 at
> `crates/filament-shell/src/open.rs:366`, and six more bound through their doc
> comment. The justification is independent of the count: **`fn tc744_x` and
> `fn tc_744_x` are the same token under the declared convention** — `tc`, the
> number, then the name — and `(?i:tc)` already admits four spellings of that
> token, so the separator is the same class of variation.
>
> **Precision does not move.** `_?` is anchored on both sides, adds no capture
> group and no list, and the `+13` untracked symbols are the confirmation rather
> than the cost: all thirteen are real tests whose ids no matrix declares
> (TC-1058, TC-1060…TC-1069 in the `filament-cli`/`filament-mcp` front-door
> suites, TC-1484 ×2 in `embedding_worker.rs`). The widened form surfaces
> genuine orphan tests; it binds no garbage.
>
> **The comment that appeared to forbid this** said `rust-test-name-id` is
> "deliberately not widened". That is CR-024, and it is about **list support** —
> the comma-separated-group widening applied to the `*-trace-line` and
> `*-comment-id` forms, which cannot apply to a form rendering `TC-{1}` over a
> function name. Orthogonal to the separator. Both notes now say which axis they
> mean.
>
> **Deliberately not fixed here:** the same repository writes `/// Tracing:`
> 643 times against a declared `rust-trace-line` keyword of `Trace:`. **That one
> is bad corpus.** Measured, widening to `Trac(?:e|ing):` on top of this change
> buys **+56 backed** while taking untracked symbols from **32 to 200** — those
> lines are semicolon-separated and carry `Task-NNN` ids, so the comma form
> reads ids that are not test-case declarations. Precision loss for marginal
> recall; the corpus is swept onto the declared form instead
> (`agent-ix/filament-ide-rs#460`).
>
> **Consequence for published reviews.** Three SpecReviews in filament-ide-rs
> (SR-150, SR-151, SR-152) cite coverage figures computed under the broken
> pattern; those figures measure marker-form mismatch, not coverage. SR-152's
> FND-004 concludes "binding is on the `tc_NNNN_` function name" — the form that
> bound nothing at all. FR-004-AC-11, TC-071.

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
> assumed: `quire-rs` v0.41.0, then **both** `quire-cli` v0.28.0 (the binary
> `subprocess` tests shell out to) and the `quire` **Python wheel** (which
> `testmatrix_sweep.py` imports), then `spec-artifacts-iso` v0.18.0 for the
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
