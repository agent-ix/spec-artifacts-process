---
id: FR-021
title: "RoleSpec trace targets and cross-row integrity: rules, evaluations, objectives, metrics"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-004"
    type: "satisfies"
  - target: "ix://agent-ix/spec-artifacts-process/FR-020"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/dev-team/FR-007"
    type: "implements"
---
# FR-021: RoleSpec trace targets and cross-row integrity: rules, evaluations, objectives, metrics

## Description

A rule is a requirement and an evaluation is its criterion ([dev-team FR-007](ix://agent-ix/dev-team/FR-007)). The module SHALL declare the `RoleSpec` ids as trace targets and the table cells that name them as document references, so that Quire's existing traceability computes the lint: a rule with no evaluation is unmeasured, an evaluation naming no rule is dangling, and an evaluator's registered query binds an evaluation by carrying its id as a trace tag, exactly as a test binds `FR-001-AC-1`. No role-spec-specific checker is written.

Where the engine cannot yet express a check, this requirement states the check and the gap is tracked against quire-rs (see the capability list below), not worked around in this module.

## Behavior

Declared in `manifest.yaml` `traceability:`:

- Trace targets, archetype `RoleSpec`, excluding `tests/**`, `tests_integration/**` and `fixtures/**`: `role-metric` (section `Metrics`, id column `ID`), `role-objective` (`Objectives`), `role-rule` (`Rules`) and `role-evaluation` (`Evaluations`). Rule and objective targets declare `evidence: reference-only`; `role-evaluation` is the evidence-bearing criterion target, bound by evaluator trace tags.
- Document references, each resolving only to the named target, with a pattern admitting the `<PREFIX>-R01`, `<PREFIX>-R01-E1`, `<PREFIX>-M01` and `<PREFIX>-O01` shapes (the module's existing id patterns do not admit a letter-led number, so the `RoleSpec` references declare their own):
  - `Objectives.Metrics` to `role-metric`; `Rules.Objective` to `role-objective`; `Evaluations.Rule` to `role-rule`.
- A reference to an undefined id SHALL report as the engine's `dangling-trace-reference` finding, naming the referencing row.

Checks, and where each is computed:

- Objective to metric: an objective whose `Metrics` cell is empty fails `quire validate` (the column is a required non-empty cell); one naming an undefined metric is a dangling reference.
- Rule to evaluation: a rule that no evaluation's `Rule` cell names is reported as unmeasured and fails. This needs the engine to treat a rule as the parent of the evaluations that reference it (capability 1 below).
- Evaluation to rule: an evaluation naming an undefined rule is a dangling reference and fails.
- Unused metric: a metric that no objective names is reported as a warning (capability 2).
- Metric query distinct from evaluation queries: a metric whose `Query` equals the `Query or rubric` or `Trigger` of any evaluation fails, naming both ids (capability 3).
- Duplicate ids within one role spec fail (capability 4, or the engine's duplicate-mint finding if it reports one for table-minted ids).
- Versioned rubric references: the shape `<rubric>@<version>#<check-slug>` is asserted by FR-020. Whether the reference resolves to a rubric file, version and check slug is a binding check reported `unbound` (capability 5).

Engine capabilities this module cannot supply and quire-rs would need:

1. Rule-parented criteria through a column: a criterion target that names the column holding its parent's id, so `quire matrix` groups rows by rule and reports a parent with no criterion. Today a criterion's parent is the document whose id prefixes it.
2. Orphan check on a minted id class: a declaration that a target's ids must be referenced by at least one reference of a named kind, reported at warning severity.
3. A cross-table row assert: equality or inequality between a cell in one table and cells in another, naming both rows.
4. A uniqueness assert over a table's id column within one document (the module already records this as missing, see the `TC-024` note in the Test Matrix mapping).
5. Resolution of a versioned reference of the form `<name>@<version>#<slug>` against a declared artifact class (depends on the rubric home, an open question).

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-021-AC-1 | The manifest declares `role-metric`, `role-objective`, `role-rule` and `role-evaluation` trace targets over a `RoleSpec` fixture, and `quire matrix --scope` over that fixture mints every rule and evaluation id of the worked minder spec. | Test |
| FR-021-AC-2 | A role spec containing a rule that no evaluation names exits nonzero from the matrix-based lint, naming the rule id. | Test |
| FR-021-AC-3 | An evaluation naming an undefined rule, an objective naming an undefined metric, and a rule naming an undefined objective each produce `dangling-trace-reference` naming the referencing id. | Test |
| FR-021-AC-4 | An objective whose `Metrics` cell is empty fails `quire validate`, naming the objective id. | Test |
| FR-021-AC-5 | A metric no objective names produces a warning and does not change the exit status. | Test |
| FR-021-AC-6 | A metric whose `Query` equals the query of an evaluation fails, naming the metric and evaluation ids. | Test |
| FR-021-AC-7 | Two rows with the same id in one table fail, naming the id. | Test |
| FR-021-AC-8 | A `RoleSpec` placed outside `spec/` produces no matrix rows, and `quire validate` over its path still validates its shape. | Test |
| FR-021-AC-9 | When the engine lacks a capability listed above, the corresponding check is absent from the module, no substitute parser exists in this repository, and a ticket for the capability is linked from this requirement. | Inspection |
| FR-021-AC-10 | A judgement evaluation whose rubric reference is well formed but resolves to no rubric is reported `unbound` and fails the lint; deterministic evaluations with no trace-tagged query are `unbound` under `quire matrix --repo`. | Test |

## Dependencies

- [FR-004](./FR-004-traceability-declaration.md), the traceability declaration this extends.
- [FR-020](./FR-020-rolespec-archetype.md), the tables whose ids and cells these declarations read.
- quire-rs capabilities 1 to 5 above, tracked as quire-rs tickets.
- dev-team FR-007, the lint these checks compute.
