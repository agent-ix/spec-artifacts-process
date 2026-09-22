---
id: NFR-001
title: "Additive compatibility of the process-artifact contract"
type: NFR
quality_attribute: compatibility
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-010"
    type: "constrains"
  - target: "ix://agent-ix/spec-artifacts-process/FR-012"
    type: "constrains"
  - target: "ix://agent-ix/spec-artifacts-process/FR-013"
    type: "constrains"
---
# NFR-001: Additive compatibility of the process-artifact contract

## Statement

The module SHALL keep every archetype declaration it published at manifest version 0.1.0 present
and byte-identical at 0.2.0, apart from the reference-form `data_schema` key FR-010 adds and the
two `required: false` locators FR-012 adds.

NFR-001-AC-5 (the two-consumer measurement against `agent-ix/spec-objects-business` and
`agent-ix/filament-core-data`, TC-131) is removed: it validated other repositories from `~/dev`
through the `quire` CLI, and the owner ruled that prerelease software carries no backward-compat
test.

## Scope

- Applies to: `manifest.yaml`, the emitted schemas, and the shipped skeletons.
- Operational context: this module owns the archetypes every repository in the programme validates
  its Test Matrix, plans and reviews against, so a tightened pattern here is a build break
  everywhere. The change is advisory-only until human promotion, and no corpus repository is
  edited.
- Measured population: the 0.1.0 manifest baseline checked into `tests/fixtures/baseline-0.1.0/`
  and the twelve shipped skeletons.

## Rationale

The ticket's safety gate is "no enforcing release until the advisory sweep and human promotion"
and "do not broaden vocabularies solely to make malformed corpus data pass". Both directions are
failures: a widened vocabulary launders bad data, and a narrowed one turns a green consumer red
for a change that had nothing to do with it.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| 0.1.0 archetype declarations changed | 0 | 0 | Test |
| Declared vocabulary members added or removed | 0 | 0 | Test |
| Locators added that are `required: true` | 0 | 0 | Test |
| Shipped skeletons with an error finding under 0.2.0 | 0 | 0 | Test |

## Verification

The 0.1.0 manifest is checked in as a baseline fixture and compared key by key against 0.2.0: the
comparison is a structural diff, not a spot check, and the only differences it may report are the
twelve `data_schema` keys, the two added `Standard` locators, and the top-level `version` and
`semantic` keys.

The engine used is the one the tests run against: `quire` is a dev dependency resolved from
`internal-pypi` (`poetry install`), and the semantic tests fail rather than skip when it is
absent, because a skipped row is not coverage.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-001-AC-1 | Every 0.1.0 archetype, artifact type, object type, grammar, doc kind, traceability declaration and verification-catalog entry is present at 0.2.0 with identical content apart from the additions FR-010 and FR-012 name. | Test (TC-127) |
| NFR-001-AC-2 | No declared vocabulary — `Status`, `Type`, `Priority`, `Traces To`, `Severity`, `Escape Cause`, `Evidence Kind`, `Verdict`, `analysis`, `review_set` — gains or loses a member. | Test (TC-128) |
| NFR-001-AC-3 | Every locator added at 0.2.0 is `required: false`. | Test (TC-129) |
| NFR-001-AC-4 | Every shipped skeleton validates under 0.2.0 with zero error findings. | Test (TC-130) |

## Dependencies

- **Upstream**: [FR-010](../functional/FR-010-semantic-manifest-contract.md), [FR-012](../functional/FR-012-executable-skeletons.md), [FR-013](../functional/FR-013-definitions-not-occurrences.md); quoin FR-074 (`ix://agent-ix/quoin/FR-074`)
- **Downstream**: the advisory sweep and human promotion (`agent-ix/quoin#291`), outside this module
