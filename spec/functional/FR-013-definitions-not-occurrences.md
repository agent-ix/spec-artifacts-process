---
id: FR-013
title: "Authored process definitions are separated from execution occurrences"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-002"
    type: "implements"
  - target: "ix://agent-ix/spec-artifacts-process/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/engineering-assurance/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/engineering-assurance/FR-008"
    type: "depends_on"
---
# FR-013: Authored process definitions are separated from execution occurrences

## Description

Every model this module emits SHALL describe an authored process definition or an authored
evidence act, and SHALL NOT carry a property that records the outcome of a verification run, so
that a Plan or Task definition can never be reused as an execution record and a reader can tell
from the schema alone which concept a document owns.

## Inputs

- The emitted models of [FR-009](./FR-009-emitted-json-schemas.md).
- The evidence-layer split this module already declares in FR-006: the authored half is
  `SuiteRegistry` and `Inspections`; the machine-transcribed half — `bindings.json`,
  `baseline.json`, `runs/**` — is typeless and corpus-invisible, and its schemas are owned by
  Engineering Assurance and quoin.
- The `verification_catalog` of FR-007, which names methods rather than runs.

## Outputs

- A `definition` / `evidence-act` role recorded per exported model in `mappings.yaml`, and a
  documented list of the run-record concepts this module deliberately does not model.

## Behavior

- `Plan`, `Task`, `ADR`, `Review`, `SpecReview`, `Finding`, `Feedback`, `TestMatrixIndex`,
  `TestMatrix` and `Standard` SHALL carry the role `definition`.
- `SuiteRegistry` and `Inspections` SHALL carry the role `evidence-act`: each records that a human
  or a named command was declared as the source of evidence, not what a particular run produced.
- No emitted model SHALL declare a property naming a run identifier, a run timestamp, a duration, a
  pass/fail count, a log location, or an artefact produced by a run.
- The `TestMatrix` model SHALL carry a row's `Status` marker as the authored coverage claim it is,
  never as an execution result; whether the claim is true is decided by the coverage rollup
  against the evidence store, outside this module.
- The `Inspections` model SHALL carry a row's `Commit` and `Verdict` as the authored record of an
  inspection act — who performed it, against which commit, with what verdict — because that record
  *is* the evidence for a method that produces no source symbol rather than a transcription of a
  machine run.
- A `SuiteRegistry` row SHALL declare a suite's identity, command, tool and evidence kind.
- A `SuiteRegistry` row SHALL declare nothing about any particular execution of that suite.
- Where a definition needs to refer to an occurrence, the reference SHALL be a `SemanticId` or an
  authored id token, never an embedded run record.
- The module SHALL record, in `mappings.yaml`, that run records, binding records, baselines and
  freshness are owned by Engineering Assurance and quoin, so an absent property reads as "owned
  elsewhere" rather than "not yet written".
- `Finding` SHALL remain a document type distinct from the `FND-` rows inside a `SpecReview`,
  because the document is a child of `Review` while the rows are a `SpecReview` property.
- The module SHALL keep the two id namespaces distinct, `FIND-` for the document and `FND-` for
  the row.
- The `SpecReview` model SHALL carry its findings rows with their `refs` and optional
  `escapeCause`, so a finding stays queryable from the review that raised it and grounded in the
  artifacts it names.
- The `TestMatrix` and `TestMatrixIndex` models SHALL carry the trace tokens of each row as an
  ordered list, so the coverage relationship a matrix asserts stays queryable without re-parsing
  the cell.
- This requirement SHALL change no archetype declaration: it constrains what the emitted models
  may contain, and every existing document keeps validating unchanged.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-013-CON-1 | Each emitted model SHALL carry exactly one role, so no model is reused for both a definition and an occurrence. | Architecture | Test |
| FR-013-CON-2 | The module SHALL NOT declare a schema for a run record, a binding record or a baseline, because those are owned by Engineering Assurance and quoin. | Scope | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-013-AC-1 | Every exported model carries exactly one role, `definition` or `evidence-act`, and the assignment matches the list above. | Test (TC-120) |
| FR-013-AC-2 | No emitted model declares a property whose **name** matches the run-record lexicon (`run`, `runId`, `startedAt`, `finishedAt`, `duration`, `passed`, `failed`, `log`, `artifact`) as a whole word. | Test (TC-121) |
| FR-013-AC-3 | `Plan` and `Task` declare no execution property; a Task record carries its authored `track`, dependencies and verification references only. | Test (TC-122) |
| FR-013-AC-4 | `SpecReview` findings rows carry `id`, `severity`, `summary`, `refs` and an optional `escapeCause`, and a `Finding` document id matches `FIND-` while a row id matches `FND-`. | Test (TC-123) |
| FR-013-AC-5 | `TestMatrix` and `TestMatrixIndex` rows carry their trace tokens as an ordered list, and a matrix record answers "which criteria does this row claim to cover" without re-parsing the cell. | Test (TC-124) |
| FR-013-AC-6 | `mappings.yaml` records the run-record concepts this module does not model and names their owner. | Test (TC-125) |
| FR-013-AC-7 | This requirement adds no manifest declaration of its own: the baseline comparison is [FR-010-AC-3](./FR-010-semantic-manifest-contract.md), which is the single normative statement of it, and this criterion is discharged by that test rather than by a second copy. | Inspection |
| FR-013-AC-8 | A reviewer has read every emitted model's property documentation and recorded that none *means* a run outcome under a different name. A test can check names; only a reader can check meaning, and presenting that judgement as a test would be the fabrication this module's own escape-cause vocabulary exists to name. | Inspection (TC-143) |

## Dependencies

- **Upstream**: [FR-006](./FR-006-evidence-layer-archetypes.md), [FR-007](./FR-007-verification-method-catalog.md), [FR-009](./FR-009-emitted-json-schemas.md); engineering-assurance FR-004 and FR-008 (`ix://agent-ix/engineering-assurance/FR-004`, `ix://agent-ix/engineering-assurance/FR-008`), which own evidence state and the verification-semantics split this requirement defers to
- **Downstream**: the Engineering Assurance reconciliation of run records, outside this module
