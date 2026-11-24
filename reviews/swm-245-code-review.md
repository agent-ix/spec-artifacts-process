---
id: SR-913
title: "Code review — RoleSpec and Rubric archetypes (PR 165)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR165 head 0f6579d; spec_artifacts_process/manifest.yaml, spec_artifacts_process/mappings.yaml, spec_artifacts_process/schemas/RoleSpecFields.json, spec_artifacts_process/schemas/role-spec-frontmatter.schema.json, spec_artifacts_process/schemas/rubric-frontmatter.schema.json, spec_artifacts_process/semantic/main.tsp, spec_artifacts_process/skeletons/RoleSpec.md, spec_artifacts_process/skeletons/Rubric.md, tests/test_role_spec.py, tests/fixtures/roles/**, tests/support/reference_mapping.py"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-artifacts-process/FR-020", type: references }
  - { target: "ix://agent-ix/spec-artifacts-process/FR-021", type: references }
  - { target: "ix://agent-ix/spec-artifacts-process/FR-022", type: references }
  - { target: "ix://agent-ix/spec-artifacts-process/FR-023", type: references }
  - { target: "ix://agent-ix/spec-artifacts-process/US-004", type: references }
---

# SR-913: Code review — RoleSpec and Rubric archetypes (PR 165)

## Summary

Ticket: SWM-245. This review covers PR 165 at head 0f6579d. The contract is FR-020 to FR-023 and US-004 on origin/main. The diff is YAML, JSON Schema, TypeSpec and Python tests. The review used the Python lane and the repo's own test idiom: plain functions with `pytest.mark.trace`.

Evidence:

- `tests/test_role_spec.py` passes 65 of 65 on quire-cli 0.46.0 (the pinned version, engine 0.61.0) and on 0.52.1 (engine 0.62.2).
- The four suites named in the PR pass 185 of 185, and ruff is clean.
- Every negative fixture was run by hand and its diagnostics read.
- The deviations were checked against quire-rs origin/main sources.

The owner's intent is that the lint fails when a rule has no evaluation or a reference dangles. As shipped, nothing fails in either case. A dangling reference is only a warning under `--okf` (exit 0) and is not checked at all by plain `quire validate`. A disallowed link verb is a warning with exit 0. Part of this can be fixed in the module now. The rest needs named engine capabilities.

## Verdict

**FAIL**: three high findings.

1. A dangling reference never fails, although the module can make it fail under `--okf` today.
2. FR-020-AC-12 is tagged as covered but its "fails" clause does not hold.
3. The enum and pattern vocabularies are declared in three to five places, which violates FR-020-AC-9. Part of that can be removed now.

What is sound:

- The table shapes, `{id}`/`{version}` interpolation, closed enums and record_validation conditionals all work.
- The minder fixture is byte-identical to dev-team `docs/examples/minder-role-spec.md`.
- Every existing negative fixture differs from the positive fixture in exactly the intended cell, and fails with a diagnostic for that cell.
- The rubric version and slug resolution works.
- The pre-existing failures in `test_skeletons_and_roles.py` and `test_semantic_manifest.py` are pre-existing: the Python `quire` wheel 0.60.0 rejects `traceability.trace_tags.formalizes`, which is already on origin/main. One exception is FND-004.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | A dangling reference never fails. FR-021 says an evaluation naming an undefined rule "is a dangling reference and fails". Plain `quire validate` (the FR-022-AC-1 gate command) does not check document references at all. `quire validate --okf` reports `dangling-trace-reference` as a warning and exits 0. The module can declare `grammar_severity: {"trace:dangling-trace-reference": error}`, and then `--okf` exits 3 on the dangling-rule corpus and 0 on the valid corpus (verified on 0.46.0 and 0.52.1). That key is module-wide, but it only tightens OKF posture, because the Strict posture already errors. The tests assert only that the warning text is present. | spec_artifacts_process/manifest.yaml:1287-1326, tests/test_role_spec.py:353, tests/test_role_spec.py:375 |
| FND-002 | high | FR-020-AC-12 is tagged but does not hold. The AC says a `RoleSpec` with any other relationship verb fails. `bad-link-verb.md` and `rubric-bad-link-verb.md` exit 0 with a `disallowed-edge-type` warning. The engine hard-codes this as a warning (quire-rs src/validate_document.rs:797-805) and has no severity key, so the module cannot raise it. `quire validate --strict` exits 3 on both fixtures and 0 on the positive fixtures, but the tests do not pin that, and the PR records the AC as covered. | tests/test_role_spec.py:247, tests/test_role_spec.py:436 |
| FND-003 | high | The vocabularies have more than one home, which violates FR-020-AC-9. The evidence-source list is written twice in the manifest (`metrics` and `evaluations` column_choices) and again as the TypeSpec `EvidenceSource` enum, projected to schemas/EvidenceSource.json. Method, cadence, comparator and direction are in both the manifest and TypeSpec. `RoleSpecFields.json` restates deterministic/judgement, evaluator/director/team-retro, tick, the query-reference regex and the rubric-reference regex. The query-reference regex appears five times (manifest Query and Trigger, RoleSpecFields.json, TypeSpec QueryRef, skeleton). The two in-manifest copies can be removed now with YAML anchors, which quire loads (verified). The manifest-versus-TypeSpec copies need an engine capability. | spec_artifacts_process/manifest.yaml:729, spec_artifacts_process/manifest.yaml:775, spec_artifacts_process/semantic/main.tsp, spec_artifacts_process/schemas/RoleSpecFields.json:13-28 |
| FND-004 | medium | `allowed_links` names `satisfies` and `implements`, but neither is registered in this module's `edge_types`, and neither is mapped to an external owner. Every validate run prints four `UnknownEdgeType` registry warnings. The existing guard `test_every_allowed_link_verb_is_registered` gains two new violations, hidden behind its pre-existing failure on `segregates_for_requirement`. spec-artifacts-iso owns `implements`. No spec module registers `satisfies`. | spec_artifacts_process/manifest.yaml:709, spec_artifacts_process/manifest.yaml:789, tests/test_semantic_manifest.py:61-75 |
| FND-005 | medium | Some asserts have no negative fixture, so FR-020-AC-10 and FR-023-AC-5 are incomplete. Missing cases: the `Objectives` or `Rules` table removed; a column missing or out of order in `Metrics`, `Rules` or `Evaluations` (AC-1 says "any required column", and only Objectives is tested); `min_rows` on metrics, rules or evaluations; empty cells for metric Name, Unit or Target, Objective, rule Rule, Objective, Class or Source, and evaluation Rule; frontmatter `id` missing (RoleSpec and Rubric); empty rubric Check or Scale. | tests/fixtures/roles/invalid/, tests/test_role_spec.py:128 |
| FND-006 | medium | FR-020 requires the evaluation conditionals to be reported in the same run as the shape checks. They are not: a fixture with both a bad cadence and a judgement row with evaluator `evaluator` reports only the cadence. The cause is in the engine: `record_check::record_findings` returns nothing when `extract()` fails on any assert (quire-rs src/record_check.rs:45). This is recorded only in the PR body. No test or tracker item pins it. | spec_artifacts_process/manifest.yaml:706, spec_artifacts_process/schemas/RoleSpecFields.json |
| FND-007 | low | FR-021-AC-1 and FR-021-AC-12 name `quire matrix`, but the tests use `quire coverage`, because `quire matrix` prints "No obligations matched this scope" for these targets on 0.46.0 and 0.52.1. On matrix output, AC-12 holds only vacuously. The coverage substitute checks the substance (evaluations minted, metrics not minted), but the tags claim the matrix form. | tests/test_role_spec.py:329, tests/test_role_spec.py:337 |
| FND-008 | low | The record_validation fixtures (deterministic-*, judgement-*) are checked only for the row id. They do not check which conditional fired (`allOf/0/then`, `allOf/1/then` or `then/not`), so a regression that fails the row through the wrong branch would still pass. Each fixture is a one-cell diff, which limits the risk. | tests/test_role_spec.py:144, tests/test_role_spec.py:165 |
| FND-009 | low | Five fixtures fail for their intended frontmatter reason plus incidental cascades: id-lower-case, id-too-long, rubric-bad-id, rubric-version-zero and rubric-missing-version. Every row id also fails the interpolated `id_pattern`, giving up to 17 extra diagnostics. The test still hits the intended diagnostic through `at id` or `version`, but the fixtures are not single-cause. | tests/fixtures/roles/invalid/id-lower-case.md, tests/fixtures/roles/invalid/id-too-long.md |

## Deviation rulings

