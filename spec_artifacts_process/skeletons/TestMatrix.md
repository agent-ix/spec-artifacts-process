---
id: TM-001
title: "Example module test matrix"
type: TestMatrix
---
<!-- TestMatrix authoring skeleton (spec-artifacts-process). This is the LEAF
     of the matrix tree: the document that declares test cases. The ROOT of a
     repository with more than one matrix is a `TestMatrixIndex` instead —
     see that skeleton.

     Contract (manifest body_extraction asserts, validated by `quire validate`):
     - REQUIRED: `Functional Requirement Coverage` (columns exactly
       Functional Req | Acceptance Criteria | Test Cases | Coverage Status)
       and `Test Case Summary` (columns exactly
       Test ID | Title | Type | Priority | Traces To | Status), each with
       >= 1 data row.
     - OPTIONAL: Stakeholder Requirement Coverage, User Story Coverage,
       Non-Functional Requirement Coverage. Absent is fine; present is asserted.
     - `Priority` is an OPTIONAL COLUMN (CR-018): a matrix that authors no
       priority anywhere omits the whole column rather than inventing values.
       When present, values are P0..P4.
     - `Test ID` matches ^(TC|IT)(-[A-Za-z0-9]+)*-\d+[A-Za-z0-9]*(-[A-Za-z0-9]+)*$
       — segmented forms like TC-060-01 and TC-SB-001 are legal; TC1, tc-001
       and TCX-001 are not. The prefix set is TC and IT because those are the
       only artifact types any module mints test ids for.
     - `Type` is one of Unit | Integration | E2E | Property | Fuzz | Benchmark |
       Static | Compile | Snapshot | Manual | Eval | Inspection | Analysis |
       Demonstration. What kind of testing a row records is this column's job.
     - `Status` is a marker FIRST, optionally followed by the note that says
       why: ✅ | ❌ | 🚧 | ⛔. `⚠️` IS NOT VALID and is not an oversight: it was
       retired because `traceability.status` classed it as nothing, so every row
       carrying it was exempt from the status-lie check by construction. If a
       skill or a template tells you `⚠️` is a status, that is the defect
       (agent-ix/quoin#337), not this contract.
     - `Traces To` is a comma-separated list of requirement ids; a same-prefix
       continuation (`FR-001-AC-2, -AC-3`) and a slash enumeration
       (`FR-016-AC-1/2/3`) both mean the expanded list. A lone `-` is the
       explicit no-trace form and is for RETIRED rows: a live row that traces
       to nothing is what a traceability matrix exists to catch. Never trace to
       another TC. -->
# TM-001: Example module test matrix

## Requirements Traceability

### Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Coverage Status |
|----------------|---------------------|------------|-----------------|
| FR-001 | FR-001-AC-1 | TC-001 | ✅ Complete |
| FR-001 | FR-001-AC-2 | TC-002 | ✅ Complete |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---------|-------|------|----------|-----------|--------|
| TC-001 | A matching digest persists the artifact | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-002 | A mismatched digest rejects the import and names both digests | Unit | P0 | FR-001-AC-2 | ✅ |
| TC-003 | Import throughput holds at the declared threshold | Benchmark | P2 | NFR-001-AC-1 | 🚧 not yet run at scale |
| TC-004 | Digest computed before any transform | Unit | P1 | - | ⛔ superseded by TC-001 |
