---
id: SR-019
title: "Integrity analysis of PLAT-1079 — FR-004, FR-007, tests.md"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-artifacts-process@96080f274c171c3bbab17b6379c67b681611cd98; spec/functional/FR-004-traceability-declaration.md, spec/functional/FR-007-verification-method-catalog.md, spec/functional/FR-010-semantic-manifest-contract.md, spec/tests.md, spec/log.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-007"
    type: "reviews"
  - target: "ix://agent-ix/spec-artifacts-process/FR-010"
    type: "references"
---
# SR-019: Integrity analysis of PLAT-1079 — FR-004, FR-007, tests.md

## Summary

Ticket: PLAT-1079. This is the structural lens over the PR diff: whether each new
criterion is actually minted, matrix consistency, and cross-FR consistency. The
checks used `quire coverage --scope . --json` (`minted_targets`, `obligations`)
and `quire validate --okf --scope .` (exit 0) at 96080f2, compared against
`origin/main` a723c22.

The FR-004 changes are well formed. FR-004-AC-20 and FR-004-AC-21 are minted,
and TC-148/TC-149 resolve to them. The matrix rows (tests.md:63-64, :90,
:312-314) use the right shape. The log entry matches the diff.

## Verdict

**NOT READY.** FND-001 means FR-007-AC-15 is not a criterion at all, so the only
AC that governs the new obligation source is invisible to the computed matrix
this epic builds.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-007-AC-15 is appended to a headerless table that sits directly after a blockquote (FR-007:255-258). That table is not in `## Acceptance Criteria` (FR-007:186-200), and the extractor does not read it. Measured: `quire coverage --json` has no FR-007-AC-15 in `minted_targets` or `obligations`, and `quire validate` gains exactly one warning over main, `'FR-007-AC-15' (row 'TC-150') … resolves to no … target`. The same defect already orphans FR-007-AC-9/10/11 on main (dangling from TC-056/057/065). Move all four rows into the AC table. | spec/functional/FR-007-verification-method-catalog.md:255-258; spec/tests.md:90, :314 |
| FND-002 | medium | FR-010-AC-3 / TC-091 is a structural diff against the 0.1.0 baseline that enumerates every allowed change. The PR adds three manifest changes that list does not name: a new `constraint` trace target, emptied (or otherwise changed) `verification`/`nfr-verification` targets, and a new `constraint` obligation source. It also implies widened `traces-to`/`inspection-obligation` targets (SR-018 FND-004). FR-010-AC-3 is not updated, so the implementation stage fails TC-091, or FR-010 goes stale. | spec/functional/FR-010-semantic-manifest-contract.md:105; spec/tests.md:259 |
| FND-003 | low | Obligation-source counts disagree within FR-007. The prose says PLAT-1079 "adds a sixth" source (FR-007:72), while the CR-006 note calls it "a fourth row shape" (FR-007:268) and says user stories are "not added as a fourth obligation source" (FR-007:270). The manifest has five sources today, so constraint is the sixth. | spec/functional/FR-007-verification-method-catalog.md:72, :268, :270 |
