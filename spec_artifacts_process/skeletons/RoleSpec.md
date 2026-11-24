---
id: ROLE
role: role-name
version: 1
type: RoleSpec
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
---
<!-- RoleSpec authoring skeleton (spec-artifacts-process, FR-020).

     One role per document, at `spec/roles/<role>.md`, inside the spec root so
     `quire matrix` reads it.

     Contract (manifest body_extraction asserts, validated by `quire validate`):
     - Frontmatter: `type: RoleSpec`; `id` is the role's rule prefix, 2 to 6
       upper-case letters; `role` is the role name; `version` is an integer >= 1.
       Quoin's version-bump and skill-citation checks read `version` (FR-022).
     - Allowed relationship verbs: satisfies, depends_on.
     - REQUIRED (level 2), each a table with >= 1 row and these exact headers:
       Metrics:     ID | Name | Evidence source | Query | Unit | Target | Direction
       Objectives:  ID | Objective | Metrics
       Rules:       ID | Rule | Objective | Class | Source
       Evaluations: ID | Rule | Evidence source | Trigger | Method | Query or rubric | Evaluator | Comparator | Value | Unit | Cadence
     - Other sections (such as Purpose) are allowed and asserted by nothing.
     - Ids: <id>-M01, <id>-O01, <id>-R01, <id>-R01-E1.
     - Evidence source: ledger | relay-receipts | hook-events | linear | github | transcript | ix-board-metric.
     - Direction: higher | lower. Method: deterministic | judgement.
     - Cadence: tick | session-end | 3h | daily | weekly. Comparator: < | <= | = | >= | >.
     - Query and Trigger are query references `<source>.<name>`.
     - deterministic: Evaluator `evaluator`, Query or rubric a query reference.
     - judgement: Evaluator `director` or `team-retro`, Query or rubric
       `<rubric>@<version>#<check-slug>`, cadence not `tick`.
     - Every objective names a metric, every rule an objective, every evaluation
       a rule; an undefined id is a `dangling-trace-reference`. -->

# Role spec: role-name

## Purpose

What the role is for.

## Metrics

| ID | Name | Evidence source | Query | Unit | Target | Direction |
|----|------|-----------------|-------|------|--------|-----------|
| ROLE-M01 | Example metric | ledger | ledger.example_metric | minutes/day | 30 | lower |

## Objectives

| ID | Objective | Metrics |
|----|-----------|---------|
| ROLE-O01 | Example objective | ROLE-M01 |

## Rules

| ID | Rule | Objective | Class | Source |
|----|------|-----------|-------|--------|
| ROLE-R01 | The role SHALL do the example thing. | ROLE-O01 | example-class | Example incident |

## Evaluations

| ID | Rule | Evidence source | Trigger | Method | Query or rubric | Evaluator | Comparator | Value | Unit | Cadence |
|----|------|-----------------|---------|--------|-----------------|-----------|------------|-------|------|---------|
| ROLE-R01-E1 | ROLE-R01 | ledger | ledger.example_trigger | deterministic | ledger.example_violations | evaluator | = | 0 | ticks | tick |
