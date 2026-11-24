---
id: FR-020
title: "RoleSpec archetype: a role as typed tables of metrics, objectives, rules and evaluations"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-004"
    type: "satisfies"
  - target: "ix://agent-ix/spec-artifacts-process/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-011"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-012"
    type: "depends_on"
  - target: "ix://agent-ix/dev-team/FR-006"
    type: "implements"
---
# FR-020: RoleSpec archetype: a role as typed tables of metrics, objectives, rules and evaluations

## Description

The module SHALL declare the artifact type `RoleSpec` so that a role spec at `spec/roles/<role>.md` ([dev-team FR-006](ix://agent-ix/dev-team/FR-006)) validates under `quire validate`. A role spec says what a role is for, which behavior it requires or forbids, and how each statement is checked. Giving it an archetype means a malformed role spec fails before any evaluator reads it, and the vocabularies the evaluator relies on (evidence source, method, cadence, comparator) have one declared home rather than one copy per consumer.

This requirement covers the document shape and the checks that read one row or one field. Checks that relate rows to each other, including the all-judgement warning, are [FR-021](./FR-021-rolespec-trace-and-cross-row-checks.md). Rubrics that judgement evaluations cite are [FR-023](./FR-023-rubric-archetype.md). Checks that need git history or other files are [FR-022](./FR-022-rolespec-lint-ownership.md).

## Inputs

- A Markdown file with `type: RoleSpec`.

## Outputs

- Frontmatter members: `id` (the role's rule prefix, for example `MIND`), `role`, `version` (a positive integer) and `relationships`.
- Four required sections, each a table with a stable id column: `Metrics`, `Objectives`, `Rules`, `Evaluations`.
- A skeleton for `RoleSpec` (FR-012) and a frontmatter schema.

## Behavior

- The `RoleSpec` frontmatter schema SHALL require `id`, `role`, `version` and `type`.
- The `RoleSpec` frontmatter schema SHALL accept `id` only as an upper-case prefix of 2 to 6 letters.
- The `RoleSpec` frontmatter schema SHALL accept `version` only as an integer of at least 1.
- The `RoleSpec` manifest entry SHALL declare `allowed_links` of `satisfies`, `depends_on` and `implements`.
- The `RoleSpec` archetype SHALL accept sections other than the four tables, such as `Purpose`. The archetype asserts nothing about those sections.
- The `RoleSpec` archetype SHALL require the four tables, each with exactly these columns in order:
  - `Metrics`: `ID`, `Name`, `Evidence source`, `Query`, `Unit`, `Target`, `Direction`.
  - `Objectives`: `ID`, `Objective`, `Metrics`.
  - `Rules`: `ID`, `Rule`, `Objective`, `Class`, `Source`.
  - `Evaluations`: `ID`, `Rule`, `Evidence source`, `Trigger`, `Method`, `Query or rubric`, `Evaluator`, `Comparator`, `Value`, `Unit`, `Cadence`.
- Each table SHALL require at least one row.
- Row ids SHALL match, with the frontmatter `id` interpolated as the prefix: metrics `^<id>-M\d{2}$`, objectives `^<id>-O\d{2}$`, rules `^<id>-R\d{2}$`, evaluations `^<id>-R\d{2}-E\d+$`. An id whose prefix differs from the frontmatter `id` fails.
- The `Evidence source` columns (metrics and evaluations) SHALL accept only `ledger`, `relay-receipts`, `hook-events`, `linear`, `github`, `transcript` or `ix-board-metric`.
- `Direction` SHALL accept only `higher` or `lower`. `Method` SHALL accept only `deterministic` or `judgement`. `Cadence` SHALL accept only `tick`, `session-end`, `3h`, `daily` or `weekly`. `Comparator` SHALL accept only `<`, `<=`, `=`, `>=` or `>`.
- A query reference is the id of a query registered with the evaluator (`ix-board retro eval`, SWM-221), written as `<source>.<name>` with a lower-case `<source>` and a lower-case snake_case `<name>`, for example `ledger.unknown_lane_ticks`. The `RoleSpec` archetype SHALL assert the pattern `^[a-z][a-z0-9-]*\.[a-z][a-z0-9_]*$` for every query reference. Whether the id is registered is the evaluator's binding check, not this module's.
- The `Query` column of a metric and the `Trigger` column of an evaluation SHALL each hold a query reference, because dev-team FR-006 defines a trigger as a deterministic query reference.
- The `Value` column SHALL hold a number.
- The `Unit` column SHALL be non-empty, so a threshold is always comparator, value and unit.
- The `RoleSpec` record schema SHALL apply the following to each evaluation row and report the failures in the same run as the shape checks. For a `deterministic` row, `Evaluator` is `evaluator` and `Query or rubric` is a query reference. For a `judgement` row, `Evaluator` is `director` or `team-retro`, `Query or rubric` has the form `<rubric>@<version>#<check-slug>`, and `Cadence` is not `tick`.
- The enum vocabularies SHALL be declared once in the archetype's schema and mirrored by no other declaration in the module.
- The module SHALL ship `RoleSpec` as a validated archetype in `manifest.yaml`, with a schema for the emitted record projected from the TypeSpec source (FR-009) and an entry in the markdown mapping (FR-011) with role `definition`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-020-AC-1 | A complete role spec with all four tables validates; removing the `Evaluations` table, any required column, or `version` fails with a diagnostic naming the missing element. | Test |
| FR-020-AC-2 | An evaluation with an evidence source outside the closed list, a cadence outside `tick`, `session-end`, `3h`, `daily`, `weekly`, or a method other than `deterministic` or `judgement` fails, each naming the offending cell. A metric with an evidence source outside the list or a direction other than `higher` or `lower` fails. | Test |
| FR-020-AC-3 | A deterministic evaluation whose `Query or rubric` is empty, is a rubric reference or is free text, a judgement evaluation whose `Query or rubric` is not of the form `<rubric>@<version>#<check-slug>`, and an evaluation whose `Trigger` is empty or free text each fail. A metric whose `Query` is free text fails. | Test |
| FR-020-AC-4 | A judgement evaluation with cadence `tick` fails. | Test |
| FR-020-AC-11 | A role spec carrying a `## Purpose` section in addition to the four tables validates. | Test |
| FR-020-AC-12 | The `RoleSpec` manifest entry declares `allowed_links` of exactly `satisfies`, `depends_on` and `implements`, and a `RoleSpec` with any other relationship verb fails. | Test |
| FR-020-AC-5 | A row id whose prefix differs from the frontmatter `id`, or whose shape differs from its table's id pattern, fails naming the id. | Test |
| FR-020-AC-6 | A threshold with a comparator outside the five accepted, a non-numeric `Value`, or an empty `Unit` fails. | Test |
| FR-020-AC-7 | A judgement evaluation whose `Evaluator` is neither `director` nor `team-retro`, and a deterministic evaluation whose `Evaluator` is not `evaluator`, each fail. | Test |
| FR-020-AC-8 | `version: 0`, a non-integer `version`, and a lower-case or over-long `id` each fail naming the field. | Test |
| FR-020-AC-9 | The enum vocabularies are declared once in the `RoleSpec` schema; the manifest and mapping declare none of the same values. | Inspection |
| FR-020-AC-10 | The `RoleSpec` skeleton validates, and a negative counterpart exists for each failing case above (FR-012). | Test |

## Dependencies

- [FR-001](./FR-001-module-manifest-activates.md), [FR-009](./FR-009-emitted-json-schemas.md), [FR-011](./FR-011-markdown-record-mapping.md) and [FR-012](./FR-012-executable-skeletons.md) for the manifest, record schema, mapping and skeleton mechanics.
- dev-team FR-006, the format this archetype validates (SWM-245).
- The evaluator query registry (SWM-221), which owns what a registered query id is.
