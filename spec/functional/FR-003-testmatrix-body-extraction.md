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
  `^TC(-INT)?-\d+[a-z]?$` (plain `TC-NNN` rows plus the template's
  `TC-INT-NNN`/lettered variants).
- The `Type` column **SHALL** be constrained via the Quire `column_choices`
  assert to exactly `Unit | Integration | E2E | Property` (requires
  [FR-033](ix://agent-ix/quire-rs/spec/functional/FR-033)).
- The `Priority` column **SHALL** be constrained via `column_choices` to
  exactly `P0 | P1 | P2 | P3 | P4`, where P0 = must-pass blocker,
  P1 = critical path, P2 = standard, P3 = low, and P4 = nice-to-have/deferred.
- The `Status` column **SHALL** be constrained via `column_choices` to the
  status-marker vocabulary `✅ | ⚠️ | ❌ | 🚧`.
- Each `Traces To` cell **SHALL** be constrained via the Quire
  `column_patterns` assert to one or more comma-separated trace tokens, each
  matching `(StR|US|FR|NFR)-\d+(-(AC|CON)-\d+)?` or `IT-\d+(-SC-\d+)?`
  (constraint-boundary tests trace to CON rows; integration test cases trace
  to IT ids and their success criteria), i.e. the cell pattern
  `^((StR|US|FR|NFR)-\d+(-(AC|CON)-\d+)?|IT-\d+(-SC-\d+)?)(,\s*((StR|US|FR|NFR)-\d+(-(AC|CON)-\d+)?|IT-\d+(-SC-\d+)?))*$`;
  existence of the referenced ids is **not** checked by this contract.
- Test-case rows **SHALL** be extractable as records (`multiple: true`) so
  tooling (gap analysis, planning) can select each test case by id.
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
| FR-003-AC-3 | A `Type` cell outside `Unit\|Integration\|E2E\|Property` fails via `column_choices` (reason `assert`) | Test (TC-001) |
| FR-003-AC-4 | A `Test ID` cell not matching `^TC(-INT)?-\d+[a-z]?$` fails validation | Test (TC-001) |
| FR-003-AC-5 | A `Status` cell outside `✅\|⚠️\|❌\|🚧` fails via `column_choices` | Test (TC-001) |
| FR-003-AC-6 | A `Traces To` cell that is not comma-separated tokens of `(StR\|US\|FR\|NFR)-\d+(-(AC\|CON)-\d+)?` or `IT-\d+(-SC-\d+)?` fails via `column_patterns` | Test (TC-001) |
| FR-003-AC-7 | A doc omitting the StR/US/NFR coverage tables still validates (optional extractions) | Test (TC-001) |
| FR-003-AC-8 | Test-case rows are extracted as one record per row (`multiple: true`) | Test (TC-001) |
| FR-003-AC-9 | The contract is added without altering the TestMatrix frontmatter schema or the other archetypes | Inspection |
| FR-003-AC-10 | A `Priority` cell outside `P0\|P1\|P2\|P3\|P4` fails via `column_choices` | Test (TC-001) |

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md) (manifest
  activation carries the contract), quire-rs
  [FR-033](ix://agent-ix/quire-rs/spec/functional/FR-033) (CR-010
  `column_choices` / `column_patterns` table asserts),
  [US-001](../usecase/US-001-machine-validated-test-matrix.md)
- **Downstream**: the quoin `spec-matrix` flow that authors `tests.md`, and
  gap-analysis/planning tooling that consumes extracted test-case records
