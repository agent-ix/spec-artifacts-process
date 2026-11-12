---
id: FR-015
title: "Anomaly safety-impact assessment with resolving links"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-003"
    type: "implements"
  - target: "ix://agent-ix/spec-artifacts-process/FR-014"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-safety/spec/spec"
    type: "depends_on"
---
# FR-015: Anomaly safety-impact assessment with resolving links

## Description

The `Anomaly` type ([FR-014](./FR-014-anomaly-archetype-and-state-lifecycle.md)) SHALL carry a
required safety-impact field and a `## Safety Impact Assessment` section linking the anomaly to the
requirements and hazards it affects, SHALL fail validation when an anomaly that has reached
`assessed` or later has no assessment, and SHALL fail validation when a link names an id that
resolves to nothing.

## Inputs

- Frontmatter `safety_impact` of an `Anomaly` document.
- The `## Safety Impact Assessment` section of that document.
- The corpus the document is validated in: its requirement artifacts (`FR`, `NFR`) and its `hazard`
  artifacts (the hazard id class is owned by `agent-ix/spec-objects-safety`).

## Outputs

- A validated assessment, or located validation failures naming the missing assessment or the
  dangling link.

## Behavior

- Every `Anomaly` SHALL carry `safety_impact`, one of exactly `unassessed`, `none`, `impacting`.
- While `status` is `identified`, `safety_impact` MAY be `unassessed` and the section MAY be absent.
- When `status` is `assessed`, `resolved` or `closed`, `safety_impact` SHALL NOT be `unassessed`
  and the document SHALL carry a `## Safety Impact Assessment` section; otherwise validation fails.
- The section SHALL be a table with headers exactly `Kind | Target | Impact | Rationale` and at
  least one row. `Kind` is one of `Requirement`, `Hazard`, `None`. `Rationale` SHALL be non-empty.
- A `Requirement` row's `Target` SHALL be the id of an `FR` or `NFR` artifact, or of one of its
  acceptance criteria, that exists in the validated corpus. A `Hazard` row's `Target` SHALL be the
  id of a `hazard` artifact that exists in the validated corpus. A `Target` that resolves to
  nothing, or to an artifact of another kind, SHALL fail validation as a dangling reference.
- `Impact` SHALL be one of `Affects`, `Mitigates`, `Introduces`, `Reviewed - unaffected`.
- When `safety_impact` is `impacting`, the table SHALL hold at least one `Requirement` or `Hazard`
  row whose `Impact` is not `Reviewed - unaffected`.
- When `safety_impact` is `none`, the table SHALL hold exactly one row, of `Kind` `None`, with
  `Target` `-` and a non-empty `Rationale`; no `Requirement` or `Hazard` row SHALL appear.
- The assessment SHALL be a statement of an engineer's judgement, not a computed risk acceptance;
  this requirement SHALL NOT add any risk-acceptance or sign-off field.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-015-AC-1 | The manifest declares `safety_impact` with exactly the three-member vocabulary, and the section table with exactly the four columns, `min_rows: 1`, and the `Kind` and `Impact` vocabularies above. | Test |
| FR-015-AC-2 | An `identified` anomaly with `safety_impact: unassessed` and no section validates. | Test |
| FR-015-AC-3 | For each of `assessed`, `resolved` and `closed`, a fixture with no `## Safety Impact Assessment` section fails validation, and a fixture with `safety_impact: unassessed` fails validation. | Test |
| FR-015-AC-4 | In a corpus containing `FR-001` and hazard `HAZ-001`, an `impacting` anomaly whose rows target `FR-001` and `HAZ-001` validates. | Test |
| FR-015-AC-5 | The same anomaly with a `Requirement` row targeting `FR-999`, or a `Hazard` row targeting `HAZ-999`, fails validation with a diagnostic naming the unresolved id and its row. | Test |
| FR-015-AC-6 | A `Requirement` row whose `Target` is `HAZ-001`, and a `Hazard` row whose `Target` is `FR-001`, each fail validation as a kind mismatch. | Test |
| FR-015-AC-7 | An `impacting` anomaly whose only rows are `Reviewed - unaffected` fails validation; a `none` anomaly with one `None` row and a rationale validates; a `none` anomaly that also carries a `Hazard` row fails validation. | Test |
| FR-015-AC-8 | A row with an empty `Rationale`, or with an `Impact` outside the vocabulary, fails validation. | Test |
| FR-015-AC-9 | The skeleton validates as authored in a corpus that supplies its linked ids, and negative counterparts exist for a missing assessment and a dangling link. | Test |

## Dependencies

- **Upstream**: [FR-014](./FR-014-anomaly-archetype-and-state-lifecycle.md); quire-rs FR-050 (traceability model and document references); `agent-ix/spec-objects-safety` (owner of the `hazard` type and its ids)
- **Downstream**: quoin [FR-136](ix://agent-ix/quoin/FR-136)
