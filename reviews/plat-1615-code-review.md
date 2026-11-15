---
id: SR-20261115175456
title: "PLAT-1615 PR157 code-review"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR157; spec_artifacts_process/semantic/main.tsp, spec_artifacts_process/schemas/DossierKind.json, spec_artifacts_process/schemas/DossierDocument.json, spec_artifacts_process/schemas/dossier-document-frontmatter.schema.json, spec_artifacts_process/skeletons/DossierDocument.md, spec_artifacts_process/examples/DossierDocument.record.json, tests/fixtures/dossier/invalid/bad-kind.md, tests/test_dossier_document.py"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-018", type: references}
---

## Summary

Ticket: PLAT-1615. Reviewed `git diff origin/main...HEAD` at e8d30ff (one commit). The PR adds six `document_kind` members to the TypeSpec `DossierKind` enum, the projected `DossierKind.json`, and the frontmatter schema enum. It adds a `soup` → `as_of` conditional to both the TypeSpec `@extension("allOf")` and the frontmatter schema. It updates the skeleton contract comment and the golden record body to match. It repoints the invalid-kind fixture to `not-a-dossier-kind`, and adds parametrized tests for AC-14 and AC-15.

No builds or tests were run (per the brief). `quire` and `quoin` invocations were refused by the local permission layer ("This command requires approval"), so this artifact has not been run through `quire validate`. The four vocabulary copies were compared by reading: the TypeSpec enum, `DossierKind.json`, the frontmatter enum and the skeleton comment all list the same ten members in the same order. The projected `DossierDocument.json` `allOf` matches the TypeSpec extension. The golden `body.endLine` moves 24→25, which matches the one line the skeleton comment gains.

## Verdict

**PASS with low findings.** The schema changes are correct and consistent across all representations. One test assertion is weaker than the file's own helper, and the two `as_of` conditionals are duplicated where one would do.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The AC-15 frontmatter check asserts a bare `"as_of" in message` substring instead of using `fails_naming`, which checks for the quoted field form. Every other "fails naming X" test in the file uses `fails_naming`, so this one would also pass on any message that only mentions `as_of` in passing. | tests/test_dossier_document.py:217 |
| FND-002 | low | The `rmm` and `soup` `as_of` conditionals are two identical `if/then` blocks that differ only in the const, in both the frontmatter schema and the TypeSpec extension. One block with `"enum": ["rmm", "soup"]` would state the rule once and stop it growing by one block per kind. | spec_artifacts_process/schemas/dossier-document-frontmatter.schema.json:49-63 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1 (head 52170c3): the malformed-`as_of` check now calls the shared helper: `fails_naming(document, "as_of", scope=tmp_path)` (tests/test_dossier_document.py:224), and `fails_naming` gained a `scope` keyword so tmp-path fixtures use it. |
| FND-002 | fixed | Round 1 (head 52170c3): the `soup` conditional was removed from the frontmatter schema, `DossierDocument.json` and the TypeSpec `@extension("allOf")`, so each now carries the single `rmm` block and no duplicate remains. |
