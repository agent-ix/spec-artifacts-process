---
id: SR-20261112181935
title: "PLAT-1478 spec-artifacts-process PR142 code-review"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR142 @7205efb over origin/main 481a2b2; spec_artifacts_process/schemas/AnomalyFields.json, spec_artifacts_process/manifest.yaml, spec_artifacts_process/semantic/scripts/generate.mjs, tests/test_anomaly.py, pyproject.toml, poetry.lock, spec_artifacts_process/semantic/package.json, package-lock.json"
review_set: subset
---

## Summary

Ticket: PLAT-1478. Code review of the module side of record_validation for the
Anomaly archetype, scoped to `git diff origin/main...HEAD`.

Measured with quire 0.42.0 (engine 0.58.0) and a worktree venv holding quire
0.58.0. `@agent-ix/semantic-core` was supplied from a local 0.3.0 install
(pinned 0.3.3, not installable here). With it, `tests/test_anomaly.py` gives
69 passed and 1 xfailed on the PR head, and 67 passed and 3 xfailed on main.

- The real fixtures: all 11 valid documents pass `quire validate`. Every
  record-layer invalid fixture fails, with one `semantic.record-invalid`
  finding per defect. Absences are reported at the `status:` line and present
  values at their own line.
- 600 reviewer-written documents cover every combination of status (4) ×
  resolution (5) × closed_by (5) × safety_impact (3) × section (2). Each
  matches the FR-014/FR-015 prose in verdict, finding count and absence line.
  The only exception is that a placeholder `closed_by` on a non-closed anomaly
  is reported twice: once as forbidden and once as a placeholder.
- Mutation: removing `record_validation` from the manifest fails both
  record-layer test cases, as the PR claims. Of 9 schema mutants, 5 survive.
- generate.mjs: a stale `Stale.json` and a byte change to `Anomaly.json` are
  still reported. `AnomalyFields.json` is reported stale on main and is not
  reported on the PR head.
- The lock diffs contain only the quire 0.57.0 to 0.58.0 change and the
  quire-cli 0.41.0 to 0.42.0 entries.

## Verdict

**CHANGES REQUESTED.** The schema matches the FR prose. However, most of its
conditionals are pinned by no test at the layer that now runs them. FND-001
must be fixed. FND-002 restores coverage that already passed.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | 5 of 9 AnomalyFields.json mutants survive the whole suite. These are dropping the `resolution` forbidden-otherwise `else`, the resolved=>fixed rule, the `closed_by` forbidden-otherwise `else`, the identified none/impacting=>assessment rule, and the ClosedBy placeholder `$ref`. The FR-014-AC-4/5/6 and FR-015-AC-3/7 tests assert only the Python mapped-record path (Anomaly.json). The record_validation path (`quire validate`) is exercised only by fixtures (a) and (b). Add `quire_validate` assertions, with located lines, to those existing tests over the existing invalid fixtures. | tests/test_anomaly.py:157-226; tests/test_anomaly.py:291-312; spec_artifacts_process/schemas/AnomalyFields.json:28-71 |
| FND-002 | medium | The PR deletes the passing `test_fixture_c_empty_rationale_is_reported_once_with_its_line`. That test asserted that fixture (c)'s empty Rationale is reported once at its row line. The CLI can report this line today. The only remaining line assertion for fixture (c) is now inside the strict xfail, so a regression in that line goes unnoticed while TC-187 stays xfail. Keep the line assertion for the located defect in a passing test. | tests/test_anomaly.py:540-567 |
| FND-003 | low | An out-of-vocabulary `status` (for example `status: open` on an otherwise valid closed document) gives the `status` assert finding plus two spurious `<root>` findings from the `else` branches. These read "resolution is not allowed" and "closed_by is not allowed". A typo is reported as three defects, which works against NFR-001's one-defect-one-diagnostic intent. Scope the `else` branches to the legal non-closed statuses (`if status in [identified, assessed]` then `not required`). | spec_artifacts_process/schemas/AnomalyFields.json:29-50 |
| FND-004 | low | `isProjection` exempts every file whose name ends in `Fields.json`. A future TypeSpec model whose name ends in `Fields` would be emitted but never reported stale or removed. Matching on a hand-authored list, or on a marker in the file, would leave the projection check whole. | spec_artifacts_process/semantic/scripts/generate.mjs:172-178 |
| FND-005 | low | The module docstring of tests/test_anomaly.py still says the record layer is only "the document mapped by `mappings.yaml` and validated against the emitted `Anomaly.json`". The record_validation layer that `quire validate` now runs is not described. | tests/test_anomaly.py:1-17 |

## Examined scope

```yaml
scope:
- id: AnomalyFields.json
  path: spec_artifacts_process/schemas/AnomalyFields.json
  role: examined
  excerpt: "allOf: resolved/closed => resolution else not; resolved => fixed; closed => closed_by else not; assessed+ => assessment and safety_impact != unassessed; identified + none/impacting => assessment"
- id: manifest.yaml Anomaly
  path: spec_artifacts_process/manifest.yaml
  role: examined
  excerpt: "record_validation: {schema: schemas/AnomalyFields.json, locate_absence_at: status}; closed_by: {from: frontmatter_field, path: [closed_by], required: false}"
- id: generate.mjs isProjection
  path: spec_artifacts_process/semantic/scripts/generate.mjs
  role: examined
  excerpt: "name.endsWith('.json') && !name.endsWith('-frontmatter.schema.json') && !name.endsWith('Fields.json')"
- id: test_record_layer_defects_are_located
  path: tests/test_anomaly.py
  role: examined
  excerpt: "An absence is reported at the `status` line (`locate_absence_at`); a present-but-invalid value, such as `safety_impact: unassessed`, at its own."
- id: test_fixture_c_every_defect_carries_a_line
  path: tests/test_anomaly.py
  role: examined
  excerpt: "strict xfail: the quire CLI's bundle output (0.42.0) prints no line for a bundle finding"
```

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-006 | low | One AnomalyFields.json mutant survives the round-1 suite. Loosening the `none` row pattern from `^None\t-\tNone\t` to `^None\t[^\t]*\tNone\t` lets a `none` row with a `Target` other than `-` pass, and no test fails. FR-015 says a `none` table's single row has `Target` `-`. A fixture such as `none-with-target` (`None \| FR-001 \| None \| ...`) asserted in `test_quire_validate_reports_the_assessment_row_rules_inside_the_table` would pin the rule. This does not block merge. | spec_artifacts_process/schemas/AnomalyFields.json:93-106; tests/test_anomaly.py |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | - |
| FND-002 | fixed | - |
| FND-003 | fixed | - |
| FND-004 | fixed | - |
| FND-005 | fixed | - |
