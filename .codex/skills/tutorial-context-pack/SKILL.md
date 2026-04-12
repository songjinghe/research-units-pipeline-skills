---
name: tutorial-context-pack
description: |
  Build writer-ready per-module context packs for source-tutorial drafting.
  **Trigger**: tutorial context pack, module pack, writer pack, 教程上下文包, 模块写作包.
  **Use when**: `source-tutorial` 的 C2，想把 module plan 和 source grounding 组织成稳定的写作输入。
  **Skip if**: module/source coverage 还没完成。
  **Network**: none.
  **Guardrail**: 只整理上下文，不直接写教程正文。
---

# Tutorial Context Pack

Goal: combine module plan, source coverage, and provenance snippets into one deterministic pack per module.

The pack builder should pull module structure from `outline/module_plan.yml`, grounding from `outline/source_coverage.jsonl`, and concrete source pointers from `sources/provenance.jsonl`.

## Inputs

- `outline/module_plan.yml`
- `outline/source_coverage.jsonl`
- `sources/provenance.jsonl`

## Outputs

- `outline/tutorial_context_packs.jsonl`

## Suggested fields

- `module_id`
- `title`
- `objective`
- `core_concepts`
- `worked_example_candidates`
- `pitfalls`
- `exercise_seed`
- `source_snippets`

## Definition of Done

- One pack per module.
- Packs mention actual source IDs/snippets.
- Packs are prose-ready but not reader-facing prose.
