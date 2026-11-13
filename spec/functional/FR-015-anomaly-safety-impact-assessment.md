---
id: FR-015
title: "Anomaly safety-impact assessment and fix verification with resolving links"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-003"
    type: "implements"
  - target: "ix://agent-ix/spec-artifacts-process/FR-014"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/FR-001"
    type: "depends_on"
---
# FR-015: Anomaly safety-impact assessment and fix verification with resolving links

## Description

The `Anomaly` type ([FR-014](./FR-014-anomaly-archetype-and-state-lifecycle.md)) SHALL carry a
required safety-impact field and a `## Safety Impact Assessment` section linking the anomaly to the
requirements and hazards it affects, SHALL fail validation when an anomaly that has reached
`assessed` or later has no assessment, and SHALL fail validation when a link names an artifact that
does not exist or is of the wrong kind.

The same type SHALL require an anomaly resolved as `fixed` to link the test case or acceptance
criterion that demonstrates the fix, in a `## Fix Verification` section, and SHALL fail validation
when such a link names an artifact that does not exist or is of the wrong kind. The change that made
the fix is not recorded in the document: quoin [FR-136](ix://agent-ix/quoin/FR-136) derives it from
the git history of the file (the commit that moved `status` to `resolved`, or, where squashing hides
that move, the commit that first reached a terminal `fixed` status). No commit hash, date or author
is authored anywhere in the record.

### Who owns which check

| Check | Owner |
|---|---|
| `safety_impact` vocabulary, section table shape, `Kind` and `Impact` vocabularies | This module (manifest, `assert` facet, quire-rs FR-033) |
| Section required by `status` and `safety_impact`, and the row rules (`none` admits one `None` row; `impacting` needs a `Requirement` or `Hazard` row that is not `Unaffected`; `Impact` `None` only on a `None` row) | This module's `record_validation` schema `AnomalyFields.json` over the YAML-extracted record (FR-014; quire-rs FR-069-AC-21..28), an absence reported at the `status` line and a row defect at the row's line; the emitted record schema `Anomaly.json` (FR-009) states the same rules for the mapped record (quoin FR-073) |
| `Target` resolution against the corpus (dangling reference) | quire-rs [FR-049](ix://agent-ix/quire-rs/FR-049), the `Target` column being a declared document reference of this module's traceability model; the finding is `dangling-trace-reference`, an error under the `Strict` posture and a warning under `Okf` |
| `## Fix Verification` required when `resolution` is `fixed`; its table shape and `Kind` vocabulary; row presence | This module (manifest, `assert` facet, `AnomalyFields.json`), as for the assessment; `Target` resolution and kind through quire-rs [FR-049](ix://agent-ix/quire-rs/FR-049): the manifest declares a document reference for the section with `kind_column` `Kind` (`Criterion` to acceptance-criterion targets, `Test` to the `test-case` target), reported as `dangling-trace-reference` and `reference-kind-mismatch` |
| The fixing change | quoin [FR-136](ix://agent-ix/quoin/FR-136), the git history of `status` |
| Missing `spec-objects-safety` reported once per document | quoin [FR-136](ix://agent-ix/quoin/FR-136), as one `anomaly.missing-module` diagnostic alongside the engine's per-row reports |
| `Target` kind (`Requirement` row names an `FR`/`NFR`/acceptance criterion; `Hazard` row names a hazard) | quire-rs [FR-049](ix://agent-ix/quire-rs/FR-049) kind-typed references (`kind_column`, finding `reference-kind-mismatch`, FR-049-AC-10..18), typing the reference by the row's `Kind` rather than a per-row check written here. [FR-040](ix://agent-ix/quire-rs/FR-040) edge findings are warnings only and are not this check |

## Inputs

- Frontmatter `safety_impact`, `resolution` and `status` of an `Anomaly` document.
- The `## Safety Impact Assessment` section of that document, and its `## Fix Verification` section.
- The corpus the document is validated in: its `FR` and `NFR` artifacts and their acceptance
  criteria, and its hazard artifacts. A document is a hazard when its frontmatter carries
  `type: hazard` and `object: hazard`, as declared by `agent-ix/spec-objects-safety`; no hazard id
  pattern is assumed.
- For the fix verification, the same corpus's acceptance criteria and the test cases minted by the
  module's `TestMatrix` documents (`Test Case Summary`, `Test ID` column).

## Outputs

- A validated assessment, or located validation failures naming the missing assessment, the
  dangling link, or the missing module.
- A validated fix verification, or located validation failures naming the missing section, the
  dangling link or the wrong-kind link.

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
- If `resolution` is `fixed`, then the document SHALL carry a `## Fix Verification` section, and
  validation SHALL fail, at the `status` line, when it does not.
- If `resolution` is absent or is not `fixed`, then the section is not required.
- The section SHALL be a table with headers exactly `Kind | Target | Rationale` and at least one row.
- The `Kind` of a row SHALL be one of `Criterion`, `Test`.
- The `Rationale` of a row SHALL be non-empty.
- A `Criterion` row's `Target` SHALL be the id of an acceptance criterion of an `FR` or `NFR`
  artifact that exists in the validated corpus.
- A `Test` row's `Target` SHALL be the id of a test case (a `Test ID` of a `TestMatrix` document)
  that exists in the validated corpus.
- The manifest SHALL declare a document reference for the section (name `anomaly-fix-verification`,
  `column` `Target`, `kind_column` `Kind`, and `targets` listing `acceptance-criterion`,
  `nfr-acceptance-criterion`, `test-case`, `requirement-document`, `nfr-document` and
  `hazard-document`, because an id resolves only against `targets`) with `kind_targets` `Criterion` to
  `acceptance-criterion` and `nfr-acceptance-criterion`, and `Test` to `test-case`, so that
  resolution and kind checking are the engine's (quire-rs FR-049): validation SHALL fail a `Target`
  that resolves to nothing as a dangling reference, and one that resolves to an artifact of the
  other kind (including a requirement document such as `FR-001`) as a kind mismatch. Both
  diagnostics are the engine's, not text written by this module.
- The manifest SHALL declare, for the `Target` column of the section, a `column_patterns` rule
  requiring an id token (a value that begins with a letter or digit), because a cell matching no
  reference pattern produces no reference and no finding (quire-rs FR-049-AC-14) and `-` would
  otherwise pass; an empty `Target` and a `-` `Target` SHALL each fail validation.
- The module SHALL map the rows to the record key `verification` as a `typed-table` mapping
  ([FR-011](./FR-011-markdown-record-mapping.md)), one entry per row with `kind`, `target` and
  `rationale` carried as authored.
- The `Anomaly` type SHALL NOT carry a commit hash, author or date of the fix.
- The `Anomaly` type SHALL NOT carry a field that names the fixing change.
- The `Anomaly` type SHALL NOT carry a verdict or sign-off on the verification.
- The module SHALL ship, as fixtures for AC-11 to AC-16, a corpus holding an `FR`, one of its
  criteria and a `TestMatrix` test case, the valid `fixed` anomalies, and the negatives of those
  criteria.
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
| FR-015-AC-11 | The manifest declares the `## Fix Verification` table with exactly the columns `Kind`, `Target`, `Rationale`, `min_rows: 1` and the `Kind` vocabulary `Criterion`, `Test`, and declares a document reference `anomaly-fix-verification` with `column` `Target`, `kind_column` `Kind`, `targets` listing `acceptance-criterion`, `nfr-acceptance-criterion`, `test-case`, `requirement-document`, `nfr-document` and `hazard-document`, and `kind_targets` `Criterion` to the acceptance-criterion targets and `Test` to `test-case`; and it declares a `column_patterns` rule on `Target` requiring an id token. | Test |
| FR-015-AC-12 | A `resolved` anomaly and a `closed` anomaly with `resolution` `fixed` each fail validation, at the `status` line, with no `## Fix Verification` section; a `closed` anomaly with `resolution` `not-a-defect`, `duplicate` or `wont-fix` and no section validates. | Test |
| FR-015-AC-13 | In the corpus of AC-4 plus a `TestMatrix` test case `TC-001`, a `fixed` anomaly with a `Criterion` row targeting `FR-001-AC-1` and a `Test` row targeting `TC-001` validates. | Test |
| FR-015-AC-14 | In that corpus, a `Criterion` row targeting `FR-001-AC-99` and a `Test` row targeting `TC-999` each fail as a dangling reference naming the id and its row. | Test |
| FR-015-AC-15 | In that corpus, a `Criterion` row targeting `FR-001` (a requirement document), a `Criterion` row targeting the hazard, and a `Test` row targeting `FR-001-AC-1` each fail as a kind mismatch. | Test |
| FR-015-AC-16 | A row with an empty `Rationale` or a `Kind` outside the vocabulary fails validation. | Test |
| FR-015-AC-17 | The mapping yields `verification` entries with `kind`, `target` and `rationale` as authored. | Test |
| FR-015-AC-18 | No field or table column of the `Anomaly` type holds a commit hash, author or date of the fix, a field naming the fixing change, or a verdict or sign-off on the verification. | Inspection |
| FR-015-AC-19 | A `fixed` anomaly whose only row is `Test`, `-`, `verified`, and one whose only row has an empty `Target`, each fail validation at the row. | Test |

## Dependencies

- **Upstream**: [FR-014](./FR-014-anomaly-archetype-and-state-lifecycle.md); quire-rs [FR-049](ix://agent-ix/quire-rs/FR-049) (document-reference resolution) and its kind-typed references (`kind_column`, FR-049-AC-10..18); requires quire-rs >= 0.58.0 (quire CLI >= 0.43.0), as older engines reject `kind_column` and `record_validation`; quire-rs FR-033; [FR-009](./FR-009-emitted-json-schemas.md); `agent-ix/spec-objects-safety` [FR-001](ix://agent-ix/spec-objects-safety/FR-001) (the `hazard` object type)
- **Downstream**: quoin [FR-136](ix://agent-ix/quoin/FR-136)
