---
name: section-briefs
description: |
  Build chapter-level briefs (`outline/section_briefs.jsonl`) from chapter skeleton plus section bindings before stable H3 decomposition.
  **Trigger**: section briefs, chapter planning cards, section-first briefs, 章节 brief, 章级 brief.
  **Use when**: section bindings exist and the run needs chapter-level rationale and decomposition guidance before emitting stable H3 ids.
  **Skip if**: `outline/section_briefs.jsonl` already exists and is refined.
  **Network**: none.
  **Guardrail**: NO PROSE; do not invent papers; emit planning constraints, not reader-facing text.
---

# Section Briefs

## Load Order

Always read:
- `references/overview.md`

Use `scripts/run.py` only for deterministic brief assembly.

## Inputs

- `outline/chapter_skeleton.yml`
- `outline/section_bindings.jsonl`
- Optional: `GOAL.md`

## Outputs

- `outline/section_briefs.jsonl`

## Asset contract

- `assets/output_contract.json`

## Script

### Quick Start

- `python .codex/skills/section-briefs/scripts/run.py --workspace <workspace_dir>`
