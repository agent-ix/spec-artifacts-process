---
id: SR-006
title: "Retroactive code review — ⚠️ retirement and source_exclude declaration (PRs #54, #55)"
type: SpecReview
analysis: code-review
scope: "spec_artifacts_process/manifest.yaml, tests/test_manifest.py, tests/test_testmatrix_body_extraction.py, spec/functional/FR-003-testmatrix-body-extraction.md, spec/functional/FR-004-traceability-declaration.md, spec/tests.md"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-artifacts-process/spec/functional/FR-003", type: references }
  - { target: "ix://agent-ix/spec-artifacts-process/spec/functional/FR-004", type: references }
  - { target: "ix://agent-ix/spec-artifacts-process/spec/tests", type: references }
---

# SR-006: Retroactive code review — ⚠️ retirement and source_exclude declaration (PRs #54, #55)

## Summary

Retroactive review of the two PRs of the trace-status-integrity batch that landed
in this repository, both merged 2026-08-21 with zero reviews: #54 (`75c5d0b`,
retire the `⚠️` status marker, FR-003 CR-031) and #55 (`f4e5f83` = tag
**v0.23.0**, declare `traceability.source_exclude`, FR-004 CR-032). Reviewed as
merged, against main; the suite at HEAD runs 81 passed / 1 xfailed. #54 is a
model change — red-test-first, with a bidirectional drift guard. #55 declares a
safety-critical key with zero targeted tests, mints a matrix row no test backs,
and was tagged ahead of the engine release that tolerates it. Remediation is
ticketed (#56 here, spec-artifacts-iso#29); this document records the findings
and the glob-safety evidence so the verdict does not have to be re-derived.

## Verdict

**CONDITIONAL** — no finding requires touching the merged code beyond what #56
already tracks; one high (release ordering), two medium, and the #55 gaps are
ticketed. #54 is APPROVED retroactively without qualification.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | #54 is a good change and the record should say so: the drift guard was made bidirectional AND run red against the pre-change manifest first | tests/test_manifest.py:285 |
| FND-002 | medium | #55 declared the three `source_exclude` globs with ZERO targeted tests; the "`tests/**` MUST NEVER appear here" invariant is prose-only in all three places it exists | spec_artifacts_process/manifest.yaml:509, #56 |
| FND-003 | medium | #55 minted matrix row TC-070 as `✅ Complete` with no test binding it — no test in tests/ mentions TC-070 or `source_exclude` — an unbacked ✅ of exactly the class #54 exists to expose | spec/tests.md:85 |
| FND-004 | high | Release-ordering violation, live at review time: v0.23.0 is tagged at #55's merge commit declaring `source_exclude`, while the first `deny_unknown_fields`-tolerant engine release (quire-cli v0.28.0) was never published — npm tops at 0.27.0 | pyproject.toml, agent-ix/quire-cli |
| FND-005 | low | Latent glob footgun, recorded not fired: globset compiles with `literal_separator=false`, so a future `*/fixtures/**` would match at ANY depth; nothing today rejects a leading-wildcard pattern | spec_artifacts_process/manifest.yaml:512, #56 |

## Detail

**FND-001 — #54, approved.** The defect was real and well-diagnosed: the
contract admitted `⚠️` at `column_patterns.Status` while `traceability.status`
classed it as nothing, so `class_of` returned `Unknown` and a `⚠️` row was
exempt from the status-lie check by construction. Two things make the fix
exemplary rather than merely correct. First,
`test_column_vocabularies_have_one_source` was upgraded from a one-directional
containment check — the direction that could never catch this — to set equality
both ways, with named diagnostics for each direction. Second, the commit records
a real red-test step: the new assertion was run against the pre-change manifest
and confirmed to fail with `admitted but not classed: ['⚠️']` before the
manifest was touched. A drift guard that cannot fail is the defect it exists to
prevent, and this one was proven able to fail. The second hardcoded pattern copy
in `test_testmatrix_body_extraction_contract` was fixed and cross-referenced,
and the corpus was normalized to zero `⚠️` rows before the enforcing change
merged (FR-003-CON-1: normalize before enforce). Nothing to remediate.

**FND-002 — #55 shipped an invariant with no guard.** The three globs
(`tests/fixtures/**`, `tests_integration/fixtures/**`, `fixtures/**`) landed in
`manifest.yaml:509-512` with no test change in the PR at all. The existing
suite gives only incidental coverage — `test_manifest_loads` and
`test_manifest_validates_against_fr035_schema` prove the key loads and passes
the iso shape gate (this is real: declaring the key against the old toolchain
turned 38 of 81 tests red) — but nothing pins the glob values, and the
load-bearing invariant "`tests/**` MUST NEVER APPEAR HERE" exists only as prose:
the manifest comment block (manifest.yaml:490-508), the iso schema's
`description` string, and a quire-rs doc comment. Today
`source_exclude: ["tests/**"]` or `["**"]` loads, validates, and silently
subtracts the evidence tree from the symbol walk — excluded files' trace tags
never bind, and their rows read as unbacked/status-lies, indistinguishable from
missing tests. The mechanical guard (pin the list; reject `**`, `tests/`-prefix,
leading wildcard) is ticketed as **#56**; the companion schema-value constraint
is **spec-artifacts-iso#29**.

**FND-003 — TC-070 is an unbacked ✅.** #55 added two matrix rows to
`spec/tests.md`: `FR-004-AC-1 | TC-070 | ✅ Complete` and a TC-070 summary row
marked `✅`. `grep -rn "TC-070\|source_exclude" tests/` returns nothing — the id
is bound to no test. The row's own description ("is declared and loads … still
validates against the FR-035 schema") is true of the incidental coverage in
FND-002, but the repository's convention (and #54's whole argument) is that a
`✅` row names tests that verify it, not behavior that happens to hold. The same
defect class was found in quire-cli #54 (FR-015-AC-5 minted without a test) —
it is a batch-wide pattern, not a one-off. Disposition: #56's contract test
should carry the `TC-070` binding when it lands, which retires this finding
without a matrix edit.

