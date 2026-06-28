---
id: TRK-001
title: "<track name>"
type: Track
relationships:
  - target: "ix://agent-ix/<repo>/Task-001"
    type: contains
---
<!-- Track authoring skeleton (spec-artifacts-process). A Track is a first-class
     node that sits BETWEEN a Plan and its Tasks, grouping related Tasks into a
     parallelizable workstream. It lets a four-level hierarchy
     (Spec -> Plan -> Track -> Task) map onto external trackers (e.g. Jira's
     Initiative -> Epic -> Story -> Sub-task).

     Contract (validated by `quire validate`):
     - Frontmatter: `type: Track`; `id` matches ^[A-Za-z]{2,4}-[0-9]+$
       (e.g. TRK-001).
     - A Track `contains` its member Tasks (mirroring how a Plan `contains`
       its members); the parent Plan declares the Plan -> Track edge from its
       own side. Each `relationships[].target` is an `ix://` URI.

     Backward compatibility: the legacy `track:` string field on a Task
     (e.g. `track: C`) remains valid. A Track node is the nodal form of that
     grouping; migrate by creating one Track per distinct legacy `track:` value
     and linking the corresponding Tasks via `contains`. -->

## Summary

<!-- One or two sentences: what workstream this Track groups and why its Tasks
     belong together. -->

## Tasks

<!-- List the member Tasks of this Track (each also declared via a `contains`
     relationship in frontmatter). -->
