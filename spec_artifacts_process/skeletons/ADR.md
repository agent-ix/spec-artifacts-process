---
id: ADR-001
title: "Bind emitted schemas by digest rather than by version"
type: ADR
relationships:
  - target: "ix://agent-ix/example/ADR-000"
    type: "relates_to"
---
<!-- ADR authoring skeleton (spec-artifacts-process). Fill every section with
     substantive content. Contract:
     - Frontmatter: `type: ADR`; `id` matches ^[A-Z]{2,4}-[0-9]+$ (ADR-001).
     - The archetype declares NO `body_extraction`, so no section is asserted
       by `quire validate`. The sections below are the convention this module
       ships, not a validated contract: adding one to the manifest would make
       every existing ADR in every consuming repository fail, which the
       module's compatibility posture forbids.
     - `allowed_links`: supersedes | superseded_by | relates_to | depends_on.
     - The archetype's `composition.states` are proposed | accepted |
       superseded | rejected; record the current one under `## Status`. -->
# ADR-001: Bind emitted schemas by digest rather than by version

## Status

Accepted, 2026-09-04. Supersedes nothing.

## Context

A module manifest references the JSON Schema of each type it declares. A
reference by version alone names whatever bytes that version currently holds,
so two consumers resolving the same version string from two registries can read
different schemas and neither can tell.

## Decision

The manifest SHALL reference each schema by path **and** SHA-256 digest, and the
build SHALL refuse a tree where a recorded digest and the shipped bytes differ.

## Consequences

Every schema regeneration rewrites the digests, so the schemas, the digests and
the manifest version move in one commit or the drift gate fails. A consumer that
resolves the reference can prove it read the bytes the module published. The
cost is that a version bump is no longer a one-line edit; that cost is accepted
and is discharged by `make schemas && make manifest-digests`.

## Alternatives Considered

- **Version-only reference.** Cheaper to maintain and unable to detect the
  failure it exists to prevent.
- **Inline the schema in the manifest.** Removes the resolution problem and
  makes the manifest unreadable; it also duplicates bytes the package already
  ships.
