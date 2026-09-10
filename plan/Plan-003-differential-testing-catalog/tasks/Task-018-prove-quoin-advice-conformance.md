---
id: Task-018
title: "FR-007-AC-16 — prove Quoin catalogue and advice conformance"
type: Task
status: blocked
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-artifacts-process/Task-017
    type: depends_on
  - target: ix://agent-ix/spec-artifacts-process/FR-007
    type: references
  - target: ix://agent-ix/spec-artifacts-process/TC-145
    type: verifies
---
# Task-018: FR-007-AC-16 — prove Quoin catalogue and advice conformance

## Scope

Use Engineering Assurance's accepted typed Rust process producer to execute exact pinned Quoin catalogue and advice commands over a closed module set, then evaluate Quoin's structured results in a Rust TC-145 consumer.

## Subtasks

- [ ] Bind the accepted Engineering Assurance producer without a repository-local process runner, verdict scraper or evidence store.
- [ ] Freeze executable revision/digest, argv, repository/module identities, environment allowlist and resource bounds in the test input.
- [ ] Assert the reference-equivalence obligation selects `differential-testing` for that exact reason with all catalogue metadata preserved.
- [ ] Assert property-only, metamorphic-only and integration-only controls do not select the method.
- [ ] Refuse non-completed producer states and malformed catalogue/advice payloads without fabricating a conformance result.
- [ ] Carry bare `ix-trace-rs` bindings for TC-145, FR-007-AC-16 and FR-007-CON-1.

## Deliverables

- Rust TC-145 fixture corpus and strict readers.
- Reproducible local execution evidence for the exact pinned Quoin producer configuration.

## Notes

- **External blocker:** `agent-ix/engineering-assurance#34` has not yet published the accepted typed Rust process-execution result this task consumes.
- Quoin owns catalogue/advice semantics. Engineering Assurance owns process execution. This module owns only the acceptance consumer and its fixtures.
