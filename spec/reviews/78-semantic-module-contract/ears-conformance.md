---
id: SR-010
title: "EARS requirement-grammar review of the #78 spec set"
type: SpecReview
analysis: ears-conformance
scope: "spec/usecase/US-002, spec/functional/FR-009..FR-013, spec/non-functional/NFR-001"
review_set: all
---
# SR-010: EARS requirement-grammar review of the #78 spec set

## Summary

Engine check plus statement-by-statement reading of every `shall` in FR-009..FR-013 and NFR-001.
`quire validate --scope . "spec/**/*.md" --summary` reports **26/28 documents grammar-clean (92%)
and 9 grammar findings, none of them in a document authored for #78** — the six
`quality:agentless-passive`, one `quality:mixed-modal`, one `ears:unclassifiable` and one
`ears:missing-subject` all land on the pre-existing FR-003 and FR-004 and are out of this
ticket's scope; they are named here so the clean result for the new files is not read as a claim
about the whole repository.

The five new FRs and the NFR were brought to zero engine findings during authoring: eleven
statements that packed two `shall` clauses were split, and two that carried a subject only in
their first clause were rewritten. The remaining judgment findings are the ones the engine cannot
make.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | medium | FR-011 "The mapping SHALL accept `CRLF` input by normalising line endings before slicing, so a Windows checkout produces the same record and the same digest is computed over the bytes as read" states two different obligations in one sentence — normalise before slicing, and digest the bytes as read — and they are in tension: one reads normalised text, the other reads raw bytes. The engine passes it because there is one `shall`. Split it, and say explicitly which byte sequence the digest covers. | FR-011 | wrong-requirement |
| FND-002 | medium | FR-012 "The typed declaration form SHALL be shown on `Standard` and on no other type" is a statement about the *module's authoring choice*, not about a system behaviour, and it carries its own justification in the same sentence. As written it cannot fail a test — nothing observes "is shown". Restate as the observable form: the `Standard` skeleton carries the section and no other skeleton does. | FR-012 | wrong-requirement |
| FND-003 | low | Six statements across FR-009 and FR-011 use "the mapping SHALL …" and "the generator SHALL …" as the subject. Both are named artifacts of this module and the engine accepts them, but neither is a component in `spec.md`'s System Overview, so a reader tracing allocation finds no owner. Name both in the System Description. | FR-009, FR-011, spec.md | missing-requirement |
| FND-004 | low | NFR-001's Statement is two paragraphs, each with one `shall` — the archetype and the engine both accept it, and splitting it into two NFRs would separate a claim from the measurement that grounds it. Recorded as reviewed-and-kept so it is not re-raised. | NFR-001 | correct-requirement-no-evidence |
| FND-005 | low | FR-010 "Measured against quire 0.46.0 the two available refusals are silent…" is a measurement note inside `## Behavior`, not a requirement, and carries no `shall`. It belongs there for the reader, but it means the Behavior section mixes obligations with evidence. Consider moving it to Inputs or a Notes block in a later pass. | FR-010 | correct-requirement-no-evidence |
