---
id: NFR-001
title: "Anomaly validation reports every coexisting defect in one pass, located"
type: NFR
quality_attribute: usability
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-014"
    type: "constrains"
  - target: "ix://agent-ix/spec-artifacts-process/FR-015"
    type: "constrains"
---
# NFR-001: Anomaly validation reports every coexisting defect in one pass, located

## Statement

When an `Anomaly` document has several defects that can coexist, validation SHALL report every one
of them in a single run, and each defect that is present in the text SHALL carry the document line
of the offending field, row or section heading.

## Scope

- Applies to: the checks of FR-014 and FR-015 on one document.
- A defect that is an absence (a missing section, a missing field) has no line of its own. Its
  diagnostic carries the line of the frontmatter `status` field, which is what makes the absence a
  defect.

## Rationale

An author fixing one defect per run, with no line to look at, will paper over a record rather than
repair it. Defects that exclude each other (no assessment section and a bad row in that section)
cannot be reported together, so the measure is taken over fixtures that group only coexisting ones.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| Fraction of injected defects reported in one run, over three fixtures: (a) `closed` with no `closed_by` and no `resolution`; (b) `assessed` with `safety_impact: unassessed` and no assessment section; (c) `impacting` with a dangling `Requirement` row, a kind-mismatched `Hazard` row and an empty `Rationale` | 100% | 100% | Test |
| Fraction of reported defects carrying a line (the `status` line for an absence) | 100% | 100% | Test |

## Verification

Each of the three fixtures is validated once; the test asserts one diagnostic per injected defect
and that each carries a line.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-001-AC-1 | Validating fixture (a), (b) or (c) yields exactly one diagnostic per injected defect in that fixture. | Test |
| NFR-001-AC-2 | Every diagnostic from those runs carries a line; for an absence the line is that of the `status` field. | Test |
