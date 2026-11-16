---
id: SR-20261115175468
title: "PLAT-1542 PR159 spec-review integrity"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-artifacts-process PR159 @57be7e8 over origin/main; spec/functional/FR-018-dossier-document-archetype.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-018"
    type: references
---

## Summary

Ticket: PLAT-1542. Integrity review (completeness, consistency, atomicity) of the FR-018 amendment. Consistency: the eleven-member list agrees with quoin FR-191's M3 paragraph (`threat-model`, `DOS-TM`) and with FR-202. The two halves of AC-17 that are new are verifiable on their own: the frontmatter fixture validates with no `as_of`, and the record schema accepts `documentKind: threat-model` with no `asOf`. The third clause repeats a check that already exists (FND-001).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | AC-17's third clause ("the frontmatter and record `document_kind` enums are equal and both contain `threat-model`") restates AC-11, which already requires the two `document_kind` member sets to be equal. It also bundles a third check into an AC that already has two. Its only new content is "contain `threat-model`", which the first two clauses already imply. The clause should be dropped, or narrowed to the record enum containing `threat-model`. | spec/functional/FR-018-dossier-document-archetype.md:88 |

## Verdict

PASS WITH NOTES. One low atomicity finding; nothing blocks implementation.

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | still-open | Round 1: the PR head is still 57be7e8, the commit this review examined, and no fix commit has landed since. AC-17 at FR-018 line 88 still carries "the frontmatter and record `document_kind` enums are equal and both contain `threat-model`", which restates AC-11. Missing: drop the clause, or narrow it to the record enum containing `threat-model`. |
| FND-001 | fixed | Round 2 (2bd0f32): AC-17's third clause narrowed to "the record `document_kind` enum contains `threat-model`"; the duplicate of AC-11's equality check is gone. |
