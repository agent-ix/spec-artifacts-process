---
id: SR-20261115175472
title: "PLAT-1855 spec-artifacts-process PR163 code-review"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR163 @b4fdfc2 over origin/main; spec_artifacts_process/manifest.yaml, tests/test_adr_links.py, tests/fixtures/adr/adr-segregates_for_requirement.md, tests/fixtures/adr/adr-requirement_segregated_by.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-019"
    type: references
---

## Summary

Ticket: PLAT-1855. Code review of the one-line manifest change that adds `segregates_for_requirement: [FR, NFR]` to the `ADR` `allowed_links`, its two tests and two fixtures. The line copies the PLAT-1680 `realizes_requirement: [FR, NFR]` entry and matches spec-objects-architecture FR-016 Dependencies (verb, targets `FR`, `NFR`, `ADR` only, inverse not listed). The ADR skeleton comment and golden record are unchanged.

Measured with quire 0.52.0 (engine 0.62.2), sibling modules taken from origin/main of spec-artifacts-iso and spec-objects-architecture into a scratch modules dir, and again with spec-objects-architecture PR #60 head beff9a8:

- Architecture origin/main (verb undeclared): TC-248 and TC-249 pass. Every load of this module prints `UnknownEdgeType: archetype 'ADR' allowed_links uses 'segregates_for_requirement' which is not in any edge_types registry` (exit 0).
- Architecture PR #60 (verb declared with inverse `requirement_segregated_by`): TC-248 passes; TC-249 fails, because the ADR fixture that authors `requirement_segregated_by` draws no `disallowed-edge-type` (FND-001).
- Mutation: deleting the manifest line makes both new tests fail under either architecture state, so the forward assertions can fail.

Pre-existing failures (outside this diff): `test_adr_realizing_a_part_draws_the_advisory_finding_naming_the_ids`, `test_adr_realizing_a_missing_id_fails_strict_with_a_located_error` and `test_relations_report_the_adr_as_realizing_fr_and_nfr` fail on untouched origin/main. They fail the same way with fresh origin/main sibling modules, with the installed `~/.ix` copies, and with the pinned quire-cli 0.46.0, so stale installed modules are not the cause. `quire relations` reports no `required_relations` unless spec-objects-security is also loaded (the `SIBLINGS` tuple loads only iso and architecture), and under `--strict` the part-target `disallowed-edge-target` line is now an error-format line, not `warning:`.

## Verdict

**CHANGES REQUESTED.** The manifest line is correct. The inverse half of TC-249 asserts a finding that exists only while the verb is undeclared, and it goes red once spec-objects-architecture PR #60 is loaded (FND-001). Merge after PR #60 (FND-002).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | `test_adr_authoring_the_segregation_verb_draws_no_disallowed_edge_type` asserts `disallowed-edge-type` for an ADR authoring `requirement_segregated_by`. Under quire-rs FR-041 Tier-1 any declared inverse label is type-allowed on every archetype, so once spec-objects-architecture declares the verb (PR #60) the finding disappears and the test fails (measured with PR #60 head beff9a8). It passes today only because the verb is undeclared. The FR-017 precedent asserts the inverse only at manifest level (FR-017-AC-2). Fix: drop the inverse validate assertion and the `adr-requirement_segregated_by.md` fixture, with FR-019-AC-5. | tests/test_adr_links.py:157-160, tests/fixtures/adr/adr-requirement_segregated_by.md |
| FND-002 | low | Until spec-objects-architecture declares `segregates_for_requirement`, every quire run that loads this module with architecture origin/main prints an `UnknownEdgeType` registry diagnostic (exit 0). Merge after spec-objects-architecture PR #60. | spec_artifacts_process/manifest.yaml:80 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | f1e2472 removes the inverse assertion and `tests/fixtures/adr/adr-requirement_segregated_by.md`; the test is now tagged `FR-019-AC-4`, `TC-249` only. `tests/test_adr_links.py` passes 11/11 with origin/main iso, security and architecture modules and with architecture PR #60 head beff9a8 (quire 0.52.0). Deleting the `segregates_for_requirement` line still fails TC-248 and TC-249 under PR #60. |
| FND-002 | fixed | The PR #163 body now states "Merge order: merge AFTER spec-objects-architecture #60" and explains the `UnknownEdgeType` advisory. |
