---
id: FR-011
title: "Markdown mapping and round-trip policy for the process artifact records"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/US-002"
    type: "implements"
  - target: "ix://agent-ix/spec-artifacts-process/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-010"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-071"
    type: "uses"
  - target: "ix://agent-ix/quoin/FR-072"
    type: "uses"
---
# FR-011: Markdown mapping and round-trip policy for the process artifact records

## Description

The module SHALL publish, for every model FR-009 emits, a machine-readable mapping from the
authored Markdown to each property of the record, using exactly the nine mapping kinds the
manifest declares, and SHALL declare that the Markdown is the sole authority and the record is a
derived projection, so that every consumer builds the same record from the same document.

The Markdown forms are the ones this module's archetypes already assert. This requirement adds no
table header, renames no heading, reorders no column, and admits no vocabulary member.

## Inputs

- `spec_artifacts_process/mappings.yaml`: per model, the authority and round-trip policy, and per
  property the mapping kind, its source, and the cell-level parse the kind applies.
- `spec_artifacts_process/mappings.schema.json`: the schema `mappings.yaml` itself validates
  against, so a malformed mapping is a schema error rather than a reader's surprise.
- The emitted schemas of [FR-009](./FR-009-emitted-json-schemas.md), which fix the property set
  every mapping entry must name.
- The `body_extraction` locators of [FR-010](./FR-010-semantic-manifest-contract.md), which fix the
  section names and column lists a mapping may name.
- The quoin conventions for typed tables and clauses (quoin FR-071, FR-072) and the quire-rs
  byte-exact section slice (quire-rs FR-008).

## Outputs

- `spec_artifacts_process/mappings.yaml` and `spec_artifacts_process/mappings.schema.json`,
  shipped in the sdist, the wheel and the npm payload.
- One golden record per skeleton at `spec_artifacts_process/examples/<Type>.record.json`, built by
  the reference mapping and validated against that type's emitted schema, shipped in all three
  payloads.
- A reference mapping implementation in the module's test support (Python). It is a test oracle,
  not module code; the module ships data only.

## Behavior

- The mapping SHALL use exactly the nine kinds the manifest declares: `frontmatter`, `section`,
  `table`, `typed-table`, `sysml-fence`, `ocl-clause`, `list`, `token`, `provenance`.
- Every declared mapping kind SHALL be used by at least one model property, so the manifest
  declares no kind the module does not exercise: `list` fills `SpecReview.scope` and the `Plan`
  and `Task` bullet sections, and `token` fills the trace-token lists of `TestMatrix` and
  `TestMatrixIndex` and the `refs` of a findings row. The module SHALL remove from
  `semantic.mappings` any kind no property uses, rather than declaring it aspirationally.
- The mapping SHALL be strict: any reported error means no record is built for that document, and
  every error found in one pass is reported. Reporting three errors and building no record is one
  behaviour, not two — a partial record whose missing properties are indistinguishable from
  absent ones is the failure this rule removes.
- Every property of every emitted model SHALL be named by exactly one mapping entry, and every
  mapping entry SHALL name a property its model declares.
- A `frontmatter` mapping SHALL name a frontmatter key path and the record property it fills.
- A `frontmatter` mapping SHALL drop every frontmatter key it does not name.
- `mappings.yaml` SHALL record the dropped key set per model, so the loss is declared rather than
  silent.
- A `section` mapping SHALL name a level-2 heading and fill a `Section` property with the
  heading's byte-exact content and its 1-based start and end lines.
- A `table` mapping SHALL name a section and a column list equal to the `assert.columns` of the
  corresponding locator, and SHALL fill an array with one object per data row in authored order,
  cells trimmed, each row carrying its 1-based line.
- A `table` mapping SHALL omit a column the locator declares in `optional_columns` when the
  authored table does not carry it, and SHALL NOT synthesise a value for it.
- A `typed-table` mapping SHALL be a `table` mapping whose cells are parsed further: an id cell
  into the row `id`, a marker cell into `{marker, note}`, and a trace cell into an ordered list of
  reference tokens.
- The `Status` marker parse SHALL split the leading marker from the remainder of the cell, so
  `🚧 scale evidence deferred` is `marker: 🚧` and `note: "scale evidence deferred"`, and a cell
  carrying only a marker SHALL omit `note`.
- The `Traces To` parse SHALL expand the two authoring shorthands the archetype admits — the
  elided-parent continuation (`FR-001-AC-2, -AC-3`) and the slash enumeration (`FR-016-AC-1/2/3`)
  — into the token list they abbreviate.
- The `Traces To` parse SHALL carry a parenthesised remainder verbatim as that token's `note`.
- The `Traces To` parse SHALL map a lone `-` to an empty token list with `noTrace: true`, so the
  explicit no-trace form and a missing cell are distinguishable.
- A `sysml-fence` mapping SHALL read one ```` ```sysml ```` fence under a named section as the
  alternate form of the same typed-table declarations.
- The module SHALL declare a `sysml-fence` mapping only where the model carries a typed
  declaration list.
- If a document carries both the typed table and the `sysml` fence under one section, then the
  mapping SHALL report a `both-forms` error and build no record, because one artifact carries one
  form.
- An `ocl-clause` mapping SHALL read, under a named section, each `### <clauseId>` subsection
  holding exactly one ```` ```ocl ```` fence, and fill a `ClauseRef` per clause with
  `language: ocl` and that `clauseId`.
- The `ocl-clause` mapping SHALL omit `sourceSpan`, because semantic-core `SourceLocus` requires a
  `sourceIdentity` and this module's surface does not supply one.
- If the named section holds prose and no fence, then the `ocl-clause` mapping SHALL yield an
  empty clause list rather than an error, because the section is optional and prose under it is
  commentary.
- If a fence appears under the section with no `### <clauseId>` heading of its own, if a
  subsection holds a second fence, if a fence is unterminated, or if two subsections declare the
  same `clauseId`, then the mapping SHALL report `orphan-fence`, `second-fence`,
  `unterminated-fence` or `duplicate-clause-id` respectively and SHALL build no record.
