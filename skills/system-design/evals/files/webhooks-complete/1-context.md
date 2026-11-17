# Level 1: Context

Zooms into: — · Status: approved 2026-11-10

## Diagram
Webhook delivery system context. Blue is the system being designed; grey is existing or external.

```mermaid
flowchart TB
  dev["Customer developer<br/>[Person]<br/>Registers endpoints and inspects deliveries"]:::person
  sys["Webhook delivery service<br/>[Software system]<br/>Delivers signed order events to customer endpoints"]:::internal
  orders["Order system<br/>[External system]<br/>Publishes order changes"]:::external
  cust["Customer endpoint<br/>[External system]<br/>Receives events over HTTPS"]:::external

  dev -->|"Registers endpoints, views failures, replays events"| sys
  orders -->|"Publishes order change events"| sys
  sys -->|"POSTs signed events"| cust

  classDef person fill:#08427b,stroke:#052e56,color:#ffffff
  classDef internal fill:#1168bd,stroke:#0b4884,color:#ffffff
  classDef external fill:#8a8a8a,stroke:#5c5c5c,color:#ffffff
```

## Elements
| Element | Type | Technology | Responsibility |
| --- | --- | --- | --- |
| Customer developer | Person | — | Registers endpoints, inspects and replays failed deliveries |
| Webhook delivery service | System | — | Delivers signed order events to customer endpoints |
| Order system | External system | — | Publishes order changes |
| Customer endpoint | External system | — | Receives events |

## Relationships
| From | To | Purpose | Protocol | Failure behaviour |
| --- | --- | --- | --- | --- |
| Customer developer | Webhook service | Manage endpoints and replay | — | Developer sees an error; deliveries continue |
| Order system | Webhook service | Publish order changes | — | Events buffer upstream until the service consumes |
| Webhook service | Customer endpoint | Deliver events | — | Retry, then dead letter |

## Deferred to the next level
- Storage, queueing, retry scheduling, signing key management.
