---
id: SR-914
title: "Gap analysis — RoleSpec and Rubric archetypes (PR 165)"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process PR165 head 0f6579d; spec/functional/FR-020..FR-023, spec/usecase/US-004, tests/test_role_spec.py, tests/fixtures/roles/**, spec_artifacts_process/manifest.yaml, spec_artifacts_process/mappings.yaml, spec_artifacts_process/schemas/**, spec_artifacts_process/semantic/main.tsp, spec_artifacts_process/skeletons/RoleSpec.md, spec_artifacts_process/skeletons/Rubric.md"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-artifacts-process/FR-020", type: references }
  - { target: "ix://agent-ix/spec-artifacts-process/FR-021", type: references }
  - { target: "ix://agent-ix/spec-artifacts-process/FR-022", type: references }
  - { target: "ix://agent-ix/spec-artifacts-process/FR-023", type: references }
  - { target: "ix://agent-ix/spec-artifacts-process/US-004", type: references }
---

# SR-914: Gap analysis — RoleSpec and Rubric archetypes (PR 165)

## Summary

Ticket: SWM-245. This is a planless gap analysis of PR 165 at head 0f6579d against FR-020 to FR-023 and US-004. It used `quire matrix --scope . --format json` over the repository (quire-cli 0.52.1), and checked tagged tests against what they assert.

Results:

- Of 33 criteria, 23 are tagged.
- Five are untagged because they are blocked on the engine (SWM-247, SWM-248).
- One is untagged because it is a dev-team demonstration.
- Four are inspection rows (`method-without-symbol`).
- One tagged criterion (FR-020-AC-12) does not hold as written.
- One inspection criterion (FR-020-AC-9) fails on inspection.

No reverse gaps or stubs were found. The changed Python (`tests/support/reference_mapping.py`, `{field}` interpolation in the oracle) and `projection.mjs` both have owning requirements, FR-011 and FR-009/FR-014.

## Verdict

**FAIL**: untagged criteria and two high findings. The five engine-blocked criteria are deferred by design under FR-021-AC-9, and their disposition should be `deferred` to SWM-247 or SWM-248.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-020-AC-12 is tagged by two tests, but its "any other relationship verb fails" clause does not hold: the fixture exits 0 with a `disallowed-edge-type` warning. | tests/test_role_spec.py:247 |
| FND-002 | high | FR-020-AC-9 (Inspection) fails. The vocabularies are declared in the manifest `column_choices` (evidence source twice), in the TypeSpec enums and their projected schemas, and in `RoleSpecFields.json`. | spec_artifacts_process/manifest.yaml:729, spec_artifacts_process/manifest.yaml:775 |
| FND-003 | medium | FR-021-AC-2 (a rule no evaluation names is reported with no criterion) is untagged. It is blocked on SWM-247 capability 1, rule-parented criteria. | spec/functional/FR-021-rolespec-trace-and-cross-row-checks.md |
| FND-004 | medium | FR-021-AC-5 (unused-metric warning) is untagged. It is blocked on SWM-247 capability 2, the orphan check. | spec/functional/FR-021-rolespec-trace-and-cross-row-checks.md |
| FND-005 | medium | FR-021-AC-6 (a metric query distinct from evaluation queries) is untagged. It is blocked on SWM-248 capability 3, the cross-table assert. | spec/functional/FR-021-rolespec-trace-and-cross-row-checks.md |
| FND-006 | medium | FR-021-AC-7 (duplicate row ids fail) is untagged. It is blocked on SWM-248 capability 4, the uniqueness assert. | spec/functional/FR-021-rolespec-trace-and-cross-row-checks.md |
| FND-007 | medium | FR-021-AC-11 (all-judgement rule warning) is untagged. It is blocked on SWM-247 capability 1. | spec/functional/FR-021-rolespec-trace-and-cross-row-checks.md |
| FND-008 | medium | FR-020-AC-10 is tagged, but its "negative counterpart for each failing case" is incomplete. The missing fixtures are listed in SR-913 FND-005. | tests/test_role_spec.py:128 |
| FND-009 | low | FR-022-AC-1 is untagged. It is a Demonstration that runs in dev-team after the minder spec moves, and no test is expected here. | spec/functional/FR-022-rolespec-lint-ownership.md |

## Coverage

- Criteria in scope: 33. Tagged: 23. Untagged: 6 (FR-021-AC-2, 5, 6, 7, 11 and FR-022-AC-1). Inspection or `method-without-symbol`: 4 (FR-020-AC-9, FR-021-AC-9, FR-022-AC-2, FR-022-AC-3).
- FR-021-AC-9 passes on inspection. There is no substitute parser, and SWM-247 and SWM-248 are linked from FR-021.
- FR-022-AC-2 passes on inspection. No code compares against a base revision or reads skill frontmatter.
- FR-022-AC-3 passes on inspection. The RoleSpec skeleton names Quoin and `version`.
- Reverse gaps: none. Stubs: none.
- Semantic review: skipped as a separate pass. The intent checks that matter are in SR-913.
- Plan completion: not assessed

## Dispositions

Disposition pass 1 was checked against fix head cc809ce.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | FR-020-AC-12 was amended by lead decision to the `--strict` form. Two tests pin exit 3 on the bad verb and exit 0 on the valid fixtures. |
| FND-002 | deferred | FR-020-AC-9 still fails on inspection. The in-manifest copies are gone, and the TypeSpec single-home capability is tracked on SWM-248. |
| FND-003 | deferred | FR-021-AC-2 waits on SWM-247 capability 1, and the PR body lists it as deferred. |
| FND-004 | deferred | FR-021-AC-5 waits on SWM-247 capability 2. |
| FND-005 | deferred | FR-021-AC-6 waits on SWM-248 capability 3. |
| FND-006 | deferred | FR-021-AC-7 waits on SWM-248 capability 4. |
| FND-007 | deferred | FR-021-AC-11 waits on SWM-247 capability 1. |
| FND-008 | fixed | 28 new and 4 revised negative fixtures. Each fails for its intended reason (verified by running every one). |
| FND-009 | deferred | FR-022-AC-1 is a Demonstration that runs in dev-team after the minder spec moves to spec/roles/. |
