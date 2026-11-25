---
id: SR-2026112016223475846355039
title: "Specification integrity — DossierDocument producer identity"
type: SpecReview
analysis: integrity
scope: "spec/functional/FR-018-dossier-document-archetype.md; spec_artifacts_process/semantic/main.tsp; spec_artifacts_process/mappings.yaml; spec_artifacts_process/schemas/DossierDocument.json; spec_artifacts_process/schemas/DossierProducerIdentity.json; spec_artifacts_process/schemas/dossier-document-frontmatter.schema.json; tests/test_dossier_document.py"
review_set: subset
---
## Summary

FR-018-AC-20 bundles several input rejection variants, exact field projection, and three record-schema rejection cases into one criterion. The single criterion concerns one identity object, but splitting frontmatter validation from record-schema validation would make failures and evidence attribution clearer.

## Verdict

**CONDITIONAL** — FR-018-AC-20 bundles several input rejection variants, exact field projection, and three record-schema rejection cases into one criterion. The single criterion concerns one identity object, but splitting frontmatter validation from record-schema validation would make failures and evidence attribution clearer.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-018-AC-20 combines frontmatter and projected-record obligations | spec/functional/FR-018-dossier-document-archetype.md:109 |
