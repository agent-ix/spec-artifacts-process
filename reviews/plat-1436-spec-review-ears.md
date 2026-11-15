---
id: SR-20261115175452
title: "PLAT-1436 PR155 spec-review EARS conformance"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-artifacts-process PR155; spec/functional/FR-018-dossier-document-archetype.md"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-018", type: references}
---

## Summary

Ticket: PLAT-1436. Checked the two Description SHALL statements and the seven Behavior SHALL statements of FR-018 against EARS grammar. All are ubiquitous ("The <system> SHALL <response>"), each has one subject and one response, and none is compound except the `as_of` statement. The `require`, `document_kind`, `generated_by`, no-digest and skeleton statements are clean.

## Verdict

**CONDITIONAL.** One statement is ambiguous about what it constrains, and one embeds a rationale clause.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The `as_of` statement mixes a schema rule ("optional text holding an ISO-8601 instant") with a generator rule ("present only where the source needs one"). It does not say whether non-instant text is rejected, and the schema accepts any non-empty string. | spec/functional/FR-018-dossier-document-archetype.md:41 |
| FND-002 | low | The `version` statement embeds a rationale clause ("because `quire export` needs a version or a release") in the normative sentence; it belongs in Description. | spec/functional/FR-018-dossier-document-archetype.md:38 |

## Examined scope

```yaml
scope:
  - {id: FR-018-B-1, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` frontmatter schema SHALL require `id`, `title`, `version`, `document_kind` and `generated_by`."}
  - {id: FR-018-B-2, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` frontmatter schema SHALL accept only non-empty text for `version`, because `quire export` needs a version or a release."}
  - {id: FR-018-B-3, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` frontmatter schema SHALL accept only `srs`, `architecture`, `trace-matrix` or `rmm` for `document_kind`."}
  - {id: FR-018-B-4, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` frontmatter schema SHALL accept only `quoin dossier` for `generated_by`."}
  - {id: FR-018-B-5, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` frontmatter schema SHALL treat `as_of` as optional text holding an ISO-8601 instant, present only where the source needs one."}
  - {id: FR-018-B-6, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The archetype SHALL declare no digest, hash or source-revision member."}
  - {id: FR-018-B-7, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The archetype SHALL declare a skeleton and a mapped record schema, like every artifact type (FR-012)."}
  - {id: FR-018-D-1, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "Both need a document type that validates, so this module SHALL declare the artifact type `DossierDocument`."}
  - {id: FR-018-D-2, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` archetype SHALL carry the identity `quire export` reads from the committed blob (`title`, `id`, `version`; quire-cli FR-034)."}
```
