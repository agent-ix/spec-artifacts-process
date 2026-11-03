---
id: SR-20261102086803
title: "IR-868 process guard adoption code-review"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR129; linked cohort guard adoption, actual inherited draft scope and Python/public CLI controls"
review_set: subset
---

## Summary

Python/declaration code review records two medium behavior/evidence findings; no shell injection, copied semantic type or fixture suppression found. Native subprocess inputs are argument vectors and failures are asserted.

Frozen processPR129 sourcea503c3c44421cc173a4f35b3456a0ad1f1d56630 overmaine6ce2f63; linked CLI14497be14a selects merged engine56633d82907. Separate CLI code/gap reviews are clean and already posted; this artifact set owns process review only. Old other-lanePR123 and its artifact ownership remain untouched. Read AGENTS, actual four-file diff, changed FR004/TC rows and Python declaration tests, plus relevant code/Python and scoped spec method instructions. No source/worktree edits, Cargo/backend jobs, CI, publish/credentials or merge actions by reviewer. Only small read-only Python regex and explicitly scoped built-CLI validator probes were executed; no upstream corpus/code copied.

The mandatory syntax:rust_attribute guard is declared on the new Rust form, which remains separate from markers and the retained Rust/Python/TypeScript comment forms. Live TC156 has no xfail/skip: authentic block-comment/raw-string adverse examples share a run with a genuine outer-attribute control, and only that control binds. Native CLI production-scope tests assert exact edges and zero backed evidence, with existing comment scope retained. These actual guarded inputs address the prior123 source-position defect; old findings are not re-owned or silently rewritten here. Module regex/template and exact engine candidate ownership retain their separate authorities. Unsupported engines must reject guard input rather than fall back. Consumer Python-wheel/release qualification remains explicitly future work.

The inherited candidate also adds a combined Analyze table extraction/reference, AC23/24 and TC152/153 and changes manifest0.2.1->0.2.2. This actual scope is recorded accurately; no release is implied. Its status-lie control has real adverse and backed/planned controls. Its TC152 declaration-only placeholder lacks the new behavioral acceptance though the built CLI now supports it. The owner has identified these as accidental old123 additions and proposes reverting only that unlanded unrelated feature/version bump to original main, which is a valid scope correction rather than an exception to an existing main requirement. Original main requirements and other-lane123 stay intact.

Native regex probe reproduces a real trailing-comma whitespace false negative; add independently authored whitespace/newline cases and actual guarded engine evidence. Low specification subject ambiguity is separate. Preserved built-CLI process target34PASS/0FAIL and package coverage100percent are meaningful, but do not cover these omitted cases. The100percent number covers six package initializer statements, not every manifest semantic clause. Locked Python3.13 tooling Ruff/Black PASS and two changed-doc validations pass with advisories. Frozen matrix and quoin advice were generated; executable tests are reviewer-selected appropriate evidence for declared syntax and adverse cases, not assumed complete from a tag count. Final aggregate/hosted and release/install acceptance remain owed. Plan completion: not assessed

## Verdict

Scoped method verdict **CONDITIONAL**, with final gates unqualified.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The Rust attribute regex permits an immediate trailing comma but rejects legal token whitespace before it: #[implements("FR-001",)] matches while #[implements("FR-001" ,)] and a newline before that comma do not. ix-trace-rs consumes Rust TokenStream, whose whitespace does not change these literal/comma tokens. Permit that whitespace and add Python declaration plus actual guarded engine controls so the final complete-candidate match retains valid trailing-comma forms. | spec_artifacts_process/manifest.yaml:rust-implements-attribute.pattern |
| FND-002 | medium | The inherited candidate adds a combined-table feature/AC23/TC152 but only checks its declaration shape, with no public behavioral TC152 oracle; spec and Known Limits still cite an old0.36.2 unknown-type blocker. Actual new CLI scoped probes accept conforming and absent tables and reject a renamed required column, so that blocker is stale. Complete this feature evidence/status, or remove the unrelated draft additions under the explicitly small guard-adoption scope; do not waive or narrow any original-main criterion. | tests/test_traceability_declaration.py:test_combined_table_extraction_declaration / spec/tests.md TC152 |

