---
id: AN-001
title: "Fixture e2"
type: Anomaly
status: resolved
resolution: fixed
safety_impact: impacting
severity: major
---
# [AN-001] Fixture e2

## Description

The importer accepted a file whose checksum did not match.

## Fix Verification

| Kind | Target | Rationale |
|------|--------|-----------|
| Criterion | FR-001-AC-1 | The criterion now rejects a mismatching checksum. |
| Test | TC-001 | The regression test fails without the fix and passes with it. |
