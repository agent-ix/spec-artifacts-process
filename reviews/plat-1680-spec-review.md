---
id: SR-20261113084042
title: "PLAT-1680 spec-artifacts-process PR149 spec-review"
type: SpecReview
analysis: base
scope: "agent-ix/spec-artifacts-process PR149 @14cf518 over origin/main; spec/functional/FR-017-adr-design-realization-verb.md, spec/functional/index.md, spec/spec.md, spec/tests.md TC-217"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-017"
    type: references
---

## Summary

Ticket: PLAT-1680. Spec review of the new FR-017, covering EARS and integrity. This is the right home: no existing FR in this repository specifies the `ADR` archetype's links. FR-001 covers the whole manifest, and FR-009, FR-010 and FR-013 mention ADR only as one artifact type among twelve. FR-017 is the next free number after FR-016 (Anomaly release rationale). Index, scope and TestMatrix rows are added. The verb, its direction and the claim that the relation counts the edge regardless all match spec-objects-architecture FR-010 and quire-rs FR-086 on main. The cross-repository `ix://` form matches this repository's convention (as in FR-001). `quire validate` on FR-017 raises one `ears:non-singular` warning (FND-003). `spec/tests.md` fails `functional_coverage` structural validation on origin/main as well, so that failure predates this PR and is not attributed to it.

## Verdict

**PASS WITH MINOR FINDINGS.** The direction and placement are sound. AC-1 needs its pass/fail wording tightened (FND-001), and three wording defects are low.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-017-AC-1 says `quire validate` "accepts" the forward verb and "does not accept" `requirement_realized_by`. In fact `quire validate` exits 0 for both. The only observable difference is the advisory `disallowed-edge-type` warning, so "does not accept" reads as a rejection that never happens. Fix: state the criterion in terms of the presence or absence of that finding. | spec/functional/FR-017-adr-design-realization-verb.md:40 |
| FND-002 | low | FR-017-AC-1 is compound: it bundles three independent outcomes (forward verb clean, inverse flagged, unlisted verb flagged) into one criterion, so a failure cannot be attributed to one of them. | spec/functional/FR-017-adr-design-realization-verb.md:40 |
| FND-003 | low | The third Behavior bullet carries two SHALLs (existing verbs stay listed, and an unlisted verb still draws the finding). quire reports `ears:non-singular`. Split it into two statements. | spec/functional/FR-017-adr-design-realization-verb.md:34 |
| FND-004 | low | The TC-217 description omits the inverse-verb negative (`requirement_realized_by` draws the finding), which both FR-017-AC-1 and the test assert. | spec/tests.md:199 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | AC-1..3 are now worded as whether quire validate reports a `disallowed-edge-type` finding, which matches the measured exit-0 advisory behaviour. |
| FND-002 | fixed | AC-1 is split into AC-1..4, one outcome each, with one tagged test per AC. |
| FND-003 | fixed | The Behavior bullet is split into two single-SHALL lines, and quire validate no longer reports `ears:non-singular` on FR-017. |
| FND-004 | fixed | TC-218 covers the inverse-verb negative, and TC-217..220 mirror AC-1..4. |
