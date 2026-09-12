---
id: TM-900
title: "negative — a Status cell carrying the retired warning marker"
type: TestMatrix
expect: mapping.status-marker
because: "⚠️ was retired by CR-031: traceability.status classed it as nothing, so every row carrying it was exempt from the status-lie check by construction (quire-rs CR-083). The quoin:spec-matrix skill that still documents it is the defect, agent-ix/quoin#337."
---
# TM-900: negative — a Status cell carrying the retired warning marker

## Requirements Traceability

### Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Status |
|----------------|---------------------|------------|-----------------|
| FR-001 | FR-001-AC-1 | TC-001 | ✅ |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---------|-------|------|----------|-----------|--------|
| TC-001 | a row claiming a warning status | Unit | P0 | FR-001-AC-1 | ⚠️ partial |
