---
id: IT-001
title: "Manifest activation roundtrip against filament-core"
type: IT
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-001"
    type: "verifies"
---
# IT-001: Manifest activation roundtrip

## Objective

Verify the integration boundary between this Module's manifest and filament-core: activating the manifest against a clean filament-core-service instance shall land every declared contribution in the database, and re-activating the same manifest shall be an idempotent no-op. Without this test, missing or duplicated contributions would go undetected.

## Target Integration

The system under test is filament-core-service, reached over its HTTP module API. The integration exercised is the activation of `spec_artifacts_process/manifest.yaml` via `POST /api/v1/modules/activate`, followed by read-back of the registered contributions through the archetype, object-type, grammar, and artifact-type endpoints.

## Preconditions

A filament-core-service instance is running and reachable on a clean cluster (or the kind dev cluster) with an empty modules table, so the absence or presence of registered contributions is meaningful for this Module.

## Inputs

The Module manifest `spec_artifacts_process/manifest.yaml`, which declares 5 archetypes, 1 grammar, and 7 artifact types. The same manifest bytes are submitted twice to exercise the idempotency path.

## Test Procedure

Each step performs one discrete action and has its own success criterion.

1. Deploy filament-core-service to a clean cluster (or use the kind dev cluster).
   - IT-001-SC-01: the service is reachable and the modules table is empty.
2. `POST spec_artifacts_process/manifest.yaml` to `/api/v1/modules/activate`.
   - IT-001-SC-02: the endpoint returns 200 OK and a Module row is created.
3. `GET /api/v1/archetypes`, `/api/v1/object-types`, `/api/v1/grammars`, and `/api/v1/artifact-types`.
   - IT-001-SC-03: each declared contribution is present with the correct attributes.
4. Re-`POST` the same manifest to `/api/v1/modules/activate`.
   - IT-001-SC-04: activation is an idempotent no-op (same `modules.id`, no row duplication, same SHA-256 content hash).

## Expected Results

The first activation returns 200 OK, creates the Module row, and registers every declared archetype, object type, grammar, and artifact type with correct attributes. The second activation produces the same `modules.id` and SHA-256 content hash with no duplicated rows. The test passes only when every per-step success criterion holds.
