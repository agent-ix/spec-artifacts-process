---
id: SR-025
title: "Gap analysis — Plan-003 differential testing catalogue method"
type: SpecReview
analysis: gap-analysis
scope: "plan/Plan-003-differential-testing-catalog/, spec/functional/FR-007-verification-method-catalog.md, spec/tests.md, spec_artifacts_process/manifest.yaml, rust-tests/"
review_set: subset
relationships:
  - target: ix://agent-ix/spec-artifacts-process/Plan-003
    type: reviews
  - target: ix://agent-ix/spec-artifacts-process/TM-001
    type: references
---
# SR-025: Gap analysis — Plan-003 differential testing catalogue method

## Summary

QUOIN `/gap-analysis` audited Plan-003 at `d8d3724`, the FR-007 acceptance
subset, TM-001, the authoritative catalogue data and the Rust acceptance target.
The implemented TC-144 checkpoint is traced, executable and semantically faithful;
the plan is incomplete because its two cross-tool cases still lack the accepted
Engineering Assurance producer and therefore have neither implementation nor
backing trace symbols.

## Verdict

**FAIL** — Task-018 and Task-019 are blocked P0 work, and TC-145 and TC-146 are
unbacked. This is the expected honest result for the current checkpoint and
prevents issue #86, Plan-003 or its future PR from being called complete.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | Task-018 is blocked pending the accepted typed Rust process-execution result from `agent-ix/engineering-assurance#34`; without it the plan cannot prove exact Quoin catalogue/advice execution, non-completion or malformed-output refusal. | Task-018, FR-007-AC-16, TC-145 |
| FND-002 | high | Task-019 is blocked on Task-018 and therefore cannot execute the frozen-corpus advice delta or the complete promotion gate. | Task-019, FR-007-AC-17, TC-146 |
| FND-003 | high | TM-001 and FR-007 both reference TC-145, but `quire coverage` finds no backing test symbol. The authored blocked marker is honest; the acceptance criterion remains unproved. | TC-145, FR-007-AC-16, spec/tests.md:88 |
| FND-004 | high | TM-001 and FR-007 both reference TC-146, but `quire coverage` finds no backing test symbol. The authored blocked marker is honest; the acceptance criterion remains unproved. | TC-146, FR-007-AC-17, spec/tests.md:89 |

## Coverage

- Target bundle: `plan/Plan-003-differential-testing-catalog/`; spec root
  `spec/`; matrix `spec/tests.md` (`TM-001`); identity prefix
  `ix://agent-ix/spec-artifacts-process`; source data
  `spec_artifacts_process/manifest.yaml`; tests `rust-tests/`.
- Plan completion: **1 / 3 tasks done**. Task-017 is done; Tasks 018 and 019
  remain blocked. Task states, plan checkboxes and the task mapping agree.
- Reconciliation: `quire coverage --scope . --json`, Quire CLI 0.31.0 / engine
  0.46.0. The full repository report is **135 / 279 rows backed**; within the
  three Plan-003 test cases, **1 / 3** is backed. TC-144 is backed; TC-145 and
  TC-146 produce the four exact unbacked reference records summarized above.
- Target status integrity: TC-144 is marked complete and backed; TC-145/146 are
  marked blocked and unbacked. No Plan-003 trace is untracked and no Plan-003
  complete row is a status lie.
- Report limit: the repository-wide run emits 13 diagnostics. The functional
  coverage table's `Coverage Status` header does not match the module's configured
  `Status` column, so that table's status classification is skipped; this
  pre-existing defect is already tracked by `agent-ix/spec-artifacts-process#81`.
  Direct reference reconciliation still exposes both Plan-003 unbacked cases;
  the diagnostic is not treated as evidence that either passed.
- Reverse gap: one declarative catalogue behavior, three private test helpers,
  three traced test functions and their Cargo/toolchain configuration were
  inventoried. **0 untraced behaviors, 0 source stubs, 0 test stubs.**
- Semantic review: ran over FR-007-AC-15 and FR-007-CON-1 at the implemented
  checkpoint. The test validates the exact method and claim ceiling, reads the
  real committed manifest, and discriminates missing, unknown, changed and
  unrelated-extension cases. The data matches the requirement. No semantic
  finding remains. AC-16 and AC-17 were confirmed absent rather than judged from
  planned prose.
- Hosted execution: neither workflow changed and both retain
  `workflow_dispatch` as their only trigger. No hosted workflow was dispatched.
