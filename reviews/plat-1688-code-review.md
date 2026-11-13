---
id: SR-20261113192026
title: "PLAT-1688 spec-artifacts-process PR151 code-review"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR151 @637685d over origin/main; spec_artifacts_process/manifest.yaml, pyproject.toml, poetry.lock, spec/functional/FR-017-adr-design-realization-verb.md, spec/functional/FR-007-verification-method-catalog.md, spec/tests.md, tests/test_adr_links.py, tests/test_criticality_field.py, tests/fixtures/design_edges/**, tests/fixtures/criticality/**"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-017"
    type: references
  - target: "ix://agent-ix/spec-artifacts-process/FR-007"
    type: references
---

## Summary

Ticket: PLAT-1688 (also the spec-artifacts-process part of PLAT-1597). Code review, with the Python test lane folded in, of two manifest changes. First, the `ADR` `allowed_links` becomes a map, with `realizes_requirement: [FR, NFR]` and `"*"` for the four older verbs. Second, `criticality_field: criticality` is added to the `acceptance-criterion` and `nfr-acceptance-criterion` obligation sources.

Measured with quire-cli 0.45.0 (engine 0.60.0), installed in a scratch prefix, and the quire 0.60.0 wheel from the PR lock. Sibling modules are origin/main of spec-objects-architecture (a26a778) and spec-artifacts-iso (d83c1ce), loaded through `IX_FILAMENT_MODULES_PATH`. The two test files pass (11 passed). `quire validate` of FR-017, FR-007 and spec/tests.md exits 0. The lock diff changes only the `quire` entry and `content-hash`.

Mutations: removing either or both `criticality_field` lines fails both criticality tests. Setting `realizes_requirement` to `["*"]` fails TC-221 and TC-223, and removing the verb fails three tests. Setting it to `[FR]` or `[part]` fails only the static TC-221. The behavioural test TC-222 still passes, and the cause is FND-001.

The criticality key is on the right sources. It sits on the two criterion sources whose archetypes (FR, NFR) carry a `criticality` frontmatter field. It is not on `interface-acceptance-criterion`, whose archetype carries no such field. The ticket's remaining-work comment names the spec-artifacts-iso manifest, but the obligation sources are declared in this module, so this is the right place. No standard is named, nothing is vendored, and no pin or digest ceremony is added.

## Verdict

**CHANGES REQUESTED.** The criticality change is correct and its tests fail without the key. The ADR change meets ticket AC 1 (the verb is listed toward FR and NFR) and AC 3 (relations report the realizing ADR, through `relations --json`, because `relations --design` does not exist in quire-cli 0.45.0). It does not meet ticket AC 2's wrong-kind half. A wrong-kind target is detected only when the target is an object type such as a part. An ADR realizing another ADR draws nothing (FND-001). Where it is detected, the finding is advisory: it stays a warning under `--strict`, does not change the exit status, and names the document id, not the file (FND-002). FR-017 was amended to call the finding "advisory", so the spec now records less than the ticket asks for, and no owner decision is recorded. An advisory finding is not enough for "fail validate with a located message". The dangling half of AC 2 is met: `--strict` fails with `dangling-reference` naming the ADR file and `FR-999`.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The `realizes_requirement: [FR, NFR]` target list is enforced only against object-type targets. ADR-002 realizing ADR-001 (an artifact-type document of the wrong kind) draws no `disallowed-edge-target`, even under `--okf --strict`. With the list set to `[part]` or `[FR]`, ADR-001 to FR-001 and ADR-002 to NFR-001 still draw no finding. FR-017's new SHALL, that an edge toward a document of another object type draws the finding, holds only for object types, and ticket AC 2's wrong-kind case is not met for artifact-type targets. The cause is probably in the engine's kind check (quire-rs). Fix: have the engine check artifact-type targets too, or narrow the SHALL and the ticket AC to object types with an owner decision. | spec_artifacts_process/manifest.yaml:75, spec/functional/FR-017-adr-design-realization-verb.md:35 |
| FND-002 | high | Ticket AC 2 says a wrong-kind target fails with a located message. `disallowed-edge-target` stays a `warning:` under `--strict` and is not counted in the exit status: the strict run of the invalid fixture reports `3 OKF bundle validation error(s)`, which are the two `dangling-reference` lines and one `unowned-quality-characteristic`, and the wrong-kind edge is not among them. The message is located by the document id (`ADR-004:`), not by the file path that `dangling-reference` carries. The FR-017 amendment recasts the ticket AC as "advisory" with no recorded decision. Fix: make the engine report the finding as an error under `--strict`, with the file path, or get the ticket owner to amend the AC. | spec/functional/FR-017-adr-design-realization-verb.md:35, spec/functional/FR-017-adr-design-realization-verb.md:51 |
| FND-003 | medium | The new tests resolve spec-objects-architecture and spec-artifacts-iso from the ambient `~/.ix/filament/modules` store, and `quire` from `PATH`. Neither is a declared dependency. With this machine's installed module set, whose architecture module has no `realizes_requirement`, TC-225 fails (measured: 1 failed, 10 passed). With the installed quire 0.44.0, the new manifest keys are rejected. Fix: resolve module directories from declared dev dependencies (spec-artifacts-iso already is one; add spec-objects-architecture), or have `make test` set the path explicitly. | tests/test_adr_links.py:69, tests/test_criticality_field.py:15 |
| FND-004 | low | The `IX_FILAMENT_MODULES_PATH` / `~/.ix/filament/modules` resolution is duplicated in both new test files. Move it to `conftest.py`. | tests/test_adr_links.py:69, tests/test_criticality_field.py:15 |
| FND-005 | low | FR-017's `## Outputs` still reads only "`realizes_requirement` in the `ADR` `allowed_links`". It does not mention the `FR`/`NFR` target list or the `"*"` targets that the amended Behavior now requires. | spec/functional/FR-017-adr-design-realization-verb.md:26 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-006 | high | The repository's declared quire CLI is still `@agent-ix/quire-cli` 0.43.0 (spec_artifacts_process/semantic/package.json and its lock). `pytest_sessionstart` puts `semantic/node_modules/.bin` first on PATH whenever `make semantic-install` has run, and `make lint` needs that install for `schemas-check`. quire-cli 0.43.0 rejects this manifest (`traceability.obligations[0]: unknown field criticality_field`), and the iso module's `carried_fields` with it. Measured with 0.43.0 first on PATH: 6 of the 11 rows fail, including the existing TC-218 and TC-219, so every CLI-backed row in the suite is expected to fail too. `QUIRE_CLI_REQUIRED = "0.45.0"` appears only in the `shutil.which` failure message, so a 0.43.0 on PATH passes that check. Fix: bump `@agent-ix/quire-cli` to 0.45.0 in semantic/package.json and its lock, and drop the unchecked constant. | spec_artifacts_process/semantic/package.json:17, tests/conftest.py:60, tests/conftest.py:77 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | deferred | Engine limitation, deferred to PLAT-1689 (quire-rs) by the coordinator's ruling. The FR-017 SHALL at fd3cd8b now says honestly that only targets which declare an object type are checked, and that an `ADR` target is not, citing PLAT-1689. |
| FND-002 | deferred | Deferred to PLAT-1689 by the coordinator's ruling. FR-017-AC-7 and TC-223 now say the finding is an advisory warning that leaves the exit status unchanged, and the test pins the `warning:` prefix. The spec no longer claims a failure. Ticket AC 2's wrong-kind half moves to PLAT-1689. |
| FND-003 | still-open | fd3cd8b moves the lookup to conftest and improves the failure messages, but the sibling modules still come from the ambient store, and the CLI from PATH. Measured at fd3cd8b with the default `IX_FILAMENT_MODULES_PATH`: TC-225 fails (1 failed, 10 passed). The CLI the repository does declare is 0.43.0 (FND-006). |
| FND-004 | fixed | `MODULES_ROOT`, `ix_module` and `run_quire` live once in tests/conftest.py, and both test files import `run_quire`. |
| FND-005 | fixed | Outputs now reads: "`realizes_requirement` in the `ADR` `allowed_links` with the target list `FR`, `NFR`, and the four earlier verbs ... each with the target `\"*\"`." |
