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
every declared artifact type's emitted schema by path (quoin FR-073), so that Quoin verifies the shipped schemas at install and a consumer can resolve
a type's record schema from the manifest alone, while every existing archetype contract keeps the
exact meaning it has today.

## Inputs

- The emitted schemas of [FR-009](./FR-009-emitted-json-schemas.md).
- The module-manifest schema carrying the `semantic` block, as `filament-core-service` FR-035
  defines it and as Quoin and Quire each vendor it.

## Outputs

- `manifest.yaml` carrying a `semantic` block and a reference-form
  `data_schema` on each of the twelve declared artifact types.

## Behavior

- The `semantic` block SHALL carry exactly these keys and values: `contract_version: 1.0.0`,
  `semantic_core` (the declared semantic-core pin), `package: agent-ix/spec-artifacts-process`, `exports` listing every
  artifact type that ships a schema, `imports: {}`, `targets: [json-schema, markdown]`,
  `mappings: [frontmatter, section, table, typed-table, sysml-fence, ocl-clause, list, token, provenance]`,
  `compatibility_posture: additive`, `legacy_forms: warning`.
- `semantic.exports` SHALL name all twelve declared artifact types: `ADR`, `Plan`, `Task`,
  `Review`, `SpecReview`, `Finding`, `Feedback`, `TestMatrixIndex`, `TestMatrix`, `Standard`,
  `SuiteRegistry`, `Inspections`.
- Every declared artifact type SHALL carry `data_schema: { schema: schemas/<Model>.json }`.
- No artifact type SHALL carry an inline `data_schema`.
- `manifest_version` SHALL stay `1.0.0`, because it names the manifest format
  rather than this module.
- The `Status` column pattern `^(✅|❌|🚧|⛔)(\s+.*)?$` SHALL admit exactly the four markers it names.
- The engine SHALL dispatch a document on frontmatter `type:`, so `type: Standard` resolves to the
  artifact type `Standard` with `Standard.json` as its record schema, while the object type
  `standard` is reached only through `object: standard`.
- This change SHALL NOT alter which of the two declarations a given document resolves to.
- The `object_types` entry `standard` SHALL keep its inline `data_schema`, because converting it
  to the reference form would change how the engine resolves a declaration a consumer already
  activates against, and the record shape it declares is the frontmatter projection rather than
  the document record `Standard.json` describes.
- The manifest SHALL load through Quire's registry loader with no load failure for any artifact
  type.
- If Quoin or Quire rejects the manifest, then this module SHALL correct its own manifest or
  schemas rather than relax a contract key, an `$id` rule, or an archetype vocabulary
  to make a consumer accept them.
- The two available refusals are silent: a `semantic` key the loader
  cannot parse drops every declaration of the module. `agent-ix/quire-rs#221` owns that defect; the naming half of FR-010-AC-6 is carried as an
  explicit expected failure rather than dropped.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-010-CON-1 | The `semantic` block SHALL contain no key outside the nine admitted names. | Compatibility | Test |
| FR-010-CON-3 | `⚠️` SHALL NOT be admitted to the `Status` pattern; it was retired by CR-031 because every row carrying it was exempt from the status-lie check by construction, and the divergent `quoin:spec-matrix` skill is the defect (`agent-ix/quoin#337`). | Compatibility | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-010-AC-1 | The loaded `semantic` block equals the nine admitted keys with the values above, and `exports` equals the set of `artifact_types[].name` — derived from the manifest, so the count in `spec.md` and the declared type list cannot drift apart. | Test (TC-089) |
| FR-010-AC-5 | `quire.Registry.load_from` over the module directory lists every declared archetype and reports no load failure. | Test (TC-093) |
| FR-010-AC-6 | A manifest copy whose `semantic` block gains a key `foo` is refused by the loader. | Test (TC-094) |
| FR-010-AC-8 | The `object_types` entry `standard` still carries its inline `data_schema`, the artifact type `Standard` carries the reference form, and a document is dispatched on frontmatter `type:` to the first and on `object:` to the second. | Test (TC-096) |
| FR-010-AC-9 | The refusal of an unknown `semantic` key names the key. Both refusals are silent, so this criterion is a **strict expected failure** naming `agent-ix/quire-rs#221`: the test asserts the current silence and turns red the day the engine starts naming them. It is never skipped — a skipped row is not coverage. | Test (TC-135) |

## Dependencies

- **Upstream**: [FR-009](./FR-009-emitted-json-schemas.md); quoin FR-070/FR-073 (`ix://agent-ix/quoin/FR-070`, `ix://agent-ix/quoin/FR-073`); quire-rs FR-069 (`ix://agent-ix/quire-rs/FR-069`)
- **Downstream**: [FR-011](./FR-011-markdown-record-mapping.md), [FR-012](./FR-012-executable-skeletons.md)
