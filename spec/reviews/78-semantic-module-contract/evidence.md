---
id: SR-011
title: "evidence and verification-method review of the #78 spec set"
type: SpecReview
analysis: evidence
scope: "spec/functional/FR-009..FR-013, spec/non-functional/NFR-001, spec/tests.md rows TC-080..TC-131"
review_set: all
---
# SR-011: evidence and verification-method review of the #78 spec set

## Summary

Method review driven by `quoin advise` over this repository, plus `quire properties --json` on
every new criterion. `quoin advise` reports **4 mismatches of 123 obligations, 4 uncatalogued,
0 inconclusive**; three of the four mismatches are on artifacts authored here
(`NFR-001-AC-5`, `NFR-001-M-4`, `NFR-001-M-5`) and one is pre-existing (`FR-003-AC-9`).
`quire properties` classifies **all 52 new criteria as `assertion`** — none is
property-extractable in the FR-052 sense.

The `assertion` result is the finding worth reading. Several criteria are written with universal
quantifiers — "every shipped projection", "every `$ref`", "byte-identical over two runs", "total
in both directions" — which the `spec-matrix` guidance would push toward `Property`. They are not
property-shaped in the generative sense: each quantifies over a **finite, enumerable population
this module owns** (the emitted file set, the model property set, the twelve artifact types), so
an exhaustive test over the whole population is stronger evidence than a generator sampling it.
The matrix `Type: Unit` is therefore correct, and the reason is recorded here rather than left as
a habit — but only where the test genuinely enumerates. A test that checks three of twelve types
and calls itself exhaustive is the failure mode this paragraph exists to prevent.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | `quoin advise` flags NFR-001-M-4 and NFR-001-M-5 (the two consumer-repository measurement rows) as authored `Demonstration` against a recommended `performance-benchmarking` — a rule match on `quantified-threshold`, because the rows carry the numbers 2 and 0. The recommendation is wrong for this obligation (nothing is being timed) but it exposes a real defect: the two rows state thresholds with no stated measurement procedure, so "0 new error findings" has no defined comparison method in the Measurement table itself. Move the comparison procedure from prose into the Method column. | NFR-001-M-4, NFR-001-M-5 | correct-requirement-no-evidence |
| FND-002 | high | FR-010-AC-6 is authored `Test` but half of it cannot pass: quire-rs#221 and quire-rs#394 make both refusals silent, so nothing *names* the key or the path. The FR's Behavior section says so and calls it an explicit expected failure, but the acceptance criterion does not, and TC-094 carries the caveat only in a parenthetical. An AC that reads as passing while its own FR says it cannot is the shape that produces a green matrix over an unverified claim. Split it: AC-6a (the refusal happens) verified by Test, AC-6b (the refusal names the offender) carried as a strict expected failure naming the two issues. | FR-010-AC-6, TC-094 | correct-requirement-no-evidence |
| FND-003 | medium | `quoin advise` flags NFR-001-AC-5 authored `Demonstration` against `bdd-spec-by-example`, `negative-abuse-testing`, `unit-testing`. `Demonstration` is defensible — it runs two whole external repositories and compares finding sets — but the catalog has no method for "re-validate a consumer against a candidate module version", which is why the advisor reaches for unit testing. That is a catalog gap in this module's own `verification_catalog`, and this module owns it (FR-007). Record the gap; do not silently accept a recommendation that does not fit. | NFR-001-AC-5, FR-007 | missing-requirement |
| FND-004 | medium | Six criteria assert a property of *every* member of a set — FR-009-AC-2, FR-009-AC-3, FR-010-AC-2, FR-011-AC-2, FR-012-AC-4, FR-013-AC-2 — and their test rows are `Unit`. That is right only if the test enumerates the population from the manifest or the emitted bundle rather than from a hard-coded list. Make enumeration-from-source a stated obligation of those tests; a hard-coded list silently stops covering the type added after it was written. | FR-009-AC-2, FR-009-AC-3, FR-010-AC-2, FR-011-AC-2, FR-012-AC-4, FR-013-AC-2 | implementation-bug-despite-evidence |
| FND-005 | medium | FR-012-AC-9 asserts `quire coverage` mints no id from `tests/fixtures/`, verified `Unit`. Coverage minting is an engine behaviour over the whole repository, not a unit of this module; the honest method is `Integration`, and the existing TC-033 already runs `quire coverage` over this repo for exactly this class of claim. Retype TC-119 or fold it into TC-033's pattern. | FR-012-AC-9, TC-119, TC-033 | wrong-requirement |
| FND-006 | low | No criterion in the set is verified by `Analysis`, and two would be better served by it: FR-013-AC-2 (no model declares a run property) is a structural analysis over the emitted schemas, and FR-011-CON-2 (mapping totality) is a closure check. Both are currently `Test`, which is acceptable; noting that the module's own catalog has the `Analysis` class and this set never reaches for it. | FR-013-AC-2, FR-011-CON-2 | correct-requirement-no-evidence |
| FND-007 | low | Every new matrix row is `Status: 🚧` and the engine's status-lie check therefore has nothing to catch yet. The check only becomes meaningful when the rows flip; until then this set has no evidence at all, which is correct for a pre-implementation review and is stated so the 🚧 count is not mistaken for partial coverage. | spec/tests.md | correct-requirement-no-evidence |
