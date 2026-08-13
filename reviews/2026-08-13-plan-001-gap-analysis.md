---
id: SR-005
title: "Gap analysis — Plan-001 testmatrix-body-extraction"
type: SpecReview
analysis: gap-analysis
scope: "plan/Plan-001-testmatrix-body-extraction/, spec/tests.md"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-artifacts-process/Plan-001", type: reviews }
  - { target: "ix://agent-ix/spec-artifacts-process/TM-001", type: references }
---

# SR-005: Gap analysis — Plan-001 testmatrix-body-extraction

## Summary

First run of this skill against `quire coverage` rather than a grep index. Two
of six plan tasks are `not_started` and one matrix row claims `✅` with no test
behind it. The reconciliation itself found a defect in the engine on its first
outing — a test that exists and passes was reported unbacked because a formatter
had wrapped its signature.

## Verdict

**FAIL** — two incomplete tasks and one unbacked matrix Test Case marked `✅`.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | TC-026 is marked `✅` and no test carries it — the matrix overclaims coverage | TC-026, FR-003-AC-4 |
| FND-002 | high | Task-005 and Task-006 are `not_started`, so the plan is not done | Task-005, Task-006 |
| FND-003 | medium | A test that exists and passes read as unbacked because black wrapped its signature; engine defect, fixed as quire-rs CR-037 | TC-029, FR-004-AC-2 |
| FND-004 | low | `plan.md` checkboxes are all unchecked while four of six tasks are `completed` — stale | plan/Plan-001-testmatrix-body-extraction/plan.md:19 |
| FND-005 | low | No test tags an acceptance-criterion id directly, so AC-level backing is 0/27; the repo's convention is TC ids in docstrings | spec/tests.md |

## Detail

**FND-001.** `TC-026 | An IT- id validates; a prefix naming no declared archetype
(BENCH-001) fails (CR-019)` is marked `✅` in the Test Case Summary and cited by
FR-003-AC-4's coverage row. No test in `tests/` references `BENCH-001` or an
`IT-` id assertion. `quire coverage` reports it as the repo's one remaining
status lie. This is the finding the rollup exists to produce, and it is the
first one it has ever produced here.

**FND-002.** Task-005 (`normalize-before-enforce-signoff`) and Task-006
(`publish-enforcing-version`) are `not_started`. These are the FR-003-CON-1 gate
— an ecosystem `tests.md` sweep plus explicit user sign-off before the enforcing
module version publishes. The gate is deliberate and pre-existing, not drift;
the plan is nonetheless incomplete, and the verdict rule says so.

**FND-003.** Not a spec or test gap — an engine defect this run surfaced.
`block_end` in the Python adapter ended a suite at the first line indented no
deeper than the declaration, and a black-wrapped `def` closes with `) -> None:`
at the declaration's own column. The span stopped one line before the docstring
carrying the tag. Isolated to two tests identical but for the wrapping. Fixed in
quire-rs (CR-037, FR-051-AC-13, TC-800); this repo went 26/60 backed with two
status lies to 27/60 with one.

**FND-005.** Not a defect. The repo tags tests with `TC` ids in docstrings, and
the matrix carries the AC→TC mapping, so criteria are reachable through the
matrix rather than directly from source. Recorded because the `acceptance-criterion`
group reads `0/27` and that number invites a wrong conclusion on its own.

## Coverage

- Reconciliation: quire coverage (module spec-artifacts-process, working tree)
- Tasks done: 4 / 6
- Rows backed by a tagged test: 27 / 60 — test-case 27/33, acceptance-criterion 0/27
- Status lies: 1 (TC-026)
- Untracked symbols: 0
- Untraced behaviors / stubs: none — the package is 21 lines of resource paths with no logic to under-specify
- Semantic review: skipped
