---
id: SR-20261115175454
title: "PLAT-1436 PR155 spec-review dependency"
type: SpecReview
analysis: dependency
scope: "agent-ix/spec-artifacts-process PR155; spec/functional/FR-018-dossier-document-archetype.md"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-018", type: references}
---

## Summary

Ticket: PLAT-1436. Checked FR-018's `relationships` and its Dependencies section. `depends_on` FR-001 (manifest activation) and FR-012 (executable skeletons) are correct enablement edges. quire-cli FR-034 (document identity) exists on quire-cli main. The `references` edge to quoin FR-188 points at a file that exists only on open PR agent-ix/quoin#924, not on quoin main. FR-018 delivers a record schema and a mapping, but it does not declare the requirements that govern them.

## Verdict

**CONDITIONAL.** The merge order is undeclared, and two enablement edges are missing.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The `references` edge to `ix://agent-ix/quoin/FR-188` dangles: FR-188 exists only on open quoin PR #924, so merging this PR first leaves a reference that does not resolve. | spec/functional/FR-018-dossier-document-archetype.md:10-11 |
| FND-002 | medium | FR-018 delivers a record schema and a mapping but has no `depends_on` to FR-009 (TypeSpec-projected schemas) or FR-011 (record mapping, including `provenance`); those contracts are the ones the implementation missed. | spec/functional/FR-018-dossier-document-archetype.md:5-11 |

## Examined scope

```yaml
scope:
  - {id: FR-018, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "relationships: depends_on FR-001; depends_on FR-012; references ix://agent-ix/quoin/FR-188"}
  - {id: FR-018-deps, path: "spec/functional/FR-018-dossier-document-archetype.md", role: examined, excerpt: "**Upstream**: FR-001, FR-012. **Downstream**: quoin FR-188"}
  - {id: FR-034, path: "quire-cli/spec/functional/FR-034-document-identity.md", role: context_only, excerpt: "quire-cli FR-034 document identity (exists on quire-cli main)."}
```
