---
id: StR-001
title: "Process artifact templates"
artifact_type: StR
---
# [StR-001] Process artifact templates

## Stakeholder

Filament platform / spec authors / agent CLI generators.

## Need

Engineering teams need standardized templates for ADRs, plans, reviews, findings, test matrices, and standards.

## Acceptance Criteria

| ID | Criteria |
|----|----------|
| StR-001-AC-1 | A Module activation against filament-core registers the contents this module declares. |
| StR-001-AC-2 | Agent CLI generators (minijinja-cli) can produce valid artifacts using the templates and schemas this module ships. |

## Dependencies

- **Upstream**: filament-core-service FR-035 (Module Manifest Schema)
