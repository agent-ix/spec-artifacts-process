---
id: RV-001
title: "Review of the artifact import path"
type: Review
relationships:
  - target: "ix://agent-ix/example/FR-001"
    type: "reviews"
---
<!-- Review authoring skeleton (spec-artifacts-process). Fill every section
     with substantive content. Contract:
     - Frontmatter: `type: Review`; `id` matches ^[A-Z]{2,4}-[0-9]+$.
     - The archetype declares NO `body_extraction`, so no section is asserted.
     - `allowed_links`: reviews | references.
     - `composition.expected_artifacts` is `Finding`: a Review is the parent of
       `Finding` DOCUMENTS, whose ids are minted `FIND-NNN`.
     - Do NOT confuse a `Finding` document with a `FND-NNN` row inside a
       `SpecReview`. They are different things with deliberately different id
       namespaces; the analysis skills emit SpecReview documents with an inline
       findings table, and nothing authors a Finding document today.
     - For a per-analysis, machine-validated review, use `SpecReview` instead —
       that is the archetype whose findings table is asserted. -->
# RV-001: Review of the artifact import path

## Scope

The import path from receipt to persistence, read at commit `a1b2c3d`.

## Summary

The import path verifies the declared digest before persisting and names both
digests on mismatch. Two observations are recorded below; neither blocks.

## Observations

- The rejection message names the declared and computed digests, which is what
  makes a failed import diagnosable rather than merely reported.
- Re-verification on read is not performed. That is a deliberate scope
  boundary rather than an omission, and it is recorded here so the next reader
  does not raise it again.
