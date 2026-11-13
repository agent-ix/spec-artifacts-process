---
id: AN-001
title: "Fixture assessed with resolution"
type: Anomaly
status: assessed
resolution: fixed
safety_impact: impacting
severity: major
---
# [AN-001] Fixture assessed with resolution

## Description

The importer accepted a file whose checksum did not match.

## Safety Impact Assessment

| Kind | Target | Impact | Rationale |
|------|--------|--------|-----------|
| Requirement | FR-001 | Affects | The anomaly shows FR-001 is not enforced. |
| Requirement | FR-001-AC-1 | Affects | The criterion is not met. |
| Hazard | HAZ-001 | Introduces | A corrupt artifact is accepted. |
