---
id: SR-20261102086814
title: "PLAT-277 process PR134 spec-review integrity"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-artifacts-process PR134 @9878e24 over origin/main 9fc6a8b; spec/functional/FR-010-semantic-manifest-contract.md, spec/spec.md, spec/tests.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-010"
    type: references
---

## Summary

Ticket: PLAT-277. Spec review of rewritten FR-010-AC-8, new FR-010-AC-10, TC-096,
TC-167, the two new FR-010 Behavior bullets and the spec.md Standard paragraph.
The spec.md paragraph is accurate after the change: the `standard` object type
is governed by its locator and the artifact type by `Standard.json`, and the
removed `DuplicateArchetype` sentence no longer applies. TC-096 and TC-167 rows
match their criteria and the coverage table.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-010's title says "without altering an archetype", and its Description says "every existing archetype contract keeps the exact meaning it has today". This PR changes one contract and five names: it drops the `standard` object type's record schema and renames five `archetypes:` entries. The FR now contradicts its own Behavior bullets. Restate the Description so it allows these two deliberate changes. | spec/functional/FR-010-semantic-manifest-contract.md:3; spec/functional/FR-010-semantic-manifest-contract.md:19-22; spec/functional/FR-010-semantic-manifest-contract.md:54-64 |
| FND-002 | medium | FR-010-AC-10 joins two independent conditions: names are unique across sections, and no declaration is inline. The second clause also gives the wrong location for the schema. "No declaration carries an inline `data_schema` under the `semantic` block" reads as if `data_schema` sits inside `semantic:`, but it sits on each `artifact_types`/`object_types` entry. The object-type half has no Behavior bullet of its own; the existing bullet covers artifact types only (line 46). Split the criterion into two, and say "no `artifact_types` or `object_types` entry carries an inline `data_schema`". | spec/functional/FR-010-semantic-manifest-contract.md:89; spec/functional/FR-010-semantic-manifest-contract.md:46 |
| FND-003 | low | The new Behavior bullet gives as its reason an engine behaviour, "Quire loads all three sections into one archetype registry". It then fixes six display names as the workaround and names no owning quire-rs ticket. FR-010 records every other engine limitation with its ticket (`agent-ix/quire-rs#221`). Without a ticket, the rename reads as the intended design rather than a workaround for an engine limitation (see the code-review SR, FND-003). | spec/functional/FR-010-semantic-manifest-contract.md:59-64 |
| FND-004 | low | In the Acceptance Criteria table, FR-010-AC-10 comes before FR-010-AC-9. | spec/functional/FR-010-semantic-manifest-contract.md:88-90 |

## Verdict

**CHANGES REQUESTED.** FND-001 and FND-002 are wording fixes in FR-010. The
TC rows and the spec.md paragraph are clean.

## Examined scope

```yaml
scope:
- {id: FR-010-AC-8, path: spec/functional/FR-010-semantic-manifest-contract.md, role: examined}
- {id: FR-010-AC-10, path: spec/functional/FR-010-semantic-manifest-contract.md, role: examined}
- {id: TC-096, path: spec/tests.md, role: examined}
- {id: TC-167, path: spec/tests.md, role: examined}
- {id: spec.md Standard paragraph, path: spec/spec.md, role: examined}
- {id: FR-010, path: spec/functional/FR-010-semantic-manifest-contract.md, role: examined}
```

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | 46221a1 retitles FR-010 to "Declare the semantic-module contract in the manifest" (index.md and spec.md updated to match). The Description now reads "...keeps the exact meaning it has today, except one: the `standard` object type carries no record schema and is validated by its locator and the `Standard` frontmatter schema". With the renames reverted, that wording is true. |
| FND-002 | fixed | Fixed by removal: FR-010-AC-10 is dropped. |
| FND-003 | fixed | Fixed by removal: the rename Behavior bullet is dropped, and the engine cause moves to quire-rs. |
| FND-004 | fixed | Fixed by removal: AC-10 no longer exists, so the table order is AC-1, 5, 6, 8, 9. |
