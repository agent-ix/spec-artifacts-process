---
id: AN-001
title: "<short summary of the anomaly>"
type: Anomaly
status: assessed
safety_impact: impacting
severity: major
---
<!-- Anomaly authoring skeleton (spec-artifacts-process). One document per
     reported anomaly. Contract (validated by `quire validate`):
     - Frontmatter: type: Anomaly; id matches ^[A-Z]{2,4}-[0-9]+$ (e.g. AN-001);
       status ∈ identified|assessed|resolved|closed;
       resolution ∈ fixed|not-a-defect|duplicate|wont-fix, present exactly when
       status is resolved or closed (resolved requires fixed);
       closed_by is a named person, present exactly when status is closed;
       safety_impact ∈ unassessed|none|impacting;
       severity ∈ minor|major|critical, assigned by a person: it has no default
       and is derived from nothing. It may be omitted while status is
       identified and is required from assessed onward.
     - There is no typed history. Who moved the status, and when, is the git
       history of this file; the legality of each move is judged by
       `quoin anomaly check`.
     - REQUIRED body (level 2): ## Description.
     - ## Safety Impact Assessment: optional while status is identified, required
       (and safety_impact not unassessed) from assessed onward. A table with
       headers Kind | Target | Impact | Rationale and at least one row.
       Kind ∈ Requirement|Hazard|None; Impact ∈
       Affects|Mitigates|Introduces|Unaffected|None, where None is admitted only
       on a row of Kind None. A Requirement row's Target is an FR, NFR or
       acceptance-criterion id; a Hazard row's Target is a hazard id.
       safety_impact: none takes exactly one row: Kind None, Target -, Impact None.
       safety_impact: impacting takes at least one Requirement or Hazard row
       whose Impact is not Unaffected.
     - ## Fix Verification: required when resolution is fixed, otherwise omit
       it. A table with headers Kind | Target | Rationale and at least one row.
       Kind ∈ Criterion|Test; a Criterion row's Target is an FR or NFR
       acceptance-criterion id, a Test row's Target is a test-case id of a
       TestMatrix. This skeleton is an assessed anomaly, so it carries none.
     - ## Release Rationale: optional, only on an anomaly that is not closed or
       is closed as wont-fix. A table with headers Author | Rationale and at
       least one row; each cell is non-empty and not a placeholder (n/a, none,
       unknown, tbd, -). It is a person's written reason for releasing with the
       anomaly not fixed; it is never filled in for you, so it is not in this
       skeleton. -->
# [AN-001] <short summary of the anomaly>

## Description

<What was observed, where, and how it differs from what was expected.>

## Safety Impact Assessment

| Kind | Target | Impact | Rationale |
|------|--------|--------|-----------|
| Requirement | FR-001 | Affects | <why the anomaly bears on this requirement> |
| Requirement | FR-001-AC-1 | Affects | <why the anomaly bears on this acceptance criterion> |
| Hazard | HAZ-001 | Introduces | <why the anomaly introduces or worsens this hazard> |
