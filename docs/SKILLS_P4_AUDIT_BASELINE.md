# Phase 4 Audit Baseline

Date: 2026-03-10

## Purpose

Record the pre-Phase-4 state of both audit tools so fixes can be verified against this baseline.

## audit_skills.py Summary

- Skills scanned: 85
- Files scanned: 240
- Total findings: 261 (WARN=79, INFO=182)
- By rule:
  - `reader_faced_ellipsis`: 240 (mostly INFO; WARNs are in script string templates for truncation — not actual reader leakage)
  - `generic_domain_hardcoding`: 20 (all in `assets/domain_packs/llm_agents.json` or `agent-survey-corpus` — intentional domain-specific content in the correct location)
  - `script_heavy_without_references`: 1 (`idea-shortlist-curator`)

### Accepted WARNs (not targeted for fix)

- `generic_domain_hardcoding` in `assets/domain_packs/*.json` and `references/domain_pack_overview.md`: these files ARE the externalized domain packs; having "LLM Agents" there is correct by design.
- `agent-survey-corpus` domain hardcoding: this skill is domain-specific by purpose ("Download agent survey PDFs").
- `reader_faced_ellipsis` in script string templates used for truncation (e.g., `" ..."` for long lists): these are internal report formatting, not reader-facing artifact leakage.

### Targeted for fix

- `script_heavy_without_references`: `idea-shortlist-curator` → U032

## validate_repo.py Summary

- Errors: 4
- Warnings: 8
- Info: 7

### Errors (targeted for fix → U030)

All 4 errors in `deliverable-selfloop/SKILL.md`:
- declared input `output/trace/IDEA_DIRECTION_POOL.md` not referenced outside Inputs section
- declared input `output/trace/IDEA_SCREENING_TABLE.md` not referenced outside Inputs section
- declared input `output/trace/IDEA_SHORTLIST.md` not referenced outside Inputs section
- declared input `output/trace/IDEA_SIGNAL_TABLE.md` not referenced outside Inputs section

### Warnings (targeted for fix → U031)

8 skills with `scripts/run.py` but missing `### Quick Start`/`### All Options`/`### Examples`:
- idea-direction-generator
- idea-memo-writer
- idea-screener
- idea-shortlist-curator
- idea-signal-mapper
- opener-variator
- paragraph-curator
- style-harmonizer

### Info (no action needed)

7 pipelines report LLM-first skills without scripts — this is expected/correct.
