---
id: FR-008
title: "A Finding records which layer a defect escaped through"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-artifacts-process/FR-002"
    type: "extends"
---
# FR-008: A Finding records which layer a defect escaped through

## Description

Escape analysis is the only **empirical** validation of a completeness claim. Every other signal
this module produces says how much was written or how much was verified; a distribution of real
escaped defects says which layer is actually leaking, and nothing else does.

The infrastructure half-existed. A `Finding` artifact type was declared — `allowed_links`
`[found_in, blocks, references]`, a frontmatter schema, and the `review` archetype's composition
already expecting Finding children — but with **no `body_extraction` contract and no skeleton**.
So nothing emitted one, and had anything emitted one there would have been nothing to aggregate.

The module **SHALL** declare a body contract for `Finding` requiring a `Summary` and a
`Classification` table, and **SHALL** ship an authoring skeleton so the standard path works.

### The classification axis

`Classification` carries `Escape Cause | Detected In | Traces`, with `Escape Cause` drawn from
exactly four values. The four are a partition of *which layer leaked*:

| Escape cause | What it says |
|---|---|
| `missing-requirement` | Nobody wrote the requirement. The specification is the leak. |
| `wrong-requirement` | The requirement existed and said the wrong thing. |
| `correct-requirement-no-evidence` | The requirement was right and nothing verified it. |
| `implementation-bug-despite-evidence` | Requirement right, evidence real, code still wrong. |

The fourth is the one worth watching. It is the only cause that does **not** indict the
specification, and the only one a green Test Matrix would have called healthy — which makes its
share of the distribution the honest measure of how much the rest of this module is worth.

`Detected In` records the phase that **caught** the defect, not the one that introduced it; the
cause column carries that. `Traces` names the requirement or acceptance-criterion ids concerned,
or `-` where the cause is `missing-requirement` and there is nothing to point at — an absence that
is itself the finding.

### Escape cause is orthogonal to severity

`SpecReview` already carries `Severity ∈ {low, medium, high}`, and it stays. Severity classifies by
**reader action** — how urgently to look. Escape cause classifies by **origin**. A `high` severity
defect can have any of the four causes, and a `low` one can be a `missing-requirement`. Neither
replaces the other, and collapsing them would lose the only axis that answers "which layer".

### The id defect this fixes

One concept had **three** id shapes, none of which agreed:

- `defaults.id_pattern: Finding-{next:03d}` minted `Finding-001`.
- The archetype's own frontmatter schema requires `^[A-Z]{2,4}-[0-9]+$`. `Finding` is seven
  letters, so **every id the default pattern minted failed the archetype's own schema.** A Finding
  authored the standard way could not validate.
- `SpecReview`'s findings table asserts `^FND-\d+$`, a third shape.

The pattern becomes `FND-{next:03d}`, which satisfies both schemas. This is a **unification**, not
a new spelling: `FND-` was already the form SpecReview asserted and the only one the frontmatter
schema could accept.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-008-AC-1 | The `Finding` artifact type declares a `body_extraction` requiring a `Summary` section body and a `Classification` table with columns exactly `Escape Cause \| Detected In \| Traces` and at least one row. | Test (TC-060) |
| FR-008-AC-2 | `Escape Cause` is constrained to exactly the four declared values; any other value fails validation. | Test (TC-061) |
| FR-008-AC-3 | `skeletons/Finding.md` exists, and the id in its frontmatter satisfies both the archetype's frontmatter schema and the `^FND-\d+$` form `SpecReview` asserts. | Test (TC-062) |
| FR-008-AC-4 | `defaults.id_pattern` mints an id that satisfies the archetype's own frontmatter schema — the property the previous `Finding-{next:03d}` violated for every id it produced. | Test (TC-063) |
| FR-008-AC-5 | The skeleton's declared headings and its `Classification` table header match the manifest asserts exactly, in both directions (the FR-002 I1/I2 parity property). | Test (TC-064) |
| FR-008-AC-6 | Adding this contract widens nothing else: the set of artifact types carrying a `body_extraction` gains `Finding` and no other, and no frontmatter schema changes. | Test (TC-017, extended) |

## Constraints

| ID | Constraint | Verification |
|----|-----------|--------------|
| FR-008-CON-1 | Classification is a **recorded human or agent judgment**, never computed. There is no automated classifier, and a Finding whose cause was inferred rather than decided is worth nothing as evidence about which layer leaks. | Inspection |
| FR-008-CON-2 | `Escape Cause` SHALL NOT be merged into, or derived from, `SpecReview.Severity`. They classify different things — origin versus reader action — and either can take any value independently of the other. | Inspection |

## Dependencies

- **Upstream**: [FR-002](./FR-002-specreview-archetype.md) (the archetype + body-contract pattern this follows), [StR-001](../stakeholder/StR-001-module-activation.md)
- **Downstream**: the `gap-analysis` and `code-review` skills mint a Finding per confirmed defect; the cause distribution becomes an evidence-store view (agent-ix/quoin#79) once enough exist
