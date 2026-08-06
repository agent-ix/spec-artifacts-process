---
id: Task-004
title: "FR-003-CON-1 — ecosystem tests.md sweep with per-repo normalization diffs"
type: Task
status: completed
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

- [x] **Enumerate.** Discover ecosystem repos carrying `spec/tests.md` with
      `type: TestMatrix` (the ~214 normalized master-spec repos are the base
      population).
- [x] **Validate.** Run each through the Task-001 harness with the candidate
      manifest; record pass/fail and per-cell/per-table failure reasons.
- [x] **Diff.** For each failing repo, generate the normalization diff that
      brings its `tests.md` to the required shape (columns, bare status markers,
      Test ID shapes, Traces To tokens) without inventing coverage content —
      structural normalization only; genuine coverage gaps are reported, not
      papered over.
- [x] **Report.** Sweep summary (repo list, failure taxonomy, diff artifacts)
      packaged for user review at Task-005.

## Deliverables

- Sweep report + per-repo diff artifacts (report/diffs live outside the swept
  repos until sign-off)

## Notes

- Runs in parallel with Task-003 once Task-002 lands.
- Fabricating rows to satisfy `min_rows` is forbidden — see
  feedback: matrices must reflect actual coverage; surface gaps instead.
- Unblocks: Task-005 (sign-off gate).

## Sweep record (2026-08-04) — read-only, no repository modified

Artifacts: `reports/2026-08-04-tests-md-sweep.md` (report) and
`reports/2026-08-04-tests-md-sweep.json` (per-repo diagnostics). They live
outside `plan/**` because a sweep report is gate evidence, not a typed spec
artifact.

**Result: 189 `spec/tests.md` files; 12 are not `type: TestMatrix`; of the 177
that are, 6 pass and 171 fail the candidate contract.** Publishing today would
break 96% of the ecosystem's matrices — exactly what FR-003-CON-1 exists to
prevent.

The shape of the failures matters more than the count. Repo-level causes:
missing `Test Case Summary` (116 repos), missing `Functional Requirement
Coverage` (112), wrong column sets (48), then the vocabulary failures.

**The sweep surfaces contract questions, not just corpus drift** — the detail
is in the report, but in short: the corpus uses `Type` values the contract does
not admit (`Static`, `Benchmark`, `pg_test`, `Storybook`, `Fixture`, compound
forms), word-and-marker `Status` values beyond the four markers, and `Traces To`
ranges (`FR-001..FR-006`). quire-rs's own matrix — the reference corpus — uses
`Static` and `Property`. Recommendation carried into the gate: settle the
vocabulary questions as FR-003 amendments **before** normalizing 171 repos,
or the corpus gets rewritten twice.

Mechanically normalizable today (deterministic, safe to script once signed
off): decorated statuses → bare markers (81 cells) and id cells carrying
trailing prose → bare id with the prose moved to `Title` (16 cells).

**No diffs were applied and nothing was published.** Task-005's sign-off gate
is next and remains untouched.
