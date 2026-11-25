---
id: SR-2026112016223475846355042
title: "Python code review — rating schema tests"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process; PLAT-1848; spec/functional/FR-025-feature-risk-rating-archetype.md, spec/functional/FR-027-human-acceptance-of-risk-ratings.md, spec/non-functional/NFR-002-human-owned-feature-risk-decisions.md, tests/test_feature_risk_rating.py"
review_set: subset
---

## Summary

Focused Python test review found one missing negative test for proposed ratings and one weak trace binder for NFR-002-AC-1.

## Verdict

**CONDITIONAL** — Focused Python test review found one missing negative test for proposed ratings and one weak trace binder for NFR-002-AC-1.

## Scope

| ID | Path | Role | Excerpt |
| --- | --- | --- | --- |
| FR-025-AC-17 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-17 \| A proposed rating has `status: proposed` and no `rated_by`; an accepted rating requires `status: accepted` and `rated_by`. \| Test \| |
| FR-025-AC-7 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-7 \| A rating record carries covered requirements through relationships and does not carry per-requirement failure-mode or detection details. \| Test \| |
| FR-027-AC-13 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-13 \| A rating marked `proposed` is reported `not_accepted`, including when its commit is otherwise signed-valid. \| Test \| |
| FR-027-AC-14 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-14 \| An accepted rating requires a `rated_by` principal matching the verified signer and the exact acceptance trailer. \| Test \| |
| NFR-002-AC-1 | spec/non-functional/NFR-002-human-owned-feature-risk-decisions.md | examined | \| NFR-002-AC-1 \| Every supplier and adopter rating requires its applicable intended-use context; accepted ratings also require the accepting person's identity. \| Test \| |
| test_proposed_and_accepted_ratings_have_consistent_authorship | tests/test_feature_risk_rating.py | examined | A proposed fixture without rated_by validates; accepted without rated_by fails; accepted with rated_by validates. No test supplies rated_by to a proposed fixture. |
| test_authorship_and_computed_decision_boundaries_are_schema_visible | tests/test_feature_risk_rating.py | examined | The test asserts status is required, rated_by is not globally required, and computed fields are absent; it does not assert intended-use context or conditional accepted identity. |

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The test verifies a proposed rating without rated_by and both accepted cases, but never adds rated_by to a proposed rating and asserts rejection. That leaves the new forbidden-field branch untested. | tests/test_feature_risk_rating.py:102-125 |
| FND-002 | medium | The only test tagged to NFR-002-AC-1 checks required status, global rated_by optionality, and absent computed fields. It does not verify intended-use context or that accepted ratings require an accepting identity, so the criterion is not supported by its current binding. | tests/test_feature_risk_rating.py:674-694 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | The focused schema test now supplies rated_by to a proposed rating and asserts validation rejects it. |
| FND-002 | fixed | The tagged NFR-002 test now asserts missing supplier/adopter intended-use context and missing accepted identity are rejected. |
