# FR-003 sign-off gate: classifying the 171 failures

**Date:** 2026-08-06
**Answers:** agent-ix/spec-artifacts-process#12
**Umbrella:** agent-ix/quire-rs#17
**Harness:** `scripts/testmatrix_sweep.py` — committed, unlike the original run's
**Method:** real `quire.validate_document` against this repo's `manifest.yaml`, so
the result is exactly what `quire validate` says rather than a reimplementation

> **Nothing published, no repo edited.** This report does work items 1 and 2 and
> proposes 3. FR-003-CON-1 gates the rest.

## First: the headline number was inflated

The original sweep reported **171 of 177**. Re-running it surfaced a counting
defect: `ecaz` carries **20 worktree checkouts** under `.worktrees/` and
`.claude/worktrees/`, each a byte-copy of its `spec/tests.md`. Every one of that
repo's diagnostics was therefore counted 20 times, which made a single repo's
authoring style look like a corpus-wide trend — 945 `Status` cell failures
collapse to **111** once deduplicated.

Deduplicated (worktree checkouts and `<repo>-task<N>` clones excluded):

| | |
|---|---|
| `spec/tests.md` typed `TestMatrix` | **169** |
| passing | **13 (7.7%)** |
| failing | **156 (92.3%)** |

The pass rate is essentially as reported. The *composition* of the failures is
not.

## Work item 1 — the three classes

| Class | Docs | Share | What it actually is |
|---|---|---|---|
| **missing-table** | **70** | 41.4% | No `## Test Case Summary`, and no id-column table anywhere. The repo has never authored a matrix. |
| **renamable** | **44** | 26.0% | No `## Test Case Summary`, but an id-column table exists under some other heading. |
| **malformed** | **42** | 24.9% | The sections exist and the contract rejects their content. |

**This is the finding that matters.** Only **42 repos have a matrix that could
be normalized**. The other 114 do not have one to fix — 92% failing reads as "the
contract is too strict", but two thirds of it is "the artifact was never
written".

The earlier addendum already checked the `renamable` class and found only ~4 are
genuinely a renamed summary; the rest carry a *different artifact* under an
id-column heading (an edge-case risk register, a constraint→TC map). So they
belong with `missing-table`: **~110 repos need authoring, ~4 need a rename, 42
need normalization.**

## Work item 2 — is the contract too narrow?

The issue asks for the proportion between "undeclared but legitimate" and
"genuinely non-conformant", determined from evidence rather than picked. Taking
each rejecting column in turn.

### `Type` — 158 cells, 63 distinct, 21 repos. **No amendment. Corpus.**

CR-016 already widened this once. What remains does not contain a missing
category; it contains four other things:

| Kind | Examples | Remedy |
|---|---|---|
| abbreviation of a declared value | `Bench` (19), `Perf` (8) | → `Benchmark` |
| annotation that belongs in `Title` | `Unit (git)` (11), `Integration (browser)` (3), ``Benchmark (`ecaz bench suite`)`` (2), `Unit / pg_test` (2) | move the parenthetical |
| a **harness**, not a test type | `pg_test` (8), `Storybook` (13), `Fixture` (13), `axe-core` (3) | → the type describing how it runs |
| a **verification method** in the wrong column | `Inspection` (2), `Review` (3), `Inspect` (1) | that vocabulary belongs to an AC `Verification` cell |

The residual arguable-category cells — `Security` (4), `Parity` (5), `Service`
(5), `Build` (4), `Chaos`, `Smoke`, `Concurrency`, `Fault` — are ~25 cells, and
each is better expressed by *how the test runs*. A security test is `Unit`,
`Integration` or `E2E`; `Security` describes intent, and intent belongs in
`Title`. quoin#49 documents exactly this for the authoring side.

Widening `Type` again would be fitting the check to non-conforming data.

### `Status` — 111 cells, 7 repos. **No amendment. Corpus.**

The pattern already admits a marker plus a trailing note, so a conformant author
writes `✅ Implemented`. What remains is markers outside the set — `⬜` (34),
`🔴` (10), `⊘` (4) — and bare word statuses (`Implemented`, `Complete`,
`Planned: …`). Seven repos. Mechanically normalizable.

### `Traces To` — 70 cells, 8 repos. **One amendment proposed.**

This is the one place the contract is genuinely too narrow. Two authoring forms
are legitimate, unambiguous and widely used, and the pattern rejects both:

```
FR-001-AC-2, -AC-3, -AC-4            continuation shorthand — the parent id is elided
FR-016-AC-1/2/3/6/7/8                slash enumeration of sub-ids
```

Together ~25 cells across ~6 repos. Both mean exactly what the expanded list
means, and expanding them by hand makes matrices longer and no clearer.

The remaining `Traces To` failures are **not** a contract problem: `—` (10) and
empty (6) are test cases that trace to nothing, which is precisely what a
traceability matrix exists to prevent. Those should keep failing.

**Proposed CR-017** (this repo's next CR number) on FR-003: extend the
`Traces To` pattern to admit `-<KIND>-<n>` continuation terms and `<n>/<n>`
sub-id enumeration. Nothing else.

### Column headers — 87 mismatches, 40 repos. **No amendment. Corpus.**

Only **4 documents fail on headers alone**, and only 5 mismatches are a
one-word near-synonym (`Status` vs `Coverage Status`). The rest are genuinely
different tables — `["US", "AC", "TC", "Type", "Priority"]`,
`["StR", "Trace", "Validation", "Status"]` — mostly in the *optional* coverage
sections. Admitting them would make the contract mean nothing.

### Proportion, answered

| Reading | Share of the failure mass |
|---|---|
| contract too narrow | **~25 cells, ~6 repos** — one `Traces To` amendment |
| corpus non-conformant | 42 repos of malformed matrices |
| **artifact never authored** | **~110 repos** |

Reading 2 dominates among repos that *have* a matrix, and the third class —
which the issue rightly asked to separate — is the largest of all.

## Work item 3 — what should actually happen

The gate has been framed as "publishing would turn a validation pass into a
failure for effectively every repo simultaneously". That framing deserves one
correction: **module adoption is per-repo**. A repo installs this module
explicitly (`quoin plugin install package:@agent-ix/spec-artifacts-process`, or
`--module` against a pinned path) and picks up a new contract when it updates.
Publishing does not reach into 156 repos; it changes what a repo gets *when it
next updates*.

That is not a licence to publish carelessly, and one thing must be checked
first: whether `quoin module ensure-defaults` resolves to latest, which would
turn adoption into a broadcast. **That check is a prerequisite to publishing and
has not been done here.**

Recommended sequence:

1. **Amend `Traces To`** (CR-017 above). It is the only place the contract is
   wrong, and it is cheap.
2. **Normalize the 42 malformed matrices**, per-repo with reviewed diffs. This
   is the sweep Task-005 exists to authorize, and it is a 42-repo job rather
   than a 171-repo one.
3. **Treat the ~110 unauthored matrices as a backlog, not a blocker.** They are
   not a contract problem and will not be fixed by any amendment. A repo with no
   Test Case Summary has no traceability today either — the contract is
   reporting a real gap, which is the point of building it.
4. **Verify `ensure-defaults` version-resolution behaviour**, then publish.

Publishing behind step 2 rather than step 3 is the substantive proposal here: it
unblocks the module for every repo that has done the work, instead of holding it
until the slowest repo in the ecosystem authors a matrix it has never had.

## Reproducing

```bash
python3 scripts/testmatrix_sweep.py --root ~/dev --out /tmp/tm.json
python3 scripts/testmatrix_sweep.py --root ~/dev --show-values Type
```

The harness is read-only and never edits a document.
