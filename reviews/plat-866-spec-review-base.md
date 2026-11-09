---
id: SR-20261102086809
title: "Base review of PLAT-866 structural Python and TypeScript implements forms"
type: SpecReview
analysis: base
scope: "agent-ix/spec-artifacts-process PR133 @c50b1ee over origin/main; spec/functional/FR-004-traceability-declaration.md, spec/tests.md"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-004"
    type: references
---

## Summary

Ticket: PLAT-866. Base checklist review of PR #133. It is a spec-only change.
It adds FR-004-AC-31..35 and TC-160..164, rewrites FR-004-AC-10 and
FR-004-AC-26, and retitles TC-155. Scope is `git diff origin/main...HEAD`. The
review compared it with the sibling quire-rs#628 FR-062 section, with
ix-trace-py#4 and ix-trace-ts#8, and with the open spec-artifacts-process#132.

The `syntax` values match quire-rs#628 exactly: `python_decorator`,
`typescript_decorator` and `typescript_wrapper`. FR-004 keeps `implements`
separate from `markers`, so it does not contradict FR-062's load rules (a form
in the wrong language, outside `implements`, or in `markers` is rejected).
FR-062 owns those rules and FR-004 does not need to repeat them. No new id
collides with main or with any open PR (#132, #123, #58). There is no
public-repo leak: no roadmap, no delivery order beyond this repo's own
sequencing, and no private research.

The two rewritten criteria are the problem. AC-10 and AC-26 now describe a
manifest that does not exist yet. Their matrix rows still say ✅ Complete, and
they are bound to tests that assert the opposite.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The rewritten FR-004-AC-10 requires "no Python or TypeScript line-comment form". The manifest today declares `python-implements-line` and `typescript-implements-line`. The bound test TC-066 asserts `len(forms) == 4` and that each language's only form is `<language>-implements-line`. The TC-066 row title still says it "retains exactly one templated comment form each for Python and TypeScript". The coverage row still says `✅ Complete`. The spec now claims a verified state that both the manifest and the test contradict. Scope AC-10 as a target and mark its coverage row `🚧 Planned`, or keep the current AC-10 and carry the end state only in a new Planned AC. Retitle TC-066 to match whichever AC-10 stands. | spec/functional/FR-004-traceability-declaration.md:199; spec/tests.md:54; spec/tests.md:226; tests/test_traceability_declaration.py:385-410; spec_artifacts_process/manifest.yaml:1137-1144 |
| FND-002 | high | FR-004-AC-26 and the TC-155 title were moved to "the Rust line-comment form", but the test bound to them, `test_comment_implements_forms_match_language_syntax` (`@pytest.mark.trace("TC-155", "FR-004-AC-26")`), loops only over `("python", "# "), ("typescript", "// ")`. It never loads `rust-implements-line`. The `✅` on TC-155 and `✅ Complete` on the AC-26 coverage row are therefore false: no test exercises what AC-26 now says. The binding is wrong (a trace defect). The follow-up code ticket will delete the Python and TypeScript forms this test asserts, so it cannot keep that binding. Mark AC-26 and TC-155 `🚧 Planned` until a Rust-form test carries the tag. Alternatively, re-point the tag in this PR to the Rust prose-guard assertions already in TC-066 (lines 409-410). | spec/functional/FR-004-traceability-declaration.md:209; spec/tests.md:63; spec/tests.md:290; tests/test_traceability_declaration.py:413-444 |
| FND-003 | medium | FR-004-AC-31 and AC-32 judge each form only by whether its pattern captures ids from sample text, through TC-160 and TC-161, which are Unit tests. quire-rs#628 FR-062 applies the pattern to the whole candidate node: the full decorator including `@`, or the inner wrapper call. A pattern that matches only a proper substring yields `partial-implements-syntax-match` and no relation (FR-062-AC-25). An unanchored pattern such as `implements\((...)\)` would pass AC-31 and AC-32. Under the engine it would bind nothing for `@ix_trace_py.implements("X")`. AC-33's integration fixture does not require a qualified spelling, so it would not catch the gap either. Require each pattern to match the entire candidate for every spelling AC-31 and AC-32 list, and include a qualified spelling in AC-33. | spec/functional/FR-004-traceability-declaration.md:214-216 |
| FND-004 | medium | FR-004-AC-32 requires capture "with and without the `ixTrace.` namespace qualifier". ix-trace-ts#8 defines no namespace or alias. A namespace-import name is chosen by the author (`import * as anything`), so a pattern fixed to `ixTrace.` covers one arbitrary spelling. An implementer could equally read "package-qualified" as any identifier prefix. Python has the same issue in milder form: `ix_trace_py.` is canonical, but `import ix_trace_py as t` is not covered. State which qualified spellings bind. Either name a closed set and say it is a convention, or admit any `<identifier>.` prefix. | spec/functional/FR-004-traceability-declaration.md:215; spec/functional/FR-004-traceability-declaration.md:152-163 |
| FND-005 | low | FR-004-AC-10 requires each structural form to be "templated" but does not fix the template text or the order of the two TypeScript forms. quire-rs#628 FR-062-AC-26 renders the FR-051 advisory from "the first structural `implements` form of that file's language that declares a `template`", and expects `@implements("…")` and `@implementing("…")`. If `typescript_wrapper` is declared first, the advisory names `implementing(...)` in its place. Pin the templates (`@implements({ids})`, `@implementing({ids})`, `implementing({ids})`) and declare `typescript_decorator` before `typescript_wrapper`. | spec/functional/FR-004-traceability-declaration.md:199 |

## Detail

AC-to-TC audit for the criteria this PR adds or changes:

| AC | TC | TC defined in Test Case Summary | Coverage row | Can fail |
| --- | --- | --- | --- | --- |
| FR-004-AC-10 | TC-066 | yes (title contradicts AC) | ✅ (false, FND-001) | yes |
| FR-004-AC-26 | TC-155 | yes (test exercises other forms) | ✅ (false, FND-002) | yes |
| FR-004-AC-31 | TC-160 | no, misplaced (integrity SR FND-001) | 🚧 | yes |
| FR-004-AC-32 | TC-161 | no, misplaced | 🚧 | yes |
| FR-004-AC-33 | TC-162 | no, misplaced | 🚧 | yes |
| FR-004-AC-34 | TC-163 | no, misplaced | 🚧 | yes |
| FR-004-AC-35 | TC-164 | no, misplaced | 🚧 | yes |

Every new AC has a TC id and can fail. AC-34 and AC-35 are clear about what
must not bind. The table is complete for the changed set. Its one structural
defect, that the TC rows are never minted, is recorded in the integrity
review.

Collisions: `git grep` on origin/main finds no `FR-004-AC-3[1-9]` and no
`TC-16[0-9]`. None of the open PRs #132, #123 or #58 adds either. A trial merge
of #132 into this head conflicts textually in FR-004. Both PRs edit the
`markers`/`implements` bullets and the AC-3/AC-10 table rows. The conflict is
trivial to resolve by keeping both, and it is not a defect of this PR.

## Verdict

**NOT MERGEABLE.** FND-001 and FND-002 mark a planned manifest state as
verified. Fix those and the integrity SR's FND-001, then re-review. FND-003 and
FND-004 should be fixed in the same round because the follow-up code ticket
will implement them literally.

## Examined scope

```yaml
scope:
- {id: FR-004-AC-10, path: spec/functional/FR-004-traceability-declaration.md, role: examined}
- {id: FR-004-AC-26, path: spec/functional/FR-004-traceability-declaration.md, role: examined}
- {id: FR-004-AC-31, path: spec/functional/FR-004-traceability-declaration.md, role: examined}
- {id: FR-004-AC-32, path: spec/functional/FR-004-traceability-declaration.md, role: examined}
- {id: FR-004-AC-33, path: spec/functional/FR-004-traceability-declaration.md, role: examined}
- {id: FR-004-AC-34, path: spec/functional/FR-004-traceability-declaration.md, role: examined}
- {id: FR-004-AC-35, path: spec/functional/FR-004-traceability-declaration.md, role: examined}
- {id: FR-004, path: spec/functional/FR-004-traceability-declaration.md, role: examined}
- {id: TC-066, path: spec/tests.md, role: examined}
- {id: TC-155, path: spec/tests.md, role: examined}
- {id: FR-062, path: "agent-ix/quire-rs#628 spec/functional/FR-062-implements-relation.md", role: context_only}
```
