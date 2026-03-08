---
name: idea-top3-expander
description: |
  Expand the strongest shortlisted ideas into a more proposal-like report, writing `output/IDEA_TOP3_REPORT.md`.
  **Trigger**: idea top3, top3 report, expand ideas, mini proposals, proposal cards, top ideas, 前三选题, idea report.
  **Use when**: the shortlist exists but still feels too thin to support execution or advisor discussion.
  **Skip if**: you only need a shortlist and do not want proposal-style detail.
  **Network**: none.
  **Guardrail**: do not invent papers; all expanded ideas must remain anchored to the current shortlist and core set.
---

# Idea Top3 Expander

Goal: turn a shortlist into something that actually feels like research ideas.

## Inputs
- `output/IDEA_BRIEF.md`
- `output/IDEA_SHORTLIST.md`
- `output/IDEA_SCREENING_TABLE.md`
- `output/IDEA_OPPORTUNITY_TABLE.md`
- `papers/paper_notes.jsonl`
- `papers/core_set.csv`

## Outputs
- `output/IDEA_TOP3_REPORT.md`

## Required fields per top idea
- why now
- sharp gap
- concrete testbed
- minimal artifact
- strong positive signal
- interesting negative result
- main confound
- kill criterion
- closest prior work
- evidence hooks