1. **`quire matrix` is empty, so the tests use `quire coverage`.** This is an engine limitation and acceptable as an interim. `quire matrix` renders no criterion whose parent is not a requirement document. SWM-247 capability 1 covers it, and SWM-247 should require re-pointing these two tests to `quire matrix` (FND-007).
2. **FR-020-AC-9 does not hold.** Partly a module fix: dedupe the in-manifest lists and patterns with YAML anchors now. The rest is an engine limitation: `column_choices`, `column_patterns` and `record_validation` need to read an enum or pattern from the module's projected schema (`schemas/EvidenceSource.json`, `QueryRef.json`), so the TypeSpec is the single home (FND-003).
3. **A disallowed verb is a warning with exit 0.** This is an engine limitation. In the module now: assert `--strict` exits 3 and record AC-12 as partial (FND-002).
4. **record_validation runs only after the shape asserts are clean.** This is an engine limitation (FND-006).
5. **Dangling references show only under `--okf` and only as warnings.** The module must change this now: declare the `trace:dangling-trace-reference` error severity and assert exit 3. Engine capabilities are still needed for a per-declaration severity and for the check in plain `quire validate` (FND-001).

## Dispositions

Disposition pass 1 was checked against fix head cc809ce.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | The manifest now declares `grammar_severity: {"trace:dangling-trace-reference": error}`. `test_a_reference_to_an_undefined_row_dangles` asserts that `quire validate --okf` exits 3. The per-declaration severity and the check in plain `quire validate` stay with SWM-247. |
| FND-002 | fixed | By lead decision, FR-020-AC-12 now requires `quire validate --strict` to exit nonzero. Both bad-verb tests pin exit 3 and assert that the valid fixtures exit 0 under `--strict`. The engine severity key for `disallowed-edge-type` is on SWM-248. |
| FND-003 | deferred | The in-manifest copies are removed: `&evidence_sources`, `&query_ref` and a test that counts them. The TypeSpec and RoleSpecFields.json copies remain until the SWM-248 schema-`$ref` capability lands. FR-020-AC-9 still fails on inspection until then. |
| FND-004 | fixed | `satisfies` is registered in `edge_types` and `implements` is dropped, with FR-020 and FR-023 amended by lead decision. `test_every_allowed_link_verb_is_registered` now fails only on the pre-existing `segregates_for_requirement`, the same as origin/main. |
| FND-005 | fixed | 28 fixtures were added and 4 changed. Each one was run, and each fails on the intended table, column, cell or field. |
| FND-006 | deferred | SWM-248 tracks same-run reporting. `test_shape_and_record_defects_are_reported_in_two_passes` pins the current two-pass behaviour. |
| FND-007 | deferred | SWM-247 has a scope note to re-point the AC-1 and AC-12 tests to `quire matrix` when capability 1 lands. |
| FND-008 | fixed | The conditional needles now include the schema path (`allOf/0/then`, `allOf/1/then/pattern`, `allOf/1/then/not`). |
| FND-009 | fixed | id-lower-case, id-too-long, rubric-bad-id and rubric-version-zero each produce exactly one diagnostic. The cascades left in missing-id and rubric-missing-version are the engine's `unresolved-field` for an absent field, which a fixture cannot avoid. |
| FND-010 | fixed | Round 2, head 85d21a8. The US-001 and US-002 tokens are removed from TC-001, TC-002, TC-005 and TC-100. The `traces-to` reference resolves only to acceptance-criterion targets, so those tokens never resolved and never reached the matrix; US-001 and US-002 keep their lineage through FR-003/FR-004 and FR-009 to FR-013 `satisfies`. TC-037's `-AC-2` became FR-005-AC-2, the same criterion. `quire validate --okf` over the repo exits 0, and the PR body records the consumer-facing change. |
| FND-011 | fixed | Round 2, head 85d21a8. The skeleton now reads "Allowed relationship verbs: satisfies, depends_on." The regenerated golden record changes only the provenance digest in examples/RoleSpec.record.json, and the golden-record tests pass. |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-010 | medium | The module-wide `trace:dangling-trace-reference: error` key turns `quire validate --okf` over this repository from exit 0 to exit 3. Five dangling `traces-to` references already exist in spec/tests.md: TC-001, TC-002 and TC-005 cite US-001, TC-100 cites US-002 and TC-037 cites AC-2. Every consumer that runs this module under OKF inherits the same change. The PR does not mention it, and nothing fixes those five references. | spec_artifacts_process/manifest.yaml:2170, spec/tests.md:12, spec/tests.md:46 |
| FND-011 | low | The RoleSpec skeleton still lists `implements` as an allowed verb, which contradicts the amended FR-020. An author who follows it gets a `disallowed-edge-type` warning, and a failure under `--strict`. | spec_artifacts_process/skeletons/RoleSpec.md:19 |
