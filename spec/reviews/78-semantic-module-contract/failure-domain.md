---
id: SR-012
title: "failure-domain review of the #78 spec set"
type: SpecReview
analysis: failure-domain
scope: "spec/functional/FR-009..FR-013, spec/non-functional/NFR-001, spec/spec.md"
review_set: all
---
# SR-012: failure-domain review of the #78 spec set

## Summary

Extension points, entity identity, evaluation purity and topological robustness across the #78
set. The generator (FR-009) is the one true extension point — it shells out to an external
compiler and reads whatever that compiler wrote — and the spec handles it well: an unexpected
emitter output is a hard failure naming the entry rather than a silent subset, and a failed
compile writes nothing. Identity is mostly explicit. The gaps are in evaluation purity of the
mapping and in what happens when the two schema consumers disagree.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | Identity: `Standard` is declared twice in this manifest — as an artifact type (`Standard`, frontmatter-schema-backed, id `^[A-Za-z]{2,}-[0-9]+$`) and as an object type (`standard`, inline `data_schema`). FR-010 keeps both and says why, but no requirement states **which one a document carrying `type: Standard` resolves to** when both are active, nor what a consumer sees when they disagree. `quire validate` already emits `DuplicateArchetype: 'standard' … first-wins` on every run of this repository. First-wins across two declarations in *one* manifest is an identity collision, not a merge policy. State the resolution or the duplication is a latent contract defect the migration is now blessing. | FR-010-AC-8, spec.md | missing-requirement |
| FND-002 | high | Extension-point failure policy is undefined for the mapping. FR-011 says the mapping "SHALL report `<error>` and build no record" for six distinct defects, but never says what a caller does with a document that is *partly* mappable — whether one bad table poisons the whole record or only its property. FR-011-AC-10 asks for three errors in one pass, which implies the mapping keeps going; "build no record" implies it stops. Both cannot hold. Choose strict (any error → no record, all errors reported) and say so once. | FR-011-AC-8, FR-011-AC-9, FR-011-AC-10 | wrong-requirement |
| FND-003 | medium | Evaluation purity: FR-009's generator both *reads* the manifest (for the version) and, through `make manifest-digests`, *writes* it (FR-010). Nothing forbids the two running in an order that makes the digest describe bytes the generator has since replaced. The spec has `make schemas` then `make manifest-digests` as a documented sequence but no requirement that the check detects the stale intermediate state. `make schemas-check` compares schemas to source and digests to schemas, but a tree where both were regenerated from a *different* manifest version passes both halves. State the ordering as an invariant the check enforces. | FR-009-AC-4, FR-010-AC-7 | correct-requirement-no-evidence |
| FND-004 | medium | Topology: `mappings.yaml` references model properties and model properties reference each other through `$ref`. Nothing in FR-011 bounds the reference depth or forbids a cycle, and the emitted schemas can legitimately contain one (a `Section` inside a row inside a table). A totality checker that walks properties recursively (FR-011-AC-2) will not terminate on a cyclic model. Require the walk to be cycle-safe. | FR-011-AC-2 | missing-requirement |
| FND-005 | medium | Identity: FR-011's `duplicate-row-id` (AC-11) is defined per table, but three archetypes carry two or more id-bearing tables in one document (`TestMatrixIndex` has `INT-` and `GAP-`; `TestMatrix` has test-case rows and four coverage tables). Whether an id must be unique per table or per document is unstated, and the two answers give different records. | FR-011-AC-11 | missing-requirement |
| FND-006 | low | The negative fixtures carry `expect:` and `because:` frontmatter (FR-012), which the `Standard`/`SpecReview` frontmatter schemas admit only because `additionalProperties: true`. A later tightening of any frontmatter schema would silently invalidate the whole negative corpus. Note the dependency in FR-012 so the coupling is visible. | FR-012-AC-7 | correct-requirement-no-evidence |
| FND-007 | low | Nothing states what happens when `@agent-ix/semantic-core` is resolvable but at a version other than 0.1.0 — `semantic.semantic_core: 0.1.0` is a declaration, not a check. `toolchain.json` records the resolved version (FR-009-AC-9) but no criterion compares the two. One line closes it. | FR-009-AC-9, FR-010-AC-1 | missing-requirement |
