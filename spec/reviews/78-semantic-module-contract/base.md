---
id: SR-008
title: "base review of the #78 semantic-module contract spec set"
type: SpecReview
analysis: base
scope: "spec/spec.md, spec/usecase/US-002, spec/functional/FR-009..FR-013, spec/non-functional/NFR-001, spec/tests.md (TC-080..TC-131)"
review_set: all
---
# SR-008: base review of the #78 semantic-module contract spec set

## Summary

Checklist review of the seven artifacts authored for #78 (US-002, FR-009..FR-013, NFR-001) and the
52 Test Matrix rows TC-080..TC-131, run against the quoin `spec-review` checklist and three
automated passes: id format and uniqueness, AC→TC coverage, and structural validation. The set is
structurally clean — `quire validate --scope . "spec/**/*.md"` reports zero errors and
26/28 documents grammar-clean, with all nine remaining grammar findings in the pre-existing
FR-003 and FR-004 rather than in anything authored here. Every one of the 52 new acceptance
criteria has at least one test case, no test-case id is duplicated in the Test Case Summary, and
every new row traces to a requirement criterion rather than to another test case.

Seven findings. The one that matters is FND-001: thirteen Test Case Summary rows (TC-055..TC-070, with TC-058, TC-059 and TC-066 absent from the range)
are physically inside the `### Functional Requirement Coverage` table in this repository's own
`tests.md`. It is pre-existing, it predates this branch, and it is exactly the defect this module
exists to catch in other repositories — the leaf matrix of the module that owns the matrix
contract is malformed and its own validator does not see it, because `columns:` asserts headers
and not per-row arity.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | `spec/tests.md` lines 79-91: thirteen six-column Test Case Summary rows (TC-055, TC-056, TC-057, TC-060..TC-065, TC-067..TC-070) sit inside the four-column `### Functional Requirement Coverage` table. Pre-existing on `main`, invisible to `quire validate` because the `columns:` assert checks headers, not row arity. Relocated into `## Test Case Summary` on this branch under agent-ix/spec-artifacts-process#79; the general arity gap is filed as agent-ix/quire-rs#396. | spec/tests.md, FR-003-AC-1 | correct-requirement-no-evidence |
| FND-002 | medium | FR-009-CON-1, FR-009-CON-2, FR-011-CON-3 and FR-013-CON-2 are Inspection-verified constraints with no row anywhere in `tests.md`. The matrix already has the precedent form (`Inspection (plan gate, no TC)` on FR-003-CON-1); add a Constraint Boundary row for each so an Inspection obligation is recorded rather than absent. | FR-009-CON-1, FR-009-CON-2, FR-011-CON-3, FR-013-CON-2 | correct-requirement-no-evidence |
| FND-003 | medium | FR-013's frontmatter declares `depends_on ix://agent-ix/engineering-assurance/FR-001`, which is *Inventory before proposal* — not the requirement that owns evidence state. The intended target is `engineering-assurance` FR-004 (*Evidence state and provenance*) and FR-008 (*Distinguish verification semantics*). A dangling-in-meaning cross-repo edge is worse than none: it asserts a relationship the reader cannot check. | FR-013 | wrong-requirement |
| FND-004 | low | The `### Non-Functional Requirement Coverage` table groups NFR-001 by verification method, not by acceptance criterion, because the archetype's column set is `Non-Functional Req \| Verification Method \| Evidence/Test Cases \| Status` and carries no criterion column. Per-criterion coverage for NFR-001-AC-1..AC-5 therefore lives only in the `Traces To` cells of TC-127..TC-131. That is sound but undocumented; state it in the matrix Overview so a reader does not read the grouped table as the whole claim. | NFR-001, spec/tests.md | correct-requirement-no-evidence |
| FND-005 | low | All 52 new rows are authored `Status: 🚧`, correctly, because nothing is implemented yet. They must be flipped to `✅` only by the test that actually runs — a status marker moved by hand at the end of the change is the status lie this module's own coverage rollup exists to catch. Record the flip as a plan task rather than a tidy-up. | spec/tests.md | correct-requirement-no-evidence |
| FND-006 | low | US-002 declares no `## Priority and Risk` value beyond prose ("value high, urgency medium"), which the checklist asks for as an explicit priority. The US archetype makes the section informative, so this is a checklist-versus-archetype disagreement rather than a defect; recorded so it is not re-raised. | US-002 | missing-requirement |
| FND-007 | low | `spec/spec.md` In Scope now says "the 12 artifact types the manifest declares" where the previous text said 13 and named eleven. The count is now right and matches `manifest.yaml`, but nothing in the spec set asserts the count against the manifest, so the two can drift again. FR-010-AC-1 asserts `exports` equals the twelve names; add the same assertion against `artifact_types` so the prose count is machine-checked. | spec/spec.md, FR-010-AC-1 | correct-requirement-no-evidence |
