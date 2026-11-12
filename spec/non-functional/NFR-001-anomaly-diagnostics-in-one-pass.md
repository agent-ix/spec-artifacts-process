---
id: NFR-001
title: "Anomaly validation reports every defect in one pass, located"
type: NFR
quality_attribute: usability
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-014"
    type: "constrains"
  - target: "ix://agent-ix/spec-artifacts-process/FR-015"
    type: "constrains"
---
# NFR-001: Anomaly validation reports every defect in one pass, located

## Statement

When an `Anomaly` document has several lifecycle or assessment defects, validation SHALL report
every defect in a single run, each with the document line of the offending row or section.

## Scope

- Applies to: the checks of FR-014 and FR-015 on one document.

## Rationale

An author fixing one defect per run, with no line to look at, will paper over a lifecycle record
rather than repair it.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| Fraction of injected defects reported in one run, over a fixture with one defect of each kind in FR-014-AC-4 to AC-8 and FR-015-AC-3 to AC-8 | 100% | 100% | Test |
| Fraction of reported defects carrying a document line | 100% | 100% | Test |

## Verification

A single fixture combining one defect of each kind is validated once; the test asserts one
diagnostic per injected defect and that each names a line.
