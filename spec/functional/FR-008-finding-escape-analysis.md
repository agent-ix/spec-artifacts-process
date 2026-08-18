---
id: FR-008
title: "A finding records which layer a defect escaped through"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-artifacts-process/FR-002"
    type: "extends"
---
# FR-008: A finding records which layer a defect escaped through

## Description

A defect that is found got past everything meant to catch it. **Escape cause records which layer
let it through**, and it is the only axis in this module that does. Severity says how urgently to
look; a count of defects says how many there were; neither says whether the specification, the
evidence, or the implementation is leaking.

`SpecReview` **SHALL** accept an optional fifth findings column, `Escape Cause`, constrained to
four values:

| Value | What happened |
|---|---|
| `missing-requirement` | Nobody wrote the requirement. There was nothing to test against. |
| `wrong-requirement` | A requirement was written and said the wrong thing. |
| `correct-requirement-no-evidence` | The requirement was right and nothing verified it. |
| `implementation-bug-despite-evidence` | Requirement right, evidence real, code still wrong. |

The fourth is the one worth watching. It is the only cause that does **not** indict the
specification, and the only one a fully green Test Matrix would have called healthy — which makes
its share of the distribution the honest measure of what the rest of this module is buying.

### Why the column and not the `Finding` archetype

The obvious home is the `Finding` artifact type, and it is the wrong one.

`SpecReview` was created on 2026-06-20 **deliberately beside** the freeform `Review` archetype —
"NOT overloading freeform `Review`, which is used ecosystem-wide with heterogeneous bodies —
would break" — precisely so the analysis skills would not have to touch the `Review`/`Finding`
container-and-child path. Findings-as-inline-rows was the decision, not an accident.

**[RAN]** over the `~/dev` corpus: **169 `SpecReview` documents**, **90 `Review` documents**, and
**2 documents typed `Finding`** — both of which are mistyped analyses (`AN-002 "Spec Integrity
Analysis"`) rather than findings. Nothing has ever authored a real `Finding`.

So an escape-cause contract on `Finding` would attach the axis to a form nobody produces, and
wiring the skills to emit one would reverse a shipped decision. The axis goes where the findings
actually are.

### Optional, because 169 documents already exist

`Escape Cause` is declared in `optional_columns` (CR-023). Headers must be an ordered subsequence
of the declared list containing every non-optional column, so a four-column table
`ID | Severity | Summary | Refs` stays valid and a table that records the cause appends it last.
Making it required would invalidate every SpecReview in the corpus on the day it shipped.

It is optional in a second sense that matters: **not every finding is an escaped defect.** A
completeness observation or a style note has no layer that leaked, and forcing a value would
manufacture data. The column is recorded where the finding is a real escape and omitted where it
is not.

### The `Finding` id defect, fixed separately

`Finding`'s `defaults.id_pattern` was `Finding-{next:03d}`, minting `Finding-001` — which fails
the archetype's own frontmatter schema, `^[A-Z]{2,4}-[0-9]+$`, because seven letters is not
two-to-four. **Every id the default pattern produced was invalid**, so a Finding authored the
standard way could not validate. That is fixed here to `FIND-{next:03d}`.

Deliberately **not** `FND-`: that is the id namespace of the findings *rows* inside a SpecReview.
A `Finding` is a document and a child of `Review`; giving the two the same prefix would read as
unification and be a conflation. `Finding` gains no body contract — nothing authors one, and a
contract for a form nobody produces is the mistake this FR exists to avoid repeating.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-008-AC-1 | The `SpecReview` findings assert declares `Escape Cause` as the fifth column and lists it in `optional_columns`, so a four-column findings table remains valid. | Test (TC-060) |
| FR-008-AC-2 | `Escape Cause` is constrained to exactly the four declared values. | Test (TC-061) |
| FR-008-AC-3 | `Severity` keeps its own vocabulary unchanged and independent — the two columns classify different things and neither derives from the other. | Test (TC-061) |
| FR-008-AC-4 | `Finding.defaults.id_pattern` mints an id satisfying the archetype's own frontmatter schema — the property `Finding-{next:03d}` violated for every id it produced — and does **not** collide with the `^FND-\d+$` namespace SpecReview's findings rows use. | Test (TC-063) |
| FR-008-AC-5 | `Finding` declares no `body_extraction`: nothing authors one, and the two corpus documents typed `Finding` are mistyped analyses. | Test (TC-064) |
| FR-008-AC-6 | The `SpecReview` skeleton documents the column and all four values, so an author never opens the manifest to find the options. | Test (TC-062) |

## Constraints

| ID | Constraint | Verification |
|----|-----------|--------------|
| FR-008-CON-1 | Escape cause is a **recorded human or agent judgment**, never computed. A cause that was inferred rather than decided is worth nothing as evidence about which layer leaks. | Inspection |
| FR-008-CON-2 | `Escape Cause` SHALL NOT be merged into, or derived from, `Severity`. They classify different things — which layer leaked versus how urgently to look — and either can take any value independently of the other. | Inspection |
| FR-008-CON-3 | The analysis skills SHALL keep emitting `SpecReview` documents. This FR adds a column; it does not move findings onto the `Review`/`Finding` path, which the 2026-06-20 decision deliberately left alone. | Inspection |

## Dependencies

- **Upstream**: [FR-002](./FR-002-specreview-archetype.md) (the SpecReview archetype and its findings contract), [StR-001](../stakeholder/StR-001-module-activation.md)
- **Downstream**: the `code-review` and `gap-analysis` skills record a cause per escaped defect; the distribution becomes an evidence-store view (agent-ix/quoin#79) once enough exist
