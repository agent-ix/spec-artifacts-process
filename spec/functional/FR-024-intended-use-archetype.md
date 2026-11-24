---
id: FR-024
title: "IntendedUse archetype for a tool's stated operating purpose"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-artifacts-process/FR-009"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-011"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-012"
    type: "depends_on"
---
# FR-024: IntendedUse archetype for a tool's stated operating purpose

## Description

A person who rates a tool feature needs a stable account of what the tool is meant to do and which records it produces. The module SHALL declare the `IntendedUse` artifact type for a supplier's statement of one tool's purpose, users, outputs, limitations and operating context.

## Inputs

- A Markdown document with `type: IntendedUse`.
- The supplier tool package name.

## Outputs

- An `IntendedUse` record with a generated or authored `IU-NNN` identifier.
- A validated statement that a `FeatureRiskRating` can reference.

## Behavior

- The module SHALL require frontmatter fields `id`, `type`, `title`, `tool` and `relationships` for an `IntendedUse` document.
- The `id` field SHALL match `IU-{next:03d}`.
- The `type` field SHALL equal `IntendedUse`.
- The `tool` field SHALL identify one package or executable by its published name.
- The initial tool-validation scope SHALL include `quoin`, `quire-rs`, `quire-cli`, `engineering-assurance` and `filament-analyze`.
- A supplier tool repository SHALL contain exactly one `IntendedUse` document per tool package.
- The body SHALL contain `Purpose`, `Records produced`, `Who relies on them`, `Limits` and `Operating context` sections.
- `Records produced` SHALL name each record kind and the command that writes it.
- `Limits` SHALL state which conclusions the tool does not establish, including that the tool is not a compliance oracle and does not decide product or clinical safety.
- `Operating context` SHALL describe material inputs, execution environments and external tools used by the package.
- An `IntendedUse` document SHALL identify each external tool used by the package.
- Quoin's [FR-217](ix://agent-ix/quoin/FR-217) validation-report command SHALL report each external tool's version and its configuration-index reference.
- Quoin's [FR-220](ix://agent-ix/quoin/FR-220) external-tools configuration index SHALL provide the referenced tool configuration.
- The document SHALL use generic language.
- The document MAY name the public FDA guidance "Computer Software Assurance for Production and Quality System Software" as context.
- The document SHALL NOT reproduce that guidance's text.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-024-AC-1 | A document with every required field and body section validates as `IntendedUse`. | Test |
| FR-024-AC-2 | Removing any required section, including `Limits`, fails validation with a diagnostic naming that section. | Test |
| FR-024-AC-3 | An unknown frontmatter field fails validation with a diagnostic naming the field. | Test |
| FR-024-AC-4 | A valid intended-use fixture for each of `quoin`, `quire-rs`, `quire-cli`, `engineering-assurance` and `filament-analyze` validates. | Test |
| FR-024-AC-5 | A statement that omits a material limit or claims the tool decides product or clinical safety fails its content review criteria. | Inspection |
| FR-024-AC-6 | The `tool` vocabulary contains exactly the five named initial tools. | Test |
| FR-024-AC-7 | The validation report identifies the version and configuration-index entry for each external tool declared by the applicable `IntendedUse`. | Test |
| FR-024-AC-8 | An `IntendedUse` id has the form `IU-NNN` with exactly three digits. | Test |

## Dependencies

- The `IntendedUse` record is the supplier-side context for [FR-025](./FR-025-feature-risk-rating-archetype.md).
- [FR-009](./FR-009-emitted-json-schemas.md) declares the record schema, [FR-011](./FR-011-markdown-record-mapping.md) declares the Markdown mapping and [FR-012](./FR-012-executable-skeletons.md) declares its skeleton.
