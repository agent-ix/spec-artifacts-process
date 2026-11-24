---
id: FR-023
title: "Rubric archetype: versioned checks that judgement evaluations cite"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-004"
    type: "satisfies"
  - target: "ix://agent-ix/spec-artifacts-process/FR-020"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/dev-team/FR-006"
    type: "implements"
---
# FR-023: Rubric archetype: versioned checks that judgement evaluations cite

## Description

A judgement evaluation in a role spec cites a rubric check as `<rubric>@<version>#<check-slug>` ([FR-020](./FR-020-rolespec-archetype.md)), for example `rubric-minder@1#failed-probe`. The module SHALL declare the artifact type `Rubric` so that the cited rubric, its version and the check slug exist as validated document content. A citation then resolves through the same dangling-reference check every other reference uses, and a rubric edit that changes its version makes stale citations visible.

## Inputs

- A Markdown file with `type: Rubric`, kept with the role specs under `spec/roles/`.

## Outputs

- Frontmatter members: `id` (a lower-case slug such as `rubric-minder`), `version` (a positive integer), `type: Rubric` and `relationships`.
- A required `Checks` section holding a table with columns `ID`, `Check`, `Scale` in that order.
- A skeleton for `Rubric` (FR-012) and a frontmatter schema.

## Behavior

- The `Rubric` frontmatter schema SHALL require `id`, `version` and `type`.
- The `Rubric` frontmatter schema SHALL accept `id` only as a lower-case slug starting with `rubric-`.
- The `Rubric` frontmatter schema SHALL accept `version` only as an integer of at least 1.
- The `Rubric` archetype SHALL require a `Checks` table with at least one row.
- The `Rubric` archetype SHALL assert that each `ID` cell matches `^<id>@<version>#[a-z][a-z0-9-]*$`, with the frontmatter `id` and `version` interpolated, so a check id always carries the rubric's current version.
- The manifest SHALL declare a trace target `rubric-check` over archetype `Rubric`, section `Checks`, id column `ID`, with `evidence: reference-only`, excluding `tests/**`, `tests_integration/**` and `fixtures/**`.
- The `Rubric` manifest entry SHALL declare `allowed_links` of `satisfies`, `depends_on` and `implements`.
- The module SHALL ship a `Rubric` mapping entry with role `definition` (FR-011) and a skeleton (FR-012).

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-023-AC-1 | A rubric with `id`, `version` and a `Checks` table validates; removing `version`, the `Checks` table or any column fails naming the missing element. | Test |
| FR-023-AC-2 | A check id whose rubric name or version differs from the frontmatter, or whose slug is not lower-case hyphenated, fails naming the id. | Test |
| FR-023-AC-3 | `quire matrix` over a fixture mints `rubric-minder@1#failed-probe` from the rubric, and the `Evaluations` reference in the worked minder spec resolves to it without a dangling finding. | Test |
| FR-023-AC-4 | Changing the fixture rubric to `version: 2` without editing its check ids fails validation, and a role spec still citing `@1` produces `dangling-trace-reference`. | Test |
| FR-023-AC-5 | The `Rubric` skeleton validates and a negative counterpart exists for each failing case above. | Test |

## Dependencies

- [FR-004](./FR-004-traceability-declaration.md) for the trace-target and document-reference mechanics.
- [FR-020](./FR-020-rolespec-archetype.md), which defines the reference form, and [FR-021](./FR-021-rolespec-trace-and-cross-row-checks.md), which declares the `Evaluations` reference to `rubric-check`.
- dev-team FR-006, which defines judgement evaluations.
- Open question for the owner: where rubric files live in dev-team (the archetype assumes `spec/roles/` so `quire matrix` reads them).
