---
id: SR-20261102086818
title: "Code review of PLAT-1415/PLAT-1416 — Anomaly archetype, record schema and fixtures"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process@94e98ba over origin/main 7c15a5f; spec_artifacts_process/manifest.yaml, spec_artifacts_process/semantic/main.tsp, spec_artifacts_process/schemas/Anomaly*.json, Assessment*.json, ClosedBy.json, SafetyImpact.json, anomaly-frontmatter.schema.json, spec_artifacts_process/mappings.yaml, spec_artifacts_process/mappings.schema.json, spec_artifacts_process/skeletons/Anomaly.md, spec_artifacts_process/examples/Anomaly.record.json, tests/fixtures/anomaly/**, tests/test_anomaly.py, tests/support/reference_mapping.py, tests/test_manifest.py, tests/test_skeletons_and_roles.py"
review_set: subset
---
# SR-20261102086818: Code review of PLAT-1415/PLAT-1416 — Anomaly archetype

## Summary

Ticket: PLAT-1415 (with PLAT-1416). PR: spec-artifacts-process#140, head `94e98ba`, base
`origin/main` `7c15a5f`. Python lane. No Rust or React files are in the diff.

What I ran:

- `pytest tests/test_anomaly.py`: 54 passed and 5 xfailed. All 5 xfails are the strict
  `test_dangling_and_mismatched_targets_fail_validation_in_the_corpus` cases.
  `tests/test_markdown_mappings.py -k Anomaly`: 4 passed, which covers skeleton to record,
  golden record reproduction, CRLF, and dropped keys. The remaining failures in
  `test_skeletons_and_roles.py` / `test_markdown_mappings.py` come from the environment.
  The python `quire` wheel is missing, `make build` fails, and semantic-core 0.3.0 does not
  resolve the 0.3.3 `$ref` for Standard. None of them involves Anomaly.
- Schema projection: `npm run check` with the local `node_modules` (semantic-core 0.3.0,
  @typespec 1.15.0) reproduces every new Anomaly schema byte-for-byte. It reports only
  `Provenance.json` and `Standard.json`, and it reports the same two on main with the same
  toolchain, so that drift predates this PR. The new schemas `$ref` only module-local
  schemas, so the semantic-core version does not affect them. Nothing about the committed
  generated schemas looks suspicious.
- Probes: I mapped every fixture and validated it against `Anomaly.json`. Each invalid
  fixture fails for its intended reason only. The dangling/mismatch fixtures produce no
  record error, which is correct, because reference resolution belongs to the engine.
  `quire validate` over the corpus with spec-artifacts-iso and spec-objects-safety accepts
  `dangling-requirement.md` with exit 0. That confirms the xfail reason for quire 0.56.

## Verdict

**CHANGES REQUESTED.** The archetype, the conditional record schema, the mapping and the
fixtures are correct. The tests exercise the real artifacts with no mocks. Four test-intent
defects remain. The highest is a test tagged NFR-001-AC-1 that asserts the current engine
gap as passing behaviour. The xfail stand-ins for FR-015-AC-5/6 are strict, which is
honest, but they are incomplete. The `AssessmentTarget` pattern also assumes ids contain a
hyphen, and FR-015 says no hazard id pattern is assumed.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | `test_fixture_c_document_layer_defect_is_reported_with_its_line` is tagged NFR-001-AC-1. Fixture (c) injects three defects: a dangling Requirement row, a kind-mismatched Hazard row and an empty Rationale. The test asserts `len(found) == 1`, but NFR-001-AC-1 requires exactly one diagnostic per injected defect, which is three. So it passes while the AC is unmet, and it will fail once the engine reports references. Assert the Rationale diagnostic in a passing test, and assert the three located diagnostics in a strict xfail. | tests/test_anomaly.py:439-445 |
| FND-002 | medium | The strict-xfail stand-ins for FR-015-AC-5/AC-6 assert only `returncode != 0`. AC-5 requires a dangling-reference diagnostic that names the id and its row, and AC-6 requires a kind-mismatch diagnostic. There is no positive control: a valid impacting anomaly in the same copied corpus and harness that is expected to pass. A module-load error or any unrelated defect would XPASS the case and flip the strict marker, with nothing proving the reference diagnostic. Add the positive control and assert the diagnostic text, id and line. | tests/test_anomaly.py:338-381 |
| FND-003 | medium | The test tagged FR-015-AC-4 validates only the corpus documents (FR-001, HAZ-001..003). It never validates the `impacting` anomaly inside that corpus with spec-artifacts-iso and spec-objects-safety loaded, which is what the AC states. That run passes today: I copied `valid/impacting-all-targets.md` into the corpus and got exit 0. The real AC-4 assertion could therefore be written now. | tests/test_anomaly.py:310-335 |
| FND-004 | medium | The `AssessmentTarget` pattern `^[A-Za-z][A-Za-z0-9_]*(-[A-Za-z0-9_]+)+$` requires at least one hyphen. FR-015 says no hazard id pattern is assumed, and spec-objects-safety constrains no hazard id. A hazard with id `H1` or `HAZARD_1` is therefore rejected as a record-schema pattern error rather than resolved or reported by the engine. Loosen it to a non-empty token without whitespace, or a single id shape that does not require a hyphen. | spec_artifacts_process/semantic/main.tsp AssessmentTarget; spec_artifacts_process/schemas/AssessmentTarget.json |
| FND-005 | low | Several parametrised negatives assert only that some error exists. The FR-014-AC-5 and FR-015-AC-7 cases use `!= []`. The FR-014-AC-6 case uses `"closedBy" in e.message or e.validator == "not"`, which any `not` error satisfies, including the resolution rule. They pass on an unrelated error. Pin `absolute_path` and `validator`, as the FR-014-AC-4 tests already do. | tests/test_anomaly.py:180-201,280-291 |
| FND-006 | low | An `impacting` or `none` anomaly at `assessed` or later with no section gets `'assessment' is a required property` twice: once from the status rule and once from the safety-impact rule. That is one defect with two diagnostics, which works against NFR-001's one-diagnostic-per-defect intent. Probe output on assessed-no-section, resolved-no-section and closed-no-section shows it. | spec_artifacts_process/semantic/main.tsp Anomaly allOf; spec_artifacts_process/schemas/Anomaly.json |
