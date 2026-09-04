---
id: Task-010
title: "GATE — SpecReview end to end: model, mapping, skeleton, authored golden record, negative fixtures"
type: Task
status: done
track: Gate
priority: P0
relationships:
  - target: ix://agent-ix/spec-artifacts-process/FR-011
    type: references
  - target: ix://agent-ix/spec-artifacts-process/FR-012
    type: references
  - target: ix://agent-ix/spec-artifacts-process/TC-097
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-100
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-142
    type: verifies
---
# Task-010: GATE — SpecReview end to end

## Scope

One artifact type proven all the way through before the other eleven are attempted. `SpecReview`
is the slice: this repository authors dozens of them, its `body_extraction` is non-trivial
(a required section plus a five-column table with an optional column, an id pattern and two
closed vocabularies), and a mistake anywhere in the chain is visible immediately.

## Subtasks

- [ ] `mappings.schema.json` and the `SpecReview` entry of `mappings.yaml`, using only the declared mapping kinds.
- [ ] The reference mapping in `tests/support/`, strict: any error means no record, and every error of one document is reported in one pass.
- [ ] The `SpecReview` golden record **authored** from the skeleton and the schema, then reproduced by the reference mapping. A record recorded from the mapping's output is a snapshot of the mapping's bugs and does not pass this gate (SR-014 FND-001).
- [ ] Two negative fixtures for `SpecReview`: a missing `## Findings` table and a `Severity` outside the vocabulary, each with `expect:` and `because:`.
- [ ] `tests/conftest.py`: fail-not-skip on a missing engine, and a schema registry resolving every `$ref` locally — module models from the committed `schemas/`, grammar models from the installed `@agent-ix/semantic-core`.

## Deliverables

`mappings.schema.json`, the `SpecReview` half of `mappings.yaml`, `tests/support/`,
`examples/SpecReview.record.json`, two negative fixtures, `tests/conftest.py`.

## Gate criterion

The gate passes only when the model, the mapping entry, the skeleton, the authored golden record
and both negative fixtures agree with each other. It fails if the golden record had to be
regenerated to make the mapping pass.
