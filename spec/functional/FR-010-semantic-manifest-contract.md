---
id: FR-010
title: "Declare the semantic-module contract in the manifest without altering an archetype"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-002"
    type: "implements"
  - target: "ix://agent-ix/spec-artifacts-process/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-070"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-073"
    type: "depends_on"
---
# FR-010: Declare the semantic-module contract in the manifest without altering an archetype

## Description

`spec_artifacts_process/manifest.yaml` SHALL carry the quoin FR-070 `semantic` block, referencing
every declared artifact type's emitted schema by path and digest (quoin FR-073) at manifest
`version` 0.2.0, so that Quoin verifies the shipped schemas at install and a consumer can resolve
a type's record schema from the manifest alone, while every existing archetype contract keeps the
exact meaning it has today.

## Inputs

- The emitted schemas of [FR-009](./FR-009-emitted-json-schemas.md).
- The module-manifest schema carrying the `semantic` block, as `filament-core-service` FR-035
  defines it and as Quoin and Quire each vendor it.
- The checked-in 0.1.0 baseline of `archetypes`, `artifact_types`, `object_types`, `doc_kinds`,
  `grammars`, `traceability` and `verification_catalog`, which NFR-001 measures against.

## Outputs

- `manifest.yaml` at `version: 0.2.0`, carrying a `semantic` block and a reference-form
  `data_schema` on each of the twelve declared artifact types.
- `scripts/manifest_digests.py`, which rewrites every `data_schema.digest` from the shipped bytes
  of the file its `data_schema.schema` names.

## Behavior

- The `semantic` block SHALL carry exactly these keys and values: `contract_version: 1.0.0`,
  `semantic_core: 0.1.0`, `package: agent-ix/spec-artifacts-process`, `exports` listing every
  artifact type that ships a schema, `imports: {}`, `targets: [json-schema, markdown]`,
  `mappings: [frontmatter, section, table, typed-table, sysml-fence, ocl-clause, list, token, provenance]`,
  `compatibility_posture: additive`, `legacy_forms: warning`.
- `semantic.exports` SHALL name all twelve declared artifact types: `ADR`, `Plan`, `Task`,
  `Review`, `SpecReview`, `Finding`, `Feedback`, `TestMatrixIndex`, `TestMatrix`, `Standard`,
  `SuiteRegistry`, `Inspections`.
- Every declared artifact type SHALL carry `data_schema: { schema: schemas/<Model>.json, digest:
  sha256:<hex> }`, where `<hex>` is the SHA-256 of the shipped file bytes.
- No artifact type SHALL carry an inline `data_schema`.
- The manifest `version` SHALL be `0.2.0`, because the emitted `$id` embeds it and the previous
  value was `0.1.0`; `manifest_version` SHALL stay `1.0.0`, because it names the manifest format
  rather than this module.
- Every `archetypes`, `artifact_types`, `object_types`, `doc_kinds`, `grammars`, `traceability`,
  `lint_rules` and `verification_catalog` declaration present at 0.1.0 SHALL be present at 0.2.0
  with byte-identical content, except for the `data_schema` key this requirement adds and the
  `body_extraction` locators FR-012 adds.
- Every `body_extraction` locator this change adds SHALL be `required: false`, so no document that
  validates at 0.1.0 stops validating at 0.2.0.
- The `Status` column pattern `^(✅|❌|🚧|⛔)(\s+.*)?$` SHALL keep exactly the four markers it
  admits today, and no vocabulary declared in this manifest SHALL be widened or narrowed by this
  change.
- The engine SHALL dispatch a document on frontmatter `type:`, so `type: Standard` resolves to the
  artifact type `Standard` with `Standard.json` as its record schema, while the object type
  `standard` is reached only through `object: standard`.
- This change SHALL NOT alter which of the two declarations a given document resolves to.
- The `traceability.trace_targets` and `document_references` entries bind by archetype name, so
  adding a `data_schema` key to an artifact type changes no binding; the manifest test SHALL
  assert that the trace-target set is byte-identical to the 0.1.0 baseline.
- The `object_types` entry `standard` SHALL keep its inline `data_schema`, because converting it
  to the reference form would change how the engine resolves a declaration a consumer already
  activates against, and the record shape it declares is the frontmatter projection rather than
  the document record `Standard.json` describes.
- The manifest SHALL load through Quire's registry loader with no load failure for any artifact
  type, and every recorded schema digest SHALL equal the SHA-256 of the shipped file.
