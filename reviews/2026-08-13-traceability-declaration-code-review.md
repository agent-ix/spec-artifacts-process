---
id: SR-003
title: "Code review — traceability declaration (FR-004)"
type: SpecReview
analysis: code-review
scope: "spec_artifacts_process/manifest.yaml, tests/test_traceability_declaration.py"
review_set: subset
---

# SR-003: Code review — traceability declaration (FR-004)

## Summary

Reviewed the FR-004 `traceability:` declaration and its tests against the real
corpus rather than against the fixture it started from. Three defects, all in
the declaration and all found by measuring what it bound in quire-rs, quoin and
this repo. Every one is fixed on the branch; this records what they were,
because each is a trap the next declaration will hit.

## Verdict

**CONDITIONAL** — no high findings survive; one medium and two low, all fixed.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The line-comment legacy form bound prose that merely names a requirement, claiming coverage a test does not provide | spec_artifacts_process/manifest.yaml:555 |
| FND-002 | low | The canonical marker matched itself inside documentation, minting a trace id of literally `...` | spec_artifacts_process/manifest.yaml:531 |
| FND-003 | low | A pattern used a Rust-regex-only escape (`\x{2013}`) that `re.compile` rejects | spec_artifacts_process/manifest.yaml:555 |
| FND-004 | low | `document: spec/evals.md` is one repo's filename in an ecosystem-wide module; harmless but carried by every consumer | spec_artifacts_process/manifest.yaml:390 |

**Disposition.** FND-001 to FND-003 are fixed on this branch. FND-004 is the
visible cost of an engine gap — a trace target cannot exclude fixture paths, so
archetype binding is unusable and paths must be enumerated — filed as
agent-ix/quire-rs#61 and left in place until it lands.

## Detail

**FND-001.** `# FR-003-CON-1 sweep found in real matrices` — a wrapped prose line
in this repo's own tests — bound that constraint to a test that does not verify
it. It surfaced only because `-CON-` ids are not minted; the same wrapped line
naming an `-AC-` id would have marked that criterion backed with no signal at
all.

The first fix was wrong and measurement said so: requiring a bare id dropped
quire-rs from 148 backed rows to 84, because quire-rs writes 344 line comments
and its convention is an id *plus* prose (`// TC-480 / FR-025-AC-1: len == …`).
The discriminator is punctuation after the id — `:` `/` `(` `,` a dash, or end
of line. A tag has it; a sentence flowing through the id does not.

Net effect: 143/905 on quire-rs. The five bindings this drops against the
unanchored form are all commentary (`// TC-002 claims ✅ but nothing binds it.`),
so **148 was inflated and 143 is the honest number.**

**FND-002.** `bind_symbol` scans a symbol's raw source with no comment
awareness, so `#[trace(...)]` written in a doc comment *explaining the marker
form* minted a trace id of `...`. Arguments must now be quoted — which is how
FR-051 writes them and what `marker_ids` already prefers.

**FND-003.** These patterns are consumed by two regex engines: the Rust engine
at module load, and Python in TC-031. `\x{2013}` compiles in one and not the
other. TC-031 caught it on the first run, which is the whole reason that
assertion exists.

**FND-004.** `spec/evals.md` exists in exactly one repo out of the ecosystem
(quoin), against `spec/tests.md` in 184 and `spec/matrix.md` in 3. An absent file
contributes no rows, so the cost is a dead declaration everyone carries; the
alternative is quoin shipping its own module, which is heavier.

The path enumeration exists only because archetype binding drags test fixtures
in and cannot see `tests.md` at all. Both are engine gaps, filed as
agent-ix/quire-rs#61. When that lands, nine declaration entries collapse to two
and this finding disappears with them.

## Coverage

- Reconciliation: quire coverage (module spec-artifacts-process, working tree)
- Rows backed by a tagged test: 27 / 60 (this repo), 144 / 907 (quire-rs), 94 / 273 (quoin)
- Module test suite: 43 passed, 1 skipped, 1 xfailed
- Semantic review: skipped
