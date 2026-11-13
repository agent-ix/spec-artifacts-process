---
id: SR-20261113075807
title: "PLAT-1499 spec-artifacts-process PR144 spec-review ears-conformance"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-artifacts-process PR144 @b782a70 over origin/main; spec/functional/FR-003-testmatrix-body-extraction.md Behavior bullet, spec/functional/FR-004-traceability-declaration.md reworded sentence"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-003"
    type: references
---

## Summary

Ticket: PLAT-1499. EARS conformance of the one new normative statement, the
FR-003 Behavior bullet "`body_extraction` SHALL NOT declare a `Functional
Requirement Coverage` extraction". It is a ubiquitous unwanted-behaviour
prohibition with a named subject (`body_extraction`), the same form as its
sibling bullets. `quire validate` raises no grammar diagnostic on it. The FR-004
edit changes no SHALL.

## Verdict

**PASS with one low finding.** The statement conforms. Its rationale clause
belongs in the PLAT-1499 note, not in the normative statement.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The new SHALL NOT bullet carries its justification inline ("The requirement-to-criterion-to-test coverage ... is computed by `quire matrix` ..., so the computed matrix is the single source and a second, authored copy can only drift from it"). The PLAT-1499 note under the criteria already says this. Keep the bullet to the prohibition and leave the reasoning in the note. | spec/functional/FR-003-testmatrix-body-extraction.md:36-41 |

## Examined scope

```yaml
scope:
- id: FR-003
  path: spec/functional/FR-003-testmatrix-body-extraction.md
  role: examined
  excerpt: "`body_extraction` **SHALL NOT** declare a `Functional Requirement Coverage` extraction, required or optional. The requirement-to-criterion-to-test coverage a hand-kept `Functional Req | Acceptance Criteria | Test Cases | Status` table restates is computed by `quire matrix` from the criteria and the tests' trace tags, so the computed matrix is the single source and a second, authored copy can only drift from it (PLAT-1499)."
- id: FR-004
  path: spec/functional/FR-004-traceability-declaration.md
  role: context_only
  excerpt: "each binds to its TC row by the TC row's own `Traces To` cell, which is a different column and is not affected."
```
