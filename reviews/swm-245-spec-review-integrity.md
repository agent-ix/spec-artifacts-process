---
id: SR-20261115175477
title: "SWM-245 PR164 spec-review integrity"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-artifacts-process PR164; spec/functional/FR-020-rolespec-archetype.md, spec/functional/FR-021-rolespec-trace-and-cross-row-checks.md, spec/functional/FR-022-rolespec-lint-ownership.md, spec/usecase/US-004-author-role-specs-that-validate.md"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-020", type: references}
  - {target: "ix://agent-ix/spec-artifacts-process/FR-021", type: references}
  - {target: "ix://agent-ix/spec-artifacts-process/FR-022", type: references}
---

## Summary

Ticket: SWM-245. Integrity check of the new FR-020 to FR-022 and US-004. It covered:

- Completeness: whether every Behavior statement maps to an AC.
- Consistency between each FR's stated scope and its statements.
- Atomicity and testability of the ACs.

Every FR-020 Behavior statement has at least one AC (AC-1 to AC-10). Every FR-021 check maps to AC-2 to AC-7 or AC-10. The three US-004 examples map to FR-021-AC-2, AC-3, AC-4 and AC-5. The index entries match the titles.

## Verdict

**CONDITIONAL.** Coverage is complete. One statement sits in the wrong FR and hides an engine dependency. One trace-target posture is unstated. One AC names no command to run.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-020 limits itself to "checks that read one row or one field" and puts cross-row checks in FR-021. Its warning for "a rule whose evaluations are all `judgement`" is a cross-row check: it groups evaluations by rule, which needs the rule-parenting capability (FR-021 capability 1, SWM-247). FR-021 does not list it as a check or as an engine gap, so FR-020-AC-4 looks implementable now when it is not. | spec/functional/FR-020-rolespec-archetype.md:19,47,58 |
| FND-002 | medium | The evidence posture of the `role-metric` trace target is not stated. Rule and objective targets are `reference-only` and `role-evaluation` is evidence-bearing. Under the manifest's default (`source`), every metric id would join the criterion denominator and show as untested in `quire matrix`, although nothing binds metrics. | spec/functional/FR-021-rolespec-trace-and-cross-row-checks.md:27 |
| FND-003 | medium | FR-021-AC-2 says "exits nonzero from the matrix-based lint" but does not name the command. This module ships no lint. The dev-team FR-007 lint is computed by `quire matrix` and `quoin gap-analysis`. A test author cannot tell which invocation must exit nonzero or which repository the test belongs to. | spec/functional/FR-021-rolespec-trace-and-cross-row-checks.md:55 |
| FND-004 | low | FR-022-AC-1 verifies a file in dev-team (`spec/roles/minder.md`), so no test in this repository can discharge it as `Test`. FR-022-AC-4 already covers the module-local copy. AC-1 is a cross-repository acceptance gate and should say so, for example as Demonstration in dev-team. | spec/functional/FR-022-rolespec-lint-ownership.md:32 |
