---
id: TM-000
title: "Example repository matrix index"
type: TestMatrixIndex
---
<!-- TestMatrixIndex authoring skeleton (spec-artifacts-process). This is the
     ROOT of the matrix tree (CR-039). A repository past a certain size does not
     have one matrix; it has a tree, and this document indexes the module
     matrices while the detail lives one level down.

     Use this type for the root and `TestMatrix` for each leaf. The split is not
     cosmetic: an index mints NO test-case ids, because `trace_targets.test-case`
     binds `archetype: TestMatrix` and this is not one. Under the old typing the
     root was a minting document that minted nothing, and copying the module
     test cases up would give every TC two declaring matrices — after which a
     tracking tag binds to neither.

     Contract (manifest body_extraction asserts):
     - REQUIRED: `Requirements Traceability` (columns exactly
       Subsystem | Local Matrix), >= 1 row.
       `Local Matrix` is a relative link and is what makes the tree navigable;
       asserting the column is what makes a dropped cell visible. The
       requirements and status of a subsystem are read from `quire matrix`,
       never authored here.
     - OPTIONAL: `Integration Test Matrix` (id column `Integration ID`,
       ^INT-\d+$) and `Coverage Gaps` (id column `ID`, ^GAP-\d+$). A repository
       whose subsystems do not integrate has no INT rows, and an absent gap
       register and an empty one are different claims — requiring either would
       force an empty table.
     - Status columns elsewhere (e.g. `Integration Test Matrix`) keep the
       marker-first vocabulary: ✅ | ❌ | 🚧 | ⛔. -->
# TM-000: Example repository matrix index

## Requirements Traceability

| Subsystem | Local Matrix |
|-----------|--------------|
| Import | [import](./import/tests.md) |
| Storage | [storage](./storage/tests.md) |

## Integration Test Matrix

| Integration ID | Purpose | Target | Type | Test Cases | Status |
|----------------|---------|--------|------|------------|--------|
| INT-001 | Import writes through to the object store | object-store | service | IT-001 | ✅ |

## Coverage Gaps

| ID | Description | Risk Level | Mitigation |
|----|-------------|------------|------------|
| GAP-001 | Re-verification on read is unspecified, so no row can cover it | Low | Raised as FIND-001; a requirement is needed before a test |
