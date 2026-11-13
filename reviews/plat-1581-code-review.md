---
id: SR-20261113084033
title: "PLAT-1581 spec-artifacts-process PR148 code-review"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR148 @d95f76c over origin/main; spec_artifacts_process/{manifest.yaml,mappings.yaml,schemas/AnomalyFields.json,schemas/Anomaly.json,schemas/AnomalySeverity.json,schemas/anomaly-frontmatter.schema.json,semantic/main.tsp,skeletons/Anomaly.md}; tests/test_anomaly.py; tests/fixtures/anomaly/**"
review_set: subset
---

## Summary

Ticket: PLAT-1581. Code review of the FR-014 severity slice (commit ab153ed). Severity is a `frontmatter_field` locator with `assert: choices` of exactly minor/major/critical, required from `assessed` onward in both `AnomalyFields.json` (status-guarded) and the emitted `Anomaly.json`, with no default anywhere. The frontmatter-schema enum and the locator assert do not double-report: an out-of-vocabulary value (`high`, `Major`, `""`) yields exactly one finding at the severity line (probed and tested). A bare `severity:` (YAML null) yields the one `required` finding at the status line.

## Verdict

**PASS.** No defects in the severity slice. The vocabulary, the no-default rule, the status-guarded presence rule and the single-finding behaviour are correct and tested through `quire validate` and the mapped-record schema. FR-014-AC-18 (inspection) is asserted by `test_the_type_holds_no_who_when_or_verdict_field`, which pins the emitted property set.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |

## Examined scope

```yaml
scope:
- id: FR-014-AC-14
  path: spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md
  role: examined
  excerpt: 'The `Anomaly` `yield_pattern.match` carries a `severity` `frontmatter_field` locator (`required: false`) whose `assert` is `choices` of exactly `minor`, `major`, `critical`, and the manifest and `AnomalyFields.json` define no default for `severity`.'
- id: FR-014-AC-15
  path: spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md
  role: examined
  excerpt: For each of `assessed`, `resolved` and `closed`, a fixture with no `severity` fails, reported at the `status` line; an `identified` fixture with no `severity` validates.
- id: FR-014-AC-16
  path: spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md
  role: examined
  excerpt: A fixture whose `severity` is outside the vocabulary (including `high`, `Major` and the empty string) fails with exactly one finding, at the `severity` line.
- id: FR-014-AC-17
  path: spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md
  role: examined
  excerpt: Two fixtures identical except for one differing field (`safety_impact`, or the assessment rows) validate with the same `severity`, and no schema, locator or mapping of the `Anomaly` type computes `severity` from another field.
- id: FR-014-AC-18
  path: spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md
  role: examined
  excerpt: No field of the `Anomaly` type records who set `severity` or when.
```
