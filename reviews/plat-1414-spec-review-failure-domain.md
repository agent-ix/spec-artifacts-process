---
id: SR-20261102086817
title: "Failure-domain review of PLAT-1414 Anomaly lifecycle"
type: SpecReview
analysis: failure-domain
scope: "agent-ix/spec-artifacts-process PR139 @36754ea over origin/main; spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md, spec/functional/FR-015-anomaly-safety-impact-assessment.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-014"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/FR-015"
    type: references
---

## Summary

Ticket: PLAT-1414. Failure-domain analysis of the FR-014 state lifecycle and
its interaction with the FR-015 assessment. It looks at the design choices the
ticket did not specify: the `resolved` to `assessed` reopen transition and the
terminal `closed` state.

The reopen transition is sound. It models a resolution that failed
verification without inventing a fifth state, and keeping `closed` terminal is
a defensible policy (a regression after closure becomes a new anomaly). The
gaps are the paths the lifecycle does not have.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The only way to reach `closed` is through `resolved`. An anomaly that is assessed and found not to be a defect, a duplicate, or accepted without change has no legal path to closure. The author must write a `resolved` row for a fix that never happened, so the record ends up asserting something false. Add a disposition: either a transition from `assessed` to `closed` with a required non-empty `Note`, or a resolution kind such as fixed, not-a-defect, duplicate or won't-fix, and add criteria for it. | spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:40-43 |
| FND-002 | low | When the reopen transition `resolved` to `assessed` is taken, nothing requires the safety-impact assessment to be revisited. A failed fix can change what the anomaly affects, but the earlier `none` assessment carries over silently. State whether a reopen needs a fresh assessment. If so, a `Note` on the reopen row naming the re-assessment is the lightest form. | spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:40-41; spec/functional/FR-015-anomaly-safety-impact-assessment.md:37-39 |
| FND-003 | low | FR-014-AC-4 lists the illegal skips `identified` to `resolved` and `identified` to `closed`, but not `assessed` to `closed`. That is the skip most likely to slip through, because it is one step short of the legal path. Add it to AC-4. | spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:63 |

## Verdict

PASS WITH FINDINGS. One medium finding (no honest closure path for a
non-defect) should be fixed in this PR. The reopen design is accepted as
written.
