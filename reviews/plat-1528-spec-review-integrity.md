---
id: SR-20261113084031
title: "Integrity review of FR-016 anomaly release rationale (spec-artifacts-process#147)"
type: SpecReview
analysis: integrity
review_set: subset
scope: "agent-ix/spec-artifacts-process; PR #147 (git diff origin/main...plat-1528-spec-sap at 2b6d5e3): spec/functional/FR-016-anomaly-release-rationale.md, spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md, spec/spec.md, spec/functional/index.md"
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-016"
    type: references
---

# Integrity review of FR-016 anomaly release rationale (spec-artifacts-process#147)

## Summary

Ticket: PLAT-1528. Method: spec-review/spec-integrity-analysis, scoped to `git diff origin/main...HEAD` of agent-ix/spec-artifacts-process#147 at 2b6d5e3.
Read against FR-011, FR-014 and FR-015 on main and the consuming side in agent-ix/quoin#857 (FR-162, FR-163, FR-164, NFR-035).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | NFR-001's scope now covers FR-016's checks, but its measurement table and AC-1/AC-2 still range over fixtures (a)-(c) only, none of which carries a Release Rationale. FR-016-AC-6 asserts the three findings in one run but not that each carries a line, so no criterion measures NFR-001's location half for FR-016. Add the AC-6 document as fixture (d) of NFR-001's table and AC-1/AC-2. | spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md:51 |
| FND-002 | low | The Dependencies section lists FR-009 and FR-012 as upstream, but the frontmatter `relationships` carries no `depends_on` edge to either, so the dependency graph omits them. Add both edges or drop them from Dependencies. | spec/functional/FR-016-anomaly-release-rationale.md:5-13 |
| FND-003 | low | AC-4 omits the 'in any letter case' and the passing counterpart that AC-3 states for `Author`, so a case-sensitive or over-broad `Rationale` check passes it. Add both. | spec/functional/FR-016-anomaly-release-rationale.md:79 |
| FND-004 | low | AC-5 states no location, while every other FR-016 negative does and NFR-001 now requires each defect located. Name the line (the section heading for wrong headers or no row). | spec/functional/FR-016-anomaly-release-rationale.md:80 |

## Verdict

Changes requested: one medium (NFR-001's widened scope is not measured for FR-016) and three low.

Checked and clean: each Behavior statement is atomic and backed by an AC (AC-1/2 status rule, AC-3/4 value rules, AC-5 shape, AC-6 one-pass, AC-7 mapping, AC-8 no default or computation, AC-9 no attribution fields, AC-10 no effect on other findings); the index entry and spec.md scope line match the FR; NFR-001's new `constrains` edge resolves; `quire validate` reports no diagnostic on the four changed files.

Examined (role examined): FR-016, FR-016-AC-1, FR-016-AC-2, FR-016-AC-3, FR-016-AC-4, FR-016-AC-5, FR-016-AC-6, FR-016-AC-7, FR-016-AC-8, FR-016-AC-9, FR-016-AC-10, NFR-001, NFR-001-AC-1, NFR-001-AC-2.
Context only: FR-014, FR-015.

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-005 | low | The new `release_rationale` locator (`required: false`) statement has no criterion; FR-014-AC-10 checks the analogous `closed_by` locator. Add an AC that the `yield_pattern.match` carries it with `required: false`. | spec/functional/FR-016-anomaly-release-rationale.md:58 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Fixed in f5b30a4; after-text: Validating fixture (a), (b), (c) or (d) yields exactly one diagnostic per injected defect in that fixture. |
| FND-002 | fixed | Fixed in f5b30a4; after-text:   - target: "ix://agent-ix/spec-artifacts-process/FR-009"     type: "depends_on"   - target: "ix://agent-ix/spec-artifacts-process/FR-012"     type: "depends_on" |
| FND-003 | fixed | Fixed in f5b30a4; after-text: A row whose `Rationale` is empty, or `TBD`, `unknown`, `n/a`, `none` or `-` in any letter case, fails validation, at the row's line; the same row with a non-placeholder `Rationale` passes. |
| FND-004 | fixed | Fixed in f5b30a4; after-text: A section whose headers are not exactly `Author \| Rationale`, or that has no row, fails validation, at the section heading line. |
| FND-005 | fixed | Fixed in e3e4bb8; after-text: \| FR-016-AC-11 \| The `Anomaly` `yield_pattern.match` carries a `release_rationale` locator with `required: false`, and `AnomalyFields.json` names the property `release_rationale`. \| Test \| |
