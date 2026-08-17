---
id: FR-007
title: "Verification-method catalog: the 29119-4 method registry as module data"
type: FR
relationships:
  - target: "ix://agent-ix/quire-rs/FR-054"
    type: "implements"
  - target: "ix://agent-ix/quire-rs/FR-053"
    type: "references"
---
# FR-007: Verification-method catalog: the 29119-4 method registry as module data

## Description

This module **SHALL** declare the `verification_catalog` block — the
machine-readable answer to *"how should this requirement be verified"* — as
module data conforming to the shape quire-rs
[FR-054](ix://agent-ix/quire-rs/FR-054) defines.

Choosing how a requirement gets verified is the core of a testing plan, and
until now that knowledge was prose in three disconnected places: the ISO 29148
`Inspection | Analysis | Demonstration | Test` set lived only inside two
`spec-artifacts-iso` lint rules; test techniques lived in
`traceability.vocabularies.test_type`; and quoin's `spec-evidence-analysis`
skill assigned a method per requirement from a **skill-local prose table that no
manifest declared and no code read**. Nothing could advise a method, and nothing
could check that a chosen one was honoured.

### The seed set is the full sweep

31 methods, covering every technique the ADR-0011 survey dispositioned as a
catalog entry — not a starter subset. A catalog that ships half the techniques
teaches the advisor that the other half do not exist, which is worse than
shipping none: an absent entry reads as "not applicable" rather than as "not
yet written".

| Class | Methods |
|---|---|
| **Test** (21) | unit, integration, e2e, property-based, metamorphic, model-based generation, combinatorial t-way, mutation, fuzzing, grammar-based fuzzing, BDD/spec-by-example, contract testing, design-by-contract, runtime monitoring, deterministic simulation, fault injection, performance benchmarking, golden/approval, negative/abuse, DAST, IAST |
| **Analysis** (7) | concolic/symbolic, SAST, SCA/SBOM, architecture conformance, static quality (5055), formal analysis (SMT), temporal model checking |
| **Inspection** (1) | inspection |
| **Demonstration** (2) | demonstration, agent-behaviour evaluation |

### Evidence kind is method-class-shaped, never per-tool

`evidence_kind` is drawn from the declared `test_type` vocabulary — the **same**
vocabulary the Test Matrix `Type` column and the suite registry's `Evidence
Kind` use. The **tool** lives in the suite registry's own `tool` column, so
semgrep, an SBOM generator and a DAST scanner need no vocabulary entries of
their own. Without that split, every adapter quoin adds
(agent-ix/quoin#91) would push a new term into a vocabulary three other things
already read.

> **Restated, not referenced — a known debt.** `evidence_kind` repeats values
> that `traceability.vocabularies.test_type` already declares, because
> `from_vocabulary` does not exist: quire-rs#133's Specify pass deferred it
> (agent-ix/quire-rs#146) since resolving a vocabulary reference has to happen
> after the cross-module merge, which is a public-API change on the validation
> path. This is the third copy of one vocabulary, and the reconciliation
> agent-ix/spec-artifacts-process#35 asked for is therefore **partial**: the
> catalog single-sources the *method* axis for consumers, via quire-rs's derived
> `verification_method` / `verification_class` lookups, but the *kind* axis is
> still three literal lists kept honest by a test.

### The obligation sources ship here too

quire-rs FR-053 derives obligations from rows a **module** declares. Without a
declaration the machinery is inert: it ships, runs, and derives nothing. Three
sources are declared — the FR and NFR acceptance-criterion targets, and the NFR
`Measurement and Evaluation` table, whose rows carry no id of their own.

> **Found end-to-end, not by inspection.** `quoin evidence record` against a
> real repository bound **nothing** and reported every trace id as unmatched,
> because no module stated an obligation for the criteria those tests were
> tagged against. The engine was correct and the ecosystem was silent.

### Applicability rules are this module's axes, not the engine's

The engine stores and surfaces `applicability` and interprets none of it
(FR-054-CON-2). This module uses `property_shapes` (the FR-052 shapes),
`characteristics` (requirement traits like `temporal`, `reliability`,
`untrusted-input`), and `object_types` (declared object types such as
`attack_surface`). An advisor matches them; nothing here does.

That is what makes the interesting recommendations possible: an `attack_surface`
object present suggests DAST, temporal phrasing suggests runtime monitoring or
model checking, a reliability NFR suggests fault injection, and a concurrency
property shape suggests deterministic simulation. None of those are reachable
from `Verification: Test` defaulted by habit.

## Inputs

- The ADR-0011 technique disposition table (agent-ix/quire-rs#81)
- The declared `traceability.vocabularies.test_type` vocabulary

## Outputs

- A merged `verification_catalog` readable through `Registry::verification_catalog()`
- The derived `verification_method` and `verification_class` vocabularies

## Behavior

- Every entry **SHALL** declare `name`, `class` and `definition`; the engine
  fails module load on an empty one.
- `class` **SHALL** be one of the ISO 29148 IADT values. The engine does not
  enforce this — it treats `class` as a free string so another module may
  classify differently — so it is this module's contract to keep, and its test's
  job to check.
- `evidence_kind` **SHALL** be a member of the declared `test_type` vocabulary.
- Every entry **SHALL** declare at least one `applicability` rule, because an
  entry no rule can ever select is a definition, not a catalog entry.
- The catalog **SHALL NOT** name a tool in `evidence_kind`, `class` or an
  applicability rule. Tools appear only in `tooling`, which is documentation.
- The catalog **SHALL NOT** carry a **cadence** as a method. *When* a check runs
  — on every push, nightly, at release — is the suite registry's schedule, and a
  `CI Gate` entry would let one axis stand in for the other.

### What a `Method` cell should say (CR-005)

quire-rs FR-054-AC-11 began reporting a declared method this catalog does not
carry, and the first sweep — quire-rs' own 20 NFR `Measurement and Evaluation`
tables, **55 rows, 17 distinct strings** — showed the corpus reaching for four
different things in one column. Fifteen of the seventeen named something the
catalog already had:

| what the cell said | what it is | write instead |
|---|---|---|
| `Proptest`, `` `cargo-mutants` ``, `Criterion Benchmark`, `Load Benchmark`, `Criterion / pytest-benchmark`, `Fuzz Run`, `loom Exhaustive Interleaving` | a **tool** | the method it implements — `property-based-testing`, `mutation-testing`, `performance-benchmarking`, `fuzzing`, `deterministic-simulation`. The tool goes in the entry's `tooling`. |
| `Unit Test`, `Integration Test`, `Snapshot Test`, `Static Analysis`, `Static Inspection` | a **class synonym** or an evidence kind | the method — `unit-testing`, `integration-testing`, `golden-approval-testing`, `static-quality`, `inspection`. |
| `CI Gate`, `Scheduled CI Gate` | a **cadence** | the method actually being run (`static-quality` for a lint script's exit status, `sca-sbom` for `cargo deny check licenses`). The schedule belongs to the suite. |

The remaining two were real: the corpus was verifying by means this catalog had
no word for, and they are added rather than forced into a near neighbour
(FR-007-AC-9).

- **`compile-time-check`** — the property is encoded so a violation does not
  build. `#![forbid(unsafe_code)]` is not `static-quality` measuring a weakness
  over source, and not `design-by-contract` checking an executable annotation
  wherever it runs; there is nothing to run.
- **`dynamic-analysis-sanitizer`** — TSAN, ASAN, Miri. Not `static-quality`
  (it executes), not `fuzzing` (it generates no input), not `fault-injection`
  (it induces nothing). The catalog had **no dynamic-analysis entry at all**,
  which is a real hole in a 29119-4-shaped registry.

### Criticality is not an acceptance-criterion fact here (CR-005)

This module declares no `criticality_column`, so every obligation the ecosystem
derives carries none. That is the arrangement quire-rs
[FR-053](ix://agent-ix/quire-rs/FR-053) already specifies — *"criticality is
genuinely optional today … declaring one is a module's choice rather than a
precondition for obligations to exist at all"* — not a gap this module left.

The ISO acceptance-criteria contract asserts exactly
`ID | Criteria | Verification` with no `optional_columns`, so the column cannot
be authored without a `spec-artifacts-iso` change; `Priority` exists only on the
Test Matrix row (`P0`..`P4`), where it rates the **test** rather than the
requirement. A consumer **SHALL NOT** assume any obligation carries a
criticality: a rule keyed on one is inert, and inert is better than silently
wrong.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-007-AC-1 | The manifest declares a `verification_catalog` whose entries cover every technique the ADR-0011 survey dispositioned as a catalog entry, across all four IADT classes. | Test (TC-048) |
| FR-007-AC-2 | Every entry declares a non-empty `name`, `class` and `definition`, and every `class` is one of `Inspection`, `Analysis`, `Demonstration`, `Test`. | Test (TC-049) |
| FR-007-AC-3 | Every `evidence_kind` is a member of the declared `test_type` vocabulary, so the catalog, the Test Matrix and the suite registry cannot disagree about what a kind means. | Test (TC-050) |
| FR-007-AC-4 | Every entry declares at least one applicability rule, and the rule names are drawn from this module's declared axes rather than being invented per entry. | Test (TC-051) |
| FR-007-AC-5 | The engine loads the manifest and exposes all entries through `Registry::verification_catalog()`, with applicability rules carried verbatim. | Test (TC-052) |
| FR-007-AC-6 | The derived `verification_class` vocabulary is exactly the four IADT values, and the derived `verification_method` vocabulary is exactly the catalog keys. | Test (TC-053) |
| FR-007-AC-7 | The methods that mint no source symbol — inspection, demonstration, agent-behaviour evaluation — carry an evidence kind in the declared `no_source_symbol` set, so a row verified that way is never reported as a status lie. | Test (TC-054) |
| FR-007-AC-8 | The traceability model declares the ecosystem's obligation sources — the two acceptance-criterion targets and the NFR measurement table — so quire-rs FR-053 derives obligations rather than shipping inert. | Test (TC-055) |
| FR-007-AC-9 | The catalog carries a method for verifying a property at **compile time** (a violation does not build) and one for **dynamic analysis under an instrumented runtime** (sanitizers). Neither is expressible as static analysis, executable contracts or fuzzing, and the first corpus sweep found both in use with no catalog word for them. | Test (TC-056) |
| FR-007-AC-10 | No catalog entry names a **tool**, a **class synonym** or a **cadence** as a method: a tool belongs in the entry's `tooling`, a class is already the `class` axis, and when a check runs belongs to the suite registry's schedule. | Test (TC-057) |

## Dependencies

- **Upstream**: quire-rs [FR-054](ix://agent-ix/quire-rs/FR-054) (the block shape and the merge, released in v0.29.0), FR-006 (the suite registry sharing the evidence-kind vocabulary)
- **Downstream**: agent-ix/quoin#89 (the test-plan advisor reads the merged catalog and matches its applicability rules), agent-ix/quoin#80 (method conformance is checked against it), agent-ix/quoin#91 (evidence adapters map tool output onto these kinds)
