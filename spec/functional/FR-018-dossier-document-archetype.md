---
id: FR-018
title: "DossierDocument archetype for generated submission-dossier documents"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-011"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-012"
    type: "depends_on"
  - target: "ix://agent-ix/quire-cli/FR-034"
    type: "references"
  - target: "ix://agent-ix/quoin/FR-191"
    type: "references"
  - target: "ix://agent-ix/quoin/FR-202"
    type: "references"
  - target: "ix://agent-ix/quoin/FR-207"
    type: "references"
---
# FR-018: DossierDocument archetype for generated submission-dossier documents

## Description

`quoin dossier` ([quoin FR-191](ix://agent-ix/quoin/FR-191)) writes its source-derived
documents into a repository, and `quire export` renders them. Both need a
document type that validates, so this module declares the artifact type
`DossierDocument`. Its document kinds include the vulnerability-management plan
that records a tool's vulnerability intake, coordination, remediation and
communication process.

`quire export` reads `title`, `id` and, for document kinds that use it, `version`
from its committed input ([quire-cli FR-034](ix://agent-ix/quire-cli/FR-034)). The records-of-processing
document is generated for direct use and does not require export or version metadata. The body is free
Markdown. A commit is not a field or identity in the dossier record; the archetype records no digest or
subject-source hash, and its record carries no generic `provenance`. [FR-011](./FR-011-markdown-record-mapping.md)
gives every other model a `provenance` entry; `DossierDocument` remains the one exception. The document
also declares the distinct producer tool name and version in `producer_identity`; those fields identify
the generator and do not identify the document or its subject.

The producer names each document's `id` (for example `DOS-SRS`); this module
constrains it to non-empty text and mints no default. This module requires
`as_of` for `rmm`. A source-backed SOUP list needs the producer's `as_of`
under quoin FR-197, but this generic archetype also accepts a SOUP gap
document with no source binding and no `as_of`.

## Inputs

- A Markdown file with `type: DossierDocument`.

## Outputs

- Frontmatter members: `id`, `title`, `type: DossierDocument`, `document_kind`, `generated_by`, required `producer_identity: {name, version}`, optional `version` for document kinds that use it, and optional `as_of`.
- A record schema `DossierDocument.json`, projected from the `DossierDocument` TypeSpec model ([FR-009](./FR-009-emitted-json-schemas.md)).

## Behavior

- The `DossierDocument` frontmatter schema SHALL require `id`, `title`, `document_kind` and `generated_by`.
- For every `document_kind` other than `records-of-processing`, the frontmatter schema SHALL require a non-empty `version`. For `records-of-processing`, `version` SHALL be optional and, when present, non-empty.
- The `DossierDocument` frontmatter schema SHALL accept only non-empty text for `id`, `title` and any present `version`.
- The `DossierDocument` frontmatter schema SHALL accept only `srs`, `architecture`, `trace-matrix`, `rmm`, `verification-report`, `soup`, `anomalies`, `risk-management`, `risk-management-plan`, `release-record`, `threat-model`, `records-of-processing` or `vulnerability-management-plan` for `document_kind`.
- The `DossierDocument` frontmatter schema SHALL accept only `quoin dossier` for `generated_by`.
- The `DossierDocument` frontmatter schema SHALL require `producer_identity` as an object.
- The `producer_identity` object SHALL contain exactly `name` and `version`.
- The `producer_identity.name` value SHALL be `quoin`.
- The `producer_identity.version` value SHALL be non-empty text.
- The archetype SHALL treat `producer_identity` solely as generator identity, not as dossier-document or subject identity.
- The `DossierDocument` frontmatter schema SHALL accept `as_of` only as an RFC 3339 `date-time` instant in its upper-case `T` and `Z` form.
- Where `document_kind` is `rmm`, the `DossierDocument` frontmatter schema SHALL require `as_of`.
- The schema generator SHALL project the `DossierDocument` record schema from the `DossierDocument` TypeSpec model, with the same conditional `version` requirement as the frontmatter schema.
- The `DossierDocument` TypeSpec model SHALL declare `producerIdentity` with exactly `name` and `version`.
- The mapping SHALL copy those two values from `producer_identity` without deriving either value from the document's `version`, source document or Git commit.
- The emitted `DossierDocument` record schema SHALL require `producerIdentity.name` to be `quoin` and `producerIdentity.version` to be non-empty text.
- Where `documentKind` is `rmm`, the `DossierDocument` record schema SHALL require `asOf`.
- The `DossierDocument` frontmatter schema SHALL be the only validation authority for the `document_kind` and `generated_by` vocabularies.
- The `DossierDocument` TypeSpec model SHALL list the same `document_kind` and `generated_by` members as the frontmatter schema.
- The manifest SHALL declare no `choices` for `document_kind` or `generated_by`.
- The manifest SHALL declare no `id_pattern` default for `DossierDocument`.
- The archetype SHALL declare no member whose name contains `digest`, `hash`, `sha`, `revision` or `provenance` (case-insensitive) in its frontmatter schema, its record schema or its mapping.
- The archetype SHALL declare a skeleton.
- The archetype SHALL declare a mapped record schema.
- The `DossierDocument` mapping SHALL carry the role `definition`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-018-AC-1 | A fixture carrying `id`, `title`, `version`, `type`, `document_kind`, `generated_by`, `producer_identity: {name: quoin, version: "0.36.8"}` and `as_of` validates with `quire validate`, and the same fixture without `as_of` validates. | Test |
| FR-018-AC-2 | A non-`records-of-processing` fixture with no `version`, and one with an empty `version`, each fail `quire validate` naming `version`; a `records-of-processing` fixture without `version` validates, while one with an empty `version` fails naming `version`. | Test |
| FR-018-AC-3 | A fixture with `document_kind: not-a-dossier-kind` fails `quire validate`, with a diagnostic naming `document_kind`. | Test |
| FR-018-AC-4 | A fixture with `generated_by: hand` fails `quire validate`, and a fixture with no `generated_by` fails, each with a diagnostic naming `generated_by`. | Test |
| FR-018-AC-5 | No property name in the `DossierDocument` frontmatter schema, record schema or mapping, and no key of the golden record, contains `digest`, `hash`, `sha`, `revision` or `provenance` (case-insensitive), and the record schema has no `$ref` to `Provenance.json`. | Test |
| FR-018-AC-6 | The skeleton `DossierDocument.md` validates with `quire validate`. | Test |
| FR-018-AC-7 | `DossierDocument` carries the role `definition` in `mappings.yaml`. | Test |
| FR-018-AC-8 | A fixture with `document_kind: rmm` and no `as_of` fails `quire validate` with a diagnostic naming `as_of`, and a fixture with `document_kind: rmm` and an `as_of` validates. | Test |
| FR-018-AC-9 | A fixture whose `as_of` is the date `2026-11-01`, which is not an RFC 3339 `date-time`, fails `quire validate` with a diagnostic naming `as_of`. | Test |
| FR-018-AC-10 | A fixture with `id: SRS-2026` validates, a fixture with an empty `id` fails with a diagnostic naming `id`, and the manifest declares no `id_pattern` default for `DossierDocument`. | Test |
| FR-018-AC-11 | The `document_kind` and `generated_by` members of the frontmatter schema equal those of the projected record schema, and the manifest `body_extraction` of `DossierDocument` declares no `choices` for either. | Test |
| FR-018-AC-12 | `DossierDocument.json` matches a fresh projection of the TypeSpec model, so the schema generator's `--check` reports no drift. | Test |
| FR-018-AC-13 | The emitted record schema rejects a record with `documentKind: rmm` and no `asOf`, and accepts the same record with an RFC 3339 `asOf`. | Test |
| FR-018-AC-14 | Fixtures using `document_kind` values `verification-report`, `soup`, `anomalies`, `risk-management`, `risk-management-plan` and `release-record` each validate with `quire validate` when their required fields are present. | Test |
| FR-018-AC-15 | A `soup` fixture with no `as_of` validates as a gap document; the same fixture with a valid RFC 3339 `as_of` validates, while a malformed `as_of` fails `quire validate` naming `as_of`. | Test |
| FR-018-AC-16 | The emitted record schema accepts a `soup` record both without `asOf` and with a valid RFC 3339 `asOf`, and rejects a malformed `asOf`. | Test |
| FR-018-AC-17 | A fixture with `document_kind: threat-model` and `id: DOS-TM` validates with `quire validate` without `as_of`; the emitted record schema accepts `documentKind: threat-model` with no `asOf`; the record `document_kind` enum contains `threat-model`. | Test |
| FR-018-AC-18 | A fixture with `document_kind: records-of-processing` and `id: DOS-ROP` validates without `version` or `as_of`; the emitted record schema accepts `documentKind: records-of-processing` with neither `version` nor `asOf`; both projected schemas contain the new enum member. | Test |
| FR-018-AC-19 | A fixture with `document_kind: vulnerability-management-plan`, a non-empty `version`, and `generated_by: quoin dossier` validates with `quire validate`; the emitted record schema accepts `documentKind: vulnerability-management-plan`; the frontmatter and record kind vocabularies contain that member. | Test |
| FR-018-AC-20 | A `DossierDocument` fixture with `producer_identity: {name: quoin, version: "0.36.8"}` validates; omitting `producer_identity`, omitting either member, using a name other than `quoin`, using an empty version, or adding a third member fails validation naming `producer_identity`. | Test |
| FR-018-AC-21 | Mapping a valid dossier fixture copies its `producer_identity.name` and `producer_identity.version` values unchanged to `producerIdentity.name` and `producerIdentity.version`, without deriving either value from document version, source document or Git commit. | Test |
| FR-018-AC-22 | The projected `DossierDocument` record schema accepts a valid `producerIdentity` object and rejects a missing `producerIdentity`, missing `name`, missing `version`, or an additional member. | Test |

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md), [FR-009](./FR-009-emitted-json-schemas.md), [FR-011](./FR-011-markdown-record-mapping.md), [FR-012](./FR-012-executable-skeletons.md), quire-cli [FR-034](ix://agent-ix/quire-cli/FR-034)
- **Downstream**: quoin [FR-191](ix://agent-ix/quoin/FR-191) and its M2 content requirements [FR-196](ix://agent-ix/quoin/FR-196), [FR-197](ix://agent-ix/quoin/FR-197), [FR-198](ix://agent-ix/quoin/FR-198), [FR-199](ix://agent-ix/quoin/FR-199), [FR-200](ix://agent-ix/quoin/FR-200), [FR-201](ix://agent-ix/quoin/FR-201), M3 threat-model content [FR-202](ix://agent-ix/quoin/FR-202), and records-of-processing content [FR-207](ix://agent-ix/quoin/FR-207).
- **Merge order**: quoin FR-191 defines the producer and precedes this archetype.
