---
id: AN-001
title: "Fixture severity capitalised"
type: Anomaly
status: assessed
safety_impact: impacting
severity: Major
---
# [AN-001] Fixture severity capitalised

## Description

The importer accepted a file whose checksum did not match.

## Safety Impact Assessment

| Kind | Target | Impact | Rationale |
|------|--------|--------|-----------|
| Requirement | FR-001 | Affects | The anomaly shows FR-001 is not enforced. |
| Requirement | FR-001-AC-1 | Affects | The criterion is not met. |
| Hazard | HAZ-001 | Introduces | A corrupt artifact is accepted. |
