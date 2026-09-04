---
id: SR-009
title: "dependency review of the #78 semantic-module contract spec set"
type: SpecReview
analysis: dependency
scope: "spec/spec.md, spec/usecase/US-002, spec/functional/FR-009..FR-013, spec/non-functional/NFR-001, spec/tests.md"
review_set: all
---
# SR-009: dependency review of the #78 semantic-module contract spec set

## Summary

Dependency and ordering analysis of the #78 set, with every named external dependency verified
read-only on 2026-09-04. Everything the spec names exists and is at the stated version:
`@agent-ix/semantic-core` resolves at `0.1.0`; `@typespec/compiler` and `@typespec/json-schema`
both resolve at `1.15.0`; quoin declares FR-070..FR-075 as named; quire-rs declares FR-008,
FR-050, FR-053, FR-054 and FR-069..FR-072 as named; `filament-core-service#23` is OPEN with the
title the spec's Out of Scope paraphrases; the installed engine is `quire 0.31.0 (engine 0.46.0)`
and the Python wheel exposes `extract_semantic`, `validate_document` and `Registry.load_from`.
The sibling migrations `spec-artifacts-iso` (merged `6686f11`) and `spec-objects-business`
(merged `567e5c4`) exist and are the reference this set follows.

Classification: FR-009 is the only pure enablement requirement — nothing else can be built until
one schema exists. FR-010, FR-011 and FR-012 are features that consume it. FR-013 is a constraint
on FR-009's output and is therefore tasked with it, not after it. NFR-001 is a gate over the
whole set. The declared `Dependencies` sections form a DAG with no cycle.

Four findings, all about ordering honesty rather than missing dependencies.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | FR-013 is written as a downstream constraint ("no emitted model SHALL declare a run property") but is only enforceable *while* the models are authored. Tasked after FR-009 it becomes an audit of a decision already made, and the cheapest fix at that point is to relax the audit. It must be a gate inside the FR-009 task, and the plan must say so. | FR-013, FR-009 | correct-requirement-no-evidence |
| FND-002 | medium | FR-011's `mappings.yaml` names sections and columns from the manifest (`FR-011-CON-1`) and properties from the emitted schemas (`FR-011-CON-2`), so it has two prerequisites — FR-009 *and* FR-010 — and both are declared. But FR-012's skeletons are also a prerequisite of FR-011-AC-4 (golden records are built from skeletons), while FR-012 declares FR-011 as *its* upstream. That is a soft cycle between the mapping and the skeletons: it resolves only because the two land in one task. State the joint task in the plan rather than leaving the reader to find that the arrows point both ways. | FR-011-AC-4, FR-012 | wrong-requirement |
| FND-003 | medium | NFR-001-AC-5 depends on two repositories this specification does not own (`spec-objects-business`, `filament-core-data`) at whatever commit they happen to be on. Without a recorded commit the measurement is not reproducible and a later failure cannot be attributed. The Verification section says "at the commit recorded in the measurement" but no requirement obliges recording it. Make the commit an output of the measurement. | NFR-001-AC-5 | correct-requirement-no-evidence |
| FND-004 | low | The engine the spec depends on is provisioned by `make dev-quire` (quire-rs#392) and that target does not yet exist in this repository's Makefile — `spec-objects-business` has it, this module does not. FR-009..FR-013 all assume it. It is an enablement step with no requirement of its own; carry it as the first plan task rather than as an assumption. | FR-009, NFR-001 | missing-requirement |
