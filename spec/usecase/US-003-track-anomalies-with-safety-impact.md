---
id: US-003
title: "Track an anomaly and its safety impact through to closure"
type: US
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/StR-001"
    type: "traces_to"
---
# US-003: Track an anomaly and its safety impact through to closure

## Story

**As a** quality or safety engineer responsible for a regulated software product
**I want** each reported anomaly kept as one validated record that shows how far it has progressed, what it could affect safety-wise, and who closed it
**So that** a reviewer or auditor can see that no anomaly was closed without its safety impact being judged and a named person standing behind the closure.

This story expresses the engineer's perspective in informal language and does not prescribe the record layout or the validation mechanism.

## Context

Anomalies today live in free-form tickets. Nothing checks that an anomaly was assessed before it was resolved, that its link to the requirements and hazards it touches still points at something real, or that a closure was made by an identifiable person.

## Acceptance Examples (Illustrative)

These examples clarify the engineer's expectations. They are illustrative only, not test cases and not verification criteria.

### US-003-EX-1: Closure without a person is refused

- **Given** an anomaly that has been resolved
- **When** it is marked closed with no one named as having closed it
- **Then** the record is reported as invalid

### US-003-EX-2: Assessed anomaly with no safety-impact judgement is refused

- **Given** an anomaly marked as assessed
- **When** it carries no safety-impact assessment
- **Then** the record is reported as invalid
