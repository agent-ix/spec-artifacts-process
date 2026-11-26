---
id: SR-967175026302197768900474181941935084891
title: "Code review — PLAT-1915 older process test criteria (PR 174)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR 174 @e35aeff2060f93d0ed5670a3f972f9cf15460c91; tests/test_semantic_manifest.py, tests/test_semantic_schemas.py, tests/test_verification_catalog.py"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-007"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/FR-009"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/FR-010"
    type: references
---
# SR-967175026302197768900474181941935084891: Code review — PLAT-1915 older process test criteria (PR 174)

## Summary

Ticket: PLAT-1915. Reviewed the three changed test modules in `git diff origin/main...HEAD` at `e35aeff2060f93d0ed5670a3f972f9cf15460c91`, focusing on the added FR-007/009/010 bindings and whether each test has a discriminating oracle. The criterion tags match the assertions; focused reruns passed, with the existing FR-010-AC-9 strict expected failure.

## Verdict

**PASS** — no trace-binding, test-intent, or oracle-strength defects found in the changed tests. This is a test-only change, so production/spec gap analysis and separate spec analyses were not applicable.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |

## Review evidence

- `git diff origin/main...HEAD` contains only the three scoped test files.
- `quire trace --file` shows the changed criterion markers on the intended test functions. The CLI labels these matches `line_heuristic`; I checked the marker placement and test bodies directly.
- Focused command, run through `/home/peter/dev/worktrees/locked-build.sh`: selected 17 test nodes from the three changed files; **16 passed, 1 xfailed** in 26.90s. The xfail is the declared strict expected failure for FR-010-AC-9.
- The new CLI-backed FR-010 tests check schema resolution for each manifest artifact type and validate both Standard artifact/object dispatch cases; the FR-009 npm staging test checks the staged manifest bytes and full schema set against the authoritative package.

## Reviewed criteria and bindings

| Criterion | Test binding | Review |
| --- | --- | --- |
| FR-010-AC-1 | `test_semantic_block_carries_exactly_the_admitted_keys` | Exact admitted keys and values; exports derived from manifest. |
| FR-010-CON-1 | `test_semantic_block_carries_exactly_the_admitted_keys` | Set equality rejects any extra semantic key. |
| FR-010-AC-5 | `test_the_module_loads_with_every_declared_archetype` | Iterates manifest archetypes and requires successful CLI schema resolution with matching archetype name. |
| FR-010-AC-8 | `test_the_standard_object_type_is_governed_by_its_locator`; `test_the_engine_requires_code_on_a_standard` | Declaration shape and locator source/required flag are checked; CLI validates artifact and object dispatch, missing code, and invalid code. |
| FR-010-AC-9 | `test_the_refusal_names_the_offending_key` | Strict xfail asserts the offending key in refusal diagnostics, matching the criterion's documented current gap. |
| FR-010-CON-3 | `test_the_status_and_type_vocabularies_have_one_source` | Exact equality checks admitted and classed status symbols. |
| FR-009-AC-2 | `test_every_projection_declares_the_id` | Checks `$schema` and exact file-name-derived `$id` on every projection. |
| FR-009-AC-3 | `test_every_ref_resolves_to_a_sibling_or_to_semantic_core` | Each reference is constrained to a shipped sibling or semantic-core model. |
| FR-009-AC-4 | `test_check_is_clean_and_fails_on_one_changed_byte` | Clean check, mutation failure naming the projection, and no rewrite. |
| FR-009-AC-6 | `test_a_stale_projection_is_named_and_frontmatter_schemas_are_left_alone` | Stale projection is named; hand-authored frontmatter schemas stay unchanged. |
| FR-009-AC-7 | `test_the_wheel_and_the_npm_tree_carry_every_projection` | Wheel contents and staged manifest/schema set are checked against source bytes. |
| FR-009-AC-8 | `test_two_runs_are_byte_identical` | Snapshots generated outputs across two runs and compares bytes. |
| FR-009-AC-10 | `test_a_missing_toolchain_names_the_component_and_the_install` | Missing-toolchain path checks nonzero status and actionable component/install diagnostics. |
| FR-009-CON-3 | `test_two_runs_are_byte_identical` | Byte-for-byte determinism assertion. |
| FR-007-AC-12 | `test_tc055_obligation_sources_are_declared` | Checks combinatorial strength and the exclusions column on the configuration-matrix source. |
| FR-007-AC-9 | `test_tc056_compile_time_and_dynamic_analysis_are_catalogued` | Checks both catalog entries, classes, evidence kinds, and distinction from neighboring methods. |
| FR-007-AC-10 | `test_tc057_no_entry_names_a_tool_a_class_or_a_cadence` | Rejects cadence/class/tool names as method ids and verifies tooling is confined to tooling. |
| FR-007-AC-11 | `test_tc065_a_declared_hazard_advises_fault_injection` | Checks hazard and failure-mode applicability and the retained fault-injection entry. |
