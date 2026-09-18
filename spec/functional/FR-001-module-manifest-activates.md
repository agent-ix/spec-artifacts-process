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

## Outputs

- Module row in `modules` table
- Contributed archetypes, object_types, grammars, artifact_types per the manifest

## Behavior

The manifest **SHALL** validate against `module-manifest.schema.json` v1.0.0. Re-activation **SHALL** be a no-op (idempotent by content hash per FR-026-AC-1).

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-001-AC-1 | Manifest validates against FR-035 JSON Schema | Schema Test |
| FR-001-AC-2 | Activation against clean filament-core succeeds with 200 | Integration Test |
| FR-001-AC-3 | Re-activation returns no-op (same content hash) | Integration Test |
| FR-001-AC-4 | Each declared archetype/object_type/artifact_type appears in the corresponding filament-core table after activation | Integration Test |

## Notes

- **FR-001-AC-1 known contract lag**: the Schema Test (`test_manifest_validates_against_fr035_schema`) strips `required` from every `traceability.trace_targets` entry before validating, because quire-rs `traceability.rs` has typed `TraceTarget.required` since #327 but the published FR-035 schema this repo imports predates it. Tracked upstream at `agent-ix/spec-artifacts-iso#32` (CR-013), open, not yet merged. Remove the strip once #32 ships a schema revision that types `required`.

## Dependencies

- **Upstream**: filament-core-service [FR-035](ix://agent-ix/filament-core-service/FR-035), FR-026, FR-034
- **Downstream**: consumer agents/editors discovering this module's contributions
