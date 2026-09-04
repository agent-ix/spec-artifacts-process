---
id: US-002
title: "Declare the process artifact types against semantic-core"
type: US
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/StR-001"
    type: "traces_to"
---
# US-002: Declare the process artifact types against semantic-core

## Story

**As a** maintainer of the process-artifact module every other repository validates against
**I want** each process artifact type to carry one machine-readable declaration of what a
document of that type contains
**So that** a reviewer, a generator and the engine read the same definition instead of three
copies that drift apart.

This story describes the maintainer's need in informal language and does not prescribe the
declaration language, the schema format, or where the declaration is stored.

## Context

This module declares the archetypes the whole programme validates against: `TestMatrix`,
`TestMatrixIndex`, `Plan`, `Task`, `SpecReview`, `Standard` and the evidence-layer registries.
Today what a document of one of those types *contains* is written down in three places that
nothing keeps in agreement: a frontmatter JSON Schema that constrains only frontmatter, a
`body_extraction` locator set that names sections and asserts table shapes, and the prose of a
shipped skeleton. A consumer that wants the whole record — the frontmatter identity, the
sections, and the table rows together — has to reconstruct it by reading the manifest.

The sibling modules `spec-objects-business` and `spec-artifacts-iso` have already taken the
semantic-module contract, so the maintainer's question is no longer whether such a declaration
is possible but why this module is the one still missing it.

## Acceptance Examples (Illustrative)

These examples clarify the maintainer's expectations. They are illustrative only — not test
cases and not verification criteria.

### US-002-EX-1: One declaration per type

- **Given** a process artifact type the module declares
- **When** the maintainer looks for what a document of that type contains
- **Then** there is exactly one declaration to read, and the shipped schema was generated from it

### US-002-EX-2: A skeleton that is also a fixture

- **Given** the skeleton the module ships for a type
- **When** a generator copies it
- **Then** the copy is a document the declaration accepts, because the skeleton itself is checked
  against that declaration

### US-002-EX-3: A change here is visible where it lands

- **Given** a repository that validates its Test Matrix against this module
- **When** the module changes
- **Then** the maintainer can see, before releasing, whether that repository still validates

## Options (Exploratory)

Approaches discussed during discovery, none of which imply commitment: hand-writing a second
JSON Schema per type beside the frontmatter schema; generating the schema from a typed source
shared with the sibling modules; or teaching the engine to synthesise a schema from the
`body_extraction` locators. These options may or may not influence later requirements.

## Constraints (Contextual)

Maintainers noted that this module is a dependency of every other repository's validation, so
discovery treated "nothing a consuming repository authors today may stop validating" as the
governing worry. This context is not binding and is made normative by NFR-001 rather than here.

## Dependencies (Contextual)

Relationships observed during discovery. Upstream: the semantic-core declaration grammar and
the module-manifest `semantic` block. Downstream: the corpus promotion sweep, which is not part
of this story. These are potential relationships, not formal traceability.

## Priority and Risk (Informative)

Business value is high because this module is the last artifact module without a machine-readable
declaration; urgency is medium; the risk if unmet is that the three drifting copies keep
producing contract defects that only a reader notices. This information is for planning only.

## Notes (Informative)

Open question raised in discovery: whether the definition/occurrence split belongs in this
module's schemas or in Engineering Assurance. Captured here for later analysis; FR-013 answers
it, this story does not.

## Traceability (Informative)

Potential trace relationships established during refinement: this story may trace to the
stakeholder requirement for module activation and to functional requirements for schema
emission, the manifest contract, the Markdown mapping, and executable skeletons. Links may be
updated as understanding evolves.
