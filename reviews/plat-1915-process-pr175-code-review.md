---
id: SR-967175026302197768900474181941935084892
title: "Code review — PLAT-1915 Process FR-011 tests (PR 175)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR 175 @5d895334c63b276f3e84b526d77e41bea0f87aa3; tests/test_markdown_mappings.py, tests/test_mapping_failures.py, tests/test_semantic_manifest.py"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-011"
    type: references
---

## Summary

Reviewed the FR-011 behavior test changes, added trace bindings, and refreshed golden records in PR 175. One assertion does not establish that the shipped schema graph traversal visits every reachable schema.

## Verdict

**CONDITIONAL** — strengthen TC-138's shipped-graph assertion before relying on it for FR-011-AC-16 coverage.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | TC-138 only asserts that the traversal result contains its seed roots, which are present by construction; it can miss reachable child schemas in the shipped graph. | tests/test_markdown_mappings.py:127 |

## Review Evidence

The added and changed test markers point to the criteria their assertions address. I checked `quire trace` for both changed mapping test modules; criterion matches include line-heuristic results, and I verified the markers in source. The targeted suite passed: 136 tests. `git diff --check` passed.

The `npm exec --package=@agent-ix/quoin@0.37.0 -- quoin matrix --scope . --json` verification attempt failed before matrix execution with npm E401 (invalid authentication token). The installed `quire matrix --strict` exited non-zero because 60 repository criteria outside this PR remain untagged; the changed FR-011 binders were present in `quire trace`.

This PR changes no production code. No production gap analysis or Rust/React lane applied. The existing `FR-010-AC-9` xfail remains outside this diff's changed behavior and is not newly attributed here.

## Reviewed Criteria

| Unit | Role | Excerpt |
| --- | --- | --- |
| FR-011-AC-1 | examined | '`mappings.yaml` validates against `mappings.schema.json`, and every model FR-009 emits has an entry declaring the authority and the round-trip policy.' |
| FR-011-AC-2 | examined | Every property of every emitted model is named by exactly one mapping entry, and every mapping entry names a property its model declares. |
| FR-011-AC-3 | examined | Every section and column `mappings.yaml` names is declared by the manifest's `body_extraction` for that type. |
| FR-011-AC-4 | examined | For each shipped skeleton, the reference mapping builds a record that validates against that type's emitted schema, and the record equals the shipped `examples/<Type>.record.json` byte for byte. |
| FR-011-AC-5 | examined | A `Status` cell carrying a marker and a note splits into `marker` and `note`; a bare marker yields no `note`. |
| FR-011-AC-6 | examined | The `Traces To` parse expands the elided-parent and slash shorthands into the tokens they abbreviate, carries a parenthesised remainder as `note`, and maps a lone `-` to an empty list with `noTrace: true`. |
| FR-011-AC-7 | examined | A table omitting a declared optional column yields rows without that key rather than rows with a synthesised value. |
| FR-011-AC-8 | examined | Prose under the clause section yields an empty clause list; an orphan fence, a second fence in one subsection, an unterminated fence and a duplicate `clauseId` each report their named error and build no record. |
| FR-011-AC-9 | examined | A document carrying both the typed table and the `sysml` fence under one section reports `both-forms` and builds no record. |
| FR-011-AC-10 | examined | A document with three independent defects reports three errors in one pass, each naming the model, the property and the line. |
| FR-011-AC-11 | examined | Two rows sharing an id report `duplicate-row-id` naming both lines. |
| FR-011-AC-12 | examined | An escaped pipe inside a cell is carried as a literal pipe and does not split the row. |
| FR-011-AC-13 | examined | A CRLF copy of a skeleton produces the same record as its LF original. |
| FR-011-AC-14 | examined | Every frontmatter key a model does not declare is listed in that model's dropped key set. |
| FR-011-AC-15 | examined | For every key an emitted model and that type's `frontmatter_schema_ref` both describe, the two agree on type and pattern — the drift this ticket exists to end is not replaced by a new pair of drifting declarations. |
| FR-011-AC-16 | examined | The totality walk visits every schema reachable from the emitted models and terminates when a reference cycle is present. |
| TC-138 | examined | The mapping totality walk visits every reachable schema and terminates when a reference cycle is present. |
| FR-011-AC-17 | examined | Two rows sharing an id in **different** tables of one document are accepted; two in the same table are not. |
| FR-011-AC-18 | examined | Every mapping kind named in `semantic.mappings` is used by at least one model property. |
| FR-011-CON-1 | examined | '`mappings.yaml` SHALL name only sections and columns the manifest\'s `body_extraction` already declares.' |
| FR-011-CON-2 | examined | The mapping SHALL be total in both directions: no unmapped model property and no mapping entry naming an undeclared property. |

## Finding Detail

- **FND-001 — tests/test_markdown_mappings.py:127.** The assertion `walk(roots, edges) >= set(roots)` only proves the seed set survived: each root is inserted into `seen` before any edges are followed. It therefore passes even if traversal omits every child schema referenced by a shipped model. The separate two-node synthetic cycle check establishes termination on that fixture, but it does not establish full reachability over the shipped graph. Assert the actual reachable closure for the shipped graph (or otherwise assert every expected reachable schema), while retaining the explicit cyclic input.

## Bindings Checked

| Test | Criterion(s) | Review |
| --- | --- | --- |
| `test_the_totality_walk_traverses_shipped_models_and_stops_at_cycles` | FR-011-AC-16 | Tag matches; shipped-graph reachability assertion is incomplete (FND-001). |
| `test_the_mapping_is_total_in_both_directions` | FR-011-AC-2, FR-011-CON-2 | Exact property-set equality. |
| `test_three_independent_defects_are_reported_in_one_pass` | FR-011-AC-10 | Exact count, named reasons, model/property/line fields. |
| `test_duplicate_row_id_names_both_lines` | FR-011-AC-11 | Checks both source row lines and model/property. |
| `test_row_ids_are_unique_per_table_not_per_document` | FR-011-AC-17 | Accepts same ids across separate tables. |
| `test_each_negative_fails_exactly_the_check_it_names` and clause tests | FR-011-AC-8 | Marker additions correspond to negative checks exercised. |

## Related Code Checked

The changed assertions are confined to the test oracle. I checked the changed trace markers in `tests/test_mapping_failures.py`, `tests/test_markdown_mappings.py`, and `tests/test_semantic_manifest.py`; no source function implementing these criteria changed. No dependency revision moved.
