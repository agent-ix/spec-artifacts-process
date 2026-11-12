---
id: SR-20261102086815
title: "Base review of PLAT-1414 Anomaly archetype and safety-impact assessment"
type: SpecReview
analysis: base
scope: "agent-ix/spec-artifacts-process PR139 @36754ea over origin/main; spec/usecase/US-003-track-anomalies-with-safety-impact.md, spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md, spec/functional/FR-015-anomaly-safety-impact-assessment.md, spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md, spec/spec.md, spec/*/index.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-014"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/FR-015"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/NFR-001"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/US-003"
    type: references
---

## Summary

Ticket: PLAT-1414. Base checklist review of PR #139, a spec-only change that
adds US-003, FR-014, FR-015 and NFR-001 and indexes them. Scope is
`git diff origin/main...HEAD`. `quire validate --scope . "spec/**/*.md"`
exits 0 with no diagnostic on the new files. `quire matrix` lists the new FR
criteria as `untagged`, which is expected before implementation, and warns
`section-matches-nothing` for NFR-001.

IDs are well formed and do not collide with main. US-003 uses the story form.
FR-014 and FR-015 link to US-003 and state inputs, outputs, behaviour and
error paths, and every FR criterion can fail. FR-015's explicit refusal to add
a risk-acceptance or sign-off field fits the rule that people, not the tool,
accept risk.

The defects are in the record design and in NFR-001. FR-014's `## History`
table is a hand-typed audit trail (who, when, which state change) that git
already holds, and its "named person" check is a placeholder denylist that
any typed string passes. NFR-001 asks for one fixture that combines defects
that cannot coexist in one document, and it has no Acceptance Criteria
section, so it mints nothing.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-014 makes the `## History` table (`From, To, By, Date, Note`) the audit trail of the anomaly: who moved it to which state and when, typed by hand into the document. That is a second record of what git already records for the file (the commit that changed `status`, its author, its date, and a signature where commits are signed). A hand-typed `By` and `Date` can be written by anyone, including an agent, and validation cannot tell a true row from a made-up one. So the closure attribution US-003 asks for ("a named person standing behind the closure") is not actually backed by anything. Take attribution and dates from the git history of the `status` field (the commit that sets `closed`), or state that FR-014 checks only the shape of the record and leave attribution to signed commits. Do not ship a parallel ledger. | spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:35-47; spec/usecase/US-003-track-anomalies-with-safety-impact.md:15 |
| FND-002 | medium | "Every row's `By` SHALL name a person" is checked only against the denylist `n/a, none, unknown, tbd, -`. Values such as `x`, `nobody`, `TBA`, `?`, `N/A.` or `agent` pass, so the check passes in the state it is meant to catch. FR-014-AC-7 tests only the `closed` row, so nothing tests the rule on the other rows, and the "closing requirement" and "attribution rule" wording describes one check twice. Either bind `By` to a real identity (see FND-001), or reword the statement to what it really checks ("non-empty and not a placeholder token") and test that on a non-`closed` row as well. | spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:45-48; spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:66 |
| FND-003 | high | NFR-001 measures "one fixture with one defect of each kind in FR-014-AC-4 to AC-8 and FR-015-AC-3 to AC-8", validated once. Those defects cannot all exist in one document. FR-015-AC-3 (no assessment section) excludes the row defects of FR-015-AC-5, AC-6 and AC-8. FR-015-AC-7 needs both `safety_impact: impacting` and `safety_impact: none`. FR-014-AC-5's first-row defect and AC-4's transition defects interact through the same chain. The measurement cannot be carried out as written. The second metric ("100% of defects carry a document line") also cannot be met for defects that are absences (a missing section has no line) unless the line is defined, for example as the frontmatter `status` line. Specify a small set of fixtures, each combining the defects that can coexist, and define the line reported for an absence. | spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md:15-38 |
| FND-004 | medium | NFR-001 has no `## Acceptance Criteria` section. `quire matrix` reports `section-matches-nothing` for declaration `nfr-acceptance-criterion` on this file, so the NFR mints no criterion and no test can ever be tagged to it. Add an Acceptance Criteria table (for example NFR-001-AC-1 and AC-2 for the two metrics). | spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md:13-38 |
| FND-005 | medium | FR-015 requires the single `None` row of a `safety_impact: none` anomaly to have `Target` `-` and a rationale, but does not say what its `Impact` cell holds. `Impact` must be one of `Affects, Mitigates, Introduces, Reviewed - unaffected`, and none of these clearly fits "no safety impact". One implementer will require `Reviewed - unaffected`, another will accept any value, and a third will expect `-`, which the Impact vocabulary rejects. State the required `Impact` for a `None` row and add it to FR-015-AC-7. | spec/functional/FR-015-anomaly-safety-impact-assessment.md:42-51; spec/functional/FR-015-anomaly-safety-impact-assessment.md:65 |
| FND-006 | low | FR-015 allows a `Requirement` row to target an acceptance-criterion id, not only an FR or NFR id, but no criterion exercises an AC-id target or a dangling AC id (FR-015-AC-4 and AC-5 use only `FR-001` and `FR-999`). Add an AC-id case to AC-4 and AC-5, or drop AC ids from the statement. | spec/functional/FR-015-anomaly-safety-impact-assessment.md:43-44; spec/functional/FR-015-anomaly-safety-impact-assessment.md:62-63 |
| FND-007 | low | spec.md's In Scope bullet still says "the 12 artifact types the manifest declares" and lists them, while the new bullet adds `Anomaly` as a further type. The two bullets now disagree about how many types the manifest declares. Fold `Anomaly` into the list, or drop the count. | spec/spec.md:29-30 |

## Verdict

FAIL. Two high findings (the hand-maintained History ledger and an NFR
measurement that cannot be carried out) and three medium findings must be
fixed before the spec is ready for implementation. The FR-015 assessment
design and the error-path coverage of FR-014 and FR-015 are otherwise sound.
