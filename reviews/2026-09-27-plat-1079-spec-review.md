---
id: SR-018
title: "Spec review of PLAT-1079 — mint constraint and retire TC verification refs"
type: SpecReview
analysis: base
scope: "agent-ix/spec-artifacts-process@96080f274c171c3bbab17b6379c67b681611cd98; spec/functional/FR-004-traceability-declaration.md, spec/functional/FR-007-verification-method-catalog.md, spec/tests.md, spec/log.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-004"
    type: "reviews"
  - target: "ix://agent-ix/spec-artifacts-process/FR-007"
    type: "reviews"
---
# SR-018: Spec review of PLAT-1079 — mint constraint and retire TC verification refs

## Summary

Ticket: PLAT-1079 (epic PLAT-1076), PR spec-artifacts-process#105, head 96080f2.
Reviewed the base checklist over the diff: FR-004-AC-20/21, the new FR-004
normative bullets, the CR-064 note and Known Limits, FR-007-AC-15 and its CR-006
note, TC-148..150 and the log entry. The structural lens is in SR-019.

Measured with quire 0.33.0 (engine 0.47.1@92dbebc4) and quoin 0.24.1:
`quire validate --okf --scope .` exits **0**, with 77 warnings on the branch
against 76 on `origin/main` a723c22. The one new warning is FR-007-AC-15 being
dangling (see SR-019 FND-001). The CR-064 measurement is accurate: 13
`dangling-trace-reference` warnings name a `-CON-` id, and `manifest.yaml`
declares neither a `constraint` trace target nor a `constraint` obligation.

The constraint half is sound in intent. The name `constraint` collides with no
declared target, reference or obligation. The TestMatrix `## Constraint Boundary
Tests` table (tests.md:333) is not a declared reference, so it does not collide.
Its `Constraint` column is simply never checked, which this PR leaves as it was.
`US-002`'s `## Constraints` table is correctly outside an `archetype: FR` target.

The TC-retirement half (FR-004-AC-21) cannot be implemented as written.

## Verdict

**NOT READY.** FND-001 blocks: the specified manifest change fails module load
in the engine this repo pins. FND-002..FND-005 must be settled in the spec before
the implementation stage, or that stage will either fail TC-091 or leave the
repo with about 156 new warnings the spec never planned for.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-004-AC-21 mandates `targets: []` on `verification`/`nfr-verification`, but quire-rs rejects an empty `targets` at module load ("document_references entry '…' declares no targets", src/traceability.rs:1014 @92dbebc, the installed engine). As written, the implementation makes the module fail to load for every consumer instead of reporting a dangling reference. | spec/functional/FR-004-traceability-declaration.md:55-64, :123; spec/tests.md:313 |
| FND-002 | medium | AC-21 names no severity. Even if an empty target set were admitted, `dangling-trace-reference` is warning-tier and `quire validate --okf` exits 0 (measured), so the ruled "TC in Verification becomes a finding" is a non-failing warning mixed among about 77 others. Specify the mechanism and severity directly, for example a `Verification` column `assert` pattern in FR/NFR `body_extraction` that rejects `TC-`/`IT-` ids at a stated severity. | spec/functional/FR-004-traceability-declaration.md:55-64, :123 |
| FND-003 | medium | The new SHALL ("a `Verification` cell SHALL name a method only") is violated by 156 `TC-` ids across this repo's FR/NFR AC tables. That includes the three rows this PR itself authors: FR-004-AC-20 `Test (TC-148)`, FR-004-AC-21 `Test (TC-149)` and FR-007-AC-15 `Test (TC-150)`. No AC, TC or plan note covers sweeping them, so implementing AC-21 immediately produces about 156 findings in this repo and many more in consumers. The manifest's own sweep note counts 99 `Test (TC-nnn)` in quire-rs/quoin/this repo. | spec/functional/FR-004-traceability-declaration.md:59-62, :122-123; spec/functional/FR-007-verification-method-catalog.md:258 |
| FND-004 | medium | FR-004-AC-20 asserts that every `-CON-` `Traces To` reference resolves, but it only declares the target. Resolution also requires adding `constraint` to `traces-to`'s `targets` (manifest.yaml:948), and to `inspection-obligation` (manifest.yaml:896-899) so an Inspection-validated constraint can be discharged by an `Inspections` record. Neither change is stated, so the declared change alone fails TC-148. | spec/functional/FR-004-traceability-declaration.md:50-54, :122; spec/tests.md:312 |
| FND-005 | medium | FR-004 says `interface-verification` is "unaffected in shape — same pattern, same empty `targets`". The manifest has `targets: [test-case]` (manifest.yaml:937), and AC-21 names only `verification`/`nfr-verification`. Whether a `TC-` id in an `interface` Verification cell is reported or still silently resolves is therefore contradictory. Under the epic-wide TC retirement it should be reported like the other two. | spec/functional/FR-004-traceability-declaration.md:62-64 |
| FND-006 | low | Minting `constraint` as an evidence-bearing target adds every `-CON-` row to the coverage denominator. About half of this repo's constraints are `Inspection` (FR-008-CON-1..3, FR-009-CON-1/2, FR-011-CON-3, FR-013-CON-2, FR-003-CON-1), and no test tag can back them. AC-20 does not say whether the target is `evidence: reference_only` or how the unbacked count is expected to move. The manifest note at manifest.yaml:1041-1045 also records that prose-bound CON tags were harmless only because CON was never minted. | spec/functional/FR-004-traceability-declaration.md:50-54, :122 |

