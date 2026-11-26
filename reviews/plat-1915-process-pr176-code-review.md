---
id: SR-967175026302197768900474181941935084895
title: "Code review — PLAT-1915 process test trace bindings PR 176"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process; spec/functional/FR-012-executable-skeletons.md, spec/tests.md, tests/test_mapping_failures.py, tests/test_markdown_mappings.py, tests/test_skeletons_and_roles.py; PR 176 @e03d14a097e50bdf0cfc9a2c9d083280257f3cc6"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-012"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/FR-013"
    type: references
---
# SR-967175026302197768900474181941935084895: Code review — PLAT-1915 process test trace bindings PR 176

## Summary

Reviewed PR #176's trace additions and the corrected FR-012 Standard properties wording at `e03d14a097e50bdf0cfc9a2c9d083280257f3cc6`. The trace links reviewed are correctly attached to tests for their named criteria, but three newly claimed older criteria have an oracle gap: exact negative-failure reasons, multi-token ordering, and the complete unmodeled-concepts list are not asserted.

## Verdict

**CONDITIONAL** — three medium findings remain in tests used to support FR-012-AC-7, FR-013-AC-5 and FR-013-AC-6.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The negative fixture test accepts extra mapping failures instead of requiring exactly the declared failure. | tests/test_mapping_failures.py:57 |
| FND-002 | medium | The matrix-token test checks a one-token list, so it cannot detect a reordered multi-token list. | tests/test_skeletons_and_roles.py:293 |
| FND-003 | medium | The unmodeled-concepts test checks only minimum count plus `run` and `baseline`; it can miss omitted binding-record or freshness ownership. | tests/test_skeletons_and_roles.py:303 |

## Review evidence

- `git diff --name-only origin/main...HEAD` is the five files in scope above; the worktree is clean at the reviewed head.
- Quoin 0.37.0 matrix (`npm_config_userconfig=/dev/null npm_config_cache=/tmp/npm-cache-quire npm exec --yes --package=@agent-ix/quoin@0.37.0 -- quoin matrix --repo . --json`) reports all 21 eligible `Test` / `Unit Test` criteria in FR-012 and FR-013 as tagged. FR-013-AC-9 was already tagged; the other 20 now have binders. FR-012-AC-9 is Integration and FR-013-AC-8 is Inspection, so neither is in the 21.
- The tests are behavioral and use real mapping/schema/CLI paths. The changed tags match their criterion assertions; no wrong test-to-criterion binding was found.
- Coder-reported focused evidence: 218 passed, 2 integration tests deselected; Ruff and Black passed; Quire CLI validation passed. Reviewer did not rerun tests.

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
