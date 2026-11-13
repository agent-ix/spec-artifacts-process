---
id: SR-20261113084039
title: "PLAT-1584 spec-artifacts-process PR148 gap-analysis"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process PR148 @d95f76c over origin/main; spec/functional/FR-016-anomaly-release-rationale.md AC-1..11; spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md; spec/tests.md TC-186, TC-207..216; tests/test_anomaly.py; tests/fixtures/anomaly/**"
review_set: subset
---

## Summary

Ticket: PLAT-1584. Planless gap analysis over FR-016-AC-1..11 and NFR-001-AC-1..2. Plan completion: not assessed. Every test-method criterion is `tagged` in `quire matrix`. Each runs `quire validate` on shipped fixtures and checks the located finding, and AC-7 also checks the mapped record against the emitted `Anomaly.json`. NFR-001 fixture (d) yields exactly 3 findings: the section finding at the heading, and the author and rationale findings at the row. AC-9 (inspection) is asserted over the emitted and row property sets. The FR-016 negatives of AC-2..AC-6 are all shipped. The one coverage gap (a section with no table) is code-review FND-001 of SR-20261113084038 and is not repeated here.

## Verdict

**PASS** on coverage, conditional on SR-20261113084038 FND-001 landing with its two negatives.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |

## Examined scope

```yaml
scope:
- id: FR-016-AC-1
  path: spec/functional/FR-016-anomaly-release-rationale.md
  role: examined
  excerpt: An `impacting` anomaly at `identified`, `assessed` and `resolved` that carries a well-formed `## Release Rationale` validates, and the same anomalies without the section validate.
- id: FR-016-AC-2
  path: spec/functional/FR-016-anomaly-release-rationale.md
  role: examined
  excerpt: A `closed` anomaly with `resolution` `fixed`, `duplicate` or `not-a-defect` that carries a well-formed `## Release Rationale` fails validation, at the section heading line; a `closed` anomaly with `resolution` `wont-fix`, a `closed_by` and the section validates; a `closed` anomaly with no `resolution`, or a `resolution` outside the vocabulary, and the section yields the one FR-014 finding and no finding for the section.
- id: FR-016-AC-3
  path: spec/functional/FR-016-anomaly-release-rationale.md
  role: examined
  excerpt: A row whose `Author` is empty, or `TBD`, `unknown`, `n/a`, `none` or `-` in any letter case, fails validation, at the row's line; the same row with a non-placeholder `Author` passes.
- id: FR-016-AC-4
  path: spec/functional/FR-016-anomaly-release-rationale.md
  role: examined
  excerpt: A row whose `Rationale` is empty, or `TBD`, `unknown`, `n/a`, `none` or `-` in any letter case, fails validation, at the row's line; the same row with a non-placeholder `Rationale` passes.
- id: FR-016-AC-5
  path: spec/functional/FR-016-anomaly-release-rationale.md
  role: examined
  excerpt: A section whose headers are not exactly `Author | Rationale`, or that has no row, fails validation, at the section heading line.
- id: FR-016-AC-6
  path: spec/functional/FR-016-anomaly-release-rationale.md
  role: examined
  excerpt: A `closed` `fixed` anomaly whose section has a placeholder `Author` and an empty `Rationale` yields one finding for the section, one for the author and one for the rationale, in one run, the section finding at the section heading line and the others at their row's line.
- id: FR-016-AC-7
  path: spec/functional/FR-016-anomaly-release-rationale.md
  role: examined
  excerpt: The mapping lists `releaseRationale` for `Anomaly` as a `typed-table` entry set with `author` and `rationale` as authored; the key is absent for an anomaly without the section; and the emitted `Anomaly` schema declares it and rejects a mapped record with a placeholder or empty `author` or `rationale`, and one with a `releaseRationale` on a `closed` `fixed` anomaly.
- id: FR-016-AC-8
  path: spec/functional/FR-016-anomaly-release-rationale.md
  role: examined
  excerpt: The shipped skeleton contains no `## Release Rationale` section, the manifest, mapping and `AnomalyFields.json` define no default for any of its cells, and no schema, locator or mapping computes a cell from another field.
- id: FR-016-AC-9
  path: spec/functional/FR-016-anomaly-release-rationale.md
  role: examined
  excerpt: No field or table column of the `Anomaly` type holds a date, commit hash, release identifier, signature or sign-off of the rationale, or marks an anomaly accepted.
- id: FR-016-AC-10
  path: spec/functional/FR-016-anomaly-release-rationale.md
  role: examined
  excerpt: Two fixtures identical except for the presence of the section validate the same on every other finding.
- id: FR-016-AC-11
  path: spec/functional/FR-016-anomaly-release-rationale.md
  role: examined
  excerpt: 'The `Anomaly` `yield_pattern.match` carries a `release_rationale` locator with `required: false`, and `AnomalyFields.json` names the property `release_rationale`.'
- id: NFR-001-AC-1
  path: spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md
  role: examined
  excerpt: Validating fixture (a), (b), (c) or (d) yields exactly one diagnostic per injected defect in that fixture.
- id: NFR-001-AC-2
  path: spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md
  role: examined
  excerpt: Every diagnostic from those runs carries a line; for an absence the line is that of the `status` field.
```
