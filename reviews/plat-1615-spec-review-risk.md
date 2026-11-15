---
id: SR-20261115175464
title: "PLAT-1615 PR157 spec-review risk and complexity"
type: SpecReview
analysis: risk-complexity
scope: "agent-ix/spec-artifacts-process PR157; spec/functional/FR-018-dossier-document-archetype.md"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-018", type: references}
---

## Summary

Ticket: PLAT-1615. Risk and complexity check of the FR-018 amendment. The change is additive. It widens a closed enum and adds one conditional requirement. No existing valid document becomes invalid, and the only existing document that becomes valid is the invented `bad-kind` fixture's old value `verification-report`, which is now an intended kind.

The vocabulary stays closed by design: line 59 makes the frontmatter schema the only validation authority. Each future dossier kind therefore needs a release of this module before the producer can emit it. FR-191 already sequences this ("selectable when its generator is registered"). The per-kind `as_of` rule grows by two statements and two schema blocks per kind; code-review SR-20261115175456 FND-002 covers the duplication, so it is not repeated here.

## Verdict

**PASS.** The change is low-risk and additive, and its volatility is handled by the producer-side registration rule.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |
