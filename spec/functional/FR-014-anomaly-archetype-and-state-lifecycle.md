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
carrying its current `status`, how it ended (`resolution`) and who closed it (`closed_by`), so that
an anomaly record cannot be closed without a resolution and a named closer.

The record keeps no hand-typed history. Who changed the status, and when, is the git history of
the file, which already records it and which a typed table could only duplicate or falsify.

### Who owns which check

| Check | Owner |
|---|---|
| Field vocabularies, required sections, table shapes | This module, through its manifest and the `assert` facet (quire-rs FR-033) |
| Status-conditional presence (`resolution`, `closed_by`, the legal `status`/`resolution` pairs) | This module's emitted record schema (FR-009), run as record validation (quoin FR-073); the `assert` facet cannot express a condition on another field |
| Transition legality, and re-assessment on reopen, judged over the git history of `status` | quoin [FR-136](ix://agent-ix/quoin/FR-136) |

## Inputs

- An `Anomaly` document: frontmatter `id`, `title`, `type: Anomaly`, `status`, `resolution`,
  `closed_by`, `safety_impact` ([FR-015](./FR-015-anomaly-safety-impact-assessment.md)), and a
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
- A change of status between two commits SHALL be legal when the later status is reachable from the
  earlier one by one or more legal moves, because squash-merged history can hide intermediate
  states; any other change SHALL fail; in effect `identified` is never re-entered and `closed` is final. The check is owned by
  quoin FR-136 and verified by quoin FR-136-AC-3, not by a criterion here.
- When `status` is `closed`, `closed_by` SHALL be present. Its check is of shape only: non-empty
  after trimming and not a placeholder (`n/a`, `none`, `unknown`, `tbd`, `-`, compared
  case-insensitively). It does not establish that the value is a real person; the commit that sets
  `closed` carries the author and, where commits are signed, the signature, and that is the
  attribution of record.
- When `status` is not `closed`, `closed_by` SHALL be absent.
- The module SHALL ship the emitted schema for `Anomaly` and a skeleton that validates as authored,
  with negative counterparts for a closed anomaly with no `closed_by`, a placeholder `closed_by`,
  a `resolved` anomaly with no `resolution`, and an `identified` anomaly carrying `closed_by`.
- The module SHALL publish the `Anomaly` record mapping in `mappings.yaml` ([FR-011](./FR-011-markdown-record-mapping.md)),
  naming the record keys `status`, `resolution`, `closedBy` (from frontmatter `closed_by`) and
  `safetyImpact`, each a `frontmatter` mapping carried verbatim, and the key `assessment`
  ([FR-015](./FR-015-anomaly-safety-impact-assessment.md)). The key `statusHistory` is not
  authored anywhere: quoin FR-136 derives it from git.
- The module SHALL ship fixtures as part of its tests for the criteria below: one valid document per
  `status`, a `closed` document for each `resolution`, the negatives named above, and the
  negatives of FR-015. Quoin holds no copy of these documents.
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
| FR-014-AC-7 | The mapping lists `status`, `resolution`, `closedBy`, `safetyImpact` and `assessment` for `Anomaly`, each named by exactly one entry, and the golden record built from the skeleton validates against the emitted `Anomaly` schema. | Test |
| FR-014-AC-8 | A repository declaring no `Anomaly` document loads and validates exactly as it did before the type existed. | Test |

## Dependencies

- **Upstream**: [FR-009](./FR-009-emitted-json-schemas.md), [FR-012](./FR-012-executable-skeletons.md), quire-rs FR-033 (the `assert` facet), quoin FR-073 (record validation)
- **Downstream**: [FR-015](./FR-015-anomaly-safety-impact-assessment.md); quoin [FR-136](ix://agent-ix/quoin/FR-136) (history-based transition check and record mapping)
