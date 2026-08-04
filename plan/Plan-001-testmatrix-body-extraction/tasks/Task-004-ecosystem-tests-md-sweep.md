---
id: Task-004
title: "FR-003-CON-1 — ecosystem tests.md sweep with per-repo normalization diffs"
type: Task
status: not_started
track: S
priority: P1
relationships:
  - target: ix://agent-ix/spec-artifacts-process/Task-002
    type: depends_on
  - target: ix://agent-ix/spec-artifacts-process/FR-003
    type: references
  - target: ix://agent-ix/spec-artifacts-process/FR-003-CON-1
    type: verifies
---
# Task-004: FR-003-CON-1 — ecosystem tests.md sweep with per-repo normalization diffs

## Scope

Read-only sweep of ecosystem repositories' `type: TestMatrix` documents
(`spec/tests.md`) against the candidate `body_extraction` contract, producing a
pass/fail report and per-repo normalization diffs for user review. This is the
evidence input to the FR-003-CON-1 sign-off gate — **no repository is edited by
this task**.

## Subtasks

- [ ] **Enumerate.** Discover ecosystem repos carrying `spec/tests.md` with
      `type: TestMatrix` (the ~214 normalized master-spec repos are the base
      population).
- [ ] **Validate.** Run each through the Task-001 harness with the candidate
      manifest; record pass/fail and per-cell/per-table failure reasons.
- [ ] **Diff.** For each failing repo, generate the normalization diff that
      brings its `tests.md` to the required shape (columns, bare status markers,
      Test ID shapes, Traces To tokens) without inventing coverage content —
      structural normalization only; genuine coverage gaps are reported, not
      papered over.
- [ ] **Report.** Sweep summary (repo list, failure taxonomy, diff artifacts)
      packaged for user review at Task-005.

## Deliverables

- Sweep report + per-repo diff artifacts (report/diffs live outside the swept
  repos until sign-off)

## Notes

- Runs in parallel with Task-003 once Task-002 lands.
- Fabricating rows to satisfy `min_rows` is forbidden — see
  feedback: matrices must reflect actual coverage; surface gaps instead.
- Unblocks: Task-005 (sign-off gate).
