---
id: SR-2026112016223475846355043
title: "Specification base review — rating lifecycle"
type: SpecReview
analysis: base
scope: "agent-ix/spec-artifacts-process; PLAT-1848; spec/functional/FR-025-feature-risk-rating-archetype.md, spec/functional/FR-027-human-acceptance-of-risk-ratings.md, spec/non-functional/NFR-002-human-owned-feature-risk-decisions.md, spec_artifacts_process/examples/FeatureRiskRating.md, spec_artifacts_process/manifest.yaml, spec_artifacts_process/schemas/FeatureRiskRating.json, spec_artifacts_process/semantic/main.tsp"
review_set: subset
---

## Summary

The base requirements checklist found a duplicate FR-027 acceptance-criterion ID and two new acceptance criteria without test trace tags. The object model was also checked across the source model, projections, example, and skeleton; that structure is consistent.

## Verdict

**CONDITIONAL** — The base requirements checklist found a duplicate FR-027 acceptance-criterion ID and two new acceptance criteria without test trace tags. The object model was also checked across the source model, projections, example, and skeleton; that structure is consistent.

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
| FR-025 object | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | FeatureRiskRating exposes status and rates_feature coverage; the removed assessment table and property are explicitly forbidden. |
| FeatureRiskRating model | spec_artifacts_process/semantic/main.tsp | examined | FeatureRiskRating declares scope, rating, status, optional ratedBy, relationships, provenance, rationale, and assuranceActivities; it has no FeatureAssessmentRow. |
| FeatureRiskRating schema | spec_artifacts_process/schemas/FeatureRiskRating.json | examined | Generated JSON Schema has no featureAssessments property and rejects unevaluated properties. |
| FeatureRiskRating manifest and mapping | spec_artifacts_process/manifest.yaml | examined | Markdown extraction no longer declares the removed assessment table; relationship tracing supplies requirement coverage. |
| FeatureRiskRating example and skeleton | spec_artifacts_process/examples/FeatureRiskRating.md | examined | The example record and skeleton have proposed status and no Feature assessments section. |

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-027-AC-13 is assigned to both the new proposed-rating criterion and the existing external-tool-version criterion. Duplicate IDs make test traceability ambiguous. | spec/functional/FR-027-human-acceptance-of-risk-ratings.md:85-87 |
| FND-002 | medium | The new proposed and accepted rating criteria have no test trace tags. The computed matrix reports the proposed criterion, accepted criterion, and duplicate external-tool-version criterion as untagged. | spec/functional/FR-027-human-acceptance-of-risk-ratings.md:85-87 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | medium | FR-027-AC-14 is tagged only to a schema-shape test; the test never exercises a signed-valid commit or verifies that a proposed rating is reported not_accepted. | tests/test_feature_risk_rating.py:102-141 |
| FND-004 | medium | FR-027-AC-15 is tagged only to a schema-shape test; it does not verify rated_by matches the mapped signer or the exact acceptance trailer. | tests/test_feature_risk_rating.py:102-141 |

| FND-003 | medium | FR-027-AC-14 has a trace tag on a schema-only test; the test never exercises a signed-valid commit or verifies that a proposed rating is reported not_accepted. | tests/test_feature_risk_rating.py:102-141 |
| FND-004 | medium | FR-027-AC-15 has a trace tag on a schema-only test; it never checks that rated_by matches the mapped signer and exact acceptance trailer. | tests/test_feature_risk_rating.py:102-141 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | The external-tool criterion is now AC-13, with proposed and accepted status criteria at AC-14 and AC-15. |
| FND-002 | still-open | AC-14 and AC-15 now carry tags, but FR-027-AC-13 remains untagged in `quire matrix`; its only marker is in a multiline decorator that the current matrix does not bind. The new AC-14/15 tags also point to schema-only assertions and do not test their report/signature behavior; see FND-003 and FND-004. |
| FND-002 | fixed | The matrix now binds AC-13, AC-14, and AC-15 to criterion-tagged tests. |
| FND-003 | fixed | The proposed-rating test exercises signed-valid evidence and asserts the proposed state returns not_accepted despite matching signer and trailer. |
| FND-004 | fixed | The accepted-rating test covers matching signer/trailer acceptance and rejects a signer mismatch or wrong trailer. |
| FND-002 | fixed | The current matrix binds FR-027-AC-13, AC-14, and AC-15 to their exact test functions. |
| FND-003 | fixed | The proposed-rating test creates and verifies a real signed commit with the exact acceptance trailer, then asserts the proposed state returns not_accepted despite otherwise valid mapped evidence. |
| FND-004 | fixed | The accepted-rating test asserts matching mapped principal plus exact trailer returns accepted, and signer mismatch or wrong trailer returns not_accepted. |
