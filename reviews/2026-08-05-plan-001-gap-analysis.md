---
id: SR-002
title: "Gap analysis — Plan-001 TestMatrix body_extraction (FR-003)"
type: SpecReview
analysis: gap-analysis
scope: "plan/Plan-001-testmatrix-body-extraction/, spec/functional/FR-003-testmatrix-body-extraction.md, spec/tests.md, spec_artifacts_process/manifest.yaml, tests/"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-artifacts-process/plan/Plan-001", type: reviews }
  - { target: "ix://agent-ix/spec-artifacts-process/spec/tests", type: references }
  - { target: "ix://agent-ix/spec-artifacts-process/spec/functional/FR-003", type: references }
---

## Summary

Post-implementation gap analysis of Plan-001 on `task/testmatrix-body-extraction`
(= PR #10 head). Steps 1–3 were run; the optional semantic review (step 4) was
**skipped** — it was not opted into.

**Plan completion.** Tasks 001–004 are `completed`. Task-005
(normalize-before-enforce sign-off) and Task-006 (publish the enforcing version)
are `not_started` and blocked by FR-003-CON-1, a gate this review cannot clear:
Task-005 is the sign-off itself, and Task-006 is strictly downstream of it.

**Matrix verification.** 31 Test Case rows. The 26 rows belonging to this slice
(TC-001..TC-018, TC-024, and the CR-016 additions) are backed by real tests in
`tests/test_testmatrix_body_extraction.py` and `tests/test_manifest.py`, each
driving the actual `quire validate --module` and asserting quire's bracketed
reason token, so a fixture cannot pass for the wrong reason. All 28 fixtures are
referenced; no fixture is orphaned and no test references a missing one. Five
rows (TC-019..TC-023) are unbacked and marked 🚧 Planned — they belong to FR-002,
not this slice (FND-002).

**Underspecified code.** The contract is declarative data in
`manifest.yaml`; there is no procedural code to under-specify. The one
consistency risk — the `Type` vocabulary existing in both the contract and the
traceability declaration — is closed by a drift guard that asserts the two
lists are equal.

## Verdict

**CONDITIONAL**, after a `high` finding raised and closed inside the review.

Two deviations from the verdict rule, both stated rather than applied silently:

1. Two tasks are incomplete, which is a FAIL by the letter. Both are parked on
   the FR-003-CON-1 sign-off — a decision, not missing work.
2. FND-006 is `high`, which is also a FAIL by the letter. It was found *by* this
   review (dispatching CI published as a side effect), cancelled before anything
   reached the registry, and fixed in `d077d3b` before the review was filed. It
   is recorded at its true severity rather than downgraded to fit the verdict.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The FR-003 suite does not run in CI (`ci.yml` is `workflow_dispatch` only and installs no `quire`), and the module-level `skipif` makes a missing CLI a silent skip rather than a failure. Measured on run 31027554861: **6 passed, 30 skipped** — a green CI run that exercised none of the contract. Locally it runs against whatever `quire` is on `PATH`; because the manifest's top-level struct does not deny unknown fields, an older CLI silently ignores the `traceability:` block while the drift guard still passes. | FR-003, tests/test_testmatrix_body_extraction.py |
| FND-002 | medium | FR-002's `SpecReview` `body_extraction` contract ships in `manifest.yaml` with no test behind it: TC-019..TC-023 are 🚧 Planned. Pre-existing rather than introduced here, but the repo is now publishing two contracts of which only one is verified. | FR-002, TC-019..TC-023 |
| FND-003 | low | Dropping kind enumeration from `Traces To` means a `TC-nnn` token there is no longer rejected syntactically — the regex engine has no lookaround, so the pattern cannot express "any kind except TC". It is caught at reference resolution during bundle validation, not single-file validation. Pinned by an executable test rather than a comment. | FR-003, tests/fixtures/testmatrix/traces-to-test-case-token.md |
| FND-004 | low | TC-024 (id uniqueness within a matrix) is a `strict=True` xfail: quire-rs exposes no id-uniqueness table assert, so the contract cannot state it. The gap is in the engine, not the contract, and the xfail names it. | FR-003-AC-11, TC-024 |
| FND-005 | low | The sweep leaves 164 of 177 ecosystem matrices failing structurally — 114 have no Test Case Summary, 109 no Functional Requirement Coverage. That is the input to the Task-005 gate, not a defect here, but it means the contract cannot be enforced without an authoring campaign across roughly 150 repos. | FR-003-CON-1, Task-005 |
| FND-006 | high | `ci.yml` hung `publish-to-pypi` off the same bare `workflow_dispatch` as the checks, so dispatching the workflow to run lint and tests published the package as a side effect — while FR-003-CON-1 holds the enforcing version behind a sign-off gate. Found by dispatching it during this review; the run was cancelled during job setup and nothing reached the registry. Fixed in `d077d3b`: publishing now needs an explicit `publish: true` input. | FR-003-CON-1, Task-006 |

## Coverage

| Check | Result |
| --- | --- |
| Tasks `completed` | 4 / 6 (2 user-gated) |
| Slice matrix rows backed by a test | 26 / 26 |
| Rows unbacked | 5 (all FR-002, marked 🚧 Planned) |
| Fixtures referenced by a test | 28 / 28 |
| Ecosystem matrices passing (read-only sweep) | 13 / 177 |
| Semantic review (step 4) | skipped — not opted into |