- `make manifest-digests` SHALL rewrite every `data_schema.digest` from the shipped bytes.
- `make manifest-digests` SHALL change no byte of the manifest outside a `data_schema.digest`
  value.
- If Quoin or Quire rejects the manifest, then this module SHALL correct its own manifest or
  schemas rather than relax a contract key, a digest, an `$id` rule, or an archetype vocabulary
  to make a consumer accept them.
- Measured against quire 0.46.0 the two available refusals are silent: a `semantic` key the loader
  cannot parse drops every declaration of the module, and a `data_schema` digest mismatch drops the
  type alone, and neither names the offending key, path or digest. `agent-ix/quire-rs#221` and
  `agent-ix/quire-rs#394` own those defects; the naming half of FR-010-AC-6 is carried as an
  explicit expected failure rather than dropped.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-010-CON-1 | The `semantic` block SHALL contain no key outside the nine admitted names. | Compatibility | Test |
| FR-010-CON-2 | This change SHALL add no required key, no required section, and no new vocabulary member to any existing archetype. | Compatibility | Test |
| FR-010-CON-3 | `⚠️` SHALL NOT be admitted to the `Status` pattern; it was retired by CR-031 because every row carrying it was exempt from the status-lie check by construction, and the divergent `quoin:spec-matrix` skill is the defect (`agent-ix/quoin#337`). | Compatibility | Test |
| FR-010-CON-4 | The digest rewriter SHALL edit `manifest.yaml` only at `data_schema.digest` values. | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-010-AC-1 | The loaded `semantic` block equals the nine admitted keys with the values above, and `exports` equals the set of `artifact_types[].name` — derived from the manifest, so the count in `spec.md` and the declared type list cannot drift apart. | Test (TC-089) |
| FR-010-AC-2 | For every declared artifact type, `data_schema` is the reference form, the referenced file exists under `schemas/`, and its SHA-256 equals the recorded digest, with no artifact type carrying an inline `data_schema`. | Test (TC-090) |
| FR-010-AC-3 | Every 0.1.0 declaration, compared against the checked-in 0.1.0 baseline of the manifest, is present unchanged apart from the added `data_schema` keys and the added `required: false` locators. | Test (TC-091) |
| FR-010-AC-4 | The `Status`, `Type`, `Priority`, `Traces To`, `Severity`, `Escape Cause`, `Evidence Kind` and `Verdict` vocabularies are byte-identical to the 0.1.0 baseline. | Test (TC-092) |
| FR-010-AC-5 | `quire.Registry.load_from` over the module directory lists every declared archetype and reports no load failure. | Test (TC-093) |
| FR-010-AC-6 | A manifest copy whose `semantic` block gains a key `foo` is refused by the loader, and a copy whose `data_schema.digest` is altered is refused — the refusal happens in both cases. | Test (TC-094) |
| FR-010-AC-7 | `make manifest-digests` on the committed tree rewrites no byte, and after one schema is regenerated it rewrites exactly that type's digest and nothing else. | Test (TC-095) |
| FR-010-AC-8 | The `object_types` entry `standard` still carries its inline `data_schema` with the same properties and `required` list as at 0.1.0, the artifact type `Standard` carries the reference form, and a document is dispatched on frontmatter `type:` to the first and on `object:` to the second. | Test (TC-096) |
| FR-010-AC-9 | The refusal of an unknown `semantic` key names the key, and the refusal of a mismatched digest names the path. Measured against quire 0.46.0 both refusals are silent, so this criterion is a **strict expected failure** naming `agent-ix/quire-rs#221` and `agent-ix/quire-rs#394`: the test asserts the current silence and turns red the day the engine starts naming them. It is never skipped — a skipped row is not coverage. | Test (TC-135) |
| FR-010-AC-10 | `traceability.trace_targets` and `document_references` are byte-identical to the 0.1.0 baseline. | Test (TC-136) |

## Dependencies

- **Upstream**: [FR-009](./FR-009-emitted-json-schemas.md); quoin FR-070/FR-073 (`ix://agent-ix/quoin/FR-070`, `ix://agent-ix/quoin/FR-073`); quire-rs FR-069 (`ix://agent-ix/quire-rs/FR-069`)
- **Downstream**: [FR-011](./FR-011-markdown-record-mapping.md), [FR-012](./FR-012-executable-skeletons.md), [NFR-001](../non-functional/NFR-001-additive-compatibility.md)
