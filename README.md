# Personal agent skills

[![skills.sh](https://skills.sh/b/bryanbarton525/skills)](https://skills.sh/bryanbarton525/skills)

Locally maintained skills for coding agents.

## Skills

| Skill | Purpose |
| --- | --- |
| [review-with-rules](skills/review-with-rules/SKILL.md) | Review PRs, branches, commits, and local changes with scoped REVIEW.md policy and verified findings. Create or update review policy when requested. |
| [golang-best-practices](skills/golang-best-practices/SKILL.md) | Develop Go components with meaningful interfaces, factories, observability, clear error and resource ownership, cohesive packages, behavioral testing, and measured optimization. |

## Install with skills.sh

Install the review skill globally for Codex:

```bash
npx skills add bryanbarton525/skills --skill review-with-rules --agent codex --global
```

Install the Go development skill:

```bash
npx skills add bryanbarton525/skills --skill golang-best-practices --agent codex --global
```

Omit `--global` to install into the current project. Omit `--agent codex` to choose another supported agent.

List available skills, or install interactively:

```bash
npx skills add bryanbarton525/skills --list
npx skills add bryanbarton525/skills
```

Manage CLI-installed skills with:

```bash
npx skills list --global
npx skills check
npx skills update review-with-rules
```

Invoke with `$review-with-rules`, or request a code review. It can review code without REVIEW.md; established repository policies add scoped rules and severity calibration.

Invoke `$golang-best-practices` for Go development. Its detailed references cover concurrency, resource lifetimes, API and configuration contracts, testing, and performance. Its [behavioral evaluation suite](skills/golang-best-practices/evals/README.md) includes ten scenarios; the staging script prepares isolated inputs without exposing grading criteria.

See the [skills CLI documentation](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) for installation and update options. Public leaderboard discovery is based on installations; a listing may not appear immediately.

## Local development

Clone this repository, then link the skill into Codex's skill directory:

```bash
git clone https://github.com/bryanbarton525/skills.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/skills/skills/review-with-rules" "${CODEX_HOME:-$HOME/.codex}/skills/review-with-rules"
```

The link command assumes the clone is named `skills` in the current directory. If a skill already exists at the destination, inspect and move it aside before linking.

This development link reads directly from the checkout. Use Git to update it; the CLI installation above manages its own installed copy.

## Maintain

Edit skills in this repository. Symlinked installations use the same files. Keep each skill in `skills/<name>/SKILL.md` with YAML `name` and `description` fields. Add supporting resources only when needed.
