# 0.1.0 manifest baseline

A byte copy of `spec_artifacts_process/manifest.yaml` as it stood at manifest
version 0.1.0, taken **before** the #78 semantic-module contract touched it.

It exists so NFR-001-AC-1 and FR-010-AC-3 are a structural diff over every
declaration class rather than a spot check. This module owns the archetypes
every repository in the programme validates against; the only differences the
diff may report are:

- the twelve `data_schema` reference-form keys FR-010 adds,
- the two `required: false` locators FR-012 adds to `Standard`,
- the top-level `version` (0.1.0 -> 0.2.0),
- the top-level `semantic` block.

Anything else is a breaking change to every consuming repository and stops the
merge. Do not regenerate this file: a baseline you can refresh is not a baseline.
