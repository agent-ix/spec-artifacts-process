---
id: SR-2026112016223475846355025
title: "Code review of PLAT-1448 + PLAT-1636"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process; spec/functional/FR-024..FR-027.md, spec/non-functional/NFR-002.md, spec_artifacts_process/{manifest,mappings,semantic,schema,example,skeleton}, tests/test_feature_risk_rating.py"
review_set: subset
---

## Summary

The Python tests follow the repo class/docstring/trace conventions and use real JSON Schema validators, but the schemas do not enforce all cross-record and per-feature constraints claimed by FR-025. The ID patterns also accept undersized identifiers.

## Verdict

CONDITIONAL

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The ID schemas use `^FRR-[0-9]+$` and `^IU-[0-9]+$`, so values such as `FRR-1` and `IU-1` pass despite the authored three-digit contract. | FR-025 |
| FND-002 | medium | `intended_use` is only a non-empty string and assessment-row `requirement` is text; neither is checked against an IntendedUse or the rating’s target FRs, so invalid references and incomplete per-target coverage validate. | FR-025-AC-1, FR-025-AC-3 |
| FND-003 | medium | The only FR-026 test asserts manifest YAML. No test runs validation to assert missing/duplicate diagnostics, JSON statuses, default-off behavior, or that the tree remains unchanged. | FR-026-AC-7, FR-026-AC-1, FR-026-AC-4, FR-026-AC-8 |
