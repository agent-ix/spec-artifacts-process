# TestMatrix expanded sweep — 2026-08-07

Scope: **every** failing TestMatrix in the ecosystem, including the `renamable`
and `missing-table` classes that an earlier pass wrongly set aside as an
"authoring backlog". Measurement is `scripts/testmatrix_sweep.py` against the
real engine (quire 0.16.0), worktree-deduped.

## Result

| | before | after |
|---|---|---|
| passing | 64 (37.9%) | **70 (41.4%)** |
| malformed | 15 | **7** |
| renamable | 34 | 36 |
| missing-table | 56 | 56 |

`renamable` rises by 2 because documents left `malformed` and land in a class
named for the shape they now fail on, not for new breakage.

**`cell:Test ID` is now zero.** No document in the ecosystem fails on the id
pattern.

## What the contract change fixed

CR-018 made `Priority` an optional column (quire-rs CR-023, `optional_columns`).
49 of 169 matrices carry real test-case rows with no priority anywhere. The
alternative was to write an invented priority into each, which is fabricating
planning data to satisfy a checker.

Five repos that had already received a defaulted `P2` were corrected: the
invented column was removed from four (`code-block-renderer`,
`local-workspace-service`, `workflow-plugin-sdk`, `secrets-injector-webhook`);
`ts-auth-ui` kept its priorities because they were read from the document.

## What the second contract change fixed

CR-019 set the `Test ID` prefix set to `TC|IT`, mirroring the **declared
evidence archetypes** rather than enumerating kinds of testing.
`spec-artifacts-iso` mints exactly two test-id families — `TC-{next:03d}` and
`IT-{next:03d}` — so a contract admitting only `TC` contradicted a sibling
module. `quire-cli` alone carries 84 `IT-` ids referenced across seven of its
spec files.

The two axes stay separate, which is what keeps this from being an open-ended
widening: *what kind of testing* a row records is the `Type` column's job and
that vocabulary is open and module-extensible, while *what kind of artifact* an
id names is closed, one prefix per declared archetype. A new technique —
mutation, contract, chaos — is a new `Type` value and needs no new prefix.

The prefixes naming no archetype were renamed rather than admitted, because
each encoded in the id what its row already stated one column over:

| repo | was | now | `Type` |
|---|---|---|---|
| quire-cli | `UT-SU-1..3` | `TC-085..087` | Unit |
| quire-cli | `BENCH-001` | `TC-088` | Benchmark |
| quire-cli | `AUDIT-001..005` | `TC-089..093` | Static |
| chat-window | `SB-001..009` | `TC-101..109` | Integration |
| chat-window | `IS-001..004` | `TC-110..113` | Integration |

Eight quire-cli rows had also been authored with five cells instead of six,
leaving `Status` empty. Each was filled from the status the document itself
reports for that id in its own coverage tables; none was invented.

## What remains, and why converting it would be fabrication

The 101 still failing do not share one cause. Classified from primary
measurement:

| count | cause | what conversion would require |
|---|---|---|
| 31 | no test cases in the document at all | writing the test cases |
| 28 | no `Type` column | asserting how each case is verified |
| 16 | no traces recorded | inventing traceability |
| 17 | `Type` values that are not test types (`FR`, `Interaction`, `System`) | reclassifying someone's evidence |
| 7 | per-document data errors (see below) | per-document judgement |

The first four classes are **authoring, not normalization**. Each would require
stating a claim the document does not make — precisely what a traceability
matrix exists to prevent.

## The 9 data errors — open questions

1. ~~**`IT-`/`BENCH-`/`AUDIT-` ids in the Test Case Summary.**~~ **Resolved by
   CR-019** — see above. `IT` is admitted as a declared archetype; the rest
   were renamed.
2. **Range ids** (`TC-001..TC-010`, `mcp-gateway-ui`) — one row standing for ten
   cases. Expanding invents ten titles; keeping fails the id pattern.
3. **Non-id traces** (`Future Task 13`, `Arch guard`, `**FR-001** (GitHub)`) —
   genuinely wrong data in 3 documents.
4. `py-permissions` carries a duplicate `Functional Requirement Coverage`
   heading; `orchestrator-service` an NFR coverage table with drifted columns.

## Landed this pass

`ix-agent-messaging-bridge`, `cloudmanager-local-sync`, `filament-view-editor`,
`scheduler-service`, `code-block-editor`, `code-diff-editor`, `markdown-editor`
— restructured into the two asserted sections, every value
derived from the document, each verified with `quire.validate_document` before
the PR was opened (validate-or-revert; nothing was committed on the strength of
the converter alone).

## Judgement calls, stated so they are reviewable

Two `Type` mappings in this pass are readings of someone else's evidence rather
than renames, and are recorded here so they can be overturned:

- **`Story` / `Interact` → `Integration`** (chat-window). Storybook stories and
  interaction scripts execute the real component in a browser runtime, which is
  what `Integration` names in the declared vocabulary.
- **`Stress` → `Benchmark`** (chat-window, one row against a scalability NFR).
  `Benchmark` is the vocabulary's term for evidence measured against a
  threshold.

## Shipped

quire-rs **v0.16.0** + wheels (CR-023 `optional_columns`) · quire-cli **v0.10.0**
· spec-artifacts-process **v0.8.0** then **v0.9.0** (PyPI) · quoin **v0.8.0**
then **v0.9.0** (npm), each with the `default-modules.yaml` pin moved — a
published module reaches nobody until that pin moves.
