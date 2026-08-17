---
id: SUR-001
title: "Suite registry"
type: SuiteRegistry
---
<!-- Suite registry authoring skeleton (spec-artifacts-process, ADR-0011).

     ONE per repository, at `spec/evidence/suites.md`. The path matters: the
     quire document walk is bounded to `<scope>/spec` (quire-rs CR-045), so a
     registry outside it is validated by nothing and mints nothing while
     looking authoritative — the exact failure the evidence store exists to
     close. The machine-written half of the store (bindings.json, baseline.json,
     runs/**) is typeless and corpus-invisible by design and lives wherever the
     consuming workflow puts it.

     Contract (manifest body_extraction asserts, validated by `quire validate`):
     - Frontmatter: `type: SuiteRegistry`; `id` matches ^[A-Z]{2,4}-[0-9]+$.
     - REQUIRED (level 2): Suites.
     - `## Suites` MUST be a table with headers EXACTLY:
       ID | Name | Command | Tool | Evidence Kind — with >= 1 data row.
     - `ID` matches ^SUITE-\d+$. It is doc-scoped and NEVER renumbered:
       run directories, bindings and freshness all join on it, and a
       policy-immutable semantic slug is what produced the 1,014 dead trace
       tags (quire-rs#72).
     - `Evidence Kind` is one of the declared test-type values — the SAME
       vocabulary the Test Matrix `Type` column and the obligation record's
       verification method use. The TOOL goes in its own column, so a
       tool-specific report (semgrep, SARIF, SBOM) needs no new vocabulary.

     One suite = one command that can be run and whose result is one record.
     Splitting `make ci` into the suites it actually runs is the point: a
     partial run must never be able to masquerade as a full one. -->

## Suites

| ID | Name | Command | Tool | Evidence Kind |
|----|------|---------|------|---------------|
| SUITE-001 | Rust unit tests | `make test` | cargo test | Unit |
| SUITE-002 | Property suite | `make audit-property` | proptest | Property |
| SUITE-003 | Mutation score | `make mutants` | cargo-mutants | Static |
