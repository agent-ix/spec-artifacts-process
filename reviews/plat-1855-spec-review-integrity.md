---
id: SR-20261115175475
title: "PLAT-1855 spec-artifacts-process PR163 spec-review integrity"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-artifacts-process PR163 @b4fdfc2; spec/functional/FR-019-adr-segregation-verb.md, spec/functional/index.md, spec/spec.md, spec/tests.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-019"
    type: references
---

## Summary

Ticket: PLAT-1855. Integrity review of the new FR-019, its index and scope entries, and TC-248/TC-249. `quire validate --scope .` over FR-019, `spec/tests.md`, `spec/spec.md` and `spec/functional/index.md` exits 0. FR-019, TC-248 and TC-249 do not collide with origin/main or with open PRs #123 and #58. FR-019 depends on FR-001, FR-017 and spec-objects-architecture FR-016, which matches its Dependencies section. The scope line in `spec/spec.md` and the index entry are consistent.

## Verdict

**CHANGES REQUESTED.** FR-019-AC-5 asserts behaviour that quire-rs FR-041 contradicts once the verb is declared (FND-001).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-019-AC-5 says `quire validate` of an `ADR` that authors `requirement_segregated_by` reports `disallowed-edge-type`. quire-rs FR-041-AC-2 makes a declared inverse label type-allowed regardless of the archetype's `allowed_links`. Once spec-objects-architecture FR-016 declares the verb with that inverse, which is the state this FR exists for, the ADR draws no finding (measured with architecture PR #60 head beff9a8). The AC is true only while the verb is undeclared, so it is not a property of this module. FR-017 keeps the inverse at manifest level only (FR-017-AC-2), which FR-019-AC-2 already copies. Fix: delete AC-5 and its TC-249 clause. | spec/functional/FR-019-adr-segregation-verb.md:47, spec/tests.md:232 |
| FND-002 | low | The third Behavior bullet requires the `ADR` `allowed_links` to keep "every verb it listed before this requirement", but AC-3 checks only `realizes_requirement`. FR-017-AC-4 already guards the four older verbs. Fix: narrow the bullet to `realizes_requirement`, or cite FR-017-AC-4. | spec/functional/FR-019-adr-segregation-verb.md:37 |
