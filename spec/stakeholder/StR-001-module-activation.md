---
id: StR-001
title: "Process artifact templates"
type: StR
---
# StR-001: Process artifact templates

## Stakeholder Need

Engineering teams, spec authors, and agent CLI generators require standardized templates for ADRs, plans, reviews, findings, test matrices, and standards. The platform shall provide a Module whose activation registers these process archetypes so that authors and generators can produce consistent, valid process artifacts.

## Rationale

Process artifacts today are authored ad hoc, producing inconsistent structure that downstream tooling cannot reliably parse or validate. Shipping the templates, schemas, and archetypes as an activatable Module gives both human authors (via spec authoring) and agent CLI generators (via minijinja-cli) a single authoritative source, reducing drift and rework.

## Validation Criteria

This need is satisfied when:

- A Module activation against filament-core registers the contents this module declares (5 archetypes, 1 grammar, and 7 artifact types).
- Agent CLI generators (minijinja-cli) can produce valid artifacts using the templates and schemas this module ships.

## Stakeholders

The primary stakeholders are the Filament platform, spec authors, and agent CLI generators that rely on these archetypes.

## Dependencies

**Upstream**: filament-core-service [FR-035](ix://agent-ix/filament-core-service/FR-035) (Module Manifest Schema).