**FND-004 — the ordering hazard #55 documented is the state it shipped.** The
PR text is unusually clear that publishing a manifest declaring `source_exclude`
before the consuming engine ships fails module load outright
(`deny_unknown_fields` — "module load fails, for every command that loads the
module set"), and it even corrected the dependency chain to four hops
(quire-rs v0.41.0 → quire-cli v0.28.0 + the `quire` Python wheel →
spec-artifacts-iso v0.18.0 → this module). Yet v0.23.0 was tagged at the merge
commit while quire-cli v0.28.0 — the first tolerant release — has no GitHub
release, no publish workflow run, and npm serves 0.27.0 (verified 2026-08-21).
Any environment that installs SAP v0.23.0 against a published quire-cli gets a
hard `unknown field 'source_exclude'` failure on every command. The local
toolchain only works because both consumers were rebuilt by hand. Remediation
is owned by the release work packages (quire-cli consolidated v0.29.0 release;
GitHub Releases for iso v0.18.0 / SAP v0.23.0), not by this repo's code.

**FND-005 and the glob-safety evidence.** Recorded so the verdict is
re-checkable rather than folklore. The globs as shipped are **SAFE**:

- globset **0.4.18** (quire-rs Cargo.lock) compiles patterns start-anchored
  against the full scope-relative path: `fixtures/**` → `(?-u)^fixtures/.*$`.
  A pattern anchors at the start unless it opens with `**/`, so
  `tests/fixtures/**` matches `tests/fixtures/a/b.rs` and cannot reach
  `src/tests/fixtures/x.rs` (quire-rs src/symbols/mod.rs — `ExcludeSet` — and
  src/corpus/declared_tables.rs).
- quire-rs pins the anchoring in a regression test:
  `tc944_declared_globs_subtract_from_the_source_walk` asserts "a start-anchored
  glob must not match a nested directory of the same name", and
  `tc944_source_globs_cannot_un_exclude_the_document_root` pins the
  subtract-only property.
- Ecosystem sweep, re-verified at review time: every top-level `fixtures/`
  directory across ~/dev (15 directories in 13 repositories, including three
  ecaz worktrees; the original exploration counted 12) contains **zero** source
  files (`.rs .py .ts .tsx .js .go`) — so the bare `fixtures/**` glob is
  currently a complete no-op ecosystem-wide, and the only intended target is
  quire-rs's own `tests/fixtures/`. Nested `fixtures/` trees that do hold real
  source are unreachable because of the anchoring.
- The latent footgun is the flag, not the patterns: `literal_separator=false`
  means `*` matches across `/`, so a future `*/fixtures/**` would match at any
  depth — the exact unanchored failure mode everything above rules out. #56's
  leading-wildcard rejection is the cheap fence.

One further observation, no finding minted: `ExcludeSet::compile` silently
drops globs that fail to compile and the walk `continue`s on a match with no
diagnostic or count — an excluded file's legitimate backing silently becomes
unbacked rows. That is quire-rs surface (observability ticket in the batch
follow-ups), out of this repository's scope; noted here because this manifest
is now the largest user of the key.
