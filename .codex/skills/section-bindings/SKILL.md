---
name: section-bindings
description: |
  Bind papers to chapter-level sections first, writing `outline/section_bindings.jsonl` and `outline/section_binding_report.md`.
  **Trigger**: section bindings, chapter bindings, section-first binding, 章节绑定, 章级绑定.
  **Use when**: survey structure should measure chapter saturation before stable H3 decomposition.
  **Skip if**: chapter skeleton is missing or the bindings are already refined.
  **Network**: none.
  **Guardrail**: NO PROSE; do not invent papers; produce auditable PASS/BLOCKED/REROUTE signals.
---

# Section Bindings

## Load Order

Always read:
- `references/overview.md`

Use `scripts/run.py` only for deterministic binding and report materialization.

## Inputs

- `papers/core_set.csv`
- `outline/chapter_skeleton.yml`
- Optional: `papers/papers_dedup.jsonl`

## Outputs

- `outline/section_bindings.jsonl`
- `outline/section_binding_report.md`

## Asset contract

- `assets/output_contract.json`

## Script

### Quick Start

- `python .codex/skills/section-bindings/scripts/run.py --workspace <workspace_dir>`
