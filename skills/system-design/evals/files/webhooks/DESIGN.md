# Webhook delivery design

Status: level 2 in progress · Updated: 2026-11-10

## Problem statement
Customers integrating with our order system poll the orders API every few seconds to detect changes. Polling costs us roughly 40% of API traffic, customers see changes up to a minute late, and enterprise prospects reject the integration for lacking push notifications.

## Proposed solution
A webhook delivery service: customers register HTTPS endpoints and event types, and the service sends HMAC-signed order events with retries and a dead letter queue.

## Goals
- G1: Customers receive an order event within 10 seconds of the change at p95.
- G2: No event is lost; undeliverable events are retained for 7 days and can be replayed.
- G3: Customers can verify each event came from us.

## Non-goals
- Event types other than order lifecycle events.
- Customer-defined filtering beyond event type.

## Constraints
- Runs on the existing EKS cluster; team of three Go engineers.
- Order system already publishes order changes to Kafka topic `orders.v1`.

## Design map
| Level | Doc | Status |
| --- | --- | --- |
| 1 Context | [1-context.md](1-context.md) | approved 2026-11-10 |
| 2 Containers | 2-containers.md | not started |

## Glossary
| Term | Meaning |
| --- | --- |
| Endpoint | A customer-registered HTTPS URL plus the event types it subscribes to |
| Delivery | One attempt to POST one event to one endpoint |

## Decisions
| # | Level | Decision | Alternatives considered | Reason |
| --- | --- | --- | --- | --- |
| 1 | 1 | Consume `orders.v1` rather than have the order system call us | Synchronous call from order system | Keeps the order system unaware of webhooks |

## Open questions
| # | Question | Blocks | Owner |
| --- | --- | --- | --- |

## Traceability
| Goal | Delivered by |
| --- | --- |
