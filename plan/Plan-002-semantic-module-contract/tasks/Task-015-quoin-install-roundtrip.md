---
id: Task-015
title: "IT-002 — quoin module install accepts the semantic contract, and the prior state is restored"
type: Task
status: done
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

## Outcome (2026-09-04)

Done, and it found what it was written to find. Quoin refuses the manifest:
`semantic.export-without-schema` on every export, because its FR-070 validator resolves
`semantic.exports` against `object_types` only and this module's schemas are referenced from
`artifact_types`. The already-merged `spec-artifacts-iso` is refused the same way with
`semantic.unknown-export`, so this is an upstream gap rather than a defect in either module —
`agent-ix/quoin#347`.

The test is a **strict expected failure**, not a skip: the boundary runs on every opted-in
invocation and the row turns green when Quoin resolves an artifact-type export. Step 5 was
verified on the run — the operator's module store was byte-identical to a copy taken beforehand.
