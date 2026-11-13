---
id: SR-20261113084036
title: "PLAT-1583 spec-artifacts-process PR148 gap-analysis"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process PR148 @d95f76c over origin/main; spec/functional/FR-015-anomaly-safety-impact-assessment.md AC-11..19; spec/tests.md TC-199..206; tests/test_anomaly.py; tests/fixtures/anomaly/**"
review_set: subset
---

## Summary

Ticket: PLAT-1583. Planless gap analysis over FR-015-AC-11..19. Plan completion: not assessed. All test-method criteria are `tagged` in `quire matrix`; AC-18 (inspection) is asserted over the emitted property set and the VerificationRow fields. The PR claims no quoin-side work: ticket AC-2/AC-3 (`quoin anomaly check`, evidence-store corpus) are absent from the diff, the PR body and spec/tests.md. Upstream check: quire-rs FR-049 (origin/main) defines a target kind's resolution set as the ids of documents of the target archetype together with the minted ids, so `FR-001` is in the `acceptance-criterion` resolution set by the engine's own spec. No Linear ticket tracks a change to that (searched `reference-kind-mismatch`, `kind_targets`).

## Verdict

**CONDITIONAL.** One clause of FR-015-AC-15 is unmet and nothing upstream tracks it (FND-001). The xfail is the right local disposition. It needs a quire-rs ticket.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The clause 'a Criterion row targeting FR-001 fails as a kind mismatch' cannot pass with this module on any engine that follows quire-rs FR-049. FR-049 puts the ids of archetype-FR documents into the resolution set of every target bound to FR, `acceptance-criterion` included. Reproduced: neither `Criterion \| FR-001` nor `Criterion \| NFR-002` (untested, same cause) yields a finding. The strict xfail is honest, but it cites no ticket and its 'turns green when the engine types document ids' names no planned change. A quire-rs ticket is needed: a target declared with `id_column` should resolve only its minted ids, or there should be a declared opt-out. The alternative is to amend FR-015-AC-15 and the FR-015 Behavior clause 'including a requirement document such as FR-001'. Cite the ticket in the xfail reason. | tests/test_anomaly.py:1062-1080 |

## Examined scope

```yaml
scope:
- id: FR-015-AC-11
  path: spec/functional/FR-015-anomaly-safety-impact-assessment.md
  role: examined
  excerpt: 'The manifest declares the `## Fix Verification` table with exactly the columns `Kind`, `Target`, `Rationale`, `min_rows: 1` and the `Kind` vocabulary `Criterion`, `Test`, and declares a document reference `anomaly-fix-verification` with `column` `Target`, `kind_column` `Kind`, `targets` listing `acceptance-criterion`, `nfr-acceptance-criterion`, `test-case`, `requirement-document`, `nfr-document` and `hazard-document`, and `kind_targets` `Criterion` to the acceptance-criterion targets and `Test` to `test-case`; and it declares a `column_patterns` rule on `Target` requiring an id token.'
- id: FR-015-AC-12
  path: spec/functional/FR-015-anomaly-safety-impact-assessment.md
  role: examined
  excerpt: A `resolved` anomaly and a `closed` anomaly with `resolution` `fixed` each fail validation, at the `status` line, with no `## Fix Verification` section; a `closed` anomaly with `resolution` `not-a-defect`, `duplicate` or `wont-fix` and no section validates.
- id: FR-015-AC-13
  path: spec/functional/FR-015-anomaly-safety-impact-assessment.md
  role: examined
  excerpt: In the corpus of AC-4 plus a `TestMatrix` test case `TC-001`, a `fixed` anomaly with a `Criterion` row targeting `FR-001-AC-1` and a `Test` row targeting `TC-001` validates.
- id: FR-015-AC-14
  path: spec/functional/FR-015-anomaly-safety-impact-assessment.md
  role: examined
  excerpt: In that corpus, a `Criterion` row targeting `FR-001-AC-99` and a `Test` row targeting `TC-999` each fail as a dangling reference naming the id and its row.
- id: FR-015-AC-15
  path: spec/functional/FR-015-anomaly-safety-impact-assessment.md
  role: examined
  excerpt: In that corpus, a `Criterion` row targeting `FR-001` (a requirement document), a `Criterion` row targeting the hazard, and a `Test` row targeting `FR-001-AC-1` each fail as a kind mismatch.
- id: FR-015-AC-16
  path: spec/functional/FR-015-anomaly-safety-impact-assessment.md
  role: examined
  excerpt: A row with an empty `Rationale` or a `Kind` outside the vocabulary fails validation.
- id: FR-015-AC-17
  path: spec/functional/FR-015-anomaly-safety-impact-assessment.md
  role: examined
  excerpt: The mapping yields `verification` entries with `kind`, `target` and `rationale` as authored.
- id: FR-015-AC-18
  path: spec/functional/FR-015-anomaly-safety-impact-assessment.md
  role: examined
  excerpt: No field or table column of the `Anomaly` type holds a commit hash, author or date of the fix, a field naming the fixing change, or a verdict or sign-off on the verification.
- id: FR-015-AC-19
  path: spec/functional/FR-015-anomaly-safety-impact-assessment.md
  role: examined
  excerpt: A `fixed` anomaly whose only row is `Test`, `-`, `verified`, and one whose only row has an empty `Target`, each fail validation at the row.
```
