---
name: idea-finder
version: 3.1
target_artifacts:
  - STATUS.md
  - UNITS.csv
  - CHECKPOINTS.md
  - DECISIONS.md
  - GOAL.md
  - queries.md
  - output/IDEA_BRIEF.md
  - papers/papers_raw.jsonl
  - papers/papers_dedup.jsonl
  - papers/core_set.csv
  - papers/retrieval_report.md
  - outline/taxonomy.yml
  - papers/paper_notes.jsonl
  - papers/evidence_bank.jsonl
  - output/IDEA_OPPORTUNITY_TABLE.md
  - output/IDEA_OPPORTUNITY_TABLE.jsonl
  - output/IDEA_POOL.md
  - output/IDEA_POOL.jsonl
  - output/IDEA_SCREENING_TABLE.md
  - output/IDEA_SCREENING_TABLE.jsonl
  - output/IDEA_SHORTLIST.md
  - output/IDEA_SHORTLIST.jsonl
  - output/IDEA_TOP3_REPORT.md
  - output/DELIVERABLE_SELFLOOP_TODO.md
  - output/QUALITY_GATE.md
  - output/RUN_ERRORS.md
  - output/CONTRACT_REPORT.md
default_checkpoints: [C0,C1,C2,C3,C4,C5]
units_template: templates/UNITS.idea-finder.csv
---

# Pipeline: research ideation (table-first -> shortlist -> top-3 report)

Goal: produce a **research-idea deliverable stack** that separates:
- **evidence and gap mapping**,
- **large-pool expansion**,
- **table-based screening and convergence**,
- **proposal-like expansion of the strongest ideas**.

This pipeline is designed for “找 research idea / brainstorm / 选题 / 找方向”, not for writing a full survey paper.

Artifact policy:
- Reader-facing artifacts live in Markdown (`*.md`).
- Audit / replay sidecars live in paired `*.jsonl` files for the modular ideation stages.
- The full run is only considered shareable when both layers are present and pass contract audit.

Default profile (Lite+):
- Retrieval route: `literature-engineer` (multi-route recall)
- `core_size=100`
- Idea Pool: 60–80
- Screened candidates: 12–18
- Final shortlist: 5–7
- Top-3 report: 3
- Evidence mode: `abstract` (no fulltext download by default)

## Stage 0 - Init + idea brief (C0)
required_skills:
- workspace-init
- pipeline-router
- idea-brief
- human-checkpoint
produces:
- STATUS.md
- UNITS.csv
- CHECKPOINTS.md
- DECISIONS.md
- GOAL.md
- queries.md
- output/IDEA_BRIEF.md

Notes:
- The brief (`output/IDEA_BRIEF.md`) is the single source of truth for scope, constraints, rubric, and artifact policy.
- The pipeline should **block once** at C0 for human approval of the brief before retrieval.

## Stage 1 - Retrieval + core set (C1)
required_skills:
- literature-engineer
- dedupe-rank
produces:
- papers/papers_raw.jsonl
- papers/papers_dedup.jsonl
- papers/core_set.csv
- papers/retrieval_report.md

Notes:
- Use multi-query buckets from `queries.md` (not a single giant query).
- If recall is too low/noisy, fix it upstream (rewrite buckets + exclusions) and rerun C1.

## Stage 2 - Idea map / focus (C2) [NO PROSE]
required_skills:
- taxonomy-builder
- pipeline-router
- human-checkpoint
produces:
- outline/taxonomy.yml
- DECISIONS.md

human_checkpoint:
- approve: focus clusters + exclusions (based on `outline/taxonomy.yml`)
- write_to: DECISIONS.md

Notes:
- Taxonomy is used as an **idea map**, not a paper outline.
- Default behavior: pause at C2 so the human can pick 1–2 focus clusters and hard excludes.

## Stage 3 - Evidence substrate + opportunity map (C3) [table-first]
required_skills:
- paper-notes
- idea-opportunity-mapper
produces:
- papers/paper_notes.jsonl
- papers/evidence_bank.jsonl
- output/IDEA_OPPORTUNITY_TABLE.md
- output/IDEA_OPPORTUNITY_TABLE.jsonl

Notes:
- Notes must include limitations / failure modes.
- The opportunity table is the bridge from paper evidence to idea wedges.
- This stage should remain compact and table-first; no long prose.
- The JSONL sidecar should preserve row-level fields so downstream expansion and audits do not rely on Markdown parsing.

## Stage 4 - Expansion + screening (C4)
required_skills:
- idea-pool-expander
- idea-screener
produces:
- output/IDEA_POOL.md
- output/IDEA_POOL.jsonl
- output/IDEA_SCREENING_TABLE.md
- output/IDEA_SCREENING_TABLE.jsonl

Notes:
- Expansion should be broad, operator-driven, and still evidence-anchored.
- Screening should happen in tables first, before writing the shortlist.
- Tables should carry the main analytic load at this stage.
- Sidecars should make the pool and the screening decisions replayable without re-reading the free-form Markdown.

## Stage 5 - Shortlist + top-3 report + self-loop (C5)
required_skills:
- idea-shortlist-curator
- idea-top3-expander
- deliverable-selfloop
- artifact-contract-auditor
produces:
- output/IDEA_SHORTLIST.md
- output/IDEA_SHORTLIST.jsonl
- output/IDEA_TOP3_REPORT.md
- output/DELIVERABLE_SELFLOOP_TODO.md
- output/CONTRACT_REPORT.md

Notes:
- `IDEA_SHORTLIST.md` is no longer the whole ideation stack; it is the converged shortlist layer.
- `IDEA_TOP3_REPORT.md` is the first artifact that should feel like real research ideas rather than screening cards.
- `deliverable-selfloop` should evaluate the full ideation stack, not only the shortlist file.
- The final contract audit should verify both the reader-facing artifacts and the replayable sidecars.
