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
