---
id: SR-020
title: "Code review of PLAT-1079 — constraint trace target, obligation source and Verification lint rule"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process@16a673e9e59c6c424ef67d0eccc967286931ffdb; spec_artifacts_process/manifest.yaml, tests/test_traceability_declaration.py, tests/test_verification_catalog.py, tests/test_semantic_manifest.py, tests/test_evidence_archetypes.py, spec/tests.md"
review_set: subset
---
# SR-020: Code review of PLAT-1079 — constraint trace target, obligation source and Verification lint rule

## Summary

Ticket: PLAT-1079 (epic PLAT-1076). PR: spec-artifacts-process#106, reviewed at `16a673e`.
Python lane. The diff is manifest-only on the production side: a `constraint` trace target,
`constraint` added to the `traces-to` and `inspection-obligation` targets, a `constraint`
obligation source, and a single `lint_rules` entry `acceptance-criterion-verification-method`.
The tests change with it, and `spec/tests.md` flips four rows to Complete.

Gates. CI run 36367894292 (workflow_dispatch on `16a673e`) passed ruff, black, schemas-check and
pytest. Its pytest artifact shows 261 passed, 44 skipped and 1 xfailed. The CI runner has no
`quire` CLI, so three new behavioural tests skipped there:
`test_constraint_target_mints_and_dangling_con_references_resolve`,
`test_verification_lint_rule_flags_stale_test_ids_only` and
`test_tc150_constraint_obligations_are_derived`. I ran all of them locally against quire 0.33.0
(engine 0.47.1), and they passed.

Oracle strength was checked by mutation in a scratch copy of the tree:

- The origin/main manifest under the PR's tests fails all 11 new or widened tests.
  `test_the_trace_targets_are_byte_identical` passes, which is correct, because it only excludes
  the new entries.
- Removing `constraint` from `traces-to.targets` is killed by TC-091, TC-148 structural and
  TC-148 end-to-end. The end-to-end test reproduces the measured baseline of 13 `-CON-`
  `dangling-trace-reference` warnings, and origin/main also shows 13.
- Adding a stray target to `inspection-obligation` is killed by TC-043's exact set.
- **Adding a stray target (`stakeholder-validation-criterion`) to `traces-to.targets` is killed
  by nothing.** See FND-001.

End-to-end measurements at `16a673e`:

- 22 `constraint` rows appear in `minted_targets`, and 22 `constraint` obligations. That equals
  the 22 `FR-NNN-CON-N` table rows across 7 FR documents.
- There are 0 `-CON-` dangling references.
- `quire lint` flags `Test (TC-999)`, `Inspection (IT-3)` and `Eval` at `warning`, and passes
  `Test` and `property-based-testing`.

Two failures reproduce identically on origin/main with the local quire, so this PR did not
cause them: `test_tc047_adoption_is_optional`, and 2 `test_semantic_manifest` fixture errors.
Both come from a duplicate `spec-artifacts-process` in the operator's installed module store.

## Verdict

