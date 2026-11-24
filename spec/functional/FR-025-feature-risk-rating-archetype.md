---
id: FR-025
title: "FeatureRiskRating records human-owned risk and detection evidence"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/StR-001"
    type: "satisfies"
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

- The module SHALL require frontmatter fields `id`, `type`, `scope`, `rating`, `rated_by` and `relationships` for a `FeatureRiskRating` document.
- A supplier rating SHALL identify its intended use with the typed `uses_intended_use` relationship.
- An adopter rating SHALL identify its intended use with the `intended_use` field.
- The `id` field SHALL match `FRR-{next:03d}`.
- The `type` field SHALL equal `FeatureRiskRating`.
- `scope` SHALL be exactly `supplier` or `adopter`.
- The `rating` field SHALL equal `high_process_risk` or `not_high_process_risk`.
- The schema SHALL reject every other `rating` value.
- The schema SHALL declare no default `rating` value.
- `rated_by` SHALL name the allowed-signers principal of the person who chose the rating.
- A supplier rating SHALL have exactly one `uses_intended_use` relationship to an `IntendedUse` record in the same tool repository.
- An adopter rating's `intended_use` field SHALL identify the adopter's own intended-use subject in the engineering-assurance integrator package.
- This module SHALL NOT redefine the adopter's intended-use subject or copy the adopter configuration.
- The module SHALL declare the edge `re_rates` from adopter `FeatureRiskRating` to supplier `FeatureRiskRating`, with inverse `rerated_by`.
- The module SHALL declare the edge `uses_intended_use` from supplier `FeatureRiskRating` to `IntendedUse`, with inverse `used_by_rating`.
- A supplier rating SHALL carry one or more `rates_feature` relationships to functional requirements.
- A supplier rating SHALL NOT carry a `re_rates` relationship.
- An adopter rating SHALL carry one or more `re_rates` relationships to supplier `FeatureRiskRating` records.
- Each adopter `re_rates` target SHALL cover the same functional requirements as the adopter rating.
- An adopter rating SHALL NOT carry a `rates_feature` relationship.
- The schema SHALL reject relationships that do not match the rating's `scope`.
- The `Feature assessments` table SHALL have the columns `Requirement`, `Failure mode` and `Detection`.
- Every `Requirement` cell SHALL reference an existing functional requirement.
- Every target requirement SHALL have one corresponding `Feature assessments` row.
- A `Feature assessments` table SHALL NOT contain a row for a requirement the rating does not target.
- A `Feature assessments` table SHALL NOT contain more than one row for the same requirement.
- The failure-mode cell SHALL describe a plausible failure of that feature and its effect on records named by the applicable intended use.
- The detection cell SHALL identify the activity or observation by which the failure can be found.
- The document SHALL contain a `Rationale` section.
- The document SHALL contain an `Assurance activities` section.
- The rationale SHALL explain why the rating fits the intended use.
- Assurance activities SHALL identify each selected test, inspection or analysis and the acceptance criterion it addresses.
- A rating document MAY cover multiple requirements.
- When one rating covers multiple requirements, its rating SHALL apply to each target.
- When one rating covers multiple requirements, its rationale SHALL apply to each target.
- An adopter rating SHALL be a separately authored assessment for the adopter's intended use.
- An adopter rating SHALL NOT replace or edit its supplier rating.
- An adopter rating SHALL NOT imply acceptance of its supplier rating.
- The records SHALL contain no calculated risk score, threshold or probability.
- The records SHALL contain no product-criticality value.
- The records SHALL contain no assigned software-safety-class value.
- The records SHALL contain no computed rating.
- The adopter MAY use the recorded failure-mode and detection information with other evidence to make its own TCL, TQL or T-class determination.
- This module SHALL define no formula or mapping for those determinations.
- This ticket specifies the rating data. Human acceptance of a rating is specified by [FR-027](./FR-027-human-acceptance-of-risk-ratings.md).

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-025-AC-1 | A supplier rating with an allowed enum value, named rater, valid IntendedUse reference, one `rates_feature` target, a corresponding feature-assessment row, `Rationale` and `Assurance activities` validates. | Test |
| FR-025-AC-2 | A supplier rating with `rating: medium` fails validation and names the invalid rating. | Test |
| FR-025-AC-3 | A supplier rating with two `rates_feature` targets validates when both targets are existing FRs and both have assessment rows. | Test |
| FR-025-AC-4 | An adopter rating that identifies its own intended-use subject and re-rates a supplier record covering the same requirement validates. | Test |
| FR-025-AC-5 | An adopter rating remains a separate document and does not alter its supplier rating's content. | Test |
| FR-025-AC-6 | The schema rejects undeclared calculated-risk, product-criticality and software-safety-class fields. | Test |
| FR-025-AC-7 | The feature-assessment data records a failure mode and a detection activity without assigning a TCL, TQL or T-class determination. | Test |
| FR-025-AC-8 | A supplier rating without a `uses_intended_use` relationship fails validation. | Test |
| FR-025-AC-9 | A supplier rating with one `uses_intended_use` relationship to the repository's `IntendedUse` record validates. | Test |
| FR-025-AC-10 | A requirement cell naming a missing FR fails with a dangling-reference diagnostic. | Test |
| FR-025-AC-11 | A `uses_intended_use` target that does not use the `IU-NNN` identifier form fails schema validation. | Test |
| FR-025-AC-12 | A supplier rating id has the form `FRR-NNN` with exactly three digits. | Test |
| FR-025-AC-13 | The manifest types `Feature assessments.Requirement` references as FRs. | Test |
| FR-025-AC-14 | Cross-checking assessment-row equality and uniqueness against relationship targets is declared as an SWM-248 engine gap, not as a local implemented validation. | Inspection |
| FR-025-AC-15 | A `uses_intended_use` relationship to a missing `IU-NNN` record fails with a dangling-reference diagnostic. | Test |
| FR-025-AC-16 | A supplier rating with more than one `uses_intended_use` relationship fails schema validation. | Test |

## Dependencies

- [FR-024](./FR-024-intended-use-archetype.md) defines supplier intended use.
- [FR-026](./FR-026-feature-rating-completeness.md) requires exactly one supplier rating per functional requirement.
- [FR-027](./FR-027-human-acceptance-of-risk-ratings.md) defines human acceptance.
- Quire-rs [SWM-248](https://linear.app/agent-ix/issue/SWM-248) owns the missing cross-table equality and table-value uniqueness assertions; this module declares the typed reference but does not claim those engine checks are implemented.
