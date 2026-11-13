---
id: AN-001
title: "Fixture nfr"
type: Anomaly
status: assessed
safety_impact: impacting
severity: major
---
# [AN-001] Fixture nfr

## Description

The importer accepted a file whose checksum did not match.

## Safety Impact Assessment

| Kind | Target | Impact | Rationale |
|------|--------|--------|-----------|
| Requirement | NFR-002 | Affects | The latency requirement is bypassed by the failure. |
| Requirement | NFR-002-AC-1 | Affects | The criterion is not met. |
