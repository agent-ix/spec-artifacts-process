---
id: SR-20261115175453
title: "PLAT-1436 PR155 spec-review integrity"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-artifacts-process PR155; spec/functional/FR-018-dossier-document-archetype.md, spec_artifacts_process/mappings.yaml, spec_artifacts_process/schemas/DossierDocument.json, spec_artifacts_process/schemas/Provenance.json"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-018", type: references}
  - {target: "ix://agent-ix/spec-artifacts-process/FR-011", type: references}
---

## Summary

Ticket: PLAT-1436. Checked FR-018 for consistency with the artifacts that implement it and with FR-011. The frontmatter schema, the record schema and the manifest locators agree on the required members and the vocabularies. They contradict FR-018's own no-digest statement: `mappings.yaml` gives `DossierDocument` the shared `provenance: {kind: provenance, required: true}` entry, and `DossierDocument.json` requires `provenance`. `Provenance.json` requires `digest` (SHA-256 over the document bytes, FR-011). Every mapped `DossierDocument` record therefore carries a digest, even though FR-018, the mapping note, the skeleton comment and the schema description all say none is recorded.

## Verdict

**FAIL.** FR-018's central constraint is false for the mapped record (FND-001).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-018 says the archetype records no digest and declares no digest member, but the record schema requires `provenance`, whose schema requires `digest` (SHA-256, FR-011). | spec_artifacts_process/schemas/DossierDocument.json:40-42 |

## Examined scope

```yaml
scope:
  - {id: FR-018-B-6, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The archetype SHALL declare no digest, hash or source-revision member."}
  - {id: FR-018-AC-5, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` frontmatter schema and mapped record schema declare no member named like a digest, hash or revision."}
  - {id: FR-018-B-1, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` frontmatter schema SHALL require `id`, `title`, `version`, `document_kind` and `generated_by`."}
  - {id: FR-018-B-3, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` frontmatter schema SHALL accept only `srs`, `architecture`, `trace-matrix` or `rmm` for `document_kind`."}
  - {id: Provenance.json, path: "spec_artifacts_process/schemas/Provenance.json", role: context_only, excerpt: "\"digest\": {... \"description\": \"SHA-256 over the line-ending-normalised document bytes (FR-011).\"}, \"required\": [\"path\", \"digest\"]"}
```
