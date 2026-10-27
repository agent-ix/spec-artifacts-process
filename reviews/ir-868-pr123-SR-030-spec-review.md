---
id: SR-030
title: 'Spec review of IR-868 PR #123 (Opus, head 7146b86)'
type: SpecReview
analysis: base
scope: agent-ix/spec-artifacts-process@7146b86030944e09a594e6b88687a002550a24cb; spec/functional/FR-004-traceability-declaration.md,
  spec/tests.md
review_set: subset
---
# SR-030: Spec review of IR-868 PR #123 (Opus, head 7146b86)

## Summary

Ticket: IR-868, with VER-25 in the same diff. Reviewed the FR-004 statement bullet for `trace_tags.implements`; FR-004-AC-2, AC-10 and AC-19; the CR-028 and CR-063 rationale notes; Known Limits; and the TC-039, TC-066 and TC-147 rows. Both changed documents pass `quire validate --scope .`, with advisory grammar warnings only.

## Verdict

**FAIL — changes requested.** One medium finding and one low.

The FR, AC and TC wording agrees with the manifest on the form set: Rust attribute only, Python and TypeScript line comments. It also keeps the scope-versus-evidence split. TC-039 and TC-066 restate their ACs faithfully.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-004-AC-10 rules out only "malformed attributes and prose". It is silent on the two observable edges. A well-formed attribute inside a block comment or raw string binds as scope. A valid attribute followed by a trailing `//` comment, or by the item on the same line, binds nothing. Known Limits records neither, so a conforming test cannot tell intended behaviour from a defect. This continues SR-024 FND-001. | spec/functional/FR-004-traceability-declaration.md:174 |
| FND-002 | low | The dated CR-028 note (2026-08-19) and the CR-063 note were rewritten in place to describe the new Rust attribute decision. The original "a comment form, not an attribute" rationale is gone, and no new dated CR note records the reversal or the VER-25 addition to AC-2. That breaks the file's own convention, where a reversal gets its own note (for example "CR-062 note: FR-004-AC-2 reverses"). | spec/functional/FR-004-traceability-declaration.md:342-346 |

## Examined scope

- FR-004 statement bullet, lines 143-151 (examined): "`trace_tags.implements` **SHALL** declare a Rust `#[implements(...)]` attribute form and one line-comment form for each of Python and TypeScript … the Rust attribute form **SHALL** capture one or more separately quoted ids, separated by commas, as accepted by `ix-trace-rs`."
- FR-004-AC-2, FR-004-AC-10 and FR-004-AC-19 (examined).
- The CR-028 and CR-063 notes and Known Limits (examined).
- TC-039, TC-066 and TC-147 (examined).

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | medium | Known Limits, the AC-29 and TC-158 matrix status ("🚧 Blocked: syntax-aware quire-rs binding"), the TC-158 xfail reason and the PR body all blame Quire 0.36.2 for missing a valid attribute followed by a trailing comment or a same-line item. The cause is this module's own trailing `[ \t]*$` anchor. Removing only that anchor makes the same engine bind both forms, with every existing positive and negative unchanged. This misroutes a defect the PR can fix itself to an upstream owner, and records a false blocker in the spec. | spec/functional/FR-004-traceability-declaration.md:553-557 |

## Dispositions

Fix head `8d9b1283bfaca5a9688261d476ce62b7df406eb1`, reviewed against `7146b86`. Round 1.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | - |
| FND-002 | fixed | - |

Round 2: fix head `f5e2f8f749d35b3d9a06deeae4b26af071a9d324`, checked against round-1 head `8d9b1283`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-003 | fixed | - |
