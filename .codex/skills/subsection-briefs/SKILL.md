---
name: subsection-briefs
description: |
  Build per-subsection writing briefs (NO PROSE) so later drafting is driven by evidence and checkable comparison axes (not outline placeholders).
  **Trigger**: subsection briefs, writing cards, intent cards, H3 briefs, scope_rule, axes, clusters, 写作意图卡, 小节卡片, 段落计划.
  **Use when**: `outline/outline.yml` + `outline/mapping.tsv` + `papers/paper_notes.jsonl` exist and you want section-by-section drafting without template leakage.
  **Skip if**: `outline/subsection_briefs.jsonl` already exists and is refined (no placeholders/ellipsis; axes+clusters+paragraph_plan are filled).
  **Network**: none.
  **Guardrail**: NO PROSE; do not invent papers; only reference `paper_id`/`bibkey` that exist in `papers/paper_notes.jsonl`.
---

# Subsection Briefs

Build deterministic H3 brief cards from outline + mapping + paper notes.

Compatibility mode is active: this skill keeps the current `outline/subsection_briefs.jsonl` field contract and paragraph-plan shape while moving phrase/domain logic into `references/` and `assets/`.

## Quick Use

- Run `scripts/run.py` as the deterministic materializer.
- Keep the output NO PROSE: subsection-scoped plans, axes, clusters, and bridge handles only.
- Preserve current downstream compatibility for `transition-weaver`, `writer-context-pack`, and `subsection-writer`.

## Load Order

Always read:
- `references/overview.md`

Read by task:
- If `thesis` feels repetitive or copyable, read `references/thesis_patterns.md`.
- If `tension_statement` is too generic, read `references/tension_patterns.md`.
- If axes are weak or domain-biased, read `references/axis_catalog_generic.md` and `references/axis_catalog_llm_agents.md`.
- If transition handles feel bland, read `references/bridge_terms.md`.
- For calibration, read `references/examples_good.md`.

Machine-readable assets:

- `assets/phrase_packs/thesis_patterns.json`
- `assets/phrase_packs/bridge_contrast.json`
- `assets/domain_packs/generic.json`
- `assets/domain_packs/llm_agents.json`
- `assets/domain_packs/text_to_image.json`

The script loads these packs first; patch them before changing Python when the issue is phrasing, domain routing, or axis inventory.

## Inputs

- `outline/outline.yml`
- `outline/mapping.tsv`
- `papers/paper_notes.jsonl`
- Optional: `GOAL.md`
- Optional: `outline/claim_evidence_matrix.md`

## Output

- `outline/subsection_briefs.jsonl`

Required record shape remains compatibility-preserving:

- identity: `sub_id`, `title`, `section_id`, `section_title`
- planning core: `rq`, `thesis`, `scope_rule`, `axes`, `bridge_terms`, `contrast_hook`, `tension_statement`
- evidence hooks: `evaluation_anchor_minimal`, `required_evidence_fields`, `clusters`
- execution plan: `paragraph_plan`, `evidence_level_summary`, `generated_at`

## What `run.py` Should Do

- Read outline, mapping, and notes.
- Normalize subsection seeds from outline bullets.
- Load thesis/tension/domain-axis packs from `assets/`.
- Produce stable JSONL records with the existing contract.

## What `run.py` Should Not Do

- Do not invent papers, citations, or claims.
- Do not emit reader-facing narrative prose.
- Do not hardcode domain-specific sentence templates when an asset pack can hold them.

## Block / Reroute

- If outline, mapping, or notes are missing, stop.
- If evidence is thin, keep `thesis`/`tension_statement` conservative and let downstream evidence skills strengthen the subsection.
- Do not “fix” thin evidence by inventing more specific axes or stronger claims.


## Execution notes

When running in compatibility mode, `scripts/run.py` currently reads:
- `outline/outline.yml` for section/subsection structure
- `outline/mapping.tsv` for paper-to-subsection coverage
- `papers/paper_notes.jsonl` for structured evidence
- `GOAL.md` for topic/domain cues
- `outline/claim_evidence_matrix.md` as optional supporting context when present

## Script

### Quick Start

- `python .codex/skills/subsection-briefs/scripts/run.py --workspace <workspace_dir>`

### All Options

- `--workspace <dir>`
- `--unit-id <id>`
- `--inputs <a;b;...>`
- `--outputs <a;b;...>`
- `--checkpoint <C*>`

### Examples

- `python .codex/skills/subsection-briefs/scripts/run.py --workspace workspaces/<ws>`

## Troubleshooting

- If the wrong domain pack is selected, inspect `GOAL.md` and the asset packs before changing the script.
- If briefs sound too generic, adjust the phrase/domain packs instead of adding more Python prose.
- If `papers/paper_notes.jsonl` is thin, reroute to note extraction rather than inventing axes.
