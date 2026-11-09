---
id: SR-20261102086813
title: "PLAT-277 process PR134 gap-analysis"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-artifacts-process PR134 @9878e24 over origin/main 9fc6a8b; spec/functional/FR-010-semantic-manifest-contract.md, spec/tests.md, tests/test_semantic_manifest.py"
review_set: subset
---

## Summary

Ticket: PLAT-277. This is a planless gap analysis of the criteria the PR changed
or added, FR-010-AC-8 and FR-010-AC-10, against their tagged tests, TC-096 and
TC-167. Plan completion was not assessed. The touched test files pass:
`tests/test_semantic_manifest.py` and `tests/test_manifest.py` give 23 passed
and 1 xfailed. Both tests inspect the parsed `manifest.yaml` and never run the
engine.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-010-AC-8 and the FR-010 Behavior bullet make behavioural claims: a document is dispatched on `type:` to the artifact type and on `object:` to the object type, and "one without [`code:`] is refused". TC-096 asserts only the manifest's shape: no `data_schema`, and `code` marked `required: true`. No test validates a Standard document. Measured by hand: a corpus Standard passes, and the same file without `code:` is refused by both the `Standard` frontmatter schema and the `standard` locator. Add an engine-level test that validates a Standard with and without `code:` through `quire_engine`. | spec/functional/FR-010-semantic-manifest-contract.md:88; spec/functional/FR-010-semantic-manifest-contract.md:54-58; tests/test_semantic_manifest.py:112-128 |
| FND-002 | low | FR-010-AC-10 says loading the module "reports no `DuplicateArchetype`". TC-167 checks name uniqueness in the parsed YAML and never loads the module or reads the loader's diagnostics. Quire keys the registry by exact name, so the two checks agree today. An assertion on the loader's diagnostics would test the claim the AC makes. | spec/functional/FR-010-semantic-manifest-contract.md:89; tests/test_semantic_manifest.py:130-146 |

## Verdict

**CHANGES REQUESTED.** The coverage table maps both new criteria. FND-001 is a
real gap: the refusal that F2 relies on is asserted only through manifest
structure.

## Examined scope

```yaml
scope:
- {id: FR-010-AC-8, path: spec/functional/FR-010-semantic-manifest-contract.md, role: examined}
- {id: FR-010-AC-10, path: spec/functional/FR-010-semantic-manifest-contract.md, role: examined}
- {id: TC-096, path: spec/tests.md, role: examined}
- {id: TC-167, path: spec/tests.md, role: examined}
- {id: FR-010, path: spec/functional/FR-010-semantic-manifest-contract.md, role: context_only}
```
