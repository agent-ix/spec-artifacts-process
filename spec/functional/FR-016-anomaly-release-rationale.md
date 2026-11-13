---
id: FR-016
title: "Anomaly release rationale: a human-authored, named reason for releasing with an anomaly not fixed"
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
  - target: "ix://agent-ix/spec-artifacts-process/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-012"
    type: "depends_on"
---
# FR-016: Anomaly release rationale: a human-authored, named reason for releasing with an anomaly not fixed

## Description

The `Anomaly` type ([FR-014](./FR-014-anomaly-archetype-and-state-lifecycle.md)) SHALL accept an
optional `## Release Rationale` section in which a named person states why releasing with this
anomaly while it is not fixed is justified. An anomaly that is not `closed`, or is `closed` as `wont-fix` (a defect deliberately shipped), is a **carried** anomaly in quoin's term (FR-162), and it is the one that may hold the section. The rationale is an engineer's written judgement, as the
safety-impact assessment is ([FR-015](./FR-015-anomaly-safety-impact-assessment.md)). The module
validates only its shape and the status it may appear at; the tools that read it (quoin
[FR-162](ix://agent-ix/quoin/FR-162) and [FR-164](ix://agent-ix/quoin/FR-164)) never write, fill in
or default it.

The record keeps no date, commit or signature of the rationale. Who wrote it and when is the git
history of the file, which quoin FR-163 reads, as it reads the history of `status`.

### Who owns which check

| Check | Owner |
|---|---|
| Section table shape, column names, row presence, `Author` and `Rationale` non-empty and not a placeholder, the section absent while `status` is `closed` with a `resolution` of `fixed`, `not-a-defect` or `duplicate` | This module (manifest, `assert` facet, `AnomalyFields.json`), as for FR-014 and FR-015 |
| The same rules stated for the mapped record | The emitted record schema `Anomaly.json` (FR-009), as FR-014 and FR-015 state theirs (quoin FR-073) |
| Whether a carried anomaly needs a rationale, and whether the rationale is the author's own | Not this module: quoin FR-164 decides the first; the second is a person's attestation recorded by git, not a check |

## Inputs

- The optional `## Release Rationale` section of an `Anomaly` document, and its frontmatter `status`.

## Outputs

- A validated rationale, or located validation failures.
- The record key `releaseRationale` ([FR-011](./FR-011-markdown-record-mapping.md)).

## Behavior

- The `Anomaly` type SHALL accept a `## Release Rationale` section at any `status` other than `closed`.
- The `Anomaly` type SHALL accept the section at `status` `closed` when `resolution` is `wont-fix`, because that is how a defect deliberately shipped unfixed is closed (FR-014).
- The `Anomaly` type SHALL NOT require the section at any `status`.
- If `status` is `closed` and `resolution` is `fixed`, `not-a-defect` or `duplicate`, then validation SHALL fail an `Anomaly` that carries the section, at the section heading line.
- The closed-status rule SHALL apply only to a `resolution` present and in the FR-014 vocabulary, so a `closed` anomaly with no `resolution`, or one outside it, yields the finding FR-014 reports and no finding for the section. `AnomalyFields.json` SHALL encode the rule with a condition that requires `resolution` to be present and one of those three values, so that it does not hold vacuously on an absent key.
- The `Anomaly` archetype SHALL declare a `release_rationale` locator (`required: false`) for the section in its `yield_pattern.match`, and `AnomalyFields.json` carries the section rules over that property.
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
- The emitted record schema `Anomaly.json` SHALL state the same rules for the mapped record: the `releaseRationale` entry shape, the non-empty and placeholder rules for `author` and `rationale`, and the closed-status rule.
- The module SHALL ship, as fixtures for the criteria below, valid `impacting` anomalies at `identified`, `assessed` and `resolved` that carry the section, each with a counterpart identical but for the section (AC-10), and a valid `impacting` `closed` `wont-fix` anomaly that carries a `closed_by` and the section, with a counterpart identical but for the section (quoin FR-164-AC-5).
- The `closed_by` of the shipped `closed` `wont-fix` fixture SHALL differ from the `Author` of every row of its section, so that a reader can tell the typed rationale author from the closer (quoin FR-163-AC-4).
- The module SHALL ship the negatives of AC-2 to AC-6. Quoin holds no copy of these documents.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-016-AC-1 | An `impacting` anomaly at `identified`, `assessed` and `resolved` that carries a well-formed `## Release Rationale` validates, and the same anomalies without the section validate. | Test |
| FR-016-AC-2 | A `closed` anomaly with `resolution` `fixed`, `duplicate` or `not-a-defect` that carries a well-formed `## Release Rationale` fails validation, at the section heading line; a `closed` anomaly with `resolution` `wont-fix`, a `closed_by` and the section validates; a `closed` anomaly with no `resolution`, or a `resolution` outside the vocabulary, and the section yields the one FR-014 finding and no finding for the section. | Test |
| FR-016-AC-3 | A row whose `Author` is empty, or `TBD`, `unknown`, `n/a`, `none` or `-` in any letter case, fails validation, at the row's line; the same row with a non-placeholder `Author` passes. | Test |
| FR-016-AC-4 | A row whose `Rationale` is empty, or `TBD`, `unknown`, `n/a`, `none` or `-` in any letter case, fails validation, at the row's line; the same row with a non-placeholder `Rationale` passes. | Test |
| FR-016-AC-5 | A section whose headers are not exactly `Author \| Rationale`, or that has no row, fails validation, at the section heading line. | Test |
| FR-016-AC-6 | A `closed` `fixed` anomaly whose section has a placeholder `Author` and an empty `Rationale` yields one finding for the section, one for the author and one for the rationale, in one run, the section finding at the section heading line and the others at their row's line. | Test |
| FR-016-AC-7 | The mapping lists `releaseRationale` for `Anomaly` as a `typed-table` entry set with `author` and `rationale` as authored; the key is absent for an anomaly without the section; and the emitted `Anomaly` schema declares it and rejects a mapped record with a placeholder or empty `author` or `rationale`, and one with a `releaseRationale` on a `closed` `fixed` anomaly. | Test |
| FR-016-AC-8 | The shipped skeleton contains no `## Release Rationale` section, the manifest, mapping and `AnomalyFields.json` define no default for any of its cells, and no schema, locator or mapping computes a cell from another field. | Test |
| FR-016-AC-9 | No field or table column of the `Anomaly` type holds a date, commit hash, release identifier, signature or sign-off of the rationale, or marks an anomaly accepted. | Inspection |
| FR-016-AC-10 | Two fixtures identical except for the presence of the section validate the same on every other finding. | Test |
| FR-016-AC-11 | The `Anomaly` `yield_pattern.match` carries a `release_rationale` locator with `required: false`, and `AnomalyFields.json` names the property `release_rationale`. | Test |

## Dependencies

- **Upstream**: [FR-014](./FR-014-anomaly-archetype-and-state-lifecycle.md), [FR-015](./FR-015-anomaly-safety-impact-assessment.md), [FR-011](./FR-011-markdown-record-mapping.md), [FR-009](./FR-009-emitted-json-schemas.md), [FR-012](./FR-012-executable-skeletons.md)
- **Downstream**: quoin [FR-162](ix://agent-ix/quoin/FR-162), [FR-163](ix://agent-ix/quoin/FR-163), [FR-164](ix://agent-ix/quoin/FR-164)
