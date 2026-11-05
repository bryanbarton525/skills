# API and configuration contracts

## Public and component APIs

- Export the smallest coherent capability. Document caller-visible behavior: zero-value usability, nil handling where relevant, mutation, resource ownership, cancellation, concurrency safety, and partial success.
- Choose receiver and return types deliberately. Copying a value containing a used mutex is unsafe; returning an interface containing a typed nil pointer does not return a nil interface.
- Make constructors validate invariants and return actionable errors. A zero value may be useful or may require initialization; document the actual contract rather than promising both.
- State whether returned slices or maps alias internal state. Copy when isolation is part of the contract; avoid defensive copies without a reason.
- Preserve existing signatures and semantics when extending public APIs. An exported helper's previous acceptance of a value is not permission to tighten it incidentally while adding another function.
- Exposing a wrapped dependency error may make it part of the API. Preserve causes needed by callers while choosing deliberately which implementation details become contractual.

## Configuration and construction

- Load files, environment variables, and flags at an application or composition boundary; define their precedence explicitly. Inject validated configuration into components instead of reading environment variables throughout the codebase.
- Distinguish missing values, explicitly empty values, and invalid values where the configuration format requires it. Document defaults and apply only those the contract establishes.
- Aggregate independent parsing and validation failures with field names before starting side effects. Stop dependent validation when a prerequisite is unavailable, without hiding unrelated failures.
- Keep credentials out of error messages, configuration dumps, and logs. Describe the field and requirement rather than reproducing its secret value.
- Register providers explicitly during construction or wiring. Validate duplicates and unsupported selections when applicable; avoid mutable package globals or init side effects as the default registration mechanism.
- Keep configuration read-only after startup unless reload behavior, synchronization, validation, and failure recovery are designed explicitly.

Reference: [Go code review comments](https://go.dev/wiki/CodeReviewComments). These configuration and construction rules express this skill's project preferences, rather than a mandatory Go framework.
