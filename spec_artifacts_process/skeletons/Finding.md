---
id: FND-001
title: "<what escaped, in one line>"
type: Finding
relationships:
  - target: "ix://<org>/<repo>/spec/functional/FR-000"
    type: "found_in"
---
<!-- Finding authoring skeleton (spec-artifacts-process). One Finding per
     confirmed defect that escaped — to a later phase, to review, or to the
     field. Contract (manifest body_extraction asserts, validated by
     `quire validate`):
     - Frontmatter: `type: Finding`; `id` matches ^[A-Z]{2,4}-[0-9]+$ and is
       minted `FND-{next:03d}`. `relationships` link the finding to what it was
       found in (`found_in`), what it blocks (`blocks`), or related artifacts
       (`references`).
     - REQUIRED (level 2): Summary, Classification.
     - `## Classification` MUST be a table with headers EXACTLY:
       Escape Cause | Detected In | Traces — with >= 1 data row.
       `Escape Cause` is one of:
         missing-requirement
         wrong-requirement
         correct-requirement-no-evidence
         implementation-bug-despite-evidence

     WHY THE CAUSE MATTERS. Severity (on a SpecReview) says how urgently to
     look. Escape cause says WHICH LAYER LEAKED, and it is the only axis that
     does. A distribution over enough Findings answers a question no coverage
     number can: is the specification the weak link, is the evidence, or is the
     implementation? The fourth cause is the one to watch — a defect that
     shipped with a correct requirement AND real evidence behind it is the only
     one that does not indict the spec, and the only one a green matrix would
     have called healthy. -->

## Summary

<!-- What escaped, and how it was noticed. Enough for a reader to recognise the
     same shape elsewhere without opening the linked artifacts. -->

## Classification

| Escape Cause | Detected In | Traces |
| ------------ | ----------- | ------ |
| missing-requirement | code-review | FR-000-AC-1 |

<!-- Escape Cause: pick the layer that leaked, not the one easiest to fix.
       missing-requirement                  nobody wrote it
       wrong-requirement                    it was written and said the wrong thing
       correct-requirement-no-evidence      right requirement, nothing verified it
       implementation-bug-despite-evidence  right requirement, real evidence, wrong code

     Detected In: the phase or activity that caught it — review, gap-analysis,
     integration, staging, production. Where it was *caught*, not where it was
     introduced; the cause column carries that.

     Traces: the requirement / acceptance-criterion ids this concerns, or `-`
     when the cause is missing-requirement and there is nothing to point at.
     That absence is itself the finding. -->
