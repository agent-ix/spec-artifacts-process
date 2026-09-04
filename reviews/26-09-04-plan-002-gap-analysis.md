---
id: SR-017
title: "Gap analysis — Plan-002 semantic module contract"
type: SpecReview
analysis: gap-analysis
scope: "plan/Plan-002-semantic-module-contract/, spec/tests.md, spec_artifacts_process/, tests/"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/Plan-002"
    type: "reviews"
  - target: "ix://agent-ix/spec-artifacts-process/TM-001"
    type: "references"
---
# SR-017: Gap analysis — Plan-002 semantic module contract

## Summary

Post-implementation gate over Plan-002. All ten tasks are `done`. `quire coverage --scope .`
reports **133/270 rows backed (49%)**, against **56/128 (44%)** on `origin/main`, with **zero
untracked symbols** and **zero status lies introduced by this branch**. Every row this ticket
added is either backed by a test that runs, or carries an explicit non-passing marker with the
upstream issue that owns it.

The semantic review (step 4) was **not run**: it was not requested, and steps 1–3 already produce
a decisive verdict.

## Verdict

**CONDITIONAL** — no unbacked live row and no incomplete task, but three medium findings, all of
them upstream defects the branch records rather than defects it can close.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | IT-002 has no green run: Quoin refuses every artifact-type semantic module, this one and the merged `spec-artifacts-iso` alike. Held as `xfail(strict=True)` so the boundary is exercised on every opted-in run. `agent-ix/quoin#347`, GAP-003. | tests/test_quoin_install_roundtrip.py, spec/integration/IT-002-quoin-module-install.md |
| FND-002 | medium | FR-010-AC-9 is unsatisfiable against quire 0.46.0 and TC-135 carries `❌` in the matrix rather than a marker that would read as complete. `agent-ix/quire-rs#221`, `#394`; and `#400` for the digest that is never checked. GAP-004. | spec/tests.md:300 |
| FND-003 | medium | The `acceptance-criterion` trace channel is 1/125 backed. This repository tags TC ids and reaches criteria through the matrix row; the convention predates #78 (0/65 on `origin/main`) and this ticket does not change it. Recorded as GAP-005 rather than closed, because changing a tagging convention is an ecosystem decision. | spec/tests.md, quire coverage |
| FND-004 | low | `tests/test_evidence_archetypes.py::test_tc047_adoption_is_optional` fails. It fails identically on `origin/main` and is fixed by `737987b` on the unmerged `epic/264-assurance-integration`; this branch neither causes nor hides it, and deliberately does not carry that branch's traceability edit, which would breach its own byte-identity guard (TC-136). | tests/test_evidence_archetypes.py:244 |
| FND-005 | low | Thirteen Test Case Summary rows were sitting in the Functional Requirement Coverage table on `origin/main` and minted nothing. Relocated here under `agent-ix/spec-artifacts-process#79`; the engine hole that hid it is `agent-ix/quire-rs#396`. Quantified: the `test-case` channel mints 61 rows on main and 138 after. | spec/tests.md, agent-ix/quire-rs#396 |
| FND-006 | low | No reverse gap found: every file this branch adds is owned by a requirement — the TypeSpec source and generator by FR-009, the manifest block by FR-010, `mappings.yaml` and the reference implementation by FR-011, the skeletons and negatives by FR-012, the role map by FR-013, the consumer measurement by NFR-001, the install roundtrip by IT-002. | — |

## Coverage

| Channel | Backed / total | On `origin/main` |
| --- | --- | --- |
| `test-case` | 130 / 138 (94%) | 56 / 61 (92%) |
| `acceptance-criterion` | 1 / 125 | 0 / 65 |
| `nfr-acceptance-criterion` | 2 / 5 | — (no NFR existed) |
| `stakeholder-validation-criterion` | 0 / 2 | 0 / 2 |
| **headline** | **133 / 270 (49%)** | **56 / 128 (44%)** |

**What the headline counts, and why it is not the `spec/tests.md` figure.** `quire coverage`
counts every id minted by any declared trace target: 138 Test Case Summary rows *plus* 125
acceptance criteria, 5 NFR criteria and 2 stakeholder validation criteria — 270 rows over four
channels. "Backed" means a real trace tag in the source names that id.

`spec/tests.md` counts something narrower: of its 138 Test Case Summary rows, **130 carry `✅`**,
and each of those 130 is backed by a `@pytest.mark.trace` on a test that runs. That is the
`test-case` channel at 130/138 (94%), and it is the same measurement read against the same
population. The eight rows that are not `✅`: six pre-existing `🚧` rows inherited from `main`,
one `⛔` (TC-126, retired because SR-013 FND-004 made FR-010-AC-3 the single normative baseline
claim and the row duplicated TC-091), and one `❌` (TC-135, the strict expected failure).

The gap between 94% and 49% is entirely the `acceptance-criterion` channel, which this
repository has never tagged directly (FND-003). Averaging the two numbers, or quoting either
without its population, would be the reporting error this module's own guidance forbids.

## Plan completion

Ten of ten tasks `done`. Both gates held:

- **Gate 1 (Task-010)** — `SpecReview` proved end to end through model, mapping entry, skeleton,
  authored golden record and two negative fixtures before the other eleven types were attempted.
  The golden record was not regenerated to make the mapping pass.
- **Gate 2 (Task-014)** — two consumers re-validated at 0.1.0 and 0.2.0.
  `spec-objects-business` @ `d1840b8`: **27 documents graded, 0 error findings under either
  version, 0 regressions**. `filament-core-data` @ `de49a49`: **165 documents, 0 / 0 / 0**.
  The measurement is proved able to fail — narrowing the `Status` pattern to `✅` alone yields
  **8** regressions on the first and **4** on the second — and proved not to be vacuous: the
  document count is asserted non-zero and equal on both sides. A first version of it compared
  nine `SymlinkLoop` lines to nine `SymlinkLoop` lines and reported success; that is why the
  count guard exists.
