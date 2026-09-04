---
id: Task-016
title: "Matrix status flip, coverage reconciliation, and the recorded inspections"
type: Task
status: todo
track: C
priority: P1
relationships:
  - target: ix://agent-ix/spec-artifacts-process/FR-009
    type: references
  - target: ix://agent-ix/spec-artifacts-process/FR-013
    type: references
  - target: ix://agent-ix/spec-artifacts-process/TC-143
    type: verifies
---
# Task-016: Matrix status flip, coverage reconciliation, and the recorded inspections

## Scope

Closing the loop between what the matrix claims and what the suite proves.

## Subtasks

- [ ] Flip TC-080..TC-143 from `🚧` to `✅` **only** where the backing test exists and runs green. A marker moved by hand ahead of its test is the status lie this module's own coverage rollup exists to catch.
- [ ] Leave TC-135 at `🚧` with its note: a strict expected failure against quire-rs#221/#394, red by design, never skipped.
- [ ] Run `quire coverage --scope .` and reconcile its headline against the `spec/tests.md` figure, stating what each number counts — they count different populations and the difference must be explained, not averaged.
- [ ] Grep for non-binding trace tags before the PR: a `black`-wrapped `@pytest.mark.trace` binds nothing (quire-rs#395), a tag on a module docstring or a plain helper binds nothing, and a bare TC id in a comment binds to the **next** symbol. The target is zero.
- [ ] Record FR-013-AC-8 and FR-009-AC-13 as inspections with a named reviewer and the commit inspected.
- [ ] `spec/log.md` entry for the 0.2.0 contract.

## Deliverables

`spec/tests.md` with honest markers, `spec/log.md` entry, the recorded inspections.
