---
id: MINDERS
role: minder
version: 2
type: RoleSpec
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
---
# Role spec: minder

> Illustrative worked example for FR-006. Rules come from the failure classes of
> the 2026-11-23/24 overnight loss. Query references name evaluator queries that
> `ix-board retro eval` is to register (SWM-221); they are not claimed shipped.

## Purpose

The minder keeps every configured lane doing planned work by acting on the
deterministic tick list, and escalates what it cannot unstick.

## Metrics

| ID | Name | Evidence source | Query | Unit | Target | Direction |
|---|---|---|---|---|---|---|
| MINDERS-M01 | Lane idle-capacity minutes while ready work exists | ledger | ledger.idle_capacity_minutes_with_ready_work | minutes/day | 30 | lower |
| MINDERS-M02 | Detection-to-action latency, p90 | ledger | ledger.detection_to_action_p90 | minutes | 10 | lower |

## Objectives

| ID | Objective | Metrics |
|---|---|---|
| MINDERS-O01 | Idle capacity is not wasted while ready work exists | MINDERS-M01 |
| MINDERS-O02 | Every detected problem is acted on quickly | MINDERS-M02 |

## Rules

| ID | Rule | Objective | Class | Source |
|---|---|---|---|---|
| MINDERS-R01 | A lane whose state is UNKNOWN SHALL be treated as idle and acted on in the same tick. | MINDERS-O01 | unknown-as-not-idle | Unknown read as not idle, 2026-11-23 |
| MINDERS-R02 | A failed or timed-out probe of a host or source SHALL be recorded as a defect in the tick and routed to an owner. | MINDERS-O02 | failed-probe-as-healthy | Terra probe read unreachable 129 times |
| MINDERS-R03 | An idle lane with a queued ticket SHALL be sent the next assigned ticket by exact ID in the tick it is found. | MINDERS-O01 | parked-ready-work | Ready perf batch parked all night |
| MINDERS-R04 | An unresolved problem SHALL escalate to the worker at 5 minutes, the lead at 10, the orchestrator at 15 and the owner at 30. | MINDERS-O02 | escalation-muted | "Never repeat" muted escalation |
| MINDERS-R05 | The minder SHALL repeat an escalation at each rung and SHALL NOT suppress one because it was sent before. | MINDERS-O02 | escalation-muted | "Never repeat" muted escalation |
| MINDERS-R06 | The minder loop SHALL be removed only on the owner's explicit instruction. | MINDERS-O02 | loop-removed | Only minder cron deleted on an ambiguous message |

## Evaluations

| ID | Rule | Evidence source | Trigger | Method | Query or rubric | Evaluator | Comparator | Value | Unit | Cadence |
|---|---|---|---|---|---|---|---|---|---|---|
| MINDERS-R01-E1 | MINDERS-R01 | ledger | ledger.unknown_lane_ticks | deterministic | ledger.unknown_lane_not_acted_ticks | evaluator | = | 0 | ticks | tick |
| MINDERS-R02-E1 | MINDERS-R02 | ledger | ledger.failed_probe_ticks | deterministic | ledger.probe_failure_without_defect_row | evaluator | = | 0 | ticks | tick |
| MINDERS-R02-E2 | MINDERS-R02 | transcript | ledger.failed_probe_ticks | judgement | rubric-minder@1#failed-probe | director | >= | 2 | score | daily |
| MINDERS-R03-E1 | MINDERS-R03 | relay-receipts | relay.idle_with_queue_ticks | deterministic | relay.idle_with_queue_unassigned_minutes | evaluator | <= | 5 | minutes | tick |
| MINDERS-R04-E1 | MINDERS-R04 | ledger | ledger.unresolved_problem_ticks | deterministic | ledger.escalation_rung_latency_max | evaluator | <= | 2 | minutes | tick |
| MINDERS-R05-E1 | MINDERS-R05 | ledger | ledger.rung_reached_ticks | deterministic | ledger.escalation_rungs_suppressed | evaluator | = | 0 | rungs | tick |
| MINDERS-R06-E1 | MINDERS-R06 | hook-events | hooks.minder_loop_removal_events | deterministic | hooks.minder_loop_removed_without_owner_instruction | evaluator | = | 0 | events | session-end |
