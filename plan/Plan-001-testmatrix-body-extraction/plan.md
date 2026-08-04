---
id: Plan-001
title: "spec-artifacts-process — TestMatrix body_extraction (FR-003)"
type: Plan
status: active
relationships:
  - target: ix://agent-ix/spec-artifacts-process/StR-001
    type: references
  - target: ix://agent-ix/spec-artifacts-process/US-001
    type: references
  - target: ix://agent-ix/spec-artifacts-process/FR-003
    type: references
---
# Implementation Plan: TestMatrix body_extraction (FR-003)

## Requirements Summary

### Stakeholder Requirements
- [ ] **StR-001**: Process artifact templates registered by Module activation (context — activation machinery already shipped via FR-001).

### User Stories
- [ ] **US-001**: Trust the test matrix through machine validation — `tests.md` checked for expected coverage tables and test-case columns on every validation.

### Functional Requirements
- [ ] **FR-003**: `body_extraction` contract on the `TestMatrix` artifact type — required Functional Requirement Coverage + Test Case Summary tables, `Test ID` id pattern, `column_choices` on Type/Priority/Status, `column_patterns` on Traces To, optional StR/US/NFR tables, `multiple: true` records.
  - Constraint **FR-003-CON-1**: normalize-before-enforce — the enforcing module version SHALL NOT be published until an ecosystem `tests.md` sweep has produced per-repo diffs and the user has signed off.

### Explicit Non-Scope
- **No quire-rs engine work.** `column_choices` / `column_patterns` table asserts already exist (quire-rs FR-033, CR-010). This plan is manifest **data** + fixtures/tests + rollout choreography only.
- FR-001 / FR-002 implementation (already shipped). Executing FR-002's planned matrix coverage (TC-019..TC-023, added closing TM-001 GAP-001 / SR-001 FND-002) is likewise outside this plan.
- **FR-003-AC-11 enforcement (TC-024).** Test ID uniqueness is normative in FR-003, but quire-rs exposes no uniqueness assert (`LocatorAssert`/`assert_eval` verified 2026-08-04) — enforcement is blocked on an external quire-rs engine capability and is explicitly NOT delivered by this plan (no engine work). TC-024 stays ⚠️ blocked in TM-001.

## Dependency Graph

### Core dependency edges
- `FR-001 -> FR-003`
  Reason: manifest activation is the carrier — the `body_extraction` contract ships inside the already-activating manifest.
- `quire-rs FR-033 -> FR-003`
  Reason: the contract's `column_choices`/`column_patterns` asserts are engine capabilities; already released, consumed as-is.
- `quire-rs uniqueness assert (does not exist yet) -> FR-003-AC-11 / TC-024`
  Reason: external dependency, mirroring the FR-033 pattern — AC-11 (Test ID uniqueness) cannot be machine-enforced until quire-rs ships an id-uniqueness table assert; tracked as a capability request, out of this plan's scope.
- `FR-003 (contract exists) -> FR-003-CON-1 sweep`
  Reason: the sweep validates ecosystem `tests.md` files against the candidate contract, so the contract must exist (locally, unpublished) first.
- `FR-003-CON-1 sign-off -> enforcing publish`
  Reason: normative rollout gate — publishing before sign-off violates the constraint.

### Shared dependencies
- **Fixture corpus + validation harness** (conforming and drifted `TestMatrix` fixture docs, pytest wrapper around `quire validate` with this module active) is used by every test task and by the sweep tooling. Built once in Task-001.

### Cross-cutting constraints
- `FR-003-CON-1` applies to the release path only — local development, fixtures, and this repo's own `spec/tests.md` may adopt the shape immediately.
- FR-003-AC-9 applies to every manifest edit in this plan: the TestMatrix frontmatter schema and all other archetypes stay byte-identical.

## Test Plan

The authoritative test enumeration is the Test Matrix (`spec/tests.md`, TM-001,
TC-001..TC-018). Grouping by target:

### Unit Tests (fixtures + `quire validate` harness)
- [ ] **test_conforming_matrix_validates_and_extracts** (TC-001: FR-003-AC-1, FR-003-AC-8)
- [ ] **test_missing_required_tables_fail** (TC-002, TC-003: FR-003-AC-2)
- [ ] **test_type_vocabulary_pass_and_fail** (TC-004, TC-005: FR-003-AC-3)
- [ ] **test_test_id_shapes_pass_and_fail** (TC-006, TC-007: FR-003-AC-4)
- [ ] **test_status_markers_pass_and_fail** (TC-008, TC-009: FR-003-AC-5)
- [ ] **test_priority_vocabulary_pass_and_fail** (TC-010, TC-011: FR-003-AC-10)
- [ ] **test_traces_to_tokens_pass_and_fail** (TC-012, TC-013, TC-018: FR-003-AC-6)
- [ ] **test_optional_tables_omitted_or_malformed** (TC-014, TC-015: FR-003-AC-7)
- [ ] **test_min_rows_boundary** (TC-016: FR-003-AC-1, FR-003-AC-2)
- [ ] **test_manifest_scope_unchanged** (TC-017: FR-003-AC-9 — manifest diff assertion complementing Inspection)
- [ ] **test_duplicate_test_id_rejected** (TC-024: FR-003-AC-11 — ⚠️ BLOCKED: requires the quire-rs uniqueness assert; do not scaffold until the engine capability exists)