**PASS WITH FINDINGS.** There are no high findings. There is one medium: a widened baseline test
checks membership where it should pin the exact list, and a docstring overclaims what it pins.
The lows cover oracle precision and a stale count. The manifest change itself is correct and
matches FR-004-AC-20/21/22 and FR-007-AC-15.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | TC-091 checks the widened `traces-to` and `inspection-obligation` `targets` only by membership (`"constraint" in entry["targets"]`), then resets `targets` wholesale to the baseline. TC-136 does the same wholesale reset. Neither pins the exact new list, so an unrelated extra target added to `traces-to` passes every test. Mutation confirmed this: adding `stakeholder-validation-criterion` to `traces-to.targets` is killed by no test (TC-043 does catch the same mutation on `inspection-obligation`). The TC-136 docstring's claim "TC-091 pins both" is therefore false. Fix: assert `entry["targets"] == baseline_targets + ["interface-acceptance-criterion", "constraint"]` before the reset. | tests/test_semantic_manifest.py:181-185, tests/test_semantic_manifest.py:504-519 |
| FND-002 | low | TC-091's `lint_rules` pin is self-referential for `allowed` (`"allowed": current["lint_rules"][0]["allowed"]`), so TC-091 pins nothing about the allowed values. TC-151's set-equality test does cover them, so nothing is left unguarded. A one-line comment pointing at TC-151 would stop a reader mistaking this for a pin. | tests/test_semantic_manifest.py:274 |
| FND-003 | low | The TC-149 behavioural test does not assert that the finding is at `warning` severity or that it names the rule id `acceptance-criterion-verification-method`. It only checks for the substrings `row 3`/`TC-999`. Its `quire validate --okf` exit-code assertion is vacuous: `validate` does not evaluate `lint_rules` at all (0 rule diagnostics in its output), so the assertion would still pass at `severity: error`. The `warning` severity is actually pinned only by the structural test. The test also writes its fixture into the repo's `tests/fixtures/` rather than `tmp_path`. | tests/test_traceability_declaration.py:769-801 |
| FND-004 | low | TC-150's oracle checks only that at least one `constraint` obligation exists and that each id contains `-CON-`. FR-007-AC-15/TC-150 say "an `FR-NNN-CON-N` obligation for every `## Constraints` row". I measured 22 obligations against 22 minted `constraint` targets, so the behaviour holds today. The test would still pass if some rows were dropped. Asserting that the obligation ids equal the minted `constraint` target ids would close it. | tests/test_verification_catalog.py:319-326 |
| FND-005 | low | The manifest and test comments both cite "roughly 156" pre-existing `Test (TC-…)`/`Inspection (TC-…)` Verification cells in this repository. Measured at `16a673e`, running `quire lint` over `spec/functional` and `spec/non-functional` gives 123 rule warnings, and a grep finds 121 FR/NFR AC rows with a `(TC-`/`(IT-` Verification. The comments claim a measurement in this repository, so they should carry the real figure. | spec_artifacts_process/manifest.yaml:684, tests/test_traceability_declaration.py:789 |
| FND-006 | low | The behavioural halves of TC-148 and TC-149, and all of TC-150, are skipped in CI because the runner has no `quire` CLI. FR-007-AC-15 is flipped to Complete, but its only CI-executed evidence is the structural TC-055 extension. This is a pre-existing repo-wide pattern (44 skips), and all three tests pass locally. Recorded so the Complete status is not read as "CI-verified". | tests/test_verification_catalog.py:302-303, spec/tests.md:91 |

## Mock and test style

No mocks. Every behavioural test drives the real `quire` CLI. The tests are module-level test
functions and follow the repository's idiom. Trace binding uses the repo's `python-docstring-id`
form (`"""TC-148 (FR-004-AC-20): …`), which matches the existing tests in the same files. There
are no TODO, FIXME or stub bodies.

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-007 | low | The fix for FND-003 correctly removed the vacuous `quire validate --okf` exit-code assertion from the TC-149 behavioural test. However, FR-004-AC-21 and the TC-149 matrix row still claim "`quire validate --okf` exit code is unaffected either way", and no test now backs that clause. The clause is true only because `validate` never evaluates `lint_rules`. Resolve it by rewording the TC-149 row and the AC clause, for example to "lint is advisory; `validate` does not evaluate `lint_rules`", or by accepting it as-is. This is non-blocking. | spec/tests.md:314, spec/functional/FR-004-traceability-declaration.md:179 |

## Dispositions

Round 1, reviewed at `828819c33b95486ab8054ced04a8fbb2c956ac18`. Fix commit `828819c`. CI run 36369416368 succeeded on this sha (verified with `gh run view`). All mutations were re-run on a scratch copy of the tree:

- A stray `stakeholder-validation-criterion` added to `traces-to` is now killed by TC-091 and TC-136.
- Reordering the `traces-to` targets is killed by the same two tests.
- Dropping `Analysis` from `allowed` is killed by TC-091 and TC-151.
- `severity: error` is killed by TC-149 (structural and behavioural) and by TC-091.
- Retargeting the `constraint` obligation is killed by TC-055, TC-150 and TC-091.
- The origin/main manifest fails 12 of the 12 targeted tests.

| FND | Outcome | sha/reason |
| --- | --- | --- |
| FND-001 | fixed | 828819c |
| FND-002 | fixed | 828819c |
| FND-003 | fixed | 828819c |
| FND-004 | fixed | 828819c |
| FND-005 | fixed | 828819c |
| FND-006 | deferred | PLAT-1087 (CI workflow change, owner approval) |
