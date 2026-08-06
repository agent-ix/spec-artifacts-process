---
id: Task-005
title: "FR-003-CON-1 — user sign-off gate (normalize-before-enforce)"
type: Task
status: not_started
track: Gate
priority: P0
relationships:
  - target: ix://agent-ix/spec-artifacts-process/Task-004
    type: depends_on
  - target: ix://agent-ix/spec-artifacts-process/FR-003
    type: references
  - target: ix://agent-ix/spec-artifacts-process/FR-003-CON-1
    type: verifies
---
# Task-005: FR-003-CON-1 — user sign-off gate (normalize-before-enforce)

## Scope

Hard gate satisfying FR-003-CON-1: the user reviews the Task-004 sweep report
and per-repo diffs and explicitly approves (a) applying the normalizations and
(b) publishing the enforcing module version. Nothing in Track C may start before
this gate closes.

## Subtasks

- [ ] **Present.** Deliver the sweep report + diffs for review.
- [ ] **Decide.** Record the user's decision per repo (approve / amend / defer)
      and any contract-strictness feedback.
- [ ] **Iterate if rejected.** Feed amendments back: contract changes re-enter
      via spec review (FR-003 edit), diff changes re-run Task-004.
- [ ] **Record.** Persist the sign-off (date, scope of approval) in the plan log
      as the Inspection evidence for FR-003-CON-1.

## Deliverables

- Recorded user sign-off (or documented rejection + follow-up loop)

## Notes

- This is a human decision point — the agent must not infer approval.
- Unblocks: Task-006 (enforcing publish).
