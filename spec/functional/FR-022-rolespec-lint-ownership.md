---
id: FR-022
title: "RoleSpec checks that need history or other files: owner, and the worked example gate"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-004"
    type: "satisfies"
  - target: "ix://agent-ix/spec-artifacts-process/FR-020"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-021"
    type: "depends_on"
  - target: "ix://agent-ix/dev-team/FR-007"
    type: "implements"
---
# FR-022: RoleSpec checks that need history or other files: owner, and the worked example gate

## Description

Two lint checks in [dev-team FR-007](ix://agent-ix/dev-team/FR-007) read something other than the role-spec document: the version bump compares against a base git revision, and the skill citation scan reads skills' frontmatter. A Quire module validates documents and holds no git or cross-repository state; Quoin already owns checks over git history (anomaly transition legality, quoin FR-136). This requirement assigns both checks to Quoin so this module carries only the archetype, and records the acceptance gate that the worked example validates.

## Behavior

- Version bump against base: owned by Quoin, not this module. For a `RoleSpec` whose Metrics, Objectives, Rules or Evaluations rows differ from the merge base with the default branch, Quoin SHALL require a strictly higher `version` and name the changed table. Deleting a rule with its evaluations requires the same bump.
- Skill citation scan: owned by Quoin, not this module. For each skill whose frontmatter has `role_spec_version`, Quoin SHALL report any cited rule id absent from the role spec at that version, read from the base history of the role spec, and fail.
- This module SHALL declare for the `RoleSpec` archetype that `version` is the field these checks read, and SHALL implement neither check.
- The worked example `docs/examples/minder-role-spec.md` in dev-team, once moved to `spec/roles/minder.md`, SHALL validate with exit code 0 under `quire validate --scope . "spec/**/*.md"` with this module installed, and a copy ships in this module's examples as the positive fixture for FR-020 and FR-021.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-022-AC-1 | The dev-team minder role spec at `spec/roles/minder.md`, validated with this module installed, exits 0 and reports no error. | Test |
| FR-022-AC-2 | This repository contains no code that compares a role spec with a base revision or scans skill frontmatter. | Inspection |
| FR-022-AC-3 | The module's `RoleSpec` documentation names Quoin as the owner of the version-bump and skill-citation checks and names `version` as the field they read. | Inspection |
| FR-022-AC-4 | A copy of the worked minder spec is the module's positive `RoleSpec` fixture and validates with the module's own `quire validate`. | Test |

## Dependencies

- [FR-020](./FR-020-rolespec-archetype.md) and [FR-021](./FR-021-rolespec-trace-and-cross-row-checks.md).
- Quoin, the owner of the version-bump and skill-citation checks (ticket to be filed in the Quoin project).
- dev-team FR-007 and the move of the worked example (dev-team#30).
