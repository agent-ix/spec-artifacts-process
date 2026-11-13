---
id: SR-20261113081929
title: "PLAT-1499 spec-artifacts-process PR146 code-review"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR146 @5890952 over origin/main 26bf530; spec_artifacts_process/manifest.yaml, mappings.yaml, semantic/main.tsp, schemas/, skeletons/TestMatrix.md, skeletons/TestMatrixIndex.md, examples/, scripts/testmatrix_sweep.py, spec/tests.md, tests/"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-003"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/FR-004"
    type: references
---

## Summary

Ticket: PLAT-1499. Python/test lane code review of the implementation pass that
drops the hand-kept functional, stakeholder, user-story and non-functional
coverage tables from `TestMatrix`, and the `Requirements` and `Status` columns
from the `TestMatrixIndex` subsystem table, so `quire matrix` is the single
source of coverage.

Checked: manifest `body_extraction` (TestMatrix match is `test_cases` only;
TestMatrixIndex asserts `Subsystem | Local Matrix`, no `column_patterns`), the
`functional-coverage` document reference and its CR-062 comment are removed,
`mappings.yaml`, `semantic/main.tsp`, the four deleted row schemas, the
regenerated `TestMatrix.json`/`SubsystemIndexRow.json` (`npm run check`:
"schema projection is up to date (69 files)"), both skeletons and both example
records, the dead `FR_COVERAGE_HEADING` regex in the sweep script, all fixtures,
and the rewritten tests. A repo-wide grep for `functional_coverage`,
`FunctionalCoverageRow`, `stakeholder_coverage`, `user_story_coverage`,
`non_functional_coverage` and the camelCase forms finds no remnant outside
historical review and plan records and the merged spec's CR notes.

## Verdict

**CONDITIONAL.** The change is complete and correct; nothing was left behind,
the schemas match the TypeSpec source, and the focused suites pass (manifest,
body-extraction, traceability, markdown-mappings, skeletons, semantic schemas,
semantic manifest, evidence archetypes, mapping failures). Deleted fixtures
(`missing-fr-coverage`, `optional-tables-omitted`,
`optional-table-renamed-column`) covered only the dropped tables;
`priority-column-omitted` and the negative fixtures were kept and only lost
their coverage sections. The two findings below are test-strength and wording
issues, not behaviour defects.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | medium | TC-039 (`test_matrix_entries_are_not_enumerated_per_filename`) now selects matrix entries by `section == "Test Case Summary"`. A reintroduced TestMatrix-bound `document_references` entry reading any other section (the removed `functional-coverage` one included) is not selected, so the "exactly one entry per kind of table (`test-case`, `traces-to`)" claim of FR-004-AC-2 cannot fail for it, and no other test guards that removal. Select by `archetype == "TestMatrix"` instead; today that yields exactly `test-case` and `traces-to`. | tests/test_traceability_declaration.py:227 |
| FND-002 | low | TC-001 title in spec/tests.md still reads "Conforming TestMatrix (all tables) validates"; the conforming fixture now carries the Test Case Summary only. | spec/tests.md:12 |
