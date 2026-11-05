# Concurrency and resource ownership

## Goroutine ownership

- Before starting a goroutine, identify who starts it, what stops it, and who waits for it. Request work belongs to the request; long-lived background work belongs to a component or application supervisor.
- Bound workers and queues. A semaphore acquired inside a newly spawned goroutine still permits unbounded goroutine creation; acquire capacity before spawning or use a fixed worker pool.
- Propagate the caller's context through cancellable work. Pass context as the first parameter, use it for request-scoped values rather than configuration, and release derived cancellation resources when finished.
- Check cancellation while scheduling and while blocking on channels or I/O. Already active callbacks must cooperate; context cancellation cannot forcibly stop arbitrary code.
- Define shutdown order: stop accepting work, signal cancellation or completion, wait for owned work, and release dependencies. Bound external shutdown waits when needed and report work that could not stop.
- Use synchronization for shared state. Make channel send, receive, and close ownership clear; closing a channel must not race with active senders.
- Select the synchronization mechanism for the responsibility. Use mutexes for shared state and channels for coordination where they simplify ownership. Do not introduce concurrency without useful independent work.

## Resources and partial startup

- The acquiring scope normally owns cleanup. If ownership transfers to the caller, say so in the API contract.
- Release files, connections, response bodies, and other acquired resources on success and failure. Place cleanup after successful acquisition and keep its scope appropriate; a defer inside a long loop can retain resources until the entire function returns.
- Close resources created internally. Leave injected shared clients, writers, and pools under the caller's ownership unless the contract explicitly transfers ownership.
- If constructing a later component fails, release resources already acquired during startup, usually in reverse dependency order. Preserve the primary failure and actionable cleanup failures.
- For HTTP, close response bodies on every response-handling path, inspect status explicitly, and bound reads when payload size is untrusted. Reuse clients and transports. Draining to enable reuse should not mean consuming an unlimited response.
- Distinguish flushing or commit failures that affect correctness from best-effort cleanup. Return meaningful failures to the owner rather than adding duplicate lower-layer logs.
- Keep library code free of process exits. Let the application finish cleanup before selecting an exit status; os.Exit does not run deferred functions.

Validate these properties with synchronization-based tests and controlled resources. A green race test only covers executed paths; it does not prove absence of deadlocks or leaks.

Authoritative references: [context](https://pkg.go.dev/context), [sync](https://pkg.go.dev/sync), [net/http](https://pkg.go.dev/net/http), and [race detector](https://go.dev/doc/articles/race_detector). Check APIs against the repository's Go version.
