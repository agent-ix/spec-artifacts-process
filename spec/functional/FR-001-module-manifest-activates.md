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
  by it at activation. This repository holds no copy of that schema and depends on
  no package that redistributes it as a document this repository validates against
  (PLAT-902), so it states no criterion over the schema as a document. The engines
  do carry copies of their own and apply them when they read this manifest
  (FR-010 Inputs); that is the carriers' business, not a source this repository
  validates against.

## Outputs

- Module row in `modules` table
- Contributed archetypes, object_types, grammars, artifact_types per the manifest

## Behavior

The manifest **SHALL** conform to the FR-035 module-manifest schema
`filament-core-service` applies at activation, and re-activation **SHALL** be a
no-op (idempotent by content hash per FR-026-AC-1).

**Conformance to that schema is verified nowhere in this repository today**, and
this requirement claims no otherwise. It is verified where the schema is applied,
at `POST /api/v1/modules/activate` — FR-001-AC-2 through AC-4, whose IT-001 has
no implementing test (`spec/tests.md` carries FR-001 as `🚧 Specified`). What
*is* executed here is narrower and is not a substitute: `quire.Registry.load_from`
over this module loads every declared archetype against the 0.1.0 baseline
(FR-010-AC-5, TC-093), and a `semantic` block gaining an unknown key is refused
at load (FR-010-AC-6, TC-094 — whose digest half pins measured engine inertness,
`agent-ix/quire-rs#400`, and whose "names the offender" half is a strict expected
failure, GAP-004). A manifest edit that breaks FR-035 conformance without
breaking the loader ships green.

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
