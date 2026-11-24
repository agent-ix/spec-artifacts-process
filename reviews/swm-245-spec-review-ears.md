---
id: SR-20261115175479
title: "SWM-245 PR164 spec-review EARS conformance"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-artifacts-process PR164; spec/functional/FR-020-rolespec-archetype.md, spec/functional/FR-021-rolespec-trace-and-cross-row-checks.md, spec/functional/FR-022-rolespec-lint-ownership.md"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-020", type: references}
  - {target: "ix://agent-ix/spec-artifacts-process/FR-022", type: references}
---

## Summary

Ticket: SWM-245. Checked the SHALL statements of FR-020, FR-021 and FR-022 against EARS grammar. `quire validate --scope .` on the four new documents (quire 0.52.1, engine 0.62.2) reports five grammar warnings and no errors:

- FR-020 line 33: `ears:non-singular`.
- FR-020 line 17: `quality:mixed-modal`.
- FR-020 lines 44 and 47: `quality:agentless-passive`.
- FR-022 line 25: `ears:non-singular`.

FR-021's single SHALL statements (lines 19 and 30) are ubiquitous and conform.

## Verdict

**CONDITIONAL.** The engine warnings are low-severity wording defects. FR-022 puts binding SHALLs on a system outside this module, which is an allocation defect.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | One statement carries three obligations: the frontmatter schema SHALL require four fields, SHALL accept `id` only as a 2-to-6-letter prefix, and SHALL accept `version` only as an integer of at least 1. It should be split into one statement per SHALL (`ears:non-singular`). | spec/functional/FR-020-rolespec-archetype.md:33 |
| FND-002 | low | The Description mixes `SHALL` with `must` ("what it must and must not do"), so a reader cannot tell which part is binding (`quality:mixed-modal`). | spec/functional/FR-020-rolespec-archetype.md:17 |
| FND-003 | low | "Row-conditional rules SHALL be checked on each evaluation row" names no agent (`quality:agentless-passive`). It should name the `RoleSpec` archetype or `quire validate` as the subject. | spec/functional/FR-020-rolespec-archetype.md:44 |
| FND-004 | low | "A rule whose evaluations are all `judgement` SHALL be reported as a warning" names no agent (`quality:agentless-passive`). | spec/functional/FR-020-rolespec-archetype.md:47 |
| FND-005 | low | One statement carries two obligations: "This module SHALL declare … and SHALL implement neither check" (`ears:non-singular`). | spec/functional/FR-022-rolespec-lint-ownership.md:25 |
| FND-006 | medium | Two binding SHALLs have Quoin as their subject ("Quoin SHALL require a strictly higher `version`", "Quoin SHALL report any cited rule id"). Quoin is outside this module, no AC here verifies them, and the sentence "Deleting a rule … requires the same bump" carries no modal at all. These obligations belong in a Quoin requirement. Here they should be stated as an allocation, for example "This module SHALL NOT implement …; the check is allocated to Quoin (ticket)". | spec/functional/FR-022-rolespec-lint-ownership.md:23-24 |
