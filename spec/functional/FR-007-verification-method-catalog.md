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

### The one source whose arity is not one-per-row

Every other obligation source mints one obligation per row: an acceptance
criterion states one obligation, an NFR metric row states one. A
**configuration-dimensions** table does not. It states a *space* —
`features(default|python|wasm)` crossed with `target(linux|wasm32)`, minus
whatever cannot co-exist — and the obligation is about the **interaction** of
its rows. No single row can carry that, so the table mints exactly one
(quire-rs FR-061).

`strength: 2` is pairwise. Published evidence puts most configuration-space
defects in pairs, and 3-way multiplies the target for a return nobody in this
ecosystem has measured. The engine knows no default; a module wanting more says
so.

**This declaration is why quire-rs FR-061 and quoin FR-035 can fire at all.**
Both shipped in ADR-0011 Phase 2 wave D against a `module-manifest.schema.json`
that rejected the key, so zero combinatorial obligations existed anywhere —
the third instance of the engine-before-module ordering gap in that program.

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
| FR-007-AC-8 | The traceability model declares the ecosystem's obligation sources — the two acceptance-criterion targets, the NFR measurement table, and the configuration-dimensions table — so quire-rs FR-053 derives obligations rather than shipping inert. | Test (TC-055) |
| FR-007-AC-12 | The configuration-matrix source declares `combinatorial`, so a `## Configuration Dimensions` table mints ONE obligation for the whole table rather than one per row (quire-rs FR-061). It declares an exclusions column, because a space with forbidden combinations and no way to state them demands coverage of combinations that cannot exist. | Test (TC-055) |
| FR-007-AC-13 | No method declares `path-sensitive` or `hard-to-reach-branch`. Both name the implementation's control flow, which no specification states and no fact source can read, and a method keyed only on them can never be recommended. | Test (TC-067) |
| FR-007-AC-14 | No method declares `surviving-mutants` or `suite-quality-unknown`. Both were considered and rejected — the first names one tool's artifact, the second over-claims and names the wrong subject — and the axis is method-class-shaped, as `evidence_kind` is (CR-015). | Test (TC-068) |

> **CR-029 note (concolic execution becomes reachable — 2026-08-19):**
> `concolic-execution` was keyed on `path-sensitive` and `hard-to-reach-branch`,
> and **nothing could produce either**. Both describe the *implementation's*
> control flow; a specification states what the system must do, never that a
> branch behind it is hard to reach. Measured across this catalog, it was the
> last of 33 methods no requirement could elicit (agent-ix/quoin#128).
>
> **The re-key follows how the technique is actually reached.** Nobody starts
> there — it path-explodes and it is slow. The industrial pattern is *hybrid
> fuzzing*: fuzz until the coverage curve flattens, hand the stuck branches to a
> solver, feed the solved inputs back as seeds (Driller 2016, then QSYM, SymCC,
> Fuzzolic). Four documented reasons people reach for it, and each is observable:
>
> | Reason | How it is observed |
> |---|---|
> | the fuzzer stopped finding branches | `fault-detection-unmeasured` / `fault-detection-failed`, from the evidence store |
> | a safety standard mandates path coverage — DO-178C Level A MC/DC, ISO 26262 ASIL D, IEC 62304 Class C | `high-criticality`, from the obligation's own value |
> | constant-time code, no secret-dependent branch | `secret-dependent-branch`, stated in the requirement |
> | equivalence with a reference implementation over all inputs | `reference-equivalence`, stated in the requirement |
>
> plus `magic-value-comparison` — a checksum, CRC, HMAC or magic number, the
> classic wall a fuzzer cannot climb — and `structured-input`.
>
> **The evidence pair is not called `surviving-mutants`.** That would name
> mutation testing's artifact, and this method reads the same signal while
> producing no mutants — the reasoning that made `evidence_kind`
> method-class-shaped rather than per-tool (CR-015). `suite-quality-unknown` is
> renamed to `fault-detection-unmeasured` for the same discipline: "quality"
> over-claimed and "suite" named the wrong subject. It was declared once and
> produced by nothing, so the rename was free; it will not be once it fires.
>
> **Deliberately absent: a `fuzz-plateau` value**, which is the literal Driller
> trigger. Nothing records coverage over time, and inventing a proxy is the
> CR-014 failure — an open set whose membership had to be judged rather than
> read.
>
> **What the entry still cannot say** is that it is an escalation of last
> resort. `advise` ranks by how many rules matched, so this now outranks
> `unit-testing` on a statement matching two of the above with nothing marking
> the difference. Filed as agent-ix/quire-rs#190; until it lands, the guidance
> lives in quoin's `spec-evidence-analysis` and `spec-fuzz` skills — which is
> the skill-local-prose arrangement ADR-0011 moved away from, recorded as a debt
> rather than left to be rediscovered.
>
> **AC-13 and AC-14 are denylists, and that is a deliberate limit.** Two general
> forms of AC-14 were written and both were worse than nothing. "Does a declared
> tool name appear inside the value" passes `surviving-mutants` cleanly, because
> no tool is called *mutants*. Reversed — "does a stem of the value appear inside
> a tool name" — it fires on `cross` in `crosshair` and `fault` in
> `fs-fault-injection`. Deciding whether a name is per-tool is a judgement, and a
> check that needs judgement is the CR-014 failure this catalogue keeps citing.
> So the principle is stated here and enforced in review; the tests guard the
> specific mistakes rather than pretending to guard the class.
| FR-007-AC-9 | The catalog carries a method for verifying a property at **compile time** (a violation does not build) and one for **dynamic analysis under an instrumented runtime** (sanitizers). Neither is expressible as static analysis, executable contracts or fuzzing, and the first corpus sweep found both in use with no catalog word for them. | Test (TC-056) |
| FR-007-AC-10 | No catalog entry names a **tool**, a **class synonym** or a **cadence** as a method: a tool belongs in the entry's `tooling`, a class is already the `class` axis, and when a check runs belongs to the suite registry's schedule. | Test (TC-057) |
| FR-007-AC-11 | The presence of a declared object type is an applicability signal: `attack_surface`/`threat` advise the security methods and `hazard`/`failure_mode` advise `fault-injection`. Every object type any entry advises on is one a `spec-objects-*` module actually declares — a typo is a rule that silently never fires. | Test (TC-065) |

## Dependencies

- **Upstream**: quire-rs [FR-054](ix://agent-ix/quire-rs/FR-054) (the block shape and the merge, released in v0.29.0), FR-006 (the suite registry sharing the evidence-kind vocabulary)
- **Downstream**: agent-ix/quoin#89 (the test-plan advisor reads the merged catalog and matches its applicability rules), agent-ix/quoin#80 (method conformance is checked against it), agent-ix/quoin#91 (evidence adapters map tool output onto these kinds)
