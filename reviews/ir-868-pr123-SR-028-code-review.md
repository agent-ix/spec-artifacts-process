---
id: SR-028
title: 'Code review of IR-868 PR #123 (Opus, head 7146b86)'
type: SpecReview
analysis: code-review
scope: agent-ix/spec-artifacts-process@7146b86030944e09a594e6b88687a002550a24cb; spec_artifacts_process/manifest.yaml,
  tests/test_traceability_declaration.py, spec/functional/FR-004-traceability-declaration.md, spec/tests.md
review_set: subset
---
# SR-028: Code review of IR-868 PR #123 (Opus, head 7146b86)

## Summary

Ticket: IR-868 (the diff also carries the VER-25 combined Analyze coverage reference). Reviewed `git diff origin/main...HEAD` (origin/main `34a4531`, head `7146b86`) with installed Quire 0.36.2 / engine 0.50.2 and Quoin 0.29.1. No `.rs` file is in the diff, so the rust-review lane does not apply. The Rust surface reviewed is the manifest's regex for `ix-trace-rs`'s `#[implements]` attribute.

## Verdict

**FAIL — changes requested.** Three medium findings.

What is right:

- The per-id grammar in `rust-implements-attribute` is exactly `ix-trace-rs`'s `is_id_shaped` (origin/main `e29cc07`). A differential check of 200,013 strings (13 seeds plus 200,000 random) found 0 disagreements.
- Rustfmt-style multi-line argument lists, trailing commas, structs, `impl` methods, stacked attributes and CRLF files all bind through the real engine.
- `///`-prefixed examples and single-line string literals no longer bind. This fixes most of SR-022 FND-001.
- The old Rust `rust-implements-line` form is fully removed. No reference to it remains, and an engine test proves a `/// Implements:` line no longer credits.
- `nonfunctional-stakeholder-coverage` reports status lies correctly in both directions. A backed row and a Planned row are not lies; an unbacked Complete row and a `-` Complete row are.
- Repository coverage is unchanged from main: 123/269 backed, with the same 3 pre-existing lies.
- 29/29 focused tests pass. `ruff` and `black` pass on the changed test file, and `git diff --check` is clean.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | A well-formed `#[implements("…")]` example at the start of a line inside a `/* … */` block comment or a multi-line raw string still binds as production implementation scope. Quire 0.36.2 with this head's manifest credited FR-001-AC-1 (block comment) and FR-001-AC-2 (raw string) to `block_comment_example` and `raw_string_example`. The new line anchors fixed only the `///` and single-line string cases from SR-022 FND-001. Neither the spec nor a test records the remaining case. | spec_artifacts_process/manifest.yaml:1278-1281 |
| FND-002 | medium | The trailing anchor `\)\][ \t]*$` rejects valid attributes that `ix-trace-rs` accepts. `#[implements("FR-001-AC-1")] // why` and `#[implements("FR-001-AC-2")] pub fn f() {}` silently bind nothing. The sibling `rust-trace-attribute` marker is unanchored and binds both. FR-004 states the form is "as accepted by `ix-trace-rs`", and that crate's own doc says being stricter than the declared grammar is the same drift as being looser. | spec_artifacts_process/manifest.yaml:1278-1281 |
| FND-003 | medium | Removing `rust-implements-line` silently drops implementation scope for current consumers. Local checkouts hold about 70 Rust files in 11 repos (quire-rs 14, quire-contract-codegen 21, quire-contract-runtime 14, tl-rewrite 7, quire-contract-ir 7, …) still using `// Implements:` or `/// Implements:`; under module 0.2.2 they bind nothing. The PR description still describes the attribute as added "alongside the existing `Implements:` comment form" and asks the owner to accept that additive design, which no longer matches the diff. The removal needs a recorded owner decision and tracked consumer migration before release. This is not a request for a fallback form. | spec_artifacts_process/manifest.yaml:1276-1282 |

## Examined scope

- `spec_artifacts_process/manifest.yaml` `trace_tags.implements` (`rust-implements-attribute`, `python-implements-line`, `typescript-implements-line`). Examined.
- `spec_artifacts_process/manifest.yaml` `document_references` `nonfunctional-stakeholder-coverage` and TestMatrix `body_extraction` `nonfunctional_stakeholder_coverage`. Examined.
- `spec_artifacts_process/manifest.yaml` `version: 0.2.2`. Examined.
- `tests/test_traceability_declaration.py` tests `test_matrix_entries_are_not_enumerated_per_filename`, `test_analyze_matrix_false_complete_is_a_status_lie`, `test_implements_forms_match_language_syntax`, `test_rust_implements_attribute_declares_scope` and `test_quire_credits_ix_trace_implements_attribute_on_production`. Examined.
- `ix-trace-rs` `src/lib.rs` (`validate`, `is_id_shaped`) at origin/main `e29cc07`. Context only.

