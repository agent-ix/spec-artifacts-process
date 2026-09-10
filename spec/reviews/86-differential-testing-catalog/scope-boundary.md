---
id: SR-022
title: "Scope-boundary review of the differential-testing catalogue extension"
type: SpecReview
analysis: scope-boundary
scope: "FR-007 ownership across shared catalogue, advisor, assurance and consumer repositories"
review_set: all
evaluated_revision: "edf74a6"
review_date: "2026-09-10"
relationships:
  - { target: ix://agent-ix/spec-artifacts-process/FR-007, type: reviews }
---
# SR-022: Scope-boundary review of the differential-testing catalogue extension

## Summary

The extension stays in the shared catalogue's data and contract boundary.
Quoin continues to own advice and catalogue JSON, Engineering Assurance owns
bounded execution/results, and each consumer owns candidate/oracle identity,
dependence, comparison semantics and evidence sufficiency.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | Resolved: the catalogue definition no longer implies that a second implementation is independent or that agreement proves correctness, equivalence or qualification. | FR-007 differential boundary | wrong-requirement |
| FND-002 | high | Resolved: the repository may not add its own runner, stdout verdict parser, evidence store or Python/JavaScript acceptance path to work around the missing shared interface. | FR-007-CON-1 | missing-requirement |
| FND-003 | low | No scope overlap with native Quire frontend/profile redesign work was found; this change adds one verification-method datum and its assurance contract only. | spec-artifacts-process#86; quire-research#64 | correct-requirement-no-evidence |

## Responsibility allocation

| Owner | Responsibility |
| --- | --- |
| spec-artifacts-process | Method identity, definition, class, evidence kind, applicability and tooling metadata. |
| quire-rs | Catalogue schema, merge and derived vocabularies. |
| Quoin | Observable facts, recommendation logic and catalogue/advice JSON. |
| Engineering Assurance | Exact bounded producer execution and typed result states. |
| quire-verification | Candidate/oracle/configuration identities, dependence, comparison relation and sufficiency. |

