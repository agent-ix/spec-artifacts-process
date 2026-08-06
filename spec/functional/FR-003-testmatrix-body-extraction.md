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
(`tests.md`) against the coverage tables and Test Case Summary that the quoin
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

- `body_extraction` **SHALL** require a `Functional Requirement Coverage`
  `table_row` extraction with columns exactly
  `Functional Req | Acceptance Criteria | Test Cases | Coverage Status` and at
  least one row.
- `body_extraction` **SHALL** require a `Test Case Summary` `table_row`
  extraction with columns exactly
  `Test ID | Title | Type | Priority | Traces To | Status` and at least one row.
- The `Test ID` column **SHALL** be the id column and match
  `^TC(-[A-Za-z0-9]+)+$` with at least one numeric segment. This admits the
  plain `TC-NNN` form, the template's `TC-INT-NNN`/lettered variants, and the
  segmented forms the ecosystem authors (`TC-060-01`, `TC-SB-001`,
  `TC-001-HEADER-PARSE` — 7 repo families), while still rejecting `TC1`,
  `tc-001`, `TC-`, `TCX-001`, and ids carrying trailing prose (CR-016).
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
- The `Priority` column **SHALL** be constrained via `column_choices` to
  exactly `P0 | P1 | P2 | P3 | P4`, where P0 = must-pass blocker,
  P1 = critical path, P2 = standard, P3 = low, and P4 = nice-to-have/deferred.
- The `Status` column **SHALL** be constrained via `column_patterns` to a
  leading status marker followed by an optional note:
  `^(✅|⚠️|❌|🚧|⛔)(\s+.*)?$`. The marker carries the class and the note carries
  why — `⚠️ scale evidence deferred` says something the bare marker cannot, and
  6 repo families already author decorated statuses. `⛔` marks a retired row.
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
- Test-case rows **SHALL** be extractable as records (`multiple: true`) so
  tooling (gap analysis, planning) can select each test case by id.
- `Test ID` values **SHALL** be unique within the `Test Case Summary` (a
  duplicate id makes record selection by id ambiguous). NOTE: the quire-rs
  extraction assert vocabulary (`LocatorAssert`: `columns`, `min_rows`,
  `id_column`/`id_pattern`, `choices`, `column_choices`, `column_patterns`)
  currently provides **no uniqueness assert**, so this criterion is normative
  but not yet machine-enforceable — enforcement depends on a new quire-rs
  engine capability (see Dependencies).
- The `Stakeholder Requirement Coverage`
  (`Stakeholder Req | Trace to US/FR | Test/Validation | Coverage Status`),
  `User Story Coverage`
  (`User Story | Acceptance Criteria | Test Cases | Coverage Status`), and
  `Non-Functional Requirement Coverage`
  (`Non-Functional Req | Verification Method | Evidence/Test Cases | Status`)
  tables **SHALL** be declared as optional (`required: false`) extractions
  whose column sets are asserted when the section is present: the spec-matrix
  template emits them unconditionally, but a bundle without StR/US/NFR
  artifacts cannot truthfully populate them, and requiring rows would force
  fabricated entries.
- Sections the spec-matrix template marks conditional or scaffolding
  (`Integration Test Matrix`, `Option Permutation Matrix`,
  `Constraint Boundary Tests`, `Edge Cases`, `Coverage Gaps`,
  `Test Execution Summary`) **SHALL NOT** be required by the contract.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-003-CON-1 | The module version enforcing this `body_extraction` SHALL NOT be published until existing ecosystem `tests.md` files are normalized to the required shape; a sweep producing per-repo diffs for user sign-off precedes enforcement | Process | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-003-AC-1 | A `TestMatrix` doc with a conforming `Functional Requirement Coverage` table and `Test Case Summary` validates | Test (TC-001) |
| FR-003-AC-2 | A doc missing the `Test Case Summary` table fails with reason `missing` | Test (TC-001) |
| FR-003-AC-3 | A `Type` cell outside the core evidence vocabulary and the module's declared extensions fails via `column_choices` (reason `assert`); every core value and every declared extension passes | Test (TC-001) |
| FR-003-AC-4 | A `Test ID` cell not matching `^TC(-[A-Za-z0-9]+)+$` with a numeric segment fails validation; the segmented ecosystem forms (`TC-060-01`, `TC-SB-001`, `TC-001-HEADER-PARSE`) pass | Test (TC-001) |
| FR-003-AC-5 | A `Status` cell not headed by one of `✅ ⚠️ ❌ 🚧 ⛔` fails via `column_patterns`; a marker followed by a note (`✅ Complete`, `⚠️ scale evidence deferred`) passes | Test (TC-001) |
| FR-003-AC-6 | A `Traces To` cell that is not comma-separated `<KIND>-<N>` tokens (with an optional `-<SUBKIND>-<M>` sub-id, a same-prefix range, or a trailing parenthetical note) fails via `column_patterns`; the contract enumerates no kind names | Test (TC-001) |
| FR-003-AC-7 | A doc omitting the StR/US/NFR coverage tables still validates (optional extractions) | Test (TC-001) |
| FR-003-AC-8 | Test-case rows are extracted as one record per row (`multiple: true`) | Test (TC-001) |
| FR-003-AC-9 | The contract is added without altering the TestMatrix frontmatter schema or the other archetypes | Inspection |
| FR-003-AC-10 | A `Priority` cell outside `P0\|P1\|P2\|P3\|P4` fails via `column_choices` | Test (TC-001) |
| FR-003-AC-11 | A `Test Case Summary` containing two rows with the same `Test ID` fails validation | Test (TC-024) — blocked on a quire-rs uniqueness assert (none exists today) |

> **CR-016 note:** The FR-003-CON-1 sweep
> (`reports/2026-08-04-tests-md-sweep.md`) validated this contract against all
> 177 ecosystem `TestMatrix` documents: **6 passed**. The vocabulary failures
> were mostly the contract being narrower than reality — `Benchmark` (8 repo
> families), review/inspection (5), `Static` (3), decorated statuses (6),
> `Traces To` ranges (4), segmented test ids (7) — rather than corpus drift.
> This amendment widens the four vocabularies accordingly and moves the status
> classes into the module's traceability declaration so the contract and the
> coverage rollup cannot disagree.
>
> It is deliberately **not** enough on its own: simulating the amendment puts
> the ecosystem at 18/177. The remaining 154 failures are structural — 70
> matrices have no test-case table at all, and of the 44 with an id-column table
> under another heading, inspection showed only ~4 are a renamed test-case
> summary (the rest are edge-case registers and coverage maps). Those need
> authoring and renaming, not a looser contract: alternative section headings
> are **not** admitted, because accepting them would recover ~4 repos while
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
  verified absent from `LocatorAssert`/`assert_eval` as of 2026-08-04) —
  required to machine-enforce FR-003-AC-11; until it ships, AC-11 is normative
  guidance verified by review
- **Downstream**: the quoin `spec-matrix` flow that authors `tests.md`, and
  gap-analysis/planning tooling that consumes extracted test-case records
