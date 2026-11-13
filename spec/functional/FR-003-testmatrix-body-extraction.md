---
id: FR-003
title: "TestMatrix body extraction for structural matrix validation"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-001"
    type: "implements"
  - target: "ix://agent-ix/quire-rs/spec/functional/FR-033"
    type: "requires"
    cardinality: "1:1"
---
# FR-003: TestMatrix body extraction for structural matrix validation

## Description

The module **SHALL** declare a `body_extraction` contract on the `TestMatrix`
artifact type so that Quire machine-validates every `type: TestMatrix` document
(`tests.md`) against the Test Case Summary that the quoin
`spec-matrix` template emits. This requirement specifies the **structural and
vocabulary layer only**: column sets, id shapes, and cell vocabularies.
Resolving whether a referenced requirement/AC id actually exists is the
validation engine's cross-reference job and is out of scope here.

## Inputs

- A `TestMatrix` markdown document (`type: TestMatrix`), typically `spec/tests.md`
- The module's `testmatrix-frontmatter.schema.json` and the new `body_extraction` contract

## Outputs

- A validated `TestMatrix` artifact whose test-case rows are extractable as records
- Per-cell/per-table validation failures (reasons `missing` / `assert`) when the matrix drifts

## Behavior

- `body_extraction` **SHALL NOT** declare a `Functional Requirement Coverage`
  extraction, required or optional (PLAT-1499).
- `body_extraction` **SHALL** require a `Test Case Summary` `table_row`
  extraction with columns exactly
  `Test ID | Title | Type | Priority | Traces To | Status` and at least one row.
- The `Test ID` column **SHALL** be the id column and match
  `^(TC|IT)(-[A-Za-z0-9]+)+$` with at least one numeric segment. This admits the
  plain `TC-NNN` form, the template's `TC-INT-NNN`/lettered variants, and the
  segmented forms the ecosystem authors (`TC-060-01`, `TC-SB-001`,
  `TC-001-HEADER-PARSE` — 7 repo families), while still rejecting `TC1`,
  `tc-001`, `TC-`, `TCX-001`, and ids carrying trailing prose (CR-016).
  The prefix set mirrors the **declared evidence archetypes**, not a list of
  test kinds: `TC` and `IT` are the only two artifact types any module mints
  test ids for (CR-019).
