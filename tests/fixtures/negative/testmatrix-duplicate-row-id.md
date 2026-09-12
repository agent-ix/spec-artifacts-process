---
id: TM-902
title: "negative — two Test Case Summary rows sharing one id"
type: TestMatrix
expect: mapping.duplicate-row-id
because: "a duplicated Test ID makes record extraction by id ambiguous and a tracking tag bind to neither row"
---
# TM-902: negative — two Test Case Summary rows sharing one id

## Requirements Traceability

### Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Status |
|----------------|---------------------|------------|-----------------|
| FR-001 | FR-001-AC-1 | TC-001 | ✅ |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---------|-------|------|----------|-----------|--------|
| TC-001 | the first row claiming this id | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-001 | the second row claiming this id | Unit | P0 | FR-001-AC-2 | ✅ |
