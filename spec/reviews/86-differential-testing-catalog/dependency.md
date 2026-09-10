---
id: SR-019
title: "Dependency review of the differential-testing catalogue extension"
type: SpecReview
analysis: dependency
scope: "FR-007 dependencies across quire-rs, Quoin, Engineering Assurance and quire-verification"
review_set: all
evaluated_revision: "e5035b1"
review_date: "2026-09-10"
relationships:
  - { target: ix://agent-ix/spec-artifacts-process/FR-007, type: reviews }
---
# SR-019: Dependency review of the differential-testing catalogue extension

## Summary

The declarative entry depends on the existing quire-rs catalogue shape and the
already-mintable Quoin `reference-equivalence` fact. Executable conformance
depends separately on Engineering Assurance #34. The resulting order is
acyclic and does not require a Quoin frontend or adviser change.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | Open enablement dependency: TC-145 and TC-146 cannot be implemented without the accepted typed Rust execution/result seam from Engineering Assurance #34. | FR-007-CON-1; engineering-assurance#34 | correct-requirement-no-evidence |
| FND-002 | medium | Resolved: applicability reuses Quoin's existing `reference-equivalence` fact instead of inventing an unmintable `multiple-comparable-implementations` value. | FR-007 applicability rationale; quoin FR-031 | wrong-requirement |
| FND-003 | low | No dependency cycle was found; quire-verification consumes the accepted method but does not define or feed the shared catalogue. | spec-artifacts-process#86; quire-verification#21 | correct-requirement-no-evidence |

## Dependency order

```text
quire-rs FR-054 catalogue shape + Quoin FR-031 reference-equivalence fact
  -> spec-artifacts-process differential-testing entry
  -> Engineering Assurance #34 typed execution for TC-145/TC-146
  -> accepted catalogue revision
  -> quire-verification Task-028 consumption
```

