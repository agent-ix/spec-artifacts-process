---
id: US-004
title: "Author a role spec and have its rules and evaluations checked like requirements"
type: US
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/StR-001"
    type: "traces_to"
  - target: "ix://agent-ix/dev-team/US-002"
    type: "traces_to"
---
# US-004: Author a role spec and have its rules and evaluations checked like requirements

## Story

**As a** department owner who runs agent roles for days at a time
**I want** each role written as one document of objectives, metrics, rules and checks that is validated the way requirements are, and that fails when a rule has no check or an objective has no measure
**So that** every rule a role carries can be measured, and a rule nobody can check is rejected before it ships instead of discovered after the next incident.

This story expresses the owner's perspective in informal language and does not prescribe the document layout or the validation mechanism.

## Context

Role guidance grows by one rule after each incident, and nothing later shows whether the rule was followed. dev-team US-002 and FR-006 to FR-008 define the role-spec format and the evaluator. This module is where Quire learns the document type, so the format is validated and its ids enter the same traceability the requirements use.

## Acceptance Examples (Illustrative)

These examples clarify the owner's expectations. They are illustrative only, not test cases and not verification criteria.

### US-004-EX-1: A rule with no check is refused

- **Given** a role spec with a rule that no evaluation checks
- **When** the role spec is validated
- **Then** the rule is named and the result is a failure

### US-004-EX-2: An objective with no measure is refused

- **Given** a role spec with an objective that lists no metric, or a metric that does not exist
- **When** the role spec is validated
- **Then** the objective is named and the result is a failure

### US-004-EX-3: A measure nothing uses is called out

- **Given** a role spec with a metric that no objective uses
- **When** the role spec is validated
- **Then** the metric is reported as a warning
