---
id: Task-017
title: "FR-007-AC-15 — declare and check the differential method"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-artifacts-process/FR-007
    type: references
  - target: ix://agent-ix/spec-artifacts-process/TC-144
    type: verifies
---
# Task-017: FR-007-AC-15 — declare and check the differential method

## Scope

Add one exact `differential-testing` catalogue entry and a Rust acceptance target that checks its identity, comparison semantics and claim ceiling from the authoritative manifest bytes.

## Subtasks

- [x] Add the exact method data without altering a pre-existing catalogue entry.
- [x] Add a Rust 1.98.1 test-only Cargo target with bare `ix-trace-rs` tags.
- [x] Check the 34-method census, every identity-bearing field and the complete definition claim ceiling.
- [x] Prove an accepted extension to an unrelated catalogue entry cannot make TC-144 fail before it reaches the differential contract.
- [x] Run bounded format, Clippy and test gates and apply the exact Rust review.

## Deliverables

- `spec_artifacts_process/manifest.yaml` differential method declaration.
- `rust-tests/catalogue_contract.rs` TC-144 acceptance tests.
- `reviews/2026-09-10-differential-catalogue-rust-review.md` checkpoint review.

## Notes

- The checkpoint does not implement or claim Quoin selection behavior; Tasks 018 and 019 own those integration cases.
