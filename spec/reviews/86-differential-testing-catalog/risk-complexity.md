---
id: SR-021
title: "Risk and complexity review of the differential-testing catalogue extension"
type: SpecReview
analysis: risk-complexity
scope: "FR-007 differential-testing method and advisor impact"
review_set: all
evaluated_revision: "edf74a6"
review_date: "2026-09-10"
relationships:
  - { target: ix://agent-ix/spec-artifacts-process/FR-007, type: reviews }
---
# SR-021: Risk and complexity review of the differential-testing catalogue extension

## Summary

Technical risk is medium because one declarative entry changes recommendations
across every consumer of the shared catalogue. Volatility is low: the method
boundary and observable applicability fact are explicit, while the missing
Engineering Assurance interface is an implementation dependency rather than a
changing semantic decision.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | Resolved: TC-146 constrains the ecosystem-wide advice blast radius to obligations already carrying `reference-equivalence` and preserves every prior recommendation and state. | FR-007-AC-17; TC-146 | missing-requirement |
| FND-002 | high | Resolved: agreement cannot inflate into independence or qualification; those claims require separately retained consumer evidence. | FR-007 differential boundary; FR-007-AC-15 | missing-requirement |
| FND-003 | medium | Retained implementation risk: the first shared Rust producer-execution consumer may expose requirements missing from Engineering Assurance #34; any such need belongs in that shared interface before local implementation continues. | FR-007-CON-1; engineering-assurance#34 | correct-requirement-no-evidence |

## Risk controls

| Risk | Control |
| --- | --- |
| Advice over-selection | Frozen before/after corpus comparison in TC-146. |
| Method confusion | Negative property, metamorphic and integration controls in TC-145. |
| Correlated oracle evidence | Explicit claim ceiling and consumer-owned dependence classification. |
| Local tooling growth | Rust-only constraint and Engineering Assurance execution dependency. |
