# Webhook delivery design

Status: level 1 in review · Updated: 2026-11-16

## Problem statement
Customers poll the order system for changes, adding traffic and delaying integrations.

## Proposed solution
Deliver HMAC-signed order events to registered customer HTTPS endpoints with retries and retained failures.

## Goals
- G1: Deliver events within 10 seconds at p95 under an agreed workload.
- G2: Retain undeliverable events for seven days for internal operational replay.
- G3: Customers can verify event authenticity.

## Constraints
Go on the existing EKS cluster; the order system publishes orders.v1 to Kafka.

## Design map
| Level | Doc | Status |
| --- | --- | --- |
| 1 Context | [1-context.md](1-context.md) | in review |
| 2 Containers | 2-containers.md | not started |

## Decisions
| # | Level | Decision | Alternatives considered | Reason |
| --- | --- | --- | --- | --- |
| 1 | 1 | Replay is an internal operational action | Customer self-service replay | The user rejected customer-triggered replay; revised context awaits approval |

## Open questions
| # | Question | Classification | Affected work | Owner |
| --- | --- | --- | --- | --- |
