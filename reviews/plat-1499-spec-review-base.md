---
id: SR-20261113075805
title: "PLAT-1499 spec-artifacts-process PR144 spec-review base"
type: SpecReview
analysis: base
scope: "agent-ix/spec-artifacts-process PR144 @b782a70 over origin/main; spec/functional/FR-003-testmatrix-body-extraction.md, spec/functional/FR-004-traceability-declaration.md, spec/tests.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-003"
    type: references
---

## Summary

Ticket: PLAT-1499. Base checklist review of the spec-only PR that drops the
hand-kept `Functional Requirement Coverage` table from the `TestMatrix`
archetype and makes `quire matrix` the single source of functional coverage.
Review set: base + integrity + ears-conformance. No AssuranceProfile exists in
this repository, so no enforced spec-review run applies.

The decision itself is sound. Dropping the table, rather than generating it,
removes a second committed copy of what `quire matrix` already computes on
demand. It adds no generator, no freshness check and no compatibility layer.
`quire matrix --scope . --module spec_artifacts_process` was run on the PR head.
It renders FR and NFR criteria with their binders, so the dropped table loses
nothing that is not computed.

The legacy `### Functional Requirement Coverage` section still in
`spec/tests.md` (lines 23-183) is justified until the implementation PR lands.
The unchanged manifest declares `functional_coverage` as `required: true,
min_rows: 1`, so deleting it in a spec-only PR would turn `quire validate` red
on this repository. It expires with the PLAT-1499 implementation PR, which
deletes it in the same change as the manifest entry. It must not be maintained
meanwhile. It is already stale: its FR-003-AC-1 row still lists TC-003, and it
has no AC-13/AC-14 rows. That staleness is the PR's own argument and is not a
finding.

## Verdict

**FAIL / CHANGES REQUESTED.** FND-001 is a tracking-record antipattern the PR
itself names and leaves for "the owner to decide". The owner's rule is that a
found antipattern is fixed, not noted as out of scope. The optional
Stakeholder, User Story and Non-Functional coverage tables should be dropped in
this same PR. FND-003 lists what the implementation-pass and downstream lists
are missing. FND-002 is the same pattern in `TestMatrixIndex`, at lower
confidence.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-003 still requires the optional `Stakeholder Requirement Coverage`, `User Story Coverage` and `Non-Functional Requirement Coverage` tables to be declared as extractions, and the skeleton and spec-matrix template emit them. Each is a hand-kept rollup with a hand-set `Status`. NFR criteria are already rendered by `quire matrix`. StR-to-US/FR edges live in the documents' `relationships:`, and StR VCs are minted ids. US links are already in each TC row's `Traces To` cell. This is the same antipattern as the dropped table, and the PR flags it and defers it. Drop all three in this PR: make the bullet SHALL NOT, reword FR-003-AC-7, rewrite TC-014/TC-015, delete this repository's StR and US tables, and add the manifest, skeleton, semantic, mappings, schema and fixture removals to the implementation list. | spec/functional/FR-003-testmatrix-body-extraction.md:111-121 |
| FND-002 | medium | The `TestMatrixIndex` `Requirements Traceability` table (FR-003-AC-12; `Subsystem \| Requirements \| Local Matrix \| Status`) is required, and its `Requirements` and `Status` columns are a hand rollup of what the leaf matrices and `quire matrix` already compute. Only `Local Matrix` is navigation, and archetype binding (CR-062) already reaches nested matrices without it. Decide in this PR whether the index keeps only navigation or is dropped too. Do not leave it unexamined beside FND-001. | spec/functional/FR-003-testmatrix-body-extraction.md:194 |
| FND-003 | medium | The implementation-pass list in the PR description is incomplete. It omits the manifest `document_references` entry `functional-coverage` (manifest.yaml:1156-1165), which reads the dropped section, and its CR-062 comment (manifest.yaml:856). It omits `examples/TestMatrix.record.json` (`functionalCoverage`, loaded by tests/test_markdown_mappings.py), the `test_traceability_declaration.py:232` expected kind list, and the `missing-fr-coverage.md` fixture. The downstream list omits quoin's `skills/spec-matrix/assets/test-matrix-template.md` and `test-matrix-example.md` and the `templates/semantic-module` cookiecutter `spec/matrix.md`. Those will keep generating the dropped table into new matrices. | spec_artifacts_process/manifest.yaml:1156 |

## Examined scope

```yaml
scope:
- id: FR-003
  path: spec/functional/FR-003-testmatrix-body-extraction.md
  role: examined
  excerpt: "`body_extraction` **SHALL NOT** declare a `Functional Requirement Coverage` extraction, required or optional."
- id: FR-003-AC-1
  path: spec/functional/FR-003-testmatrix-body-extraction.md
  role: examined
  excerpt: "A `TestMatrix` doc with a conforming `Test Case Summary` validates"
- id: FR-003-AC-7
  path: spec/functional/FR-003-testmatrix-body-extraction.md
  role: context_only
  excerpt: "optional StR/US/NFR coverage extractions"
- id: FR-003-AC-12
  path: spec/functional/FR-003-testmatrix-body-extraction.md
  role: examined
  excerpt: "A `TestMatrixIndex` archetype models the root index of a matrix tree: it requires a `Requirements Traceability` table of `Subsystem | Requirements | Local Matrix | Status` ..."
- id: FR-003-AC-13
  path: spec/functional/FR-003-testmatrix-body-extraction.md
  role: examined
  excerpt: "A `TestMatrix` doc with a `Test Case Summary` and no `Functional Requirement Coverage` section validates"
- id: FR-003-AC-14
  path: spec/functional/FR-003-testmatrix-body-extraction.md
  role: examined
  excerpt: "The shipped `TestMatrix` skeleton emits no `Functional Requirement Coverage` section, and its authoring comment states that requirement-to-criterion coverage is read from `quire matrix`, never authored"
- id: FR-004
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: "each binds to its TC row by the TC row's own `Traces To` cell, which is a different column and is not affected."
- id: TM-001
  path: spec/tests.md
  role: examined
  excerpt: "TC-003, TC-194, TC-076 rows; edge-case row; retained Functional Requirement Coverage section (lines 23-183)"
```
