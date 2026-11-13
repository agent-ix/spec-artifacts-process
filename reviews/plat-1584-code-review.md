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

## New findings (disposition pass 2)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-004 | low | A section with headers but no data row (`rationale-no-rows`) now yields two diagnostics at the heading for one defect: the `assert` finding "table has 0 data row(s) but assert requires at least 1", and the new no-row rule. At a4141f7 it yielded one. Tests still pass, because TC-211 asserts only the heading line. Exclude that case from the new rule, or accept the duplicate with a stated reason. | spec_artifacts_process/schemas/AnomalyFields.json:169-175 |

## New findings (disposition pass 3)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-005 | low | The delimiter-row pattern does not check for a header line. A section holding only `\|---\|---\|`, or `\|---\|---\|` followed by `\| TBD \| n/a \|` (no header), or prose followed by `\| - \|` still validates with no diagnostic. These are not tables, so they have no row, and the second hides two placeholder cells. Requiring a pipe header line before the delimiter fixes all three without bringing back FND-004: `(?m)^[ \t]*\\|.*\\|[ \t]*\n[ \t]*\\|[ \t:\|-]*-[ \t:\|-]*$`. On a scratch copy of the module it gives exactly one finding for each of these three cases and for all five TC-211 fixtures, keeps fixture (d) at 3, and passes prose-then-table and every valid fixture. Malformed tables like these are uncommon, so this does not block merge. | spec_artifacts_process/schemas/AnomalyFields.json:174-180 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | still-open | Round 1 (head a4141f7): Partly fixed at a4141f7. A bare heading and a heading followed by prose now fail at the heading (probed). Two things remain. (1) A pipe table with no delimiter row (`\| Author \| Rationale \|` then `\| TBD \| n/a \|`) is not a table, so it has no row, and it still validates with no diagnostic, hiding two placeholder cells. `(?m)^[ \t]*\\|` only checks for a line that starts with a pipe. The exact rule is `if: {required: [release_rationale_section], not: {required: [release_rationale]}}, then: {properties: {release_rationale_section: false}}`. It is still reported at the heading line. (2) No test references `rationale-bare-heading` or `rationale-heading-prose`, so nothing asserts the fix. Add both, plus a no-delimiter fixture, to the FR-016-AC-5 / TC-211 parametrize. |
| FND-002 | fixed | Round 1 (head a4141f7): for rule in fields["allOf"]:     then = rule.get("then", {}).get("properties", {})     assert "release_rationale" not in then     assert then.get("release_rationale_section") in (None, False) assert "default" not in json.dumps(fields["allOf"]) |
| FND-003 | fixed | Round 1 (head a4141f7): @pytest.mark.trace("FR-016-AC-8", "TC-214") |
| FND-001 | still-open | Round 2 (head 99cf488): The rule is fixed. The test half is not. At 99cf488 `AnomalyFields.json` carries `if: {required: [release_rationale_section], not: {required: [release_rationale]}}, then: {properties: {release_rationale_section: false}}`. Probed through `quire validate`: `rationale-no-delimiter`, `rationale-bare-heading`, `rationale-heading-prose` and a header-only, no-delimiter section each fail at the heading line (23). Prose followed by a well-formed table passes, and so do the six with/without fixtures and `closed-wont-fix-rationale`. Fixture (d) still gives 3 findings. The commit does not touch tests/test_anomaly.py. The TC-211 parametrize (line 1266) is still `["rationale-bad-headers", "rationale-no-rows"]` and no test references the three new fixtures, so nothing asserts the fix. Fix: add `rationale-no-delimiter`, `rationale-bare-heading` and `rationale-heading-prose` to that parametrize. The test body already asserts the heading line. |
| FND-001 | fixed | Round 3 (head f04b47e): "then": {"properties": {"release_rationale_section": {"pattern": "(?m)^[ \t]*\\|[ \t:\|-]*-[ \t:\|-]*$"}}} with TC-211 parametrized over rationale-bad-headers, rationale-no-rows, rationale-no-delimiter, rationale-bare-heading and rationale-heading-prose, asserting finding_lines(found) == [heading_line(path, "Release Rationale")]. Probed: each of the five gives exactly one finding at line 23. |
| FND-004 | fixed | Round 3 (head f04b47e): rationale-no-rows now yields exactly one diagnostic: line 23 [Anomaly] 'release_rationale': table has 0 data row(s) but assert requires at least 1 [assert]. |
