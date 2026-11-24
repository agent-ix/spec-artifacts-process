---
id: FRR-001
title: <feature group> risk rating for <intended use>
type: FeatureRiskRating
scope: supplier
rating: not_high_process_risk
rated_by: <named person>
relationships:
  - target: ix://agent-ix/spec-artifacts-process/IU-001
    type: uses_intended_use
  - target: ix://agent-ix/spec-artifacts-process/FR-024
    type: rates_feature
---
# <feature group> risk rating

## Feature assessments

| Requirement | Failure mode | Detection |
|---|---|---|
| FR-001 | <Describe a plausible failure and its effect on intended-use records.> | <Identify the activity or observation that detects it.> |

## Rationale

<Explain why the person-assigned rating fits this intended use.>

## Assurance activities

| Activity | Acceptance criterion |
|---|---|
| <Test, inspection, or analysis> | <Criterion addressed> |
