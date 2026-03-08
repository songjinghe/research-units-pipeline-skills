---
name: idea-screener
description: |
  Score and screen brainstorm candidates into a compact comparison table before shortlist curation. Writes `output/IDEA_SCREENING_TABLE.md`.
  **Trigger**: idea screener, screening table, score ideas, shortlist table, screening matrix, 筛题表, 评分表.
  **Use when**: you already have an opportunity map and an idea pool, and want table-based convergence before writing the shortlist.
  **Skip if**: `output/IDEA_SCREENING_TABLE.md` already exists and is refined.
  **Network**: none.
  **Guardrail**: do not invent evidence; scores must be traceable to current cards and brief constraints.
---

# Idea Screener

Goal: move convergence out of prose and into a comparison table.

## Inputs
- `output/IDEA_BRIEF.md`
- `output/IDEA_POOL.md`
- `output/IDEA_OPPORTUNITY_TABLE.md`
- `outline/taxonomy.yml`

## Outputs
- `output/IDEA_SCREENING_TABLE.md`
- optional sidecar: `output/IDEA_SCREENING_TABLE.jsonl`

## Table columns
- idea id
- cluster
- idea type
- operator
- feasibility
- novelty delta
- evidence traceability
- evaluation clarity
- writeability
- total score
- keep / maybe / drop
- rationale
