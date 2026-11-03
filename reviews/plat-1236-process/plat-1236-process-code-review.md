---
id: SR-904
title: "PLAT-1236 process code-review review"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process; spec/functional/FR-004-traceability-declaration.md; spec_artifacts_process/manifest.yaml; tests/test_traceability_declaration.py; PLAT-1236; PR 128"
review_set: subset
---

## Summary

The manifest and lint vocabulary are aligned and adverse lint controls are retained. The declared Python engine dependency excludes the required implementation release.

## Assurance Context

No applicable AssuranceProfile or review_policy declaration was found in this process repository. Active exceptions: none identified. Direct scoped review is used; no enforced workflow acceptance or publication approval is claimed.

## Examined Units

- **FR-004-AC-1** (examined): The model declares trace targets minting test-case ids from the Test Matrix and acceptance-criterion ids from `FR`, `NFR` and `interface`, and loads without a validation error
- **FR-004-AC-21** (examined): A `lint_rules` entry (`table_column_values`, `severity: warning`) scoped to `FR`/`NFR`/`interface` requires the `Acceptance Criteria` table's `Verification` column to hold one of the four IADT classes (`Test`/`Inspection`/`Analysis`/`Demonstration`), a `verification_catalog` method id or an explicitly declared `vocabularies.retired` token, with no trailing `TC-…`/`IT-…` id. `quire lint --module <this module>` over a fixture document whose `Verification` cell reads `Test (TC-999)` reports a warning-severity finding naming the id; a cell naming a bare class or a bare catalog method id (e.g. `pro
- **FR-004-AC-22** (examined): The lint rule's `allowed` set is exactly the four IADT classes union every key of the manifest's `verification_catalog` union the manifest's `traceability.vocabularies.retired` tokens — derived, not hand-maintained: a test loads both and asserts set equality, so an entry added to the catalog and the lint rule's `allowed` list cannot drift apart. `Eval` and `Manual` (`traceability.vocabularies.test_type` values, not catalog keys) are absent from `allowed`.
- **FR-004-AC-23** (examined): The model declares exactly `vocabularies.retired: [Withdrawn]`, disjoint from the verification catalog, test types and `no_source_symbol`. The existing retired Status marker remains `⛔`. The Verification lint rule accepts the declared retirement token and still rejects `Planned` and misspelled retirement values; it does not classify them as retirement.

## Evidence

Reviewed frozen head fb67cd16cb55bb1c916dc43f0c576291bae60d41 against e6ce2f63bf75fe3a51c8b92f23eb6020876007ab. No Cargo commands or source/spec edits. Three selected static declaration tests passed. Subject spec validation passed with existing module advisories. Candidate-model matrix refused the new retired field under installed quire 0.36.2 (engine 0.50.2); an explicitly labelled installed-model matrix successfully inspected current source tags and reported AC-21 tagged, AC-22 untagged, AC-23 tagged. The installed-model result is not candidate-engine admission evidence. Deterministic quoin advise ran under that same disclosed installed model. Candidate CLI and Python engine qualification remain required; no merge-ready execution claim.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | medium | The newly required retirement field needs quire 0.51.0, but the declared Python engine dependency ^0.50.0 excludes that release and poetry.lock retains 0.50.0. Python Registry.load_from semantic tests therefore cannot load this manifest in the declared environment even after qualifying a candidate CLI. Adopt a compatible minimum engine and lock once it is available, and qualify the Python loader as well as the CLI. | pyproject.toml:39 | correct-requirement-no-evidence |

## Verdict

CONDITIONAL for this method. Final PR merge is held until findings are resolved and actual candidate-engine qualification succeeds.

## Dispositions

Round 1, checked frozen head f9dc0913ae0d773fcf74b937fecbaac2f6a31bcc. Candidate CLI 0.38.1 reports engine 0.51.0; candidate Python wheel from engine b18cc5e0 loads all 14 archetypes. The provided four-target run is 64 passed and 1 pre-existing xfailed, including traceability 27 passed. Candidate qualification is not a registry release or a lockfile resolution. No Cargo runs or source edits during this pass.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | still-open | The minimum dependency now permits ^0.51.0 and the candidate 0.51.0 Python wheel loads all 14 archetypes; candidate CLI and Python qualification passed. poetry.lock still resolves quire 0.50.0, so a fresh declared install does not reproduce that qualification. Resolve and commit the lock against the released compatible package before merge. |
