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
       scope-boundary|architecture-evaluation|gap-analysis|ears-conformance|
       code-review|spec-correctness), `scope` to the spec paths/ids reviewed,
       and `review_set` to base|all|subset.
     - REQUIRED (level 2): Summary, Findings.
     - `## Findings` MUST be a table whose headers are, in order:
       ID | Severity | Summary | Refs | Escape Cause — with >= 1 data row.
       `Escape Cause` is OPTIONAL; the other four are not. The ID column
       matches ^FND-\d+$ and Severity is one of low | medium | high.
       An analysis that found nothing still records one row, e.g.
       FND-001 | low | No issues found | -.

     ESCAPE CAUSE — which layer let the defect through. Severity says how
     urgently to look; this says who is leaking, and it is the only axis that
     does. Record it where the finding is a real defect that escaped; leave the
     column off entirely for analyses where it does not apply.
       missing-requirement                  nobody wrote it; nothing to test against
       wrong-requirement                    written, and it said the wrong thing
       correct-requirement-no-evidence      requirement right, nothing verified it
       implementation-bug-despite-evidence  requirement right, evidence real, code wrong
     The fourth is the one to watch: the only cause that does not indict the
     spec, and the only one a green Test Matrix would have called healthy. -->

## Summary

<!-- One or two sentences: what this analysis examined and what it found. -->

## Findings

| ID      | Severity | Summary                          | Refs   |
| ------- | -------- | -------------------------------- | ------ |
| FND-001 | medium   | <one-line finding>               | FR-001 |
