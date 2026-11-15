---
id: SR-20261115175457
title: "PLAT-1615 PR157 gap-analysis"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process PR157; spec/functional/FR-018-dossier-document-archetype.md, spec/tests.md, tests/test_dossier_document.py, tests/fixtures/dossier/, spec_artifacts_process/"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-018", type: references}
---

## Summary

Ticket: PLAT-1615. Planless gap analysis of the FR-018 changes in PR157 (e8d30ff). Plan completion: not assessed.

`quire matrix` / `quoin matrix` could not be run: the local permission layer refused both CLIs ("This command requires approval"). The criterion-to-test check below was therefore done by hand, from the trace tags and the test bodies. It is not a computed matrix.

Manual check. AC-3 is backed by `test_document_kind_outside_enum_fails_naming_document_kind` against the repointed `bad-kind.md`. AC-14 is backed by `test_each_m2_kind_validates`, parametrized over all six new kinds, with `as_of` supplied only for `soup`. AC-15 is backed by `test_soup_requires_as_of_in_both_schemas`, which covers the frontmatter half and the record half. AC-11 still holds, because the frontmatter enum and `DossierKind.json` were extended together. AC-12 holds by reading: the `allOf` in `DossierDocument.json` matches the TypeSpec extension. The PR body claims a drift check passed, which was not re-run here. No production change lacks an owning requirement, and nothing is stubbed.

## Verdict

**CONDITIONAL.** The tests assert what the new criteria say. The test plan still describes the old AC-3 behaviour, and AC-14 and AC-15 have no TC rows. In this repository that left the PLAT-1436 criteria unbacked in the computed matrix.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | TC-232 still says `document_kind: verification-report` fails validation. After this PR `verification-report` is a valid kind (FR-018 line 51, AC-14), so the test-plan row states the opposite of the spec and of the test it names. | spec/tests.md:215 |
| FND-002 | medium | AC-14 and AC-15 have no TC rows in spec/tests.md, and their tests tag only `FR-018-AC-14`/`-15`, with no TC id. In PLAT-1436 (reviews/plat-1436-gap-analysis.md FND-001), `quire matrix` reported `criterion-tagged-outside-row` for exactly this shape, so both new criteria are likely unbacked in the computed matrix. Not reproduced here, because quire was not runnable. | spec/tests.md:225 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1 (head 52170c3): TC-232 now reads "A `DossierDocument` with `document_kind: not-a-dossier-kind` fails `quire validate` with a diagnostic naming `document_kind`." (spec/tests.md:215), matching AC-3. |
| FND-002 | fixed | Round 1 (head 52170c3): spec/tests.md adds TC-243 (AC-14), TC-244 (AC-15) and TC-245 (AC-16), and the tests carry `@pytest.mark.trace("FR-018-AC-14", "TC-243")`, `("FR-018-AC-15", "TC-244")` and `("FR-018-AC-16", "TC-245")`. Verified by inspection; the computed matrix was not re-run in this disposition-only pass. |
