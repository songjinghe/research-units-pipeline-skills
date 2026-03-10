# Idea Shortlist Curator — Overview

## Job

Take a screened direction pool and produce a small (3–5) ranked shortlist that is ready for advisor-level discussion.

## Selection algorithm

The script uses a two-pass diversity-aware greedy selection:

1. **Diversity pass**: pick the first N directions (default 3) that maximize cluster/type/program_kind diversity. Each new pick must introduce at least one unseen attribute.
2. **Score pass**: fill remaining slots by descending total_score, skipping already-selected directions.

This prevents the shortlist from collapsing into one cluster even when that cluster dominates the screening scores.

## Ranking rationale

Each direction gets an explicit `why_this_ranks_here` string:

- **#1**: frames why this direction offers the fastest decisive result and clearest thesis-sized contribution.
- **#2**: frames what makes it slower or harder to defend than #1, while noting the payoff is still thesis-sized.
- **#3+**: frames the distinct wedge it opens, noting the risk and time-to-clarity relative to the top two.

Deferred directions (outside the lead set) get a `why_not_prioritized` reason:
- overlapping program wedge with a lead
- cluster already represented
- evidence anchor too abstract
- slower path to a decisive cycle

## When to load reference files

- Read this file first to understand the selection and ranking model.
- Read `ranking_rubric.md` when you need to override or refine the ranking reasons (e.g., the canned phrases feel too uniform for a specific domain).
