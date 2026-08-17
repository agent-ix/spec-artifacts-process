---
id: FR-006
title: "Evidence-layer archetypes: the authored half of the evidence store"
type: FR
relationships:
  - target: "ix://agent-ix/quire-rs/FR-053"
    type: "references"
  - target: "ix://agent-ix/quoin/79"
    type: "references"
---
# FR-006: Evidence-layer archetypes: the authored half of the evidence store

## Description

This module **SHALL** declare two archetypes — **`SuiteRegistry`** and
**`Inspections`** — so the authored half of the ADR-0011 evidence store is a
validated corpus document rather than a convention.

The evidence store splits by who writes it: **authored → markdown, validated as
a document; machine-transcribed → JSON, typeless and corpus-invisible**
(agent-ix/quoin#79). The JSON half needs no archetype and gets none — its
schemas are quoin's. The markdown half needs both, because a suite registry that
nothing validates is a list of commands nobody checks, and an inspection record
that nothing validates is a claim about work nobody can trace.

### Suite ids are structured, not slugs

`SUITE-N` is a doc-scoped, pattern-validated, **never-renumbered** id, not a
kebab slug. Everything joins on it — run directories, bindings, freshness — and
a policy-immutable semantic string is exactly what produced the 1,014 dead trace
tags this program exists to close (agent-ix/quire-rs#72). The suite's *name* and
*command* live in their own columns, where they can change without breaking a
join.

### One vocabulary, three uses

`Evidence Kind` draws from the **same** declared `test_type` vocabulary as the
Test Matrix `Type` column and the obligation record's verification method
(CR-015 discipline). The tool goes in its own column, so a tool-specific report
— semgrep, SARIF, an SBOM — needs no vocabulary entry of its own and
`Evidence Kind` stays method-class-shaped.

> **The vocabulary is restated, not referenced, and that is a known debt.**
> `column_choices` takes a literal list; there is no `from_vocabulary` to
> dereference `traceability.vocabularies.test_type` with. That mechanism was
> specified and deliberately deferred (agent-ix/quire-rs#146) because resolving
> a vocabulary reference inside an assert has to happen after the cross-module
> merge, which is a public-API change on the validation path. Until it lands,
> the FR-003 manifest test is what keeps the copies honest — which is a real
> gate, not a hope, but it is a gate rather than an impossibility.

### Both documents live under `spec/`

`spec/evidence/suites.md` and `spec/evidence/inspections.md`.

> **This corrects a premise in agent-ix/quoin#79**, which places `evidence/` at
> the repository root on the grounds that *"corpus membership is type-driven
> post-quire-rs#73, so quire validates them wherever they live"*. **[RAN]** that
> claim and it does not hold: quire-rs **CR-045** bounds the document walk to
> `<scope>/spec`, and #73 made membership type-driven *within the walked root*,
> not everywhere on disk. A typed, well-formed `evidence/suites.md` at the
> repository root minted **nothing** and was reported nowhere; the identical
> file at `spec/evidence/suites.md` was walked, validated, and minted its ids,
> with its references reconciled.
>
> A registry that looks authoritative while being checked by nothing is the
> "green matrix over dead links" failure reproduced inside the store meant to
> prevent it. The authored half therefore lives under `spec/`. The
> machine-written half is unaffected: quoin#79 already calls it typeless and
> corpus-invisible, so nothing about it needs the walk.

### Inspections carry the methods that mint no symbol

Inspection, analysis and demonstration produce **no source symbol**, so they can
never be discharged by a tagged test — the CR-041 `no_source_symbol` class. The
record of *who* performed the act, *when*, and against *which commit* is the
evidence. `Obligation` is a declared reference, so a typo in it dangles like any
other broken trace reference instead of recording an act against nothing.

## Inputs

- `spec/evidence/suites.md` — the authored suite registry
- `spec/evidence/inspections.md` — the authored inspection/analysis acts

## Outputs

- Minted `SUITE-N` and `INSP-N` trace ids, referenceable by any declaration
- Validation failures on a malformed registry, at authoring time

## Behavior

- The module **SHALL** declare a `SuiteRegistry` artifact type whose
  `## Suites` section carries a table with headers exactly
  `ID | Name | Command | Tool | Evidence Kind`, at least one row, `ID` matching
  `^SUITE-\d+$`, and `Evidence Kind` drawn from the declared test-type
  vocabulary.
- The module **SHALL** declare an `Inspections` artifact type whose
  `## Inspections` section carries a table with headers exactly
  `ID | Obligation | Who | Commit | Verdict | Note`, at least one row, `ID`
  matching `^INSP-\d+$`, and `Verdict` one of `Pass | Fail | Waived`. That
  archetype **SHALL** mark `Note` optional, because a passing inspection often
  has nothing to add.
- The traceability model **SHALL** declare both as trace targets, which is what
  makes `SUITE-N` and `INSP-N` referenceable id classes and gives FR-049's
  `dangling-trace-reference` coverage of them for free.
- The `Obligation` column **SHALL** be a declared document reference resolving
  against the existing acceptance-criterion targets.
- Both **SHALL** ship an authoring skeleton, so creation goes through the
  standard authoring path rather than a hand-rolled fixture.
- Neither **SHALL** be `required` of any repository. A repo that has not adopted
  the evidence layer declares neither document and is unaffected.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-006-AC-1 | The manifest declares `SuiteRegistry` with a frontmatter schema and a `body_extraction` asserting the five required columns, `min_rows: 1`, and the `^SUITE-\d+$` id pattern. | Test (TC-040) |
| FR-006-AC-2 | The manifest declares `Inspections` with the six columns, `Note` optional, the `^INSP-\d+$` id pattern, and the closed `Pass\|Fail\|Waived` verdict vocabulary. | Test (TC-041) |
| FR-006-AC-3 | The `Evidence Kind` choices are exactly the declared `traceability.vocabularies.test_type` values, so the registry and the coverage rollup cannot disagree about what a kind means. | Test (TC-042) |
| FR-006-AC-4 | The traceability model declares `suite` and `inspection` trace targets bound by archetype, so both id classes mint and are referenceable. | Test (TC-043) |
| FR-006-AC-5 | A conformant suite registry validates, and copies mutating the id pattern, dropping a required column, or using an undeclared evidence kind each fail with a line-numbered diagnostic. | Test (TC-044) |
| FR-006-AC-6 | A conformant inspection record validates, a copy with an undeclared verdict fails, and a copy omitting the optional `Note` column still passes. | Test (TC-045) |
| FR-006-AC-7 | Both skeletons validate against their own archetypes as authored, so the shipped authoring path produces a conformant document. | Test (TC-046) |
| FR-006-AC-8 | A repository declaring neither document loads and validates exactly as it did before these archetypes existed. | Test (TC-047) |

## Dependencies

- **Upstream**: quire-rs [FR-053](ix://agent-ix/quire-rs/FR-053) (the obligation record these acts discharge, released in v0.29.0), FR-050 (the traceability model), FR-033 (the `assert` facet and its `optional_columns` / `column_choices` keys)
- **Downstream**: agent-ix/quoin#79 (the evidence store consumes both as a typed registry), agent-ix/quoin#80 (suite-based freshness and vacuity checks)
