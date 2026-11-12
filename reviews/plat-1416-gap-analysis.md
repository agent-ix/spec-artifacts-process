---
id: SR-20261102086822
title: "Gap analysis of PLAT-1416 kind-typed Anomaly Target references against FR-015 and NFR-001 (PR 141)"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process PR141 @7d210ed over origin/main e4e1a21; spec/functional/FR-015-anomaly-safety-impact-assessment.md, spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md, spec/tests.md, spec_artifacts_process/manifest.yaml, tests/test_anomaly.py, tests/fixtures/anomaly/**"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-015"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/NFR-001"
    type: references
---
# SR-20261102086822: Gap analysis of PLAT-1416 against FR-015 and NFR-001

## Summary

Ticket: PLAT-1416. Planless. Plan completion: not assessed.

Matrix source: `quire matrix` (quire 0.41.0, engine 0.57.0). It lists every FR-015 and
NFR-001 criterion as `untagged`, with `criterion-tagged-outside-row` warnings, because
`spec/tests.md` has no FR-014, FR-015 or NFR-001 rows. The test markers exist
(`@pytest.mark.trace("FR-015-AC-6")` and others). This state predates PR 141: it came with
#140, and the #140 gap analysis wrongly put it down to a tool defect. Bindings were taken
from the trace markers.

Checked against FR-015 and NFR-001:

- FR-015-AC-6: both cases pass on the PR head and fail with the kind declaration removed.
  The test is backed.
- FR-015-AC-5 and AC-4: still pass. The dangling cases yield no extra kind mismatch.
- FR-015 Behavior, `Requirement` → FR, NFR or criterion: a probe corpus with NFR-001 shows a
  `Requirement` row naming `NFR-001` or `NFR-001-AC-1` yields no finding, and a `Hazard` row
  naming `NFR-001` yields `reference-kind-mismatch`. The mapping is right, but no repo test
  covers the NFR branch.
- NFR-001-AC-1/AC-2: fixture (c) now reports all three defects (the empty Rationale with a
  line, plus the dangling and kind-mismatch bundle findings without one). It stays a true
  strict xfail on the line clause, which PLAT-1476 owns. The fixtures (a) and (b)
  record-layer xfail is unchanged in substance and remains true.

## Verdict

**PASS with two low findings.** The PR closes FR-015-AC-6. The gaps that remain are an
untested Behavior branch and pre-existing matrix bookkeeping. Neither blocks this PR.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | FR-015 Behavior says a `Requirement` row may name an NFR or one of its criteria. The fixture corpus has no NFR, so dropping `nfr-document` or `nfr-acceptance-criterion` from `kind_targets.Requirement` survives every test. A probe shows the current mapping behaves correctly. Adding an NFR to the corpus and a `Requirement` row naming it to the AC-4 valid fixture would cover it. | tests/fixtures/anomaly/corpus/spec; spec_artifacts_process/manifest.yaml:1140-1143 |
| FND-002 | low | `spec/tests.md` has no rows for FR-014, FR-015 or NFR-001, so the computed matrix reports FR-015-AC-6 and every other Anomaly criterion as untagged, although tagged tests exist. This predates PR 141, and PLAT-1416, the ticket that owns these criteria, is the place to close it. | spec/tests.md; spec/functional/FR-015-anomaly-safety-impact-assessment.md:86-95 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | medium | The new matrix rows for TC-186 (NFR-001-AC-1) and TC-187 (NFR-001-AC-2) read `✅ Complete` and `✅`. NFR-001-AC-2, and NFR-001-AC-1 for fixture (c), are backed only by strict xfails that PLAT-1476 owns: no passing test shows the three fixture (c) defects in one run, and no passing test shows the lines. The repo marks such rows as blocked, for example TC-135 `❌ strict expected failure: quire-rs#221` and FR-010-AC-9 `❌ blocked on quire-rs#221`. Mark both TC-186 and TC-187 as blocked on PLAT-1476. | spec/tests.md:175-176; spec/tests.md:339-340 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | 9c1de24 adds corpus NFR-002 with NFR-002-AC-1, valid/requirement-rows-name-nfr.md and invalid/hazard-row-names-nfr.md, with two new tests. Mutation results: dropping `nfr-acceptance-criterion` from Requirement, or adding the nfr targets to Hazard, fails a test. Dropping `nfr-document` alone survives, but that mutant is equivalent: under quire-rs FR-049 the resolution set of `nfr-acceptance-criterion` (archetype NFR) already holds the NFR document ids, so behaviour does not change. |
| FND-002 | fixed | 9c1de24 adds TC-168..175, TC-176..185 and TC-186..187 to the coverage and summary tables of spec/tests.md. None of these ids exists on main, and each has exactly one summary row. Every Anomaly trace marker now carries its TC id. `quire matrix` shows all 20 FR-014/FR-015/NFR-001 criteria `tagged`, with zero `criterion-tagged-outside-row`. |
