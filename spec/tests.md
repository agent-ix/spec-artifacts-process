---
id: TM-001
title: "spec-artifacts-process test matrix"
type: TestMatrix
---
# TM-001: spec-artifacts-process test matrix

## Requirements Traceability

### Stakeholder Requirement Coverage

| Stakeholder Req | Trace to US/FR | Test/Validation | Coverage Status |
|-----------------|----------------|-----------------|-----------------|
| StR-001 | US-001, FR-001, FR-002, FR-003, FR-004 | Review | ✅ Complete |

### User Story Coverage

| User Story | Acceptance Criteria | Test Cases | Coverage Status |
|------------|---------------------|------------|-----------------|
| US-001 | US-001-EX-1, US-001-EX-2 (illustrative) | TC-001, TC-002, TC-005 | 🚧 Planned |

### Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Coverage Status |
|----------------|---------------------|------------|-----------------|
| FR-001 | FR-001-AC-1 .. FR-001-AC-4 | IT-001 | 🚧 Specified |
| FR-002 | FR-002-AC-1 | TC-019 | 🚧 Planned |
| FR-002 | FR-002-AC-2 | TC-020 | 🚧 Planned |
| FR-002 | FR-002-AC-3 | TC-021 | 🚧 Planned |
| FR-002 | FR-002-AC-4 | TC-022 | 🚧 Planned |
| FR-002 | FR-002-AC-5 | TC-023 | 🚧 Planned |
| FR-002 | FR-002-AC-6 | TC-027 | ✅ Complete |
| FR-003 | FR-003-AC-1 | TC-001, TC-003, TC-016 | ✅ Complete |
| FR-003 | FR-003-AC-2 | TC-002, TC-016 | ✅ Complete |
| FR-003 | FR-003-AC-3 | TC-004, TC-005 | ✅ Complete |
| FR-003 | FR-003-AC-4 | TC-006, TC-007, TC-026 | ✅ Complete |
| FR-003 | FR-003-AC-5 | TC-008, TC-009 | ✅ Complete |
| FR-003 | FR-003-AC-6 | TC-012, TC-013, TC-018 | ✅ Complete |
| FR-003 | FR-003-AC-7 | TC-014, TC-015 | ✅ Complete |
| FR-003 | FR-003-AC-8 | TC-001 | ✅ Complete |
| FR-003 | FR-003-AC-9 | TC-017 (+ Inspection) | ✅ Complete |
| FR-003 | FR-003-AC-10 | TC-010, TC-011, TC-025 | ✅ Complete |
| FR-003 | FR-003-AC-11 | TC-024 (blocked: no quire-rs uniqueness assert) | ⚠️ Blocked |
| FR-004 | FR-004-AC-1 | TC-028 | ✅ Complete |
| FR-004 | FR-004-AC-2 | TC-029, TC-039 | ✅ Complete |
| FR-004 | FR-004-AC-3 | TC-030 | ✅ Complete |
| FR-004 | FR-004-AC-4 | TC-031 | ✅ Complete |
| FR-004 | FR-004-AC-5 | TC-032 | ✅ Complete |
| FR-004 | FR-004-AC-6 | TC-033 | ✅ Complete |
| FR-004 | FR-004-AC-7 | TC-034 | ✅ Complete |
| FR-004 | FR-004-AC-8 | TC-035 | ✅ Complete |
| FR-004 | FR-004-AC-9 | TC-036 | ✅ Complete |
| FR-005 | FR-005-AC-1 | TC-037 | ✅ Complete |
| FR-005 | FR-005-AC-2 | TC-037 | ✅ Complete |
| FR-005 | FR-005-AC-3 | TC-038 | ✅ Complete |
| FR-006 | FR-006-AC-1 | TC-040 | ✅ Complete |
| FR-006 | FR-006-AC-2 | TC-041 | ✅ Complete |
| FR-006 | FR-006-AC-3 | TC-042 | ✅ Complete |
| FR-006 | FR-006-AC-4 | TC-043 | ✅ Complete |
| FR-006 | FR-006-AC-5 | TC-044 | ✅ Complete |
| FR-006 | FR-006-AC-6 | TC-045 | ✅ Complete |
| FR-006 | FR-006-AC-7 | TC-046 | ✅ Complete |
| FR-006 | FR-006-AC-8 | TC-047 | ✅ Complete |
| FR-007 | FR-007-AC-1 | TC-048 | ✅ Complete |
| FR-007 | FR-007-AC-2 | TC-049 | ✅ Complete |
| FR-007 | FR-007-AC-3 | TC-050 | ✅ Complete |
| FR-007 | FR-007-AC-4 | TC-051 | ✅ Complete |
| FR-007 | FR-007-AC-5 | TC-052 | ✅ Complete |
| FR-007 | FR-007-AC-6 | TC-053 | ✅ Complete |
| FR-007 | FR-007-AC-7 | TC-054 | ✅ Complete |
| TC-055 | The traceability model declares the ecosystem's obligation sources — the two acceptance-criterion targets and the NFR `Measurement and Evaluation` table with its rendered ids and parameters — so quire-rs FR-053 derives obligations rather than shipping inert. Found end-to-end: `quoin evidence record` bound nothing until this landed (FR-007) | Unit | P0 | FR-007-AC-8 | ✅ |
| TC-056 | The catalog carries `compile-time-check` and `dynamic-analysis-sanitizer` — the two means the first corpus sweep found in use with no catalog word for them — and neither collapses into the neighbour it was nearly filed under | Unit | P0 | FR-007-AC-9 | ✅ |
| TC-057 | No catalog id names a tool, a cadence, or a class that has methods under it; every tool named anywhere appears only in `tooling` (`inspection`/`demonstration` are exempt — for those two IADT classes the class and the method genuinely coincide) | Unit | P1 | FR-007-AC-10 | ✅ |
| FR-007 | FR-007-AC-8 | TC-055 | ✅ Complete |
| FR-007 | FR-007-AC-9 | TC-056 | ✅ Complete |
| FR-007 | FR-007-AC-10 | TC-057 | ✅ Complete |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---------|-------|------|----------|-----------|--------|
| TC-001 | Conforming TestMatrix (all tables) validates; test-case rows extracted one record per row | Unit | P0 | FR-003-AC-1, FR-003-AC-8, US-001 | ✅ |
| TC-002 | Doc missing the Test Case Summary table fails with reason `missing` | Unit | P0 | FR-003-AC-2, US-001 | ✅ |
| TC-003 | Doc missing the Functional Requirement Coverage table fails with reason `missing` | Unit | P1 | FR-003, FR-003-AC-1 | ✅ |
| TC-004 | Type vocabulary permutation: Unit, Integration, E2E, Property each accepted | Unit | P1 | FR-003-AC-3 | ✅ |
| TC-005 | Type cell outside the vocabulary (e.g. `Manual`) fails via `column_choices` (reason `assert`) | Unit | P0 | FR-003-AC-3, US-001 | ✅ |
| TC-006 | Test ID shape permutation: `TC-001`, `TC-INT-010`, `TC-INT-010a` each accepted | Unit | P1 | FR-003-AC-4 | ✅ |
| TC-007 | Malformed Test ID (`TC1`, `tc-001`, `TC-`, `TCX-001`) fails validation | Unit | P0 | FR-003-AC-4 | ✅ |
| TC-008 | Status marker permutation: ✅, ⚠️, ❌, 🚧 each accepted bare | Unit | P1 | FR-003-AC-5 | ✅ |
| TC-009 | Status cell outside the marker vocabulary (`Done`, decorated `✅ Complete`) fails via `column_choices` | Unit | P0 | FR-003-AC-5 | ✅ |
| TC-010 | Priority vocabulary permutation: P0, P1, P2, P3, P4 each accepted | Unit | P1 | FR-003-AC-10 | ✅ |
| TC-011 | Priority cell outside the vocabulary (`P5`, `High`) fails via `column_choices` | Unit | P0 | FR-003-AC-10 | ✅ |
| TC-012 | Traces To valid-token permutation: each token kind (StR/US/FR/NFR bare, -AC-, -CON-, IT, IT-SC) alone and comma-separated | Unit | P1 | FR-003-AC-6 | ✅ |
| TC-013 | Malformed Traces To rejected: semicolon separator, space-before-comma, TC token, truncated `FR--AC-1`, trailing comma | Unit | P0 | FR-003-AC-6 | ✅ |
| TC-014 | Doc omitting the StR/US/NFR coverage tables still validates (optional extractions) | Unit | P1 | FR-003-AC-7 | ✅ |
| TC-015 | Optional coverage table present with a wrong column set fails via column assert | Unit | P1 | FR-003-AC-7 | ✅ |
| TC-016 | `min_rows` boundary: required table with zero data rows fails; exactly one row passes | Unit | P1 | FR-003-AC-1, FR-003-AC-2 | ✅ |
| TC-017 | Contract lands without altering TestMatrix frontmatter schema or other archetypes (manifest diff assertion) | Unit | P2 | FR-003-AC-9 | ✅ |
| TC-018 | Empty Traces To cell fails via `column_patterns` | Unit | P2 | FR-003-AC-6 | ✅ |
| TC-019 | Conforming SpecReview doc validates; doc missing the Findings table fails with reason `missing` | Unit | P1 | FR-002-AC-1 | 🚧 |
| TC-020 | Severity vocabulary permutation: low/medium/high accepted; cell outside fails via `column_choices` (reason `assert`) | Unit | P1 | FR-002-AC-2 | 🚧 |
| TC-021 | Findings ID shapes: `FND-001` accepted; `FND-`, `fnd-1`, `F-001` fail the `id_pattern` | Unit | P1 | FR-002-AC-3 | 🚧 |
| TC-022 | Bundled `skeletons/SpecReview.md` is itself a valid SpecReview and ships in the wheel | Unit | P2 | FR-002-AC-4 | 🚧 |
| TC-023 | SpecReview registration leaves the freeform Review archetype unaltered (manifest diff assertion) | Unit | P2 | FR-002-AC-5 | 🚧 |
| TC-024 | Duplicate `Test ID` rows in the Test Case Summary fail validation | Unit | P2 | FR-003-AC-11 | ⚠️ |
| TC-025 | A Test Case Summary omitting the `Priority` column entirely validates (CR-018) | Unit | P0 | FR-003-AC-10 | ✅ |
| TC-026 | An `IT-` id validates; a prefix naming no declared archetype (`BENCH-001`) fails (CR-019) | Unit | P0 | FR-003-AC-4 | ✅ |
| TC-027 | `analysis` enum admits both review families: the nine spec analyses plus `code-review` and `spec-correctness` | Unit | P1 | FR-002-AC-6 | ✅ |
| TC-028 | Trace targets mint test-case ids from the Test Matrix and criterion ids from FR and NFR | Unit | P0 | FR-004-AC-1 | ✅ |
| TC-029 | Every trace target and document reference binds by `archetype` and declares no `document` key; matrix entries bind `TestMatrix` and additionally exclude test data (CR-062) | Unit | P0 | FR-004-AC-2 | ✅ |
| TC-030 | Exactly one templated canonical marker per language (rust, python, typescript) | Unit | P1 | FR-004-AC-3 | ✅ |
| TC-031 | Every legacy form declares a language and rewrites to a marker of that same language | Unit | P1 | FR-004-AC-4 | ✅ |
| TC-032 | Every reference names declared targets only and its pattern compiles with a capture group | Unit | P1 | FR-004-AC-5 | ✅ |
| TC-033 | `quire coverage` over this repo backs a non-zero count and mints no row from `tests/fixtures/` | Integration | P0 | FR-004-AC-6 | ✅ |
| TC-034 | `vocabularies.test_type_column` is declared and `no_source_symbol` lists only test-type values that mint no symbol — `Eval` and `Manual` in, `Static`/`Benchmark`/`Compile` out (CR-002) | Unit | P0 | FR-004-AC-7 | ✅ |
| TC-035 | Every `id_format`-free legacy form captures a comma-separated list, so a match carries every id its line names; `rust-test-name-id` stays single-id; and the `*-comment-id` delimiter still binds `// TC-480 / FR-025-AC-1: …` to one id and still rejects prose flowing through an id (CR-024) | Unit | P0 | FR-004-AC-8 | ✅ |
| TC-036 | Every trace target and document reference declares a non-empty `exclude` covering every test-tree convention (`tests/**`, `tests_integration/**`, `fixtures/**`), so a typed fixture — `FR`/`NFR` or `TestMatrix` — mints no id in a consuming repo (CR-025, widened CR-062) | Unit | P0 | FR-004-AC-9 | ✅ |
| TC-037 | Task `track` is a declared optional string with `minLength: 1` and no enum; `track: C` validates, `track: ""`, a non-string and a null fail | Unit | P1 | FR-005-AC-1, -AC-2 | ✅ |
| TC-038 | Scope guard: no `Track` archetype or artifact type is declared, and Task keeps its schema ref, id pattern and `depends_on`/`verifies`/`references` links (CR-026) | Unit | P1 | FR-005-AC-3 | ✅ |
| TC-039 | There is exactly one entry per kind of table — `test-case`, `traces-to`, `functional-coverage` — never one per matrix filename, so a nested matrix is reached by what it is rather than by what it is called (CR-062) | Unit | P0 | FR-004-AC-2 | ✅ |
| TC-040 | The manifest declares `SuiteRegistry` with its frontmatter schema and a `body_extraction` asserting the five columns, `min_rows: 1` and the `^SUITE-\d+$` id pattern — structured, doc-scoped, never a kebab slug (FR-006) | Unit | P0 | FR-006-AC-1 | ✅ |
| TC-041 | The manifest declares `Inspections` with its six columns, `Note` optional, `^INSP-\d+$`, and the closed `Pass\|Fail\|Waived` verdict vocabulary (FR-006) | Unit | P0 | FR-006-AC-2 | ✅ |
| TC-042 | `Evidence Kind` is byte-equal to the declared `test_type` vocabulary AND to the Test Matrix `Type` choices — one vocabulary, three uses. This test is what keeps the copies honest until `from_vocabulary` lands (quire-rs#146) (FR-006) | Unit | P0 | FR-006-AC-3 | ✅ |
| TC-043 | `suite` and `inspection` are archetype-bound trace targets and `inspection-obligation` is a declared reference, so both id classes mint and a bad obligation cell dangles rather than recording an act against nothing (FR-006) | Unit | P0 | FR-006-AC-4 | ✅ |
| TC-044 | A conformant suite registry validates; a kebab-slug id, a dropped required column, and an undeclared evidence kind (`SAST`) each fail (FR-006) | Unit | P0 | FR-006-AC-5 | ✅ |
| TC-045 | A conformant inspection record validates, omitting the optional `Note` column still validates, and an undeclared verdict fails (FR-006) | Unit | P0 | FR-006-AC-6 | ✅ |
| TC-046 | Both shipped skeletons validate against their own archetypes — a skeleton that does not sends every author who copies it into a failure (FR-006) | Unit | P1 | FR-006-AC-7 | ✅ |
| TC-047 | A repo declaring neither evidence document validates and reports exactly as before: no scan diagnostic, no group, no mention of either archetype (FR-006) | Unit | P0 | FR-006-AC-8 | ✅ |
| TC-048 | The catalog covers every technique the ADR-0011 survey dispositioned — 31 methods across all four IADT classes, not a starter subset: an absent entry reads as "not applicable" rather than "not yet written" (FR-007) | Unit | P0 | FR-007-AC-1 | ✅ |
| TC-049 | Every entry declares a non-empty name, class and definition, and every class is one of the four IADT values — the engine treats `class` as a free string, so this contract is the module's to keep (FR-007) | Unit | P0 | FR-007-AC-2 | ✅ |
| TC-050 | Every `evidence_kind` is a member of the declared `test_type` vocabulary. This is the THIRD literal copy of that list (catalog, matrix `Type`, suite `Evidence Kind`) because `from_vocabulary` is deferred (quire-rs#146); deleting this test makes the duplication silent (FR-007) | Unit | P0 | FR-007-AC-3 | ✅ |
| TC-051 | Every entry declares at least one non-empty applicability rule drawn from the module's declared axes — an entry no rule can select is a definition the advisor never reaches (FR-007) | Unit | P0 | FR-007-AC-4 | ✅ |
| TC-052 | The engine loads the manifest with the catalog block present. `verification_catalog` is a quire-rs v0.29.0 key: against an older engine the top-level key is tolerated and silently ignored, so the module would look correct and contribute nothing (FR-007) | Unit | P0 | FR-007-AC-5 | ✅ |
| TC-053 | `verification_class` is exactly the four IADT values and `verification_method` exactly the catalog keys, both derived by the engine — and neither is separately declared here, which is the duplication FR-054-CON-4 forbids (FR-007) | Unit | P0 | FR-007-AC-6 | ✅ |
| TC-054 | Inspection, demonstration and agent-behaviour evaluation carry an evidence kind inside the declared `no_source_symbol` set, so a row verified that way is never reported as a status lie — CR-041 applied to the catalog (FR-007) | Unit | P0 | FR-007-AC-7 | ✅ |

## Option Permutation Matrix

The three constrained vocabularies (`Type`, `Priority`, `Status`) are
independent per-column `column_choices` asserts — no cross-column coupling —
so each-value coverage per column suffices; TC-001 additionally exercises a
mixed combination in one conforming document.

| Test Case | Type | Priority | Status | Expected Behavior |
|-----------|------|----------|--------|-------------------|
| TC-004 | Unit / Integration / E2E / Property | P1 (fixed) | 🚧 (fixed) | All four rows validate |
| TC-010 | Unit (fixed) | P0 / P1 / P2 / P3 / P4 | 🚧 (fixed) | All five rows validate |
| TC-008 | Unit (fixed) | P1 (fixed) | ✅ / ⚠️ / ❌ / 🚧 | All four rows validate |
| TC-001 | mixed | mixed | mixed | Conforming combination validates |
| TC-005 | Manual | P1 | 🚧 | Fails (`assert`, Type) |
| TC-011 | Unit | P5 | 🚧 | Fails (`assert`, Priority) |
| TC-009 | Unit | P1 | Done | Fails (`assert`, Status) |

## Constraint Boundary Tests

| Constraint | Boundary Type | Test Value | Test Case | Expected |
|------------|---------------|------------|-----------|----------|
| min_rows (required tables) | Min | 1 data row | TC-016 | pass |
| min_rows (required tables) | Below Min | 0 data rows (header only) | TC-016 | Error (`assert`) |
| Required table presence | Absent | Test Case Summary omitted | TC-002 | Error (`missing`) |
| Required table presence | Absent | Functional Requirement Coverage omitted | TC-003 | Error (`missing`) |
| Optional table presence | Absent | StR/US/NFR tables omitted | TC-014 | pass |
| Optional table presence | Present, wrong columns | renamed column | TC-015 | Error (`assert`) |
| min_rows (SpecReview Findings) | Below Min | 0 data rows (header only) | TC-019 | Error (`assert`) |
| FR-003-CON-1 | Process gate | enforcing module version published before ecosystem `tests.md` sweep + user sign-off | Inspection (plan gate, no TC) | violation |

## Edge Cases

| ID | Description | Related Req | Test Case | Risk if Untested |
|----|-------------|-------------|-----------|------------------|
| EC-001 | Empty `Traces To` cell (row exists, cell blank) | FR-003-AC-6 | TC-018 | Untraceable test rows pass silently |
| EC-002 | Decorated status marker (`✅ Complete`) in the Status column | FR-003-AC-5 | TC-009 | Legacy decorated markers keep drifting |
| EC-003 | Whitespace variants in Traces To lists (`FR-1, FR-2` legal; `FR-1 , FR-2` illegal) | FR-003-AC-6 | TC-012, TC-013 | Separator ambiguity across authors |
| EC-004 | Duplicate Test ID rows in the Test Case Summary | FR-003-AC-11 | TC-024 (blocked; see GAP-002) | Ambiguous record extraction by id |

## Coverage Gaps

| Gap ID | Description | Risk Level | Mitigation |
|--------|-------------|------------|------------|
| GAP-001 | Resolved 2026-08-04: FR-002 acceptance criteria now covered by planned TC-019..TC-023 | — | Closed via matrix expansion (SR-001 FND-002) |
| GAP-002 | FR-003-AC-11 (Test ID uniqueness) is normative but not machine-enforceable: quire-rs exposes no uniqueness assert (verified in `LocatorAssert`/`assert_eval`, 2026-08-04) | Low | External quire-rs capability request (follow-on to FR-033); TC-024 stays ⚠️ blocked until it ships |
