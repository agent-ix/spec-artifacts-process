---
id: FR-019
title: "ADR may author the segregation design verb"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-017"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-architecture/FR-016"
    type: "depends_on"
---
# FR-019: ADR may author the segregation design verb

## Description

An ADR records a design decision, so it is the place where a person records how the software item that carries a
risk-control requirement is kept apart from other items, including the decision that no segregation is needed.
spec-objects-architecture [FR-016](ix://agent-ix/spec-objects-architecture/FR-016) declares the verb
`segregates_for_requirement` (inverse `requirement_segregated_by`) and accepts an `ADR` among the elements its segregation
relations read. This module owns the `ADR` archetype, so it SHALL list the verb in the archetype's `allowed_links`, as
[FR-017](./FR-017-adr-design-realization-verb.md) does for `realizes_requirement`. Otherwise an ADR that authors the verb draws
the advisory `disallowed-edge-type` finding although the relation still counts the edge.

## Inputs

- The `ADR` artifact type's `allowed_links` in the manifest.

## Outputs

- `segregates_for_requirement` in the `ADR` `allowed_links` with the targets `FR` and `NFR`.

## Behavior

- The `ADR` `allowed_links` SHALL include `segregates_for_requirement`, authored by the ADR toward the requirement it segregates, with exactly the targets `FR` and `NFR`.
- The `ADR` `allowed_links` SHALL NOT include `requirement_segregated_by`, which a requirement authors toward the element.
- The `ADR` `allowed_links` SHALL keep `realizes_requirement` and every verb it listed before this requirement.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-019-AC-1 | The `ADR` `allowed_links` lists `segregates_for_requirement` with exactly the targets `FR` and `NFR`. | Test |
| FR-019-AC-2 | The `ADR` `allowed_links` does not include `requirement_segregated_by`. | Test |
| FR-019-AC-3 | The `ADR` `allowed_links` still lists `realizes_requirement` with the targets `FR` and `NFR`. | Test |
| FR-019-AC-4 | `quire validate` of an `ADR` that authors `segregates_for_requirement` toward a requirement reports no `disallowed-edge-type` finding. | Test |
| FR-019-AC-5 | `quire validate` of an `ADR` that authors the inverse `requirement_segregated_by` reports a `disallowed-edge-type` finding. | Test |

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md), [FR-017](./FR-017-adr-design-realization-verb.md), spec-objects-architecture [FR-016](ix://agent-ix/spec-objects-architecture/FR-016)
