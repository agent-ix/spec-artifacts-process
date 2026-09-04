---
id: FR-009
title: "Emit one JSON Schema per declared process artifact type from a TypeSpec source"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-002"
    type: "implements"
  - target: "ix://agent-ix/filament-core-data/FR-033"
    type: "depends_on"
  - target: "ix://agent-ix/filament-core-data/FR-034"
    type: "depends_on"
---
# FR-009: Emit one JSON Schema per declared process artifact type from a TypeSpec source

## Description

The module build SHALL emit one JSON Schema 2020-12 document per declared process artifact type
from a TypeSpec source that imports `@agent-ix/semantic-core` 0.1.0, using the official
`@typespec/json-schema` emitter at a pinned toolchain, into
`spec_artifacts_process/schemas/`, so that the shipped schema is the compiled one and any drift
between the source and the shipped bytes fails the build.

## Inputs

- `spec_artifacts_process/semantic/main.tsp`: namespace `AgentIx.SpecArtifactsProcess`, decorated
  `@jsonSchema("https://schemas.agent-ix.org/agent-ix/spec-artifacts-process/<version>/")` where
  `<version>` is the manifest `version`.
- `@agent-ix/semantic-core` 0.1.0, resolved from the scope-routed registry through the user-level
  npm config, supplying `ClauseRef`, `FieldDecl`, `TypeRef`, `Multiplicity`, `ConstraintDecl`,
  `Identifier` and `SemanticId`.
- `@typespec/compiler` 1.15.0 and `@typespec/json-schema` 1.15.0 as exact `devDependencies` of
  `spec_artifacts_process/semantic/package.json`, resolved through its committed
  `package-lock.json`.
- `spec_artifacts_process/semantic/scripts/generate.mjs`, Node built-ins only.
- Node 20 or later, the runtime `@typespec/compiler` 1.15.0 requires.

## Outputs

- `spec_artifacts_process/schemas/<Model>.json`, one per model of the module namespace, rendered
  as two-space JSON with one trailing newline.
- `spec_artifacts_process/semantic/generated/toolchain.json`, recording the compiler and emitter
  names and versions, the resolved `@agent-ix/semantic-core` version and the SHA-256 of that
  package's own `generated/toolchain.json`, the `$id` base, the manifest version, the excluded
  imported files, the emitted file list, the normalization record, and `sha256:<hex>` over the
  emitted files.

## Behavior

- If `node` is absent, is older than 20, or `spec_artifacts_process/semantic/node_modules` does not
  hold the pinned compiler, emitter and `@agent-ix/semantic-core`, then the generator SHALL exit
  non-zero naming the missing component and the command that installs it
  (`make semantic-install`), rather than failing inside the compiler.
- If the resolved `@agent-ix/semantic-core` version differs from the manifest's
  `semantic.semantic_core`, then the generator SHALL exit non-zero naming both values, so the
  declared grammar version and the compiled-against grammar version cannot diverge.
- `make schemas` SHALL run the generator.
- `make schemas-check` SHALL run the generator with `--check`.
- The generator SHALL compile `spec_artifacts_process/semantic/` with `tsp compile` into a
  temporary directory.
- If `tsp compile` fails, then the generator SHALL write no file under
  `spec_artifacts_process/schemas/`.
- The generator SHALL keep only the emitted files whose `$id` starts with the module base.
- The generator SHALL record every file it discarded because that file's `$id` starts with
  `https://schemas.agent-ix.org/semantic-core/`.
- If the emitter writes any entry that is not a top-level `*.json` file, then the generator SHALL
  exit non-zero naming that entry rather than bundling a subset.
- If the emitter leaves any `$id` relative, then the generator SHALL rewrite that `$id` to
  `<base><file>` and record the file in `toolchain.json`.
- Where no `$id` is relative, the generator SHALL record the normalization as `applied: false`.
- If the `@jsonSchema` base in `main.tsp` differs from the manifest `version`, then the generator SHALL exit non-zero naming both values.
- Every emitted schema SHALL declare `$schema: https://json-schema.org/draft/2020-12/schema` and
  `$id: https://schemas.agent-ix.org/agent-ix/spec-artifacts-process/<manifest version>/<Model>.json`
  matching its file name.
- Every `$ref` in an emitted schema SHALL name either a sibling schema that ships under
  `spec_artifacts_process/schemas/`, or a `https://schemas.agent-ix.org/semantic-core/0.1.0/` model.
- The module SHALL emit one exported model for each of the twelve declared artifact types — `ADR`,
  `Plan`, `Task`, `Review`, `SpecReview`, `Finding`, `Feedback`, `TestMatrixIndex`, `TestMatrix`,
  `Standard`, `SuiteRegistry`, `Inspections` — and SHALL emit no artifact model for a type the
  manifest does not declare.
- In `--check` mode the generator SHALL write no file anywhere in the repository.
- If any emitted file differs from the committed output, a committed projection under
  `spec_artifacts_process/schemas/` has no emitted counterpart in this run, or
  `generated/toolchain.json` differs, then the check SHALL exit non-zero naming each such file;
  otherwise it SHALL exit zero.
- The generator SHALL treat a file named `*-frontmatter.schema.json` as hand-authored, neither
  emitting, deleting, nor reporting it, because the frontmatter schemas predate this projection
  and are referenced by `frontmatter_schema_ref`.
- `make lint` SHALL run `make schemas-check`, so a `main.tsp` edit that was never regenerated
  fails before push rather than at review.