## Reproduction

Fixtures and scripts are under `/home/peter/dev/qualification-logs/ir868-pr123-opus-review/`:

- `probes/rust/` covers FND-002: trailing comment, same line, multi-line, path-qualified, struct, method, stacked and CRLF.
- `probes/falsepos/` covers FND-001: block comment, raw string, doc example and a real attribute.
- `scripts/id_shape_diff.py` is the grammar differential.

The probes ran as `quire coverage --scope <probe> --module <PR module dir> --json`.

## Dispositions

Fix head `8d9b1283bfaca5a9688261d476ce62b7df406eb1`, reviewed against `7146b86`. Round 1.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | still-open | The manifest is unchanged in 8d9b128, so the `^[ \t]*#\[implements\(` regex still matches line-start attribute text inside block comments and multi-line raw strings. TC-156 now measures this and xfails, which documents the defect but does not fix it. The fix is upstream-blocked on syntax-aware quire-rs binding, and no follow-up ticket id is cited. |
| FND-002 | still-open | The manifest is unchanged, so the trailing `\)\][ \t]*$` anchor still drops valid attributes. This is not an engine limitation. Probe (probes/trailing, probes/anchor-relaxed-module): with this head's manifest, Quire 0.36.2 binds nothing from `#[implements("FR-001-AC-1")] // why` and `#[implements("FR-001-AC-2")] pub fn same_line() {}`. With a scratch copy whose only change drops the trailing `[ \t]*$` anchor, the SAME engine binds both, still rejects the `///` example, and every TC-154 positive and TC-159 negative still holds. A manifest-only fix exists. The fix round mislabels it as blocked on quire-rs; see SR-030 FND-003. |
| FND-003 | still-open | The stale half is fixed: the PR body now says the attribute is the sole Rust form and that 0.2.2 must not be released until Peter decides the migration. The owner decision and tracked consumer migration are still outstanding, with no ticket id cited. The body names only quire-contract-codegen, quire-contract-runtime and tl-rewrite. The 7146b86 measurement also found quire-rs (14 files), quire-contract-ir (7) and others. |

Round 2: fix head `f5e2f8f749d35b3d9a06deeae4b26af071a9d324`, checked against round-1 head `8d9b1283`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | still-open | Real attribute text inside block comments and multi-line raw strings still binds as production scope at f5e2f8f7: probes/falsepos credits block_comment_example and raw_string_example, and TC-156 still xfails. Removing the end anchor also widens this class. Two shapes that bound nothing at 8d9b128 now bind (probes/widening): a block comment closing `*/` on the attribute's own line, and a raw string with text after the attribute. Both are the same comment/raw-string defect. Fixing it is upstream-blocked on syntax-aware quire-rs binding; no fix has landed. |
| FND-002 | fixed | - |
| FND-003 | still-open | There is still no owner migration decision and no tracked consumer migration; release and install remain held. A re-measure at this pass found 72 Rust files in 11 local repos still using `// Implements:` or `/// Implements:` (quire-contract-codegen 21, quire-rs 14, quire-contract-runtime 14, quire-contract-ir 7, tl-rewrite 7, tl-mltl 4, and one each in five more). The PR body names only quire-contract-codegen, quire-contract-runtime and tl-rewrite. |

Round 3: fix head `1aec2181409a626bbcd426b1de244b169317bd1a`, checked against round-2 reviewed head `8c215724100e328d044646e9d53ecb75074b8f9c`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | still-open | Quire 0.36.2 still credits line-shaped attribute text inside a Rust block comment and a multi-line raw string. The unchanged attribute regex scans text; the focused engine negative case xfails. PLAT-1181 tracks syntax-aware binding, but FR-004-AC-27/TC-156 remain unmet on this head. |
| FND-003 | fixed | The exact rust-implements-line name, language, pattern and template from main 34a4531 are restored in the manifest. The engine integration test credits comment_only via rust-implements-line alongside handle_input via rust-implements-attribute. FR-004-AC-10, TC-066 and the PR body describe both forms. |
