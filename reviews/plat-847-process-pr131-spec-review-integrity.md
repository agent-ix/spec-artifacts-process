---
id: SR-16444
title: "PLAT-847 process PR131 spec-review integrity"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-artifacts-process PR131 @a7b0683 over origin/main e1af989; spec/functional/FR-004-traceability-declaration.md, spec/tests.md"
review_set: subset
---

## Summary

Ticket: PLAT-847. Integrity review of the spec half of the `trace_tags.legacy`
removal: FR-004 loses AC-4/8/11/15 and the `legacy` SHALL bullet, and
`spec/tests.md` loses the matching audit-table and TC-031/035/071/075 rows.

The removals themselves are consistent. All four ACs test only the removed
machinery: AC-4 is `rewrite_to` language pairing, AC-8 is the legacy
comma-list and `id_format` single-id shape, AC-11 is the `rust-test-name-id`
separator, and AC-15 is the doc-comment trailing delimiter. No other AC or TC
row cites them, and the audit table and the TC table agree with each other and
with FR-004's Acceptance Criteria table. Interface-id binding through the
canonical markers and `implements` forms stays covered elsewhere (the
`implements` scope test at tests/test_traceability_declaration.py:428 and the
Traces To pattern test at :710). The edited `Implements:` prose bullet still
states the prose guard without the legacy comparison. `quire validate` over
both files exits 0 with the same five pre-existing grammar warnings before and
after.

Two live references to the removed forms survive, though. One is a live AC
(medium), and the other is historical notes that cite deleted ids as if they
were current (low).

## Verdict

**CONDITIONAL.** Fix FND-001 (strike `legacy` from FR-004-AC-19 and TC-147).
FND-002 is low. The EARS sub-analysis was not run separately: the only edited
requirement statement lost a clause and gained no words, and the grammar
warnings count is unchanged (5 before, 5 after).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-004-AC-19 still requires `interface_NNN-AC-N` to resolve through "the declared `legacy` and `implements` forms", and TC-147's row repeats it. The module no longer declares any `legacy` form, so the live AC names machinery that no longer exists. Drop "`legacy` and" from both. | spec/functional/FR-004-traceability-declaration.md:194; spec/tests.md:274 |
| FND-002 | low | Historical notes in FR-004 still describe the deleted forms in the present tense and cite deleted ids. The CR-034 note ends "FR-004-AC-11, TC-071." The CR-024 note says "`rust-test-name-id` is not list-widened" and "The delimiter still holds". The interface note lists "the `legacy`/`implements` comment, docstring ... forms admit it too". Either delete these legacy paragraphs or give each a one-line note saying CR-215/PLAT-847 removed the forms, so no reader takes AC-11/TC-071 as live. | spec/functional/FR-004-traceability-declaration.md:278-303, :439-468, :526-530 |

## Examined scope

```yaml
scope:
- id: FR-004-AC-19
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: "The `interface-acceptance-criterion` target declares `required: false`, so a corpus with no `interface` documents or an `interface` document without an Acceptance Criteria section is healthy; and an `interface_NNN-AC-N` id resolves everywhere an `FR`/`NFR` acceptance-criterion id already does — `inspection-obligation`, `traces-to`, the `Traces To` column check, the declared `legacy` and `implements` forms, and a new `interface-verification` reference covering its own `Verification` column."
- id: FR-004-AC-3
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: "`trace_tags.markers` declares exactly one marker for each of rust, python and typescript, and each declares a `template`"
- id: FR-004-AC-10
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: "`trace_tags.implements` declares exactly the existing templated Rust `Implements:` line-comment form plus the new templated Rust `#[implements(...)]` attribute form, and exactly one templated `Implements:` line-comment form each for Python and TypeScript."
- id: FR-004-AC-4
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: "(removed) Every `legacy` form declares a `language`, and its `rewrite_to` names a marker of that same language"
- id: FR-004-AC-8
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: "(removed) Every `legacy` form without an `id_format` declares its id as a comma-separated list, so a match carries every id the line names; a form declaring `id_format` declares a single id; and the `*-comment-id` delimiter still rejects prose flowing through an id."
- id: FR-004-AC-11
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: "(removed) `rust-test-name-id` binds both spellings of its token — `fn tc744_x` and `fn tc_744_x` render the same `TC-744` — while the separator stays optional, adds no capture group, and admits nothing new"
- id: FR-004-AC-15
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: "(removed) Every doc-comment form (`rust-doc-comment-id`, `python-docstring-id`, `typescript-doc-comment-id`) requires a trailing delimiter after the id list, so a sentence beginning with an id is not read as a tag"
- id: FR-004
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: "The Rust, Python and TypeScript line-comment `implements` forms **SHALL** require the literal keyword `Implements:` before a comma-separated id list. The keyword is the prose guard: a sentence that merely names a requirement matches nothing."
- id: TM-001
  path: spec/tests.md
  role: examined
  excerpt: "Functional Requirement Coverage rows FR-004-AC-1..AC-21 and Test Case Summary rows TC-028..TC-076, TC-147"
```

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1 (head 42249eb): FR-004-AC-19 and the TC-147 row now read "the declared `implements` forms", with no `legacy`. The audit table row FR-004-AC-19 / TC-147 is unchanged and consistent. |
| FND-002 | fixed | Round 1 (head 42249eb): the CR-034 and CR-024 notes are deleted, the interface note's bullet is reduced to the `implements` forms, and the dangling "(CR-024)" citation in the implements note is dropped. A grep of spec/, the manifest, tests/ and README finds no reference to AC-4/8/11/15, TC-031/035/071/075, CR-024/034 or a removed form. `quire validate` exits 0 with the same 5 warnings. |
