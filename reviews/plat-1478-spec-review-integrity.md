---
id: SR-20261112181937
title: "PLAT-1478 spec-artifacts-process PR142 spec-review integrity"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-artifacts-process PR142 @7205efb over origin/main 481a2b2; spec/functional/FR-009, FR-014, FR-015 edits, spec/tests.md"
review_set: subset
---

## Summary

Ticket: PLAT-1478. Integrity review of the FR-009, FR-014 and FR-015 edits
and of the spec/tests.md rows. `quire validate` was run over spec/tests.md
and the three FRs on both main and the PR head. Main is clean. The PR head
fails on spec/tests.md.

Clean units:

- The FR-014 owner-table row and the new Behavior bullet agree with the
  manifest and the schema.
- The FR-015 minimum-engine statement is accurate.
- TC ids are unique. TC-188 is new and is not reused.
- No stale PLAT-1476 references remain in spec/tests.md.

## Verdict

**CHANGES REQUESTED.** The PR breaks spec validation on spec/tests.md
(FND-001). FND-002 and FND-003 are wording-level.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The TC-188 Test Case Summary row (6 cells) is inserted into the Functional Requirement Coverage table (4 columns). `quire validate` on the PR head reports `spec/tests.md: line 165: [TestMatrix] 'functional_coverage': table row has 6 cell(s) but the header declares 4 [row-width]`, and main is clean. TC-188 is also missing from the Test Case Summary table. Move the row to follow TC-187 in `## Test Case Summary`. | spec/tests.md:165 |
| FND-002 | low | FR-009 adds a SHALL that the generator treats `*Fields.json` as hand-authored, but no acceptance criterion states it. FR-009-AC-6 still names only `*-frontmatter.schema.json`. Extend AC-6 to cover `*Fields.json` being neither reported nor removed. | spec/functional/FR-009-emitted-json-schemas.md:76-80 |
| FND-003 | low | FR-014-AC-9 is compound. One criterion carries four separately failing clauses: the manifest declaration, the `closed_by` locator, the schema shipping and surviving the generator, and the located finding. A failure cannot be attributed to one of them. Split it, or tag one test per clause. | spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:99 |

## Examined scope

```yaml
scope:
- id: FR-009
  path: spec/functional/FR-009-emitted-json-schemas.md
  role: examined
  excerpt: "It SHALL treat a file named `*Fields.json` the same way: these are the `record_validation` schemas of the YAML-extracted record (FR-014), not projections of a model."
- id: FR-014
  path: spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md
  role: examined
  excerpt: "The `Anomaly` archetype SHALL declare `record_validation: { schema: schemas/AnomalyFields.json, locate_absence_at: status }` and a `closed_by` `frontmatter_field` locator (`required: false`) in its `yield_pattern.match`."
- id: FR-014-AC-9
  path: spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md
  role: examined
  excerpt: "The `Anomaly` archetype declares `record_validation` with schema `schemas/AnomalyFields.json` and `locate_absence_at: status`, with a `closed_by` locator; the schema file ships beside the emitted schemas and is not removed by the schema generator; a `closed` anomaly with no `closed_by` and no `resolution` is reported once per missing field at the `status` line."
- id: FR-015
  path: spec/functional/FR-015-anomaly-safety-impact-assessment.md
  role: examined
  excerpt: "requires quire-rs >= 0.58.0 (quire CLI >= 0.42.0), as older engines reject `kind_column` and `record_validation`"
- id: TM-001
  path: spec/tests.md
  role: examined
  excerpt: "| TC-187 | Every diagnostic from those runs carries a line; for an absence the line is that of the `status` field. | Unit | P1 | NFR-001-AC-2 | ❌ blocked: quire CLI prints no line for a bundle finding |"
```

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | - |
| FND-002 | fixed | - |
| FND-003 | fixed | - |
