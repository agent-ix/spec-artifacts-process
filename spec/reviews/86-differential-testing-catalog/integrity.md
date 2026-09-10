---
id: SR-018
title: "Integrity review of the differential-testing catalogue extension"
type: SpecReview
analysis: integrity
scope: "FR-007 and TM-001 differential-testing additions"
review_set: all
evaluated_revision: "e5035b1"
review_date: "2026-09-10"
relationships:
  - { target: ix://agent-ix/spec-artifacts-process/FR-007, type: reviews }
---
# SR-018: Integrity review of the differential-testing catalogue extension

## Summary

The catalogue census is internally consistent: 22 Test, 7 Analysis, 1
Inspection and 2 Demonstration methods total 32. Each new criterion owns one
observable concern and the matrix represents all three criteria plus the Rust
containment constraint.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | medium | Resolved: FR-007 acceptance rows and TM-001 coverage rows had inherited the file's non-sequential AC-12..14-before-AC-9..11 ordering; the reviewed revision restores numeric order. | FR-007 Acceptance Criteria; TM-001 | wrong-requirement |
| FND-002 | medium | Resolved: the prose census, per-class count and listed method names agree at 32 methods and make the added method visible in both the total and Test class. | FR-007 seed set | correct-requirement-no-evidence |
| FND-003 | low | No unresolved atomicity or consistency defect was found; the declarative entry, cross-tool selection and corpus-wide delta are separate criteria with separate tests. | FR-007-AC-15..17 | correct-requirement-no-evidence |

## Traceability

```text
FR-007-AC-15 -> TC-144
FR-007-AC-16 -> TC-145
FR-007-AC-17 -> TC-146
FR-007-CON-1 -> TC-144, TC-145, TC-146
```

