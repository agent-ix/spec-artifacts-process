---
id: SR-015
title: "scope and boundary review of the #78 spec set"
type: SpecReview
analysis: scope-boundary
scope: "spec/spec.md, spec/functional/FR-009..FR-013, spec/non-functional/NFR-001"
review_set: all
---
# SR-015: scope and boundary review of the #78 spec set

## Summary

System boundary, external dependencies and responsibility allocation for the #78 set.

In scope, this module guarantees: the manifest declaring twelve artifact types and their
contracts; one emitted JSON Schema per type; the published Markdown mapping; the shipped
skeletons; and that none of the above changes the meaning of an existing archetype.

External dependencies, with their trust status:

| Dependency | Type | Assumed or Guaranteed | Contract |
|------------|------|------------------------|----------|
| `@agent-ix/semantic-core` 0.1.0 | npm package | Assumed | filament-core-data FR-031..FR-034 |
| `@typespec/compiler` / `@typespec/json-schema` 1.15.0 | build tool | Assumed | exact pin + lockfile |
| Quire engine (loader, validate, coverage) | library/CLI | Guaranteed | FR-010-AC-5, FR-012-AC-2, NFR-001-AC-4 |
| Quoin module install | CLI | Assumed | quoin FR-070/FR-073; no IT in this set |
| `filament-core-service` activation | HTTP service | Guaranteed | pre-existing IT-001 |
| `spec-objects-business`, `filament-core-data` | consumer repos | Guaranteed | NFR-001-AC-5 |
| Engineering Assurance run records | out of boundary | Assumed | FR-013-CON-2 |

Allocation: FR-009 is `infrastructure` (build), FR-010 and FR-013 are `core` (the contract),
FR-011 is `core` (the mapping data), FR-012 is `core` (authoring surface), NFR-001 is
`cross-cutting` (compatibility). Every requirement has exactly one owner and one class, with no
TBD.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | Boundary crossed without a contract test: the Quoin install path. `spec-objects-business` carries IT-002 (`quoin module install path:<dir>`) for exactly this boundary and this set has no equivalent — FR-010 depends on quoin FR-070/FR-073 and asserts nothing about whether Quoin accepts the manifest. The `semantic` block is the key Quoin reads; if this module writes it in a form Quoin rejects, nothing in this specification notices. Either add the IT or state in Out of Scope that Quoin acceptance is unverified and why. | FR-010, spec.md | missing-requirement |
| FND-002 | medium | NFR-001-AC-5 reaches *into two other repositories* to take a measurement. That is the right verification, but it puts two repositories inside this specification's verification boundary while leaving them outside its responsibility boundary, and nothing states what happens when one of them is red for an unrelated reason. Define the comparison as a delta (findings under 0.2.0 minus findings under 0.1.0) rather than an absolute, which is what the Verification section already describes — then make the criterion say it. | NFR-001-AC-5 | wrong-requirement |
| FND-003 | medium | The mapping (FR-011) is declared as shipped module data with no production consumer, and the reference implementation is explicitly a test oracle (FR-011-CON-3). That means this module publishes a contract that nothing on the other side of the boundary is obliged to honour. It is the right call for now and `spec.md` names quire-rs#393 as the owner of the eventual extractor, but the Out of Scope entry should also say what happens if a consumer implements the mapping differently — whose bug that is. | FR-011-CON-3, spec.md | correct-requirement-no-evidence |
| FND-004 | medium | The `verification_catalog` (FR-007) and the `traceability` model (FR-004) are inside this manifest and therefore inside the change's blast radius, but neither appears in FR-010's list of declarations to hold byte-identical — that list names them, but only NFR-001-AC-1 makes it a criterion, and only FR-010-AC-3 gives it a baseline. The `traceability.trace_targets` block in particular binds by `archetype:` name; adding `data_schema` to an artifact type is safe, but the specification never says the trace targets were considered. State that they were. | FR-010-AC-3, NFR-001-AC-1, FR-004, FR-007 | correct-requirement-no-evidence |
| FND-005 | low | `spec.md`'s System Description still describes the module as "templates and schemas for agent CLI generators (minijinja-cli)". After #78 the module also publishes a declaration grammar and a mapping consumed by engines, not generators. Update the System Description so the boundary diagram a reader builds from it is the current one. | spec.md | wrong-requirement |
| FND-006 | low | No requirement allocates the `.gitattributes` LF pin (FR-009 Behavior) to a component; it is a repository-level guarantee that every other requirement's byte comparison depends on. Recorded as cross-cutting so it is not deleted as unowned. | FR-009 | correct-requirement-no-evidence |
