---
id: SR-20261115175461
title: "PLAT-1615 PR157 spec-review object"
type: SpecReview
analysis: base
scope: "agent-ix/spec-artifacts-process PR157; spec_artifacts_process/semantic/main.tsp (DossierKind, DossierDocument), spec_artifacts_process/schemas/DossierKind.json, spec_artifacts_process/schemas/DossierDocument.json, spec_artifacts_process/schemas/dossier-document-frontmatter.schema.json"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-018", type: references}
---

## Summary

Ticket: PLAT-1615. Method: spec-object-review. The SpecReview `analysis` enum has no object value, so this artifact uses `base`. Object review of the `DossierKind` enum and the `DossierDocument` model edits. All three representations carry the same ten kinds in the same order: the TypeSpec enum, the projected `DossierKind.json`, and the frontmatter schema's `document_kind` enum. `DossierDocument.documentKind` still `$ref`s `DossierKind.json`. The `soup` → `asOf` conditional is present in both the record schema and the TypeSpec extension, with the same `if`/`then` shape as `rmm`. The removal of "Closed in M1" from the enum doc comment matches the extended set.

Cross-repo naming was checked against the companion quoin PR (agent-ix/quoin#929). Its FR-191 amendment uses the same six kind tokens and calls the `soup` document the "SOUP list". Bidirectional tracing holds in both directions: FR-018 names quoin FR-191 downstream, and FR-191 names FR-018 upstream.

## Verdict

**PASS with one low finding.** The object definitions are consistent within the module and with the producer spec. One doc string uses a different name for the `soup` document.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The `DossierDocument` doc comment calls the `soup` document a "SOUP report". The producer spec (quoin FR-191 in agent-ix/quoin#929) and the ticket call the same document the "SOUP list", so one document has two names across the archetype and its producer. | spec_artifacts_process/semantic/main.tsp:798 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1 (head 52170c3): the TypeSpec doc comment, and the projected `DossierDocument.json` description, now say "a source-backed SOUP list supplies it, while a SOUP gap document may omit it."; "SOUP report" no longer appears. |
