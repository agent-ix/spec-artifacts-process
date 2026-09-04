---
id: Task-001
title: "FR-001 — compute and compare the artifact digest on import"
type: Task
status: todo
track: A
priority: P0
relationships:
  - target: "ix://agent-ix/example/FR-001"
    type: "references"
  - target: "ix://agent-ix/example/TC-001"
    type: "verifies"
---
<!-- Task authoring skeleton (spec-artifacts-process). Fill every section with
     substantive content. Contract:
     - Frontmatter: `type: Task`; `id` matches ^[A-Za-z]{2,4}-[0-9]+$.
     - `track` is an OPTIONAL free string with minLength 1 (FR-005). It is a
       property of a Task, not a node: a consumer that needs a tree node
       synthesizes one from this value. There is no `Track` archetype.
     - The archetype declares NO `body_extraction`, so no section is asserted.
     - `allowed_links`: depends_on | verifies | references. Author `verifies`
       edges to the TC rows this task discharges — that is what makes a plan
       traceable to the matrix.
     - A Task is an authored DEFINITION. `status` is the authored lifecycle
       word, not a record of an execution: no run id, no duration, no
       outcome (FR-013). -->
# Task-001: FR-001 — compute and compare the artifact digest on import

## Scope

The digest half of FR-001: computing the SHA-256 of the imported bytes and
comparing it with the declared digest. The rejection path is Task-002; this task
must leave a comparison result the next task can act on.

## Subtasks

- [ ] Compute the SHA-256 of the artifact bytes as read, before any transform.
- [ ] Compare it with the declared digest from the import manifest.
- [ ] Surface the pair (declared, computed) on mismatch, so the rejection can name both.

## Deliverables

The digest computation and its unit tests.

## Notes

The digest is taken over the bytes as read. Computing it after a transform would
verify the transform rather than the transfer, which is the opposite of what the
requirement asks.
