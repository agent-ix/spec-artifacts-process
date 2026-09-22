---
type: master-requirements
name: spec-artifacts-process
org: agent-ix
component_type: filament-module
implementation_language: python
tags:
  - spec-artifacts
  - process
depends_on: []
standards_alignment:
  - iso-iec-ieee-29148
relationships:
  - target: "ix://agent-ix/filament-core/FR-035"
    type: "depends_on"
    cardinality: "1:1"
security_critical: false
---
# Master Requirements Specification

## Purpose

This document specifies the requirements for spec-artifacts-process, a Filament Module that contributes standardized process artifact templates and archetypes. Engineering teams need standardized templates for ADRs, plans, reviews, findings, test matrices, and standards so that authored process artifacts share one authoritative structure that downstream tooling can parse and validate.

## Scope

### In Scope

- The Module manifest and the contributions it declares: 6 process archetypes (adr, plan, review, spec-review, test-matrix, standard), 1 grammar (process-artifacts), and the 12 artifact types the manifest declares (ADR, Plan, Task, Review, SpecReview, Finding, Feedback, TestMatrixIndex, TestMatrix, Standard, SuiteRegistry, Inspections).
- The templates and schemas this module ships for agent CLI generators (minijinja-cli).
- The semantic-module contract (issue #78): a TypeSpec source importing `@agent-ix/semantic-core` 0.1.0, one emitted JSON Schema per declared artifact type under `spec_artifacts_process/schemas/`, the manifest `semantic` block with reference-form `data_schema`, the published Markdown mapping, and the skeletons rewritten as executable fixtures with negative counterparts.

### Out of Scope

- The filament-core-service activation machinery that registers the Module, referenced here only by relationship.
- Deployment topology and infrastructure of the target cluster.
- Changing the meaning of any archetype this module already publishes. This module owns the contracts every repository in the programme validates against, so tightening or loosening an existing pattern is a build break everywhere; NFR-001 measures that nothing moved. In particular `⚠️` stays out of the `Status` vocabulary — it was retired by CR-031 because a row carrying it was exempt from the status-lie check by construction (quire-rs CR-083). The `quoin:spec-matrix` skill still documents it as valid; the skill is the defect and is filed as `agent-ix/quoin#337`.
- Editing any corpus repository. The advisory sweep and the corpus promotion are `agent-ix/quoin#291`; this specification's consumer measurement reads two repositories and writes to neither.
- Generated-language fixtures (Rust, TypeScript, Python) for the process types: produced by the TypeSpec frontend and compiler core (`agent-ix/filament-core-data#21`, `#22`, `#23`) and published only behind the promotion gate (`agent-ix/quoin#290`); the semantic-core language packages are `agent-ix/filament-core-data#11`. None is produced or faked here.
- An engine-side extractor that builds a process record from Markdown. `quire.validate_document` validates a *declaration* record on the `object:` axis and never reaches an artifact-type record; the FR-011 reference mapping is this module's test oracle, and the extractor is quire-rs work (`agent-ix/quire-rs#393`).
- Naming what a module load refused: `agent-ix/quire-rs#221` (an unknown manifest key empties the model silently) and `agent-ix/quire-rs#394` (a `data_schema` digest mismatch drops the type with no diagnostic). FR-010-AC-6's "naming the key or the path" half is blocked on them and is carried as an explicit expected failure.
- Record validation of a legacy-form artifact that declares `object:`: `agent-ix/quire-rs#391` (the engine validates an `unavailable` record as `{}`, so a legacy form errors even under `legacy_forms: warning`).
- Resolving a reference-form `data_schema` into a stored snapshot at activation: `agent-ix/filament-core-service#23`. Until it lands the service stores the reference verbatim.
- Applying `filament-core-service`'s FR-035 module-manifest schema to this
  manifest as a document. That schema is `filament-core-service`'s; this
  repository holds no copy of it and depends on no package that redistributes it
  as a document this repository validates against (PLAT-902). It is verified
  where it is applied, at activation — and **that is not verified here today**:
  IT-001 has no implementing test and IT-002 is a strict expected failure
  (GAP-003, `agent-ix/quoin#347`). The executed, copy-free checks are narrower
  and do not substitute for it: the module loads with its full archetype set
  (FR-010-AC-5, TC-093) and an unknown `semantic` key is refused at load
  (FR-010-AC-6, TC-094).
- Making Quoin install an artifact-type semantic module: `agent-ix/quoin#347`. Quoin's FR-070 validator resolves `semantic.exports` against `object_types` only, so neither this module nor the already-merged `spec-artifacts-iso` can be installed. IT-002 exercises the boundary and is carried as a strict expected failure rather than a skip; the FR-035 wording that made the ambiguity possible is `agent-ix/filament-core-service#27`.
- Run records, binding records, baselines and freshness. FR-013 states which concepts this module models and names Engineering Assurance and quoin as the owners of the rest; nothing here schematises a verification run.
- Resolving the `Standard` artifact type / `standard` object type duplication the issue notes. Both are activated by consumers today and unifying them changes how an existing declaration resolves, which is exactly the breaking change this specification refuses to make as a side effect of the migration. What #78 does do is write the resolution down rather than leave it to first-wins: a document is dispatched on frontmatter `type:`, so `type: Standard` resolves to the **artifact type** and the emitted `Standard.json` describes it; the `standard` **object type** is reached only through `object: standard` and keeps the inline `data_schema` that describes its frontmatter projection. `quire validate` emits `DuplicateArchetype: 'standard' … first-wins` on every run of this repository because the two names collide case-insensitively in the archetype registry; that diagnostic is the duplication, and FR-010-AC-8 pins both declarations so the migration does not quietly change which one wins.

## System Overview

### System Description

The Module packages process-artifact archetypes, a grammar, and artifact types into a manifest that
filament-core-service activates. Activation registers the declared contributions in the database,
after which authors and agent CLI generators can produce valid process artifacts.

After #78 the module also publishes a machine-readable declaration of what a document of each type
contains, consumed by engines rather than by generators. Two named artifacts carry that work and
are components of this system for allocation purposes: the **schema generator**
(`spec_artifacts_process/semantic/scripts/generate.mjs`), which projects the TypeSpec source into
the shipped JSON Schemas, and the **record mapping** (`spec_artifacts_process/mappings.yaml`),
which states how an authored document becomes a record. The mapping is data; the reference
implementation that reads it lives in this module's test support and is a test oracle, never
module code.

### Intended Users

The Filament platform, spec authors, and agent CLI generators that rely on these archetypes.

## Requirements Architecture

The requirement classes that make up this specification trace as follows:

- `stakeholder/` — StR-XXX stakeholder requirements.
- `usecase/` — US-XXX user stories.
- `functional/` — FR-XXX functional requirements.
- `non-functional/` — NFR-XXX non-functional requirements.
- `integration/` — IT-XXX integration tests.
- `tests.md` — test matrix linking FRs to integration tests.

FR-001 activates the manifest against filament-core; FR-002 through FR-008 declare the archetypes,
the traceability model, the evidence layer and the verification catalog. The semantic-module
contract sits on top of those: FR-009 emits one JSON Schema per declared artifact type from a
TypeSpec source, FR-010 declares the contract in the manifest without altering an archetype,
FR-011 publishes the Markdown mapping, FR-012 makes the skeletons executable fixtures with
negative counterparts, and FR-013 keeps authored definitions separate from execution occurrences.
NFR-001 bounds the whole change to additive compatibility, measured by a structural diff of every
0.1.0 archetype declaration and vocabulary against the checked-in 0.1.0 baseline and by every
shipped skeleton validating with zero error findings (AC-1..4).

## References

- ISO/IEC/IEEE 29148 — Requirements engineering.
- filament-core-service [FR-035](ix://agent-ix/filament-core-service/FR-035) (Module Manifest Schema).
- The component's source repository and README.
