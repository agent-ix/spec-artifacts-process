---
id: SR-20261102086816
title: "Dependency review of PLAT-1414 Anomaly archetype and safety-impact assessment"
type: SpecReview
analysis: dependency
scope: "agent-ix/spec-artifacts-process PR139 @36754ea over origin/main; spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md, spec/functional/FR-015-anomaly-safety-impact-assessment.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-014"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/FR-015"
    type: references
---

## Summary

Ticket: PLAT-1414. Dependency analysis of the upstream edges that FR-014 and
FR-015 declare: the in-repo FR-009 and FR-012, quire-rs FR-033 and FR-050, and
`agent-ix/spec-objects-safety`. Each was checked against that repo's
`origin/main`: quire-rs `spec/functional/FR-033-locator-assert-facet.md`,
`FR-050-declarative-coverage-computation.md`, `FR-026` and `FR-040`, and
spec-objects-safety `spec_objects_safety/manifest.yaml`, `schemas/Hazard.json`
and `skeletons/hazard.md`.

The in-repo edges (FR-009 schema emission, FR-012 skeletons with negative
counterparts) are right. The cross-repo edges either name the wrong upstream
or claim more than the upstream provides.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-014 names quire-rs FR-033 (the `assert` facet) as the mechanism for its checks. FR-033 supports per-locator keys only: `columns`, `optional_columns`, `min_rows`, `max_rows`, `choices`, `column_choices`, `column_patterns` and `id_pattern`. It has nothing for legal `From`/`To` pairs, for a row's `From` equalling the previous row's `To`, for the last row's `To` equalling frontmatter `status`, or for FR-015's rule that a section is required depending on `status`. So most of FR-014 (the AC-3 to AC-6 checks) and FR-015-AC-3 and AC-7 have no named owner, and an implementer cannot tell whether to extend quire-rs or write module-side validation. Name the capability that evaluates these rules and its owning repo or ticket, or add an FR that declares it. | spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:38-44; spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:72 |
| FND-002 | medium | FR-015 cites quire-rs FR-050 for "traceability model and document references". FR-050 is the declarative coverage rollup (`quire coverage`) and does not resolve references. Resolving references and reporting dangling ones is quire-rs FR-026, and checking the target's type on a typed edge is FR-040 (`allowed_links`). FR-015 also invents a `Target` table column instead of declaring `Anomaly` edges to `FR`/`NFR`/`hazard` through `allowed_links`, which would give the dangling-reference and kind-mismatch checks of AC-5 and AC-6 from the existing engine. Re-point the dependency to FR-026 and FR-040, and either use typed edges or say why the table cannot. | spec/functional/FR-015-anomaly-safety-impact-assessment.md:43-46; spec/functional/FR-015-anomaly-safety-impact-assessment.md:71 |
| FND-003 | medium | FR-015 says "the hazard id class is owned by `agent-ix/spec-objects-safety`". That module declares no hazard id class or id pattern. `HAZ-001` appears only in its skeleton. `hazard` is an `object_type`, and its documents carry `type: hazard` and `object: hazard`. FR-015 does not say which field makes a document "a `hazard` artifact" for the kind check of AC-6. It also does not say what happens when spec-objects-safety is not installed in the validating environment: hazard documents are then untyped, so every `Hazard` row fails as dangling or as a kind mismatch, and the failure blames the anomaly rather than the missing module. State that a hazard is identified by `object: hazard` (or by `type`), with no id-pattern assumption, and state the behaviour, with its own diagnostic, when the safety module is absent. | spec/functional/FR-015-anomaly-safety-impact-assessment.md:27-28; spec/functional/FR-015-anomaly-safety-impact-assessment.md:44-46; spec/functional/FR-015-anomaly-safety-impact-assessment.md:62-64 |
| FND-004 | low | FR-015's relationship target is `ix://agent-ix/spec-objects-safety/spec/spec`. The `spec/spec.md` of spec-objects-safety has no `id`, and no other document in this repo uses a `/spec/spec` target. Target the module itself, or record the dependency only in `## Dependencies`, where it is already stated. | spec/functional/FR-015-anomaly-safety-impact-assessment.md:10-11 |

## Verdict

FAIL. Three medium findings: the lifecycle and conditional checks have no
upstream that can express them, the reference-resolution dependency names the
wrong FR, and the hazard dependency rests on an id class that does not exist.
Resolve these before implementation is scheduled.
