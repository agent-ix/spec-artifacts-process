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

## Dependencies

- **Upstream**: quire-rs [FR-054](ix://agent-ix/quire-rs/FR-054) (the block shape and the merge, released in v0.29.0), FR-006 (the suite registry sharing the evidence-kind vocabulary)
- **Downstream**: agent-ix/quoin#89 (the test-plan advisor reads the merged catalog and matches its applicability rules), agent-ix/quoin#80 (method conformance is checked against it), agent-ix/quoin#91 (evidence adapters map tool output onto these kinds)
