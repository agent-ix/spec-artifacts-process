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

The module SHALL declare an **`Anomaly`** artifact type, one document per reported anomaly,
carrying its current `status`, how it ended (`resolution`), who closed it (`closed_by`) and a
person-assigned `severity`, so that an anomaly record cannot be closed without a resolution and a
named closer, and cannot be assessed without a severity.

The record keeps no hand-typed history. Who changed the status, and when, is the git history of
the file, which already records it and which a typed table could only duplicate or falsify.

### Who owns which check

| Check | Owner |
|---|---|
| Field vocabularies, required sections, table shapes | This module, through its manifest and the `assert` facet (quire-rs FR-033) |
| Status-conditional presence (`resolution`, `closed_by`, the legal `status`/`resolution` pairs) | This module's `record_validation` schema `AnomalyFields.json`, run by the engine on the YAML-extracted record (quire-rs FR-069-AC-21..28) and reported as `semantic.record-invalid`; the `assert` facet cannot express a condition on another field. The emitted record schema `Anomaly.json` (FR-009) states the same rules for the mapped record (quoin FR-073) |
| Transition legality, and re-assessment on reopen, judged over the git history of `status` | quoin [FR-136](ix://agent-ix/quoin/FR-136) |

## Inputs

- An `Anomaly` document: frontmatter `id`, `title`, `type: Anomaly`, `status`, `resolution`,
  `closed_by`, `severity`, `safety_impact` ([FR-015](./FR-015-anomaly-safety-impact-assessment.md)), and a
  `## Description` section.

## Outputs

- A validated `Anomaly` document, or located validation failures.
- An emitted JSON Schema for the type and an authoring skeleton that is a valid sample
  ([FR-009](./FR-009-emitted-json-schemas.md), [FR-012](./FR-012-executable-skeletons.md)).

## Behavior

- The `status` field SHALL be one of exactly `identified`, `assessed`, `resolved`, `closed`.
- The `resolution` field SHALL be one of exactly `fixed`, `not-a-defect`, `duplicate`, `wont-fix`,
  and SHALL be present when `status` is `resolved` or `closed` and absent otherwise.
- When `status` is `resolved`, `resolution` SHALL be `fixed`.
- The single legal status moves SHALL be exactly: `identified` to `assessed`, `assessed` to
  `resolved`, `resolved` to `closed`, `resolved` to `assessed` (a fix that did not hold),
  `identified` to `closed` and `assessed` to `closed`. Closing without a fix is intended for
  `resolution` `not-a-defect`, `duplicate` or `wont-fix`; that intended use is not checked against
  the move.
- A change of status between two successive recorded states (commits, or the last commit and the working tree) SHALL be legal when the later status is reachable from the
  earlier one by one or more legal moves, because squash-merged history can hide intermediate
  states; any other change SHALL fail; in effect `identified` is never re-entered and `closed` is final. The check is owned by
  quoin FR-136 and verified by quoin FR-136-AC-3, not by a criterion here.
- When `status` is `closed`, `closed_by` SHALL be present. Its check is of shape only: non-empty
  after trimming and not a placeholder (`n/a`, `none`, `unknown`, `tbd`, `-`, compared
  case-insensitively). It does not establish that the value is a real person; the commit that sets
  `closed` carries the author and, where commits are signed, the signature, and that is the
  attribution of record.
- When `status` is not `closed`, `closed_by` SHALL be absent.
- The `severity` field SHALL be one of exactly `minor`, `major`, `critical`, declared as an
  `assert: choices` constraint on a `severity` `frontmatter_field` locator in the `Anomaly`
  `yield_pattern.match`.
- The module SHALL declare no default for `severity`.
- The module SHALL NOT derive `severity` from any other field.
- While `status` is `identified`, `severity` MAY be absent.
- When `status` is `assessed`, `resolved` or `closed`, `severity` SHALL be present.
- The module SHALL add no field that records who set or changed `severity`, or when; that is the git
  history of the file, as for `status`.
- The module SHALL ship the emitted schema for `Anomaly` and a skeleton that validates as authored,
  with negative counterparts for a closed anomaly with no `closed_by`, a placeholder `closed_by`,
  an `assessed` anomaly with no `severity`, a `severity` outside the vocabulary, a `resolved` anomaly with no `resolution`, and an `identified` anomaly carrying `closed_by`.
- The module SHALL publish the `Anomaly` record mapping in `mappings.yaml` ([FR-011](./FR-011-markdown-record-mapping.md)),
  naming the record keys `status`, `resolution`, `closedBy` (from frontmatter `closed_by`), `severity`
  and `safetyImpact`, each a `frontmatter` mapping carried verbatim, and the keys `assessment`, `verification` and `releaseRationale`
  ([FR-015](./FR-015-anomaly-safety-impact-assessment.md)). The key `statusHistory` is not
  authored anywhere: quoin FR-136 derives it from git.
- The module SHALL ship fixtures as part of its tests for the criteria below: one valid document per
  `status`, a `closed` document for each `resolution`, the negatives named above, and the
  negatives of FR-015. Quoin holds no copy of these documents.
- The `Anomaly` archetype SHALL declare `record_validation: { schema: schemas/AnomalyFields.json, locate_absence_at: status }`
  and a `closed_by` `frontmatter_field` locator (`required: false`) in its `yield_pattern.match`.
  `AnomalyFields.json` is the module's own, hand-authored schema for the YAML-extracted record:
  its property names are the `yield_pattern.match` keys verbatim (`closed_by`, `severity`, `safety_impact`, `release_rationale`) and
  it carries the conditional presence rules above as `if`/`then`, so that each is reported at the
  `status` line. It is not the emitted record schema: `Anomaly.json` (camelCase keys, projected
  from TypeSpec, FR-009) validates the mapped record and is unchanged by it. The schema generator
  leaves `AnomalyFields.json` alone, as it does a frontmatter schema.
- `AnomalyFields.json` SHALL also carry the assessment row rules the `assert` facet cannot express
  (each table row is one tab-joined `Kind`, `Target`, `Impact`, `Rationale` string in the extracted
  record): `none` admits exactly one row, `None` with `Target` `-` and `Impact` `None`; `impacting`
  needs a `Requirement` or `Hazard` row whose `Impact` is `Affects`, `Mitigates` or `Introduces`;
  `Impact` `None` is refused on a `Requirement` or `Hazard` row. A row defect is reported at the
  row's line.
- The status rules SHALL apply only to a status in the vocabulary, so a mistyped `status` yields the
  `status` vocabulary finding and no other. The `closed_by` placeholder rule applies only to a
  `closed` anomaly, so a non-closed anomaly carrying `closed_by` yields the one finding that it must
  not.
- The type SHALL NOT be `required` of any repository; a repository that declares no `Anomaly`
  document is unaffected.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-014-AC-1 | The manifest declares `Anomaly` with the four-member `status` vocabulary, the four-member `resolution` vocabulary, and a `## Description` section. | Test |
| FR-014-AC-2 | The shipped skeleton validates as authored, and the `Anomaly` JSON Schema file exists beside the other emitted process-type schemas. | Test |
| FR-014-AC-3 | Fixtures for `identified`, `assessed`, `resolved` with `fixed`, `closed` with `fixed`, and `closed` with `not-a-defect` each validate when their conditional fields are correct. | Test |
| FR-014-AC-4 | A `closed` fixture with no `closed_by` fails; a `closed` fixture with `closed_by` of `TBD`, `unknown`, `n/a`, `none`, `-` or empty fails in any letter case; the same fixture with a non-placeholder value passes. | Test |
| FR-014-AC-5 | A fixture with `status` of `resolved` or `closed` and no `resolution` fails; a `resolved` fixture with `resolution` other than `fixed` fails; a fixture with `status` of `identified` or `assessed` and a `resolution` fails. | Test |
| FR-014-AC-6 | A fixture with `status` other than `closed` that carries `closed_by` fails. | Test |
| FR-014-AC-7 | The mapping lists `status`, `resolution`, `closedBy`, `severity`, `safetyImpact`, `assessment`, `verification` and `releaseRationale` for `Anomaly`, each named by exactly one entry, and the golden record built from the skeleton validates against the emitted `Anomaly` schema. | Test |
| FR-014-AC-8 | A repository declaring no `Anomaly` document loads and validates exactly as it did before the type existed. | Test |
| FR-014-AC-9 | The `Anomaly` archetype declares `record_validation` with schema `schemas/AnomalyFields.json` and `locate_absence_at: status`. | Test |
| FR-014-AC-10 | The `Anomaly` `yield_pattern.match` carries a `closed_by` `frontmatter_field` locator with `required: false`. | Test |
| FR-014-AC-11 | `AnomalyFields.json` ships in the package data beside the emitted schemas and is not counted as a projection by the schema generator. | Test |
| FR-014-AC-12 | A `closed` anomaly with no `closed_by` and no `resolution` is reported once per missing field, both at the `status` line. | Test |
| FR-014-AC-13 | An anomaly whose `status` is outside the vocabulary yields exactly one finding, at the `status` line. | Test |
| FR-014-AC-14 | The `Anomaly` `yield_pattern.match` carries a `severity` `frontmatter_field` locator (`required: false`) whose `assert` is `choices` of exactly `minor`, `major`, `critical`, and the manifest and `AnomalyFields.json` define no default for `severity`. | Test |
| FR-014-AC-15 | For each of `assessed`, `resolved` and `closed`, a fixture with no `severity` fails, reported at the `status` line; an `identified` fixture with no `severity` validates. | Test |
| FR-014-AC-16 | A fixture whose `severity` is outside the vocabulary (including `high`, `Major` and the empty string) fails with exactly one finding, at the `severity` line. | Test |
| FR-014-AC-17 | Two fixtures identical except for one differing field (`safety_impact`, or the assessment rows) validate with the same `severity`, and no schema, locator or mapping of the `Anomaly` type computes `severity` from another field. | Test |
| FR-014-AC-18 | No field of the `Anomaly` type records who set `severity` or when. | Inspection |

## Dependencies

- **Upstream**: [FR-009](./FR-009-emitted-json-schemas.md), [FR-012](./FR-012-executable-skeletons.md), quire-rs FR-033 (the `assert` facet), quire-rs FR-069-AC-21..28 (`record_validation`), quoin FR-073 (record validation)
- **Downstream**: [FR-015](./FR-015-anomaly-safety-impact-assessment.md); quoin [FR-136](ix://agent-ix/quoin/FR-136) (history-based transition check and record mapping)
