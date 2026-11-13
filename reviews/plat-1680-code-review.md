---
id: SR-20261113084040
title: "PLAT-1680 spec-artifacts-process PR149 code-review"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR149 @14cf518 over origin/main; spec_artifacts_process/manifest.yaml, spec_artifacts_process/skeletons/ADR.md, spec_artifacts_process/examples/ADR.record.json, tests/test_adr_links.py, tests/fixtures/adr/**"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-017"
    type: references
---

## Summary

Ticket: PLAT-1680. Code review of the one-line manifest change that adds `realizes_requirement` to the `ADR` `allowed_links`, its test and three fixtures. The verb and direction match spec-objects-architecture FR-010 on main: the design element (part, connection, ADR) authors `realizes_requirement` toward the requirement, and the requirement authors `requirement_realized_by` toward the element. The relations are `incoming` with `to: [part, connection, ADR]`, so the ADR needs only the forward verb. The inverse belongs in the requirement archetype's `allowed_links`, not the ADR's, and leaving it out of the ADR list is correct.

Measured on the final head with quire 0.44.0: the `realizes_requirement` fixture draws no `disallowed-edge-type`, while the inverse and `bogus_verb` fixtures each draw it. All three exit 0, because the finding is advisory. The bogus fixture differs from the realizes fixture only in the verb, so the test tells the two cases apart. `make lint` passed (schema projection up to date, 75 files; ruff and black clean). `make test` passed: 498 passed, 1 skipped, 2 xfailed, 100% coverage.

## Verdict

**CHANGES REQUESTED (minor).** The manifest change, test and fixtures are correct. Commit 14cf518 reverted the skeleton comment to keep the golden record stable, and that left the ADR authoring contract stale (FND-001).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The ADR skeleton's authoring-contract comment lists `allowed_links` as supersedes, superseded_by, relates_to and depends_on, without `realizes_requirement`, so it now contradicts the manifest. The golden record copies the same stale text. Fix: restore the comment edit from e769098 and update the record's `body.text` (and `endLine`, if the line count changes) to match. | spec_artifacts_process/skeletons/ADR.md:17, spec_artifacts_process/examples/ADR.record.json |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | edab19a restores the skeleton comment (`allowed_links`: supersedes \| superseded_by \| relates_to \| depends_on \| realizes_requirement). ADR.record.json changes only `body.text`, `endLine` 53 to 54 and `provenance.digest`. The digest equals sha256 of skeletons/ADR.md, and the golden-record test (TC-142, deep equality against the mapper build) passes for ADR. |
