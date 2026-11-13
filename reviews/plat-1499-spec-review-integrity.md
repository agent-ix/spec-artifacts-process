---
id: SR-20261113075806
title: "PLAT-1499 spec-artifacts-process PR144 spec-review integrity"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-artifacts-process PR144 @b782a70 over origin/main; spec/functional/FR-003-testmatrix-body-extraction.md, spec/functional/FR-004-traceability-declaration.md, spec/tests.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-004"
    type: references
---

## Summary

Ticket: PLAT-1499. Integrity review of consistency across FR-003, FR-004 and
spec/tests.md after the `Functional Requirement Coverage` extraction is
dropped. `quire validate --scope .` over the three changed files exits 0, with
only pre-existing grammar warnings.

Clean units:

- TC-194 is the next unused TC id, and TC-003 is reused for its new meaning
  with a 🚧 status.
- TC-003 traces FR-003-AC-13, TC-194 traces FR-003-AC-14, and TC-076 traces
  FR-003-AC-12. Each binding matches its criterion.
- The FR-004 sentence that cited the dropped table now cites the TC rows'
  `Traces To` cells. TC-148, TC-149 and TC-150 do trace FR-004-AC-20,
  FR-004-AC-21 and FR-007-AC-15.
- The edge-case row for an absent table now reads as valid.

## Verdict

**CHANGES REQUESTED.** FND-001 is a direct contradiction. FR-004-AC-2 still
requires a `functional-coverage` reference kind that reads the section FR-003
now says SHALL NOT be declared. FND-002 leaves TC-016 bound to a positive
criterion. FND-003 and FND-004 are wording-level.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-004-AC-2 still requires "exactly one entry per kind of table (`test-case`, `traces-to`, `functional-coverage`)", and TC-039 asserts the same three kinds. The `functional-coverage` document reference reads the `Test Cases` column of the `Functional Requirement Coverage` section, which FR-003 now says SHALL NOT be declared. As written, the implementation cannot satisfy both FRs: keeping the reference reads a section the contract dropped, and removing it fails FR-004-AC-2. Reword FR-004-AC-2 and TC-039 to two kinds (`test-case`, `traces-to`), and add the manifest entry removal to the implementation list. | spec/functional/FR-004-traceability-declaration.md:220 |
| FND-002 | medium | TC-016 still traces FR-003-AC-1 and FR-003-AC-2, and its title and the Constraint Boundary rows still say "required tables" (plural). FR-003-AC-1 is now a positive criterion, and its header-only-fr-coverage case will pass under the new contract. The remaining min-rows rule for the Test Case Summary (Behavior: "at least one row") has no owning criterion: AC-2 covers absence only. Add the min-rows clause to FR-003-AC-2 (or a new AC), retrace TC-016 to it, and make the TC-016 and boundary rows singular. | spec/tests.md:204 |
| FND-003 | low | FR-003-AC-13 duplicates FR-003-AC-1: both assert that a document with a conforming Test Case Summary validates. AC-13 also joins a validation outcome with a manifest-inspection claim ("the contract names no functional-coverage extraction"). Keep AC-13 as the single "no section validates" criterion and state the manifest claim as its own Inspection criterion, or fold it into AC-9. | spec/functional/FR-003-testmatrix-body-extraction.md:195 |
| FND-004 | low | The reworded FR-004 sentence begins lowercase after a full stop: "...do not themselves violate it. each binds to its TC row...". | spec/functional/FR-004-traceability-declaration.md:108 |

## Examined scope

```yaml
scope:
- id: FR-004-AC-2
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: "Every trace target and document reference is bound by `archetype` and declares no `document` path, the Test Matrix included; matrix entries additionally declare an `exclude` covering test data; and there is exactly one entry per kind of table (`test-case`, `traces-to`, `functional-coverage`), never one per matrix filename"
- id: FR-003-AC-1
  path: spec/functional/FR-003-testmatrix-body-extraction.md
  role: examined
  excerpt: "A `TestMatrix` doc with a conforming `Test Case Summary` validates"
- id: FR-003-AC-2
  path: spec/functional/FR-003-testmatrix-body-extraction.md
  role: examined
  excerpt: "A doc missing the `Test Case Summary` table fails with reason `missing`"
- id: FR-003-AC-12
  path: spec/functional/FR-003-testmatrix-body-extraction.md
  role: examined
  excerpt: "It requires no `test_cases` table, and it mints no test-case ids"
- id: FR-003-AC-13
  path: spec/functional/FR-003-testmatrix-body-extraction.md
  role: examined
  excerpt: "A `TestMatrix` doc with a `Test Case Summary` and no `Functional Requirement Coverage` section validates; the contract names no functional-coverage extraction, so no table restating the computed matrix is required or column-asserted"
- id: FR-003-AC-14
  path: spec/functional/FR-003-testmatrix-body-extraction.md
  role: examined
  excerpt: "The shipped `TestMatrix` skeleton emits no `Functional Requirement Coverage` section, and its authoring comment states that requirement-to-criterion coverage is read from `quire matrix`, never authored"
- id: FR-004
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: "violate it. each binds to its TC row by the TC row's own `Traces To` cell, which is a different column and is not affected."
- id: TM-001
  path: spec/tests.md
  role: examined
  excerpt: "TC-003, TC-016, TC-039, TC-076, TC-194 rows; Constraint Boundary min_rows rows; edge-case row"
bindings:
- {test_id: TC-003, ac_id: FR-003-AC-13, trace: correct}
- {test_id: TC-194, ac_id: FR-003-AC-14, trace: correct}
- {test_id: TC-076, ac_id: FR-003-AC-12, trace: correct}
- {test_id: TC-016, ac_id: FR-003-AC-1, trace: wrong}
```
