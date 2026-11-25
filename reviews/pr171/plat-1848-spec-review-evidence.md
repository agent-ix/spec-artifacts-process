---
id: SR-2026112016223475846355046
title: "Evidence review — rating criteria methods"
type: SpecReview
analysis: evidence
scope: "agent-ix/spec-artifacts-process; PLAT-1848; spec/functional/FR-025-feature-risk-rating-archetype.md, spec/functional/FR-027-human-acceptance-of-risk-ratings.md, spec/non-functional/NFR-002-human-owned-feature-risk-decisions.md"
review_set: subset
---

## Summary

The verification-method advisor reports Test as authored for all changed criteria and no method mismatches. Matrix inspection found the FR-027 coverage gaps recorded in the base review.

## Verdict

**PASS** — The verification-method advisor reports Test as authored for all changed criteria and no method mismatches. Matrix inspection found the FR-027 coverage gaps recorded in the base review.

## Scope

| ID | Path | Role | Excerpt |
| --- | --- | --- | --- |
| FR-025-AC-1 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-1 \| A proposed supplier rating with an allowed enum value, no `rated_by`, valid IntendedUse reference, one `rates_feature` target, `Rationale` and `Assurance activities` validates. \| Test \| |
| FR-025-AC-2 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-2 \| A supplier rating with `rating: medium` fails validation and names the invalid rating. \| Test \| |
| FR-025-AC-3 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-3 \| A supplier rating with two `rates_feature` targets validates when both targets are existing FRs. \| Test \| |
| FR-025-AC-4 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-4 \| An adopter rating that identifies its own intended-use subject and re-rates a supplier record covering the same requirement validates. \| Test \| |
| FR-025-AC-5 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-5 \| An adopter rating remains a separate document and does not alter its supplier rating's content. \| Test \| |
| FR-025-AC-6 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-6 \| The schema rejects undeclared calculated-risk, product-criticality and software-safety-class fields. \| Test \| |
| FR-025-AC-7 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-7 \| A rating record carries covered requirements through relationships and does not carry per-requirement failure-mode or detection details. \| Test \| |
| FR-025-AC-8 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-8 \| A supplier rating without a `uses_intended_use` relationship fails validation. \| Test \| |
| FR-025-AC-9 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-9 \| A supplier rating with one `uses_intended_use` relationship to the repository's `IntendedUse` record validates. \| Test \| |
| FR-025-AC-10 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-10 \| A `rates_feature` relationship naming a missing FR fails with a dangling-reference diagnostic. \| Test \| |
| FR-025-AC-11 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-11 \| A `uses_intended_use` target that does not use the `IU-NNN` identifier form fails schema validation. \| Test \| |
| FR-025-AC-12 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-12 \| A supplier rating id has the form `FRR-NNN` with exactly three digits. \| Test \| |
| FR-025-AC-13 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-13 \| The manifest restricts `rates_feature` relationships to FR targets. \| Test \| |
| FR-025-AC-14 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-14 \| The FeatureRiskRating schema rejects feature-assessment properties and per-requirement details. \| Test \| |
| FR-025-AC-15 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-15 \| A `uses_intended_use` relationship to a missing `IU-NNN` record fails with a dangling-reference diagnostic. \| Test \| |
| FR-025-AC-16 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-16 \| A supplier rating with more than one `uses_intended_use` relationship fails schema validation. \| Test \| |
| FR-025-AC-17 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | \| FR-025-AC-17 \| A proposed rating has `status: proposed` and no `rated_by`; an accepted rating requires `status: accepted` and `rated_by`. \| Test \| |
| FR-027-AC-1 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-1 \| A rating last changed by a signed-valid, mapped commit whose principal equals `rated_by` and whose trailer is present is reported as `accepted`. \| Test \| |
| FR-027-AC-2 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-2 \| An unsigned commit is reported as `not_accepted` with reason `unsigned`. \| Test \| |
| FR-027-AC-3 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-3 \| A commit signed by a key not in allowed-signers is reported as `not_accepted` with a reason naming the signer mapping failure. \| Test \| |
| FR-027-AC-4 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-4 \| A signed commit whose verified principal differs from `rated_by` is reported as `not_accepted` with a reason naming the mismatch. \| Test \| |
| FR-027-AC-5 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-5 \| A signed commit without the exact acceptance trailer is reported as `not_accepted` with reason `meaning_missing`. \| Test \| |
| FR-027-AC-6 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-6 \| The acceptance result for supplier and adopter ratings depends on the same signature conditions and the rating schema records no commit id or digest. \| Test \| |
| FR-027-AC-7 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-7 \| The workflow sends exactly the versioned FR-036 request members and accepts only the versioned FR-036 result protocol. \| Test \| |
| FR-027-AC-8 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-8 \| A verifier process that cannot start produces `not_accepted` with a verifier failure reason. \| Test \| |
| FR-027-AC-9 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-9 \| A verifier process that times out or exits unexpectedly produces `not_accepted` with a verifier failure reason. \| Test \| |
| FR-027-AC-10 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-10 \| Verifier output that cannot be parsed produces `not_accepted` with a verifier failure reason. \| Test \| |
| FR-027-AC-11 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-11 \| Missing, unreadable or malformed allowed-signers input produces `not_accepted`; FR-037's `signature_verify_allowed_signers_invalid` error never produces acceptance. \| Test \| |
| FR-027-AC-12 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-12 \| A response with a wrong protocol or missing/malformed required result members produces `not_accepted`. \| Test \| |
| FR-027-AC-13 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-13 \| A rating marked `proposed` is reported `not_accepted`, including when its commit is otherwise signed-valid. \| Test \| |
| FR-027-AC-14 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-14 \| An accepted rating requires a `rated_by` principal matching the verified signer and the exact acceptance trailer. \| Test \| |
| FR-027-AC-13 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | \| FR-027-AC-13 \| The Quoin validation report identifies the versions of external tools and references their FR-220 configuration-index entries. \| Test \| |
| NFR-002-AC-1 | spec/non-functional/NFR-002-human-owned-feature-risk-decisions.md | examined | \| NFR-002-AC-1 \| Every supplier and adopter rating requires its applicable intended-use context; accepted ratings also require the accepting person's identity. \| Test \| |

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |
