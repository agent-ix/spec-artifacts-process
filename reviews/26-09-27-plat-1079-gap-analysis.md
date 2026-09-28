---
id: SR-021
title: "Gap analysis of PLAT-1079 — AC to test to manifest"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process@16a673e9e59c6c424ef67d0eccc967286931ffdb; spec/functional/FR-004-traceability-declaration.md, spec/functional/FR-007-verification-method-catalog.md, spec/functional/FR-010-semantic-manifest-contract.md, spec/tests.md, spec_artifacts_process/manifest.yaml, tests/"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-004"
    type: "reviews"
  - target: "ix://agent-ix/spec-artifacts-process/FR-007"
    type: "reviews"
  - target: "ix://agent-ix/spec-artifacts-process/FR-010"
    type: "reviews"
---
# SR-021: Gap analysis of PLAT-1079 — AC to test to manifest

## Summary

Ticket: PLAT-1079. This is a manual AC→test→code check scoped to the PR diff. It replaces a
full-repo quoin gap analysis, which would be out of proportion for a manifest-only change.
Plan completion: not assessed.

| AC | TC | Test(s) | Manifest | Result |
| --- | --- | --- | --- | --- |
| FR-004-AC-20 | TC-148 | `test_constraint_target_mirrors_acceptance_criterion`, `test_constraint_is_a_traces_to_and_inspection_target`, `test_constraint_target_mints_and_dangling_con_references_resolve` | `trace_targets[constraint]`, `traces-to`/`inspection-obligation` targets | Met. 22 `-CON-` rows minted. `-CON-` dangling references went from 13 on origin/main to 0. |
| FR-004-AC-21 | TC-149 | `test_verification_lint_rule_is_scoped_and_advisory`, `test_verification_lint_rule_flags_stale_test_ids_only` | `lint_rules[acceptance-criterion-verification-method]` | Met. Lint output checked by hand: warning on `Test (TC-999)` and `Inspection (IT-3)`, silent on `Test` and `property-based-testing`. The `verification`/`nfr-verification`/`interface-verification` references are unchanged, and TC-091's wholesale baseline diff covers them. |
| FR-004-AC-22 | TC-151 | `test_verification_lint_rule_allowed_set_is_classes_union_catalog` | `lint_rules[].allowed` | Met. Set equality with classes ∪ catalog keys, no duplicates, `Eval`/`Manual` absent. |
| FR-007-AC-15 | TC-150 | `test_tc150_constraint_obligations_are_derived`, TC-055 extension | `obligations[constraint]` | Met. There are 22 obligations; before this PR there were none. |
| FR-010-AC-3 | TC-091 | `test_every_0_1_0_declaration_survives_unchanged`, TC-136 | whole manifest vs 0.1.0 baseline | Met with a weak spot. The trace-target and obligation deltas are pinned exactly, but the `traces-to` targets widening is checked only by membership (SR-020 FND-001). |

Every new or changed test fails when run against the origin/main manifest. There is no
production code outside the manifest, so no untracked symbols arise.

## Verdict

**PASS WITH FINDINGS.** Every in-scope AC has a test that backs it and fails on the old
manifest. The findings are about the precision of the matrix text and the oracles.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The `spec/tests.md` TC-091 description still lists only the pre-PLAT-1079 deltas. FR-010-AC-3, the requirement it traces, now also names the `constraint` target, the obligation source, the widened `targets` and the new `lint_rules` entry. The matrix row therefore understates what TC-091 checks, and the test itself does carry the PLAT-1079 exclusions. | spec/tests.md:260 |
| FND-002 | low | The TC-148 row names `evidence: source` as "declared", but the manifest omits the key, relying on the default `source` posture exactly as `acceptance-criterion` does. The test asserts the key is absent from both. The behaviour matches the spec, but the wording "declared" is loose. | spec/tests.md:313, spec_artifacts_process/manifest.yaml:884-889 |

## Dispositions

Round 1, reviewed at `828819c33b95486ab8054ced04a8fbb2c956ac18`.

| FND | Outcome | sha/reason |
| --- | --- | --- |
| FND-001 | fixed | 828819c |
| FND-002 | fixed | 828819c |
