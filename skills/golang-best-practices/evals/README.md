# Behavioral evaluations

`evals.json` contains realistic development requests, starting files, and grader-only criteria. This is a local evaluation format, not a claim of compatibility with a particular evaluation framework.

## Run a case

1. Stage fresh inputs outside the skills repository with `python3 scripts/stage_eval.py` from the skill directory. Select cases with repeated `--case <id>` arguments, or omit them for all cases. The script creates workspaces, task prompts, instruction snapshots, references, and hashes; it excludes grader criteria. Empty `files` means start without a repository fixture.
2. Give a fresh coding agent only its staged `task.txt`, working directory, `SKILL.md`, and applicable staged references. Keep criteria, other cases, and prior conclusions out of its context. Restrict edits to its workspace and answer file; allow no external mutations or installs. For design-only cases, require an answer rather than generated code.
3. Preserve the agent's answer, diff, commands, and actual validation results. Do not use the agent's self-assessment as the grade.
4. Inspect the output against each criterion. Where applicable, run `go test ./...` and `go vet ./...` from the generated module, using an isolated cache if necessary. Assess behavior, imports, error identity, and package boundaries rather than matching exact filenames or wording.
5. Record each criterion as pass, fail, or blocked, with source locations or observed output. An untested claim does not pass a criterion. A blocked environment is not a model failure, but prevents claiming the case passed.

Use the same prompt, fixtures, model settings, and permissions for a baseline run without the skill. A single successful skill run establishes an example of compliance; it does not establish improvement over baseline. Repeat cases after instruction changes and retain failures as regression evidence.

## Scoring

Cases pass when all required criteria pass. Report individual failures rather than hiding them in an aggregate score. Also record compile or vet failures, scope expansion, prohibited external actions, and invented validation claims.

Use this result shape in a separate results directory outside the published skill:

```json
{
  "case_id": "interface-restraint",
  "skill_commit_or_hash": "sha256:...",
  "model": "actual model identifier",
  "mode": "with-skill",
  "status": "not-run",
  "criteria": [],
  "commands": [],
  "limitations": []
}
```

Record instruction hashes including referenced files when evaluating an uncommitted draft; the staging script records these in metadata.json. Status values are `not-run`, `pass`, `fail`, and `blocked`. Do not ship hypothetical results as completed evaluations.

## Coverage

| Case | Main behavior |
| --- | --- |
| interface-restraint | Avoid interfaces and factories created solely for tests |
| extensible-delivery | Capability contracts, factories, provider separation, and observability |
| error-rollup | Independent failure aggregation, prerequisite failure, and one logging owner |
| cohesive-layout | Split implementations while preserving public API and package boundaries |
| dependency-choice | Standard library and official SDK preference, evidence over popularity |
| public-library | Preserve public APIs instead of blindly imposing an application layout |
| bounded-runner | Bounded concurrency, cancellation, joined work, and deterministic tests |
| response-lifecycle | Response cleanup, bounded reads, injected resource ownership, and cancellation |
| configuration-contract | Missing versus empty inputs, aggregated validation, explicit injection, and secrets |
| testing-performance-plan | Deterministic tests, fuzz properties, compatible benchmarks, and evidence before optimization |
