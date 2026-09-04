---
id: Task-007
title: "Toolchain: pinned TypeSpec package, semantic-core resolution, engine wheel, LF pin"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-artifacts-process/FR-009
    type: references
---
# Task-007: Toolchain: pinned TypeSpec package, semantic-core resolution, engine wheel, LF pin

## Scope

Everything the rest of the plan assumes and no requirement owns. It has no acceptance criterion
of its own; SR-009 FND-004 records that it was an assumption and is now a task.

## Subtasks

- [ ] Create `spec_artifacts_process/semantic/package.json`: private, `type: module`, `tspMain: main.tsp`, exact `devDependencies` on `@typespec/compiler` 1.15.0 and `@typespec/json-schema` 1.15.0, exact dependency on `@agent-ix/semantic-core` 0.1.0. No `.npmrc`, no `file:`/`link:`, no upper bound.
- [ ] `npm install` in that directory and commit `package-lock.json`.
- [ ] `spec_artifacts_process/semantic/tspconfig.yaml` with the json-schema emitter, `emitAllModels`, `emitAllRefs`, `seal-object-schemas`, and a scratch `emitter-output-dir` so a bare `tsp compile` cannot drop files into the payload.
- [ ] `.gitattributes` with `* text=auto eol=lf`, so a checkout with `autocrlf` cannot change digested bytes.
- [ ] `.gitignore`: the emitter scratch directory and `node_modules`.
- [ ] Makefile targets `semantic-install`, `schemas`, `schemas-check`, `manifest-digests`, `dev-quire`, and `make lint` extended to run `schemas-check`.
- [ ] `make dev-quire` provisions the Quire wheel the semantic tests need, with the reason in a comment: `internal-pypi` carries no build with the semantic surface and `agent-ix/quire-rs#392` is the blocking issue.

## Deliverables

`spec_artifacts_process/semantic/{package.json,package-lock.json,tspconfig.yaml}`, `.gitattributes`,
Makefile targets.

## Notes

`make schemas-check` is a **local** gate wired into `make lint`, never a GitHub-workflow gate:
`@agent-ix` resolves only through the user-level npm config and a CI job asserting it would fail
for a reason that is not a defect here (FR-009 Behavior, SR-013 FND-003).
