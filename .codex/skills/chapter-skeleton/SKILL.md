---
name: chapter-skeleton
description: |
  Build a retrieval-informed chapter skeleton (`outline/chapter_skeleton.yml`) from taxonomy/core scope before stable H3 decomposition.
  **Trigger**: chapter skeleton, chapter-level outline, H2 skeleton, section-first survey, 章节骨架, 章级骨架.
  **Use when**: survey structure should stabilize chapter-level intent before subsection mapping and writing cards.
  **Skip if**: `outline/chapter_skeleton.yml` already exists and is refined.
  **Network**: none.
  **Guardrail**: NO PROSE; do not invent papers; keep output chapter-level only.
---

# Chapter Skeleton

## Load Order

Always read:
- `references/overview.md`

Use `scripts/run.py` only for deterministic materialization:
- load taxonomy / scope hints
- emit `outline/chapter_skeleton.yml`
- preserve existing non-placeholder user work

## Inputs

- `outline/taxonomy.yml`
- Optional: `GOAL.md`

## Outputs

- `outline/chapter_skeleton.yml`

## Asset contract

- `assets/output_contract.json`

## Script

### Quick Start

- `python .codex/skills/chapter-skeleton/scripts/run.py --workspace <workspace_dir>`
