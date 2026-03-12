# research-units-pipeline: repo-global note

This file is intentionally minimal.

## Why this file still exists

- It is currently used as a repo-root marker by local tooling.
- Do not delete or rename it until repo-root discovery is migrated away from `AGENTS.md`.

## Canonical contracts live elsewhere

- Workflow execution contracts live in `pipelines/*.pipeline.md`.
- UNITS/checkpoint conventions live in `templates/UNITS.*.csv`, `templates/units.schema.md`, and `SKILLS_STANDARD.md`.
- Skill-specific behavior lives in `.codex/skills/<skill>/SKILL.md`.

## Repo-global working rules

- Keep generated run artifacts under `workspaces/<name>/`; do not scatter workspace outputs in the repo root.
- Prefer repo skills under `.codex/skills/`; if a capability is missing, add or refactor a skill instead of doing the work ad hoc.
- For executable pipelines, follow the pipeline's artifact contract, checkpoint contract, and approval flow rather than restating them here.
