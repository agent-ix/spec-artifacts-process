---
id: SR-2026112016223475846355035
title: "Code review — spec-artifacts-process DossierDocument producer identity"
type: SpecReview
analysis: code-review
scope: "spec/functional/FR-018-dossier-document-archetype.md; spec_artifacts_process/semantic/main.tsp; spec_artifacts_process/mappings.yaml; spec_artifacts_process/schemas/DossierDocument.json; spec_artifacts_process/schemas/DossierProducerIdentity.json; spec_artifacts_process/schemas/dossier-document-frontmatter.schema.json; tests/test_dossier_document.py"
review_set: subset
---
## Summary

One medium test coverage defect: the new projected-record assertion checks an extra nested member but not missing or incomplete identity members, although FR-018-AC-20 requires all three rejection cases.

## Verdict

**CONDITIONAL** — One medium test coverage defect: the new projected-record assertion checks an extra nested member but not missing or incomplete identity members, although FR-018-AC-20 requires all three rejection cases.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | Projected schema tests omit missing and incomplete producer identity cases | tests/test_dossier_document.py:119-130 |

## Review notes

The changed schema/model/mapping agree on required `name` and `version`, constrain the name to `quoin`, and close the nested object against additional members. Existing frontmatter examples and invalid fixtures were updated consistently. The added mapping test verifies preserved values and rejects an extra nested member, but leaves the missing and incomplete nested record cases unasserted.
