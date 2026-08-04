---
id: SR-001
title: "base review of FR-003 / US-001 / tests.md (spec/testmatrix-extraction)"
type: SpecReview
analysis: base
scope: "spec/functional/FR-003-testmatrix-body-extraction.md, spec/usecase/US-001-machine-validated-test-matrix.md, spec/tests.md (consistency: FR-001, FR-002, StR-001, manifest.yaml SpecReview precedent)"
review_set: base
---
# SR-001: base review of FR-003 / US-001 / tests.md (spec/testmatrix-extraction)

## Summary

Base checklist review of the artifacts added/changed on branch
`spec/testmatrix-extraction`: FR-003 (TestMatrix `body_extraction`), US-001, and
the restructured `tests.md`, checked for ID formats, US/FR quality, the six
coverage rules, and consistency with FR-001/FR-002/StR-001 and the manifest's
`SpecReview` `body_extraction` precedent. ID formats, cross-references, EARS
phrasing, and the FR-003 contract's alignment with the SpecReview precedent
(`table_row` + `column_choices`/`column_patterns` asserts, `multiple: true`
records) are sound. Findings FND-003 (stale contribution counts in `spec.md`)
and FND-004 (US-001 open question already resolved by FR-003's optional-tables
design) were fixed in place on this branch; FND-001 (FR-003 six-rules coverage
is a single planned TC-001) is deferred to the Test Matrix pass; FND-002
(FR-002 has no test coverage) and FND-005 (StR-001 carries the same stale
counts but was not changed by this branch) remain open.

## Findings

| ID | Severity | Summary | Refs |
|---------|----------|----------------------------------|--------|
| FND-001 | medium | FR-003 test coverage is a single planned TC-001 tracing all testable ACs; six-rules demands enumeration of option permutations (Type/Status/Priority `column_choices` vocabularies), constraint boundaries (`min_rows`, empty/omitted tables), and error paths (malformed `Test ID` / `Traces To` tokens) as distinct test cases — deferred to the Test Matrix pass on this branch | FR-003, TM-001 |
| FND-002 | medium | FR-002 acceptance criteria (FR-002-AC-1..5) have no test cases in the Test Case Summary; matrix honestly reports "❌ Not covered" but the coverage gap is unresolved — out of scope for this branch's FR-003 work, needs its own matrix/implementation pass | FR-002, TM-001 |
| FND-003 | low | `spec.md` In-Scope contribution counts were stale ("5 process archetypes … 7 artifact types") vs the manifest's actual 6 archetypes / 9 artifact types (SpecReview archetype, SpecReview + Feedback artifact types missing) — fixed in place (spec.md was changed by this branch) | spec.md, FR-002 |
| FND-004 | low | US-001's Notes carried an unresolved open question (demand coverage tables for unused requirement classes?) that FR-003's optional-tables behavior already answers — resolution note added in place | US-001, FR-003 |
| FND-005 | low | StR-001 Validation Criteria carry the same stale counts ("5 archetypes … 7 artifact types") as spec.md did; StR-001 was not changed by this branch, so left open for a follow-up rather than edited here | StR-001 |
