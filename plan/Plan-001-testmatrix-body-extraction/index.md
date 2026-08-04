---
type: index
title: "Plan-001 — TestMatrix body_extraction (FR-003)"
description: "Contents of the Plan-001 bundle."
okf_version: "0.1"
---
# Plan-001 — TestMatrix body_extraction (FR-003)

## Contents

* [Plan-001: TestMatrix body_extraction (FR-003)](./plan.md) - Plan overview, DAG, tracks, gates, test plan.
* [Task-001: Fixture corpus + failing validation tests (TDD red)](./tasks/Task-001-fixtures-and-red-tests.md) - Fixtures + red pytest harness for TC-001..TC-016, TC-018.
* [Task-002: TestMatrix body_extraction contract in manifest.yaml (TDD green)](./tasks/Task-002-manifest-body-extraction.md) - Manifest data change turning the suite green.
* [Task-003: Manifest-scope guard + repo self-validation](./tasks/Task-003-scope-guard-and-self-validation.md) - TC-017 (FR-003-AC-9), self-validation, packaging.
* [Task-004: Ecosystem tests.md sweep with per-repo diffs](./tasks/Task-004-ecosystem-tests-md-sweep.md) - Track S read-only sweep producing sign-off evidence.
* [Task-005: User sign-off gate (normalize-before-enforce)](./tasks/Task-005-normalize-before-enforce-signoff.md) - FR-003-CON-1 hard gate.
* [Task-006: Publish the enforcing module version](./tasks/Task-006-publish-enforcing-version.md) - Post-gate release + activation re-verification.
