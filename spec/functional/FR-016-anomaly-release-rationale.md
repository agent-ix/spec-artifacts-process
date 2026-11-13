---
id: FR-016
title: "Anomaly release rationale: a human-authored, named reason for releasing with an anomaly open"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-003"
    type: "implements"
  - target: "ix://agent-ix/spec-artifacts-process/FR-014"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-015"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-011"
    type: "depends_on"
---
# FR-016: Anomaly release rationale: a human-authored, named reason for releasing with an anomaly open

## Description

The `Anomaly` type ([FR-014](./FR-014-anomaly-archetype-and-state-lifecycle.md)) SHALL accept an
optional `## Release Rationale` section in which a named person states why releasing with this
anomaly still open is acceptable. The rationale is an engineer's written judgement, as the
safety-impact assessment is ([FR-015](./FR-015-anomaly-safety-impact-assessment.md)). The module
validates only its shape and the status it may appear at; the tools that read it (quoin
[FR-162](ix://agent-ix/quoin/FR-162) and [FR-164](ix://agent-ix/quoin/FR-164)) never write, fill in
or default it.

The record keeps no date, commit or signature of the rationale. Who wrote it and when is the git
history of the file, which quoin FR-163 reads, as it reads the history of `status`.

### Who owns which check

| Check | Owner |
|---|---|
| Section table shape, column names, row presence, `Author` and `Rationale` non-empty and not a placeholder, the section absent while `status` is `closed` | This module (manifest, `assert` facet, `AnomalyFields.json`), as for FR-014 and FR-015 |
| Whether an open anomaly needs a rationale, and whether the rationale is the author's own | Not this module: quoin FR-164 decides the first; the second is a person's attestation recorded by git, not a check |

## Inputs

- The optional `## Release Rationale` section of an `Anomaly` document, and its frontmatter `status`.

## Outputs

- A validated rationale, or located validation failures.
- The record key `releaseRationale` ([FR-011](./FR-011-markdown-record-mapping.md)).

## Behavior

- The `Anomaly` type SHALL accept a `## Release Rationale` section at any `status` other than `closed`.
- The `Anomaly` type SHALL NOT require the section at any `status`.
- If `status` is `closed`, then validation SHALL fail an `Anomaly` that carries the section, at the section heading line.
- The section SHALL be a table with headers exactly `Author | Rationale` and at least one row.
- The `Author` of a row SHALL be non-empty after trimming.
- The `Author` of a row SHALL NOT be a placeholder (`n/a`, `none`, `unknown`, `tbd`, `-`, compared
  case-insensitively), the rule of `closed_by` in FR-014. The check is of shape only; it does not
  establish that the value is a real person.
- The `Rationale` of a row SHALL be non-empty after trimming.
- The `Rationale` of a row SHALL NOT be a placeholder of the same list.
- The module SHALL map the rows to the record key `releaseRationale` as a `typed-table` mapping
  ([FR-011](./FR-011-markdown-record-mapping.md)), one entry per row with `author` and `rationale`
  carried as authored. The key is absent from the record when the section is absent.
- The module SHALL declare no default for the section, its `Author` or its `Rationale`.
- The module SHALL NOT compute the `Author` or the `Rationale` from another field, from `closed_by` or from git.
- The shipped skeleton SHALL NOT contain the section.
- The `Anomaly` type SHALL NOT carry a date, commit hash, release identifier, signature or
  sign-off verdict of the rationale, and SHALL NOT carry a field that marks an anomaly accepted.
- The section SHALL NOT change the validity of any other part of the document: an `impacting`
  anomaly validates with and without it.
- The module SHALL ship, as fixtures for the criteria below, valid `assessed` and `resolved`
  anomalies that carry the section, and the negatives of AC-3 to AC-6. Quoin holds no copy of these documents.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-016-AC-1 | An `impacting` anomaly at `identified`, `assessed` and `resolved` that carries a well-formed `## Release Rationale` validates, and the same anomalies without the section validate. | Test |
| FR-016-AC-2 | A `closed` anomaly that carries a well-formed `## Release Rationale` fails validation, at the section heading line. | Test |
| FR-016-AC-3 | A row whose `Author` is empty, or `TBD`, `unknown`, `n/a`, `none` or `-` in any letter case, fails validation, at the row's line; the same row with a non-placeholder `Author` passes. | Test |
| FR-016-AC-4 | A row whose `Rationale` is empty or one of the placeholders of AC-3 fails validation, at the row's line. | Test |
| FR-016-AC-5 | A section whose headers are not exactly `Author \| Rationale`, or that has no row, fails validation. | Test |
| FR-016-AC-6 | A `closed` anomaly whose section has a placeholder `Author` and an empty `Rationale` yields one finding for the section, one for the author and one for the rationale, in one run. | Test |
| FR-016-AC-7 | The mapping lists `releaseRationale` for `Anomaly` as a `typed-table` entry set with `author` and `rationale` as authored; the key is absent for an anomaly without the section; and the emitted `Anomaly` schema declares it. | Test |
| FR-016-AC-8 | The shipped skeleton contains no `## Release Rationale` section, the manifest, mapping and `AnomalyFields.json` define no default for any of its cells, and no schema, locator or mapping computes a cell from another field. | Test |
| FR-016-AC-9 | No field or table column of the `Anomaly` type holds a date, commit hash, release identifier, signature or sign-off of the rationale, or marks an anomaly accepted. | Inspection |
| FR-016-AC-10 | Two fixtures identical except for the presence of the section validate the same on every other finding. | Test |

## Dependencies

- **Upstream**: [FR-014](./FR-014-anomaly-archetype-and-state-lifecycle.md), [FR-015](./FR-015-anomaly-safety-impact-assessment.md), [FR-011](./FR-011-markdown-record-mapping.md), [FR-009](./FR-009-emitted-json-schemas.md), [FR-012](./FR-012-executable-skeletons.md)
- **Downstream**: quoin [FR-162](ix://agent-ix/quoin/FR-162), [FR-163](ix://agent-ix/quoin/FR-163), [FR-164](ix://agent-ix/quoin/FR-164)
