---
id: SR-20261102086819
title: "Gap analysis of PLAT-1415/PLAT-1416 — FR-014, FR-015, NFR-001 against the Anomaly implementation"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process@94e98ba over origin/main 7c15a5f; spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md, spec/functional/FR-015-anomaly-safety-impact-assessment.md, spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md, tests/test_anomaly.py, tests/fixtures/anomaly/**, spec_artifacts_process/**"
review_set: subset
---
# SR-20261102086819: Gap analysis of PLAT-1415/PLAT-1416

## Summary

Ticket: PLAT-1415 (with PLAT-1416). PR spec-artifacts-process#140 at `94e98ba`. Planless.
Plan completion: not assessed.

Matrix source: `quoin matrix` (quoin 0.30.1) reports all 20 FR-014/FR-015/NFR-001 criteria
as `untagged` with no binders. `quire trace --id <AC>` finds a `pytest-trace-marker` claim in
tests/test_anomaly.py for every one of them, from 1 to 3 claims each, and some pre-existing
markers such as FR-004-AC-23 show the same discrepancy on main. I therefore treat the
`untagged` result as a tool defect, not a gap in this PR, and I took bindings from
`quire trace`.

Each criterion was checked against its test and run. Tests that pass are FR-014-AC-1..8,
FR-015-AC-1..3 and FR-015-AC-7..10. FR-015-AC-5 and AC-6 are strict xfail, because quire
0.56 does not resolve table-cell targets; I confirmed the engine accepts a dangling target.
The test-intent defects in the FR-015-AC-4, FR-015-AC-5/6 and NFR-001-AC-1 tests are
recorded in the code-review artifact SR-20261102086818 (FND-001..003). They are not
repeated here.

Ticket ACs, checked:

- The archetype ships an emitted schema and a valid sample. Covered.
- Illegal transitions fail. These belong to quoin FR-136 by spec, and this module rightly
  owns none of it.
- Closing requires a named person. Covered.
- Assessment references resolve against requirement and hazard ids. Strict xfail, blocked
  on the engine.
- A missing assessment at `assessed` or later fails. Covered.

## Verdict

**CONDITIONAL.** Coverage is broad and honest except for one gap. NFR-001-AC-2 has no test
and no xfail for the record-layer fixtures (a) and (b). Two Behavior-level fixture gaps in
FR-014 are minor.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | NFR-001-AC-2 requires that every diagnostic from fixtures (a), (b) and (c) carries a line, and that the `status` line is used for an absence. Fixtures (a) and (b) are checked only at the record layer, where jsonschema errors carry no line, and their tests assert no line at all. The PR body defers this to quoin's record validation. NFR-001 assigns no such ownership, and there is no strict xfail or follow-up ticket, so the AC is uncovered for (a) and (b) without any marker of that. | tests/test_anomaly.py:415-434; spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md |
| FND-002 | low | FR-014 Behavior requires fixtures for "a `closed` document for each `resolution`". The valid fixtures cover closed+fixed and closed+not-a-defect only, with no closed+duplicate or closed+wont-fix. A probe shows the schema accepts both, so the gap is in the fixtures only. | tests/fixtures/anomaly/valid/ |
| FND-003 | low | FR-014-AC-5's clause "a fixture with `status` of ... `assessed` and a `resolution` fails" has no fixture or test. Only `identified-with-resolution` exists. A probe confirms the schema rejects assessed+resolution, so the behaviour is right and untested. | tests/test_anomaly.py:180-191; tests/fixtures/anomaly/invalid/ |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1 (head aa3ef43): `test_record_layer_defects_are_reported_at_the_status_line` is a strict xfail over fixtures (a) and (b). It asserts 2 diagnostics at the `status` line each. Leaving the NFR-001 text unedited is acceptable, because the NFR states the target behaviour and the strict xfail now marks the gap. Who owns record-layer line attribution (this module or quoin FR-073) is still undecided and should go to a ticket. The xfail reason names none. |
| FND-002 | fixed | Round 1: `valid/closed-duplicate.md` and `valid/closed-wont-fix.md` were added and validate at the document and record layers through the parametrised valid-fixture test. |
| FND-003 | fixed | Round 1: `invalid/assessed-with-resolution.md` was added. `test_an_identified_or_assessed_anomaly_carries_no_resolution` asserts `[("not", 0)]`. |
