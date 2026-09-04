---
id: Task-009
title: "FR-009 + FR-013 — one model per artifact type, with the definition/occurrence rule as an authoring gate"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-artifacts-process/FR-009
    type: references
  - target: ix://agent-ix/spec-artifacts-process/FR-013
    type: references
  - target: ix://agent-ix/spec-artifacts-process/TC-080
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-082
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-086
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-120
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-121
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-122
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-123
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-124
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-143
    type: verifies
---
# Task-009: FR-009 + FR-013 — one model per artifact type, with the definition/occurrence rule as an authoring gate

## Scope

Twelve exported models — `ADR`, `Plan`, `Task`, `Review`, `SpecReview`, `Finding`, `Feedback`,
`TestMatrixIndex`, `TestMatrix`, `Standard`, `SuiteRegistry`, `Inspections` — plus the support
models their rows need, every one derived from what the archetype's `body_extraction` already
extracts plus the frontmatter identity, relationships and provenance.

FR-013 is enforced **while** these are authored, not after. Tasked downstream it becomes an audit
of a decision already made, and the cheapest way to pass an audit is to weaken it (SR-009 FND-001).

## Subtasks

- [ ] Scalars mirroring the frontmatter schemas exactly — the id patterns, the `Status` marker set, the `Traces To` pattern, the test-id shape, the `Type`/`Priority`/`Severity`/`Escape Cause`/`Verdict`/`analysis`/`review_set` vocabularies — each copied from `manifest.yaml`, never reinvented.
- [ ] Support models for every asserted table: findings rows, the five matrix coverage tables, the subsystem index, the integration matrix, the gap register, suite rows, inspection rows, the feedback anchor and its two selectors.
- [ ] `Standard` carries `properties: FieldDecl[]` and `invariants: ClauseRef[]`, both optional, imported from semantic-core.
- [ ] Every field carries a constraint; where a field is free text the doc comment says `free text:` and why.
- [ ] **Role gate**: each model is annotated `definition` or `evidence-act` as it is written, and no model gains a property naming a run id, timestamp, duration, pass/fail count, log location or run artefact. Enforce with a name-lexicon test (TC-121) and record the meaning half as an Inspection with a named reviewer (TC-143).
- [ ] Run `make schemas`; the emitted set is exactly what `toolchain.json` lists.

## Deliverables

`semantic/main.tsp` complete, `spec_artifacts_process/schemas/<Model>.json` for every model.

## Notes

`Finding` and the `FND-` rows inside a `SpecReview` stay separate namespaces (`FIND-` / `FND-`).
Giving them one prefix would read as unification and be a conflation.
