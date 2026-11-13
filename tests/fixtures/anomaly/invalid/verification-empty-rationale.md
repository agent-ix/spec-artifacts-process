---
id: AN-001
title: "Fixture verification-empty-rationale"
type: Anomaly
status: resolved
resolution: fixed
safety_impact: impacting
severity: major
---
# [AN-001] Fixture verification-empty-rationale

## Description

The importer accepted a file whose checksum did not match.

## Safety Impact Assessment

| Kind | Target | Impact | Rationale |
|------|--------|--------|-----------|
| Requirement | FR-001 | Affects | The anomaly shows FR-001 is not enforced. |
| Requirement | FR-001-AC-1 | Affects | The criterion is not met. |
| Hazard | HAZ-001 | Introduces | A corrupt artifact is accepted. |

## Fix Verification

| Kind | Target | Rationale |
|------|--------|-----------|
| Test | TC-001 |  |
