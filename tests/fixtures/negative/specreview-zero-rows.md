---
id: SR-901
title: "negative — a Findings table with a header and no data row"
type: SpecReview
analysis: base
review_set: subset
expect: mapping.min-rows
because: "`min_rows: 1`; a header-only table is not an empty finding set, it is an unfinished document"
---
# SR-901: negative — a Findings table with a header and no data row

## Summary

The table below has its header and nothing under it.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
