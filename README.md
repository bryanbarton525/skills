# Personal agent skills

Locally maintained skills for coding agents.

## Skills

| Skill | Purpose |
| --- | --- |
| [review-with-rules](skills/review-with-rules/SKILL.md) | Review PRs, branches, commits, and local changes with scoped REVIEW.md policy and verified findings. Create or update review policy when requested. |

## Install for Codex

Clone this repository, then link the skill into Codex's skill directory:

```bash
git clone https://github.com/bryanbarton525/skills.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/skills/skills/review-with-rules" "${CODEX_HOME:-$HOME/.codex}/skills/review-with-rules"
```

The link command assumes the clone is named `skills` in the current directory. If a skill already exists at the destination, inspect and move it aside before linking.

Invoke with `$review-with-rules`, or request a code review. It can review code without REVIEW.md; established repository policies add scoped rules and severity calibration.

## Maintain

Edit skills in this repository. Symlinked installations use the same files. Keep each skill in `skills/<name>/SKILL.md` with YAML `name` and `description` fields. Add supporting resources only when needed.
