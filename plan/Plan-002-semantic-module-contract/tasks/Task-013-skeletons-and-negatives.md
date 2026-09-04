---
id: Task-013
title: "FR-012 — twelve executable skeletons, the Standard sysml alternate, and the negative corpus"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-artifacts-process/FR-012
    type: references
  - target: ix://agent-ix/spec-artifacts-process/TC-111
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-112
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-113
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-114
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-115
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-116
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-117
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-118
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-119
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-141
    type: verifies
---
# Task-013: FR-012 — twelve executable skeletons, the Standard sysml alternate, and the negative corpus

## Scope

Eight new skeletons beside the four the module already ships, the `Standard` typed-declaration
pair, and one negative fixture per stated rejection.

## Subtasks

- [ ] `ADR.md`, `Plan.md`, `Task.md`, `Review.md`, `Finding.md`, `TestMatrixIndex.md`, `TestMatrix.md`, `Standard.md` — each valid against its own archetype as authored, with every required section and every asserted table satisfying its locator.
- [ ] `Standard.md` carries the typed `## Properties` table (`Field | Type | Multiplicity | Constraints`) and an `## Invariants` section with at least one `### <clauseId>` holding one ```ocl fence; `Standard.sysml.md` declares the same fields in one ```sysml fence. The two must map to records that differ in no property.
- [ ] Exactly one skeleton carries `## Properties`, and it is `Standard.md` (TC-141). No other type gains a section, because a new required form on a type consuming repositories already author is the breaking change NFR-001 forbids.
- [ ] Add the two `Standard` locators to the manifest, both `required: false`.
- [ ] Eleven negative fixtures under `tests/fixtures/negative/`, each with `expect:` and `because:`: missing required section; zero-row required table; id outside `id_pattern`; cell outside `column_choices`; `Status` outside the four markers; `Traces To` the pattern rejects; dropped required column; duplicate row id; both declaration forms; a clause subsection with no fence; a clause id that is not an `Identifier`.
- [ ] Packaging: nothing under `tests/fixtures/` reaches the wheel, the sdist or the staged npm tree, and `quire coverage` over this repository mints no id from it (TC-119, Integration).

## Deliverables

Twelve `skeletons/<Type>.md` plus `Standard.sysml.md`, `tests/fixtures/negative/*.md`,
`tests/test_skeletons.py`.
