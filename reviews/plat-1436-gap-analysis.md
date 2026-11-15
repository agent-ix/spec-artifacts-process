---
id: SR-20261115175450
title: "PLAT-1436 PR155 gap-analysis"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process PR155; spec/functional/FR-018-dossier-document-archetype.md, spec/tests.md, tests/test_dossier_document.py, spec_artifacts_process/"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-018", type: references}
---

## Summary

Ticket: PLAT-1436. Planless gap analysis of FR-018 against the computed matrix (`quire matrix --scope .`, quire 0.45.0, engine 0.60.0). Plan completion: not assessed.

The matrix reports all six FR-018 criteria as `untagged` or `method-without-symbol`, so none is backed. The tests carry `@pytest.mark.trace("FR-018-AC-n")`, but quire reports `criterion-tagged-outside-row` for each one: the repository backs criteria through `spec/tests.md` TC rows (FR-014..FR-017 tag `FR-0xx-AC-n` together with `TC-nnn`), and this PR adds no TC row. No production code was found without an owning requirement, and nothing is stubbed.

## Verdict

**FAIL.** FR-018 is 0/6 backed in the matrix (FND-001). The tests exist and exercise the right fixtures, so this is a traceability fix plus two small coverage gaps.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | spec/tests.md has no TC rows for FR-018, so all six criteria are `untagged`/`method-without-symbol` in `quire matrix`, and the FR-018 trace tags give no backing (`criterion-tagged-outside-row`). | spec/tests.md:208 |
| FND-002 | medium | The second clause of AC-6 (role `definition` in mappings.yaml) is not asserted by any FR-018-tagged test; only the TC-120 test covers it, via EXPECTED_ROLES. | tests/test_dossier_document.py:62-65 |
| FND-003 | medium | AC-5 (Inspection) has no inspection record, and an honest inspection fails: the mapped record reaches `provenance.digest` through the required `provenance` member. | spec/functional/FR-018-dossier-document-archetype.md:53 |
| FND-004 | low | AC-1 requires "the same fixture without `as_of`", but the test validates two different fixtures (srs.md and rmm.md differ in id, title and kind), so the as_of-only delta is never exercised. | tests/fixtures/dossier/valid/srs.md:1 |

## Examined scope

```yaml
scope:
  - {id: FR-018-AC-1, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "A fixture carrying `id`, `title`, `version`, `type`, `document_kind`, `generated_by` and `as_of` validates with `quire validate`, and the same fixture without `as_of` validates."}
  - {id: FR-018-AC-2, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "A fixture with no `version` fails `quire validate`, with a diagnostic naming `version`."}
  - {id: FR-018-AC-3, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "A fixture with `document_kind: verification-report` fails `quire validate`, with a diagnostic naming `document_kind`."}
  - {id: FR-018-AC-4, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "A fixture with `generated_by: hand` fails `quire validate`, and a fixture with no `generated_by` fails."}
  - {id: FR-018-AC-5, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The `DossierDocument` frontmatter schema and mapped record schema declare no member named like a digest, hash or revision."}
  - {id: FR-018-AC-6, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The skeleton `DossierDocument.md` validates, and `DossierDocument` carries the role `definition` in `mappings.yaml`."}
```
