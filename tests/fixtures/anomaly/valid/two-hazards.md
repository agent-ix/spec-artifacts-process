---
id: AN-001
title: "Fixture two hazards"
type: Anomaly
status: assessed
safety_impact: impacting
severity: major
---
# [AN-001] Fixture two hazards

## Description

The importer accepted a file whose checksum did not match.

## Safety Impact Assessment

| Kind | Target | Impact | Rationale |
|------|--------|--------|-----------|
| Hazard | HAZ-001 | Introduces | A corrupt artifact is accepted. |
| Hazard | HAZ-002 | Affects | A second corrupt-artifact path. |
