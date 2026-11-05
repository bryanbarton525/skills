# Behavioral testing and performance evidence

## Test the contract

- Cover relevant success, boundary, failure, cancellation, and partial-success behavior. For a bug, add a regression test that fails because of the bug and passes after the fix.
- Use tables when cases share a setup and assertion structure; use focused tests when scenarios differ. Test public behavior rather than private call order or internal helper names.
- Prefer real in-memory implementations, temporary files, and in-process servers where practical. Use small fakes for genuine capability boundaries and controlled failures. Avoid adding interfaces solely to satisfy a mocking framework.
- Keep tests deterministic. Coordinate goroutines with channels or other synchronization; use timeouts as failure bounds rather than sleeps to assume progress.
- Use t.TempDir, t.Cleanup, and equivalent scoped cleanup where supported. Parallel tests must not mutate shared environment, logger globals, or shared fixtures unsafely.
- Use fuzzing for parsers and transformations with meaningful properties: no panic, round-trip behavior when defined, or preservation of invariants. Seed valid and malformed cases; correctness must not depend on arbitrary fuzz duration.

## Choose and report checks

- Respect repository test commands, build tags, platform assumptions, and the declared toolchain. Run affected package tests first; broaden to consumers or the module when the change warrants it.
- Run go vet and formatting checks as appropriate, and go test -race for changed concurrent behavior when supported. Existing lint configuration is the source of truth; do not add a new lint stack incidentally.
- Report commands, outcomes, and blocked checks accurately. Coverage percentage alone is not a quality target, and a passing test does not certify unexercised behavior.

## Measure before optimizing

- Identify the workload, bottleneck hypothesis, and useful metric before optimizing. Use representative benchmarks and pprof profiles where needed.
- Preserve an unmodified baseline and measure candidate changes under comparable inputs and environment. Report time, allocations, and variance where relevant; distinguish a hypothesis from an observed improvement.
- Keep benchmark setup outside the measured region as appropriate and ensure work is actually consumed. Use benchmark APIs supported by the project's Go version.
- Prefer straightforward algorithms and standard-library implementations until evidence justifies more complexity. Pools, unsafe, reflection tricks, caching, and extra goroutines need a concrete benefit and clear ownership.
- Retain behavior checks alongside benchmarks. A faster implementation with changed semantics is not a valid improvement.

References: [testing](https://pkg.go.dev/testing), [fuzzing](https://go.dev/doc/security/fuzz/), and [diagnostics and profiling](https://go.dev/doc/diagnostics).
