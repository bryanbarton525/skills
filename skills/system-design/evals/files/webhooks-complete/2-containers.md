# Level 2: Containers

Zooms into: [Webhook delivery service](1-context.md) · Status: approved 2026-11-12

## Diagram
Containers of the webhook delivery service.

```mermaid
flowchart TB
  dev["Customer developer<br/>[Person]"]:::person
  kafka["orders.v1<br/>[External: Kafka topic]"]:::external
  cust["Customer endpoint<br/>[External system]"]:::external

  subgraph boundary["Webhook delivery service"]
    api["Endpoint API<br/>[Container: Go service]<br/>Endpoint CRUD, delivery log, replay"]:::internal
    dispatcher["Dispatcher<br/>[Container: Go worker]<br/>Consumes events, signs and sends deliveries"]:::internal
    db[("Webhook DB<br/>[Container: PostgreSQL]<br/>Endpoints, deliveries, dead letters")]:::internal
    kms["Signing keys<br/>[External: AWS KMS]"]:::external
  end

  dev -->|"Manages endpoints, replays [HTTPS/JSON]"| api
  api -->|"Reads and writes endpoints, enqueues replays [SQL]"| db
  kafka -->|"Order change events [Kafka]"| dispatcher
  dispatcher -->|"Loads endpoints, records deliveries [SQL]"| db
  dispatcher -->|"Fetches signing key [HTTPS]"| kms
  dispatcher -->|"POSTs signed event [HTTPS]"| cust

  classDef person fill:#08427b,stroke:#052e56,color:#ffffff
  classDef internal fill:#1168bd,stroke:#0b4884,color:#ffffff
  classDef external fill:#8a8a8a,stroke:#5c5c5c,color:#ffffff
```

## Relationships
| From | To | Purpose | Protocol | Failure behaviour |
| --- | --- | --- | --- | --- |
| Dispatcher | Customer endpoint | Deliver | HTTPS | Non-2xx or timeout schedules a retry |
| Dispatcher | Webhook DB | Record attempts | SQL | Dispatcher stops committing Kafka offsets |
