---
id: SR-20261115175471
title: "PLAT-1658 spec-artifacts-process PR161 gap-analysis"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process PR161 @d79b938 over origin/main; FR-018-AC-17/18 and new trace markers in tests/test_dossier_document.py"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-018"
    type: references
---

## Summary

Ticket: PLAT-1658. Planless gap analysis of the new dossier-kind behavior and its tests. Quire 0.46.0's computed matrix marks both affected acceptance criteria untagged because the new test markers cite TC-247 and TC-246, which have no rows in `spec/tests.md`; plan completion: not assessed.

## Verdict

**FAIL** — both newly exercised acceptance criteria are untagged in the computed Test Matrix.

## Coverage

Reconciliation: quire matrix (quire 0.46.0, engine 0.61.0) — no run evidence read. The full repository matrix reports 238 criteria: 149 tagged, 71 untagged, 17 method-without-symbol, and 1 retired. This review reports only untagged criteria tied to the changed tests: FR-018-AC-17 and FR-018-AC-18. Reverse-gap inspection of the changed surface found no newly introduced executable behavior outside the dossier contract and its tests. Plan completion: not assessed.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The computed matrix reports FR-018-AC-17 untagged: its test cites undeclared TC-247, so the test marker does not back the criterion. | tests/test_dossier_document.py:246-247 |
| FND-002 | high | The computed matrix reports FR-018-AC-18 untagged: its tests cite undeclared TC-246, so neither marker backs the criterion. | tests/test_dossier_document.py:176-177,229-230 |
