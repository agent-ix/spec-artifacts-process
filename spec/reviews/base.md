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
records) are sound. All five findings are now resolved: FND-003 (`spec.md` counts) and FND-004
(US-001 open question) were fixed during the review pass; FND-001 was closed by
the Test Matrix expansion to TC-001..TC-018 (commit 505d537); FND-002 was
closed by adding planned FR-002 coverage (TC-019..TC-023); FND-005 (StR-001
stale counts) was fixed under explicit user authorization to edit pre-existing
artifacts. The related matrix gap GAP-002 became normative FR-003-AC-11 with
the missing quire-rs uniqueness assert recorded as an external dependency.

## Findings

| ID | Severity | Summary | Refs |
|---------|----------|----------------------------------|--------|
| FND-001 | medium | RESOLVED (2026-08-04, commit 505d537): FR-003 test coverage was a single planned TC-001; the Test Matrix pass expanded it to TC-001..TC-018 covering option permutations (Type/Status/Priority vocabularies), constraint boundaries (`min_rows`, table presence), and error paths (malformed `Test ID` / `Traces To` tokens) | FR-003, TM-001 |
| FND-002 | medium | RESOLVED (2026-08-04, user-authorized): FR-002 acceptance criteria (FR-002-AC-1..5) had no test cases; planned TC-019..TC-023 added to the matrix with per-AC coverage rows (Findings-table pass/fail, Severity vocabulary, FND id pattern, skeleton packaging, Review-archetype non-alteration) | FR-002, TM-001 |
| FND-003 | low | `spec.md` In-Scope contribution counts were stale ("5 process archetypes … 7 artifact types") vs the manifest's actual 6 archetypes / 9 artifact types (SpecReview archetype, SpecReview + Feedback artifact types missing) — fixed in place (spec.md was changed by this branch) | spec.md, FR-002 |
| FND-004 | low | US-001's Notes carried an unresolved open question (demand coverage tables for unused requirement classes?) that FR-003's optional-tables behavior already answers — resolution note added in place | US-001, FR-003 |
| FND-005 | low | RESOLVED (2026-08-04, user-authorized pre-existing-artifact edit): StR-001 Validation Criteria carried the same stale counts as spec.md; corrected to 6 archetypes / 9 artifact types | StR-001 |
