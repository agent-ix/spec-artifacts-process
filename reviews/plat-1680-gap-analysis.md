---
id: SR-20261113084041
title: "PLAT-1680 spec-artifacts-process PR149 gap-analysis"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process PR149 @14cf518 over origin/main; spec/functional/FR-017-adr-design-realization-verb.md, spec/tests.md TC-217, tests/test_adr_links.py, spec_artifacts_process/manifest.yaml"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-017"
    type: references
---

## Summary

Ticket: PLAT-1680. Planless gap analysis over FR-017. Plan completion: not assessed. `quoin matrix --json` reports FR-017-AC-1 as `static_status: tagged` (method Test), with no run evidence bound. `tests/test_adr_links.py::test_adr_may_author_realizes_requirement_but_not_unlisted_verbs` carries `trace("FR-017-AC-1", "TC-217")`. It asserts the manifest list directly, then drives `quire validate` over the three fixtures. The production change is exactly one manifest line, and no code lacks an owning requirement.

## Verdict

**PASS** on coverage, apart from one untested behaviour clause (FND-001).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | FR-017 Behavior says the existing `ADR` verbs SHALL stay listed, but no AC states this and no test asserts it. A later edit that drops `supersedes` or `depends_on` passes the suite. Fix: add the clause to FR-017-AC-1 (or a new AC) and assert that the four existing verbs are a subset of the ADR `allowed_links` in the test. | spec/functional/FR-017-adr-design-realization-verb.md:34, tests/test_adr_links.py:33-44 |
