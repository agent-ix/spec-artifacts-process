---
id: SR-20261113084032
title: "EARS review of FR-016 anomaly release rationale (spec-artifacts-process#147)"
type: SpecReview
analysis: ears-conformance
review_set: subset
scope: "agent-ix/spec-artifacts-process; PR #147 (git diff origin/main...plat-1528-spec-sap at 2b6d5e3): spec/functional/FR-016-anomaly-release-rationale.md, spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md, spec/spec.md, spec/functional/index.md"
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-016"
    type: references
---

# EARS review of FR-016 anomaly release rationale (spec-artifacts-process#147)

## Summary

Ticket: PLAT-1528. Method: spec-review/spec-ears-analysis, scoped to `git diff origin/main...HEAD` of agent-ix/spec-artifacts-process#147 at 2b6d5e3.
Read against FR-011, FR-014 and FR-015 on main and the consuming side in agent-ix/quoin#857 (FR-162, FR-163, FR-164, NFR-035).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |

## Verdict

Clean. Every FR-016 Behavior statement is a ubiquitous SHALL/SHALL NOT, a state-driven form (`at status closed when resolution is wont-fix`) or an unwanted-behaviour form (`If status is closed and resolution is not wont-fix, then validation SHALL fail ...`). The non-SHALL sentences (`The check is of shape only`, `Quoin holds no copy`) are clarifications in the same style as FR-014 and FR-015.

Examined (role examined): FR-016, FR-016-AC-1, FR-016-AC-2, FR-016-AC-3, FR-016-AC-4, FR-016-AC-5, FR-016-AC-6, FR-016-AC-7, FR-016-AC-8, FR-016-AC-9, FR-016-AC-10.
Context only: none.
