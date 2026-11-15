---
id: SR-20261115175462
title: "PLAT-1615 PR157 spec-review dependency"
type: SpecReview
analysis: dependency
scope: "agent-ix/spec-artifacts-process PR157; spec/functional/FR-018-dossier-document-archetype.md"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-018", type: references}
---

## Summary

Ticket: PLAT-1615. PR157 adds no `relationships:` edges; the FR-018 frontmatter is unchanged. The dependency check covered the `## Dependencies` section and the cross-repo ordering against the companion quoin PR (agent-ix/quoin#929, open). That PR amends FR-191 and adds FR-196 to FR-201 and NFR-041, which produce the six new kinds. FR-191 now names FR-018 upstream and says "A document kind becomes selectable when its generator is registered". So this module can accept a kind before quoin generates it, with no breakage in either merge order.

## Verdict

**PASS with one low finding.** No dependency is wrong or circular. The Downstream list leaves out the new consumers.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | Downstream still lists only quoin FR-191. The six M2 content FRs (quoin FR-196 to FR-201 in agent-ix/quoin#929) also emit `DossierDocument` with the new kinds, and FR-197 relies on the new `soup` → `as_of` rule, but they are not named as consumers. | spec/functional/FR-018-dossier-document-archetype.md:91 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1 (head 52170c3): Downstream now reads "quoin FR-191 and its M2 content requirements FR-196, FR-197, FR-198, FR-199, FR-200, FR-201", each as an `ix://agent-ix/quoin/` link (FR-018 line 92). |
