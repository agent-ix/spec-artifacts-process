---
id: FR-017
title: "ADR may author the design-realization verb"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-architecture/FR-010"
    type: "depends_on"
---
# FR-017: ADR may author the design-realization verb

## Description

An ADR records a design decision, so it is a design element that realizes requirements.
spec-objects-architecture [FR-010](ix://agent-ix/spec-objects-architecture/FR-010) declares the verb
`realizes_requirement` (inverse `requirement_realized_by`) and lists the `ADR` archetype among the
elements its design relations accept. This module owns the `ADR` archetype, so it SHALL list the
verb in the archetype's `allowed_links`; otherwise an ADR that authors the verb draws an
advisory disallowed-edge-type finding although the relation still counts the edge.

## Inputs

- The `ADR` artifact type's `allowed_links` in the manifest.

## Outputs

- `realizes_requirement` in the `ADR` `allowed_links`.

## Behavior

- The `ADR` `allowed_links` SHALL include `realizes_requirement`, authored by the ADR toward the requirement it realizes.
- The `ADR` `allowed_links` SHALL NOT include `requirement_realized_by`, which a requirement authors toward the element.
- The `ADR` `allowed_links` SHALL keep every verb it listed before this requirement.
- A verb outside the `ADR` `allowed_links` SHALL still draw the disallowed-edge-type finding.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-017-AC-1 | `quire validate` of an `ADR` that authors `realizes_requirement` toward a requirement reports no `disallowed-edge-type` finding. | Test |
| FR-017-AC-2 | `quire validate` of an `ADR` that authors `requirement_realized_by` reports a `disallowed-edge-type` finding. | Test |
| FR-017-AC-3 | `quire validate` of an `ADR` that authors a verb outside the `ADR` `allowed_links` reports a `disallowed-edge-type` finding. | Test |
| FR-017-AC-4 | `supersedes`, `superseded_by`, `relates_to` and `depends_on` are all still in the `ADR` `allowed_links`. | Test |

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md), spec-objects-architecture [FR-010](ix://agent-ix/spec-objects-architecture/FR-010)
