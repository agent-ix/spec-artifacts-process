---
id: SR-20261102086810
title: "Integrity review of PLAT-866 structural Python and TypeScript implements forms"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-artifacts-process PR133 @c50b1ee over origin/main; spec/functional/FR-004-traceability-declaration.md, spec/tests.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-004"
    type: references
---

## Summary

Ticket: PLAT-866. Structural and consistency review of the Test Matrix and the
FR-004 edits in PR #133. `quire validate --scope . spec/tests.md
spec/functional/FR-004-traceability-declaration.md` passes with no errors.
Its EARS warnings are on lines 61, 122 and 174, which this diff does not
touch. The validator does not catch the misplaced rows below.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The five new Test Case Summary rows, TC-160..TC-164 (`Test ID \| Title \| Type \| Priority \| Traces To \| Status`, six cells each), sit inside the `### Functional Requirement Coverage` table, between the FR-004 and FR-005 coverage rows. They are not under `## Test Case Summary`. The `test-case` trace target reads only `section: Test Case Summary` with `id_column: Test ID`, so TC-160..TC-164 are never minted as test-case ids. The coverage rows at lines 73-77 then cite five undefined TC ids. In the coverage table each misplaced row has six cells against a four-column header, so its `Test Cases` cell reads `Unit` or `Integration`. Move the five rows to the Test Case Summary after TC-159 (line 294). | spec/tests.md:68-72; spec/tests.md:73-77; spec/tests.md:294; spec_artifacts_process/manifest.yaml:807-811 |
| FND-002 | low | The PR reverses the decision recorded in FR-004's IR-868 note, which says the module adds the Rust attribute "while retaining ... the Python and TypeScript line-comment forms". It adds no note recording the reversal. FR-004 records every earlier reversal (CR-062, CR-064, IR-868, CR-PLAT-1236). Without a note, the history in the file contradicts the requirement above it. Add a short PLAT-866 note citing quire-rs FR-062's structural syntax positions. | spec/functional/FR-004-traceability-declaration.md:375-381; spec/functional/FR-004-traceability-declaration.md:152-163 |

## Verdict

**FAIL.** FND-001 orphans every new TC id. Moving five rows fixes it.

## Examined scope

```yaml
scope:
- {id: TC-160, path: spec/tests.md, role: examined}
- {id: TC-161, path: spec/tests.md, role: examined}
- {id: TC-162, path: spec/tests.md, role: examined}
- {id: TC-163, path: spec/tests.md, role: examined}
- {id: TC-164, path: spec/tests.md, role: examined}
- {id: FR-004-AC-31, path: spec/functional/FR-004-traceability-declaration.md, role: context_only}
- {id: FR-004, path: spec/functional/FR-004-traceability-declaration.md, role: examined}
```

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | TC-160..TC-166 appear exactly once each, under `## Test Case Summary` after TC-159 (spec/tests.md:292-298). Every Functional Requirement Coverage `FR` row has four cells. The coverage rows at lines 68-74 cite only registered ids. |
| FND-002 | fixed | A PLAT-866 note follows the IR-868 note and records the reversal for Python and TypeScript. |
| FND-003 | fixed | The note now reads "PLAT-866 (target design)". The replacement bullet says the manifest still declares the comment forms until the replacement change. |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | low | The new PLAT-866 note says Python and TypeScript production scope "is structural only" as "current design". But the Removal bullet keeps `python-implements-line` and `typescript-implements-line` declared until the consumer condition holds, and AC-10 and AC-26 describe them as current. Call it the target design and say that the comment forms remain until the removal condition. | spec/functional/FR-004-traceability-declaration.md:407-409 |
