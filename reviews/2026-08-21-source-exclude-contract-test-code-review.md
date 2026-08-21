---
id: SR-007
title: "Code review — source_exclude contract test and TC-070 binding (commit fe3adcc, #56)"
type: SpecReview
analysis: code-review
scope: "tests/test_manifest.py, spec/tests.md (TC-070), coordinated against spec-artifacts-iso CR-011"
review_set: subset
---

# SR-007: Code review — source_exclude contract test (fe3adcc, #56)

## Summary

Pre-release review of the unreviewed fix commit `fe3adcc` (contract test
pinning the three `traceability.source_exclude` globs and guarding the
evidence tree, TC-070 binding, closes #56). The test is real — exact-list pin,
a mechanical guard with red proof against ten forbidden spellings, and an
accept-set check — and the reworded TC-070 matrix row states the actual
oracle. One low defect found and fixed in this pass: the guard helper
raised `IndexError` instead of returning a violation on the empty string.
The guard's semantics were also cross-checked against spec-artifacts-iso's
CR-011 schema constraints; the divergences found there are recorded in that
repo's SR-002 (this side's guard was the correct reference on every case).

## Verdict

**CONDITIONAL** — one low finding, already fixed in this review pass; nothing
blocks release.

## Findings

| ID      | Severity | Summary                                                                                                                                          | Refs                        |
| ------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------- |
| FND-001 | low      | `_source_exclude_violation("")` raised `IndexError` (`pattern[0]` on empty input) instead of reporting a violation; FIXED — empty string now returns a violation and joins the red-proof list (#56) | tests/test_manifest.py:544  |

## Review detail

- **Oracle realness (no tautology).** The test compares the manifest's
  loaded `source_exclude` against a literal expected list, then runs every
  entry through an independent classifier, then proves the classifier can
  fail (ten bad examples) and can pass non-trivially (five good examples,
  two of them NOT in the manifest). Changing the manifest or weakening the
  guard each break a distinct assertion. This meets the SR-006 FND-001
  red-test standard the commit cites.
- **Test style.** Plain-function tests with ID-carrying docstrings are this
  file's established convention (`test_tc064_...` etc.); the new test
  matches it, carries the TC-070 / FR-004-AC-1 / CR-032 traces, uses no
  mocks and no database.
- **Matrix truthfulness.** The TC-070 row (spec/tests.md:85) now describes
  the pin + guard oracle rather than the incidental loads/validates claim
  SR-006 FND-003 called out; the green is backed
  (`test_tc070_source_exclude_pins_the_globs_and_guards_the_evidence_tree`,
  suite 82 passed + 1 xfailed, coverage 100%).
- **Cross-repo semantics.** The guard's rule — first segment literally
  `tests` and no wildcard-free later segment — was executed side-by-side
  with spec-artifacts-iso's CR-011 schema `not/pattern` constraints over a
  23-case battery. All eight coordination cases (`tests`, `tests/`,
  `tests/**`, `tests/fixtures/**`, `*/fixtures/**`, `**`, `?x/**`,
  `tests_integration/fixtures/**`) agreed; six unlisted edge cases diverged
  on the iso side and were fixed there (spec-artifacts-iso SR-002 FND-001).
  After that fix the two guards agree on all 23 cases.

## Gap analysis — does #56's acceptance hold?

| Acceptance claim (#56 / commit message)                       | Holds? | Evidence                                                                 |
| ------------------------------------------------------------- | ------ | ------------------------------------------------------------------------ |
| Exact glob list pinned, any change is a conscious diff         | yes    | `assert patterns == _SOURCE_EXCLUDE` against a literal                   |
| Forbidden forms rejected (`**`, whole-tests-tree, leading wildcard) | yes | classifier + 10-case red proof (now 11 with the FND-001 empty string)    |
| Guard proven able to fail                                      | yes    | every bad example asserted to yield a violation                          |
| TC-070 binding retires the unbacked green (SR-006 FND-002/003) | yes    | TC-070 row reworded to the real oracle; test carries the binding         |
| Manifest globs untouched                                       | yes    | commit diff touches only spec/tests.md and tests/test_manifest.py        |

No unstated requirements surfaced: the schema-shape half of FR-004-AC-1
remains covered by the pre-existing manifest-validates tests, and the value
constraints now also hold at the iso schema gate (CR-011), giving
defense in depth rather than overlap.
