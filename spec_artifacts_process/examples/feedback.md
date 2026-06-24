---
id: FB-001
title: "Bound the project root the main process may open"
type: Feedback
status: open
kind: triage
decision: Fix
anchor:
  artifact: "spec/functional/FR-001-open-project-enumerate-artifacts.md"
  text:
    quote: "the system SHALL enumerate the Quoin artifacts beneath it"
    prefix: "When the user selects a local project root, "
    suffix: " — spec artifacts"
  block:
    requirementId: "FR-001"
    headingPath: ["FR-001", "Description"]
    blockIndex: 0
relationships:
  - target: ix://agent-ix/filament-ide/FR-001
    type: references
---
# [FB-001] Bound the project root the main process may open

## Comment

Add a constraint that the main process rejects a project root that resolves —
after symlink expansion — outside an allowed base directory, closing the
path-traversal gap raised in the scope-boundary review. The enumeration itself is
fine; the missing piece is bounding which roots may be opened in the first place.

## Resolution

Pending — to be filled when the FR is updated with the bounding constraint.
