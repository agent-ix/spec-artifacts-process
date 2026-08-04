---
id: Task-006
title: "Publish the enforcing module version (post-sign-off)"
type: Task
status: not_started
track: C
priority: P0
relationships:
  - target: ix://agent-ix/spec-artifacts-process/Task-005
    type: depends_on
  - target: ix://agent-ix/spec-artifacts-process/FR-003
    type: references
  - target: ix://agent-ix/spec-artifacts-process/FR-001
    type: references
  - target: ix://agent-ix/spec-artifacts-process/IT-001
    type: verifies
---
# Task-006: Publish the enforcing module version (post-sign-off)

## Scope

Release choreography after the FR-003-CON-1 gate: signed-off normalizations are
applied (as the user directed at Task-005), then the module version carrying the
enforcing `body_extraction` is bumped and published, and activation is
re-verified (IT-001 path).

## Subtasks

- [ ] **Apply normalizations.** Land the approved per-repo `tests.md` diffs (per
      the sign-off scope; per-repo PRs or direct pushes as the user directed).
- [ ] **Version bump.** Bump the module package version; update changelog/log.
- [ ] **Publish.** Release per repo convention (`make local-publish` for the
      local registry; stable channel only if the user requests it).
- [ ] **Re-verify activation.** IT-001 manifest-activation roundtrip against the
      published version; module consumers (`~/.ix/filament/modules`) refreshed.

## Deliverables

- Published enforcing module version; activation roundtrip green
- Normalized ecosystem `tests.md` files (per sign-off scope)

## Notes

- Publishing before Task-005 closes violates FR-003-CON-1 — hard stop.
- Stable/public release channels remain user-gated per standing convention.
