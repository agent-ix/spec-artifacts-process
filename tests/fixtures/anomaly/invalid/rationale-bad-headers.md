---
id: AN-001
title: "Fixture rationale bad headers"
type: Anomaly
status: assessed
safety_impact: impacting
severity: major
---
# [AN-001] Fixture rationale bad headers

## Description

The importer accepted a file whose checksum did not match.

## Safety Impact Assessment

| Kind | Target | Impact | Rationale |
|------|--------|--------|-----------|
| Requirement | FR-001 | Affects | The anomaly shows FR-001 is not enforced. |
| Requirement | FR-001-AC-1 | Affects | The criterion is not met. |
| Hazard | HAZ-001 | Introduces | A corrupt artifact is accepted. |

## Release Rationale

| Name | Reason |
|------|--------|
| Morgan Reyes | The checksum path is not on a safety function and the operator procedure catches the case until the next release. |
