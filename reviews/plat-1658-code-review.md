---
id: SR-20261115175470
title: "PLAT-1658 spec-artifacts-process PR161 code-review"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR161 @d79b938 over origin/main; changed DossierDocument schema/TypeSpec/mapping/manifest/skeleton/example and tests/test_dossier_document.py"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-018"
    type: references
---

## Summary

Ticket: PLAT-1658. Code review of PR #161's dossier-kind enum and conditional version requirement, generated schemas, skeleton/example updates, and focused tests. The behavior and assertions align with FR-018, but the two new test markers cite matrix case ids that are not declared, so the acceptance criteria remain unbacked in the computed matrix.

## Verdict

**FAIL** — FR-018-AC-17 and AC-18 remain untagged because TC-247 and TC-246 have no rows in `spec/tests.md`.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The threat-model test's trace is not backed by a declared test-matrix row, leaving FR-018-AC-17 untagged. | tests/test_dossier_document.py:246-247 |
| FND-002 | high | The records-of-processing tests' traces are not backed by a declared test-matrix row, leaving FR-018-AC-18 untagged. | tests/test_dossier_document.py:176-177,229-230 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Commit 8f92751 adds TC-247 to spec/tests.md with FR-018-AC-17, and the Quire 0.46.0 matrix now binds the new threat-model test to that criterion. |
| FND-002 | fixed | Commit 8f92751 adds TC-246 to spec/tests.md with FR-018-AC-18, and the Quire 0.46.0 matrix now binds both records-of-processing tests to that criterion. |
