---
name: idea-opportunity-mapper
description: |
  Build an opportunity map for ideation by turning taxonomy clusters + paper notes into a table of unresolved gaps, evidence signals, and candidate wedges. Writes `output/IDEA_OPPORTUNITY_TABLE.md`.
  **Trigger**: opportunity map, idea gap table, ideation table, research gaps, 机会表, gap map, idea opportunities.
  **Use when**: you have a core set, a taxonomy, and paper notes, and need a table-first bridge from evidence to candidate ideas.
  **Skip if**: `output/IDEA_OPPORTUNITY_TABLE.md` already exists and is refined.
  **Network**: none.
  **Guardrail**: no invented papers or gaps; every row must point to existing `paper_id`s.
---

# Idea Opportunity Mapper

Goal: create a reusable, table-first artifact that answers:
- where the evidence is thin,
- what unresolved gap is still testable,
- which wedge could turn that gap into a bounded idea.

## Inputs
- `output/IDEA_BRIEF.md`
- `outline/taxonomy.yml`
- `papers/paper_notes.jsonl`
- `papers/core_set.csv`

## Outputs
- `output/IDEA_OPPORTUNITY_TABLE.md`
- optional sidecar: `output/IDEA_OPPORTUNITY_TABLE.jsonl`

## Contract
Each row should include:
- cluster
- gap type
- unresolved gap
- evidence signal
- why now
- candidate wedge
- `paper_id` pointers

This artifact is **NO PROSE** in spirit: short cells, strong evidence pointers, no essay paragraphs.
