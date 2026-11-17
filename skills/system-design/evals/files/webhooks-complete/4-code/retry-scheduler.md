# Level 4: Code of Retry scheduler

Zooms into: [Retry scheduler](../3-components/dispatcher.md) · Status: approved 2026-11-14

```mermaid
stateDiagram-v2
  [*] --> pending
  pending --> sending: due
  sending --> delivered: 2xx
  sending --> pending: retryable failure, attempts < 12
  sending --> dead_lettered: attempts = 12 or 410 Gone
  dead_lettered --> pending: replay
  delivered --> [*]
```

Backoff: 30s doubling, capped at 1h, 12 attempts (about 8 hours total).

```go
type Scheduler interface {
    // Due returns up to limit deliveries whose next attempt time has passed.
    Due(ctx context.Context, limit int) ([]Delivery, error)
    // Record applies an attempt result and computes the next state.
    Record(ctx context.Context, id DeliveryID, result AttemptResult) error
}
```
