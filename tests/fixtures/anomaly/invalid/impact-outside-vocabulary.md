---
id: AN-001
title: "Fixture k2"
type: Anomaly
status: assessed
safety_impact: impacting
severity: major
---
# [AN-001] Fixture k2

## Description

The importer accepted a file whose checksum did not match.

## Safety Impact Assessment

| Kind | Target | Impact | Rationale |
|------|--------|--------|-----------|
| Requirement | FR-001 | Breaks | Not a member of the vocabulary. |
| Hazard | HAZ-001 | Introduces | A corrupt artifact is accepted. |
