---
id: NFR-002
title: "Feature risk evidence is human-authored"
type: NFR
quality_attribute: reliability
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-artifacts-process/FR-024"
    type: "constrains"
  - target: "ix://agent-ix/spec-artifacts-process/FR-025"
    type: "constrains"
  - target: "ix://agent-ix/spec-artifacts-process/FR-026"
    type: "constrains"
  - target: "ix://agent-ix/spec-artifacts-process/FR-027"
    type: "constrains"
---
# NFR-002: Feature risk evidence is human-authored

## Statement

The module SHALL record every feature-risk rating with the identity of its author and the applicable intended-use context.

## Scope

- Applies to `IntendedUse` and `FeatureRiskRating` documents and validation rules defined by FR-024 through FR-026.
- Adopters may use the rating and other evidence to make their own TCL, TQL or T-class determination for their intended use.

## Rationale

Risk decisions belong to the person responsible for the intended use. Keeping the information and the decision separate lets adopters make their own assessment without treating a tool-generated value as an approval.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| Feature ratings traceable to a named human and an intended-use context | 100% | 100% | Test |

## Verification

Validate supplier and adopter fixtures to confirm each rating retains its named author and intended-use context.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-002-AC-1 | Every supplier and adopter rating requires a named rater and its applicable intended-use context. | Test |