- The `Type` column **SHALL** be constrained via the Quire `column_choices`
  assert (requires [FR-033](ix://agent-ix/quire-rs/spec/functional/FR-033)) to
  the **core evidence vocabulary** `Unit | Integration | E2E | Property | Fuzz |
  Benchmark | Static | Compile | Snapshot | Manual`, plus whatever the module
  declares in its `traceability.vocabularies.test_type` block. The core set
  names how the evidence is produced and what "pass" means — generative,
  measured against a threshold, compiler-enforced, tool-enforced, human — which
  is the distinction a matrix consumer acts on. Harness names (`pg_test`,
  `terraform plan`, `ecaz bench suite`) belong in `Title`, and a compound cell
  (`Unit / pg_test`) is two rows (CR-016).
- The `Priority` column **SHALL** be declared `optional_columns` — a matrix MAY
  omit it entirely — and, **when authored**, **SHALL** be constrained via
  `column_choices` to exactly `P0 | P1 | P2 | P3 | P4`, where P0 = must-pass
  blocker, P1 = critical path, P2 = standard, P3 = low, and
  P4 = nice-to-have/deferred (CR-018).
- The `Status` column **SHALL** be constrained via `column_patterns` to a
  leading status marker followed by an optional note:
  `^(✅|❌|🚧|⛔)(\s+.*)?$`. The marker carries the class and the note carries
  why — `🚧 scale evidence deferred` says something the bare marker cannot, and
  6 repo families already author decorated statuses. `⛔` marks a retired row.
  `⚠️` was admitted here and classed nowhere until CR-031 retired it.
  The classes these markers map to are declared once, in the module's
  `traceability.status` block, which the coverage rollup reads
  ([FR-050](ix://agent-ix/quire-rs/spec/functional/FR-050) CR-015) — the
  contract and the rollup SHALL NOT declare the vocabulary independently
  (CR-016).
- Each `Traces To` cell **SHALL** be constrained via the Quire
  `column_patterns` assert to one or more comma-separated trace tokens, each
  matching a `<KIND>-<N>` id with an optional `-<SUBKIND>-<M>` sub-id, where
  the kinds are **not** enumerated by the contract — the legal token set follows
  from the trace targets the module declares, and existence is checked by
  reference resolution
  ([FR-049](ix://agent-ix/quire-rs/spec/functional/FR-049)), not by this
  pattern. A cell MAY additionally use a same-prefix range (`FR-001..FR-006`)
  or carry a trailing parenthetical note (`FR-022-AC-5 (negative)`); both are
  normalized before resolution when the module declares `expand_ranges` /
  `strip_annotations` (CR-016)
  (constraint-boundary tests trace to CON rows; integration test cases trace
  to IT ids and their success criteria), i.e. the cell pattern
  `^((StR|US|FR|NFR)-\d+(-(AC|CON)-\d+)?|IT-\d+(-SC-\d+)?)(,\s*((StR|US|FR|NFR)-\d+(-(AC|CON)-\d+)?|IT-\d+(-SC-\d+)?))*$`;
  existence of the referenced ids is **not** checked by this contract.
  A cell MAY additionally use either **authoring shorthand** admitted by
  CR-017 — *continuation*, where a following token elides the parent id
  (`FR-001-AC-2, -AC-3, -AC-4`), and *slash enumeration* of sub-ids
  (`FR-016-AC-1/2/3/6`). Both denote exactly what the expanded list denotes.
  An **empty cell** and a placeholder dash (`—`) SHALL NOT be admitted: a test
  case that traces to nothing is precisely what a traceability matrix exists to
  surface.
- Test-case rows **SHALL** be extractable as records (`multiple: true`) so
  tooling (gap analysis, planning) can select each test case by id.
- `Test ID` values **SHALL** be unique within the `Test Case Summary` (a
  duplicate id makes record selection by id ambiguous). NOTE: the quire-rs
  extraction assert vocabulary (`LocatorAssert`: `columns`, `min_rows`,
  `id_column`/`id_pattern`, `choices`, `column_choices`, `column_patterns`)
  currently provides **no uniqueness assert**, so this criterion is normative
  but not yet machine-enforceable — enforcement depends on a new quire-rs
  engine capability (see Dependencies).
- `body_extraction` **SHALL NOT** declare an extraction for the
  `Stakeholder Requirement Coverage`, `User Story Coverage` or
  `Non-Functional Requirement Coverage` tables, required or optional (PLAT-1499).
- Sections the spec-matrix template marks conditional or scaffolding
  (`Integration Test Matrix`, `Option Permutation Matrix`,
  `Constraint Boundary Tests`, `Edge Cases`, `Coverage Gaps`,
  `Test Execution Summary`) **SHALL NOT** be required by the contract.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-003-CON-1 | The module version enforcing this `body_extraction` SHALL NOT be published until existing ecosystem `tests.md` files are normalized to the required shape; a sweep producing per-repo diffs for user sign-off precedes enforcement | Process | Inspection |


> **CR-039 note (2026-08-22):** the matrix layer gains its index half.
> `agent-ix/spec-artifacts-process#62`, epic `agent-ix/quoin#197`.
>
> A repository past a certain size does not have one matrix; it has a **tree**.
> `agent-ix/filament-ide-rs` states it outright in its own `CLAUDE.md` — *"root
> test matrix (TM-001), indexes module matrices + INT-NNN rows"* — and in the
> document's own Overview. Its root declares no test case and no
> functional-coverage row because both live one level down, in 12 module
> matrices. The archetype modelled only the leaf, so after bringing all 12
> module matrices onto the contract the root was the only remaining `[missing]`:
>
> ```
> spec/tests.md: [TestMatrix] required 'test_cases' (table_row(under Test Case Summary)) is missing [missing]
> spec/tests.md: [TestMatrix] required 'functional_coverage' (…) is missing [missing]
> ```
>
> **There was no way to clear those without inventing content.** Copying the
> 1,475 module test cases up into the root would duplicate every row and give
> the same TC two declaring matrices — which `check_artifact_ids.sh` rejects and
> which makes a tracking tag bind to *neither*.
>
> **A separate archetype, not a `role:` discriminator.** #62 offered both and
> preferred this one. It is also the only one expressible: `body_extraction`
> carries a single `yield_pattern` per archetype and cannot branch on a
> frontmatter value, so a discriminator would be a declaration the engine could
> not honour — the same wall CR-037 hit, one archetype over.
>
> **Two things the split buys that a variant would not.** An index mints no
> test-case ids, because `trace_targets.test-case` binds `archetype: TestMatrix`
> and this is not one — under the old typing the root was a *minting document
> that minted nothing*. And the index's own structure is asserted for the first
> time: #62 records that this repository's root matrix carried a subsystem row
> **missing its `Local Matrix` cell**, three columns where every other row had
> four, and no validator caught it. A declared `columns:` catches precisely
> that.
>
> **Optional where the corpus is genuinely optional.** The integration matrix
> and the coverage-gap register are `required: false`: a repository whose
> subsystems do not integrate has no `INT-` rows, and an absent gap register and
> an empty one are different claims — only the second is authored. Requiring
> either would force an empty table, which is the CR-018 mistake.
>
> Adoption is a one-line corpus change (`type: TestMatrix` →
> `type: TestMatrixIndex` on the root document) and nothing else moves.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-003-AC-1 | A `TestMatrix` doc with a conforming `Test Case Summary` validates | Test (TC-001) |
| FR-003-AC-2 | A doc missing the `Test Case Summary` table fails with reason `missing`; a `Test Case Summary` with a header and zero data rows fails with reason `assert`, and one with exactly one data row passes | Test (TC-001, TC-016) |
| FR-003-AC-3 | A `Type` cell outside the core evidence vocabulary and the module's declared extensions fails via `column_choices` (reason `assert`); every core value and every declared extension passes | Test (TC-001) |
| FR-003-AC-4 | A `Test ID` cell not matching `^(TC\|IT)(-[A-Za-z0-9]+)+$` with a numeric segment fails validation; the segmented ecosystem forms (`TC-060-01`, `TC-SB-001`, `TC-001-HEADER-PARSE`) pass, as does an `IT-NNN` id (CR-019); a prefix naming no declared archetype (`BENCH-001`, `AUDIT-001`, `SB-001`, `TCX-001`) fails | Test (TC-001) |
| FR-003-AC-5 | A `Status` cell not headed by one of `✅ ❌ 🚧 ⛔` fails via `column_patterns`; a marker followed by a note (`✅ Complete`, `🚧 scale evidence deferred`) passes. A `⚠️`-headed cell **fails**: the marker is retired, because `🚧` already carries that meaning and the contract had been admitting a value `traceability.status` classed as nothing (CR-031) | Test (TC-001, TC-008) |
| FR-003-AC-6 | A `Traces To` cell that is not comma-separated `<KIND>-<N>` tokens (with an optional `-<SUBKIND>-<M>` sub-id, a same-prefix range, or a trailing parenthetical note) fails via `column_patterns`; the contract enumerates no kind names | Test (TC-001) |
| FR-003-AC-7 | A `TestMatrix` doc validates whether or not it carries a `Stakeholder Requirement Coverage`, `User Story Coverage` or `Non-Functional Requirement Coverage` section, and no column set of such a section is asserted | Test (TC-014, TC-015) |
| FR-003-AC-8 | Test-case rows are extracted as one record per row (`multiple: true`) | Test (TC-001) |
| FR-003-AC-9 | The contract is added without altering the TestMatrix frontmatter schema or the other archetypes | Inspection |
| FR-003-AC-10 | A `Priority` cell outside `P0\|P1\|P2\|P3\|P4` fails via `column_choices` **when the column is authored**; a `Test Case Summary` that omits the `Priority` column entirely validates, and neither the missing column nor its absent cells are reported (CR-018) | Test (TC-001) |
| FR-003-AC-11 | A `Test Case Summary` containing two rows with the same `Test ID` fails validation | Test (TC-024) — blocked on a quire-rs uniqueness assert (none exists today) |
| FR-003-AC-12 | A `TestMatrixIndex` archetype models the **root index** of a matrix tree: it requires a `Requirements Traceability` table of `Subsystem \| Local Matrix` (navigation only: the requirement and status rollup of a subsystem is computed by `quire matrix`, never authored in the index) and optionally an `Integration Test Matrix` (`INT-NNN`) and a `Coverage Gaps` register (`GAP-NNN`). It requires no `test_cases` table, and it mints no test-case ids — `trace_targets.test-case` binds `TestMatrix` only, so an index is not a minting document. | Test (TC-076) |
| FR-003-AC-13 | A `TestMatrix` doc validates whether or not it carries a `Functional Requirement Coverage` section, and no column set of such a section is asserted | Test (TC-003) |
| FR-003-AC-14 | The shipped `TestMatrix` skeleton emits no `Functional Requirement Coverage` section, and its authoring comment states that requirement-to-criterion coverage is read from `quire matrix`, never authored | Test (TC-194) |
| FR-003-AC-15 | The `TestMatrix` manifest entry declares extractions for the `Test Case Summary` only; it declares none for the functional, stakeholder, user-story or non-functional coverage tables | Inspection (TC-017) |

> **PLAT-1499 note (2026-11-12):** the computed matrix is the single source of
> functional coverage.
>
> The required `Functional Requirement Coverage` table was a hand-kept copy of
> what `quire matrix` computes from criterion ids and trace tags. In
> `spec-artifacts-iso` it drifted: it marked untagged criteria Complete and
> listed criteria and a test case that do not exist (SR-028 FND-006). A hand
> table cannot be made to agree with the thing it duplicates; it can only be
> checked against it, and that check is a tracking ledger.
>
> **Dropped, not generated.** A generated table would be a second rendering of
> the matrix committed into every module, stale the moment a tag changes, and
> would need a generator, a freshness check and a regeneration step to stay
> honest. `quire matrix` already renders the same view on demand from the
> current tree, so the simplest change that removes the hand table is to stop
> declaring it. There is no tolerance layer for the old table: a module that
> still carries the section has prose the contract no longer reads, and deletes
> it in its own change.
>
> **Why a bullet carries no rationale.** The bullets state the prohibition; the
> reasoning is here. A hand-kept coverage table restates what `quire matrix`
> computes from the criteria and the tests' trace tags, so an authored copy can
> only drift from it.
>
> **Scope.** The same reasoning removes the optional stakeholder, user-story and
> non-functional coverage tables: `quire matrix` renders non-functional
> criteria, stakeholder-to-story edges live in `relationships:`, and a story's
> tests bind through each test case's `Traces To` cell. The `Requirements` and
> `Status` columns of the `TestMatrixIndex` `Requirements Traceability` table
> are the same rollup one level up, so the index keeps `Subsystem` and
> `Local Matrix` only. The `Test Case Summary` stays: it declares test-case
> records and their `Traces To` edges, which are authored facts, not derived
> ones.

> **CR-031 note (2026-08-20):** `⚠️` is **retired** from the `Status`
> vocabulary. agent-ix/spec-artifacts-process#52, agent-ix/quire-rs#192.
>
> The contract admitted `⚠️` at `column_patterns.Status` while
> `traceability.status` classed it as **nothing**. The two declarations
> disagreed, and the comment on the first even named the second as the source of
> truth while admitting a value it does not define.
>
> The consequence is not cosmetic. `StatusClass::class_of` returned `Unknown`,
> the coverage rollup's only consumer asked `== Complete`, and the row fell out
> of the report: **not backed, not a lie, listed nowhere.** A `⚠️` row was exempt
> from the status-lie check *by construction* — not because it was honest, but
> because the engine formed an opinion and discarded it. That is how six FR-016
> rows in `agent-ix/quire-cli` claimed evidence they did not have while
> `status_lies` read zero.
>
> **Retired rather than classed**, per the rule that unifying means enforcing.
> `🚧` already means pending, and every `⚠️` cell in the corpus reads
> `⚠️ Partial: …` or `⚠️ Pending` — the same meaning in a second form. A
> vocabulary that accepts every spelling enforces nothing.
>
> enforce**, the sequence the FR-042 EARS rollout used.
>
> **The guard that should have caught this now does.**
> `test_column_vocabularies_have_one_source` asserted only that every *classed*
> marker appears in the pattern — one direction, and the wrong one. It now
> asserts **set equality** both ways, and was confirmed to fail against the
> pre-change manifest (`admitted but not classed: ['⚠️']`) before the manifest
> was touched. A drift guard that cannot fail is the defect it exists to prevent.

> **CR-020 note (2026-08-13):** `Eval` joins the `test_type` vocabulary.
>
> CR-019 below settled that a prefix naming no declared archetype encodes in the
> id what the row already states one column over, and renamed `BENCH-`, `AUDIT-`,
> `SB-` and `IS-` to `TC-` on exactly that reasoning. `EV-` is the same case and
> was missed: quoin's `spec/evals.md` carries **bare `EV-nnn` ids shadowing
> `TC-EV-nnn` rows** — the same evals, numbered twice, with the code and the FR
> `Verification` cells (`Eval (EV-050)`) referring to the bare form.
>
> Collapsing that shadow needs a `Type` value to move the information into, and
> there was none: the rows sit at `Type: E2E`, which is not what an
> agent-behaviour eval is. This amendment adds the value; the rename itself is
> the consuming repo's, tracked in agent-ix/quoin#65.
>
> The two axes stay separate exactly as CR-019 states them — this is a new *kind
> of testing*, so it is a new `Type` value and needs no new prefix. It is also a
> pure widening: no document that validates today stops validating.
>
> One concrete consequence for coverage: a `Verification` cell reading
> `Eval (EV-050)` extracts no test id under the FR-004 reference patterns, which
> admit `TC`/`IT` only, so those rows fall back to their own criterion id. After
> the rename they bind directly.

> **CR-019 note (2026-08-07):** The `Test ID` prefix set is `TC|IT`, mirroring
> the declared **evidence archetypes** rather than enumerating kinds of
> testing. `spec-artifacts-iso` mints exactly two test-id families —
> `TC-{next:03d}` and `IT-{next:03d}` — so a contract admitting only `TC`
> contradicted a sibling module: `quire-cli` alone carries many `IT-` ids
> referenced across its spec files, minted the way the iso module
> declares. Every other artifact type that mints an id (`FR`, `NFR`, `US`,
> `SR`, `ADR`, `FB`, `GLO`) is a requirement or process artifact, not evidence.
>
> This is deliberately **not** a widening toward "whatever the corpus writes".
> The two axes are separate: *what kind of testing* a row records is the `Type`
> column's job and that vocabulary is open and module-extensible, while *what
> kind of artifact* an id names is closed, one prefix per declared archetype. A
> new technique — mutation, contract, chaos testing — is a new `Type` value and
> needs no new prefix, because it is still a test case in the matrix. A new
> prefix is justified only when a module declares a new archetype with its own
> document shape, at which point the manifest and this pattern change together.
>
> The three prefixes the sweep found that name no archetype — `BENCH-`/`AUDIT-`
> (quire-cli) and `SB-`/`IS-` (chat-window) — encode in the id
> what the row already states one column over (`Type: Benchmark | Static |
> Snapshot`), so they were renamed to `TC-` rather than admitted. No
> information is lost by that rename.
>
> **CR-018 note (2026-08-07):** `Priority` is now declared in
> `optional_columns` rather than required outright. The FR-003-CON-1 sweep
> found that many ecosystem matrices carry real, well-formed test-case
> rows with **no priority anywhere in the document** — not a formatting drift
> that a sweep can normalize, but planning data that was simply never
> recorded. The only two ways to enforce presence were to leave all of them
> permanently failing, or to write an invented priority into each. The second
> fabricates planning data to satisfy a checker, which is the exact failure
> mode this contract exists to catch, so the contract was fixed instead of the
> corpus. Nothing else relaxes: the column is still declared, still ordered,
> and its values are still constrained to `P0..P4` in every matrix that
> authors it (quire-rs FR-033-AC-14/15, CR-023). Requires an engine that
> accepts `optional_columns`: an older engine rejects it as an
> unknown assert key at load time.
>
> **CR-017 note (2026-08-06):** The FR-003-CON-1 gate was re-run and its
> failures classified (agent-ix/spec-artifacts-process#12).
>
> **Is the contract too narrow? Almost nowhere.** `Type` — **no amendment**: what
> remains is abbreviations of declared values (`Bench`, `Perf`), annotations
> belonging in `Title` (`Unit (git)`), harness names that are not test types
> (`pg_test`, `Storybook`, `axe-core`), and verification methods in the wrong
> column (`Inspection`, `Review`). CR-016 widened this once already; widening
> again would be fitting the check to non-conforming data. `Status` — **no
> amendment**: the pattern already admits a marker plus a note, and what remains
> is markers outside the set (`⬜`, `🔴`, `⊘`) and bare word statuses. Column
> headers — **no amendment**: the rest are genuinely different tables, mostly in
> the *optional* coverage sections.
>
> **One amendment, and only one.** `Traces To` rejects two legitimate authoring
> shorthands — continuation (`FR-001-AC-2, -AC-3, -AC-4`) and slash enumeration
> (`FR-016-AC-1/2/3/6`). Both denote exactly what the expanded list denotes and
> expanding them by hand makes matrices longer and no clearer, so the pattern now
> admits them. The other `Traces To` failures, `—` and empty, stay failing on
> purpose.
>
> **Publishing.** The gate has been framed as "publishing fails every repo
> simultaneously". Module adoption is per-repo — a repo installs this module
> explicitly and picks up a new contract when it updates — so the blast radius
> is repos that update, not all repos at once. That is not licence to publish
> carelessly, and one prerequisite is unchecked: whether
> `quoin module ensure-defaults` resolves to latest, which would turn adoption
> into a broadcast. Recommended sequence: this amendment → normalize the
> malformed matrices (Task-005, user-gated) → verify `ensure-defaults` → publish,
> treating the unauthored matrices as a backlog rather than a blocker.

> **CR-016 note:** The FR-003-CON-1 sweep validated this contract against the
> ecosystem's `TestMatrix` documents. The vocabulary failures were mostly the
> contract being narrower than reality — `Benchmark`, review/inspection,
> `Static`, decorated statuses, `Traces To` ranges, segmented test ids — rather
> than corpus drift. This amendment widens the four vocabularies accordingly and
> moves the status classes into the module's traceability declaration so the
> contract and the coverage rollup cannot disagree.
>
> It is deliberately **not** enough on its own: the remaining failures are
> structural — many matrices have no test-case table at all, and most of those
> with an id-column table under another heading are edge-case registers and
> coverage maps, not a renamed test-case summary. Those need authoring and
> renaming, not a looser contract: alternative section headings are **not**
> admitted, because accepting them would recover almost nothing while
> re-introducing the engine-facing alias lists that quire-rs CR-013/CR-014
> removed.

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md) (manifest
  activation carries the contract), quire-rs
  [FR-033](ix://agent-ix/quire-rs/spec/functional/FR-033) (CR-010
  `column_choices` / `column_patterns` table asserts),
  [US-001](../usecase/US-001-machine-validated-test-matrix.md)
- **External (not yet available)**: a quire-rs id-uniqueness table assert
  (follow-on to [FR-033](ix://agent-ix/quire-rs/spec/functional/FR-033);
  verified absent from `LocatorAssert`/`assert_eval`) —
  required to machine-enforce FR-003-AC-11; until it ships, AC-11 is normative
  guidance verified by review
- **Downstream**: the quoin `spec-matrix` flow that authors `tests.md`, and
  gap-analysis/planning tooling that consumes extracted test-case records
