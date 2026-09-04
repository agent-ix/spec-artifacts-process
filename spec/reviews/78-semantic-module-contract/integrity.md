---
id: SR-013
title: "integrity review of the #78 spec set"
type: SpecReview
analysis: integrity
scope: "spec/spec.md, spec/usecase/US-002, spec/functional/FR-009..FR-013, spec/non-functional/NFR-001, spec/tests.md"
review_set: all
---
# SR-013: integrity review of the #78 spec set

## Summary

Completeness, consistency and atomicity gate over the #78 set. Traceability closes: US-002 maps to
five FRs; all five FRs and NFR-001 trace to StR-001 through US-002 and each declares a verification
method on every criterion; NFR-001 names the three FRs it constrains and all three name it back.
No contradictory constraint pair was found — the only near-conflict, "emit a schema for every type"
against "change no archetype", is resolved by the reference-form `data_schema` being an added key
rather than a replaced one, and FR-010 states that resolution.

Atomicity is good after the EARS pass. The findings are about hidden assumptions: five of the
integrity probes fire on FR-009 alone, because it delegates to an external CLI, does a
multi-source lookup, and depends on a package published outside any index this repository may
commit against.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | Hidden assumption — external CLI. FR-009 delegates the whole projection to `tsp compile` and to `npm ci`, and declares neither a minimum Node version as a checked precondition (the prose says "Node 20 or later, the runtime requires" — a statement about TypeSpec, not an obligation on this module) nor the user-facing error when `node`, `npm` or `node_modules` is absent. The generator does emit an install hint in the sibling module; here it is unspecified. Add the precondition and its diagnostic as behaviour. | FR-009 | missing-requirement |
| FND-002 | high | Hidden assumption — multi-source lookup with no tie-break. Three declarations now describe the same thing in three places: the frontmatter JSON Schema, the `body_extraction` locator, and the emitted record schema. FR-010 requires the manifest and the schemas to agree by digest, and FR-011 requires the mapping and the manifest to agree by section name — but **nothing requires the emitted model and the frontmatter schema to agree**. A `Plan.id` pattern could be `^[A-Za-z]{2,4}-[0-9]+$` in one and something else in the other, and both would validate. That is the exact drift this ticket exists to end. Add the cross-check. | FR-009, FR-010, FR-011 | missing-requirement |
| FND-003 | medium | Hidden assumption — package not on a committable index. FR-009 depends on `@agent-ix/semantic-core` resolving through the user-level npm config, and NFR-001's verification depends on a `quire` wheel provisioned by `make dev-quire`. Both are recorded in `spec.md` Out of Scope with their owning issues (`filament-core-data#11`, `quire-rs#392`), which is right, but neither has a stated interim behaviour for CI: does `make lint` run `make schemas-check` in a GitHub workflow where `@agent-ix` does not resolve? FR-009 says `make lint` SHALL run it. Those two statements conflict for any CI runner. | FR-009, spec.md | wrong-requirement |
| FND-004 | medium | Duplicated requirement with different wording: FR-010-AC-3 ("every 0.1.0 declaration present unchanged apart from the named additions"), FR-013-AC-7 ("archetype declarations byte-identical to the 0.1.0 baseline apart from the additions") and NFR-001-AC-1 (the same claim, per declaration class) are three statements of one obligation, verified by three separate test cases (TC-091, TC-126, TC-127). Keep one as the normative statement and have the other two reference it, or three tests will drift and two will be deleted as redundant by whoever notices second. | FR-010-AC-3, FR-013-AC-7, NFR-001-AC-1 | wrong-requirement |
| FND-005 | medium | Non-observable obligation. FR-013-AC-2 forbids a property "whose name **or documented meaning** is a run identifier, run timestamp, …". A test can check names; it cannot check documented meaning. As written the criterion is half machine-verifiable and half a review judgement presented as a test. Split it, and make the judgement half an Inspection with a recorded reviewer. | FR-013-AC-2 | correct-requirement-no-evidence |
| FND-006 | low | `semantic.mappings` lists nine kinds and FR-011 requires all nine to be used, but `token` and `list` have no obvious consumer in the twelve models as sketched — the process artifacts are frontmatter, sections and tables. Declaring a mapping kind the module does not use is the "declaration the engine cannot honour" shape this repository has hit before (CR-037, CR-081). Either name the properties they map or drop them from the declared list. | FR-011-AC-2, FR-010-AC-1 | wrong-requirement |
| FND-007 | low | `spec.md` Out of Scope now carries eleven entries, each with an owner, which is a real improvement over the two it had. One is stated as a decision rather than a boundary — "Resolving the `Standard`/`standard` duplication" — and belongs in the requirements architecture or an ADR, because a reader looking for *why* the module has two Standards will not look in Out of Scope. | spec.md | correct-requirement-no-evidence |
