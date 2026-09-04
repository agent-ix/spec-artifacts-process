---
id: SR-016
title: "Code review — the #78 semantic module contract"
type: SpecReview
analysis: code-review
scope: "spec_artifacts_process/semantic/, spec_artifacts_process/mappings.yaml, spec_artifacts_process/manifest.yaml, spec_artifacts_process/skeletons/, scripts/manifest_digests.py, tests/"
review_set: subset
---
# SR-016: Code review — the #78 semantic module contract

## Summary

Python lane (`pyproject.toml`, `.py` files) plus the Node generator, over the whole
`spec/78-semantic-module-contract` diff against `origin/main`: the TypeSpec source and its
projection, the manifest change, the mapping and its reference implementation, thirteen
skeletons, twelve negative fixtures, and seven test modules.

Gates run rather than assumed: `make lint` (ruff + black + the schema drift gate) is clean,
`make schemas-check` is clean on the committed tree, and `pytest` reports **295 passed, 2 xfailed,
1 failed** with the coverage gate at **100%, unchanged**. The single failure,
`test_tc047_adoption_is_optional`, **fails identically on `origin/main`** and is fixed by commit
`737987b` on the unmerged `epic/264-assurance-integration`; it is not caused, worsened or hidden
here.

Mechanical checks: no `TODO`/`FIXME`/`XXX`; no mocks of any kind — every test drives the real
engine, the real generator or the real CLI; no `pytest.skip` in the new modules except the
opt-in guard on IT-002, which is documented and paired with a strict `xfail`; no weak
`is not None`/`isinstance`-only assertions; every test function asserts or raises. Both `xfail`s
are `strict=True`, so each turns red the moment the upstream defect it names is fixed.

The repository's own idiom — module-level test functions, no `TestX` classes — is followed; the
skill's class-structure check is superseded by it (`CLAUDE.md`, and every pre-existing test
module).

## Verdict

**CONDITIONAL** — no high findings. Four mediums, all of which are recorded upstream defects or
deliberate scope boundaries rather than code to change here, and three lows.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | IT-002 is red: `quoin module install` refuses this manifest (`semantic.export-without-schema`) because Quoin's FR-070 validator resolves `semantic.exports` against `object_types` only. The already-merged `spec-artifacts-iso` is refused the same way, so it is upstream. Carried as `xfail(strict=True)`, never a skip. `agent-ix/quoin#347`. | tests/test_quoin_install_roundtrip.py:60 |
| FND-002 | medium | FR-010-AC-9 cannot pass: quire 0.46.0 refuses an unknown `semantic` key and a bad digest silently. TC-135 is `xfail(strict=True)` naming `agent-ix/quire-rs#221` and `#394`. | tests/test_semantic_manifest.py:214 |
| FND-003 | medium | A reference-form `data_schema.digest` is not verified at load at all — 64 zeros load clean, while removing `schemas/` drops 7 of 14 archetypes. TC-094 pins the measured inertness and names the line to delete when the engine changes, rather than asserting a refusal that would be red for a defect this module cannot fix. `agent-ix/quire-rs#400`. | tests/test_semantic_manifest.py:196 |
| FND-004 | medium | The FR-035 conformance check is split in two — the manifest minus `semantic` against the shipped schema, and the block against an extracted sub-schema — because no published revision knows both `traceability`/`verification_catalog` and `semantic`. Both halves are checked; neither is dropped. `agent-ix/filament-core-service#27`. | tests/test_manifest.py:113 |
| FND-005 | low | `ReferenceMapper._section` takes `model`, `prop` and `errors` and uses none of them. It is the uniform per-kind signature `_one` dispatches on; dropping them would make the dispatcher branch on kind twice. Commented rather than changed. | tests/support/reference_mapping.py:346 |
| FND-006 | low | `test_no_model_declares_a_run_property` carries one named exception, `FeedbackAnchor.artifact` — the spec document a thread is anchored in, not a run artefact. Listed with its reason rather than removed from the lexicon: narrowing the words to make a check pass is how a check stops catching what it was written for. | tests/test_skeletons_and_roles.py:60 |
| FND-007 | low | The `Standard.sysml.md` skeleton has no golden record of its own; `TC-115` asserts instead that it maps to a record differing from `Standard.md` in no property but provenance. That is the stronger claim, and it is recorded here so the missing twelfth-plus-one file does not read as an omission. | tests/test_markdown_mappings.py:206 |

## Spec-code faithfulness

Every FR in scope has code and tests that do what it says, checked by opening both:

- **FR-009** — `semantic/main.tsp` + `semantic/scripts/generate.mjs`. Real projection through
  `tsp compile`; the `--check` mode was exercised against a mutated tree and refuses it by name.
  The `$id`/`$ref` normalization is genuinely exercised: `RecordString.json` comes out relative
  and `toolchain.json` records `applied: true`, so the issue-31 path is not a dead branch.
- **FR-010** — `manifest.yaml` carries the nine-key block and twelve reference-form
  `data_schema` entries; `scripts/manifest_digests.py` rewrites only digest values, textually,
  so the manifest's comments survive a refresh.
- **FR-011** — `mappings.yaml` (12 models, all nine kinds used by a real property) and a
  reference implementation that builds all thirteen skeletons into records that validate.
- **FR-012** — thirteen skeletons, each validated through `quire.validate_document` against this
  module's own manifest; twelve negative fixtures, each asserted to fail *the check it names*.
- **FR-013** — the role map is asserted whole, and the run-property check walks each model and
  everything it `$ref`s rather than the top level only.

## Edge cases and defensive coding

- The generator refuses an emitter entry that is not a top-level `*.json`, and refuses a file
  whose **absolute** `$id` names a foreign module base — a relative `$id` is left to the
  normalization, which is the bug the first version of that guard had and the projection caught.
- Missing toolchain, wrong Node, a `@jsonSchema` base that disagrees with the manifest, and a
  semantic-core version that disagrees with `semantic.semantic_core` each exit non-zero naming
  both values and the command that fixes it.
- The mapper normalises CRLF before slicing and digests the normalised bytes, treats `\|` as a
  literal pipe, scopes row-id uniqueness per table, and reports every error of one document in
  one pass.
- The consumer measurement asserts that documents were actually graded — non-zero, and the same
  count on both sides — and a companion test proves it can go red: a narrowed `Status` vocabulary
  yields 8 regressions on one consumer and 4 on the other. Both guards were earned: the first
  version symlinked the staging modules, which made the loader emit nine `SymlinkLoop` lines per
  run, and the comparison of nine noise lines to nine noise lines passed while **no document had
  been read**. Modules are now copied, the rollup lines are filtered, and the graded-document
  count is asserted.

## Recorded inspections

- **FR-013-AC-8 (TC-143)** — every emitted model's property documentation was read at commit
  `f24cfd8`. No property *means* a run outcome under a different name: `Plan.status` and
  `Task.status` are the authored lifecycle word, `TestMatrix` row `status` is the authored
  coverage claim, `InspectionRow.commit` and `.verdict` are the authored record of a human act,
  and `SuiteRow.command` names what would run rather than what did. Recorded as an inspection
  because a test can check names and only a reader can check meaning.
- **FR-009-AC-13 / FR-009-CON-6** — every "for every declared type" assertion enumerates the type
  list from `manifest.yaml` (`artifact_type_names()`) or from the emitted bundle. No test in the
  new modules carries a hard-coded type list.
