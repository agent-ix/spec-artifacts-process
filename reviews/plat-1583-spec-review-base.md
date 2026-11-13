---
id: SR-20261113084037
title: "PLAT-1583 spec-artifacts-process PR148 spec-review/base"
type: SpecReview
analysis: base
scope: "agent-ix/spec-artifacts-process PR148 @d95f76c over origin/main; spec/tests.md (TC-174, TC-186 edits; TC-195..216 added)"
review_set: subset
---

## Summary

Ticket: PLAT-1583. Spec review of the TestMatrix edits. TC-195..216 restate their criteria, each traces to the one AC it verifies, ids are contiguous after TC-194 (already used by FR-003-AC-14), and `quire validate --module spec_artifacts_process spec/tests.md` passes. Nothing is kept by hand beyond the columns the TestMatrix schema requires. The inspection ACs (FR-014-AC-18, FR-015-AC-18, FR-016-AC-9) get no TC row, which is correct.

## Verdict

**PASS with one low finding.** TC-203's status overstates a clause that is a strict xfail (FND-001).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | TC-203 is marked ✅ although its first clause (Criterion row targeting FR-001) is a strict xfail. The file's own convention for that case is `❌ strict expected failure: quire-rs#221`. Mark TC-203 the same way and cite the upstream ticket from SR-20261113084036 FND-001. | spec/tests.md:203 |

## Examined scope

```yaml
scope:
- id: TC-174
  path: spec/tests.md
  role: examined
  excerpt: The mapping lists `status`, `resolution`, `closedBy`, `severity`, `safetyImpact`, `assessment`, `verification` and `releaseRationale` for `Anomaly`, each named by exactly one entry, and the golden record built from the skeleton validates against the emitted `Anomaly` schema.
- id: TC-186
  path: spec/tests.md
  role: examined
  excerpt: Validating fixture (a), (b), (c) or (d) yields exactly one diagnostic per injected defect in that fixture.
- id: TC-195
  path: spec/tests.md
  role: examined
  excerpt: 'The `Anomaly` `yield_pattern.match` carries a `severity` `frontmatter_field` locator (`required: false`) whose `assert` is `choices` of exactly `minor`, `major`, `critical`, and the manifest and `AnomalyFields.json` define no default for `severity`.'
- id: TC-196
  path: spec/tests.md
  role: examined
  excerpt: For each of `assessed`, `resolved` and `closed`, a fixture with no `severity` fails, reported at the `status` line; an `identified` fixture with no `severity` validates.
- id: TC-197
  path: spec/tests.md
  role: examined
  excerpt: A fixture whose `severity` is outside the vocabulary (including `high`, `Major` and the empty string) fails with exactly one finding, at the `severity` line.
- id: TC-198
  path: spec/tests.md
  role: examined
  excerpt: Two fixtures identical except for one differing field (`safety_impact`, or the assessment rows) validate with the same `severity`, and no schema, locator or mapping of the `Anomaly` type computes `severity` from another field.
- id: TC-199
  path: spec/tests.md
  role: examined
  excerpt: 'The manifest declares the `## Fix Verification` table with exactly the columns `Kind`, `Target`, `Rationale`, `min_rows: 1` and the `Kind` vocabulary `Criterion`, `Test`, and declares a document reference `anomaly-fix-verification` with `column` `Target`, `kind_column` `Kind`, `targets` listing `acceptance-criterion`, `nfr-acceptance-criterion`, `test-case`, `requirement-document`, `nfr-document` and `hazard-document`, and `kind_targets` `Criterion` to the acceptance-criterion targets and `Test` to `test-case`; and it declares a `column_patterns` rule on `Target` requiring an id token.'
- id: TC-200
  path: spec/tests.md
  role: examined
  excerpt: A `resolved` anomaly and a `closed` anomaly with `resolution` `fixed` each fail validation, at the `status` line, with no `## Fix Verification` section; a `closed` anomaly with `resolution` `not-a-defect`, `duplicate` or `wont-fix` and no section validates.