## Examined scope

```yaml
scope:
- id: FR-004-AC-10
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: '`trace_tags.implements` declares exactly the existing templated Rust `Implements:`
    line-comment form plus the new templated Rust `#[implements(...)]` attribute form,
    and exactly one templated `Implements:` line-comment form each for Python and
    TypeScript.'
- id: FR-004-AC-23
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: TestMatrix body extraction accepts a present `Nonfunctional and Stakeholder
    Coverage` table with columns `Requirement`, `Acceptance Criteria`, `Test Cases`,
    `Status`, rejects a present table with a renamed required column, and permits
    that table to be absent.
- id: FR-004-AC-24
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: '`quire coverage` reports an unbacked Complete row in each Analyze coverage
    table as a status lie, while a backed Complete row and an unbacked Planned row
    in the combined table are not lies.'
- id: FR-004-AC-25
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: The Rust `implements` form captures each separately quoted id in a one-
    or multi-literal `#[implements("ID1", "ID2")]` attribute, including a trailing
    comma and an `interface_004-AC-1` id.
- id: FR-004-AC-26
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: The Python and TypeScript `implements` forms require `Implements:` before
    a comma-separated id list and bind no id from a sentence that merely names a requirement.
- id: FR-004-AC-27
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: Rust `implements` binds no scope from a syntactically complete attribute
    example inside a block comment or multi-line raw string.
- id: FR-004-AC-28
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: The Rust `implements` attribute mints production implementation scope and
    does not mint verification evidence.
- id: FR-004-AC-29
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: Rust `implements` binds a valid attribute followed by a trailing `//` comment
    or by its item on the same line.
- id: FR-004-AC-30
  path: spec/functional/FR-004-traceability-declaration.md
  role: examined
  excerpt: Malformed Rust attributes and prose naming a requirement bind no implementation
    scope.
- id: guard-declaration
  path: spec_artifacts_process/manifest.yaml
  role: examined
  excerpt: 'syntax: rust_attribute'
- id: mandatory-adverse
  path: tests/test_traceability_declaration.py
  role: examined
  excerpt: 'def test_quire_does_not_credit_attributes_in_rust_text(tmp_path: pathlib.Path)
    -> None:'
- id: TC152-placeholder
  path: tests/test_traceability_declaration.py
  role: examined
  excerpt: '"""Check the optional combined-table declaration pending validator support."""'
```

## Corrected guard-adoption scope dispositions

Disposition verified at corrected process4357f4e2c97e6068dfe85b7442f70e35f276ebb7, originalPR129. Actual diff allows whitespace/newline before optional trailing comma in the capture, adds Python positive cases and actual built-CLI production controls for spaced/newline commas, and names the Rust implements attribute form explicitly. Preserved corrected full declaration target32PASS/0FAIL with package initializer coverage100percent, including the live valid-tail and mandatory adverse guard controls. This replaces the earlier34count because two unrelated TestMatrix tests were removed; no guard-adoption test is skipped/xfail or weakened.

The accidental unlanded VER25/TestMatrix additions (combined-table extraction/reference, AC23/24, TC152/153, placeholder/status text and version bump) are removed back to exact original-main behavior. Manifest version is restored0.2.1. Original-main requirements remain untouched, other-lane123 is not rewritten and AC25..30 numbering is retained without reusing the withdrawn draft IDs. The finding's scoped-removal fix is not a waiver or deferment of an existing-main acceptance obligation and does not claim TC152 completed. No TestMatrix feature is shipped by this corrected PR.

No new findings. Code/gap/base/integrity/EARS/evidence scoped verdicts nowPASS. Existing EARS advisory pairs and the unchanged quality agentless-passive statement are baseline advisories, not new fixes/waivers. Corrected-head final aggregate/hosted gates remain the owner's responsibility and are not inferred from the32declaration tests; release/consumer-wheel qualification remains unclaimed. Linked CLI144 has its separate clean two-SR review. Reviewer ran no Cargo/backend/CI and edited no reviewed source/worktree.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Regex adds whitespace before the optional trailing comma. Python cases include space/newline variants; live guarded CLI test asserts both new production scope IDs alongside previous trailing-comment and same-line controls. |
| FND-002 | fixed | Fixed by removing only the accidental unlanded TestMatrix draft scope and restoring exact original-main declarations/tests/version. No original-main AC narrowed; no false TC152 completion, no new waiver, and no other-lane123 rewrite. The restored table-kind assertion is the surviving same test artifact. |

```yaml
dispositions:
- fnd: FND-001
  outcome: fixed
  after_excerpt: ('#[implements("FR-001" ,)]', ["FR-001"]),
  reason: Regex adds whitespace before the optional trailing comma. Python cases include
    space/newline variants; live guarded CLI test asserts both new production scope
    IDs alongside previous trailing-comment and same-line controls.
