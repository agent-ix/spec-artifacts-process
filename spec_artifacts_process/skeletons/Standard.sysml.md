---
id: Standard-001
title: "ISO/IEC/IEEE 29148 — Requirements engineering"
type: Standard
code: iso-iec-ieee-29148
description: "Requirements engineering for systems and software: the processes and the content of requirement artifacts."
guide: "Apply to any specification bundle that declares stakeholder, user, functional and non-functional requirements. Conformance is judged on artifact structure and on requirement statements, not on tooling."
link: "https://www.iso.org/standard/72089.html"
---
<!-- Standard authoring skeleton, ALTERNATE Properties form. Declares exactly
     the same fields as `Standard.md`, authored as one ```sysml fence instead of
     the typed table (FR-012-AC-5). One artifact carries one form; the alternate
     is a separate file, never a second block in the same artifact. A document
     carrying both is rejected with `both-forms`, and the two files here map to
     records that differ in no property. -->
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

```sysml
attribute code : String[1..1] { identity, pattern: ^[a-z0-9][a-z0-9.-]*$ }
attribute title : String[1..1] { minLength: 1 }
attribute edition : String[0..1] { minLength: 1 }
attribute link : String[0..1] { format: iri }
attribute supersedes : String[0..*]
```

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
