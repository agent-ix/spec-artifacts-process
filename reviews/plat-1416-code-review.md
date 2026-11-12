---
id: SR-20261102086821
title: "Code review of PLAT-1416 kind-typed Anomaly Target references (PR 141)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process PR141 @7d210ed over origin/main e4e1a21; spec_artifacts_process/manifest.yaml, tests/test_anomaly.py, pyproject.toml, poetry.lock"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-015"
    type: references
---
# SR-20261102086821: Code review of PLAT-1416 kind-typed Anomaly Target references

## Summary

Ticket: PLAT-1416. PR spec-artifacts-process#141 at `7d210ed`, scoped to
`git diff origin/main...HEAD`. The PR adds `kind_column: Kind` and `kind_targets` to the
`anomaly-assessment` document reference, removes the strict xfail on the FR-015-AC-6 test,
and points the remaining two strict xfails at quire-rs PLAT-1476.

What was measured, with quire 0.41.0 (engine 0.57.0) from PATH:

- The mapping `Requirement -> [requirement-document, nfr-document, acceptance-criterion,
  nfr-acceptance-criterion]` and `Hazard -> [hazard-document]` matches the FR-015 Behavior
  vocabulary (`Requirement | Hazard | None`). Every listed target is in `targets`, so
  FR-049-AC-15 module-load checks pass. `None` rows carry `-`, which matches no pattern and
  yields no reference (FR-049-AC-14), and an unlisted kind falls back to the union
  (FR-049-AC-13). No `Acceptance criterion` key is needed, because FR-015 has no such kind.
- Both FR-015-AC-6 cases pass, and each yields one `[reference-kind-mismatch]` line.
- The three FR-015-AC-5 dangling cases still pass, with one `[dangling-trace-reference]`
  each and no accompanying kind mismatch.
- Mutation: with the four kind lines removed from the manifest, both AC-6 cases fail.
  Everything else stays the same.
- The two remaining xfails are `strict=True` and still xfail. Fixture (c) now produces all
  three defects, two of them as bundle findings with no line, so its reason is true.
  PLAT-1476 covers both the bundle-finding lines and the record-validation lines and their
  quoin FR-073 wiring.
- Baseline and PR runs of `tests/test_semantic_manifest.py` and
  `tests/test_skeletons_and_roles.py` give the same 19 failures. The cause is the stale
  user-site quire wheel 0.53.0, which is an environment fault and not a finding.

## Verdict

**FAIL (one high).** The manifest change is correct and its test discriminates. The repo's
declared Python engine rejects the new manifest key, though: `quire = "^0.55.0"` and the lock
at 0.55.0 resolve below 0.57.0. Every engine below quire-rs 0.57.0 (quire CLI 0.41.0) refuses
the whole module, not only the Anomaly declaration.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | `DocumentReference` is `#[serde(deny_unknown_fields)]` in every quire-rs release before v0.57.0, and `kind_column` first appears in v0.57.0 (f608780). The repo's declared engine is `quire = "^0.55.0"` (Poetry caret on 0.x means >=0.55.0,<0.56.0), and `poetry.lock` holds 0.55.0. That engine rejects the manifest, so `Registry.load_from(REPO_ROOT)` fails in the locked environment. The installed 0.53 wheel already fails the same way on an earlier unknown field, which shows the wheel parses `traceability` strictly. A consumer on quire CLI 0.40.0 (engine 0.56.0) also fails to load the whole module. Fix: raise the constraint to `^0.57.0` and relock. If internal-pypi lacks the wheel, use a git or path dependency on quire-rs. | pyproject.toml:39; poetry.lock:934-935; spec_artifacts_process/manifest.yaml:1140-1143 |
| FND-002 | low | The AC-6 test filters on the substrings `mismatch`, the target and the kind word, not on the engine's finding code. Its sibling test uses the `reference_findings(result, kind)` helper with `[dangling-trace-reference]`. Using `reference_findings(result, "reference-kind-mismatch")` plus `(row '<kind>')` would pin the exact code and row and match AC-5's test. | tests/test_anomaly.py:456-466 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | medium | The repo provisions its own quire CLI through `spec_artifacts_process/semantic/package.json` (`"@agent-ix/quire-cli": "0.38.2"`), and `pytest_sessionstart` in `tests/conftest.py` puts `semantic/node_modules/.bin` first on PATH. After `make semantic-install`, every CLI-driven test therefore runs quire 0.38.2. That version rejects the manifest (`unknown field 'from'`, l.863, already the case on main), and it predates `kind_column`. Measured on this head with the repo's own provisioning: 23 failed, 44 passed and 3 xfailed in tests/test_anomaly.py. This contradicts the floor the PR just wrote into FR-015 (quire CLI >= 0.41.0). Fix: bump the devDependency to 0.41.0, which is published on npmjs, and update package-lock.json. | spec_artifacts_process/semantic/package.json:17; tests/conftest.py:58-62 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | 9c1de24: pyproject `quire = { version = "^0.57.0", source = "internal-pypi" }`; poetry.lock moves quire 0.55.0 -> 0.57.0 (five wheel entries + content-hash only, no other package churn). `poetry install` from internal-pypi resolves quire 0.57.0 and `Registry.load_from` accepts the manifest. |
| FND-002 | fixed | 9c1de24: AC-6 test now uses `reference_findings(..., "reference-kind-mismatch")`, asserts exactly one, the id and `(row '<kind>')`. |
