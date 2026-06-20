---
id: SR-001
title: "Failure-domain review of the quoin spec"
type: SpecReview
analysis: failure-domain
scope: spec/spec.md
review_set: subset
---

## Summary

One review document per analysis skill. The `## Findings` table is validated
by the SpecReview archetype: exact columns, an `FND-NNN` id per row, and a
`Severity` constrained to `low`/`medium`/`high` (quire CR-010 `column_choices`).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | ix-flow spawn failure behavior is undefined | FR-021 |
| FND-002 | low | cycle termination unstated for the graph walk | FR-024 |
