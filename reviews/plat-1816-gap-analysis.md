---
id: SR-2026112016223475846355036
title: "Gap analysis — spec-artifacts-process PLAT-1816"
type: SpecReview
analysis: gap-analysis
scope: "spec/functional/FR-018-dossier-document-archetype.md; spec_artifacts_process/semantic/main.tsp; spec_artifacts_process/mappings.yaml; spec_artifacts_process/schemas/DossierDocument.json; spec_artifacts_process/schemas/DossierProducerIdentity.json; spec_artifacts_process/schemas/dossier-document-frontmatter.schema.json; tests/test_dossier_document.py"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process", type: references}
---
## Summary

The repository-wide computed matrix reports 102 untagged criteria (and no evidence bindings). FR-018-AC-20 itself is tagged by two tests; code review separately found that its nested-schema negative assertions are partial. The global gaps predate and exceed this PR scope.

## Verdict

**FAIL** — The repository-wide computed matrix reports 102 untagged criteria (and no evidence bindings). FR-018-AC-20 itself is tagged by two tests; code review separately found that its nested-schema negative assertions are partial. The global gaps predate and exceed this PR scope.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | Repository-wide computed matrix reports 102 untagged criteria | spec/functional/FR-018-dossier-document-archetype.md |

## Coverage

- Reconciliation: quoin matrix (quoin 0.36.8, quire 0.52.0 (engine 0.62.2)).
- Plan completion: not assessed.
- Criteria: tagged 212 · untagged 102 · tagged-by-ignored-test 0 · method-without-symbol 24 · retired 1.
- Evidence: bound 0 · stale 0 · suspect 0 · undischarged 0 · no run evidence 339.
- FR-018 criteria: 20/20 tagged, including FR-018-AC-20; no evidence is bound for any criterion.
- `quire coverage --scope . --json` reports 4 untracked symbols and 42 unmatched tags; none references FR-018-AC-20.
- Reverse-gap and stub review was confined to changed model, mapping, schema, fixtures and test path; no new public runtime behavior was added. A whole-source inventory was not completed, so this artifact does not claim repository-wide reverse-gap or stub assurance.
- Semantic review: skipped; no explicit opt-in was supplied.
