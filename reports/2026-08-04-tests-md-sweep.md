# FR-003-CON-1 sweep — ecosystem `spec/tests.md` vs the candidate TestMatrix contract

**Date:** 2026-08-04 · **Mode:** read-only (no repository was modified) · **Contract:** the unpublished `TestMatrix` `body_extraction` on branch `task/testmatrix-body-extraction`

This is the evidence the FR-003-CON-1 gate (Task-005) needs. It answers one question: *what would happen to the ecosystem if the enforcing module version were published today?*

## Headline

- **189** `spec/tests.md` files under `~/dev`.
- **12** are not `type: TestMatrix` and are unaffected by the contract.
- Of the **177** TestMatrix documents: **6 pass**, **171 fail**.

Publishing today would break validation in **96%** of the ecosystem's matrices. That is the outcome FR-003-CON-1 exists to prevent, and the shape of the failures says the remedy is not purely a corpus sweep — see *Contract decisions* below.

## Failure causes

| Cause | Repos affected | Total diagnostics | Remedy class |
|---|---|---|---|
| `missing-test-case-summary` | 116 | 116 | authoring (per repo) |
| `missing-fr-coverage` | 112 | 112 | authoring (per repo) |
| `columns` | 48 | 103 | authoring (per repo) |
| `type-vocabulary` | 29 | 558 | **contract decision** |
| `traces-to-pattern` | 25 | 177 | mixed: authoring + **contract decision** |
| `test-id-pattern` | 23 | 349 | mixed: mechanical + authoring |
| `status-vocabulary` | 19 | 564 | mixed: mechanical + **contract decision** |
| `other` | 12 | 17 | review individually |

## Contract decisions this sweep surfaces (for the Task-005 gate)

The vocabulary failures are **not** all corpus drift. Real matrices in the ecosystem use categories the contract does not admit:

- **`Type`** — the corpus uses `Static` (59), `Benchmark`/`Bench` (47), `pg_test` (72), `Storybook`, `Fixture`, `Compile`, and compound forms like `Unit / pg_test`. quire-rs's own matrix — the reference corpus — uses `Static` and `Property`. Either the contract widens its `Type` vocabulary, or ~29 repos rewrite categories that carry real meaning today.
- **`Status`** — beyond the decorated forms (`✅ Complete`, `🚧 Planned`, `✅ Implemented`) that normalize mechanically, the corpus uses word statuses (`Implemented`, `Planned: implementation in progress`, `Gap: deferred`) and markers outside the set (`⬜`, `🔴`, `⛔`). Word statuses carry information the four markers cannot.
- **`Traces To`** — ranges (`FR-001..FR-006`), em-dash placeholders (`—`), and prose (`Future Task 13`) are common. Ranges in particular are an authoring convenience the contract currently forbids; admitting them is a contract change, expanding them is a per-repo edit.

**Recommendation:** treat the vocabulary questions as FR-003 spec amendments *before* normalizing 171 repos to a contract that may still move. Sequencing it the other way rewrites the corpus twice.

## Mechanically normalizable today

These transformations are deterministic and safe to script once signed off:

- decorated status → bare marker: `✅ Complete` → `✅`, `✅ Implemented` → `✅`, `🚧 Planned` → `🚧` (81 cells).
- id cells carrying trailing prose (`TC-020 SPIRE`, `TC-020 benchmark suites`) → the bare id, with the prose moved into `Title` (16 cells).

Everything else needs either a contract decision or per-repo authoring.

## Status

**No repository was modified and nothing was published.** The next step is the Task-005 gate: the user decides (a) whether the `Type`/`Status`/`Traces To` vocabularies change, and (b) whether the normalization sweep proceeds. Until that sign-off is recorded, the enforcing module version stays unreleased (FR-003-CON-1).

---

# Addendum (2026-08-05): simulating the amended vocabularies, and what the
# "missing table" population really is

## Simulated pass rate

Running the four amended vocabularies (Type core set + module extensions;
Status marker + optional note; Traces To with ranges, parentheticals and
declaration-derived kinds; the widened Test ID shape) against all 177 matrices:

**6/177 passing today → 18/177 (10.2%) with the amendment.**

Remaining failure causes: missing Test Case Summary 116, missing Functional
Requirement Coverage 111, Type 27, Traces To 15, Status 14, Test ID 13,
column set 11.

The vocabulary work is worth doing — it stops the contract rejecting categories
the corpus legitimately uses, and it fixes 12 repos outright — but it is **not**
what stands between the ecosystem and a green sweep.

## The "missing Test Case Summary" population, examined

Of the 116 matrices with no `## Test Case Summary`:

- **70** have no id-column table anywhere. They are coverage narratives —
  `Coverage Summary` (19), `Overview` (14), `Traceability` (11),
  `Status` (10). No contract change reaches these; they need authoring.
- **44** do have an id-column table under another heading, but inspecting the
  column sets shows these are mostly **different artifacts**, not renamed
  summaries:

| Heading | Repos | Columns | What it is |
|---|---|---|---|
| `Edge Cases` (+ variants) | 9 | `ID \| Description \| Related Req \| Test Case \| Risk if Untested` | risk register (already non-required scaffolding) |
| `3. Constraint / Invariant → TC` | 5 | `ID \| TC \| Status` | constraint→test coverage map |
| `Test Cases` | 4 | `TC ID \| Requirements Mapped \| Description \| Type \| Priority \| Status` | **a real test-case summary, renamed** |
| per-FR sections, `State Transition Tests`, … | ~6 | bespoke | ad-hoc breakdowns |

**So the honest split is ~150 repos needing authoring and ~4 needing a rename**,
not "116 authoring / 44 renaming". Accepting alternative headings would recover
those 4 — and only if a second *column* vocabulary were accepted too, since they
renamed `Test ID`→`TC ID`, `Title`→`Description`, `Traces To`→`Requirements
Mapped`. That is a worse trade than asking four repos to rename a heading and
three columns, and it would re-introduce the engine-facing alias lists that
quire-rs CR-013/CR-014 removed.

**Decision (2026-08-05, with the user): normalize.** One required heading, one
column set; the four renamed matrices are normalized during the sweep.

---

# Re-sweep after the CR-016 amendment (2026-08-05)

Same read-only method, against the amended contract:

**6/177 → 13/177 passing.** (The C0 simulation projected 18; it was looser than
the patterns finally shipped, since space-before-comma and trailing commas in
`Traces To` were tightened back to failing after the simulation ran. The
difference is 5 repos whose only remaining failure is that formatting.)

Remaining causes are the structural ones the addendum already identified:
missing Test Case Summary (114), missing Functional Requirement Coverage (109),
then Status (180 cells), Type (164 cells).

The Status and Type counts are cell-level, and both are now *failures of the
corpus rather than of the contract*: the marker vocabulary admits a trailing
note, so what remains are word statuses (`Implemented`, `Planned: …`) and
markers outside the set (`⬜`, `🔴`); the Type vocabulary admits ten core values
plus module extensions, so what remains are harness names (`pg_test`) and
compound cells (`Unit / pg_test`) that normalization moves to `Title` or splits
into rows.

**The gate position is unchanged: nothing published, no repo edited.** The
amendment removes the contract's own errors; the remaining 164 need the
normalization work that Task-005 exists to authorize.
