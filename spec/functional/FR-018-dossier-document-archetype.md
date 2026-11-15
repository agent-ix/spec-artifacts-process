---
id: FR-018
title: "DossierDocument archetype for generated submission-dossier documents"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-012"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-188"
    type: "references"
---
# FR-018: DossierDocument archetype for generated submission-dossier documents

## Description

`quoin dossier` ([quoin FR-188](ix://agent-ix/quoin/FR-188)) writes Markdown documents (a software
requirements specification, an architecture document, a trace matrix and a requirements mapping matrix)
into a repository, and `quire export` renders them. Both need a document type that validates, so this
module SHALL declare the artifact type `DossierDocument`.

The `DossierDocument` archetype SHALL carry the identity `quire export` reads from the committed blob
(`title`, `id`, `version`; quire-cli FR-034). The body is free Markdown. The archetype records no digest
and no source hash: the commit holding the file is its identity.

## Inputs

- A Markdown file with `type: DossierDocument`.

## Outputs

- Frontmatter members: `id` (for example `DOS-SRS`), `title`, `version`, `type: DossierDocument`,
  `document_kind`, `generated_by` and, optionally, `as_of`.

## Behavior

- The `DossierDocument` frontmatter schema SHALL require `id`, `title`, `version`, `document_kind` and `generated_by`.
- The `DossierDocument` frontmatter schema SHALL accept only non-empty text for `version`, because `quire export` needs a version or a release.
- The `DossierDocument` frontmatter schema SHALL accept only `srs`, `architecture`, `trace-matrix` or `rmm` for `document_kind`.
- The `DossierDocument` frontmatter schema SHALL accept only `quoin dossier` for `generated_by`.
- The `DossierDocument` frontmatter schema SHALL treat `as_of` as optional text holding an ISO-8601 instant, present only where the source needs one.
- The archetype SHALL declare no digest, hash or source-revision member.
- The archetype SHALL declare a skeleton and a mapped record schema, like every artifact type (FR-012).

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-018-AC-1 | A fixture carrying `id`, `title`, `version`, `type`, `document_kind`, `generated_by` and `as_of` validates with `quire validate`, and the same fixture without `as_of` validates. | Test |
| FR-018-AC-2 | A fixture with no `version` fails `quire validate`, with a diagnostic naming `version`. | Test |
| FR-018-AC-3 | A fixture with `document_kind: verification-report` fails `quire validate`, with a diagnostic naming `document_kind`. | Test |
| FR-018-AC-4 | A fixture with `generated_by: hand` fails `quire validate`, and a fixture with no `generated_by` fails. | Test |
| FR-018-AC-5 | The `DossierDocument` frontmatter schema and mapped record schema declare no member named like a digest, hash or revision. | Inspection |
| FR-018-AC-6 | The skeleton `DossierDocument.md` validates, and `DossierDocument` carries the role `definition` in `mappings.yaml`. | Test |

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md), [FR-012](./FR-012-executable-skeletons.md)
- **Downstream**: quoin [FR-188](ix://agent-ix/quoin/FR-188)
