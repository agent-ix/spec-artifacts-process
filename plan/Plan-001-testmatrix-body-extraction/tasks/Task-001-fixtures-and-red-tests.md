---
id: Task-001
title: "FR-003 — fixture corpus + failing validation tests (TDD red)"
type: Task
status: not_started
track: A
priority: P0
relationships:
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
# Task-001: FR-003 — fixture corpus + failing validation tests (TDD red)

## Scope

Build the `TestMatrix` fixture corpus and the pytest harness that drives
`quire validate` with this module's manifest, encoding TC-001..TC-016 and TC-018
as tests. They MUST be red (contract absent) before Task-002 lands the manifest
change, with each failure asserting the documented reason.

## Subtasks

- [ ] **Conforming fixture.** Full spec-matrix-shaped `tests.md` fixture (all
      coverage tables + Test Case Summary) exercising a mixed vocabulary
      combination (TC-001) and record extraction (`multiple: true`, FR-003-AC-8).
- [ ] **Structural-drift fixtures.** Missing Test Case Summary (TC-002), missing
      Functional Requirement Coverage (TC-003), header-only tables for the
      `min_rows` boundary (TC-016), omitted optional tables (TC-014), optional
      table with a renamed column (TC-015).
- [ ] **Vocabulary fixtures.** Pass-side permutations for Type (TC-004),
      Priority (TC-010), Status (TC-008); fail-side cells `Manual`, `P5`,
      `Done`/decorated `✅ Complete` (TC-005, TC-011, TC-009).
- [ ] **Id/token fixtures.** Test ID shapes `TC-001`/`TC-INT-010`/`TC-INT-010a`
      pass, `TC1`/`tc-001`/`TC-`/`TCX-001` fail (TC-006, TC-007); Traces To token
      permutations per kind + comma lists pass, semicolons/space-before-comma/TC
      tokens/truncated ids/trailing comma/empty cell fail (TC-012, TC-013, TC-018).
- [ ] **Harness.** Pytest wrapper invoking `quire validate` with the local module
      (manifest + schemas) against a fixture doc, asserting pass/fail and the
      failure reason (`missing` vs `assert`); reusable by the Track S sweep.

## Deliverables

- `tests/fixtures/testmatrix/*.md` fixture corpus
- `tests/test_testmatrix_body_extraction.py` (red)

## Notes

- Mirror the existing SpecReview `body_extraction` test approach if present.
- Unblocks: Task-002 (green step), Task-004 (sweep reuses the harness).
