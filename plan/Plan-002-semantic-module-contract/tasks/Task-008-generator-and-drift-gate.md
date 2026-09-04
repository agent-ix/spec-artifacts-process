---
id: Task-008
title: "FR-009 — the projection generator, its preconditions and the drift gate"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-artifacts-process/FR-009
    type: references
  - target: ix://agent-ix/spec-artifacts-process/TC-081
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-083
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-084
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-085
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-087
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-088
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-132
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-133
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-134
    type: verifies
---
# Task-008: FR-009 — the projection generator, its preconditions and the drift gate

## Scope

The enablement half of FR-009: everything that turns a TypeSpec source into shipped schema bytes,
and everything that refuses a tree where the two disagree. The models are Task-009; this task
works against a source that compiles.

## Subtasks

- [ ] `spec_artifacts_process/semantic/main.tsp` shell: namespace `AgentIx.SpecArtifactsProcess`, `@jsonSchema` base `https://schemas.agent-ix.org/agent-ix/spec-artifacts-process/<manifest version>/`, importing `@agent-ix/semantic-core`.
- [ ] `spec_artifacts_process/semantic/scripts/generate.mjs`, Node built-ins only: compile into a tmpdir, refuse any emitter entry that is not a top-level `*.json`, keep the files whose `$id` starts with the module base, record the discarded semantic-core files, rewrite any relative `$id`, render two-space JSON with a trailing newline.
- [ ] Preconditions with real diagnostics: missing `node_modules`, missing `tsp`, a Node older than 20 — each exits non-zero naming the missing component and `make semantic-install`, never failing inside the compiler (FR-009-AC-10).
- [ ] Version agreement: `@jsonSchema` base vs manifest `version` (AC-5); resolved `@agent-ix/semantic-core` vs `semantic.semantic_core` (AC-11); a stale version segment that is internally consistent (AC-12).
- [ ] `generated/toolchain.json`: compiler, emitter, semantic-core version **and** the SHA-256 of that package's own `generated/toolchain.json`, base, manifest version, excluded imports, file list, normalization record, digest.
- [ ] `--check` mode: writes nothing anywhere; reports differing, stale and missing files by path; leaves every `*-frontmatter.schema.json` alone.
- [ ] `scripts/manifest_digests.py`: rewrite `data_schema.digest` values textually so comments and formatting survive; touch no other byte.

## Deliverables

`semantic/main.tsp` (shell), `semantic/scripts/generate.mjs`, `semantic/generated/toolchain.json`,
`scripts/manifest_digests.py`.

## Notes

Determinism (CON-3) is a two-run byte comparison, but the real mitigation is the exact toolchain
pin; the test must not be read as licence to relax it (SR-014 FND-005).
