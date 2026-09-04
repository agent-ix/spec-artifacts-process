---
id: Plan-002
title: "spec-artifacts-process — semantic module contract (issue #78)"
type: Plan
status: active
relationships:
  - target: ix://agent-ix/spec-artifacts-process/StR-001
    type: references
  - target: ix://agent-ix/spec-artifacts-process/US-002
    type: references
  - target: ix://agent-ix/spec-artifacts-process/FR-009
    type: references
  - target: ix://agent-ix/spec-artifacts-process/FR-010
    type: references
  - target: ix://agent-ix/spec-artifacts-process/FR-011
    type: references
  - target: ix://agent-ix/spec-artifacts-process/FR-012
    type: references
  - target: ix://agent-ix/spec-artifacts-process/FR-013
    type: references
  - target: ix://agent-ix/spec-artifacts-process/NFR-001
    type: references
  - target: ix://agent-ix/spec-artifacts-process/IT-002
    type: references
---
# Implementation Plan: semantic module contract

## Requirements Summary

### Stakeholder Requirements
- [ ] **StR-001**: the module activates against filament-core and its declared contributions are what consumers validate against.

### User Stories
- [ ] **US-002**: one machine-readable declaration per process artifact type, so a reviewer, a generator and the engine read the same definition instead of three copies that drift.

### Functional Requirements
- [ ] **FR-009**: emit one JSON Schema 2020-12 document per declared artifact type from a TypeSpec source importing `@agent-ix/semantic-core` 0.1.0, at a pinned toolchain, with a drift gate and a version-embedded `$id`.
- [ ] **FR-010**: `manifest.yaml` at version 0.2.0 carries the quoin FR-070 `semantic` block and a reference-form `data_schema` per artifact type, with every 0.1.0 declaration byte-identical.
- [ ] **FR-011**: publish the Markdown mapping and the round-trip policy, nine mapping kinds, total in both directions, with golden records.
- [ ] **FR-012**: one executable skeleton per declared artifact type plus negative counterparts.
- [ ] **FR-013**: authored definitions stay separate from execution occurrences; no emitted model carries a run property.

### Non-Functional Requirements
- [ ] **NFR-001**: additive compatibility — nothing a consuming repository authors today stops validating, measured against two consumer repositories.

### Integration Test Requirements
- [ ] **IT-002**: `quoin module install path:<dir>` accepts the semantic contract, and the prior module state is restored unconditionally.

## Dependency Graph

- `toolchain -> FR-009` — nothing compiles until the pinned compiler, emitter and semantic-core are installed and the engine wheel is provisioned (`make dev-quire`, quire-rs#392). This has no requirement of its own and is Task-007 (SR-009 FND-004).
- `FR-009 (generator half) -> FR-009 (models half)` — the generator, the drift gate and the `$id` rules must run against a source that compiles before there are twelve models to emit.
- `FR-013 || FR-009 (models half)` — **not** a downstream audit. FR-013 constrains what the models may contain, and enforced after the fact its cheapest fix is to relax the audit (SR-009 FND-001). It is a gate inside the model-authoring task.
- `FR-009 -> FR-010` — the manifest references emitted files by path and digest.
- `FR-009 + FR-010 -> FR-011` — the mapping names properties from the schemas and sections from the manifest.
- `FR-011 <-> FR-012` — the golden records are built from the skeletons and the skeletons are validated by the mapping. The arrows point both ways, so the two land in one slice rather than in sequence (SR-009 FND-002).
- `FR-010 + FR-011 + FR-012 -> NFR-001` — the compatibility measurement compares the finished 0.2.0 manifest against the 0.1.0 baseline and against two consumers.
- `FR-010 -> IT-002` — the Quoin install exercises the finished `semantic` block and digests.

No cycle survives the split. The FR-011/FR-012 pair is a genuine mutual dependency and is resolved by scope, not by ordering.

## Quality Gates

**Gate 1 (Task-010) — one artifact type end-to-end before the other eleven.**
FR-011 and FR-012 together are roughly two thirds of this ticket's volume and would otherwise
land as one unreviewable commit (SR-014 FND-003). `SpecReview` is the slice: it is the only
type with a non-trivial `body_extraction` that this repository itself authors dozens of, so a
mistake in the model, the mapping or the skeleton shows up immediately. The gate passes only
when its model, its mapping entry, its skeleton, its authored golden record and its negative
fixtures all agree — and specifically when the golden record was **authored from the skeleton
and the schema** and the reference mapping reproduces it, rather than being recorded from
whatever the mapping produced (SR-014 FND-001). Nothing in Track B or C starts until it holds.

**Gate 2 (Task-014) — the consumer measurement.** A green local suite is not evidence for a
module every repository validates against. Two consumers are re-validated under 0.1.0 and 0.2.0
and the finding sets compared as a difference at a recorded commit.

## Execution Tracks

- **Track A (critical path)**: Task-007 → Task-008 → Task-009 → **Gate 1** Task-010 → Task-012 → Task-013.
- **Track B (parallel after Task-009)**: Task-011 (manifest and baseline fixture).
- **Track C (post-gate)**: Task-014 (**Gate 2**), Task-015, Task-016.

## Test Plan

The Test Matrix `spec/tests.md` is authoritative. This plan adds no test id: every task's
frontmatter `verifies` edges name the TC rows it discharges, and TC-080..TC-143 are the whole
set. Rows stay `🚧` until the test that backs them runs green; the flip is Task-016's work and
is never a hand edit (SR-008 FND-005).

Three rows will not be green at merge and are recorded rather than hidden:

- **TC-135** (FR-010-AC-9) is a **strict expected failure**: quire 0.46.0 refuses an unknown
  `semantic` key and a mismatched digest silently (quire-rs#221, quire-rs#394), so the criterion
  that the refusal *names* the offender cannot hold. The test asserts the current silence and
  turns red when the engine changes. It is never skipped.
- **TC-143** (FR-013-AC-8) is an Inspection with a recorded reviewer, not an automated row.
- **FR-009-AC-13** and the five Inspection-only constraints carry no TC by design and are
  recorded in the Constraint Boundary table.
