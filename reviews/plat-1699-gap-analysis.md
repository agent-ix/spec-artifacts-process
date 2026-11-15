---
id: SR-20261115084902
title: "PLAT-1699 PR154 gap-analysis"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process PR154 @62ba871; changed behavior in spec_artifacts_process/manifest.yaml and tests/test_semantic_manifest.py against FR-010-AC-10"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/FR-010", type: references}
---

## Summary

Ticket: PLAT-1699. Scoped gap analysis of the changed relationship registry behavior. The manifest now contains all 12 distinct `allowed_links` verbs, and the new test's set-inclusion assertion provides direct evidence for FR-010-AC-10. Quoin 0.34.0 computes FR-010-AC-10 as `tagged`, bound to `test_every_allowed_link_verb_is_registered`. It also reports an `unbacked_claims` diagnostic at the docstring's plain `Trace: TC-152, FR-010-AC-10` line: the pytest decorator already carries both tags, so the redundant docstring line should be removed. The Quire smoke check also needs to assert a successful exit code before accepting the absence of `UnknownEdgeType` text.

## Verdict

**CONDITIONAL.** The acceptance criterion is tagged and its registry-completeness assertion aligns with the requirement. The matrix's unbacked trace claim and the unchecked Quire command status leave avoidable noise and a false-pass path in the integration evidence.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The redundant unmarked `Trace:` line in the test docstring produces an `unbacked_claims` diagnostic even though the pytest decorator already tags the criterion. | tests/test_semantic_manifest.py:57-62 |
| FND-002 | medium | The Quire smoke test can pass after a failed validation command because it does not assert a successful exit status before checking for warnings. | tests/test_semantic_manifest.py:71-78 |

## Coverage

- FR-010-AC-10: tagged by `test_every_allowed_link_verb_is_registered`; registry completeness assertion matches the requirement.
- Quire FR-040-AC-3: checked as context for the expected advisory `UnknownEdgeType` warning.
- Reverse gaps, other criteria, and unrelated repository behavior: not assessed in this PR-scoped review.
- Plan completion: not assessed

## Examined scope

```yaml
scope:
  - {id: FR-010-AC-10, path: "spec/functional/FR-010-semantic-manifest-contract.md", role: examined, excerpt: "Every verb key in every artifact type's `allowed_links` is present in this module's top-level `edge_types` registry."}
  - {id: TC-152, path: "spec/tests.md", role: examined, excerpt: "| TC-152 | Every artifact type's `allowed_links` verb is registered in this module's `edge_types`, and Quire reports no `UnknownEdgeType` warnings for the module | Integration | P1 | FR-010-AC-10 | ✅ |"}
  - {id: FR-040-AC-3, path: "quire-rs/spec/functional/FR-040-object-edge-vocabulary.md", role: context_only, excerpt: "An `allowed_links` key absent from `edge_types`, or a `roles:` entry / target token absent from `roles`, emits a non-fatal `UnknownEdgeType`/`UnknownRole` diagnostic (advisory, default load succeeds); the opt-in `load_strict` path escalates AC-2 and AC-3 diagnostics to errors."}
```

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Commit 85b22fd removed the redundant unmarked trace line; the criterion remains tagged by the pytest decorator. |
| FND-002 | fixed | Commit 85b22fd now asserts successful Quire validation before checking diagnostics. |

after_excerpt FND-001: `    """Each allowed relationship verb has a local edge-type registration."""`

after_excerpt FND-002: `    assert result.returncode == 0, result.stderr`
