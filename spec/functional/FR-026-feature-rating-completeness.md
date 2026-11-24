---
id: FR-026
title: "Feature risk rating completeness and duplicate detection"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-025"
    type: "depends_on"
---
# FR-026: Feature risk rating completeness and duplicate detection

## Description

A tool repository's feature list is complete only when each functional requirement has exactly one supplier `FeatureRiskRating`. The module SHALL declare a completeness rule that reports missing and duplicate supplier ratings without imposing it on repositories that do not opt into tool validation.

## Inputs

- A corpus of functional requirements and `FeatureRiskRating` records.
- A Quire validation severity for the completeness check.

## Outputs

- A `feature-without-risk-rating` finding for each unrated functional requirement when the rule is enabled.
- A duplicate-rating finding for each functional requirement with more than one supplier rating, naming all conflicting rating ids.

## Behavior

- The module SHALL declare the edge `rates_feature` from `FeatureRiskRating` to a functional requirement and its inverse `rated_by_rating`.
- The module SHALL declare a required-relation rule named `fr-has-risk-rating` from `FR`, over `rates_feature`, to `FeatureRiskRating`, with incoming direction and check `feature-without-risk-rating`.
- The rule SHALL consider only records whose `scope` is `supplier`.
- An adopter re-rating SHALL neither satisfy nor duplicate a supplier rating.
- The check's default severity SHALL be `off`.
- The validator SHALL apply the check at severity `error` when invoked with `quire validate --severity trace:feature-without-risk-rating=error`.
- When the check is enabled, each FR with no supplier rating SHALL produce exactly one finding that names the FR.
- A tool repository's rating validation SHALL report a duplicate when one FR is targeted by more than one supplier rating, naming each conflicting `FRR` id.
- The validation SHALL not suppress a duplicate finding because the required-relation check passes.
- A tool repository SHALL have exactly one supplier `IntendedUse` document.
- The supplier rating set SHALL be complete only when every FR in `spec/functional/` is targeted by exactly one supplier rating.
- Every rating in a complete set SHALL meet the human-acceptance requirement in [FR-027](./FR-027-human-acceptance-of-risk-ratings.md).

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-026-AC-1 | Given three FRs and supplier ratings for two, validation at severity `error` reports exactly one `feature-without-risk-rating` finding naming the third FR. | Test |
| FR-026-AC-2 | The same fixture reports no `feature-without-risk-rating` finding at the default severity. | Test |
| FR-026-AC-3 | An edge from `FeatureRiskRating` to a non-FR target reports `target-kind-mismatch`. | Test |
| FR-026-AC-4 | When two supplier ratings target the same FR, the duplicate diagnostic names that FR and both rating ids. | Test |
| FR-026-AC-5 | An adopter rating for an otherwise unrated FR does not satisfy the supplier completeness rule and is not counted as a duplicate supplier rating. | Test |
| FR-026-AC-6 | A tool repository is reported complete only when every FR has exactly one supplier rating and every such rating is human-accepted. | Test |

## Dependencies

- [FR-025](./FR-025-feature-risk-rating-archetype.md) defines rating scope and `rates_feature`.
- [FR-027](./FR-027-human-acceptance-of-risk-ratings.md) defines accepted ratings.
