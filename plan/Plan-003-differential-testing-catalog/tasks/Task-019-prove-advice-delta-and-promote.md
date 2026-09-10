---
id: Task-019
title: "FR-007-AC-17 — prove advice-delta containment and promote"
type: Task
status: blocked
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-artifacts-process/Task-018
    type: depends_on
  - target: ix://agent-ix/spec-artifacts-process/FR-007
    type: references
  - target: ix://agent-ix/spec-artifacts-process/TC-146
    type: verifies
---
# Task-019: FR-007-AC-17 — prove advice-delta containment and promote

## Scope

Compare Quoin's full structured advice for one frozen obligation corpus before and after the catalogue addition, then run the complete assurance and promotion gates for issue #86.

## Subtasks

- [ ] Freeze one closed corpus and exact pre-change/post-change module identities while reusing Task-018's accepted Engineering Assurance producer configuration.
- [ ] Prove only obligations whose pre-change facts already contain `reference-equivalence` gain `differential-testing`.
- [ ] Prove every prior recommendation, reason, relative order, mismatch state, uncatalogued state and inconclusive state remains identical.
- [ ] Carry bare `ix-trace-rs` bindings for TC-146, FR-007-AC-17 and FR-007-CON-1.
- [ ] Mark TC-145/146 complete only after their real local runs pass; recount the matrix mechanically.
- [ ] Run the exact Rust review, QUOIN semantic gap analysis, Quire validation and bounded local gates over the complete branch; remediate every blocker before opening the PR.

## Deliverables

- Rust TC-146 frozen-corpus differential test and retained structured results.
- Complete Rust review and gap-analysis artifacts for the merge candidate.
- One complete reviewable PR closing issue #86 and unblocking the quire-verification consumer.

## Notes

- This task remains blocked until Task-018 proves the shared execution and strict-reader boundary. It cannot replace the external producer with a local helper to make progress appear complete.
