---
id: SR-20261112181936
title: "PLAT-1478 spec-artifacts-process PR142 gap-analysis"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process PR142 @7205efb over origin/main 481a2b2; FR-014, FR-015, NFR-001 against tests/test_anomaly.py, manifest.yaml, AnomalyFields.json; engine specs quire-rs origin/main FR-033-AC-18, FR-049-AC-19..22, FR-069-AC-21..28"
review_set: subset
---

## Summary

Ticket: PLAT-1478. This is a planless gap analysis. Plan completion: not
assessed.

`quire matrix --scope <worktree> --format tsv` was run with ambient module
discovery. On the PR head FR-014-AC-9 is `untagged`, which is new. The
NFR-001-AC-1 and NFR-001-AC-2 ACs are tagged. FR-009 ACs 2, 3, 4, 6, 7, 8 and
10 are untagged on both main and the PR head, so the PR did not change them.

The coder's deviation claims were checked against the engine and CLI specs.

- **TC-187 xfail.** quire-rs v0.58.0 has `BundleFinding.line: Option<usize>`
  (FR-049-AC-19). quire-cli origin/main (1df1208) `surface_bundle` formats
  `path: message [reason]` only. The xfail reason is true, and a bundle run of
  fixture (c) prints both reference findings without a line.
- **Fixture (b).** `safety_impact: unassessed` is located at its own line, and
  the missing assessment at the `status:` line. This matches FR-069-AC-25
  (a present-but-invalid scalar is reported at its value's line) and NFR-001,
  which allows the `status` line only for an absence.
- **Minimum engine.** quire-rs v0.57.0 has no `record_validation`. v0.58.0 has
  it. quire-cli v0.42.0's Cargo.lock pins quire-rs 0.58.0, and v0.41.0's pins
  0.57.0. The statement "quire-rs >= 0.58.0 (quire CLI >= 0.42.0)" is accurate.
- **Shipping.** `AnomalyFields.json` ships through the pyproject
  `schemas/**/*.json` include and the npm `schemas/` payload.

## Verdict

**CHANGES REQUESTED.** Two problems. FR-014-AC-9 is marked ✅ Complete but no
test is tagged with it. FR-015 now names `AnomalyFields.json` as the owner of
row rules that it does not carry.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-014-AC-9 (TC-188) is untagged in `quire matrix`, and no test names it, yet spec/tests.md marks both rows ✅ Complete. No test asserts its clauses under its id: the manifest declaring `record_validation` and the `closed_by` locator, and `AnomalyFields.json` shipping and not being removed by the generator. Its last clause is asserted, but only by a test tagged NFR-001. | spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:99; spec/tests.md:165-166; tests/test_anomaly.py |
| FND-002 | medium | FR-015's owner table now gives `AnomalyFields.json` the row "Section and rows required by `status` and `safety_impact`", "reported at the `status` line". The schema carries no row rules: `none` requires exactly one `None` row, and `impacting` requires a non-`Unaffected` Requirement or Hazard row. The manifest comment says those rules are the emitted schema's. `quire validate` exits 0 on impacting-only-unaffected, impacting-only-impact-none, impacting-row-impact-none, none-with-affects and none-with-hazard-row. Either split the row (section presence goes to record_validation, row shape to Anomaly.json) or add the rules to AnomalyFields.json. | spec/functional/FR-015-anomaly-safety-impact-assessment.md:28; spec_artifacts_process/manifest.yaml:95-99 |

## Examined scope

```yaml
scope:
- id: FR-014-AC-4
  path: spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md
  role: examined
  excerpt: "A `closed` fixture with no `closed_by` fails; a `closed` fixture with `closed_by` of `TBD`, `unknown`, `n/a`, `none`, `-` or empty fails in any letter case; the same fixture with a non-placeholder value passes."
- id: FR-014-AC-5
  path: spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md
  role: examined
  excerpt: "A fixture with `status` of `resolved` or `closed` and no `resolution` fails; a `resolved` fixture with `resolution` other than `fixed` fails; a fixture with `status` of `identified` or `assessed` and a `resolution` fails."
- id: FR-014-AC-6
  path: spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md
  role: examined
  excerpt: "A fixture with `status` other than `closed` that carries `closed_by` fails."
- id: FR-014-AC-9
  path: spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md
  role: examined
  excerpt: "The `Anomaly` archetype declares `record_validation` with schema `schemas/AnomalyFields.json` and `locate_absence_at: status`, with a `closed_by` locator; the schema file ships beside the emitted schemas and is not removed by the schema generator; a `closed` anomaly with no `closed_by` and no `resolution` is reported once per missing field at the `status` line."
- id: FR-015-AC-3
  path: spec/functional/FR-015-anomaly-safety-impact-assessment.md
  role: examined
  excerpt: "For each of `assessed`, `resolved` and `closed`, a fixture with no `## Safety Impact Assessment` section fails validation, and a fixture with `safety_impact: unassessed` fails validation."
- id: FR-015-AC-7
  path: spec/functional/FR-015-anomaly-safety-impact-assessment.md
  role: examined
  excerpt: "An `impacting` anomaly whose only rows are `Unaffected` fails validation; a `none` anomaly with one `None` row ... validates; ..."
- id: NFR-001-AC-1
  path: spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md
  role: examined
  excerpt: "Validating fixture (a), (b) or (c) yields exactly one diagnostic per injected defect in that fixture."
- id: NFR-001-AC-2
  path: spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md
  role: examined
  excerpt: "Every diagnostic from those runs carries a line; for an absence the line is that of the `status` field."
- id: FR-069-AC-24
  path: quire-rs spec/functional/FR-069-semantic-module-contract-at-load.md
  role: context_only
  excerpt: "A `required` error (outright or from an `if`/`then` conditional) is located at the document line of the value the `locate_absence_at` locator located"
- id: FR-069-AC-25
  path: quire-rs spec/functional/FR-069-semantic-module-contract-at-load.md
  role: context_only
  excerpt: "A present-but-invalid scalar is located at its value's line; ... an error with no property of its own (record root ...) at the `locate_absence_at` line."
- id: FR-049-AC-19
  path: quire-rs spec/functional/FR-049-verification-reference-integrity.md
  role: context_only
  excerpt: "`BundleFinding` has an optional `line`; a `dangling-trace-reference` finding carries `Some(line)` ..."
```
