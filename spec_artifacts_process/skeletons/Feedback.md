---
id: FB-001
title: "<short summary of the feedback>"
type: Feedback
status: open
kind: comment
anchor:
  artifact: "spec/functional/FR-003-validate-spec-in-renderer.md"
  text:
    quote: "<the exact selected text>"
    prefix: "<a few characters before the selection>"
    suffix: "<a few characters after the selection>"
  block:
    requirementId: "FR-003-AC-2"
    headingPath: ["FR-003", "Acceptance Criteria"]
    blockIndex: 0
relationships:
  - target: ix://agent-ix/example/FR-003
    type: references
---
<!-- Feedback authoring skeleton (spec-artifacts-process). A transient review
     thread the cockpit writes under ~/.ix and an agent reads to refine.
     Contract (validated by `quire validate`):
     - Frontmatter: type: Feedback; id matches ^[A-Z]{2,4}-[0-9]+$ (e.g. FB-001);
       status ∈ open|addressed|resolved; kind ∈ comment|triage;
       decision ∈ Fix|Dismiss|Defer (meaningful only when kind: triage);
       anchor.artifact required.
     - Anchor resolution is text-primary, block-fallback: prefer anchor.text.quote
       (with prefix/suffix for disambiguation); if the quote is gone, fall back to
       anchor.block (requirementId / headingPath+blockIndex); if the block is gone
       too, the reader marks the thread orphaned — it never silently re-points.
     - REQUIRED body (level 2): ## Comment — the reviewer's comment, or for a triage
       decision the "how to fix" guidance.
     - OPTIONAL body (level 2): ## Resolution — what changed, or why dismissed/deferred.
     - relationships: a `references` edge to the requirement/finding this targets. -->
# [FB-001] <short summary of the feedback>

## Comment

<The reviewer's comment. For a triage decision (kind: triage) this is the
"how to fix" guidance that tells the agent exactly what to do.>

## Resolution

<Optional — filled when the thread is addressed or resolved: what changed in the
artifact, or why the finding was dismissed or deferred.>