- fnd: FND-002
  outcome: fixed
  after_excerpt: expected = ["functional-coverage", "test-case", "traces-to"]
  reason: Fixed by removing only the accidental unlanded TestMatrix draft scope and
    restoring exact original-main declarations/tests/version. No original-main AC
    narrowed; no false TC152 completion, no new waiver, and no other-lane123 rewrite.
    The restored table-kind assertion is the surviving same test artifact.
```


## Current-main consumer refresh

This independent scoped refresh examines process PR129 against current main after CLI PR145 merged, using CLI 0.38.1 / engine 0.51.0 and the isolated installed current-main Python wheel. It does not claim a released consumer installation. The four production/spec/test files retain the main retirement vocabulary unchanged. All historical finding rows and dispositions above remain unchanged. Their latest fixed outcomes were rechecked: token whitespace before the trailing comma is accepted, the attribute obligation names its subject, and unrelated draft TestMatrix scope remains absent.

The mandatory rust_attribute guard remains declared. Existing exact production-edge assertions preserve comment scopes and zero backed verification; block-comment and raw-string adverse inputs share a genuine outer-attribute control. Same-line, trailing-comment, malformed-input and whitespace/newline-comma controls discriminate their respective cases. Independent reviewer rerun: 33 declaration tests passed, no skips or xfails. Preserved owner qualification adds the Registry/current-wheel control for 34 focused passes and package initializer coverage 100 percent (six statements, not semantic coverage). Ruff, Black and changed-document structural checks passed in retained qualification logs.

Actual computed matrix and deterministic quoin advise were rerun. Repository-wide baseline untagged criteria preclude a repository-wide gap PASS; this refresh assesses changed obligations only. No applicable AssuranceProfile was found. Optional semantic gap-review was not invoked. Plan completion: not assessed. No Rust/Cargo production changes occur in this PR, so a Rust review lane is inapplicable. EARS advisories concern retained statements, and no new requirement grammar defect was found. Test is a suitable reviewer-selected evidence method for the changed syntax and adverse cases; advisor recommendations are advisory.

The unchanged full schemas-check and semantic suite remain unavailable because private @agent-ix/semantic-core installation returns E401 and offline cache is missing. This is disclosed as unavailable aggregate evidence; the guard declaration, Registry and document checks do not depend on that npm package. No blanket registry gate or lock-refresh condition is added.

## New findings (disposition pass 2)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | medium | Existing tests for new FR-004-AC-25, FR-004-AC-26, FR-004-AC-28, FR-004-AC-29 and FR-004-AC-30 carry only TC trace IDs. The current-main computed matrix reports all five criteria untagged. Add the corresponding FR acceptance-criterion IDs to the existing tests; passing tests and TestMatrix prose do not establish those bindings. | tests/test_traceability_declaration.py:599; spec/functional/FR-004-traceability-declaration.md |

## Refresh verdict

FAIL for gap-analysis; other affected methods CONDITIONAL. FND-003 is still open and blocks scoped readiness. Existing behavioral tests need criterion tags, not replacement tests.

## Refresh examined scope

```yaml
scope:
  - {"id": "FR-004-AC-10", "path": "spec/functional/FR-004-traceability-declaration.md", "role": "examined", "excerpt": "`trace_tags.implements` declares exactly the existing templated Rust `Implements:` line-comment form plus the new templated Rust `#[implements(...)]` attribute form, and exactly one templated `Implements:` line-comment form each for Python and TypeScript."}
  - {"id": "FR-004-AC-19", "path": "spec/functional/FR-004-traceability-declaration.md", "role": "examined", "excerpt": "The `interface-acceptance-criterion` target declares `required: false`, so a corpus with no `interface` documents or an `interface` document without an Acceptance Criteria section is healthy; and an `interface_NNN-AC-N` id resolves everywhere an `FR`/`NFR` acceptance-criterion id already does \u2014 `inspection-obligation`, `traces-to`, the `Traces To` column check, the declared `legacy` and `implements` forms, and a new `interface-verification` reference covering its own `Verification` column."}
  - {"id": "FR-004-AC-25", "path": "spec/functional/FR-004-traceability-declaration.md", "role": "examined", "excerpt": "The Rust `implements` attribute form captures each separately quoted id in a one- or multi-literal `#[implements(\"ID1\", \"ID2\")]` attribute, including a trailing comma and an `interface_004-AC-1` id."}
  - {"id": "FR-004-AC-26", "path": "spec/functional/FR-004-traceability-declaration.md", "role": "examined", "excerpt": "The Python and TypeScript `implements` forms require `Implements:` before a comma-separated id list and bind no id from a sentence that merely names a requirement."}
  - {"id": "FR-004-AC-27", "path": "spec/functional/FR-004-traceability-declaration.md", "role": "examined", "excerpt": "Rust `implements` binds no scope from a syntactically complete attribute example inside a block comment or multi-line raw string."}
  - {"id": "FR-004-AC-28", "path": "spec/functional/FR-004-traceability-declaration.md", "role": "examined", "excerpt": "The Rust `implements` attribute mints production implementation scope and does not mint verification evidence."}
  - {"id": "FR-004-AC-29", "path": "spec/functional/FR-004-traceability-declaration.md", "role": "examined", "excerpt": "Rust `implements` binds a valid attribute followed by a trailing `//` comment or by its item on the same line."}
  - {"id": "FR-004-AC-30", "path": "spec/functional/FR-004-traceability-declaration.md", "role": "examined", "excerpt": "Malformed Rust attributes and prose naming a requirement bind no implementation scope."}
