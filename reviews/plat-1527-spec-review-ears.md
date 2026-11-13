---
id: SR-20261112181939
title: "EARS review of PLAT-1527 Anomaly severity and fix verification links"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-artifacts-process PR145 @67f6422 over origin/main; spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md, spec/functional/FR-015-anomaly-safety-impact-assessment.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-014"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/FR-015"
    type: references
---

## Summary

Ticket: PLAT-1527. EARS review of the requirement statements PR #145 adds or
rewrites: the FR-014 Description sentence and the seven severity bullets
(lines 66-73), and the FR-015 Description paragraph and the five fix
verification bullets (lines 87-106). `quire validate` raises no grammar
warning on either file.

Well-formed: the `severity` vocabulary, no-default and no-derivation bullets
(ubiquitous), the `assessed`/`resolved`/`closed` presence bullet
(state-driven), the `verification` mapping bullet, and the two
`SHALL NOT` bullets on hashes and verdicts.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | "Who set or changed `severity`, and when, is the git history of the file, as for `status`; the module adds no severity history field." carries no SHALL, so the prohibition it states is not normative and nothing binds AC-17's "no field ... records who set it" to a requirement. Rewrite as "The module SHALL NOT add a field recording who set or changed `severity`, or when." | spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:72-73 |
| FND-002 | low | Two FR-015 bullets are compound and mix modals. Lines 87-90 combine a state condition, a SHALL, an "otherwise validation fails" clause and a MAY. Lines 91-99 state five obligations in one bullet: table headers, `Kind` vocabulary, non-empty `Rationale`, `Criterion` target resolution and `Test` target shape. Split each obligation into its own SHALL statement so that each one maps to one criterion. The presence condition reads more clearly as "While `resolution` is `fixed`, the document SHALL carry a `## Fix Verification` section." | spec/functional/FR-015-anomaly-safety-impact-assessment.md:87-99 |

## Verdict

PASS with two low findings. The statements are testable and name their
subject. The two findings are wording, not behaviour.

## Dispositions

Disposition pass 1 (4526bbf).

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | - |
| FND-002 | fixed | - |
