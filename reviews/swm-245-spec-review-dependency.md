---
id: SR-20261115175478
title: "SWM-245 PR164 spec-review dependency"
type: SpecReview
analysis: dependency
scope: "agent-ix/spec-artifacts-process PR164; spec/functional/FR-020-rolespec-archetype.md, spec/functional/FR-021-rolespec-trace-and-cross-row-checks.md, spec/functional/FR-022-rolespec-lint-ownership.md, spec/usecase/US-004-author-role-specs-that-validate.md"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-020", type: references}
  - {target: "ix://agent-ix/spec-artifacts-process/FR-021", type: references}
  - {target: "ix://agent-ix/spec-artifacts-process/FR-022", type: references}
---

## Summary

Ticket: SWM-245. Dependency review of the new `relationships:` edges and the `## Dependencies` sections.

The new edges are:

- `satisfies` US-004 from each FR.
- `depends_on` FR-001 (FR-020), FR-004 and FR-020 (FR-021), and FR-020 and FR-021 (FR-022).
- `implements` dev-team FR-006 and FR-007.
- `traces_to` StR-001 and dev-team US-002 (US-004).

None is circular, and the order FR-020, then FR-021, then FR-022 is sound. External enablement is SWM-247 (engine capabilities 1 and 2) and SWM-248 (capabilities 3 and 4); both exist in Linear under "Fleet W4: Role specs and evaluation".

## Verdict

**CHANGES REQUIRED.** The internal ordering is sound. The external dependencies that block implementation are not linked: the quire-rs tickets, the Quoin ticket, and the dev-team installation.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-021 does not link the engine-gap tickets. Its Dependencies say only "quire-rs capabilities 1 to 5 above, tracked as quire-rs tickets". FR-021-AC-9 requires "a ticket for the capability is linked from this requirement", so the FR fails its own inspection AC as written. SWM-247 covers capabilities 1 and 2, and SWM-248 covers 3 and 4; both should be named next to the capabilities and in Dependencies. Capability 5 should be dropped in favour of the `Rubric` archetype (see the base review, FND-001). | spec/functional/FR-021-rolespec-trace-and-cross-row-checks.md:44-48,62,69 |
| FND-002 | medium | The Quoin dependency is untracked. FR-022 assigns the version-bump and skill-citation checks to Quoin, which matches lead decision 2, but the Dependencies list "ticket to be filed in the Quoin project". The SWM-245 checklist item for these checks counts as "explicitly assigned elsewhere" only once that ticket exists and is linked. | spec/functional/FR-022-rolespec-lint-ownership.md:40 |
| FND-003 | medium | The dev-team installation dependency is not stated. Lead decision 5 requires dev-team to install this module to validate `spec/roles/`. FR-022 says only "with this module installed" in passing, and no Dependencies entry or US-004 context records that dev-team must install the module and pin it. | spec/functional/FR-022-rolespec-lint-ownership.md:26,41 |
| FND-004 | low | FR-020's Dependencies name FR-009, FR-011 and FR-012, but its frontmatter `relationships:` declares only `depends_on` FR-001. Traceability tooling reads the frontmatter, so the three mechanics FR-020 relies on are not visible as edges. | spec/functional/FR-020-rolespec-archetype.md:5-11,68 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-005 | low | FR-023 relies on FR-011 (the mapping entry) and FR-012 (the skeleton), as its Behavior at line 40 says, but its frontmatter declares `depends_on` only to FR-020 and FR-004, and its Dependencies list neither. This is the same gap FND-004 found in FR-020, which round 1 fixed. | spec/functional/FR-023-rubric-archetype.md:5-13,40,54 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1 (head 23335ff): FR-021 names SWM-247 for capabilities 1 and 2 and SWM-248 for capabilities 3 and 4, in the Description, in each capability item and in Dependencies. Capability 5 is removed. |
| FND-002 | fixed | Round 1: FR-022 cites SWM-249, which exists in Linear ("Quoin: RoleSpec version-bump-vs-base and skill-citation checks"), in its Behavior and Dependencies. |
| FND-003 | fixed | Round 1: the Dependencies of FR-021 and FR-022 state that dev-team installs this module and pins the version it installs. FR-023 states the same for rubrics. |
| FND-004 | fixed | Round 1: FR-020 frontmatter adds `depends_on` FR-009, FR-011 and FR-012. |
| FND-005 | fixed | Round 2 (head cf82041): FR-023 frontmatter adds `depends_on` FR-011 and FR-012, and its Dependencies list both, for the `Rubric` mapping entry and skeleton. |