```

## Refresh dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-003 | still-open | Five new acceptance criteria lack criterion trace decorators in the computed current-main matrix. |


## Criterion-binding fix dispositions

Independently inspected the fix: exactly five existing test decorators gain their corresponding FR criterion IDs; assertions and the existing AC27 adverse-control tag are unchanged. Recomputed current-main matrix reports AC25 through AC30 all tagged to their intended behavioral tests. This is criterion binding, not an assertion that tagged status itself proves behavior. The reviewed test bodies assert multi-literal and comma whitespace captures, comment keyword/prose rejection, exact production scope without backed evidence, real-attribute versus comment/raw-string controls, valid trailing forms, and malformed rejection respectively.

Retained post-fix qualification reports 34 focused passes without skips or xfails, 100 percent package initializer coverage (six statements), Ruff and Black PASS, and all eight changed/review documents structurally valid. Current-main CLI and isolated wheel qualification remain applicable. The unchanged semantic aggregate remains unavailable because private npm installation returns E401 and the offline cache is missing; no changed guard requirement requires that package. No release/install-from-published-artifact claim is made. No new findings.

| FND | outcome | reason |
| --- | --- | --- |
| FND-003 | fixed | Added acceptance-criterion IDs to the five existing test decorators; recomputed current-main matrix binds all six new criteria to their intended tests. |

```yaml
dispositions:
  - fnd: FND-003
    outcome: fixed
    after_excerpt: |
      @pytest.mark.trace("TC-154", "FR-004-AC-25")
      @pytest.mark.trace("TC-155", "FR-004-AC-26")
      @pytest.mark.trace("TC-157", "FR-004-AC-28")
      @pytest.mark.trace("TC-158", "FR-004-AC-29")
      @pytest.mark.trace("TC-159", "FR-004-AC-30")
```

## Current disposition verdict

PASS for this bounded method and READY for bounded PR129 handoff. All historical and refresh findings are fixed. This is not a repository-wide gap PASS or a claim that the unavailable full semantic aggregate passed. Plan completion: not assessed.
