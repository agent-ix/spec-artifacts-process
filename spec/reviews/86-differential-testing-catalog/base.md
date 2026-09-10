---
id: SR-016
title: "Base review of the differential-testing catalogue extension"
type: SpecReview
analysis: base
scope: "FR-007, TM-001 rows TC-144..TC-146 and spec-artifacts-process#86"
review_set: all
evaluated_revision: "edf74a6"
review_date: "2026-09-10"
relationships:
  - { target: ix://agent-ix/spec-artifacts-process/FR-007, type: reviews }
---
# SR-016: Base review of the differential-testing catalogue extension

## Summary

The specification adds one shared catalogue method and three planned Rust
checks without changing catalogue ownership, oracle independence, producer
execution or evidence sufficiency. The first review found an uncatalogued
verification value and two missing adverse cases; the revisions through
`e5035b1` resolve them.

## Verdict

**PASS for specification readiness.** Implementation of TC-145 and TC-146
remains correctly blocked on the accepted Engineering Assurance Rust producer
boundary in agent-ix/engineering-assurance#34. The specification does not claim
that dependency exists or that any planned row is complete.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | medium | Resolved: FR-007-AC-16 originally named `Integration` as its verification method, which `quoin advise` classified as uncatalogued; it now uses IADT `Test`, while TM-001 keeps `Integration` as the evidence kind. | FR-007-AC-16; TC-145 | wrong-requirement |
| FND-002 | high | Resolved: cross-tool success now requires an exact pinned Quoin executable, a closed module set, a completed producer state and schema-valid payload; malformed or non-completed output cannot satisfy the check. | FR-007-AC-16; TC-145 | missing-requirement |
| FND-003 | high | Resolved: TC-146 freezes the pre-change advice result and permits only the intended `differential-testing` additions, preventing an applicability edit from silently changing unrelated advice or advice states. | FR-007-AC-17; TC-146 | missing-requirement |
| FND-004 | high | Open implementation dependency: Engineering Assurance #34 has not yet published the typed Rust producer-execution boundary required by FR-007-CON-1, so TC-145 and TC-146 remain planned and blocked. | FR-007-CON-1; TC-145; TC-146 | correct-requirement-no-evidence |
| FND-005 | medium | Resolved by the first TC-144 run: FR-007 still claimed 31 methods after compile-time and sanitizer methods had raised the pre-change manifest to 33; the differential entry makes the exact total 34, with 22 Test and 9 Analysis entries. | FR-007 seed set; TC-048; TC-144 | implementation-bug-despite-evidence |

## Checklist results

| Check | Result |
| --- | --- |
| IDs and uniqueness | FR-007-AC-1 through AC-17 and TC-001 through TC-146 are unique and sequential after remediation. |
| Requirement form | The method identity, fields, applicability, claim limits and external execution boundary are explicit. |
| Coverage | AC-15, AC-16, AC-17 and CON-1 each map to at least one planned TC. |
| Negative cases | Field mutation, method substitution, claim inflation, neighbour methods, malformed output, non-completion and advice-delta cases are named. |
| Completion honesty | TC-144 is planned; TC-145 and TC-146 are blocked. No implementation or qualification claim is made. |
