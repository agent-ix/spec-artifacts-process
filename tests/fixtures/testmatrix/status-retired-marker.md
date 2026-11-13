---
id: TM-016
title: "A retired marker is rejected"
type: TestMatrix
---
# TM-016: A retired marker is rejected

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---------|-------|------|----------|-----------|--------|
| TC-001 | Bare | Unit | P0 | FR-003-AC-5 | ✅ |
| TC-002 | Decorated | Unit | P0 | FR-003-AC-5 | ✅ Complete |
| TC-003 | The retired marker | Unit | P0 | FR-003-AC-5 | ⚠️ scale evidence deferred |
| TC-004 | Failing | Unit | P0 | FR-003-AC-5 | ❌ |
| TC-005 | Planned | Unit | P0 | FR-003-AC-5 | 🚧 |
| TC-006 | Retired | Unit | P0 | FR-003-AC-5 | ⛔ RETIRED — render removed |
