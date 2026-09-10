---
id: Plan-003
title: "spec-artifacts-process — differential testing catalogue method (issue #86)"
type: Plan
status: active
relationships:
  - target: ix://agent-ix/spec-artifacts-process/FR-007
    type: references
---
# Implementation Plan: differential testing catalogue method

## Requirements Summary

### Functional Requirements

- [ ] **FR-007**: extend the shared verification-method catalogue with one bounded differential-testing method and prove its advice behavior without manufacturing independence or qualification.
  - [x] **FR-007-AC-15**: one exact declarative entry and claim ceiling, checked by Rust TC-144.
  - [ ] **FR-007-AC-16**: exact pinned Quoin catalogue/advice execution through Engineering Assurance, including negative method-selection and malformed/non-completed controls.
  - [ ] **FR-007-AC-17**: frozen-corpus proof that only obligations already carrying `reference-equivalence` gain the method and no prior advice fact or order changes.
  - [ ] **FR-007-CON-1**: all three executable acceptance cases use Rust with bare `ix-trace-rs`; cross-tool execution uses Engineering Assurance and introduces no local runner, verdict scraper or evidence store.

## Dependency Graph

- `Task-017 -> Task-018` — the exact catalogue entry and its Rust unit contract must be frozen before a cross-tool consumer can prove Quoin exposes and advises it.
- `agent-ix/engineering-assurance#34 -> Task-018` — TC-145 needs the accepted typed Rust process-execution result for exact executable identity, argv, environment, bounds, completion state and retained output. This repository does not recreate that producer.
- `Task-018 -> Task-019` — the frozen-corpus delta uses the same accepted producer configuration and strict catalogue/advice readers proven by TC-145; the final review and promotion gate additionally require both integration cases complete.

### Shared dependencies

- Engineering Assurance owns bounded native process execution and typed producer outcomes.
- Quoin owns catalogue/advice semantics and structured output.
- This module owns only the catalogue data and its method-level acceptance contract.

### Cross-cutting constraints

- Rust 1.98.1 and bare compiler-checked `ix-trace-rs` tags cover every new test.
- Local verification uses one Cargo build job under `/tmp/quire-heavy-check.lock`; hosted workflows remain manual-dispatch only and are never used as evidence for this plan.
- Agreement is evidence only for the declared comparison relation. Independence, correctness, general equivalence and qualification remain unclaimed.

## Test Plan

### Unit Tests

- [x] **TC-144** (FR-007-AC-15, FR-007-CON-1): read the authoritative manifest bytes, assert the exact 34-method census and strict differential entry, mutate every identity-bearing field, and prove an accepted extension to an unrelated catalogue method cannot change this contract.

### Integration Tests

- [ ] **TC-145** (FR-007-AC-16, FR-007-CON-1): through Engineering Assurance, run an exact pinned Quoin executable and closed module set; prove reference equivalence selects `differential-testing`, three near-neighbor controls do not, and malformed or non-completed producer results cannot pass.
- [ ] **TC-146** (FR-007-AC-17, FR-007-CON-1): run the same frozen obligation corpus before and after the catalogue addition and compare structured advice so only pre-existing `reference-equivalence` facts gain the method while every prior recommendation, reason, relative order and advice state remains identical.

## Remaining Work

### Track A: Critical Path (serial)

- **A1 = Task-017** Declare and check the differential method — complete; exit: the authoritative data and strict Rust unit contract agree and mutations fail.
- **A2 = Task-018** Prove Quoin catalogue and advice conformance — blocked on Engineering Assurance #34; exit: the exact real producer path distinguishes selection, non-selection, malformed output and non-completion.
- **A3 / Gate = Task-019** Prove advice-delta containment and promote — blocked on Task-018; measures the complete change surface; pass: TC-144 through TC-146, Rust review, semantic gap analysis, validation and bounded local gates all pass with no unsupported claim.

### Track B: External Shared Enablement

- **Engineering Assurance #34** supplies the typed Rust process producer consumed by A2 and A3; this plan contributes consumer cases and does not duplicate its implementation.

## Parallel Execution Summary

```text
Task-017 (done) ----> Task-018 (wait for EA #34) ----> Task-019 / promotion gate
                          ^
Engineering Assurance #34+  (external owner, independent workstream)
```

## Task File Mapping

| Task | Track | Owns (references) | Verified by (verifies) | Status |
| --- | --- | --- | --- | --- |
| Task-017 | A | FR-007-AC-15, FR-007-CON-1 | TC-144 | done |
| Task-018 | A | FR-007-AC-16, FR-007-CON-1 | TC-145 | blocked |
| Task-019 | A | FR-007-AC-17, FR-007-CON-1 | TC-146 | blocked |

## Coordination and Merge Sequencing

1. Keep the branch unmerged and do not request review while TC-145/146 are blocked.
2. Consume the accepted Engineering Assurance Rust interface after #34 lands; report any missing reusable producer behavior back to that owner rather than adding a local runner.
3. Complete TC-145 before TC-146 so the delta case reuses one proven exact producer/reader boundary.
4. Run the exact Rust review and QUOIN semantic gap analysis over the complete branch, remediate findings, then open one reviewable PR for issue #86.

## Completion Criteria

- All three tasks are `done`, all plan checkboxes are checked, and the Test Matrix reports TC-144 through TC-146 complete without status drift.
- The exact Rust review and semantic gap analysis pass the complete branch.
- Rust format, Clippy with denied warnings, all local tests, Quire validation and workflow-trigger inspection pass under the declared bounds.
- The merged catalogue supports downstream quire-verification Task-028 without creating a second method registry, execution framework or evidence store.
