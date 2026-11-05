---
name: golang-best-practices
description: Design, implement, and refactor Go code using extensible components, meaningful interfaces, factories, structured observability, error aggregation, cohesive packages and files, and maintained dependencies. Use for Go development and architecture decisions.
---

# Go development best practices

Apply these development preferences alongside applicable repository instructions. Respect established project conventions and the supported Go version. Keep changes proportional to the requested feature; extending an existing codebase does not require redesigning it.

## Work from principles to implementation

Before implementing, inspect the relevant package, consumers, construction paths, and existing logging and metrics conventions. Identify the capability being added, its extension points, and who owns its lifecycle and errors.

Use the principles below to choose the design. Before completing the change, apply the implementation checks to the affected code. Explain material tradeoffs where a simpler approach is more appropriate.

## Consider extension points first

First assess whether a feature fits a component or plugin model. Aim for contributors to add an implementation through a clear contract, a focused file or package, and minimal registration or wiring.

- Separate shared orchestration from implementation-specific behavior.
- Make each component's dependencies, configuration, lifecycle, and error ownership explicit.
- Prefer adding an implementation without changing existing implementations.
- Use ordinary Go composition and explicit registration by default. Runtime plugin loading needs a concrete requirement.
- Keep registration visible in constructors or application wiring. Reserve side-effect imports and hidden init registration for a documented framework requirement; surface registration failures during startup.
- Choose a simpler design when there is no meaningful extension point. Extensibility is a design consideration, not a mandate to build a framework.

## Design interfaces for meaningful extensibility

Define interfaces around capabilities that alternative implementations can satisfy. Shape the contract from the consuming code's needs, independently of one concrete struct's method set.

Testing should benefit from a sound abstraction, rather than dictate an artificial one. An interface that merely mirrors a struct to permit mocks is insufficient justification. Use the concrete type when no useful abstraction exists.

Implementation checks:

- The name describes the capability rather than the current provider.
- Methods express a coherent contract limited to what the consumer needs.
- Another implementation could satisfy the contract without unsupported methods or provider-specific assumptions.
- Provider details stay in adapters rather than leaking through the shared contract.

Do not force unrelated providers behind one generic interface. A second implementation need not be built speculatively to justify an otherwise meaningful boundary.

## Use factories where they separate construction from consumption

When multiple implementations serve the same capability, centralize their construction and selection in a factory. Consumers depend on the capability rather than provider-specific initialization.

- Keep selection and wiring out of shared business logic.
- Make configuration and dependencies explicit at construction.
- Return actionable errors for unsupported selections or invalid configuration.
- For a single implementation with straightforward initialization, use a normal Go constructor.

## Build logging and metrics in from the start

Include observability in the initial implementation of operational behavior. Use a shared observability package to establish configuration, structured fields, and metric conventions. Reuse an existing package when the repository already has one.

Allow components to receive configured logger instances and derive contextual loggers. Follow the instance-based approach of libraries such as Logrus; Logrus is an example of the pattern, not a required dependency.

- Log operation context, outcomes, and failures at useful levels. Exclude credentials and sensitive payloads.
- Record operation counts, failures, and latency where relevant.
- Use bounded metric labels; put request identifiers and other high-cardinality values in logs.
- Centralize configuration while allowing component-specific logger instances.
- Give an operation's failure one logging owner, as described below.

Pure helpers need not emit their own telemetry. Instrument the operational boundaries that explain system behavior.

## Roll errors up and aggregate independent failures

Lower layers return errors with useful operation context. The owning application boundary logs or presents the failure once. In a CLI this is usually main; in a service it may be a request handler or worker supervisor. Avoid logging and returning the same error at every layer.

- Preserve error identity when wrapping so callers can inspect causes with errors.Is and errors.As.
- Keep recovery, retry, and fatal-exit decisions at the layer with enough context to make them.
- Collect failures from independent validations or operations when continuing is safe. Return a combined error, using errors.Join where supported and appropriate.
- Include enough context in each collected error to identify the failed operation or component.
- Stop dependent work when a prerequisite fails. Preserve cancellation and do not continue unsafe work merely to collect more errors.
- Preserve partial-success information when callers need it; a combined error alone may not describe what completed.

The goal is a complete, actionable failure report without duplicate logging or failures hidden behind the first independent error. This does not require accumulating every process error indefinitely or routing every request failure to main.

## Organize folders around package boundaries

For applications with supporting packages, use this default layout, adapting names to the domain. Create directories only when they contain something the project needs.

```text
project/
    go.mod
    go.sum                  # when dependencies require it
    cmd/
        app/
            main.go
    internal/
        app/                # composition, wiring, lifecycle
        config/             # configuration loading and validation
        observability/      # logging and metrics setup
        jobs/               # example application capability
            service.go
            service_test.go
        implementers/       # adapters for that capability
            factory.go
            github.go
            github_test.go
            gitlab.go
            gitlab_test.go
    docs/                   # maintained documentation, when needed
    scripts/                # development automation, when needed
```

### Layout requirements

