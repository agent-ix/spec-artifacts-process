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

## Passing today

- `core-web-ui`
- `github-projects`
- `job-execution`
- `settings-sdk`
- `spec-artifacts-process`
- `ticket-runner`

## Not a TestMatrix (unaffected)

`auth-py`, `auth-settings-react`, `data-store`, `electron-hello`, `fastapi-service`, `knowledge-graph`, `py-observability`, `quire`, `scenario-service`, `spec-objects-business`, `spec-objects-operational`, `spec-reports`

## Per-repo results

Full diagnostics per repo are in `2026-08-04-tests-md-sweep.json` (machine-readable, one entry per repo).

| Repo | Diagnostics | Causes |
|---|---|---|
| `quire-rs` | 153 | type-vocabulary ×84, traces-to-pattern ×43, status-vocabulary ×23, test-id-pattern ×3 |
| `ecaz` | 100 | status-vocabulary ×46, type-vocabulary ×45, traces-to-pattern ×6, columns ×2, test-id-pattern ×1 |
| `ecaz-task165` | 100 | status-vocabulary ×46, type-vocabulary ×45, traces-to-pattern ×6, columns ×2, test-id-pattern ×1 |
| `ecaz-task161` | 99 | status-vocabulary ×45, type-vocabulary ×44, traces-to-pattern ×6, test-id-pattern ×2, columns ×2 |
| `ecaz-task162` | 99 | status-vocabulary ×45, type-vocabulary ×44, traces-to-pattern ×6, test-id-pattern ×2, columns ×2 |
| `ecaz-task163` | 99 | status-vocabulary ×45, type-vocabulary ×44, traces-to-pattern ×6, test-id-pattern ×2, columns ×2 |
| `ecaz-task164` | 99 | status-vocabulary ×45, type-vocabulary ×44, traces-to-pattern ×6, test-id-pattern ×2, columns ×2 |
| `ix-cli` | 91 | status-vocabulary ×55, type-vocabulary ×25, traces-to-pattern ×11 |
| `workflow-execution` | 83 | test-id-pattern ×77, columns ×4, type-vocabulary ×2 |
| `ecaz-task137` | 82 | status-vocabulary ×37, type-vocabulary ×36, traces-to-pattern ×5, test-id-pattern ×2, columns ×2 |
| `ecaz-task139` | 82 | status-vocabulary ×37, type-vocabulary ×36, traces-to-pattern ×5, test-id-pattern ×2, columns ×2 |
| `ecaz-task168` | 82 | status-vocabulary ×37, type-vocabulary ×36, traces-to-pattern ×5, test-id-pattern ×2, columns ×2 |
| `filament-editor` | 78 | test-id-pattern ×46, status-vocabulary ×25, type-vocabulary ×4, traces-to-pattern ×3 |
| `filament-ui-shared` | 52 | test-id-pattern ×47, type-vocabulary ×5 |
| `filament-view-review` | 48 | test-id-pattern ×45, type-vocabulary ×3 |
| `cloud-manager-ui-services` | 45 | traces-to-pattern ×18, type-vocabulary ×7, test-id-pattern ×6, other ×6, status-vocabulary ×6, columns ×2 |
| `cloudmanager-local-sync` | 41 | status-vocabulary ×19, traces-to-pattern ×14, columns ×5, type-vocabulary ×2, other ×1 |
| `spec-comments` | 29 | test-id-pattern ×23, type-vocabulary ×6 |
| `spec-hierarchy` | 24 | test-id-pattern ×22, type-vocabulary ×2 |
| `ts-plugin-kit` | 24 | type-vocabulary ×12, traces-to-pattern ×9, columns ×3 |
| `code-diff-renderer` | 23 | test-id-pattern ×12, type-vocabulary ×5, columns ×4, traces-to-pattern ×2 |
| `status-service` | 23 | status-vocabulary ×23 |
| `chat-markdown-renderer` | 18 | type-vocabulary ×7, test-id-pattern ×6, columns ×4, other ×1 |
| `scenario-runner` | 15 | status-vocabulary ×13, missing-fr-coverage ×1, columns ×1 |
| `spec-reviews` | 15 | test-id-pattern ×15 |
| `ix-agent-terminal-control` | 13 | test-id-pattern ×12, columns ×1 |
| `permission-service` | 13 | traces-to-pattern ×8, status-vocabulary ×4, type-vocabulary ×1 |
| `cli-agent-evals` | 12 | status-vocabulary ×8, traces-to-pattern ×3, missing-fr-coverage ×1 |
| `filament-view-editor` | 10 | test-id-pattern ×10 |
| `filament-ide` | 9 | type-vocabulary ×7, traces-to-pattern ×1, columns ×1 |
| `spec-view-project` | 9 | test-id-pattern ×9 |
| `config-service` | 8 | type-vocabulary ×5, columns ×3 |
| `user-profile-ui` | 6 | columns ×5, other ×1 |
| `deploy-worker` | 5 | traces-to-pattern ×5 |
| `ix-cli-core` | 5 | columns ×4, missing-test-case-summary ×1 |
| `ix-ui` | 5 | columns ×3, missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-workflow-runner` | 5 | columns ×4, missing-test-case-summary ×1 |
| `naming-lib` | 5 | type-vocabulary ×3, columns ×2 |
| `quire-cli` | 5 | columns ×4, other ×1 |
| `settings-react` | 5 | status-vocabulary ×5 |
| `ecaz-landing` | 4 | columns ×3, other ×1 |
| `filament-analysis-worker` | 4 | columns ×2, missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `filament-domain-events` | 4 | columns ×2, missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `filament-editor-app` | 4 | columns ×2, missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `filament-editor-integration` | 4 | columns ×2, missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-sandbox-backend` | 4 | columns ×3, type-vocabulary ×1 |
| `py_code` | 4 | traces-to-pattern ×3, missing-fr-coverage ×1 |
| `sync-github-service` | 4 | traces-to-pattern ×3, type-vocabulary ×1 |
| `workflow-service` | 4 | columns ×2, missing-fr-coverage ×1, other ×1 |
| `agent-duncan` | 3 | missing-fr-coverage ×1, missing-test-case-summary ×1, columns ×1 |
| `catalog-service` | 3 | missing-fr-coverage ×1, missing-test-case-summary ×1, columns ×1 |
| `config-overlay` | 3 | type-vocabulary ×2, traces-to-pattern ×1 |
| `filament-view-object` | 3 | columns ×2, missing-test-case-summary ×1 |
| `ix-agent-sandbox-control` | 3 | columns ×3 |
| `settings-service` | 3 | missing-fr-coverage ×1, columns ×1, other ×1 |
| `agent-cli-daemon` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `agent-config-cookiecutter` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `agent-config-loader` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `agent-config-models` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `auth` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `auth-fastapi` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `auth-service` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `build-chain` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `chat-input` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `chat-window` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `cloud-manager` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `cloud-manager-app` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `cloud-manager-ui` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `cloud-manager-ui-components` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `cloud-manager-ui-config` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `cloud-manager-ui-core` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `cloud-manager-ui-dashboard` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `cloud-manager-ui-domain` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `cloud-manager-ui-flow-editor` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `cloud-manager-ui-repos` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `cloud-manager-ui-types` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `code-block-editor` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `code-block-renderer` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `code-diff-editor` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `cookiecutter-service` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `deploy-app` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `event-models` | 2 | columns ×1, other ×1 |
| `event-schema-registry` | 2 | columns ×1, other ×1 |
| `fastapi-cookiecutter` | 2 | columns ×1, other ×1 |
| `faststream-worker` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `filament-core-service` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `filament-editor-gateway` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `filament-ide-rs` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `filament-parser-lib` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `filament-review-service` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `filament-ui` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `filament-view-document` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `filament-view-ecosystem` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `filament-view-standard` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `flowkit` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `gateway-bff-contract` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `github-models` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `helm-charts` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `identity` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-agent-browser-control` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-agent-chat` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-agent-chat-app` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-agent-client` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-agent-core` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-agent-discord-adapter` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-agent-fastapi` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-agent-messaging-bridge` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-agent-messaging-sdk` | 2 | columns ×1, missing-test-case-summary ×1 |
| `ix-agent-telegram-adapter` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-agent-test-kit` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-agent-tools` | 2 | columns ×1, missing-test-case-summary ×1 |
| `ix-coder-workflows` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-local-build` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-local-data` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-local-llm` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ix-local-observability` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `js-deps` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `local-workspace-service` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `loki-mcp` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `markdown-editor` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `mcp-gateway` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `mcp-gateway-ui` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `mesh_dashboard` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `nodejs-lib` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `orchestrator-service` | 2 | missing-test-case-summary ×1, columns ×1 |
| `paperclip` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `pg-data-service` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `platform-test-kit` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `py-permissions` | 2 | columns ×1, missing-test-case-summary ×1 |
| `pytest-sqlmodel` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `quire-wasm` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `reference-sdk` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `review-worker` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `scheduler-service` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `scheduler-view` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `secrets-injector-webhook` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `spec-artifacts-app` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `spec-artifacts-iso` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `spec-objects-architecture` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `spec-objects-enterprise` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `spec-objects-security` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `sqlmodel-fixtures` | 2 | traces-to-pattern ×1, columns ×1 |
| `sqlmodel-publisher` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `sync-cloudmanager` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `sync-core` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `sync-filament` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `sync-github` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `sync-local` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ts-auth-sdk` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ts-auth-ui` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ts-build-chain` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ts-observability` | 2 | columns ×1, other ×1 |
| `typescript-react-lib` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `typesetter` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ui-data-table` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ui-reference-component` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `ui-workflow-pane` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `user-admin-ui` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `web-app` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `workflow-app` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `workflow-plugin-sdk` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `workflow-worker-pool` | 2 | missing-fr-coverage ×1, missing-test-case-summary ×1 |
| `fastmcp-cookiecutter` | 1 | missing-fr-coverage ×1 |
| `filament-editor-repos` | 1 | traces-to-pattern ×1 |
| `glitchtip-mcp` | 1 | missing-test-case-summary ×1 |
| `ix-agent-extensions` | 1 | missing-test-case-summary ×1 |
| `ix-agent-flow` | 1 | missing-fr-coverage ×1 |
| `ix-agent-hitl` | 1 | missing-test-case-summary ×1 |
| `ix-agent-memory` | 1 | columns ×1 |
| `ix-agent-memory-service` | 1 | columns ×1 |
| `py-state-machine` | 1 | missing-test-case-summary ×1 |

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
  `Coverage Status` (10). No contract change reaches these; they need authoring.
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
