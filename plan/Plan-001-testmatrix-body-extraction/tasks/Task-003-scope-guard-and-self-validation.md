---
id: Task-003
title: "FR-003-AC-9 — manifest-scope guard + repo self-validation"
type: Task
status: completed
track: A
priority: P1
relationships:
  - target: ix://agent-ix/spec-artifacts-process/Task-002
    type: depends_on
  - target: ix://agent-ix/spec-artifacts-process/FR-003
    type: references
  - target: ix://agent-ix/spec-artifacts-process/TC-017
    type: verifies
---
# Task-003: FR-003-AC-9 — manifest-scope guard + repo self-validation

## Scope

Prove the contract landed without collateral change (FR-003-AC-9) and that this
repository itself conforms: TC-017 manifest-scope assertion, self-validation of
`spec/tests.md` under the new contract, and packaging check.

## Subtasks

- [x] **Manifest-scope test (TC-017).** Assert the TestMatrix frontmatter schema
      and every other archetype/artifact_type entry are unchanged relative to the
      pre-contract manifest (targeted structural diff, complements Inspection).
- [x] **Self-validation.** `quire validate --scope . "spec/**/*.md"` passes with
      the local module active — this repo's TM-001 is the first real conforming
      matrix.
- [x] **Packaging.** `make build`; confirm the manifest ships in the wheel and
      `quoin write . --types TestMatrix` still resolves skeleton + schema.

## Deliverables

- TC-017 test green; full `make test` green
- Clean `quire validate` on this repo

## Notes

- Gate "contract green" closes when this task is done — Track C remains blocked
  on the Track S sign-off regardless.

## Implementation record (2026-08-04)

- `test_testmatrix_contract_does_not_widen_the_manifest` (TC-017) pins the
  TestMatrix frontmatter schema (required keys, `const`, property set), the
  archetype's carry-over fields, and the fact that exactly `Feedback`,
  `SpecReview`, and `TestMatrix` carry a `body_extraction` — the contract is
  additive. (The first cut asserted `{SpecReview, TestMatrix}` and caught the
  pre-existing `Feedback` contract, which is the guard working.)
- `test_testmatrix_body_extraction_contract` pins the contract as manifest
  data, including the rule that no optional coverage table carries `min_rows`
  (requiring rows would force fabricated entries, FR-003-AC-7).
- `test_repo_test_matrix_self_validates` runs `quire validate` over this repo's
  own `spec/tests.md`: the module does not ship a shape it violates.
- Gate (contract green): `make test` green (33 passed, 1 skipped, 1 xfailed,
  100% coverage), `make lint` clean, and
  `quire validate --scope . "spec/**/*.md"` exits 0.
