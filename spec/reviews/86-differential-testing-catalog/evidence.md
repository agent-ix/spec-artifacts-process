---
id: SR-020
title: "Evidence review of the differential-testing catalogue extension"
type: SpecReview
analysis: evidence
scope: "FR-007-AC-15..17, TC-144..TC-146 and Quoin advisor output"
review_set: all
evaluated_revision: "edf74a6"
review_date: "2026-09-10"
relationships:
  - { target: ix://agent-ix/spec-artifacts-process/FR-007, type: reviews }
---
# SR-020: Evidence review of the differential-testing catalogue extension

## Summary

The pre-implementation `quoin advise --json` run covered 139 obligations. It
correctly minted `reference-equivalence` for FR-007-AC-16 and recommended the
existing concolic method; the new method is absent because the manifest has not
yet been implemented. Four unrelated pre-existing mismatches and zero
inconclusive rows remain. The planned evidence separates source-data structure,
end-to-end selection and whole-corpus regression.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | medium | Resolved: `Property` is the evidence kind because the method evaluates a relation over cases and can consume generated cases; the requirement explicitly keeps input generation distinct from comparison. | FR-007 evidence-kind rationale; FR-007-AC-15 | wrong-requirement |
| FND-002 | high | Resolved: one positive advice assertion was insufficient because the same applicability edit could change unrelated obligations; TC-146 freezes all prior recommendation and state fields. | FR-007-AC-17; TC-146 | correct-requirement-no-evidence |
| FND-003 | medium | Retained expected gap: TC-144, TC-145 and TC-146 have no implementation evidence yet and remain marked planned/blocked rather than complete. | TM-001 | correct-requirement-no-evidence |
| FND-004 | low | Pre-existing adviser residue is outside this change: FR-003-AC-9, FR-009-AC-13, FR-013-AC-7 and NFR-001-AC-5 remain mismatches; no new criterion is inconclusive. | `/tmp/sap86-advise.json` | correct-requirement-no-evidence |

## Method assessment

| Criterion | Method | Rationale |
| --- | --- | --- |
| FR-007-AC-15 | Test / Unit evidence | Exhaustive inspection of one finite manifest entry and discriminating field mutations. |
| FR-007-AC-16 | Test / Integration evidence | Crosses the module-data, Quoin and typed producer boundaries. |
| FR-007-AC-17 | Test / Integration evidence | Differential comparison of full structured advice results before and after one catalogue change. |
