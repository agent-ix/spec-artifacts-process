---
id: SR-001
title: "<analysis> review of <scope>"
type: SpecReview
analysis: failure-domain
scope: "spec/spec.md"
review_set: subset
---
<!-- SpecReview authoring skeleton (spec-artifacts-process). One SpecReview
     document per analysis skill (parallel-safe). Fill every section with
     substantive content. Contract (manifest body_extraction asserts,
     validated by `quire validate`):
     - Frontmatter: `type: SpecReview`; `id` matches ^[A-Z]{2,4}-[0-9]+$
       (e.g. SR-001); set `analysis` to this doc's analysis
       (base|failure-domain|integrity|dependency|evidence|risk-complexity|
       scope-boundary|gap-analysis), `scope` to the spec paths/ids reviewed, and
       `review_set` to base|all|subset.
     - REQUIRED (level 2): Summary, Findings.
     - `## Findings` MUST be a table with headers EXACTLY:
       ID | Severity | Summary | Refs — with >= 1 data row. The ID column
       matches ^FND-\d+$ and Severity is one of low | medium | high.
       An analysis that found nothing still records one row, e.g.
       FND-001 | low | No issues found | -. -->

## Summary

<!-- One or two sentences: what this analysis examined and what it found. -->

## Findings

| ID      | Severity | Summary                          | Refs   |
| ------- | -------- | -------------------------------- | ------ |
| FND-001 | medium   | <one-line finding>               | FR-001 |
