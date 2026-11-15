---
id: SR-20261115175458
title: "PLAT-1615 PR157 spec-review base"
type: SpecReview
analysis: base
scope: "agent-ix/spec-artifacts-process PR157; spec/functional/FR-018-dossier-document-archetype.md"
review_set: base
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-018", type: references}
---

## Summary

Ticket: PLAT-1615. Base spec review of the FR-018 amendment in PR157 (e8d30ff). The amendment does four things:

- It rewrites the Description's producer sentence so that it no longer enumerates the documents.
- It extends the `document_kind` Behavior statement to ten members.
- It adds two `soup` → `as_of` statements, one for the frontmatter schema and one for the record schema.
- It repoints AC-3 to an invented kind and adds AC-14 and AC-15.

The amendment is in scope for PLAT-1615 ("Amend the spec-artifacts-process DossierDocument FR … to extend the `document_kind` enum"). It uses generic document names only and names no paywalled standard. `quire validate` was not run, because the local permission layer refused it. The PR body reports exit 0, which was not re-measured.

## Verdict

**CONDITIONAL.** The amendment is well scoped and agrees with the companion quoin FR-191 text. One new acceptance criterion depends on an undefined milestone label.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | AC-14 says "each of the six M2 `document_kind` values", but FR-018 never defines "M2" or says which six of its ten kinds are meant. A reader cannot tell the set under test from the spec alone. The AC should list the six values. | spec/functional/FR-018-dossier-document-archetype.md:85 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1 (head 52170c3): AC-14 now lists the six values explicitly: "Fixtures using `document_kind` values `verification-report`, `soup`, `anomalies`, `risk-management`, `risk-management-plan` and `release-record` each validate with `quire validate` when their required fields are present." |
