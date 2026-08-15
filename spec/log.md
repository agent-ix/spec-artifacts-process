---
type: log
title: "Update Log"
description: "Chronological log of structural changes to this bundle."
---
# Update Log

## History

* **2026-06-15** — Adopted OKF-compatible bundle structure with directory indexes.
* **2026-08-04** — Added `usecase/` (US-001) and FR-003 (TestMatrix `body_extraction`); restructured `tests.md` to the spec-matrix table shape.
* **2026-08-04** — FR-003 refined per review: `Priority` `column_choices` (P0–P4 vocabulary), widened `Traces To` tokens (CON rows, IT ids/success criteria), normalize-before-enforce rollout constraint (FR-003-CON-1).
* **2026-08-04** — Base spec review recorded (`reviews/base.md`, SR-001): fixed stale contribution counts in `spec.md` and marked US-001's open question resolved by FR-003; FR-003 matrix coverage and FR-002 coverage gaps left open.
* **2026-08-04** — Test Matrix completed for FR-003 per the six coverage rules: TC-001..TC-018 (vocabulary permutations, `min_rows`/table-presence boundaries, Test ID / Traces To / Status / Priority error paths), per-AC coverage rows, US-001 coverage, option-permutation/constraint-boundary/edge-case/gap sections (resolves SR-001 FND-001).
* **2026-08-04** — TDD plan bundle authored for FR-003 (`plan/Plan-001-testmatrix-body-extraction/`): 6 tasks, tracks A/S/Gate/C, FR-003-CON-1 modeled as a hard sign-off gate before the enforcing publish; no quire-rs engine work in scope.
* **2026-08-04** — All open SR-001 findings resolved (user-authorized, incl. pre-existing artifacts): FR-002 matrix coverage added (TC-019..TC-023, closes FND-002/GAP-001); StR-001 contribution counts corrected to 6 archetypes / 9 artifact types (FND-005); FR-003-AC-11 added for Test ID uniqueness with the missing quire-rs uniqueness assert recorded as an external dependency (GAP-002, TC-024 blocked).
* **2026-08-15** — Added FR-005 declaring the Task `track` property (optional string, no enum) with TC-037/TC-038; 230 task files across the ecosystem carried the key through `additionalProperties: true` and nothing checked it. The competing nodal `Track` archetype (PR #9) is closed unmerged per filament-ide-rs SR-074 / #232 — a track is a Task property and the tree node is synthesized by the consumer (CR-026).
