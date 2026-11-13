---
id: SR-20261113192027
title: "PLAT-1688 spec-artifacts-process PR151 gap-analysis"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process PR151 @637685d over origin/main; FR-017-AC-4..9, FR-007-AC-17, TC-220..226, tests/test_adr_links.py, tests/test_criticality_field.py"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-017"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/FR-007"
    type: references
---

## Summary

Ticket: PLAT-1688 (also the spec-artifacts-process part of PLAT-1597). Plan completion: not assessed (planless). This is a scoped gap analysis of the amended criteria FR-017-AC-4 to AC-9 and the new FR-007-AC-17, against their tagged tests. Each test was mutated against the manifest. It also covers the AC-strength and ceremony check that the brief asked for on the two amendments.

Each criterion has one tagged test, and all pass on the PR head (11 passed). The bindings from TC-220 to TC-226 are correct. TC-221, TC-223, TC-225 and both TC-226 tests fail under the matching mutation. TC-222 does not (FND-001). TC-224 does not test the "fails" clause of its AC (FND-002). Neither amendment adds ceremony: no standard is named, there is no pin or digest, and the fixtures are this repository's own.

## Verdict

**CHANGES REQUESTED.** The criticality criterion is properly covered. Two FR-017 tests do not check what their criteria claim, and FR-007-AC-17 leaves the other requirement-derived sources unrated without saying why.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | TC-222 (FR-017-AC-6) passes when `realizes_requirement` is set to `[FR]` or `[part]`. The engine never checks the kind of an artifact-type target (code-review FND-001), so this test cannot fail through the property it is meant to guard. Only the static TC-221 catches a narrowed target list. Fix: once the engine checks artifact-type targets, the test holds as written; until then the behavioural half of AC-6 is unverified. | tests/test_adr_links.py:105, spec/functional/FR-017-adr-design-realization-verb.md:49 |
| FND-002 | medium | TC-224 (FR-017-AC-8) asserts only that one line contains `dangling-reference`, `'realizes_requirement'`, `ADR-003.md` and `FR-999`. It checks neither the exit status nor that the line is an error and not a `warning:`. Without `--strict`, the same line prints as a warning and the test would still pass. The invalid fixture's strict run also fails for an unrelated `unowned-quality-characteristic` error, so the exit status would not isolate the dangling reference either. Fix: assert a non-zero return code and a line without the `warning:` prefix, and keep the fixture free of other strict errors. | tests/test_adr_links.py:123, spec/functional/FR-017-adr-design-realization-verb.md:51 |
| FND-003 | medium | PLAT-1597 AC 1 reads "an obligation derived from a requirement with `criticality: high` carries `high`". FR-007-AC-17 rates only the two criterion sources. Measured: `FR-001-CON-1` (constraint source) of a `criticality: high` FR, and `NFR-001-M-1` (nfr-metric) of a `criticality: low` NFR, both carry no `criticality`. `configuration-matrix` (FR) declares no key either. The ticket's Outcome speaks of acceptance criteria, so excluding these may be intended, but FR-007 does not say so. Fix: add `criticality_field` to those sources, or state the exclusion and its reason in FR-007. | spec/functional/FR-007-verification-method-catalog.md:204, spec_artifacts_process/manifest.yaml:1331 |