## New findings (disposition pass 1)

Reviewed at 50350b611cba63ae51cc43032601c1762ed13fbe. `quire validate --okf --scope .` exits 0 with 73 warnings. None of them names a `-CON-` id, or FR-004-AC-20/21 or FR-007-AC-9/10/11/15.

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-007 | medium | The lint rule's allowed list (`Test`/`Inspection`/`Analysis`/`Demonstration`) equals the catalog's `class` set, but not the catalog's 33 method ids. The same `Verification` cell is the `method_column` of the `acceptance-criterion` obligation, and quire-rs FR-054-AC-11 accepts a catalog method id **or** a class there. FR-007 CR-005 steers authors to the precise method (`property-based-testing`, `fuzzing`, `agent-behaviour-eval`). Failure scenario: an author follows FR-007 and writes `property-based-testing`; the obligation resolves to a catalog method, and the new rule still warns. `Eval`/`Manual` are `test_type` values, not catalog entries, so their absence is correct. Allow the classes plus the catalog keys, derived from the manifest and asserted equal by the test. | spec/functional/FR-004-traceability-declaration.md:67-68, :154; spec/tests.md:313 |
| FND-008 | medium | The new rule duplicates and contradicts `spec-artifacts-iso`'s existing `ac-verification-method` rule (spec-artifacts-iso manifest.yaml:795-803 @c654673). Both have the same archetypes, section, column and allowed set, but iso admits a `(TC-\d+(, TC-\d+)*)` annotation. The registry merges `lint_rules` from every loaded module, so `Test (TC-035)` passes iso's rule and fails this one. That leaves two modules declaring opposite contracts for a column iso owns. Either change iso's rule (drop `annotation_pattern`) or have FR-004 record the override and the iso change it requires. | spec/functional/FR-004-traceability-declaration.md:66-81, :154 |
| FND-009 | low | FR-004 defers clearing the ~156 existing cells and the warning-to-error promotion to "the epic's own sweep ticket" without naming it. The leader's ruling names PLAT-1082 for the promotion. Name the owning ticket or tickets so the deferral can be checked. | spec/functional/FR-004-traceability-declaration.md:83-88; spec/log.md:19 |

## Dispositions

| FND | Outcome | sha/reason |
| --- | --- | --- |
| FND-001 | fixed | 50350b6 — `targets: []` dropped; the three verification references are unchanged and the rule is now a `lint_rules` `table_column_values` entry (FR-004:66-81, :154) |
| FND-002 | fixed | 50350b6 — `severity: warning` stated in FR-004:83 and AC-21; validate exit code stated as unaffected |
| FND-003 | deferred | Leader ruling 2026-09-27: the epic's sweep clears existing cells and the rule ships at warning. This PR's own three rows are fixed in 50350b6 (bare `Test`, FR-004:153-154, FR-007:204); the remaining ~153 cells are still present |
| FND-004 | fixed | 50350b6 — `constraint` added to `traces-to` and `inspection-obligation` targets (FR-004:61-65, AC-20 :153) |
| FND-005 | fixed | 50350b6 — all three verification references are left unchanged, and the lint rule is scoped to FR/NFR/interface uniformly (FR-004:76-81) |
| FND-006 | fixed | 50350b6 — the target is evidence-bearing (`source`), with Inspection rows reported under `method-without-symbol` (FR-004:54-60, AC-20) |
| FND-007 | fixed | e34aba7 — `allowed` is the classes plus the `verification_catalog` keys, derived from the manifest, with an equality test (FR-004:81-94, AC-21/AC-22 :179-180, TC-151); `Eval`/`Manual` are excluded |
| FND-008 | fixed | e34aba7 — FR-004:109-120 states this module owns the column contract; PLAT-1085 (exists, Backlog) removes iso's `ac-verification-method` and the StR TC annotation, and ships together under a SHALL; Dependencies records "Ships with" |
| FND-009 | fixed | e34aba7 — FR-004:99-101 names PLAT-1081 (sweep) and PLAT-1082 (promotion); both tickets exist in Linear |

## New findings (disposition pass 2)

Reviewed at e34aba759c60530a30610fc5830d6f46054ee90b. `quire validate --okf --scope .` exits 0 with 73 warnings, unchanged from round 1. FR-004-AC-22 is minted. The 13 `-CON-` dangling warnings remain, as expected: this is a spec-only PR, and the manifest change lands in the implementation stage. I found no regression.

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-010 | low | FR-004 says "the rest of the 31 catalog keys", but `verification_catalog` declares **33** keys (measured; 31 was the 2026-08-17 seed count before CR-005 added `compile-time-check` and `dynamic-analysis-sanitizer`). The derived-set test in AC-22 is unaffected, but the normative prose states a wrong count. Drop the number or correct it to 33. | spec/functional/FR-004-traceability-declaration.md:85 |
