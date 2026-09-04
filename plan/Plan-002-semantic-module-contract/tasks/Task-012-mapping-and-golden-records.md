---
id: Task-012
title: "FR-011 — the mapping for the remaining eleven types and their golden records"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-artifacts-process/FR-011
    type: references
  - target: ix://agent-ix/spec-artifacts-process/TC-098
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-099
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-101
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-102
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-103
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-104
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-105
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-106
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-107
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-108
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-109
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-110
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-137
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-138
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-139
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-140
    type: verifies
---
# Task-012: FR-011 — the mapping for the remaining eleven types and their golden records

## Scope

Everything Gate 1 proved, applied to the other eleven types, plus the cell-level parses and the
failure modes.

## Subtasks

- [ ] Mapping entries for the eleven remaining models; totality checked in both directions with a cycle-safe walk.
- [ ] The `Status` marker/note split and the `Traces To` parse — both shorthands expanded, a parenthesised remainder carried as `note`, a lone `-` mapped to `noTrace: true`.
- [ ] Optional-column omission yields a row without the key, never a synthesised value.
- [ ] The `ocl-clause` failure modes: prose yields an empty list; orphan fence, second fence, unterminated fence and duplicate `clauseId` each report their named error and build no record. `sourceSpan` is omitted, because semantic-core `SourceLocus` requires a `sourceIdentity` this surface does not supply.
- [ ] `both-forms` on a document carrying both the typed table and the `sysml` fence.
- [ ] Escaped-pipe cells, CRLF normalisation with the digest over the normalised bytes, per-table row-id uniqueness, one-pass multi-error reporting.
- [ ] Frontmatter drop sets per model, and the note that `expect:`/`because:` survive only because the frontmatter schemas admit additional properties.
- [ ] TC-137: every key an emitted model and its frontmatter schema both describe agrees on type and pattern.
- [ ] The run-record concepts this module does not model, with Engineering Assurance and quoin named as owners.

## Deliverables

`spec_artifacts_process/mappings.yaml` complete, `examples/<Type>.record.json` for all twelve
types, `tests/test_markdown_mappings.py`, `tests/test_mapping_failures.py`.