- A `list` mapping SHALL name a section and fill a string array with one entry per top-level
  bullet, the bullet marker removed and the text trimmed.
- A `token` mapping SHALL name a pattern and fill a scalar or a string array from the matches in
  the named section, in document order.
- A `provenance` mapping SHALL fill `provenance` with the document path as supplied, the SHA-256 of
  the document bytes as read, and the caller's `sourceIdentity` when one is supplied.
- The record SHALL carry no property that is not derivable from the document and the caller's
  provenance inputs; the Markdown is the sole authority and no default is invented.
- If a required section, a required table, or a required cell is absent, then the mapping SHALL
  report one error naming the model, the property and the document line, and SHALL report every
  such error of one document in one pass rather than stopping at the first.
- If a table declares two data rows with the same id, then the mapping SHALL report
  `duplicate-row-id` naming both lines.
- The mapping SHALL scope row-id uniqueness **per table**, not per document: a `TestMatrixIndex` carries
  `INT-` and `GAP-` ids in different tables and a `TestMatrix` carries rows in five, and the id
  namespaces are per table by construction. A document-scoped rule would reject conforming
  documents.
- The totality walk that checks the mapping against the emitted models (CON-2) SHALL be
  cycle-safe: the models `$ref` each other and a naive recursive walk does not terminate.
- The mapping SHALL treat `\|` inside a cell as a literal pipe rather than a column separator.
- The mapping SHALL normalise `CRLF` to `LF` before slicing sections, so a Windows checkout
  produces the same record as a Unix one.
- The mapping SHALL compute `provenance.digest` over the **normalised** bytes rather than the
  bytes as read, so one document has one digest whatever the checkout did to its line endings; the repository
  pins `eol=lf` (FR-009) so the two are the same in practice, and this rule is what makes that a
  guarantee rather than a coincidence.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-011-CON-1 | `mappings.yaml` SHALL name only sections and columns the manifest's `body_extraction` already declares. | Consistency | Test |
| FR-011-CON-2 | The mapping SHALL be total in both directions: no unmapped model property and no mapping entry naming an undeclared property. | Completeness | Test |
| FR-011-CON-3 | Nothing in production builds a process record from Markdown today; the reference mapping is a test oracle and the module ships data only. | Architecture | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-011-AC-1 | `mappings.yaml` validates against `mappings.schema.json`, and every model FR-009 emits has an entry declaring the authority and the round-trip policy. | Test (TC-097) |
| FR-011-AC-2 | Every property of every emitted model is named by exactly one mapping entry, and every mapping entry names a property its model declares. | Test (TC-098) |
| FR-011-AC-3 | Every section and column `mappings.yaml` names is declared by the manifest's `body_extraction` for that type. | Test (TC-099) |
| FR-011-AC-4 | For each shipped skeleton, the reference mapping builds a record that validates against that type's emitted schema, and the record equals the shipped `examples/<Type>.record.json` byte for byte. | Test (TC-100) |
| FR-011-AC-5 | A `Status` cell carrying a marker and a note splits into `marker` and `note`; a bare marker yields no `note`. | Test (TC-101) |
| FR-011-AC-6 | The `Traces To` parse expands the elided-parent and slash shorthands into the tokens they abbreviate, carries a parenthesised remainder as `note`, and maps a lone `-` to an empty list with `noTrace: true`. | Test (TC-102) |
| FR-011-AC-7 | A table omitting a declared optional column yields rows without that key rather than rows with a synthesised value. | Test (TC-103) |
| FR-011-AC-8 | Prose under the clause section yields an empty clause list; an orphan fence, a second fence in one subsection, an unterminated fence and a duplicate `clauseId` each report their named error and build no record. | Test (TC-104) |
| FR-011-AC-9 | A document carrying both the typed table and the `sysml` fence under one section reports `both-forms` and builds no record. | Test (TC-105) |
| FR-011-AC-10 | A document with three independent defects reports three errors in one pass, each naming the model, the property and the line. | Test (TC-106) |
| FR-011-AC-11 | Two rows sharing an id report `duplicate-row-id` naming both lines. | Test (TC-107) |
| FR-011-AC-12 | An escaped pipe inside a cell is carried as a literal pipe and does not split the row. | Test (TC-108) |
| FR-011-AC-13 | A CRLF copy of a skeleton produces the same record as its LF original. | Test (TC-109) |
| FR-011-AC-14 | Every frontmatter key a model does not declare is listed in that model's dropped key set. | Test (TC-110) |
| FR-011-AC-15 | For every key an emitted model and that type's `frontmatter_schema_ref` both describe, the two agree on type and pattern — the drift this ticket exists to end is not replaced by a new pair of drifting declarations. | Test (TC-137) |
| FR-011-AC-16 | The totality walk terminates on the shipped models, which contain at least one reference cycle. | Test (TC-138) |
| FR-011-AC-17 | Two rows sharing an id in **different** tables of one document are accepted; two in the same table are not. | Test (TC-139) |
| FR-011-AC-18 | Every mapping kind named in `semantic.mappings` is used by at least one model property. | Test (TC-140) |

## Dependencies

- **Upstream**: [FR-009](./FR-009-emitted-json-schemas.md), [FR-010](./FR-010-semantic-manifest-contract.md); quoin FR-071/FR-072 (`ix://agent-ix/quoin/FR-071`, `ix://agent-ix/quoin/FR-072`)
- **Downstream**: [FR-012](./FR-012-executable-skeletons.md)
