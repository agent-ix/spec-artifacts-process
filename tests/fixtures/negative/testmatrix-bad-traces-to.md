---
id: TM-901
title: "negative — a Traces To cell the pattern rejects"
type: TestMatrix
expect: mapping.trace-tokens
because: "a semicolon is not the declared separator; an ambiguous separator makes one authored list mean two things"
---
# TM-901: negative — a Traces To cell the pattern rejects

## Requirements Traceability

### Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Coverage Status |
|----------------|---------------------|------------|-----------------|
| FR-001 | FR-001-AC-1 | TC-001 | ✅ |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---------|-------|------|----------|-----------|--------|
| TC-001 | a row separating its traces with semicolons | Unit | P0 | FR-001-AC-1; FR-001-AC-2 | ✅ |
