# Level 1: Context

Zooms into: — · Status: in review

## Diagram
Webhook delivery system context. Blue is the system being designed; grey is existing or external.

```mermaid
flowchart TB
  dev["Customer developer<br/>[Person]<br/>Registers endpoints and inspects deliveries"]:::person
  ops["Operations engineer<br/>[Person]<br/>Replays retained failures"]:::person
  sys["Webhook delivery service<br/>[Software system]<br/>Delivers signed order events to customer endpoints"]:::internal
  orders["Order system<br/>[External system]<br/>Publishes order changes"]:::external
  cust["Customer endpoint<br/>[External system]<br/>Receives events over HTTPS"]:::external

  dev -->|"Registers endpoints and views failures"| sys
  ops -->|"Replays retained failures"| sys
  orders -->|"Publishes order change events"| sys
  sys -->|"POSTs signed events"| cust

  classDef person fill:#08427b,stroke:#052e56,color:#ffffff
  classDef internal fill:#1168bd,stroke:#0b4884,color:#ffffff
  classDef external fill:#8a8a8a,stroke:#5c5c5c,color:#ffffff
```

## Elements
| Element | Type | Technology | Responsibility |
| --- | --- | --- | --- |
| Customer developer | Person | — | Registers endpoints and inspects failed deliveries |
| Operations engineer | Person | — | Replays retained failures internally |
| Webhook delivery service | System | — | Delivers signed order events to customer endpoints |
| Order system | External system | — | Publishes order changes |
| Customer endpoint | External system | — | Receives events |

## Relationships
| From | To | Purpose | Protocol | Failure behaviour |
| --- | --- | --- | --- | --- |
| Customer developer | Webhook service | Manage endpoints and inspect deliveries | — | Developer sees an error; deliveries continue |
| Operations engineer | Webhook service | Replay retained failures | — | Operator sees an error; retained events remain available |
| Order system | Webhook service | Publish order changes | — | Events buffer upstream until the service consumes |
| Webhook service | Customer endpoint | Deliver events | — | Retry, then dead letter |

## Deferred to the next level
- Storage, queueing, retry scheduling, signing key management.

## Review history
The user rejected a draft that let customer developers request direct replay. The revised diagram retains endpoint registration and inspection, while replay is now an internal operational action deferred to Level 2. Awaiting approval of this revision.
