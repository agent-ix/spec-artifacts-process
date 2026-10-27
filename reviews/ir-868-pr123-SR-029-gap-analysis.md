---
id: SR-029
title: 'Gap analysis of IR-868 PR #123 (Opus, head 7146b86)'
type: SpecReview
analysis: gap-analysis
scope: agent-ix/spec-artifacts-process@7146b86030944e09a594e6b88687a002550a24cb; spec/functional/FR-004-traceability-declaration.md,
  spec/tests.md, spec_artifacts_process/manifest.yaml, tests/test_traceability_declaration.py
review_set: subset
---
# SR-029: Gap analysis of IR-868 PR #123 (Opus, head 7146b86)

## Summary

Ticket: IR-868, with VER-25 in the same diff. Planless gap analysis of the changed criteria FR-004-AC-2, FR-004-AC-10 and FR-004-AC-19, against TC-039, TC-066 and TC-147 and their tagged tests. The run used `quire coverage --module <PR module>` over this repository and over throwaway probes. Plan completion: not assessed.

## Verdict

**FAIL — changes requested.** Two medium findings and one low.

What is aligned:

- TC-066 matches every clause of FR-004-AC-10 with both regex-level and engine-level tests. The engine tests cover multi-id binding to a production symbol, the old doc-line form no longer crediting, `backed == 0` (scope, not evidence), and the name being absent from `markers`.
- TC-039 backs AC-2's entry-count clause and its status-lie clause.
- The TC-147 and AC-19 wording edits only follow the removal of the Rust line form.
- Repository-wide coverage with the PR module equals main: 123/269 backed, with the same three pre-existing lies (FR-007, FR-013, TC-065).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The TC-039 status-lie test is one-directional. Every coverage row in its fixture is an unbacked Complete row, so its set-equality assertion would still pass if the new reference reported every Complete row as a lie. No backed row and no Planned row is present. A probe shows the engine is correct today (a backed `StR-001` row and a Planned `NFR-002` row were not reported), but no test can catch over-reporting. | tests/test_traceability_declaration.py:259-305 |
| FND-002 | medium | TC-066 has no engine-level negative case for a well-formed attribute inside a `/* */` block comment or a multi-line raw string. Both bind as scope at this head (SR-028 FND-001). SR-023 FND-001 is only partly addressed: the regex-level negatives cover only `///` and single-line string inputs. | tests/test_traceability_declaration.py:642-677 |
| FND-003 | low | AC-2's new clause "TestMatrix body extraction recognizes the combined nonfunctional and stakeholder table's four columns" is backed only by reading the YAML declaration back. No `quire validate` fixture checks that a combined table with the right headers passes and one with wrong headers fails. This could not be run here (see Unavailable checks). | tests/test_traceability_declaration.py:223-239 |

## Examined scope

- FR-004-AC-2 (examined): "…exactly one entry per kind of table (`test-case`, `traces-to`, `functional-coverage`, `nonfunctional-stakeholder-coverage`), never one per matrix filename. TestMatrix body extraction recognizes the combined nonfunctional and stakeholder table's four columns. A complete row with no bound test in either Analyze coverage table appears in `quire coverage` as a status lie."
- FR-004-AC-10 (examined): "`trace_tags.implements` declares exactly one templated form for each of Rust, Python and TypeScript. Rust uses only `#[implements("ID1", "ID2")]`… Malformed attributes and prose naming a requirement match no Rust form. The Rust attribute mints implementation scope, not verification evidence."
- FR-004-AC-19 (examined): wording-only change, "the declared `legacy` and `implements` forms".
- TC-039, TC-066 and TC-147 rows in `spec/tests.md` (examined).

## Unavailable checks

`quire validate --module <abs module dir> <TestMatrix doc>` returns `unknown type 'TestMatrix' (no archetype registered for it)` under Quire 0.36.2 / engine 0.50.2. It does so for this repository's own `tests/fixtures/testmatrix/conforming.md`, on main's module as well, so it is pre-existing and not caused by this PR. `tests/test_testmatrix_body_extraction.py` fails 31 tests here (1 xfailed). Validating in scoped mode is ambiguous: two `spec-artifacts-process` copies are discovered, the first wins, and the installed copy is 0.2.0. So the body-extraction clause could not be checked against behaviour.

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-004 | medium | The xfailed TC-156 and TC-158 engine tests and the declaration-only TC-152 test carry their TC id in the docstring. The python-docstring-id form therefore mints a `verifies` claim for each. `quire trace --id` shows exactly one claim per TC (test_traceability_declaration.py:810, :832, :242), and `quire coverage` reports TC-152, TC-156 and TC-158 as `backed: True`. Those three rows are honestly 🚧 Blocked today, but flipping any of them to ✅ without a fix would raise no status lie: the guard is disabled for exactly the criteria known to fail. A test that xfails, or that checks only a declaration, should not mint evidence for the blocked TC. | tests/test_traceability_declaration.py:810-845 |

## Dispositions

Fix head `8d9b1283bfaca5a9688261d476ce62b7df406eb1`, reviewed against `7146b86`. Round 1.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | - |
| FND-002 | fixed | - |
| FND-003 | still-open | AC-23 and TC-152 now state the accept/reject/absent behaviour and are honestly marked 🚧 Blocked. The only test is still the declaration-shape read-back (test_combined_table_extraction_declaration), and no follow-up ticket is cited for the `quire validate` unknown-TestMatrix path. The behavioural check is still missing. |

Round 2: fix head `f5e2f8f749d35b3d9a06deeae4b26af071a9d324`, checked against round-1 head `8d9b1283`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-003 | still-open | AC-23 and TC-152 are honestly 🚧 Blocked, but the combined-table accept/reject behaviour is still unverified: the only test reads back the declaration shape. `quire validate --module` still returns unknown type 'TestMatrix' under Quire 0.36.2. This is an external blocker, not fixed. |
| FND-004 | fixed | - |

Round 3: fix head `1aec2181409a626bbcd426b1de244b169317bd1a`, checked against round-2 reviewed head `8c215724100e328d044646e9d53ecb75074b8f9c`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-003 | still-open | Quire 0.36.2 still rejects the pre-existing conforming TestMatrix fixture with unknown type 'TestMatrix' under the candidate module. TC-152 reads the declaration shape only; there is no passing engine accept/reject check for FR-004-AC-23. This remains an external validator blocker. |
