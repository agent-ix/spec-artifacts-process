---
id: AN-001
title: "Fixture e3"
type: Anomaly
status: closed
resolution: fixed
closed_by: "Dana Lee"
safety_impact: impacting
severity: major
---
# [AN-001] Fixture e3

## Description

The importer accepted a file whose checksum did not match.

## Fix Verification

| Kind | Target | Rationale |
|------|--------|-----------|
| Criterion | FR-001-AC-1 | The criterion now rejects a mismatching checksum. |
| Test | TC-001 | The regression test fails without the fix and passes with it. |
