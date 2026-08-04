---
id: Task-003
title: "FR-003-AC-9 — manifest-scope guard + repo self-validation"
type: Task
status: not_started
track: A
priority: P1
relationships:
  - target: ix://agent-ix/spec-artifacts-process/Task-002
    type: depends_on
  - target: ix://agent-ix/spec-artifacts-process/FR-003
    type: references
  - target: ix://agent-ix/spec-artifacts-process/TC-017
    type: verifies
---
# Task-003: FR-003-AC-9 — manifest-scope guard + repo self-validation

## Scope

Prove the contract landed without collateral change (FR-003-AC-9) and that this
repository itself conforms: TC-017 manifest-scope assertion, self-validation of
`spec/tests.md` under the new contract, and packaging check.

## Subtasks

- [ ] **Manifest-scope test (TC-017).** Assert the TestMatrix frontmatter schema
      and every other archetype/artifact_type entry are unchanged relative to the
      pre-contract manifest (targeted structural diff, complements Inspection).
- [ ] **Self-validation.** `quire validate --scope . "spec/**/*.md"` passes with
      the local module active — this repo's TM-001 is the first real conforming
      matrix.
- [ ] **Packaging.** `make build`; confirm the manifest ships in the wheel and
      `quoin write . --types TestMatrix` still resolves skeleton + schema.

## Deliverables

- TC-017 test green; full `make test` green
- Clean `quire validate` on this repo

## Notes

- Gate "contract green" closes when this task is done — Track C remains blocked
  on the Track S sign-off regardless.
