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
- The `ADR` `allowed_links` SHALL keep every verb it listed before this requirement, each accepting any target (`"*"`).
- The `ADR` `allowed_links` SHALL limit the targets of `realizes_requirement` to `FR` and `NFR`, so an edge toward a document of another object type draws the advisory `disallowed-edge-target` finding naming the source, the target and the target's object type.
- An `ADR` edge `realizes_requirement` whose target resolves to no document SHALL fail `quire validate --okf --strict` with `dangling-reference` naming the file and the target id.
- With the module that declares the verb and the design relations loaded, `quire relations --json` SHALL report a requirement that an `ADR` realizes as `covered` with that `ADR` in `linked`.
- A verb outside the `ADR` `allowed_links` SHALL still draw the disallowed-edge-type finding.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-017-AC-1 | `quire validate` of an `ADR` that authors `realizes_requirement` toward a requirement reports no `disallowed-edge-type` finding. | Test |
| FR-017-AC-2 | `quire validate` of an `ADR` that authors `requirement_realized_by` reports a `disallowed-edge-type` finding. | Test |
| FR-017-AC-3 | `quire validate` of an `ADR` that authors a verb outside the `ADR` `allowed_links` reports a `disallowed-edge-type` finding. | Test |
| FR-017-AC-4 | `supersedes`, `superseded_by`, `relates_to` and `depends_on` are all still in the `ADR` `allowed_links`, each accepting any target. | Test |
| FR-017-AC-5 | The `ADR` `allowed_links` lists `realizes_requirement` with exactly the targets `FR` and `NFR`. | Test |
| FR-017-AC-6 | `quire validate --okf` of an `ADR` that authors `realizes_requirement` toward an `FR` and one that authors it toward an `NFR` reports neither `disallowed-edge-type` nor `disallowed-edge-target` for either. | Test |
| FR-017-AC-7 | `quire validate --okf --strict` of an `ADR` that authors `realizes_requirement` toward a part reports `disallowed-edge-target` naming the `ADR`, the part and its object type `part`. | Test |
| FR-017-AC-8 | `quire validate --okf --strict` of an `ADR` that authors `realizes_requirement` toward an id no document has fails with `dangling-reference` naming the `ADR` file and the id. | Test |
| FR-017-AC-9 | Over a corpus holding an `FR` and an `NFR` each realized by an `ADR`, `quire relations --json` reports each as `covered` with that `ADR` (archetype `ADR`) in `linked`. | Test |

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md), spec-objects-architecture [FR-010](ix://agent-ix/spec-objects-architecture/FR-010)
