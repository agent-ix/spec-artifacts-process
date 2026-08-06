---
id: US-001
title: "Trust the test matrix through machine validation"
type: US
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/StR-001"
    type: "traces_to"
---
# US-001: Trust the test matrix through machine validation

## Story

**As a** spec author (or planning agent) maintaining a repository's test matrix
**I want** the `tests.md` Test Matrix document to be checked for the expected coverage tables and test-case columns whenever it is validated
**So that** I can rely on the matrix as a parseable, trustworthy record of coverage instead of a free-form table that silently drifts.

The story expresses the author's need in informal language and does not prescribe
how the platform performs the structural checks.

## Context

Every spec bundle in the ecosystem carries a `tests.md` of `type: TestMatrix`,
and the quoin `spec-matrix` skill emits a standard template for it (coverage
tables plus a Test Case Summary). Today the TestMatrix artifact type carries no
body contract, so any body shape passes validation: matrices drift from the
template, columns get renamed, status markers vary, and downstream tooling
(gap analysis, planning) cannot reliably read coverage out of them. The sibling
`SpecReview` archetype already solves this for review findings, which shaped the
expectation that the matrix could be held to the same standard.

## Acceptance Examples (Illustrative)

These examples clarify the author's expectations. They are illustrative only —
not test cases and not verification criteria.

### US-001-EX-1: Conforming matrix passes

- **Given** a `tests.md` generated from the spec-matrix template with coverage tables and a filled Test Case Summary
- **When** the author validates the spec bundle
- **Then** validation passes and each test-case row is available to tooling as a record

### US-001-EX-2: Drifted matrix is surfaced

- **Given** a `tests.md` whose Test Case Summary is missing or whose `Type` column carries an invented value
- **When** the author validates the spec bundle
- **Then** validation fails, pointing at the missing table or the offending cell

## Dependencies (Contextual)

Relationships observed during discovery. Upstream: the module activation story
([StR-001](../stakeholder/StR-001-module-activation.md)) and the quoin
`spec-matrix` template that authors matrices. Downstream: a likely functional
requirement adding a body contract to the TestMatrix artifact type. These are
potential relationships, not formal traceability.

## Notes (Informative)

Open question raised in discovery: should coverage tables for requirement
classes a repository does not use (e.g. NFR) be demanded anyway? Captured here
for requirements analysis; it introduces no requirement. Resolved during
requirements analysis: [FR-003](../functional/FR-003-testmatrix-body-extraction.md)
declares those tables as optional (`required: false`) extractions whose column
sets are asserted only when present.
