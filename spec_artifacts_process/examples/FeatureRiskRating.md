---
id: FRR-001
title: Quoin validation feature risk rating
type: FeatureRiskRating
scope: supplier
rating: not_high_process_risk
status: proposed
relationships:
  - target: ix://agent-ix/spec-artifacts-process/IU-001
    type: uses_intended_use
  - target: ix://agent-ix/spec-artifacts-process/FR-009
    type: rates_feature
---
# Quoin validation feature risk rating

## Rationale

The example rating is a human judgement and is not calculated.

## Assurance activities

| Activity | Acceptance criterion |
|---|---|
| Validate representative valid and invalid records | Invalid records fail with a diagnostic naming the violated contract. |
