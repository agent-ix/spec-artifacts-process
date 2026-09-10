---
id: SR-017
title: "Failure-domain review of the differential-testing catalogue extension"
type: SpecReview
analysis: failure-domain
scope: "FR-007-AC-15..17, FR-007-CON-1 and TC-144..TC-146"
review_set: all
evaluated_revision: "edf74a6"
review_date: "2026-09-10"
relationships:
  - { target: ix://agent-ix/spec-artifacts-process/FR-007, type: reviews }
---
# SR-017: Failure-domain review of the differential-testing catalogue extension

## Summary

The reviewed cases distinguish method identity from neighbouring techniques,
comparison from independence, and completed typed execution from arbitrary
process output. No graph or user callback is introduced; the relevant trust
boundaries are the module set, executable identity and two machine payloads.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | Resolved: a transformed second execution of the same implementation fails the catalogue contract instead of being accepted as differential evidence. | FR-007-AC-15; TC-144 | missing-requirement |
| FND-002 | high | Resolved: shared source or correlated observations cannot be promoted to independence, correctness, general equivalence or qualification merely because the comparison agrees. | FR-007 Description; FR-007-AC-15 | missing-requirement |
| FND-003 | high | Resolved: missing execution, timeout, refusal, other non-completion and malformed JSON cannot become a passing conformance observation. | FR-007-AC-16; TC-145 | missing-requirement |
| FND-004 | medium | Resolved: a closed module set prevents an ambient or duplicate catalogue entry from shadowing the authoritative candidate during the cross-tool check. | FR-007-AC-16; TC-145 | correct-requirement-no-evidence |

## Failure-domain checks

| Domain | Disposition |
| --- | --- |
| Identity confusion | Exact method, executable and closed module-set identities are asserted. |
| Partial execution | Only completed, schema-valid catalogue and advice results can satisfy TC-145. |
| False independence | Independence remains a consumer classification outside the catalogue. |
| Silent blast radius | TC-146 compares all prior advice fields and ordering over a frozen corpus. |

