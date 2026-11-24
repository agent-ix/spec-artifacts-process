---
id: SR-20261115175473
title: "PLAT-1855 spec-artifacts-process PR163 gap-analysis"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process PR163 @b4fdfc2 over origin/main; spec/functional/FR-019-adr-segregation-verb.md, spec/tests.md TC-248 TC-249, tests/test_adr_links.py, spec_artifacts_process/manifest.yaml; against spec-objects-architecture FR-016 (origin/main)"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-019"
    type: references
---

## Summary

Ticket: PLAT-1855. Planless gap analysis over FR-019 and the upstream obligation in spec-objects-architecture FR-016. Plan completion: not assessed.

FR-016 (merged, spec-objects-architecture origin/main) Dependencies, Cross-repository: "the `ADR` archetype is declared by `spec-artifacts-process`, whose `allowed_links` for `ADR` must list `segregates_for_requirement` (targets `FR`, `NFR`)". The diff adds exactly `segregates_for_requirement: [FR, NFR]` to the `ADR` `allowed_links` and nothing else, the same form as the PLAT-1680 `realizes_requirement: [FR, NFR]` line (PR #149). FR-016 also says the requirement may author the inverse without editing the ADR (quire-rs FR-041), so not listing `requirement_segregated_by` is consistent: quire-rs FR-041-AC-2 makes any declared inverse label type-allowed at Tier-1.

`quoin matrix --json` (quoin 0.36.8) reports FR-019-AC-1..5 as `static_status: tagged`, method Test. TC-248 is tagged FR-019-AC-1..3 and TC-249 FR-019-AC-4..5. Deleting the manifest line fails both tests. The production change has an owning requirement and no untraced code was added.

Interplay with spec-objects-architecture PR #60: its FR-016-AC-12 test (`test_fr016_ac12_adr_edge_counts_and_the_advisory_follows_process`) reads the loaded spec-artifacts-process manifest and expects the advisory only while the verb is unlisted. It passed with this PR's module loaded and with the installed module, so this merge does not break it.

## Verdict

**PASS** on coverage and on the FR-016 obligation. The wrong inverse assertion (FR-019-AC-5 / TC-249) is reported in the code-review and integrity artifacts.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |
