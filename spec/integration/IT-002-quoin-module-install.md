---
id: IT-002
title: "Module installs into Quoin with the semantic contract"
type: IT
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-010"
    type: "verifies"
---
# IT-002: Module installs into Quoin with the semantic contract

## Objective

Verify the boundary between this module's shipped directory and the Quoin module installer:
`quoin module install path:<dir>` shall accept the `semantic` block, resolve every reference-form
`data_schema`, verify every digest, derive the package manifest, and list the module. Without this
test a module that Quire accepts and Quoin refuses would ship, and nothing in this specification
would notice — the gap SR-015 FND-001 records.

## Target Integration

The system under test is `spec_artifacts_process/` as consumed by a Quoin carrying FR-070, FR-073
and FR-075. The integration type is a local CLI invocation over the filesystem; no network read is
involved.

## Preconditions

A Quoin carrying the semantic module contract is on `PATH`. The current `quoin module` listing is
recorded first, so the prior `spec-artifacts-process` entry (source, ref, sha) can be restored —
this module is installed in the developer's own environment and every other repository's
validation depends on that entry.

## Inputs

The module directory `spec_artifacts_process/` from this branch, containing `manifest.yaml`,
`schemas/`, `skeletons/`, `mappings.yaml`, `mappings.schema.json` and `examples/`.

## Test Procedure

Each step performs one discrete action and has its own success criterion.

1. Record `quoin module` output before the install.
   - IT-002-SC-01: the listing is captured, including the existing `spec-artifacts-process` entry.
2. Run `quoin module install path:<checkout>/spec_artifacts_process`.
   - IT-002-SC-02: exit code 0 and no `semantic.*` diagnostic at error severity.
3. Run `quoin module`.
   - IT-002-SC-03: the listing contains `spec-artifacts-process` sourced from the path.
4. Inspect the installed module root.
   - IT-002-SC-04: the derived package manifest names `agent-ix/spec-artifacts-process` and one
     export per `semantic.exports` entry — twelve.
5. Restore the prior state unconditionally, whether or not steps 2-4 passed: re-install the
   recorded source and ref.
   - IT-002-SC-05: `quoin module` equals the recording of step 1.
   - IT-002-SC-06: the restore step runs even when an earlier step failed.

## Expected Results

The install succeeds with exit code 0, the module is listed, the derived package manifest names
the twelve exports, and the prior module state is restored. The test passes only when every
per-step success criterion holds. Because this repository's installed module entry is what every
other repository validates against, step 5 is not cleanup — a failed restore leaves the whole
development environment validating against an uncommitted branch.

## Dependencies

- **Upstream**: [FR-010](../functional/FR-010-semantic-manifest-contract.md)
- **Downstream**: none
