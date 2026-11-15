---
id: SR-20261115175451
title: "PLAT-1436 PR155 spec-review base"
type: SpecReview
analysis: base
scope: "agent-ix/spec-artifacts-process PR155; spec/functional/FR-018-dossier-document-archetype.md, spec/functional/index.md, spec/spec.md"
review_set: base
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-018", type: references}
---

## Summary

Ticket: PLAT-1436. Base review of FR-018 against the ticket's FR-F draft and Design note 3. FR-018 covers all three draft ACs (all members validate, missing `version` fails, out-of-enum `document_kind` fails) and adds `generated_by`, no-digest and skeleton/role criteria. Every AC is phrased so a test can fail it. The index entry was added. The spec names no paywalled standard text; it names the ISO 8601 date format only as an identifier. `quire validate` with the installed modules accepts FR-018 and the index.

## Verdict

**CONDITIONAL.** The requirement is sound and complete for its scope. The module scope statement in spec.md was not updated, and one schema constraint is not specified.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | spec/spec.md scope still says 6 process archetypes and 13 artifact types and does not list `DossierDocument` or FR-018; the manifest now declares 7 and 14. | spec/spec.md:29-31 |
| FND-002 | low | The frontmatter schema enforces `id` pattern `^DOS-[A-Z0-9]+(-[A-Z0-9]+)*$`, but FR-018 states no constraint on `id`; the schema goes beyond the requirement. | spec_artifacts_process/schemas/dossier-document-frontmatter.schema.json:7-10 |

## Examined scope

```yaml
scope:
  - {id: FR-018, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "`quoin dossier` writes Markdown documents ... into a repository, and `quire export` renders them. Both need a document type that validates, so this module SHALL declare the artifact type `DossierDocument`."}
  - {id: FR-018-AC-1, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "A fixture carrying `id`, `title`, `version`, `type`, `document_kind`, `generated_by` and `as_of` validates with `quire validate`, and the same fixture without `as_of` validates."}
  - {id: FR-018-AC-2, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "A fixture with no `version` fails `quire validate`, with a diagnostic naming `version`."}
  - {id: FR-018-AC-3, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "A fixture with `document_kind: verification-report` fails `quire validate`, with a diagnostic naming `document_kind`."}
  - {id: FR-018-AC-4, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "A fixture with `generated_by: hand` fails `quire validate`, and a fixture with no `generated_by` fails."}
  - {id: FR-018-AC-5, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` frontmatter schema and mapped record schema declare no member named like a digest, hash or revision."}
  - {id: FR-018-AC-6, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The skeleton `DossierDocument.md` validates, and `DossierDocument` carries the role `definition` in `mappings.yaml`."}
  - {id: spec.md-scope, path: "spec/spec.md", role: examined, excerpt: "The Module manifest and the contributions it declares: 6 process archetypes (adr, plan, review, spec-review, test-matrix, standard), 1 grammar (process-artifacts), and the 13 artifact types the manifest declares"}
```
