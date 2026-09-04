---
id: SR-014
title: "risk and complexity review of the #78 spec set"
type: SpecReview
analysis: risk-complexity
scope: "spec/functional/FR-009..FR-013, spec/non-functional/NFR-001"
review_set: all
---
# SR-014: risk and complexity review of the #78 spec set

## Summary

Every requirement scored on technical risk and volatility.

| Req | Tech risk | Volatility | Drivers | Mitigation |
|-----|-----------|------------|---------|------------|
| FR-009 | Medium | Medium | External compiler and emitter at an exact pin; a package that resolves only through user-level npm config; byte-level determinism | Pin and lock; `--check` in `make lint`; two-run determinism test |
| FR-010 | High | Low | This manifest is the contract every repository in the programme validates against; a wrong byte is a build break everywhere | Structural diff against a checked-in 0.1.0 baseline; consumer re-validation (NFR-001) |
| FR-011 | High | High | 12 models × ~9 mapping kinds hand-authored; the mapping has no engine consumer yet, so nothing but this module's own tests can contradict it | Totality check in both directions; golden records; land with FR-012 |
| FR-012 | Medium | Low | 12 new skeletons that authors copy; a bad skeleton propagates into every consuming repo | Every skeleton validated as authored; negative counterparts |
| FR-013 | Low | Medium | A constraint on modelling judgement; "documented meaning" is not machine-checkable | Enforce during authoring, not after (SR-009 FND-001) |
| NFR-001 | High | Low | The whole ticket's safety gate; measured against two external repositories | Baseline fixture + two-repo demonstration with recorded commits |

Top hazards: FR-011 (highest on both axes), FR-010 (highest blast radius), NFR-001 (the gate that
catches the other two).

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | FR-011 is the largest and least-constrained piece of the ticket: a hand-authored mapping for twelve models with **no production consumer**, which means no external system can ever contradict it. Its only oracle is this module's own reference implementation, and a reference implementation written by the same pass that wrote the mapping agrees with it by construction. The golden records (FR-011-AC-4) are the mitigation only if they are derived from the *skeletons and the schemas*, never from the reference mapping's output being blessed. Say that explicitly, or the golden records are a snapshot of the bug. | FR-011-AC-4, FR-011-CON-3 | implementation-bug-despite-evidence |
| FND-002 | high | FR-010's blast radius is not bounded by anything inside this repository. `manifest.yaml` is consumed by ~239 repositories; NFR-001 measures two. Two is far better than zero and is the right cost/value point for this ticket, but the residual risk must be stated: a change that passes both consumers can still break a third. Record the residual explicitly in NFR-001's Scope rather than letting "2 of 2 consumers validated" read as "the ecosystem validated". | NFR-001, FR-010 | correct-requirement-no-evidence |
| FND-003 | medium | FR-011 and FR-012 are scoped to land together (SR-009 FND-002) and together they are roughly two thirds of the ticket's volume. A single task carrying both is the shape that produces a 3,000-line commit nobody reviews. Slice by artifact type — one vertical slice proving model, mapping, skeleton, golden record and negative fixture end-to-end for one type first, as a gate — before the remaining eleven. | FR-011, FR-012 | correct-requirement-no-evidence |
| FND-004 | medium | Volatility on FR-011 is high because the mapping kinds are a quoin-owned vocabulary (FR-071/FR-072) still in motion, and this module pins nine of them by name in `semantic.mappings`. If quoin renames or splits a kind, this manifest is wrong and every consumer's load is affected. Record the coupling and the version it was read at. | FR-010-AC-1, FR-011 | correct-requirement-no-evidence |
| FND-005 | low | FR-009's determinism claim (CON-3, AC-8) is scored medium risk rather than low only because the emitter is external and its output ordering is not this module's to guarantee. The two-run test catches instability on one machine; it cannot catch instability across compiler patch versions. The exact pin is the real mitigation and it is declared. Recorded so the pin is not later relaxed as "we have a determinism test". | FR-009-CON-3, FR-009-AC-8 | correct-requirement-no-evidence |
