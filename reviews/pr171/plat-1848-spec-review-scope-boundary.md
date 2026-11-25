---
id: SR-2026112016223475846355047
title: "Scope and responsibility review — ratings"
type: SpecReview
analysis: scope-boundary
scope: "agent-ix/spec-artifacts-process; PLAT-1848; spec/functional/FR-025-feature-risk-rating-archetype.md, spec/functional/FR-027-human-acceptance-of-risk-ratings.md, spec/non-functional/NFR-002-human-owned-feature-risk-decisions.md"
review_set: subset
---

## Summary

The module, signature-verification workflow, and human risk decision responsibilities are separated clearly in the changed requirements. No new external dependency or ownership conflict was found.

## Verdict

**PASS** — The module, signature-verification workflow, and human risk decision responsibilities are separated clearly in the changed requirements. No new external dependency or ownership conflict was found.

## Scope

| ID | Path | Role | Excerpt |
| --- | --- | --- | --- |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | The module owns rating-record shape and intended-use/feature relationships; it leaves acceptance to FR-027 and defines no classification formula. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | The workflow verifies the signed acceptance conditions and SHALL NOT decide whether a person should accept the risk. |
| NFR-002 | spec/non-functional/NFR-002-human-owned-feature-risk-decisions.md | examined | The module records intended-use context for every rating and accepting-person identity for accepted ratings. |
| FR-027-AC-13 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-13 \| A rating marked `proposed` is reported `not_accepted`, including when its commit is otherwise signed-valid. \| Test \| |
| FR-027-AC-14 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-14 \| An accepted rating requires a `rated_by` principal matching the verified signer and the exact acceptance trailer. \| Test \| |

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |
