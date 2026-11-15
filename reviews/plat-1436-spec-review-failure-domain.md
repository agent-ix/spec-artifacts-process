---
id: SR-20261115175455
title: "PLAT-1436 PR155 spec-review failure-domain"
type: SpecReview
analysis: failure-domain
scope: "agent-ix/spec-artifacts-process PR155; spec/functional/FR-018-dossier-document-archetype.md, spec_artifacts_process/schemas/dossier-document-frontmatter.schema.json, spec_artifacts_process/manifest.yaml"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-018", type: references}
---

## Summary

Ticket: PLAT-1436. Looked for unstated failure modes and identity confusion in the archetype. Missing and empty members and out-of-vocabulary values are all rejected. The schema is pure (no wall clock, no default values). The remaining gaps are combinations that validate but are wrong for the downstream consumers (quoin dossier, quire export).

## Verdict

**CONDITIONAL.** Two combinations that are wrong for downstream use still validate.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | An `rmm` document with no `as_of` validates, though an RMM is computed `--as-of` an instant and FR-018 names RMM as the case that needs one; no rule ties `as_of` to `document_kind: rmm`. | spec_artifacts_process/schemas/dossier-document-frontmatter.schema.json:4 |
| FND-002 | low | Nothing binds `id` to `document_kind`: `id: DOS-SRS` with `document_kind: rmm` validates, and the manifest's default `id_pattern: DOS-{next:03d}` mints `DOS-001`, unlike the `DOS-<KIND>` convention. | spec_artifacts_process/manifest.yaml:198 |

## Examined scope

```yaml
scope:
  - {id: FR-018-B-5, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` frontmatter schema SHALL treat `as_of` as optional text holding an ISO-8601 instant, present only where the source needs one."}
  - {id: FR-018-B-1, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` frontmatter schema SHALL require `id`, `title`, `version`, `document_kind` and `generated_by`."}
  - {id: FR-018-B-2, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` frontmatter schema SHALL accept only non-empty text for `version`, because `quire export` needs a version or a release."}
  - {id: FR-018-B-4, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` frontmatter schema SHALL accept only `quoin dossier` for `generated_by`."}
```
