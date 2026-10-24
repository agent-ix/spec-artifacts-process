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
