---
id: SR-967175026302197768900474181941935084897
title: "EARS review — PLAT-1915 FR-012 Standard form wording PR 176"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-artifacts-process; spec/functional/FR-012-executable-skeletons.md; PR 176 @e03d14a097e50bdf0cfc9a2c9d083280257f3cc6"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-012"
    type: references
---
# SR-967175026302197768900474181941935084897: EARS review — PLAT-1915 FR-012 Standard form wording PR 176

## Summary

Reviewed FR-012's requirement statements after the Standard properties wording correction. The changed Behavior statement is concrete and correctly distinguishes the typed table from the alternate `sysml` declaration; the engine reported no EARS warnings in FR-012.

## Verdict

**PASS** — no EARS grammar or semantic defects were found in the changed requirement statement.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |

## Engine evidence

- Command: `quire validate --scope . 'spec/**/*.md' --summary`
- Exit status: 0.
- The output contains no `[ears:...]` warnings in FR-012. Warnings in unchanged FR-004, FR-020 and FR-024 were outside this analysis scope.

## Reviewed statements

- FR-012 Description: "The module SHALL ship one authoring skeleton per declared artifact type, each of which is a document its own archetype validates and whose mapped record validates against its emitted schema, together with a negative counterpart fixture for each rejection the type's contract states, so that a skeleton is an executable fixture rather than an example nothing checks."
- FR-012 Behavior, changed statement: "Exactly one skeleton — `Standard.md` — SHALL carry a `## Properties` typed table, and no other skeleton SHALL carry that table. `Standard.sysml.md` carries the alternate `sysml` declaration in its own `## Properties` section. The reason is that a Standard declares the properties a conforming artifact carries and the invariants conformance requires, and the other eleven types declare process content rather than a typed structure. Introducing a `## Properties` section on a type whose documents do not carry one would be a new required form for every consuming repository."
- FR-012-AC-10: "Exactly one skeleton carries a typed table under `## Properties`, and it is `Standard.md`; `Standard.sysml.md` carries the alternate declaration as a `sysml` fence."
