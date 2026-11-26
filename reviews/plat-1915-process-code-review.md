---
id: SR-967175026302197768900474181941935084800
title: "Code review — SpecReview test coverage in spec-artifacts-process"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-artifacts-process; spec/tests.md, tests/test_manifest.py, tests/test_skeletons_and_roles.py, tests/test_specreview_validation.py"
review_set: subset
---

## Summary

Reviewed the new SpecReview validation oracles, the added criterion tags, and the matrix updates in PLAT-1915 PR #173. The behavior assertions and criterion traces are sound; TC-022's matrix type conflicts with the `integration` marker on its backing test.

## Verdict

**CONDITIONAL** — TC-022 needs a test-type mapping correction before the matrix accurately describes the test it marks complete.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | TC-022 is marked `Unit`, but its only binder is explicitly marked `pytest.mark.integration` and builds the wheel; classify the matrix row consistently with the test. | spec/tests.md:33; tests/test_skeletons_and_roles.py:149 |

## Review Notes

The new tests exercise the expected accept/reject boundaries for FR-002-AC-1..4. `test_task_schema_declares_track_property` already checks the schema validator against `track: C`, empty string, non-string, and null, so its new FR-005-AC-2 trace is supported. The TC-022 binder validates the source skeleton and confirms its packaged path exists in the built wheel. The AC-4 trace is correct.

Focused verification passed: the five selected pytest cases, Ruff, and Black.
