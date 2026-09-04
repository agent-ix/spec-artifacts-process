---
id: FR-012
title: "Executable typed skeletons and negative counterparts for every declared artifact type"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-002"
    type: "implements"
  - target: "ix://agent-ix/spec-artifacts-process/FR-011"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-074"
    type: "depends_on"
---
# FR-012: Executable typed skeletons and negative counterparts for every declared artifact type

## Description

The module SHALL ship one authoring skeleton per declared artifact type, each of which is a
document its own archetype validates and whose mapped record validates against its emitted
schema, together with a negative counterpart fixture for each rejection the type's contract
states, so that a skeleton is an executable fixture rather than an example nothing checks.

## Inputs

- The emitted schemas of [FR-009](./FR-009-emitted-json-schemas.md) and the mapping of
  [FR-011](./FR-011-markdown-record-mapping.md).
- The four skeletons the module ships today — `SpecReview.md`, `Feedback.md`, `SuiteRegistry.md`,
  `Inspections.md` — which are the baseline this requirement extends rather than replaces.
- The `body_extraction` locators of each artifact type, which fix the required sections and the
  asserted table shapes a skeleton must satisfy.

## Outputs

- `spec_artifacts_process/skeletons/<Type>.md` for all twelve declared artifact types.
- `spec_artifacts_process/skeletons/Standard.sysml.md`, the alternate `sysml` form of the same
  declarations the `Standard.md` typed `## Properties` table carries.
- `tests/fixtures/negative/<case>.md`, one per stated rejection, each carrying `expect:` and
  `because:` frontmatter naming the rule it violates.
- The manifest's `Standard` archetype extended with two `required: false` locators — `properties`
  (the typed declaration section) and `invariants` (its `ocl` clauses).

## Behavior

- Every declared artifact type SHALL have exactly one skeleton at
  `spec_artifacts_process/skeletons/<Type>.md`.
- Every skeleton SHALL carry frontmatter its type's `frontmatter_schema_ref` accepts, including a
  `type:` equal to the artifact type name.
- Every skeleton SHALL carry every section its type's `body_extraction` marks `required: true`,
  and every asserted table in the skeleton SHALL satisfy that locator's `columns`, `min_rows`,
  `id_pattern`, `column_choices` and `column_patterns`.
- Every skeleton SHALL validate through `quire validate` against this module's own manifest with
  zero error findings.
- The record the FR-011 mapping builds from every skeleton SHALL validate against that type's
  emitted schema.
- The typed declaration form SHALL be shown on `Standard` and on no other type: a Standard
  declares the properties a conforming artifact carries and the invariants conformance requires,
  and the other eleven types declare process content rather than a typed structure. Introducing a
  `## Properties` section on a type whose documents do not carry one would be a new required form
  for every consuming repository, which NFR-001 forbids.
- The `Standard.md` skeleton SHALL carry a `## Properties` section whose table headers are exactly
  `Field | Type | Multiplicity | Constraints` with at least one data row, and an `## Invariants`
  section carrying at least one `### <clauseId>` subsection holding exactly one ```` ```ocl ````
  fence.
- `Standard.sysml.md` SHALL declare exactly the same fields as `Standard.md` in one ```` ```sysml ````
  fence under `## Properties`, and SHALL carry the same `## Invariants` clauses.
- Both `Standard` skeletons SHALL map to records that differ in no property, because the two forms
  are the same declarations.
- The `properties` and `invariants` locators added to the `Standard` archetype SHALL be
  `required: false`, so every Standard document that validates today keeps validating.
- Every negative fixture SHALL carry frontmatter `expect:` naming the rejection class and
  `because:` naming the rule, and SHALL fail exactly the check its `expect:` names.
- The negative set SHALL cover, at minimum: a missing required section; a required table with zero
  data rows; a row id outside the declared `id_pattern`; a cell outside a declared
  `column_choices`; a `Status` cell outside the four-marker pattern; a `Traces To` cell the pattern
  rejects; a dropped required column; a duplicate row id; a `Standard` carrying both the typed
  table and the `sysml` fence; a `Standard` clause subsection with no fence; and a `Standard`
  clause id that is not an `Identifier`.
- No negative fixture SHALL live under `spec/`.
- The trace-target `exclude` globs SHALL keep covering `tests/**`, so no fixture mints an id in
  this repository or a consuming one.
- If a skeleton stops validating or its record stops matching its schema, then the suite SHALL
  fail rather than skip, because a skeleton every author copies is the module's most-used
  document.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-012-CON-1 | A skeleton SHALL contain no placeholder that its own archetype rejects; the shipped bytes are the fixture. | Integrity | Test |
| FR-012-CON-2 | Adding a skeleton SHALL NOT add a required section, a required column, or a vocabulary member to any archetype. | Compatibility | Test |
| FR-012-CON-3 | Negative fixtures SHALL live under `tests/fixtures/negative/` only, never in the shipped payload. | Packaging | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-012-AC-1 | `spec_artifacts_process/skeletons/` holds exactly one `<Type>.md` for each of the twelve declared artifact types, plus `Standard.sysml.md`. | Test (TC-111) |
| FR-012-AC-2 | Every skeleton validates against its own archetype through Quire with zero error findings. | Test (TC-112) |
| FR-012-AC-3 | For every skeleton, the FR-011 reference mapping builds a record that validates against that type's emitted schema. | Test (TC-113) |
| FR-012-AC-4 | Every section each type's `body_extraction` marks required is present in that type's skeleton, and every asserted table in a skeleton satisfies its locator's asserts. | Test (TC-114) |
| FR-012-AC-5 | `Standard.md` carries the typed `## Properties` table and at least one `ocl` clause; `Standard.sysml.md` declares the same fields in one `sysml` fence, and the two map to records that differ in no property. | Test (TC-115) |
| FR-012-AC-6 | The `Standard` archetype's added `properties` and `invariants` locators are both `required: false`, and a Standard document carrying neither section still validates. | Test (TC-116) |
| FR-012-AC-7 | Every negative fixture fails exactly the check its `expect:` frontmatter names, and no negative fixture passes. | Test (TC-117) |
| FR-012-AC-8 | The negative set covers each of the eleven stated rejections, one fixture per rejection. | Test (TC-118) |
| FR-012-AC-9 | No file under `tests/fixtures/` is in the wheel, the sdist, or the staged npm tree, and `quire coverage` mints no id from it. | Test (TC-119) |

## Dependencies

- **Upstream**: [FR-011](./FR-011-markdown-record-mapping.md); quoin FR-074 (`ix://agent-ix/quoin/FR-074`)
- **Downstream**: [NFR-001](../non-functional/NFR-001-additive-compatibility.md)
