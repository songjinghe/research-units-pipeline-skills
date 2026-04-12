---
name: module-source-coverage
description: |
  Audit whether every planned tutorial module is grounded in the ingested source set.
  **Trigger**: module coverage, source coverage, tutorial grounding, 模块覆盖, 来源覆盖.
  **Use when**: `source-tutorial` 的 C2，已有 `outline/module_plan.yml`，需要在 prose 前确认每个模块都能回指到来源。
  **Skip if**: module plan 还没定，或 source ingest 不完整。
  **Network**: none.
  **Guardrail**: 只做 coverage audit；不要在这里写教程 prose。
---

# Module Source Coverage

Goal: create an auditable module-to-source grounding file before tutorial prose starts.

The coverage audit should compare each module in `outline/module_plan.yml` against the usable sources surfaced by `sources/index.jsonl` and `sources/provenance.jsonl`.

## Inputs

- `outline/module_plan.yml`
- `sources/index.jsonl`
- `sources/provenance.jsonl`

## Outputs

- `outline/source_coverage.jsonl`

## Coverage rule

Every module should:
- map to at least one source ID, or
- explicitly record why the gap exists

## Definition of Done

- `outline/source_coverage.jsonl` exists.
- Every module in `outline/module_plan.yml` appears exactly once.
- Gaps are explicit, not silently ignored.
