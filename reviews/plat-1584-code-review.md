---
id: SR-20261113084038
title: "PLAT-1584 spec-artifacts-process PR148 code-review"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR148 @d95f76c over origin/main; spec_artifacts_process/{manifest.yaml,mappings.yaml,schemas/AnomalyFields.json,schemas/Anomaly.json,schemas/NamedText.json,schemas/ReleaseRationaleRow.json,semantic/main.tsp,skeletons/Anomaly.md}; tests/test_anomaly.py; tests/fixtures/anomaly/**"
review_set: subset
---

## Summary

Ticket: PLAT-1584. Code review of the FR-016 release-rationale slice (commit d95f76c). The cell rules sit in `AnomalyFields.json` rather than in manifest `column_patterns`, which FR-016's ownership table permits. That keeps the author, rationale and section findings in one run (NFR-001 fixture d gives 3 findings). The extra `release_rationale_section` (`section_body`) key reports the closed-status rule at the heading line, and FR-014's verbatim-key rule is kept. The placeholder set and the trimming are identical to `closed_by` (FR-014) and to quoin FR-164 (`x` counts, `TBD`/`n/a`/`-`/`none`/`unknown` in any case do not). The closed rule requires `resolution` to be present and in {fixed, not-a-defect, duplicate}. The closed wont-fix fixture's `closed_by` (Dana Lee) differs from its only Author (Morgan Reyes). Each with/without pair differs only by the section (diffed), quoin FR-164-AC-5 included.

## Verdict

**CONDITIONAL.** One real edge-case defect (FND-001) plus two low test-quality findings.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | A `## Release Rationale` heading with no table validates on a non-closed anomaly. Reproduced on `rationale-assessed-without` plus a bare heading, and plus a heading followed by prose only: `quire validate` exits 0 with no diagnostic, and the mapped record has no `releaseRationale`. FR-016 requires the section to be a table with at least one row, and AC-5 says a section with no row fails at the heading. The `table_row` locator's `min_rows` does not fire when there is no table. Fix: in `AnomalyFields.json`, `if required [release_rationale_section] then required [release_rationale]`. The section key already exists and reports at the heading. Add the two negatives. | spec_artifacts_process/schemas/AnomalyFields.json:374-386 |
| FND-002 | low | The final loop in `test_the_skeleton_has_no_release_rationale_and_nothing_defaults_or_computes_it` checks `"release_rationale" not in then.properties`. The only rule that touches the section names `release_rationale_section`, so the first disjunct is always true and the assertion cannot fail. Drop it, or assert something that can fail. | tests/test_anomaly.py:1371-1374 |
| FND-003 | low | The TC-214 test is also tagged `FR-014-AC-14`, but TC-214 traces only FR-016-AC-8. `quire matrix` reports `criterion-tagged-outside-row` and the tag gives no backing (TC-195 already backs AC-14). Remove the extra tag. | tests/test_anomaly.py:1355 |

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
