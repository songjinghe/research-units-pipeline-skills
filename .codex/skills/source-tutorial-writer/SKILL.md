---
name: source-tutorial-writer
description: |
  Write a reader-first tutorial from approved source-grounded module packs.
  **Trigger**: source tutorial writer, tutorial drafting, 教程正文, 从资料写教程.
  **Use when**: `source-tutorial` 的 C3，`outline/tutorial_context_packs.jsonl` 和 `DECISIONS.md` 的 C2 批准都已就绪。
  **Skip if**: spec/module plan 还没批准，或 source packs 还没准备好。
  **Network**: none.
  **Guardrail**: 正文要以可读性和学习体验为主，但不能写出 sources 没支持的内容。
---

# Source Tutorial Writer

Goal: turn source-grounded module packs into one coherent tutorial.

The writer should treat `outline/tutorial_context_packs.jsonl` as the primary substrate, use `outline/module_plan.yml` for order/shape, and respect C2 approvals in `DECISIONS.md`.

## Inputs

- `outline/tutorial_context_packs.jsonl`
- `outline/module_plan.yml`
- `DECISIONS.md`

## Outputs

- `output/TUTORIAL.md`

## Required shape

- article-first tutorial
- clear reader orientation up front
- module-by-module flow
- concrete examples
- pitfalls/check-yourself moments
- module-end source notes

## Definition of Done

- `output/TUTORIAL.md` exists.
- Modules follow the approved order.
- Reader guidance is explicit.
- Source notes remain visible but lightweight.
