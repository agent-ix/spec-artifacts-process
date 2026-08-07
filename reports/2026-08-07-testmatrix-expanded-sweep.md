# TestMatrix expanded sweep — 2026-08-07

Scope: **every** failing TestMatrix in the ecosystem, including the `renamable`
and `missing-table` classes that an earlier pass wrongly set aside as an
"authoring backlog". Measurement is `scripts/testmatrix_sweep.py` against the
real engine (quire 0.16.0), worktree-deduped.

## Result

| | before | after |
|---|---|---|
| passing | 64 (37.9%) | **68 (40.2%)** |
| malformed | 15 | **9** |
| renamable | 34 | 36 |
| missing-table | 56 | 56 |

`renamable` rises by 2 because six documents left `malformed` and land in a
class named for the shape they now fail on, not for new breakage.

## What the contract change fixed

CR-018 made `Priority` an optional column (quire-rs CR-023, `optional_columns`).
49 of 169 matrices carry real test-case rows with no priority anywhere. The
alternative was to write an invented priority into each, which is fabricating
planning data to satisfy a checker.

Five repos that had already received a defaulted `P2` were corrected: the
invented column was removed from four (`code-block-renderer`,
`local-workspace-service`, `workflow-plugin-sdk`, `secrets-injector-webhook`);
`ts-auth-ui` kept its priorities because they were read from the document.

## What remains, and why converting it would be fabrication

The 101 still failing do not share one cause. Classified from primary
measurement:

| count | cause | what conversion would require |
|---|---|---|
| 31 | no test cases in the document at all | writing the test cases |
| 28 | no `Type` column | asserting how each case is verified |
| 17 | `Type` values that are not test types (`FR`, `Interaction`, `System`, `UI`) | reclassifying someone's evidence |
| 16 | no traces recorded | inventing traceability |
| 9 | per-document data errors (see below) | per-document judgement |

The first four classes are **authoring, not normalization**. Each would require
stating a claim the document does not make — precisely what a traceability
matrix exists to prevent.

## The 9 data errors — open questions

1. **`IT-`/`BENCH-`/`AUDIT-` ids in the Test Case Summary** (`quire-cli`,
   `ix-agent-terminal-control`). The contract's id pattern admits `TC-` only.
   `quire-cli` uses `IT-NNN` deliberately and its spec references those ids
   throughout; renaming them would break every trace. Either the id pattern
   admits declared evidence prefixes, or those repos rename ~100 ids.
   **Needs a decision — the plan said "normalize, do not widen".**
2. **Range ids** (`TC-001..TC-010`, `mcp-gateway-ui`) — one row standing for ten
   cases. Expanding invents ten titles; keeping fails the id pattern.
3. **Non-id traces** (`Future Task 13`, `Arch guard`, `**FR-001** (GitHub)`) —
   genuinely wrong data in 3 documents.
4. `py-permissions` carries a duplicate `Functional Requirement Coverage`
   heading; `orchestrator-service` an NFR coverage table with drifted columns.

## Landed this pass

`ix-agent-messaging-bridge`, `cloudmanager-local-sync`, `filament-view-editor`,
`scheduler-service` — restructured into the two asserted sections, every value
derived from the document, each verified with `quire.validate_document` before
the PR was opened (validate-or-revert; nothing was committed on the strength of
the converter alone).
