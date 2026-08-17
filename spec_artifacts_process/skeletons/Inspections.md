---
id: INS-001
title: "Inspection and analysis record"
type: Inspections
---
<!-- Inspection record authoring skeleton (spec-artifacts-process, ADR-0011).

     ONE per repository, at `spec/evidence/inspections.md` — inside `spec/`
     for the same reason as the suite registry (quire-rs CR-045 bounds the
     document walk).

     This is where the verification methods that produce NO source symbol are
     discharged: inspection, analysis, demonstration — the CR-041
     `no_source_symbol` class. A test run writes a machine record; an
     inspection is performed by a person, so the record of who did it, when,
     and against which commit IS the evidence.

     Contract (manifest body_extraction asserts, validated by `quire validate`):
     - Frontmatter: `type: Inspections`; `id` matches ^[A-Z]{2,4}-[0-9]+$.
     - REQUIRED (level 2): Inspections.
     - `## Inspections` MUST be a table with headers EXACTLY:
       ID | Obligation | Who | Commit | Verdict | Note — with >= 1 data row.
       `Note` may be omitted from the header row.
     - `ID` matches ^INSP-\d+$.
     - `Obligation` names the requirement or criterion this act discharges.
       It is a declared reference, so a typo dangles like any other broken
       trace reference rather than recording an act against nothing.
     - `Verdict` is one of Pass | Fail | Waived. A `Waived` row is a decision
       with a reason, not a silent pass — put the reason in `Note`. -->

## Inspections

| ID | Obligation | Who | Commit | Verdict | Note |
|----|------------|-----|--------|---------|------|
| INSP-001 | FR-001-AC-1 | @reviewer | abc123def456 | Pass | Read the generated output against the criterion |
