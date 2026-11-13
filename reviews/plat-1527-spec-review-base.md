---
id: SR-20261112181938
title: "Base review of PLAT-1527 Anomaly severity and fix verification links"
type: SpecReview
analysis: base
scope: "agent-ix/spec-artifacts-process PR145 @67f6422 over origin/main; spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md, spec/functional/FR-015-anomaly-safety-impact-assessment.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-014"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/FR-015"
    type: references
---

## Summary

Ticket: PLAT-1527. Base checklist review of PR #145, a spec-only change that
adds a person-assigned `severity` to the `Anomaly` type (FR-014, AC-14..17)
and a `## Fix Verification` table required when `resolution` is `fixed`
(FR-015, AC-11..16). Scope is `git diff origin/main...HEAD`.
`quire validate --scope . "spec/**/*.md"` reports no diagnostic on FR-014 or
FR-015, and `quire matrix` mints all ten new criteria (untagged, or
`method-without-symbol` for the two Inspection criteria, as expected before
implementation).

Examined: FR-014 Description, Inputs, the seven new severity bullets, the
amended skeleton, mapping and `AnomalyFields.json` bullets, FR-014-AC-7 and
AC-14..17; FR-015 Description, the two new ownership rows, the five new
Behavior bullets and FR-015-AC-11..16. Context only: FR-014-AC-1..13,
FR-015-AC-1..10, the `Anomaly` archetype and `anomaly-assessment` trace
declaration in `spec_artifacts_process/manifest.yaml`, the skeleton
`skeletons/Anomaly.md`, quire-rs FR-049 (kind-typed references,
FR-049-AC-13/14), and the companion quoin PR #854 (FR-136 `fixingChange`).

Checks the brief asked for:

- Severity has no default, is never derived, and is required from `assessed`
  on: stated (FR-014 lines 66-73) and tested for presence (AC-15) and no
  default (AC-14, AC-17). "Never derived" has no criterion (FND-003).
- A `fixed` resolution links a verifying test or criterion: stated and
  tested (FR-015-AC-12, AC-13), but the `Test` row contract cannot be met by
  the reference mechanism it names (FND-001), and its shape is undefined
  (FND-002).
- No recorded hashes: none authored. The fix is read from git history by
  quoin FR-136 (`fixingChange`, derived, not authored); FR-015-AC-16 forbids
  any hash, author or date field. No hash/digest/pin antipattern.
- No compatibility layer: none. Existing `assessed`+ anomalies without
  `severity`, and `fixed` ones without the section, simply start failing.
- No paywalled text: none quoted or paraphrased (no IEC 62304, ISO 14971 or
  IEEE 1044 text).
- `minor`/`major`/`critical`: sound. It is disjoint from the SpecReview
  `low`/`medium`/`high` scale, and AC-16 deliberately rejects `high` and
  `Major`, so the two scales cannot be confused.
- No overlap with PR #144 (PLAT-1499, FR-003, FR-004, spec/tests.md): no
  shared file, no FR or AC id collision, and this PR adds no TC id.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-015 says a `Criterion` row's `Target` resolves and kind-checks "through the same quire-rs FR-049 reference mechanism as the assessment", while a `Test` row's `Target` (a path, optionally `::symbol`) is checked for shape only. FR-049 cannot express that split over one `Target` column. A row whose `Kind` is not in `kind_targets` is still resolved against the union (FR-049-AC-13), so with the assessment-style pattern `tests/test_login.py::test_lockout` extracts `tests`, `test_login`, `py`, `test_lockout`, each a `dangling-trace-reference`, and FR-015-AC-13's valid fixture fails. Only a cell that matches no pattern is exempt (FR-049-AC-14). A pattern that matches criterion ids alone would exempt the path, but then a `Criterion` row targeting the hazard (or `FR-001`) extracts nothing and AC-13's kind-mismatch case cannot fire. No Behavior bullet or AC requires the manifest to declare a `Fix Verification` reference declaration either (AC-11 covers table shape only). Fix: make a `Test` row's `Target` a resolvable test-case id, with `kind_targets` `Test: [test-case]` and `Criterion: [acceptance-criterion, nfr-acceptance-criterion]`, which also makes the test link checkable. Or put criteria and tests in separate columns, with only the criterion column declared as a reference. Then state the declaration and add it to AC-11. | spec/functional/FR-015-anomaly-safety-impact-assessment.md:91-99; spec/functional/FR-015-anomaly-safety-impact-assessment.md:126; spec_artifacts_process/manifest.yaml:1142-1155 |
