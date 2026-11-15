---
id: SR-20261115175449
title: "PLAT-1436 PR155 code-review"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR155; spec_artifacts_process/manifest.yaml, spec_artifacts_process/mappings.yaml, spec_artifacts_process/schemas/DossierDocument.json, spec_artifacts_process/schemas/dossier-document-frontmatter.schema.json, spec_artifacts_process/skeletons/DossierDocument.md, tests/test_dossier_document.py, tests/test_skeletons_and_roles.py, tests/fixtures/dossier/"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-018", type: references}
---

## Summary

Ticket: PLAT-1436. Reviewed PR #155, which adds the `DossierDocument` archetype, artifact type, frontmatter schema, record schema, mapping, skeleton, seven fixtures and one test module. Every fixture behaves as intended under `quire validate --module spec_artifacts_process`: both valid fixtures and the skeleton pass, and each invalid fixture fails with a diagnostic that names the intended field.

The PR does not keep the module's own per-type invariants. The new type has no golden record, no TypeSpec model, and no deliberate line in the manifest `body_extraction` guard. The repository's existing tests enumerate types from the manifest, so they fail for `DossierDocument`. The PR's only CI is the CLA check, because `ci.yml` is `workflow_dispatch` only, so no gate exercised this. `make test` could not run in this worktree (no poetry env; `poetry install` was denied with "This command requires approval"). The test failures below come from reading the code, not from running it.

## Verdict

**FAIL.** Four existing gates fail for the new type (FND-001, FND-002, FND-003, FND-007). The fixture design, the schema vocabulary and the no-digest intent are sound.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | No `examples/DossierDocument.record.json` golden record; TC-113 and TC-142 enumerate every manifest type and fail for `DossierDocument`. | tests/test_skeletons_and_roles.py:278-281 |
| FND-002 | high | `DossierDocument` adds `body_extraction`, but the manifest guard's `with_contract` set in tests/test_manifest.py was not extended, so that assertion fails. | tests/test_manifest.py:237-274 |
| FND-003 | high | `schemas/DossierDocument.json` was written by hand into the projected-schema directory and has no `main.tsp` model; `make schemas-check` (part of `make lint`) treats it as a stale projection. | spec_artifacts_process/schemas/DossierDocument.json:1 |
| FND-004 | medium | The AC-2 test asserts `"version" in result.stderr`, but every diagnostic line prints the fixture path `missing-version.md`/`empty-version.md`, so the assertion holds for any failure. | tests/test_dossier_document.py:39-44 |
| FND-005 | low | `quire_validate` is a copy of `quire_validate` in tests/test_anomaly.py:62-77 and lacks conftest `run_quire`'s `shutil.which` guard; share one helper. | tests/test_dossier_document.py:15-29 |
| FND-006 | low | The `document_kind` vocabulary is declared three times (frontmatter schema, record schema, manifest `assert.choices`), and the M2 extension must edit all three in step. | spec_artifacts_process/manifest.yaml:217 |
| FND-007 | high | The frontmatter `id` pattern `^DOS-…$` has no counterpart in the model `id` (NonEmptyText, no pattern), so TC-137 `test_each_model_agrees_with_its_frontmatter_schema` fails. | spec_artifacts_process/schemas/dossier-document-frontmatter.schema.json:7-10 |

## Examined scope

```yaml
scope:
  - {id: FR-018-AC-1, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "A fixture carrying `id`, `title`, `version`, `type`, `document_kind`, `generated_by` and `as_of` validates with `quire validate`, and the same fixture without `as_of` validates."}
  - {id: FR-018-AC-2, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "A fixture with no `version` fails `quire validate`, with a diagnostic naming `version`."}
  - {id: FR-018-AC-3, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "A fixture with `document_kind: verification-report` fails `quire validate`, with a diagnostic naming `document_kind`."}
  - {id: FR-018-AC-4, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "A fixture with `generated_by: hand` fails `quire validate`, and a fixture with no `generated_by` fails."}
  - {id: FR-018-AC-6, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "The skeleton `DossierDocument.md` validates, and `DossierDocument` carries the role `definition` in `mappings.yaml`."}
  - {id: TC-113, path: "tests/test_skeletons_and_roles.py", role: context_only, excerpt: "assert (EXAMPLES_DIR / f\"{model}.record.json\").is_file()"}
  - {id: TC-142, path: "tests/test_markdown_mappings.py", role: context_only, excerpt: "assert record == golden(model)"}
  - {id: FR-009, path: "spec/functional/FR-009-emitted-json-schemas.md", role: context_only, excerpt: "`make schemas` regenerates spec_artifacts_process/schemas/<Model>.json; `make schemas-check` fails on any byte drift."}
```
