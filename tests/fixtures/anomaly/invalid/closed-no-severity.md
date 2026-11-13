---
id: AN-001
title: "Fixture closed no severity"
type: Anomaly
status: closed
resolution: not-a-defect
closed_by: "Dana Lee"
safety_impact: impacting
---
# [AN-001] Fixture closed no severity

## Description

The importer accepted a file whose checksum did not match.

## Safety Impact Assessment

| Kind | Target | Impact | Rationale |
|------|--------|--------|-----------|
| Requirement | FR-001 | Affects | The anomaly shows FR-001 is not enforced. |
| Requirement | FR-001-AC-1 | Affects | The criterion is not met. |
| Hazard | HAZ-001 | Introduces | A corrupt artifact is accepted. |
