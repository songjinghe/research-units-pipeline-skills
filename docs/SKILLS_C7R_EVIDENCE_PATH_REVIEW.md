# C7R Evidence Path Review

## Scope

Unit: `U026`

Goal:
- normalize earlier milestone evidence references into durable, clickable repo/workspace paths
- reduce ambiguity where repo-level status logs referenced only generic completion statements or shell-only history
- keep contract-level artifact names distinct from instance-level evidence paths

## Review method

Reviewed sources:
- `STATUS.md`
- `UNITS.csv`
- earlier review docs under `docs/`
- durable artifacts under `workspaces/idea-brainstorm/`

Normalization rule:
- contract docs may keep generic artifact names such as `output/REPORT.md`
- repo-level milestone evidence should point to concrete workspace or doc artifacts when available
- where historical evidence only existed in shell output, document the limitation explicitly rather than rewriting history

## Crosswalk

### C1 - Pipeline contract rebuilt
- Claim location: `STATUS.md`
- Durable evidence:
  - `pipelines/idea-brainstorm.pipeline.md`
  - `templates/UNITS.idea-brainstorm.csv`
- Notes:
  - these are contract artifacts, not run outputs

### C4 - Validation
- Claim location: `STATUS.md`, `UNITS.csv:6`
- Strongest durable evidence now available:
  - `workspaces/idea-brainstorm/llm-agent-ideas-20260309/output/REPORT.md`
  - `workspaces/idea-brainstorm/llm-agent-ideas-20260309/output/APPENDIX.md`
  - `workspaces/idea-brainstorm/llm-agent-ideas-20260309/output/REPORT.json`
  - `workspaces/idea-brainstorm/llm-agent-ideas-20260309/output/REPORT_PANEL_REVIEW.md`
- Caveat:
  - `U005` was historically recorded as `validation output in shell`; this review normalizes the evidence path with the strongest surviving durable artifacts instead of mutating that historical acceptance text

### C4R - Ideation content-thickening pass
- Claim location: `STATUS.md`, `UNITS.csv:28`, `UNITS.csv:29`
- Durable evidence:
  - `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun/output/RERUN_COMPARISON.md`
  - `workspaces/idea-brainstorm/llm-agent-ideas-20260309-skillpatch-smoke/output/REPORT.md`
  - `workspaces/idea-brainstorm/llm-agent-ideas-20260309-skillpatch-smoke/output/APPENDIX.md`
  - `workspaces/idea-brainstorm/llm-agent-ideas-20260309-skillpatch-smoke/output/DELIVERABLE_SELFLOOP_TODO.md`
  - `workspaces/idea-brainstorm/llm-agent-ideas-20260309-skillpatch-smoke/output/CONTRACT_REPORT.md`

### C5 - Phase 0 foundations
- Claim location: `STATUS.md`, `CHECKPOINTS.md`
- Durable evidence:
  - `docs/SKILLS_PHASE0_REVIEW.md`
  - `docs/SKILLS_PHASE0_VALIDATE_REPO.md`
  - `scripts/audit_skills.py`
  - `docs/SKILL_AUDIT_RULES.md`
  - `.codex/skills/_template_reference_first/SKILL.md`
  - `SKILLS_STANDARD.md`
  - `SKILL_INDEX.md`

### C6 - First P0 kickoff
- Claim location: `STATUS.md`, `CHECKPOINTS.md`
- Durable evidence:
  - `docs/FRONT_MATTER_P0_KICKOFF_REVIEW.md`
  - `.codex/skills/front-matter-writer/assets/front_matter_context.schema.json`
  - `.codex/skills/front-matter-writer/SKILL.md`
- Caveat:
  - the original smoke note referenced a temporary copy rather than a named preserved workspace

### C7 - Remaining P0 writer/planner batch
- Claim location: `STATUS.md`, `CHECKPOINTS.md`
- Durable evidence:
  - `docs/SKILLS_P0_WRITER_BATCH_REVIEW.md`
  - `docs/SKILLS_P0_VALIDATE_REPO.md`
  - `.codex/skills/subsection-writer/SKILL.md`
  - `.codex/skills/chapter-lead-writer/SKILL.md`
  - `.codex/skills/subsection-briefs/SKILL.md`
  - `.codex/skills/taxonomy-builder/SKILL.md`

## Outcome

This remediation does not claim that every earlier milestone had a perfect original audit trail.

It does make the repo-level evidence chain more explicit by:
- pointing `STATUS.md` to durable proof where available
- preserving historical caveats where evidence was originally shell-only or temporary
- separating generic contract references from concrete workspace evidence