### Verification (process constraint)
- [ ] **verify_normalize_before_enforce** (FR-003-CON-1): Inspection — sweep report with per-repo diffs exists and user sign-off is recorded BEFORE the enforcing version is tagged/published.

## Remaining Work

### Remaining Dependency Graph
```
Task-001 (fixtures + red tests)
   └─> Task-002 (manifest body_extraction → green)
          ├─> Task-003 (AC-9 guard + self-validation)  ──> [Gate: contract green]
          └─> Task-004 (Track S: ecosystem sweep + diffs)
                 └─> Task-005 (Gate: user sign-off — FR-003-CON-1)
                        └─> Task-006 (Track C: publish enforcing version)
```

### Track A: Critical Path (serial)
#### A1: Task-001 — Fixture corpus + failing tests (TDD red)
- **Scope:** Conforming + drifted `TestMatrix` fixtures and a pytest harness driving `quire validate` with this module's manifest; encodes TC-001..TC-016 + TC-018 as failing tests (contract not yet in manifest).
- **Difficulty:** Medium
- **Estimated new code:** ~300 lines (fixtures + tests)
- **Exit criteria:** Suite runs; contract-dependent tests red for the documented reason; harness reusable by the sweep.

#### A2: Task-002 — Manifest `body_extraction` contract (TDD green)
- **Scope:** Add the `body_extraction` block to the `TestMatrix` artifact_type in `spec_artifacts_process/manifest.yaml` exactly per FR-003 Behavior (mirroring the SpecReview precedent).
- **Difficulty:** Easy
- **Estimated new code:** ~40 lines of manifest data
- **Exit criteria:** TC-001..TC-016, TC-018 green; no other manifest entry touched.

#### A3: Task-003 — AC-9 guard + repo self-validation
- **Scope:** TC-017 manifest-scope assertion; this repo's own `spec/tests.md` validates under the new contract; wheel/packaging check.
- **Difficulty:** Easy
- **Estimated new code:** ~60 lines
- **Exit criteria:** Full suite green including TC-017; `quire validate` clean on this repo.

#### Gate: Contract green
- **Measures:** All TC-001..TC-018 pass; this repo self-validates under the candidate contract.
- **Pass criteria:** `make test` green; `quire validate --scope . "spec/**/*.md"` error-free.
- **If fails:** Fix contract data or FR-003 spec drift before any sweep or publish work.

### Track S: Ecosystem normalization sweep (separate track; parallel after A2)
#### S1: Task-004 — Sweep ecosystem `tests.md` files, produce per-repo diffs
- **Scope:** Enumerate ecosystem repos' `spec/tests.md`, validate each against the candidate contract via the Task-001 harness, generate normalization diffs per repo; report only — **no repo edits without sign-off**.
- **Difficulty:** Medium
- **Exit criteria:** Sweep report: repo list, pass/fail per repo, per-repo diff artifacts ready for review.

#### Gate: Task-005 — User sign-off (FR-003-CON-1)
- **Measures:** User has reviewed the sweep diffs and approved normalization + enforcement.
- **Pass criteria:** Explicit user sign-off recorded (per-repo or blanket).
- **If fails:** Adjust contract strictness or normalization diffs per feedback; re-run sweep; do NOT publish.

### Track C: Post-Gate (release)
#### C1: Task-006 — Publish the enforcing module version
- **Scope:** Apply signed-off normalizations (or confirm repos normalized), bump module version, publish/activate per repo release convention; re-verify activation (IT-001 path).
- **Difficulty:** Easy
- **Exit criteria:** Enforcing version published only after Task-005 sign-off; activation roundtrip green.

## Parallel Execution Summary

```
Track A: [Task-001] -> [Task-002] -> [Task-003] -> (Gate: contract green)
Track S:                  └────────> [Task-004] -> [Task-005: user sign-off]
Track C:                                                  └───> [Task-006 publish]
```
Track S starts as soon as Task-002 lands (needs the candidate contract); Task-003
and Task-004 can run in parallel. Track C is strictly post-gate.

## Task File Mapping

| Task | Track | Owns | Verifies | Status |
|------|-------|------|----------|--------|
| Task-001 | A | FR-003 (fixtures/tests) | TC-001..TC-016, TC-018 | not_started |
| Task-002 | A | FR-003 (manifest contract) | TC-001..TC-016, TC-018 | not_started |
| Task-003 | A | FR-003-AC-9, self-validation | TC-017 | not_started |
| Task-004 | S | FR-003-CON-1 (sweep) | FR-003-CON-1 (Inspection input) | not_started |
| Task-005 | Gate | FR-003-CON-1 (sign-off) | FR-003-CON-1 | not_started |
| Task-006 | C | Enforcing release | IT-001 | not_started |

## Coordination Rules

- **Freeze FR-003's contract shape** during implementation; spec changes re-enter via review, not ad-hoc manifest edits.
- **Single writer on `manifest.yaml`** (Task-002/Task-003 only); the sweep never edits this repo's manifest.
- **Task-004 is read-only across the ecosystem**: it produces diffs, never applies them; application happens post-sign-off (Task-006 scope or per-repo follow-ups as the user directs).
- **Hard stop at Task-005**: no version bump, tag, or publish of the enforcing module before recorded user sign-off (FR-003-CON-1).
- **No quire-rs changes** anywhere in this plan; if a needed assert is missing, that is a spec finding, not an engine patch from this plan.
