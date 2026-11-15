---
id: SR-20261115175460
title: "PLAT-1615 PR157 spec-review integrity"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-artifacts-process PR157; spec/functional/FR-018-dossier-document-archetype.md"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-018", type: references}
---

## Summary

Ticket: PLAT-1615. Integrity check of the FR-018 structural changes in PR157. Checked:

- Completeness: every new Behavior statement has an AC. Line 51 maps to AC-3 and AC-14, line 55 to AC-15, and line 58 to AC-15.
- Consistency between the Description and the Behavior statements.
- Atomicity of the new ACs.
- That AC-3 no longer contradicts the extended vocabulary. Before this PR, AC-3 named `verification-report` as invalid; it now uses `not-a-dossier-kind`, so the conflict is resolved.

## Verdict

**CONDITIONAL.** Coverage of the new statements is complete. One new AC bundles two separately stated requirements. The Description's account of who decides `as_of` now disagrees with two hard-coded rules.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | AC-15 bundles the frontmatter rule (line 55) and the record-schema rule (line 58) into one criterion. The equivalent `rmm` rules are split into AC-8 and AC-13, so AC-15 is not atomic and breaks the FR's own pattern. | spec/functional/FR-018-dossier-document-archetype.md:86 |
| FND-002 | low | The Description says "The producer also decides when a document needs `as_of`; this module only validates what is written". The module now hard-codes `as_of` as required for both `rmm` and `soup`, so the sentence understates the module's role. It should say the module requires `as_of` for those kinds and leaves the others to the producer. | spec/functional/FR-018-dossier-document-archetype.md:35-36 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1 (head 52170c3): the bundled criterion is split. AC-15 covers the frontmatter only ("A `soup` fixture with no `as_of` validates as a gap document; ... a malformed `as_of` fails `quire validate` naming `as_of`.") and the new AC-16 covers the record schema, matching the AC-8/AC-13 split. |
| FND-002 | fixed | Round 1 (head 52170c3): the Description now reads "This module requires `as_of` for `rmm`. A source-backed SOUP list needs the producer's `as_of` under quoin FR-197, but this generic archetype also accepts a SOUP gap document with no source binding and no `as_of`." (FR-018 lines 35-38), which agrees with the single hard-coded `rmm` rule. |
