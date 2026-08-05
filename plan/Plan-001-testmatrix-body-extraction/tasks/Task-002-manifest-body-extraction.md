---
id: Task-002
title: "FR-003 — TestMatrix body_extraction contract in manifest.yaml (TDD green)"
type: Task
status: completed
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-artifacts-process/Task-001
    type: depends_on
  - target: ix://agent-ix/spec-artifacts-process/FR-003
    type: references
  - target: ix://agent-ix/spec-artifacts-process/TC-001
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-002
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-003
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-004
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-005
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-006
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-007
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-008
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-009
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-010
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-011
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-012
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-013
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-014
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-015
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-016
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-018
    type: verifies
---
# Task-002: FR-003 — TestMatrix body_extraction contract in manifest.yaml (TDD green)

## Scope

Add the `body_extraction` block to the `TestMatrix` artifact_type entry in
`spec_artifacts_process/manifest.yaml`, exactly per FR-003 Behavior, turning the
Task-001 suite green. Manifest **data only** — no engine work, no schema edits.

## Subtasks

- [x] **Required extractions.** `Functional Requirement Coverage` and
      `Test Case Summary` as `table_row` extractions with exact column sets,
      `min_rows: 1`, `multiple: true`, `id_column: Test ID`,
      `id_pattern: '^TC(-INT)?-\d+[a-z]?$'`.
- [x] **Vocabulary asserts.** `column_choices` — Type: Unit/Integration/E2E/
      Property; Priority: P0..P4; Status: ✅/⚠️/❌/🚧. `column_patterns` —
      Traces To cell pattern per FR-003 (comma-separated StR/US/FR/NFR
      [-AC-/-CON-] and IT[-SC-] tokens).
- [x] **Optional extractions.** StR / US / NFR coverage tables with
      `required: false` and column asserts applied only when present; no
      extraction entries for the scaffolding sections (Option Permutation,
      Constraint Boundary, Edge Cases, Coverage Gaps, Integration/Execution).
- [x] **Green run.** Full Task-001 suite passes; `quire validate` on the
      fixture corpus behaves per each TC's expectation.

## Deliverables

- Updated `spec_artifacts_process/manifest.yaml` (TestMatrix entry only)
- Green TC-001..TC-016, TC-018

## Notes

- Mirror the `SpecReview` `body_extraction` precedent in the same manifest.
- Engine capabilities (`column_choices`, `column_patterns`) exist since quire-rs
  FR-033/CR-010 — consume, don't modify.
- Unblocks: Task-003 (AC-9 guard), Task-004 (sweep against the candidate contract).

## Implementation record (2026-08-04)

- Added the `body_extraction` block to the `TestMatrix` artifact_type in
  `spec_artifacts_process/manifest.yaml`, mirroring the SpecReview precedent:
  required `Functional Requirement Coverage` and `Test Case Summary`
  extractions (`multiple: true`, `min_rows: 1`), `Test ID` as `id_column` with
  `^TC(-INT)?-\d+[a-z]?$`, `column_choices` on Type/Priority/Status, the
  `column_patterns` trace-token regex on `Traces To`, and the three optional
  coverage tables with `required: false` and columns asserted when present.
- The whole Task-001 suite went green in one step: 27 passed, TC-024 xfailed.
- No other manifest entry touched (asserted by TC-017).
