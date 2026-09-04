---
id: FIND-001
title: "Import re-verification is not performed on read"
type: Finding
relationships:
  - target: "ix://agent-ix/example/FR-001"
    type: "found_in"
---
<!-- Finding authoring skeleton (spec-artifacts-process). Fill every section
     with substantive content. Contract:
     - Frontmatter: `type: Finding`; `id` matches ^[A-Z]{2,4}-[0-9]+$ and is
       minted `FIND-NNN`. NOT `Finding-NNN`: that old pattern produced ids the
       archetype's own frontmatter schema rejects (seven letters is not two to
       four), so every id it minted was invalid.
     - `FIND-` is deliberately NOT `FND-`. `FND-NNN` is the id namespace of the
       findings ROWS inside a SpecReview. A Finding is a DOCUMENT and a child of
       `Review`; giving the two one prefix would read as unification and be a
       conflation.
     - The archetype declares NO `body_extraction`, so no section is asserted.
       Nothing authors a Finding today — the corpus documents typed `Finding`
       are mistyped analyses — and the review skills emit SpecReview documents
       with an inline findings table. A contract here would be for a form
       nobody produces.
     - `allowed_links`: found_in | blocks | references. -->
# FIND-001: Import re-verification is not performed on read

## Summary

Artifacts are verified once, at import. Nothing re-verifies the stored bytes on
read, so corruption after persistence is not detected by this path.

## Evidence

Read at commit `a1b2c3d`: the digest comparison runs in the import handler and
has no counterpart in the read handler.

## Impact

A consumer receives bytes the system believes are intact on the strength of a
check performed once, at a different time.

## Recommendation

Either re-verify on read, or state the single-verification boundary in the
requirement so a reader is not left to infer it.
