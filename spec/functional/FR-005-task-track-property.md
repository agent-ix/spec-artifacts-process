---
id: FR-005
title: "Task `track` property: the declared contract for parallel execution tracks"
type: FR
relationships:
  - target: "ix://agent-ix/filament-ide-rs/FR-043"
    type: "references"
---
# FR-005: Task `track` property: the declared contract for parallel execution tracks

## Description

The Task artifact type **SHALL** declare `track` as an optional string property, so the
grouping label the ecosystem already authors on plan tasks validates against a *declared*
property rather than through the schema's `additionalProperties: true`.

The property is not new to the corpus — it is new to the contract. A sweep of `~/dev` found
230 task files carrying `track:` across this repo, `filament-ide-rs` and `filament-plan-sync`.
Every one of them validates today, and none of them is checked: an undeclared key passes
because the schema admits any key, which is the same unchecked door an invented `tracks:`
frontmatter map went through in `filament-ide-rs` before being removed (SR-074 FND-002/FND-004,
agent-ix/filament-ide-rs#232). `quire validate` returning 0 is not evidence a key is sanctioned;
this requirement makes it evidence.

## Inputs

- `schemas/task-frontmatter.schema.json` (this module's Task frontmatter contract)
- A plan bundle's task documents, which author `track:` values

## Outputs

- A `track` value that is validated when authored: present or absent, but never empty and
  never a non-string

## Behavior

- The Task frontmatter schema **SHALL** declare `track` with `type: string` and
  `minLength: 1`, and **SHALL NOT** add it to `required`. A plan whose tasks are serial has
  no tracks, and a task outside a plan bundle has no track to name.
- The property **SHALL NOT** constrain its values to an enumeration. Observed values across
  the ecosystem are `A`–`F`, plus `S` and `G`. An enum of letters re-creates the naming
  machinery SR-074 FND-001 removed and breaks the first time a repo names a track something
  legible; `minLength: 1` is the whole contract, and what a track *means* is the plan's job.
- This module **SHALL NOT** declare a `Track` archetype or artifact type. A track is a
  property of a Task. A consumer that needs a tree node — the four-level tracker mapping
  `Spec → Plan → Track → Task` — **synthesizes** that node from this value; that promotion is
  specified by the consumer ([filament-ide-rs FR-043](ix://agent-ix/filament-ide-rs/FR-043),
  FR-060), not by a document type here.
- `additionalProperties` on the Task schema **SHALL** remain `true`. Narrowing it is a
  separate, breaking change against every task file in the ecosystem and is not in scope.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-005-AC-1 | The Task frontmatter schema declares `track` as an optional string with `minLength: 1`, and `track` is absent from `required` | Test (TC-037) |
| FR-005-AC-2 | A task declaring `track: C` validates against the schema; `track: ""` and a non-string `track` fail | Test (TC-037) |
| FR-005-AC-3 | Scope guard: the manifest declares no `Track` archetype and no `Track` artifact type, and the Task artifact type's `allowed_links` and `defaults` are unchanged | Test (TC-038) |

> **CR-026 note (2026-08-15):** The competing design — `Track` as a first-class archetype with
> `Plan contains [Track, Task]` — was proposed as agent-ix/spec-artifacts-process#9 and is
> closed unmerged. It was adjudicated in `filament-ide-rs` SR-074
> (`reviews/2026-07-31-tracks-manifest-removal.md`, issue #232), whose FND-001 found three
> shapes competing for one concept: a `track:` letter on a Task, a nodal `Track` artifact, and
> a plan-local name map. Two were removed and the property won.
>
> **The evidence for the property form is that nothing ever authored the other one.** Zero
> `type: Track` documents exist in any repo. The consumer that motivated the archetype —
> the `filament-plan-sync` Jira driver, which maps `Spec → Initiative, Plan → Epic,
> Track → Story, Task → Sub-task` — already carries `Level = 'Spec' | 'Plan' | 'Track' | 'Task'`
> in its own model and never needed a document type to do it. A four-level mapping needs a
> four-level *tree*, and the tree is derived; it does not need a fourth kind of file on disk.
>
> **What the archetype would have cost.** A `Track` artifact makes every plan bundle grow a
> file per track, makes track membership a `contains` link that can disagree with the `track:`
> value on the Task, and gives the ecosystem a second place to say the same thing. SR-074
> FND-003 records the concrete failure mode: the only definition of a `Track` archetype that
> ever existed on disk was a stale, gitignored build artifact, and a reviewer read it as the
> module contract.

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md) (the manifest that carries the
  Task artifact type and its schema reference)
- **Downstream**: `filament-ide-rs` [FR-043](ix://agent-ix/filament-ide-rs/FR-043) and FR-060,
  which read this property and synthesize the Track node the tracker mapping needs

## Known Limits

- Declaring the property does not make it *checked against a plan*: nothing verifies that a
  task's `track` names a track the plan actually declares, because a plan declares its tracks
  in prose. Consumers that need that check derive the track set from the tasks themselves.
- `additionalProperties: true` still admits every other invented key on a Task. This
  requirement closes the door for one property, not the doorway.