- The repository SHALL run `make schemas-check` as a local pre-push gate only, never as a
  GitHub-workflow gate, because `@agent-ix/semantic-core` resolves solely through a scope-routed
  registry the workflow does not reach (`agent-ix/filament-core-data#11`). A CI job asserting it
  would fail for a reason that is not a defect in this module, and the pre-push `make lint` is
  where it holds.
- If the schemas and the digests agree with each other but carry a version segment other than the
  manifest's current `version`, then the check SHALL exit non-zero, so a half-completed version
  bump cannot pass by being internally consistent.
- The Python package SHALL include `spec_artifacts_process/schemas/*.json` in the wheel and sdist.
- The repository SHALL mark every file `eol=lf` in `.gitattributes`, so a checkout with
  `autocrlf` cannot change the digested bytes.
- `scripts/stage-npm.mjs` SHALL stage `schemas/` beside `manifest.yaml` at pack time, so a
  manifest-relative `schema:` path resolves inside the npm tarball.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-009-CON-1 | The build SHALL use the official `@typespec/json-schema` emitter only; no custom emitter and no hand-edited emitted file. | Architecture | Inspection |
| FR-009-CON-2 | The repository SHALL carry no `.npmrc`, no `file:` or `link:` dependency, and no version bound on the TypeSpec toolchain beyond the exact pin. | Packaging | Inspection |
| FR-009-CON-3 | Emission SHALL be deterministic: two runs over one source tree produce byte-identical files. | Integrity | Test |
| FR-009-CON-4 | The `$id` base SHALL embed the manifest `version`, bumped as one atomic regeneration — source base, manifest version, schemas, `data_schema` digests and `toolchain.json` in one commit. | Compatibility | Test |
| FR-009-CON-5 | Each test and fixture SHALL read the version segment of the `$id` base from the manifest `version` rather than hard-coding it. | Maintainability | Test |
| FR-009-CON-6 | Every test asserting a property of "every" member of a set SHALL enumerate that set from the manifest or the emitted bundle, never from a list written into the test, so a type added later is covered without editing the test. | Maintainability | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-009-AC-1 | After `make schemas`, `spec_artifacts_process/schemas/` holds exactly the projections `generated/toolchain.json` lists, including one model per declared artifact type, with compiler 1.15.0 and emitter 1.15.0 recorded. | Test (TC-080) |
| FR-009-AC-2 | Every shipped projection declares the 2020-12 `$schema` and an `$id` of `https://schemas.agent-ix.org/agent-ix/spec-artifacts-process/<manifest version>/<Model>.json` matching its file name, with the version segment read from `manifest.yaml` rather than hard-coded. | Test (TC-081) |
| FR-009-AC-3 | Every `$ref` across the shipped projections resolves to a shipped sibling or to a semantic-core `0.1.0` model; a `$ref` to any other host or version is absent. | Test (TC-082) |
| FR-009-AC-4 | `make schemas-check` on the committed tree exits zero; after one byte of any shipped projection is changed it exits non-zero naming that file and writes nothing. | Test (TC-083) |
| FR-009-AC-5 | A `@jsonSchema` base whose version segment differs from the manifest `version` makes the generator exit non-zero naming both values. | Test (TC-084) |
| FR-009-AC-6 | `make schemas-check` on a tree carrying an extra `spec_artifacts_process/schemas/Stale.json` exits non-zero naming that file, while the hand-authored `*-frontmatter.schema.json` files are neither reported nor removed. | Test (TC-085) |
| FR-009-AC-7 | The wheel built by `make build` contains `spec_artifacts_process/schemas/<Model>.json` for every exported model, and the tree `scripts/stage-npm.mjs` stages carries `manifest.yaml` with a sibling `schemas/` holding the same set. | Test (TC-086) |
| FR-009-AC-8 | Running the generator twice over one tree produces byte-identical files and an identical `toolchain.json` digest. | Test (TC-087) |
| FR-009-AC-9 | `generated/toolchain.json` records the resolved `@agent-ix/semantic-core` version and the SHA-256 of that package's own `generated/toolchain.json`, so the compiled-against copy is identified by bytes rather than by a version string. | Test (TC-088) |
| FR-009-AC-10 | With the toolchain uninstalled, the generator exits non-zero naming the missing component and `make semantic-install`, and does not fail inside the compiler. | Test (TC-132) |
| FR-009-AC-11 | A resolved `@agent-ix/semantic-core` version differing from `semantic.semantic_core` makes the generator exit non-zero naming both values. | Test (TC-133) |
| FR-009-AC-12 | A tree whose schemas and digests agree with each other but were generated against a different manifest `version` fails `make schemas-check`. | Test (TC-134) |
| FR-009-AC-13 | Every test in the suite that asserts a property of all declared types derives the type list from `manifest.yaml` or from the emitted bundle; none carries a hard-coded list. | Inspection |

## Dependencies

- **Upstream**: [US-002](../usecase/US-002-declare-process-artifacts-against-semantic-core.md); semantic-core FR-033/FR-034 (`ix://agent-ix/filament-core-data/FR-033`); the generator pattern shipped by `spec-artifacts-iso` FR-005
- **Downstream**: [FR-010](./FR-010-semantic-manifest-contract.md), [FR-011](./FR-011-markdown-record-mapping.md), [FR-012](./FR-012-executable-skeletons.md), [FR-013](./FR-013-definitions-not-occurrences.md)
