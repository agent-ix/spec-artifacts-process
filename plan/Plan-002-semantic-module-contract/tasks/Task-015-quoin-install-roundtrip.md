---
id: Task-015
title: "IT-002 — quoin module install accepts the semantic contract, and the prior state is restored"
type: Task
status: todo
track: C
priority: P1
relationships:
  - target: ix://agent-ix/spec-artifacts-process/IT-002
    type: references
  - target: ix://agent-ix/spec-artifacts-process/FR-010
    type: references
---
# Task-015: IT-002 — quoin module install accepts the semantic contract

## Scope

The Quoin boundary, which had no contract test at all — a manifest Quire accepts and Quoin
refuses would otherwise have shipped (SR-015 FND-001).

## Subtasks

- [ ] Record `quoin module` before anything is installed.
- [ ] `quoin module install path:<checkout>/spec_artifacts_process`; assert exit 0 and no `semantic.*` error diagnostic.
- [ ] Assert the listing contains `spec-artifacts-process` sourced from the path, and that the derived package manifest names the twelve exports.
- [ ] Restore the recorded source and ref **unconditionally**, in a `finally`. This repository's installed module entry is what every other repository validates against; a failed restore leaves the whole development environment validating against an uncommitted branch.

## Deliverables

`tests/test_quoin_install_roundtrip.py`.