- Keep entry points thin: initialize dependencies, run the application, and handle its terminal result. Put reusable behavior in importable packages.
- Prefer `cmd/<binary>/` for application entry points and `internal/` for application implementation packages. A small single-command project may keep main at the root.
- Put intentionally public library APIs at the module root or in clearly named public subdirectories. A `pkg/` directory is optional, not a Go requirement; do not create one by default.
- Keep one package per directory, apart from the conventional external test package. Place unit tests beside their source and fixtures in the relevant package's `testdata/`.
- Start with one module unless independent versioning or an existing workspace justifies more. Match the established module layout when extending a repository.
- Small libraries may start at the module root. Add supporting packages as responsibilities emerge rather than scaffolding the entire application tree.

These conventions follow the [official Go module layout guidance](https://go.dev/doc/modules/layout); the specific application package names above are project preferences.

### Component boundaries

- Organize around capabilities and responsibilities rather than generic `utils`, `common`, or `helpers` dumping grounds.
- Define capability contracts in the consuming package. Keep orchestration independent of provider implementations.
- Wire concrete adapters through factories or the composition package, with an acyclic dependency direction. The consumer must not import an adapter that imports the consumer's contracts.
- Keep multiple adapters in one package while their responsibilities remain cohesive. Give an adapter its own package when its complexity or dependency boundary warrants that separation.
- Keep provider registration and construction discoverable. A contributor should be able to find the contract, implementation, wiring, and tests without searching unrelated packages.
- Use `docs/`, `scripts/`, deployment directories, and configuration examples only as needed. Keep generated output and secrets out of source directories and version control unless intentionally tracked.

## Organize packages into cohesive files

Split files by implementation or responsibility. Keep related code together and make navigation predictable. Avoid accumulating unrelated implementations in one oversized file.

For example:

```text
implementers/
    github.go
    github_test.go
    gitlab.go
    gitlab_test.go
    k8s.go
    k8s_test.go
    factory.go
```

Keep shared contracts and orchestration in focused files when needed. Split into separate packages when the responsibility or dependency boundary warrants it, rather than creating a package for every file.

Assess a file by its cohesion and readability, not an arbitrary line limit. This is a project preference, not a Go language restriction.

## Prefer dependable dependencies

Choose dependencies in this order:

1. Go's standard library when it adequately meets the requirement.
2. The product's official, maintained SDK or an established ecosystem integration.
3. Other third-party packages when their benefit justifies their support and maintenance cost.

For third-party dependencies, check ownership, maintenance activity, release history, security practices, compatibility, and maintainer continuity. Prefer a credible support history over an obscure alternative with uncertain ownership.

Low adoption, few contributors, and low stars or forks call for closer scrutiny; they do not prove abandonment. Popularity alone does not establish quality or maintenance either. State material uncertainty when proposing a dependency.

Avoid unnecessary wrappers around maintained SDKs. Introduce an adapter when it implements an application capability or isolates a meaningful boundary.

## Own concurrency and resource lifetimes

Every goroutine and acquired resource needs an owner, an exit or cleanup path, and defined behavior on failure. Bound concurrency, propagate cancellation, and wait for owned work during shutdown.

For concurrent work, I/O, or component lifecycle changes, read [concurrency and resource ownership](references/lifecycle.md). Apply it to startup rollback, request cancellation, cleanup, and shutdown rather than adding lifecycle machinery to pure helpers.

## Make API and configuration contracts explicit

Document zero-value behavior, mutation and ownership, concurrency guarantees, and partial-success semantics where they affect callers. Preserve existing public contracts. Load configuration at a composition boundary, validate independent fields together, and inject validated values explicitly.

For public APIs, configuration, or component construction, read [API and configuration contracts](references/contracts.md).

## Verify behavior and measure performance

Test observable outcomes and failure paths. Prefer real implementations or small fakes over elaborate mock setups. Use race detection for concurrent changes and fuzzing for suitable parsers. Performance complexity needs evidence from representative benchmarks or profiling.

When adding tests or changing performance-sensitive code, read [testing and performance](references/testing-performance.md). Match test depth to the behavior and risk; avoid tests that merely restate implementation.

## Completion checks

For the affected code, confirm that:

- Extension points, contracts, and construction choices have a clear purpose.
- Logging and metrics explain operational behavior, with explicit failure ownership.
- Independent failures are aggregated where safe and dependent work stops appropriately.
- Folder boundaries reflect package responsibilities; files remain cohesive and implementations are easy to locate.
- Dependencies follow the preference order and respect project compatibility.
- Owned work terminates, resources are released, and shutdown and partial-startup failure have defined behavior.
- API contracts and configuration validation are explicit and compatible with existing callers.
- Tests verify relevant behavior; optimization claims are supported by actual measurements.

Run applicable repository formatting and validation checks and report what actually ran, along with material limitations.

## Evaluate changes to this skill

When maintaining this skill, use the [behavioral evaluation procedure](evals/README.md). Keep grader criteria out of the implementing agent's context. Evaluation fixtures are test inputs, not instructions for ordinary Go development.