| FND-002 | medium | The `Test` target format is not defined well enough to check. FR-015 says the module "checks its shape only" and gives "a repository-relative path, optionally followed by `::` and a symbol", but FR-015-AC-14 tests only an empty `Target`. One implementer accepts any non-empty string. Another rejects `test_lockout` (no path), `/abs/tests/x.py`, `TC-042` or a Rust `crate::module::test` id (not a file path). The format choice is also weak for this ecosystem, which identifies tests by TC ids and criterion trace tags rather than file paths. A free-text path that the module neither resolves nor checks means a `fixed` anomaly can be satisfied by any string. Either state that the shape check is exactly "non-empty after trimming" and drop the parenthetical as normative text, or adopt a resolvable test identifier (see FND-001) and test a malformed one in AC-14. | spec/functional/FR-015-anomaly-safety-impact-assessment.md:96-99; spec/functional/FR-015-anomaly-safety-impact-assessment.md:127 |
| FND-003 | medium | "The module SHALL NOT derive `severity` from any other field" has no criterion. FR-014-AC-14 and AC-17 cover the absence of a default and of a setter field only, so the derivation rule is never tested: a rule that, say, required `critical` for `safety_impact: impacting` would pass every AC. Add a criterion, for example: fixtures with `severity: minor` and `safety_impact: impacting`, and with `severity: critical` and `safety_impact: none`, both validate, and the mapped `severity` equals the authored value. | spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:69; spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:123-126 |
| FND-004 | medium | "declared in the manifest `vocabularies`" is ambiguous. The manifest's only `vocabularies` block is `traceability.vocabularies` (test-type values), and the other `Anomaly` vocabularies (`status`, `resolution`, `safety_impact`) are `assert: choices` on `yield_pattern.match` locators. One implementer adds a traceability vocabulary, another adds a `choices` assert. Only the second yields AC-16's finding at the `severity` line, and only a `severity` `frontmatter_field` locator puts the key into the extracted record that `AnomalyFields.json` checks. No Behavior bullet or AC names that locator; AC-10 names only `closed_by`. State that `severity` is a `frontmatter_field` locator (`required: false`) with `assert: choices: [minor, major, critical]`, and extend AC-14 or AC-10 to it. | spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:66-67; spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:85-88; spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:123 |
| FND-005 | medium | FR-015-AC-13 tests a `Criterion` row targeting a dangling criterion and one targeting the hazard, but not one targeting an existing requirement document such as `FR-001`. Naming the FR instead of its criterion is the most likely authoring mistake, and the Behavior bullet says the target must be an acceptance criterion. Without this case an implementation that puts `requirement-document` in the `Criterion` kind subset passes every AC. Add `FR-001` on a `Criterion` row as a kind-mismatch case. | spec/functional/FR-015-anomaly-safety-impact-assessment.md:92-96; spec/functional/FR-015-anomaly-safety-impact-assessment.md:126 |
| FND-006 | low | FR-015's Inputs and Outputs were not updated. Inputs lists `safety_impact`, `status` and the `## Safety Impact Assessment` section only, but the new rules read `resolution` and `## Fix Verification`. Outputs names the missing assessment, the dangling link and the missing module, but not a missing verification section. The FR-015 fixture bullet also still lists the negatives of AC-3 to AC-8 only, not those of AC-12 to AC-14 (FR-014's fixture bullet covers them only indirectly, as "the negatives of FR-015"). | spec/functional/FR-015-anomaly-safety-impact-assessment.md:41-53; spec/functional/FR-015-anomaly-safety-impact-assessment.md:84-86 |
| FND-007 | low | "No default for `severity`" is asserted twice: FR-014-AC-14 ("and no default") and AC-17 ("The manifest and `AnomalyFields.json` define no default"). Keep the default check in one criterion, preferably AC-17, which already names both files. | spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:123; spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:126 |

## Verdict

FAIL. FND-001 is high: FR-015-AC-13's valid fixture cannot pass under the
reference mechanism the FR names, so the `Test` half of the fix-verification
contract has to be redesigned (preferably to a resolvable test-case id)
before implementation. FND-002 to FND-005 are medium wording and coverage
gaps. The severity design is sound: no default, person-assigned,
present from `assessed` on, history from git, and a vocabulary disjoint from
the review severity scale. The no-hash, no-verdict and no-compatibility-layer
choices are also sound, and quoin FR-136 deriving the fixing change from git
history is the right owner for it.

## Dispositions
