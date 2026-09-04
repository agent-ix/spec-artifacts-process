---
id: Task-014
title: "GATE — NFR-001: the baseline diff and the two-consumer measurement"
type: Task
status: done
track: C
priority: P0
relationships:
  - target: ix://agent-ix/spec-artifacts-process/NFR-001
    type: references
  - target: ix://agent-ix/spec-artifacts-process/TC-127
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-128
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-129
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-130
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-131
    type: verifies
---
# Task-014: GATE — NFR-001: the baseline diff and the two-consumer measurement

## Scope

The safety gate of the whole ticket. A green local suite is not evidence for a module every
repository validates against.

## Subtasks

- [ ] Structural diff of every declaration class against `tests/fixtures/baseline-0.1.0/`: archetypes, artifact types, object types, grammars, doc kinds, traceability, lint rules, verification catalog.
- [ ] No vocabulary gains or loses a member; every added locator is `required: false`.
- [ ] Every shipped skeleton validates under 0.2.0 with zero error findings.
- [ ] **The consumer measurement.** For `spec-objects-business` and `filament-core-data`: record the commit SHA, run `quire validate --scope <repo> "spec/**/*.md"` with this module at 0.1.0 and again at 0.2.0, and compare the finding sets as a **difference**. A consumer already red for its own reasons contributes to both sides and therefore to neither. Record the commits and both counts in the plan log.
- [ ] Record the residual: two consumers of roughly 239. The measurement is a floor, not a proof, and the advisory posture plus human promotion cover the rest.

## Gate criterion

Zero changed 0.1.0 declarations, zero vocabulary movement, and an empty set difference for both
consumers. Anything else stops the merge.
