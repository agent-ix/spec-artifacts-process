---
id: FR-014
title: "Anomaly archetype with a state lifecycle"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-003"
    type: "implements"
  - target: "ix://agent-ix/spec-artifacts-process/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-012"
    type: "depends_on"
---
# FR-014: Anomaly archetype with a state lifecycle

## Description

The module SHALL declare an **`Anomaly`** artifact type, one document per reported anomaly, whose
recorded state changes are validated as a lifecycle, so that an anomaly record cannot claim a state
it did not legally reach and cannot be closed without a named person standing behind it.

## Inputs

- An `Anomaly` document: frontmatter `id`, `title`, `type: Anomaly`, `status` and `safety_impact`
  ([FR-015](./FR-015-anomaly-safety-impact-assessment.md)), and the body sections below.

## Outputs

- A validated `Anomaly` document, or located validation failures.
- An emitted JSON Schema for the type and an authoring skeleton that is a valid sample
  ([FR-009](./FR-009-emitted-json-schemas.md), [FR-012](./FR-012-executable-skeletons.md)).

## Behavior

- The `status` frontmatter field SHALL be one of exactly `identified`, `assessed`, `resolved`, `closed`.
- The document SHALL carry a `## Description` section and a `## History` section.
- The `## History` section SHALL be a table with headers exactly `From | To | By | Date | Note`, at least one row, with
  `Note` optional.
- The first `## History` row SHALL have an empty `From` and `To` of `identified`.
- Every later row's `From` SHALL equal the previous row's `To`.
- The legal transitions SHALL be exactly: `identified` to `assessed`, `assessed` to `resolved`,
  `resolved` to `closed`, and `resolved` to `assessed` (a resolution that did not hold). Every other
  `From`/`To` pair SHALL fail validation, including any transition out of `closed`, any skip of a
  state, and any row whose `From` equals its `To`.
- The last row's `To` SHALL equal the frontmatter `status`.
- Every row's `By` SHALL name a person. A `By` value that is empty or is
  one of `n/a`, `none`, `unknown`, `tbd`, `-` (compared case-insensitively after trimming) SHALL
  fail validation. This is checked for the row whose `To` is `closed` as the closing requirement,
  and for every other row as the same attribution rule.
- `Date` SHALL be an ISO 8601 calendar date.
- The module SHALL ship the emitted schema for `Anomaly` and a skeleton that validates as authored,
  with negative counterparts for an illegal transition, a status that disagrees with the history,
  and a closure with no named person.
- The type SHALL NOT be `required` of any repository; a repository that declares no `Anomaly`
  document is unaffected.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-014-AC-1 | The manifest declares `Anomaly` with the four-member `status` vocabulary, the `## History` table of exactly the five columns with `Note` optional and `min_rows: 1`, and a `## Description` section. | Test |
| FR-014-AC-2 | The shipped skeleton validates as authored, and the `Anomaly` JSON Schema file exists beside the other emitted process-type schemas. | Test |
| FR-014-AC-3 | A fixture walking `identified`, `assessed`, `resolved`, `closed` with a named person on every row validates; a fixture taking `resolved` back to `assessed` and onward to `resolved` and `closed` also validates. | Test |
| FR-014-AC-4 | Fixtures with `identified` to `resolved`, `identified` to `closed`, `assessed` to `identified`, `closed` to anything, and a row with `From` equal to `To` each fail validation with a line-numbered diagnostic naming the row. | Test |
| FR-014-AC-5 | A fixture whose first row has a non-empty `From` or a `To` other than `identified`, and a fixture whose row `From` differs from the previous row's `To`, each fail validation. | Test |
| FR-014-AC-6 | A fixture whose frontmatter `status` differs from the last row's `To` fails validation. | Test |
| FR-014-AC-7 | A fixture whose `closed` row has an empty `By`, or `By` of `TBD`, `unknown`, `n/a`, `none` or `-` in any letter case, fails validation; the same fixture with a person's name in `By` passes. | Test |
| FR-014-AC-8 | A fixture with a `Date` that is not an ISO 8601 calendar date fails validation. | Test |
| FR-014-AC-9 | A repository declaring no `Anomaly` document loads and validates exactly as it did before the type existed. | Test |

## Dependencies

- **Upstream**: [FR-009](./FR-009-emitted-json-schemas.md) (schema emission), [FR-012](./FR-012-executable-skeletons.md) (skeletons with negative counterparts), quire-rs FR-033 (the `assert` facet and its column keys)
- **Downstream**: [FR-015](./FR-015-anomaly-safety-impact-assessment.md); quoin [FR-136](ix://agent-ix/quoin/FR-136) (record mapping of the type)
