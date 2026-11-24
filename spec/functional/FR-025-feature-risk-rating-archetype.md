---
id: FR-025
title: "FeatureRiskRating records human-owned risk and detection evidence"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-011"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-012"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-024"
    type: "depends_on"
---
# FR-025: FeatureRiskRating records human-owned risk and detection evidence

## Description

A tool supplier and an adopter can assess the same feature under different intended uses. The module SHALL declare a `FeatureRiskRating` artifact type that records a named person's risk rating and per-feature failure and detection information, while keeping supplier ratings and adopter re-ratings distinct.

## Inputs

- A Markdown document with `type: FeatureRiskRating`.
- One or more target functional requirements.
- A named rater and the intended-use context for the rating.

## Outputs

- A validated rating record with explicit scope and per-feature evidence.
- A trace from an adopter re-rating to the supplier rating it reassesses.

## Behavior

- The module SHALL require frontmatter fields `id`, `type`, `scope`, `rating`, `rated_by`, `intended_use` and `relationships` for a `FeatureRiskRating` document.
- The `id` field SHALL match `FRR-{next:03d}`.
- The `type` field SHALL equal `FeatureRiskRating`.
- `scope` SHALL be exactly `supplier` or `adopter`.
- The `rating` field SHALL equal `high_process_risk` or `not_high_process_risk`.
- The schema SHALL reject every other `rating` value.
- The schema SHALL declare no default `rating` value.
- `rated_by` SHALL name the allowed-signers principal of the person who chose the rating.
- A supplier rating's `intended_use` field SHALL reference one `IntendedUse` record in the tool's repository.
- An adopter rating's `intended_use` field SHALL identify the adopter's own intended-use subject in the engineering-assurance integrator package.
- This module SHALL NOT redefine the adopter's intended-use subject or copy the adopter configuration.
- The module SHALL declare the edge `re_rates` from adopter `FeatureRiskRating` to supplier `FeatureRiskRating`, with inverse `rerated_by`.
- A supplier rating SHALL carry one or more `rates_feature` relationships to functional requirements and SHALL NOT carry a `re_rates` relationship.
- An adopter rating SHALL carry one or more `re_rates` relationships to supplier `FeatureRiskRating` records covering those same requirements and SHALL NOT carry a `rates_feature` relationship.
- The schema SHALL reject relationships that do not match the rating's `scope`.
- Every target requirement SHALL have one row in a required `Feature assessments` table with columns `Requirement`, `Failure mode` and `Detection`.
- The failure-mode cell SHALL describe a plausible failure of that feature and its effect on records named by the applicable intended use.
- The detection cell SHALL identify the activity or observation by which the failure can be found.
- The document SHALL contain a `Rationale` section.
- The document SHALL contain an `Assurance activities` section.
- The rationale SHALL explain why the rating fits the intended use.
- Assurance activities SHALL identify each selected test, inspection or analysis and the acceptance criterion it addresses.
- One rating document MAY cover multiple requirements only when its rating and rationale apply to all of them and every requirement has its own failure-mode and detection row.
- An adopter rating SHALL be a separately authored assessment for the adopter's intended use.
- An adopter rating SHALL NOT replace or edit its supplier rating.
- An adopter rating SHALL NOT imply acceptance of its supplier rating.
- The records SHALL contain no calculated score, threshold, probability, product criticality or assigned software safety class.
- The records SHALL contain no computed rating.
- The adopter MAY use the recorded failure-mode and detection information with other evidence to make its own TCL, TQL or T-class determination.
- This module SHALL define no formula or mapping for those determinations.
- This ticket specifies the rating data. Human acceptance of a rating is specified by [FR-027](./FR-027-human-acceptance-of-risk-ratings.md).

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-025-AC-1 | A supplier rating with an allowed enum value, named rater, valid IntendedUse reference, one `rates_feature` target, a corresponding feature-assessment row, `Rationale` and `Assurance activities` validates. | Test |
| FR-025-AC-2 | A supplier rating with `rating: medium`, a missing `rated_by`, missing `Rationale`, no `rates_feature` target or a missing feature-assessment row fails validation naming the invalid or missing member. An adopter rating without `re_rates` also fails. | Test |
| FR-025-AC-3 | A rating with two `rates_feature` targets validates only when it has a separate failure-mode and detection row for each target. | Test |
| FR-025-AC-4 | An adopter rating that identifies its own intended-use subject and re-rates a supplier record covering the same requirement validates; a missing supplier link, a link to a supplier rating covering a different requirement, or an adopter `rates_feature` edge fails validation. | Test |
| FR-025-AC-5 | An adopter rating does not change the supplier record when the two documents have different ratings or rationales. | Demonstration |
| FR-025-AC-6 | The schema rejects a calculated score, product-criticality field or software-safety-class field; no mapping in the module assigns those values or a rating. | Test |
| FR-025-AC-7 | The feature-assessment data names a failure mode and a detection activity, and leaves any TCL, TQL or T-class determination to the adopter. | Inspection |

## Dependencies

- [FR-024](./FR-024-intended-use-archetype.md) defines supplier intended use.
- [FR-026](./FR-026-feature-rating-completeness.md) requires exactly one supplier rating per functional requirement.
- [FR-027](./FR-027-human-acceptance-of-risk-ratings.md) defines human acceptance.
