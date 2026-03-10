# Survey Visuals — Reference-First Overview

## Purpose

This skill creates non-prose visual artifacts (timeline, figure specs) grounded in
evidence and citations. These artifacts help writers avoid template-like figures.

## Load Order

Always read:
- `references/overview.md` (this file) — orientation
- `references/figure_archetypes.md` — common figure shapes for surveys (pipeline, taxonomy, comparison)

Read by task:
- `references/timeline_patterns.md` — how to pick milestones and avoid year-list dumps

Machine-readable assets:
- `assets/figure_templates.yaml` — figure archetype specifications (extensible)

## Script Boundary

Use `scripts/run.py` only for:
- deterministic assembly of timeline bullets from paper_notes year + bibkey
- deterministic table generation from outline + mapping + notes
- figure spec skeleton generation using `assets/figure_templates.yaml`

Do not treat `run.py` as the place for:
- figure narratives or prose explanations
- hardcoded figure descriptions that should be in templates
- milestone selection heuristics that belong in references
