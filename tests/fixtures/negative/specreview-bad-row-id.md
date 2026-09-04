---
id: SR-902
title: "negative — a findings row id outside the declared pattern"
type: SpecReview
analysis: base
review_set: subset
expect: mapping.id-pattern
because: "the findings row namespace is ^FND-\\d+$; FIND- is the Finding DOCUMENT namespace and the two are deliberately different"
---
# SR-902: negative — a findings row id outside the declared pattern

## Summary

The row below uses the document namespace for a row id.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FIND-001 | low | wrong namespace for a row | FR-001 |
