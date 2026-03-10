---
name: idea-brief
description: |
  Lock an ideation run into a single-source-of-truth brainstorm brief (`output/trace/IDEA_BRIEF.md`) and a replayable multi-query plan (`queries.md`).
  **Trigger**: idea brief, ideation brief, research ideas, brainstorm, 找 idea, 选题, 点子, 找方向.
  **Use when**: the user wants research ideas and their input is long / multi-turn; you need to clarify topic + constraints before retrieval.
  **Skip if**: the goal is to write a survey draft directly (use `arxiv-survey*` pipelines instead).
  **Network**: none.
  **Guardrail**: do not invent papers/citations; do not start retrieval here; keep the brief structured (no long prose).
---

# Idea Brief (SSOT for brainstorm ideation)

Goal: turn a fuzzy research-idea request into an auditable **brainstorm contract** that downstream steps can follow without drift.

This skill does **not** retrieve papers. It only locks:
- topic + audience + constraints + exclusions,
- the discussion rubric,
- the query buckets,
- the target artifact shape,
into `output/trace/IDEA_BRIEF.md` and `queries.md`.

The brief should also define the later ideation stack:
- each lead direction must be a distinct thesis line, not the same hidden-variable template with different nouns
- the final memo must expose explicit rank logic, quick kill criteria, and a paper-specific reading guide
- signal table
- direction pool
- screening table
- shortlist
- final brainstorm memo

## Inputs
- `GOAL.md`
- `DECISIONS.md`
- `queries.md`

## Outputs
- `output/trace/IDEA_BRIEF.md`
- `queries.md`
- `DECISIONS.md`

## Required sections
- Goal
- Scope
- Audience
- Constraints
- Exclusions
- Rubric
- Targets
- Focus lenses after C2
- Query buckets
- Table policy
- Open questions


## Execution notes

This skill starts from `GOAL.md`, then refines the topic/constraints into `output/trace/IDEA_BRIEF.md`, updates `queries.md`, and records blockers or approvals in `DECISIONS.md`.

## Script

### Quick Start

- `python .codex/skills/idea-brief/scripts/run.py --workspace <workspace_dir>`

### All Options

- `--workspace <dir>`
- `--unit-id <id>`
- `--inputs <a;b;...>`
- `--outputs <a;b;...>`
- `--checkpoint <C*>`

### Examples

- `python .codex/skills/idea-brief/scripts/run.py --workspace workspaces/<ws>`
