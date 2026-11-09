---
id: SR-16443
title: "PLAT-847 process PR131 gap-analysis"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process PR131 @a7b0683 over origin/main e1af989; spec_artifacts_process/manifest.yaml trace_tags, tests/**/*.py trace evidence, spec/tests.md"
review_set: subset
---

## Summary

Ticket: PLAT-847. Planless gap analysis. Plan completion: not assessed.

The removed criteria have no surviving code or tests. Every remaining FR-004
criterion that the diff touches still has its test. Interface-id coverage
through markers and `implements` is intact.

The gap is this repository's own evidence. Until now its tests bound to the
Test Matrix mostly through the `python-docstring-id` legacy form, and that form
is deleted here. Static measurement at a7b0683 (AST walk of tests/*.py):

- 67 test functions carry `@pytest.mark.trace(...)`, and those markers bind 65
  distinct ids.
- 70 test functions carry an id only as the docstring's first token
  (`"""TC-NNN (FR-...)`) and have no marker. Those docstrings name 70 ids
  (64 TC ids, plus FR-003, FR-007, FR-010-AC-6 and FR-011-CON-1) that no marker
  anywhere binds.

Today those 70 tests bind through `python-docstring-id`. After this PR they
bind nothing on any engine. An older engine reading this manifest has no
legacy form to apply. The new engine never binds docstrings. So TC-001..TC-018,
TC-024..TC-030, TC-032..TC-034, TC-036..TC-055, TC-060..TC-064,
TC-067..TC-070, TC-072..TC-074, TC-076 and TC-147..TC-151 lose their backing,
while spec/tests.md still marks them ✅. TC-033 (FR-004-AC-6) still passes,
because it asks only for a non-zero backed count.

`quire coverage` was not run to confirm the delta. The installed CLI (0.36.2)
cannot load this manifest (`unknown field `syntax``), and quire-cli main does
not compile against the quire-rs #627 engine. The numbers above come from the
source AST, not from the engine.

## Verdict

**CONDITIONAL.** Sweep the 70 docstring-only tests onto
`@pytest.mark.trace(...)` in this PR. The sweep is mechanical, the ids are
already in each docstring, and it is this repo's own blast radius. Without it,
dropping the forms leaves ~64 ✅ matrix rows unbacked in the module's own
repository.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | Deleting `python-docstring-id` unbinds 70 of this repo's own tests whose only tag is the docstring's leading id. Their 70 ids, including 64 TC ids such as TC-001..TC-018, TC-028..TC-030 and TC-147..TC-151, are bound by no `@pytest.mark.trace` marker, so the matching ✅ rows in spec/tests.md go unbacked. The PR does not migrate them and does not state the delta. Add `@pytest.mark.trace("<ids>")` to each, using the ids already in the docstring. | tests/test_testmatrix_body_extraction.py; tests/test_manifest.py; tests/test_traceability_declaration.py; tests/test_verification_catalog.py; tests/test_evidence_archetypes.py; spec/tests.md |

## Examined scope

```yaml
scope:
- id: FR-004-AC-6
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: "`quire coverage` over this repo reports a non-zero backed count and mints no rows from `tests/fixtures/`"
- id: FR-004-AC-3
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: "`trace_tags.markers` declares exactly one marker for each of rust, python and typescript, and each declares a `template`"
- id: FR-004-AC-10
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: "`trace_tags.implements` declares exactly the existing templated Rust `Implements:` line-comment form plus the new templated Rust `#[implements(...)]` attribute form, and exactly one templated `Implements:` line-comment form each for Python and TypeScript."
- id: FR-004-AC-19
  path: spec/functional/FR-004-traceability-declaration.md
  role: context_only
  excerpt: "an `interface_NNN-AC-N` id resolves everywhere an `FR`/`NFR` acceptance-criterion id already does"
```

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | still-open | Round 1 (head 42249eb): 70 tests gained `@pytest.mark.trace(...)`. Every marker id appears in its docstring's head, none is invented, and each AC agrees with the TC's Traces To row. All 137 marker lines fully match the manifest's `pytest-trace-marker` pattern. Four ids the finding named are still bound by no marker. (1) TC-151: `test_verification_lint_rule_allowed_set_is_classes_union_catalog` (tests/test_traceability_declaration.py:843) carries only `FR-004-AC-22`, so the TC-151 row is unbacked. (2) `test_malformed_traces_to_fails` (tests/test_testmatrix_body_extraction.py:245, docstring "TC-013 (FR-003-AC-6)") has no marker at all. The review's own count missed it because a parametrize decorator containing "traces-to" read as a trace marker. (3) FR-010-AC-6, on `test_an_unknown_key_is_refused` (tests/test_semantic_manifest.py:57), which is marked only "TC-094". (4) FR-011-CON-1, on `test_every_named_section_and_column_is_declared_by_the_manifest` (tests/test_markdown_mappings.py:121), which is marked only "TC-099". Add TC-151 to the first marker, `@pytest.mark.trace("TC-013", "FR-003-AC-6")` to the second, and the docstring ids to the last two. |
