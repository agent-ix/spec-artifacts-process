---
id: TM-002
title: "Matrix with no Priority column"
type: TestMatrix
---
# TM-002: Matrix with no Priority column

## Requirements Traceability

### Stakeholder Requirement Coverage

| Stakeholder Req | Trace to US/FR | Test/Validation | Coverage Status |
|-----------------|----------------|-----------------|-----------------|
| StR-001 | US-001, FR-003 | Review | ✅ Complete |

### User Story Coverage

| User Story | Acceptance Criteria | Test Cases | Coverage Status |
|------------|---------------------|------------|-----------------|
| US-001 | US-001-EX-1 | TC-001 | 🚧 Planned |

### Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Coverage Status |
|----------------|---------------------|------------|-----------------|
| FR-003 | FR-003-AC-1 | TC-001 | 🚧 Planned |

### Non-Functional Requirement Coverage

| Non-Functional Req | Verification Method | Evidence/Test Cases | Status |
|--------------------|---------------------|---------------------|--------|
| NFR-001 | Inspection | TC-001 | 🚧 |

## Test Case Summary

| Test ID | Title | Type | Traces To | Status |
|---------|-------|------|-----------|--------|
| TC-001 | Unit case | Unit | FR-003-AC-1 | ✅ |
| TC-INT-010 | Integration case | Integration | IT-001-SC-2 | ⚠️ |
| TC-INT-010a | Lettered variant | E2E | US-001, FR-003-CON-1 | ❌ |
| TC-002 | Property case | Property | NFR-001 | 🚧 |
