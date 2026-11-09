---
id: SR-16442
title: "PLAT-847 process PR131 code-review"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR131 @a7b0683 over origin/main e1af989; spec_artifacts_process/manifest.yaml, tests/test_traceability_declaration.py"
review_set: subset
---

## Summary

Ticket: PLAT-847. Code review of the manifest deletion and the Python test
edits.

The manifest change removes exactly the `trace_tags.legacy` list (134 lines,
manifest.yaml:1088-1221 on main) and nothing else. The `markers` (3 forms) and
`implements` forms are byte-identical to main. The four deleted tests
(TC-031/035/071/075) read only `trace_tags["legacy"]`. The remaining edit to
`test_implements_is_a_separate_list_from_markers` drops the legacy names from
the union and still checks the marker/implements separation that the test
exists for. No remaining test reads `legacy`, `rewrite_to` or `id_format` under
`trace_tags`. Ruff and black pass on the changed test file.

Engine evidence: the quire-rs PR #627 head (6f257a9) was built as a library
with a scratch loader, debug=0 and jobs 4, then removed. Loading main's module
dir fails with `traceability.trace_tags: unknown field `legacy`, expected
`markers` or `implements``. Loading the PR head's module dir succeeds with a
traceability model and zero load failures. The quire CLI itself could not be
built against #627, because quire-cli main does not compile against quire-rs
0.54 (`binding_census.self_named` and the `trace_search` result type changed),
so `quire coverage` was not run with the new engine. Focused pytest over
test_traceability_declaration/test_manifest/test_semantic_manifest gives
42 passed and 9 failed at head, against 46 passed and the same 9 failed on
main. Those 9 are the known installed-engine (0.36.2) load failures
(`unknown field `syntax``) and are not findings.

## Verdict

**PASS with one low finding.**

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The `implements` block comment still explains the `Implements:` keyword by contrast with "the legacy `*-comment-id` forms [that] bind a bare id after `//`, which is why they need a trailing-delimiter rule". Those forms are gone. The PR rewrote the same comparison out of FR-004's prose but left it in the manifest comment. Reduce it to "the `Implements:` prefix is the prose guard: a sentence naming a requirement matches nothing." | spec_artifacts_process/manifest.yaml:1118-1121 |

## Examined scope

```yaml
scope:
- id: spec_artifacts_process/manifest.yaml#trace_tags
  path: spec_artifacts_process/manifest.yaml
  role: examined
  excerpt: "trace_tags: markers (rust-trace-attribute, pytest-trace-marker, ts-trace-helper) and implements (rust-implements-line, rust-implements-attribute, python/typescript implements lines); legacy list removed"
- id: tests/test_traceability_declaration.py::test_implements_is_a_separate_list_from_markers
  path: tests/test_traceability_declaration.py
  role: examined
  excerpt: "marker_names = {m[\"name\"] for m in tags[\"markers\"]}; implements_names = {f[\"name\"] for f in tags[\"implements\"]}; assert not marker_names & implements_names"
- id: tests/test_traceability_declaration.py (removed TC-031/035/071/075)
  path: tests/test_traceability_declaration.py
  role: examined
  excerpt: "test_legacy_forms_rewrite_within_their_own_language, test_legacy_forms_capture_every_id_the_line_names, test_test_name_form_binds_both_spellings_of_its_token, test_doc_comment_forms_require_a_trailing_delimiter: all read traceability['trace_tags']['legacy'] only"
```

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1 (head 42249eb): manifest.yaml:1118-1120 now reads "For line-comment forms, the `Implements:` prefix is the prose guard: a sentence naming a requirement matches nothing. Comma lists are accepted because authors already write them that way." No legacy reference remains in the manifest. |
