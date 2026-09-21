---
id: FR-001
title: "Module manifest activates against filament-core"
type: FR
relationships:
  - target: "ix://agent-ix/filament-core-service/FR-035"
    type: "implements"
---
# FR-001: Module manifest activates against filament-core

## Description

The system **SHALL** publish a Filament Module manifest (`spec_artifacts_process/manifest.yaml`) that conforms to filament-core-service [FR-035](ix://agent-ix/filament-core-service/FR-035) v1.0.0 and activates idempotently against `POST /api/v1/modules/activate`.


## Inputs

- `manifest.yaml` (this repo's package)
- Activation endpoint: `POST /api/v1/modules/activate`
- The FR-035 module-manifest schema, owned by `filament-core-service` and applied
  by it at activation. This repository holds no copy of that schema and depends
  on no package that redistributes one (PLAT-902), so it states no criterion over
  the schema as a document.

## Outputs

- Module row in `modules` table
- Contributed archetypes, object_types, grammars, artifact_types per the manifest

## Behavior

The manifest **SHALL** conform to the FR-035 module-manifest schema
`filament-core-service` applies at activation. Conformance is observed where that
schema is applied — at `POST /api/v1/modules/activate` (FR-001-AC-2) — and, for
the keys the engines read, at Quire's registry loader (FR-010-AC-6, TC-093,
TC-094). Re-activation **SHALL** be a no-op (idempotent by content hash per
FR-026-AC-1).

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-001-AC-2 | Activation against clean filament-core succeeds with 200 | Integration Test |
| FR-001-AC-3 | Re-activation returns no-op (same content hash) | Integration Test |
| FR-001-AC-4 | Each declared archetype/object_type/artifact_type appears in the corresponding filament-core table after activation | Integration Test |

## Notes

- **Why there is no schema criterion here.** The retired FR-001-AC-1 was verified
  by a test that validated this manifest against a redistributed copy of the
  schema, and to keep that copy accepting the manifest it had to remove two
  things first: the whole `semantic` block, which the copy rejects under
  `additionalProperties: false`, and `required` from every
  `traceability.trace_targets` entry, which the copy predates
  (`agent-ix/spec-artifacts-iso#32`, CR-013). The `semantic` block was then
  validated against a *second* local copy. A check that deletes what the schema
  would refuse, and reaches for a different copy for the remainder, reports on
  the copies rather than on conformance. It is deleted rather than repointed
  (PLAT-902). The wording that made the two-schema split possible is
  `agent-ix/filament-core-service#27`.

## Dependencies

- **Upstream**: filament-core-service [FR-035](ix://agent-ix/filament-core-service/FR-035), FR-026, FR-034
- **Downstream**: consumer agents/editors discovering this module's contributions
