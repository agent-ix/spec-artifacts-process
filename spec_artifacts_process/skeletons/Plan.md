---
id: Plan-001
title: "Example plan — checksum verification on artifact import"
type: Plan
status: active
relationships:
  - target: "ix://agent-ix/example/FR-001"
    type: "references"
---
<!-- Plan authoring skeleton (spec-artifacts-process). Fill every section with
     substantive content. Contract:
     - Frontmatter: `type: Plan`; `id` matches ^[A-Za-z]{2,4}-[0-9]+$
       (Plan-001 — mixed case, which is why the pattern is not upper-only).
     - The archetype declares NO `body_extraction`, so no section is asserted.
       The sections below are the convention `spec-to-plan` emits.
     - `allowed_links`: contains | depends_on | references.
     - `composition.expected_artifacts` is `Task`: a plan is a bundle
       (`plan/<Plan-id>-<slug>/`) holding this file, an index, a log and a
       `tasks/` directory.
     - A Plan is an authored DEFINITION. It records what is to be done, never
       what a run of it produced: no start time, no outcome, no duration
       (FR-013). -->
# Implementation Plan: checksum verification on artifact import

## Requirements Summary

- [ ] **FR-001**: verify the SHA-256 of every imported artifact before persisting it.

## Dependency Graph

- `FR-001 (digest computation) -> FR-001 (rejection path)` — nothing can be
  rejected for a mismatch until a digest is computed.

## Quality Gates

**Gate 1** — a mismatched digest is refused end to end before the happy path is
optimised. A rejection that does not fire is the whole failure mode.

## Execution Tracks

- **Track A**: Task-001 (digest computation) → Task-002 (rejection path).

## Test Plan

The Test Matrix in `spec/tests.md` is authoritative. This plan adds no test id;
each task's frontmatter `verifies` edges name the rows it discharges.
