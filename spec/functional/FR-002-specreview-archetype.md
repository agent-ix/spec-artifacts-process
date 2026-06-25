---
id: FR-002
title: "SpecReview archetype for validated per-analysis review docs"
type: FR
relationships:
  - target: "ix://agent-ix/quire-rs/spec/functional/FR-033"
    type: "requires"
    cardinality: "1:1"
---
# FR-002: SpecReview archetype for validated per-analysis review docs

## Description

The module **SHALL** contribute a doc-backed `SpecReview` archetype — one review
document per analysis skill — whose `## Findings` table is structurally validated
by Quire so findings are consistent, parseable, and severity-constrained. It is a
**distinct** archetype from the freeform `Review` type, which carries heterogeneous
bodies across the ecosystem and is left unconstrained.

## Inputs

- A `SpecReview` markdown document (`type: SpecReview`) authored under `spec/reviews/`
- The module's `spec-review-frontmatter.schema.json` and `body_extraction` contract

## Outputs

- A validated `SpecReview` artifact (frontmatter + `## Summary` + `## Findings` table)
- An authoring skeleton emitted by `quoin write --types SpecReview`

## Behavior

- The frontmatter **SHALL** require `id`/`title`/`type: SpecReview` and admit
  `analysis` (the six analyses plus `base`), `scope`, and `review_set`.
- `body_extraction` **SHALL** require a `## Summary` section and a `## Findings`
  `table_row` with columns exactly `ID | Severity | Summary | Refs`, at least one
  row, an `ID` column matching `^FND-\d+$`, and a `Severity` column constrained to
  `low|medium|high` via the Quire `column_choices` assert (requires
  [FR-033](ix://agent-ix/quire-rs/spec/functional/FR-033)).
- Findings **SHALL** be extractable as records (`multiple: true`) so tooling can
  select and process each finding by id.
- An authoring skeleton (`skeletons/SpecReview.md`) **SHALL** ship in the package so
  `quoin write --types SpecReview` emits the authoritative template.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-002-AC-1 | A `SpecReview` doc with a well-formed Findings table validates; one missing the `## Findings` table fails with reason `missing` | Test |
| FR-002-AC-2 | A `Severity` cell outside `low\|medium\|high` fails validation via `column_choices` (reason `assert`) | Test |
| FR-002-AC-3 | An `ID` cell not matching `^FND-\d+$` fails validation | Test |
| FR-002-AC-4 | The bundled `skeletons/SpecReview.md` is itself a valid `SpecReview` and ships in the wheel | Test |
| FR-002-AC-5 | The `SpecReview` archetype is registered without altering the freeform `Review` archetype | Inspection |

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md), quire-rs [FR-033](ix://agent-ix/quire-rs/spec/functional/FR-033) (CR-010 `column_choices`)
- **Downstream**: the quoin `spec-review` flow that authors `SpecReview` docs
