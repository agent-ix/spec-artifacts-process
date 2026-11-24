---
id: FRR-001
title: Quoin validation feature risk rating
type: FeatureRiskRating
scope: supplier
rating: not_high_process_risk
rated_by: Example Reviewer
relationships:
  - target: ix://agent-ix/spec-artifacts-process/IU-001
    type: uses_intended_use
  - target: ix://agent-ix/spec-artifacts-process/FR-009
    type: rates_feature
---
# Quoin validation feature risk rating

## Feature assessments

| Requirement | Failure mode | Detection |
|---|---|---|
| FR-009 | An invalid schema may allow malformed records to appear valid. | Run schema validation against invalid and valid fixtures and inspect diagnostics. |

## Rationale

The named reviewer selected this rating for the stated repository-validation use. The rating is a human judgement and is not calculated.

## Assurance activities

| Activity | Acceptance criterion |
|---|---|
| Validate representative valid and invalid records | Invalid records fail with a diagnostic naming the violated contract. |
