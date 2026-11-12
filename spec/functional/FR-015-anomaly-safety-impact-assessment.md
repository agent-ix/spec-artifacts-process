---
id: FR-015
title: "Anomaly safety-impact assessment with resolving links"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-003"
    type: "implements"
  - target: "ix://agent-ix/spec-artifacts-process/FR-014"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-001"
    type: "depends_on"
---
# FR-015: Anomaly safety-impact assessment with resolving links

## Description

The `Anomaly` type ([FR-014](./FR-014-anomaly-archetype-and-state-lifecycle.md)) SHALL carry a
required safety-impact field and a `## Safety Impact Assessment` section linking the anomaly to the
requirements and hazards it affects, SHALL fail validation when an anomaly that has reached
`assessed` or later has no assessment, and SHALL fail validation when a link names an artifact that
does not exist or is of the wrong kind.

### Who owns which check

| Check | Owner |
|---|---|
| `safety_impact` vocabulary, section table shape, `Kind` and `Impact` vocabularies | This module (manifest, `assert` facet, quire-rs FR-033) |
| Section required by `status` and `safety_impact`, and the row rules (`none` admits one `None` row; `impacting` needs a `Requirement` or `Hazard` row that is not `Unaffected`; `Impact` `None` only on a `None` row) | This module's `record_validation` schema `AnomalyFields.json` over the YAML-extracted record (FR-014; quire-rs FR-069-AC-21..28), an absence reported at the `status` line and a row defect at the row's line; the emitted record schema `Anomaly.json` (FR-009) states the same rules for the mapped record (quoin FR-073) |
| `Target` resolution against the corpus (dangling reference) | quire-rs [FR-049](ix://agent-ix/quire-rs/FR-049), the `Target` column being a declared document reference of this module's traceability model; the finding is `dangling-trace-reference`, an error under the `Strict` posture and a warning under `Okf` |
| Missing `spec-objects-safety` reported once per document | quoin [FR-136](ix://agent-ix/quoin/FR-136), as one `anomaly.missing-module` diagnostic alongside the engine's per-row reports |
| `Target` kind (`Requirement` row names an `FR`/`NFR`/acceptance criterion; `Hazard` row names a hazard) | quire-rs [FR-049](ix://agent-ix/quire-rs/FR-049) kind-typed references (`kind_column`, finding `reference-kind-mismatch`, FR-049-AC-10..18), typing the reference by the row's `Kind` rather than a per-row check written here. [FR-040](ix://agent-ix/quire-rs/FR-040) edge findings are warnings only and are not this check |

## Inputs

- Frontmatter `safety_impact` and `status` of an `Anomaly` document.
- The `## Safety Impact Assessment` section of that document.
- The corpus the document is validated in: its `FR` and `NFR` artifacts and their acceptance
  criteria, and its hazard artifacts. A document is a hazard when its frontmatter carries
  `type: hazard` and `object: hazard`, as declared by `agent-ix/spec-objects-safety`; no hazard id
  pattern is assumed.

## Outputs

- A validated assessment, or located validation failures naming the missing assessment, the
  dangling link, or the missing module.

## Behavior

- Every `Anomaly` SHALL carry `safety_impact`, one of exactly `unassessed`, `none`, `impacting`.
- While `status` is `identified`, `safety_impact` MAY be `unassessed` and the section MAY be absent.
- When `status` is `assessed`, `resolved` or `closed`, `safety_impact` SHALL NOT be `unassessed`
  and the document SHALL carry a `## Safety Impact Assessment` section; otherwise validation fails.
- The section SHALL be a table with headers exactly `Kind | Target | Impact | Rationale` and at
  least one row. `Kind` is one of `Requirement`, `Hazard`, `None`. `Impact` is one of `Affects`,
  `Mitigates`, `Introduces`, `Unaffected`, `None`; `None` is admitted only on a row of `Kind`
  `None`. `Rationale` SHALL be non-empty.
- A `Requirement` row's `Target` SHALL be the id of an `FR` or `NFR` artifact, or of one of its
  acceptance criteria, that exists in the validated corpus. A `Hazard` row's `Target` SHALL be the
  id of a hazard artifact that exists in the validated corpus. Validation SHALL fail a `Target` that
  resolves to nothing as a dangling reference, and SHALL fail one that resolves to an artifact of
  the other kind as a kind mismatch. Both diagnostics are the engine's reference diagnostics, not
  text written by this module.
- When a `Hazard` row is present and the `hazard` object type is not installed, quoin FR-136 SHALL
  report one missing-module diagnostic naming `spec-objects-safety` for the document, in addition to
  the engine's per-row reference diagnostics (FR-136-AC-10).
- When `safety_impact` is `impacting`, the table SHALL hold at least one `Requirement` or `Hazard`
  row whose `Impact` is not `Unaffected`.
- When `safety_impact` is `none`, the table SHALL hold exactly one row, of `Kind` `None`, with
  `Target` `-`, `Impact` `None` and a non-empty `Rationale`, and validation SHALL fail a `none`
  anomaly that also carries a `Requirement` or `Hazard` row.
- The module SHALL map the section's rows to the record key `assessment` as a `typed-table` mapping
  ([FR-011](./FR-011-markdown-record-mapping.md)), one entry per row with `kind`, `target`, `impact`
  and `rationale` carried as authored; `target` is the authored reference token (an `FR`, `NFR` or
  acceptance-criterion id, or a hazard id) and is absent for a `None` row whose `Target` is `-`.
  Whether a token resolves is not part of the record; it is reported as a diagnostic.
- The module SHALL ship, as fixtures for the criteria below, a corpus holding an `FR`, one of its
  acceptance criteria and a hazard, the valid anomalies of AC-4 and AC-7, an anomaly with two `Hazard` rows, a hazard that no anomaly names, and the negatives of
  AC-3, AC-5, AC-6, AC-7 and AC-8. Quoin holds no copy of these documents.
- The assessment SHALL be a statement of an engineer's judgement, not a computed risk acceptance;
  this requirement SHALL NOT add any risk-acceptance or sign-off field.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-015-AC-1 | The manifest declares `safety_impact` with exactly the three-member vocabulary, and the section table with exactly the four columns, `min_rows: 1`, and the `Kind` and `Impact` vocabularies above. | Test |
| FR-015-AC-2 | An `identified` anomaly with `safety_impact: unassessed` and no section validates. | Test |
| FR-015-AC-3 | For each of `assessed`, `resolved` and `closed`, a fixture with no `## Safety Impact Assessment` section fails validation, and a fixture with `safety_impact: unassessed` fails validation. | Test |
| FR-015-AC-4 | In a corpus containing `FR-001` with criterion `FR-001-AC-1`, and a hazard document with `type: hazard` and `object: hazard`, an `impacting` anomaly whose rows target `FR-001`, `FR-001-AC-1` and the hazard validates. | Test |
| FR-015-AC-5 | The same anomaly with a `Requirement` row targeting `FR-999` or `FR-001-AC-99`, or a `Hazard` row targeting an id no document carries, fails validation with a dangling-reference diagnostic naming the id and its row. | Test |
| FR-015-AC-6 | A `Requirement` row whose `Target` is the hazard's id, and a `Hazard` row whose `Target` is `FR-001`, each fail validation as a kind mismatch. | Test |
| FR-015-AC-7 | An `impacting` anomaly whose only rows are `Unaffected` fails validation; a `none` anomaly with one `None` row, `Target` `-`, `Impact` `None` and a rationale validates; a `none` anomaly with a `None` row whose `Impact` is `Affects`, or that also carries a `Hazard` row, fails validation; an `impacting` anomaly whose only rows have `Impact` `None`, or a `Requirement` or `Hazard` row with `Impact` `None`, fails validation. | Test |
| FR-015-AC-8 | A row with an empty `Rationale`, or with an `Impact` outside the vocabulary, fails validation. | Test |
| FR-015-AC-9 | The mapping yields `assessment` entries with `target` as authored, including an acceptance-criterion id, and no `target` for a `None` row. | Test |
| FR-015-AC-10 | The skeleton validates as authored in a corpus that supplies its linked ids, and negative counterparts exist for a missing assessment and a dangling link. | Test |

## Dependencies

- **Upstream**: [FR-014](./FR-014-anomaly-archetype-and-state-lifecycle.md); quire-rs [FR-049](ix://agent-ix/quire-rs/FR-049) (document-reference resolution) and its kind-typed references (`kind_column`, FR-049-AC-10..18); requires quire-rs >= 0.58.0 (quire CLI >= 0.42.0), as older engines reject `kind_column` and `record_validation`; quire-rs FR-033; [FR-009](./FR-009-emitted-json-schemas.md); `agent-ix/spec-objects-safety` [FR-001](ix://agent-ix/spec-objects-safety/FR-001) (the `hazard` object type)
- **Downstream**: quoin [FR-136](ix://agent-ix/quoin/FR-136)
