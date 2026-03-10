---
name: idea-brainstorm
version: 4.0
target_artifacts:
  - STATUS.md
  - UNITS.csv
  - CHECKPOINTS.md
  - DECISIONS.md
  - GOAL.md
  - queries.md
  - output/trace/IDEA_BRIEF.md
  - papers/papers_raw.jsonl
  - papers/papers_dedup.jsonl
  - papers/core_set.csv
  - papers/retrieval_report.md
  - outline/taxonomy.yml
  - papers/paper_notes.jsonl
  - papers/evidence_bank.jsonl
  - output/trace/IDEA_SIGNAL_TABLE.md
  - output/trace/IDEA_SIGNAL_TABLE.jsonl
  - output/trace/IDEA_DIRECTION_POOL.md
  - output/trace/IDEA_DIRECTION_POOL.jsonl
  - output/trace/IDEA_SCREENING_TABLE.md
  - output/trace/IDEA_SCREENING_TABLE.jsonl
  - output/trace/IDEA_SHORTLIST.md
  - output/trace/IDEA_SHORTLIST.jsonl
  - output/REPORT.md
  - output/APPENDIX.md
  - output/REPORT.json
  - output/DELIVERABLE_SELFLOOP_TODO.md
  - output/QUALITY_GATE.md
  - output/RUN_ERRORS.md
  - output/CONTRACT_REPORT.md
default_checkpoints: [C0,C1,C2,C3,C4,C5]
units_template: templates/UNITS.idea-brainstorm.csv
---

# Pipeline: research idea brainstorm (signals -> directions -> memo)

Goal: produce a **discussion-ready research-idea memo** for PI / PhD readers.

This pipeline is for “找 research idea / brainstorm / 选题 / 找方向”.
It is **not** for writing a survey draft and **not** for generating execution-grade project specs.

The terminal deliverable is a single default entrypoint:
- `output/REPORT.md`

That memo should feel like a mature brainstorm artifact:
- grounded in literature,
- small enough to discuss,
- clear about what is promising,
- honest about uncertainty,
- and rich enough to guide the next discussion round.

Artifact policy:
- Reader-facing terminal artifacts:
  - `output/REPORT.md`
  - `output/APPENDIX.md`
  - `output/REPORT.json`
- Trace artifacts stay under `output/trace/`.
- The run is only shareable when both layers exist and pass contract audit.

Default profile:
- Retrieval route: `literature-engineer`
- `core_size=100`
- Evidence mode: `abstract`
- Signal table: 10-20 rows
- Direction pool: 12-24
- Shortlist: 3-5
- Final memo lead directions: 3

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
- output/trace/IDEA_BRIEF.md

Notes:
- The brief is the single source of truth for topic, audience, constraints, exclusions, targets, and query buckets.
- Default behavior: block once at C0 for human approval of the brief before retrieval.

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
- Use multi-query buckets from `queries.md`.
- If recall is too low/noisy, fix it upstream and rerun C1.

## Stage 2 - Idea landscape / focus (C2) [NO PROSE]
required_skills:
- taxonomy-builder
- pipeline-router
- human-checkpoint
produces:
- outline/taxonomy.yml
- DECISIONS.md

human_checkpoint:
- approve: focus clusters / lenses + exclusions
- write_to: DECISIONS.md

Notes:
- Taxonomy is an idea landscape, not a paper outline.
- Default behavior: pause at C2 so the human can choose a few promising focus lenses.

## Stage 3 - Evidence signals (C3) [table-first]
required_skills:
- paper-notes
- idea-signal-mapper
produces:
- papers/paper_notes.jsonl
- papers/evidence_bank.jsonl
- output/trace/IDEA_SIGNAL_TABLE.md
- output/trace/IDEA_SIGNAL_TABLE.jsonl

Notes:
- The signal table should capture tensions, missing pieces, and academically meaningful axes rather than proposal-ready wedges.
- Keep this stage compact and table-first; no long prose.

## Stage 4 - Direction pool + screening (C4)
required_skills:
- idea-direction-generator
- idea-screener
produces:
- output/trace/IDEA_DIRECTION_POOL.md
- output/trace/IDEA_DIRECTION_POOL.jsonl
- output/trace/IDEA_SCREENING_TABLE.md
- output/trace/IDEA_SCREENING_TABLE.jsonl

Notes:
- Expansion should generate discussion-worthy research directions, not an operator cartesian product.
- Screening should score discussion value, distinctness, evidence grounding, and thesis potential.

## Stage 5 - Shortlist + memo synthesis + self-loop (C5)
required_skills:
- idea-shortlist-curator
- idea-memo-writer
- deliverable-selfloop
- artifact-contract-auditor
produces:
- output/trace/IDEA_SHORTLIST.md
- output/trace/IDEA_SHORTLIST.jsonl
- output/REPORT.md
- output/APPENDIX.md
- output/REPORT.json
- output/DELIVERABLE_SELFLOOP_TODO.md
- output/CONTRACT_REPORT.md

Notes:
- `output/trace/IDEA_SHORTLIST.md` is an internal convergence layer, not the user-facing final answer.
- `output/REPORT.md` is the terminal deliverable and should read like a discussion-ready research idea brainstorm memo.
- `deliverable-selfloop` should evaluate the full memo bundle plus its trace chain.
