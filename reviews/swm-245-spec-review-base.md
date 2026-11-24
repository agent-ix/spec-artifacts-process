---
id: SR-20261115175476
title: "SWM-245 PR164 spec-review base"
type: SpecReview
analysis: base
scope: "agent-ix/spec-artifacts-process PR164; spec/usecase/US-004-author-role-specs-that-validate.md, spec/functional/FR-020-rolespec-archetype.md, spec/functional/FR-021-rolespec-trace-and-cross-row-checks.md, spec/functional/FR-022-rolespec-lint-ownership.md, spec/functional/index.md, spec/usecase/index.md"
review_set: base
relationships:
  - {target: "ix://agent-ix/spec-artifacts-process/US-004", type: references}
  - {target: "ix://agent-ix/spec-artifacts-process/FR-020", type: references}
  - {target: "ix://agent-ix/spec-artifacts-process/FR-021", type: references}
  - {target: "ix://agent-ix/spec-artifacts-process/FR-022", type: references}
---

## Summary

Ticket: SWM-245. Base spec review of PR164 (head b5f09a1), scoped to `git diff origin/main...HEAD`. The PR adds US-004 and FR-020 to FR-022, which specify a `RoleSpec` archetype for dev-team role specs.

Sources of intent: dev-team origin/main FR-006, FR-007, FR-008 and `docs/examples/minder-role-spec.md`, the SWM-245 checklist, and six lead decisions on the author's open questions:

1. Rubrics are a `Rubric` archetype in this module, with version in frontmatter and check slugs minted as trace targets. A `<rubric>@<version>#<slug>` reference resolves through the existing document-reference and dangling-reference machinery.
2. Quoin owns the version-bump and skill-citation checks.
3. The role prefix is 2 to 6 letters.
4. The allowed links are `satisfies`, `depends_on` and `implements`.
5. dev-team installs this module to validate its `spec/roles/`.
6. The engine gaps are SWM-247 and SWM-248, and must be linked from FR-021.

How each SWM-245 checklist item is covered:

- Frontmatter, the four tables, and the Trigger, Evaluator and threshold columns: covered by FR-020.
- Trace targets, with the Rule column bound: covered by FR-021. Rule parenting depends on SWM-247.
- Asserts (enums, prefix, objective names a metric, rule has an evaluation, unused metric): covered by FR-020 and FR-021, with the engine gaps listed.
- Versioned rubric refs resolve: **not covered**. See FND-001.
- Lint-side checks: assigned to Quoin by FR-022, which matches decision 2. The Quoin ticket is not filed (see the dependency review).
- Moving the minder example and validating it with exit 0: covered by FR-022-AC-1 and AC-4.

FR-020 matches decision 3: the prefix is 2 to 6 upper-case letters. `quire validate` on the four new documents exits with warnings only. Those warnings are recorded in the EARS review.

## Verdict

**CHANGES REQUIRED.** The archetype shape, enums and trace-target design follow dev-team FR-006 and FR-007 closely. Two problems remain:

- The rubric-resolution item of the checklist is left as an open question, which contradicts lead decision 1.
- The `RoleSpec` allowed links are not specified (decision 4).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | Versioned rubric references are not specified to resolve. FR-021 calls resolution an open question and engine capability 5, reported `unbound`. Lead decision 1 requires a `Rubric` archetype in this module, with `version` in frontmatter and check slugs minted as trace targets, so that `<rubric>@<version>#<slug>` resolves through the existing document-reference and dangling-reference machinery. No FR specifies that archetype, so the SWM-245 checklist item "Versioned rubric refs resolve" is uncovered. Capability 5 and FR-021-AC-10 need to be rewritten against the `Rubric` target. | spec/functional/FR-021-rolespec-trace-and-cross-row-checks.md:40,48,63 |
| FND-002 | medium | FR-020 does not state `allowed_links` for `RoleSpec`. Every archetype in `manifest.yaml` declares them, and lead decision 4 fixes them as `satisfies`, `depends_on` and `implements`. The worked minder spec carries `satisfies` to dev-team FR-006. With the set unstated, the implementer must guess it and no AC checks it. | spec/functional/FR-020-rolespec-archetype.md:27,33 |
| FND-003 | medium | "Query reference" is never defined. A deterministic evaluation needs "a query reference, not a rubric reference", but no shape is given. dev-team FR-006 also requires `Trigger` to be a deterministic query reference, while FR-020 requires only that it is non-empty. FR-020-AC-3 therefore cannot distinguish a query reference from free text, and a prose Trigger validates. | spec/functional/FR-020-rolespec-archetype.md:43,45 |
| FND-004 | low | The metric-query distinctness check also compares a metric's `Query` with every evaluation `Trigger`. dev-team FR-006 forbids only equality with an evaluation's query, because the rule would then be correlated with its own violation count. A trigger is not a violation count, so this goes beyond the stated intent, and FR-021-AC-6 does not test the Trigger half. | spec/functional/FR-021-rolespec-trace-and-cross-row-checks.md:38,59 |
| FND-005 | low | FR-020 requires exactly four tables but does not say whether other sections are allowed. The worked minder spec, which FR-022-AC-1 and AC-4 require to validate, has a `## Purpose` section. If extra sections are rejected, the acceptance fixture fails. | spec/functional/FR-020-rolespec-archetype.md:28,34 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1 (head 23335ff): the new FR-023 declares a `Rubric` archetype, with `version` in frontmatter and check ids `<id>@<version>#<slug>` minted by the `rubric-check` target. FR-021 resolves the reference through `dangling-trace-reference` (line 44), capability 5 is removed, and AC-10 is rewritten. |
| FND-002 | fixed | Round 1: FR-020 line 42 declares `allowed_links` of `satisfies`, `depends_on` and `implements`, and FR-020-AC-12 tests it. |
| FND-003 | fixed | Round 1: FR-020 line 53 defines a query reference as `<source>.<name>` with the pattern `^[a-z][a-z0-9-]*\.[a-z][a-z0-9_]*$`. Line 54 requires the metric `Query` and the evaluation `Trigger` to be query references, and AC-3 tests free text in both. |
| FND-004 | fixed | Round 1: FR-021 line 41 compares only `Query or rubric` and states why `Trigger` is excluded. AC-6 tests that a Trigger-only match validates. |
| FND-005 | fixed | Round 1: FR-020 line 43 accepts sections beyond the four tables, such as `Purpose`, and FR-020-AC-11 tests it. |
