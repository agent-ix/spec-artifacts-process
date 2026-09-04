---
id: Task-011
title: "FR-010 — the semantic block, reference-form data_schema, and the 0.1.0 baseline fixture"
type: Task
status: todo
track: B
priority: P0
relationships:
  - target: ix://agent-ix/spec-artifacts-process/FR-010
    type: references
  - target: ix://agent-ix/spec-artifacts-process/TC-089
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-090
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-091
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-092
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-093
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-094
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-095
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-096
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-135
    type: verifies
  - target: ix://agent-ix/spec-artifacts-process/TC-136
    type: verifies
---
# Task-011: FR-010 — the semantic block, reference-form data_schema, and the 0.1.0 baseline fixture

## Scope

The manifest half. This is the file every repository in the programme validates against, so the
baseline fixture is written **first** and the diff is what licenses each edit.

## Subtasks

- [ ] Copy the 0.1.0 manifest to `tests/fixtures/baseline-0.1.0/manifest.yaml` before touching it.
- [ ] Add the `semantic` block: the nine keys, `exports` derived from `artifact_types[].name`, `mappings` naming only kinds a property uses.
- [ ] Add reference-form `data_schema` to all twelve artifact types; run `make manifest-digests`.
- [ ] Bump `version` to `0.2.0`; leave `manifest_version` at `1.0.0`.
- [ ] Structural-diff test: every 0.1.0 declaration present unchanged apart from the twelve `data_schema` keys, the two `Standard` locators, `version` and `semantic`. This is the single normative baseline assertion; FR-013-AC-7 defers to it rather than repeating it.
- [ ] Vocabulary-identity test over `Status`, `Type`, `Priority`, `Traces To`, `Severity`, `Escape Cause`, `Evidence Kind`, `Verdict`, `analysis`, `review_set` — and specifically that `⚠️` is still rejected.
- [ ] Trace-target identity test (`trace_targets`, `document_references` byte-identical).
- [ ] TC-135 as a strict expected failure naming quire-rs#221 and quire-rs#394 — never a skip.

## Deliverables

`spec_artifacts_process/manifest.yaml` at 0.2.0, `tests/fixtures/baseline-0.1.0/manifest.yaml`,
`tests/test_semantic_manifest.py`.

## Notes

`object_types.standard` keeps its inline `data_schema`. Converting it would change how an
existing declaration resolves for every consumer that activates this module, which is exactly the
breaking change this ticket refuses to make as a side effect.
