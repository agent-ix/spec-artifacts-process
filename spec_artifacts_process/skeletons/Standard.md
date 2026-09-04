---
id: Standard-001
title: "ISO/IEC/IEEE 29148 — Requirements engineering"
type: Standard
code: iso-iec-ieee-29148
description: "Requirements engineering for systems and software: the processes and the content of requirement artifacts."
guide: "Apply to any specification bundle that declares stakeholder, user, functional and non-functional requirements. Conformance is judged on artifact structure and on requirement statements, not on tooling."
link: "https://www.iso.org/standard/72089.html"
---
<!-- Standard authoring skeleton (spec-artifacts-process). Fill every section
     with substantive content. Contract:
     - Frontmatter: `type: Standard`; `id` matches ^[A-Za-z]{2,}-[0-9]+$;
       `code` is REQUIRED and is the stable slug spec frontmatter references
       from `standards_alignment[]`. `description`, `guide` and `link` are
       optional frontmatter and are what the `standard` OBJECT TYPE extracts.
     - `## Properties` and `## Invariants` are OPTIONAL (manifest
       `required: false`). They exist because a Standard is the one process
       artifact that declares a typed structure: the properties a conforming
       artifact carries, and the invariants conformance requires. Every Standard
       document that validates without them still validates.
     - `## Properties` is the typed table, headers exactly
       `Field | Type | Multiplicity | Constraints`. The ALTERNATE form of the
       same declarations is one ```sysml fence under the same heading — see
       `Standard.sysml.md`. ONE ARTIFACT CARRIES ONE FORM; a document with both
       is rejected (`both-forms`).
     - `## Invariants` holds one `### <clauseId>` subsection per clause, each
       owning exactly one ```ocl fence. `clauseId` is an Identifier — letters,
       digits and underscores, never a leading digit — unique in the document.
       The clause text is carried verbatim and never evaluated here. -->
# Standard-001: ISO/IEC/IEEE 29148 — Requirements engineering

## Description

The international standard for requirements engineering. It defines the
processes that produce requirements and the content each requirement artifact
carries, across stakeholder, user, system and software levels.

## Application Guidance

Apply to any specification bundle that declares stakeholder, user, functional
and non-functional requirements. Conformance is judged on the structure of the
artifacts and on the requirement statements themselves; it says nothing about
which tool validates them.

## Properties

| Field | Type | Multiplicity | Constraints |
|-------|------|--------------|-------------|
| code | String | 1..1 | identity, pattern: ^[a-z0-9][a-z0-9.-]*$ |
| title | String | 1..1 | minLength: 1 |
| edition | String | 0..1 | minLength: 1 |
| link | String | 0..1 | format: iri |
| supersedes | String | 0..* | |

## Invariants

The clauses a conforming artifact set must satisfy. Each clause owns one `ocl`
fence under its own `### <clauseId>` heading.

### EveryRequirementIsUniquelyIdentified

```ocl
context RequirementSet
inv EveryRequirementIsUniquelyIdentified:
  self.requirements->isUnique(r | r.id)
```

### EveryRequirementIsVerifiable

```ocl
context Requirement
inv EveryRequirementIsVerifiable:
  self.acceptanceCriteria->notEmpty() implies
    self.acceptanceCriteria->forAll(c | c.verification->notEmpty())
```
