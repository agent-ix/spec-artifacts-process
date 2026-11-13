---
id: SR-20261113084035
title: "PLAT-1583 spec-artifacts-process PR148 code-review"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR148 @d95f76c over origin/main; spec_artifacts_process/{manifest.yaml,mappings.yaml,schemas/AnomalyFields.json,schemas/Anomaly.json,schemas/Verification*.json,semantic/main.tsp}; tests/test_anomaly.py; tests/fixtures/anomaly/**"
review_set: subset
---

## Summary

Ticket: PLAT-1583. Code review of the FR-015 fix-verification slice (commit 3e07bd1). The `fix_verification` locator, the `anomaly-fix-verification` document reference and the `verification` mapping match FR-015-AC-11 exactly; the `Target` id-token rule rejects `-` and empty cells. The strict xfail on the `Criterion -> FR-001` case was reproduced: the engine reports no kind mismatch for it, and none either for `Criterion -> NFR-002`, while `Test -> FR-001`, `Criterion -> HAZ-001` and `Criterion -> TC-001` each raise one. The xfail is honest, strict and limited to one parameter.

## Verdict

**PASS with one low finding.** The implementation is correct. The xfail reason text trips the trace scanner (FND-001).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The xfail `reason` string on the FR-015-AC-15 parameter contains the literal id `FR-015-AC-11`, so `quire matrix` now emits `tests/test_anomaly.py:1076: FR-015-AC-11 ... was not read by the declared trace grammar` on every run. It adds a spurious warning. Write it without the id (for example 'the targets the manifest declares'). | tests/test_anomaly.py:1076 |

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

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-002 | low | The FR-015 amendment drops the 'Criterion row naming FR-001' case and the test no longer uses this fixture. It still sits under `invalid/`, but the amended spec accepts it: in the corpus it raises no finding. Quoin reads these fixtures in place, so a valid document under `invalid/` misleads. Delete it. | tests/fixtures/anomaly/invalid/verification-criterion-names-requirement.md:1-28 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1 (head a4141f7): The xfail parameter and its reason string are removed. The case list is now ("verification-criterion-names-hazard", "HAZ-001", "Criterion"), ("verification-criterion-names-test-case", "TC-001", "Criterion"), ("verification-test-names-criterion", "FR-001-AC-1", "Test"), |