- id: TC-201
  path: spec/tests.md
  role: examined
  excerpt: In the corpus of AC-4 plus a `TestMatrix` test case `TC-001`, a `fixed` anomaly with a `Criterion` row targeting `FR-001-AC-1` and a `Test` row targeting `TC-001` validates.
- id: TC-202
  path: spec/tests.md
  role: examined
  excerpt: In that corpus, a `Criterion` row targeting `FR-001-AC-99` and a `Test` row targeting `TC-999` each fail as a dangling reference naming the id and its row.
- id: TC-203
  path: spec/tests.md
  role: examined
  excerpt: In that corpus, a `Criterion` row targeting `FR-001` (a requirement document), a `Criterion` row targeting the hazard, and a `Test` row targeting `FR-001-AC-1` each fail as a kind mismatch.
- id: TC-204
  path: spec/tests.md
  role: examined
  excerpt: A row with an empty `Rationale` or a `Kind` outside the vocabulary fails validation.
- id: TC-205
  path: spec/tests.md
  role: examined
  excerpt: The mapping yields `verification` entries with `kind`, `target` and `rationale` as authored.
- id: TC-206
  path: spec/tests.md
  role: examined
  excerpt: A `fixed` anomaly whose only row is `Test`, `-`, `verified`, and one whose only row has an empty `Target`, each fail validation at the row.
- id: TC-207
  path: spec/tests.md
  role: examined
  excerpt: An `impacting` anomaly at `identified`, `assessed` and `resolved` that carries a well-formed `## Release Rationale` validates, and the same anomalies without the section validate.
- id: TC-208
  path: spec/tests.md
  role: examined
  excerpt: A `closed` anomaly with `resolution` `fixed`, `duplicate` or `not-a-defect` that carries a well-formed `## Release Rationale` fails validation, at the section heading line; a `closed` anomaly with `resolution` `wont-fix`, a `closed_by` and the section validates; a `closed` anomaly with no `resolution`, or a `resolution` outside the vocabulary, and the section yields the one FR-014 finding and no finding for the section.
- id: TC-209
  path: spec/tests.md
  role: examined
  excerpt: A row whose `Author` is empty, or `TBD`, `unknown`, `n/a`, `none` or `-` in any letter case, fails validation, at the row's line; the same row with a non-placeholder `Author` passes.
- id: TC-210
  path: spec/tests.md
  role: examined
  excerpt: A row whose `Rationale` is empty, or `TBD`, `unknown`, `n/a`, `none` or `-` in any letter case, fails validation, at the row's line; the same row with a non-placeholder `Rationale` passes.
- id: TC-211
  path: spec/tests.md
  role: examined
  excerpt: A section whose headers are not exactly `Author / Rationale`, or that has no row, fails validation, at the section heading line.
- id: TC-212
  path: spec/tests.md
  role: examined
  excerpt: A `closed` `fixed` anomaly whose section has a placeholder `Author` and an empty `Rationale` yields one finding for the section, one for the author and one for the rationale, in one run, the section finding at the section heading line and the others at their row's line.
- id: TC-213
  path: spec/tests.md
  role: examined
  excerpt: The mapping lists `releaseRationale` for `Anomaly` as a `typed-table` entry set with `author` and `rationale` as authored; the key is absent for an anomaly without the section; and the emitted `Anomaly` schema declares it and rejects a mapped record with a placeholder or empty `author` or `rationale`, and one with a `releaseRationale` on a `closed` `fixed` anomaly.
- id: TC-214
  path: spec/tests.md
  role: examined
  excerpt: The shipped skeleton contains no `## Release Rationale` section, the manifest, mapping and `AnomalyFields.json` define no default for any of its cells, and no schema, locator or mapping computes a cell from another field.
- id: TC-215
  path: spec/tests.md
  role: examined
  excerpt: Two fixtures identical except for the presence of the section validate the same on every other finding.
- id: TC-216
  path: spec/tests.md
  role: examined
  excerpt: 'The `Anomaly` `yield_pattern.match` carries a `release_rationale` locator with `required: false`, and `AnomalyFields.json` names the property `release_rationale`.'
```
