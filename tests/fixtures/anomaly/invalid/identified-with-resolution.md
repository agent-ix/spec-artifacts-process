---
id: AN-001
title: "Fixture c4"
type: Anomaly
status: identified
resolution: fixed
safety_impact: unassessed
---
# [AN-001] Fixture c4

## Description

The importer accepted a file whose checksum did not match.

## Fix Verification

| Kind | Target | Rationale |
|------|--------|-----------|
| Criterion | FR-001-AC-1 | The criterion now rejects a mismatching checksum. |
| Test | TC-001 | The regression test fails without the fix and passes with it. |
