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
