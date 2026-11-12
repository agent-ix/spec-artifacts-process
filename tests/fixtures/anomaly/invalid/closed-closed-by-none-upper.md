---
id: AN-001
title: "Fixture b4"
type: Anomaly
status: closed
resolution: fixed
closed_by: NONE
safety_impact: impacting
---
# [AN-001] Fixture b4

## Description

The importer accepted a file whose checksum did not match.

## Safety Impact Assessment

| Kind | Target | Impact | Rationale |
|------|--------|--------|-----------|
| Requirement | FR-001 | Affects | The anomaly shows FR-001 is not enforced. |
| Requirement | FR-001-AC-1 | Affects | The criterion is not met. |
| Hazard | HAZ-001 | Introduces | A corrupt artifact is accepted. |
