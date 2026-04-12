---
name: source-tutorial-spec
description: |
  Define a tutorial spec from ingested sources rather than from a bare topic prompt.
  **Trigger**: source tutorial spec, tutorial from sources, learner profile, 教程规格, 从资料生成教程.
  **Use when**: `source-tutorial` 的 C2，需要根据已 ingest 的 sources 锁定 audience、prerequisites、objectives、non-goals 和 running example 策略。
  **Skip if**: 还没有完成 source ingest，或 spec 已被人工批准且不允许改动。
  **Network**: none.
  **Guardrail**: 不要发明 sources 没支持的内容；如果 running example 不稳，就明确写“无统一 running example”。
---

# Source Tutorial Spec

Goal: write a tutorial scope contract grounded in the ingested source corpus.

The spec should explicitly read `sources/index.jsonl` and `sources/provenance.jsonl`, then use `GOAL.md` and `DECISIONS.md` only as framing constraints.

## Inputs

- `sources/index.jsonl`
- `sources/provenance.jsonl`
- `GOAL.md`
- `DECISIONS.md`

## Outputs

- `output/TUTORIAL_SPEC.md`

## Required sections

- Audience
- Prerequisites
- Learning objectives
- Non-goals
- Source scope
- Running example policy
- Delivery shape

## Definition of Done

- `output/TUTORIAL_SPEC.md` is structured, not long prose.
- Objectives are measurable.
- Source scope names the actual source families being used.
- Running example is either concrete or explicitly omitted for lack of support.
