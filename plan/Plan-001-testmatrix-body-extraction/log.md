---
type: log
title: "Plan-001 — Update Log"
description: "Chronological log of changes to the Plan-001 bundle."
---
# Plan-001 — Update Log

## History

* **2026-08-04** — Plan created from spec; scoped to StR-001, US-001, FR-003. Decomposed into 6 tasks across tracks A (fixtures → manifest contract → AC-9 guard), S (ecosystem tests.md sweep), Gate (FR-003-CON-1 user sign-off), and C (enforcing publish), with the "contract green" quality gate after Track A. No quire-rs engine work in scope.
* **2026-08-04** — Recorded external quire-rs dependency for FR-003-AC-11 (Test ID uniqueness): no uniqueness assert exists in the engine (`LocatorAssert`/`assert_eval` verified); TC-024 blocked, enforcement excluded from this plan.
* **2026-08-04** — Track A complete (branch `task/testmatrix-body-extraction`):
  Task-001 built the 28-fixture corpus and the `quire validate` harness (red:
  20 failures), Task-002 landed the `TestMatrix` `body_extraction` contract in
  the manifest (all green in one step), Task-003 added the TC-017 scope guard
  plus repo self-validation. Gate "contract green" passed; `spec/tests.md`
  marks TC-001..TC-018 ✅ and FR-003-AC-11/TC-024 ⚠️ blocked on the absent
  quire-rs uniqueness assert. **Nothing published** — Task-004's sweep and the
  Task-005 sign-off gate (FR-003-CON-1) are untouched.
* **2026-08-04** — Task-004 (Track S) completed, read-only: swept 189 ecosystem
  `spec/tests.md` files against the candidate contract — 6 pass, 171 fail, 12
  are not TestMatrix documents. Report + per-repo diagnostics in
  `reports/2026-08-04-tests-md-sweep.{md,json}`. The sweep surfaced contract
  questions (Type/Status/Traces To vocabularies vs. real corpus usage) that the
  Task-005 gate must settle before any normalization. No repository was
  modified; nothing published.

