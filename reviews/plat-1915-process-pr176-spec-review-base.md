---
id: SR-967175026302197768900474181941935084896
title: "Base spec review — PLAT-1915 process test trace bindings PR 176"
type: SpecReview
analysis: base
scope: "agent-ix/spec-artifacts-process; spec/functional/FR-012-executable-skeletons.md, spec/functional/FR-013-definitions-not-occurrences.md, spec/tests.md, tests/test_mapping_failures.py, tests/test_markdown_mappings.py, tests/test_skeletons_and_roles.py; PR 176 @e03d14a097e50bdf0cfc9a2c9d083280257f3cc6"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-012"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/FR-013"
    type: references
---
# SR-967175026302197768900474181941935084896: Base spec review — PLAT-1915 process test trace bindings PR 176

## Summary

Reviewed the changed FR-012 statement, Test Matrix rows, and all 21 eligible `Test` / `Unit Test` criterion bindings from FR-012 and FR-013. The clarified Standard table-versus-sysml wording is consistent, but the touched test suite contains file-scanning test oracles that the checklist prohibits.

## Verdict

**FAIL** — four high findings identify tests that scan fixture or skeleton files to establish criterion coverage or location.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The test bound to AC-1 enumerates skeleton files to establish their count, which the checklist prohibits. | tests/test_skeletons_and_roles.py:104 |
| FND-002 | high | The test bound to AC-8 enumerates fixture files and parses them to derive the rejection inventory. | tests/test_mapping_failures.py:64 |
| FND-003 | high | The test bound to AC-10 scans every skeleton file and its contents to locate the typed table. | tests/test_markdown_mappings.py:285 |
| FND-004 | high | The new CON-3 test recursively scans repository Markdown files and inspects their frontmatter. | tests/test_mapping_failures.py:76 |

## Coverage review

- The changed FR-012 statement now distinguishes the `Standard.md` typed table from `Standard.sysml.md`'s `sysml` declaration. FR-012-AC-10 and TC-141 express that same distinction.
- All 21 eligible criteria have at least one live test tag in the Quoin 0.37.0 matrix. FR-012-AC-9 uses Integration; FR-013-AC-8 uses Inspection and is excluded from the eligible set. FR-013-AC-9 was already tagged before this PR.
- The row↔criterion intent is consistent across the changed Test Matrix entries and the test marker bindings. Three oracle gaps are recorded separately in the code-review artifact.
- `quire validate --scope . 'spec/**/*.md' --summary` exited 0. Its EARS warnings concern unchanged FR-004, FR-020 and FR-024 statements.
- No applicable AssuranceProfile was found under `spec/`.

## Reviewed criteria and bindings

| Criterion | Binding reviewed |
| --- | --- |
| FR-012-AC-1 | `test_every_declared_type_has_exactly_one_skeleton` |
| FR-012-AC-2 | `test_every_skeleton_validates_against_its_own_archetype` |
| FR-012-AC-3 | `test_each_skeleton_maps_to_a_record_that_validates` |
| FR-012-AC-4 | `test_every_skeleton_validates_against_its_own_archetype`; `test_every_required_section_is_present_in_its_skeleton` |
| FR-012-AC-5 | `test_the_two_standard_forms_declare_the_same_fields` |
| FR-012-AC-6 | `test_the_added_standard_locators_are_optional_and_omittable` |
| FR-012-AC-7 | `test_each_negative_fails_exactly_the_check_it_names`; `test_no_negative_fixture_passes` |
| FR-012-AC-8 | `test_the_negative_corpus_covers_every_stated_rejection` |
| FR-012-AC-10 | `test_only_standard_md_carries_the_typed_properties_table` |
| FR-012-AC-11 | `test_the_golden_record_is_reproduced_exactly` |
| FR-012-CON-1 | `test_every_skeleton_validates_against_its_own_archetype` |
| FR-012-CON-2 | `test_the_added_standard_locators_are_optional_and_omittable` |
| FR-012-CON-3 | `test_negative_fixtures_live_only_in_the_test_tree` |
| FR-013-AC-1 | `test_every_model_carries_exactly_one_role` |
| FR-013-AC-2 | `test_no_model_declares_a_run_property` |
| FR-013-AC-3 | `test_plan_and_task_declare_no_execution_property` |
| FR-013-AC-4 | `test_the_finding_document_and_the_findings_row_keep_distinct_namespaces` |
| FR-013-AC-5 | `test_matrix_rows_carry_their_trace_tokens_as_a_list` |
| FR-013-AC-6 | `test_the_unmodelled_concepts_name_their_owner` |
| FR-013-AC-9 | `test_omitted_optional_priority_and_status_yield_no_keys`; `test_testcase_status_is_optional_in_the_emitted_record_schema`; `test_status_column_may_be_omitted`; `test_quire_matrix_computes_criterion_coverage_without_status` |
| FR-013-CON-1 | `test_every_model_carries_exactly_one_role` |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
