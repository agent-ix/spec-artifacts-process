---
id: rubric-example
version: 1
type: Rubric
---
<!-- Rubric authoring skeleton (spec-artifacts-process, FR-023).

     One rubric per document, at `spec/rubrics/<rubric>.md`, inside the spec
     root so `quire matrix` reads it, apart from `spec/roles/`.

     Contract (manifest body_extraction asserts, validated by `quire validate`):
     - Frontmatter: `type: Rubric`; `id` is a lower-case slug starting with
       `rubric-`; `version` is an integer >= 1.
     - REQUIRED (level 2): Checks, a table with >= 1 row and headers EXACTLY
       ID | Check | Scale.
     - `ID` is `<id>@<version>#<check-slug>` with the frontmatter id and
       version, and a lower-case hyphenated slug. A version bump therefore
       renumbers every check, and a role spec still citing the old version
       dangles. -->

# Rubric: example

## Checks

| ID | Check | Scale |
|----|-------|-------|
| rubric-example@1#example-check | Whether the behavior under judgement occurred. | 0 absent, 1 partial, 2 present |
