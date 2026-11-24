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

- Allocation, version bump against base: the check is allocated to Quoin (SWM-249). A change to any Metrics, Objectives, Rules or Evaluations row against the merge base with the default branch needs a strictly higher `version`, and a rule deleted with its evaluations needs the same bump. This module states the check and does not implement it.
- Allocation, skill citation scan: the check is allocated to Quoin (SWM-249). A cited rule id absent from the role spec at the skill's `role_spec_version` is reported and fails the lint. This module states the check and does not implement it.
- This module SHALL NOT contain code that compares a role spec with a base revision or reads skill frontmatter.
- The `RoleSpec` documentation in this module SHALL name `version` as the field these checks read and Quoin as their owner.
- The dev-team repository SHALL validate the worked example `docs/examples/minder-role-spec.md`, once moved to `spec/roles/minder.md`, with exit code 0 under `quire validate --scope . "spec/**/*.md"` with this module installed.
- This module SHALL ship a copy of the worked example as the positive fixture for FR-020 and FR-021.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-022-AC-1 | Run in the dev-team repository with this module installed, `quire validate --scope . "spec/**/*.md"` over `spec/roles/minder.md` exits 0 and reports no error. | Demonstration |
| FR-022-AC-2 | This repository contains no code that compares a role spec with a base revision or scans skill frontmatter. | Inspection |
| FR-022-AC-3 | The module's `RoleSpec` documentation names Quoin as the owner of the version-bump and skill-citation checks and names `version` as the field they read. | Inspection |
| FR-022-AC-4 | A copy of the worked minder spec is the module's positive `RoleSpec` fixture and validates with the module's own `quire validate`. | Test |

## Dependencies

- [FR-020](./FR-020-rolespec-archetype.md) and [FR-021](./FR-021-rolespec-trace-and-cross-row-checks.md).
- SWM-249, the Quoin ticket for the version-bump and skill-citation checks.
- dev-team FR-007 and the move of the worked example (dev-team#30).
- dev-team installs this module to validate `spec/roles/`, and pins the module version it installs.
