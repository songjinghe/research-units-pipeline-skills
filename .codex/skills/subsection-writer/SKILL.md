---
name: subsection-writer
description: |
  Write survey prose into per-section files under `sections/` so each unit can be QA'd independently before merging.
  **Trigger**: subsection writer, per-section writing, split sections, sections/, 分小节写, 按章节拆分写作.
  **Use when**: `Approve C2` is recorded and writer packs exist (`outline/writer_context_packs.jsonl`); you want evidence-bounded drafting without a monolithic one-shot draft.
  **Skip if**: `DECISIONS.md` approval is missing, or `outline/evidence_drafts.jsonl` / `citations/ref.bib` is missing.
  **Network**: none.
  **Guardrail**: do not invent facts/citations; no TODO/ellipsis leakage; keep citations subsection- or chapter-scoped; H3 body files and chapter leads must not contain headings.
---

# Subsection Writer (compatibility router)

Purpose: write or refine per-section survey prose under `sections/` while keeping the current pipeline contract unchanged.

Compatibility mode:
- output paths stay the same
- `scripts/run.py` still handles approval checks, missing-file bootstrap, and `sections/sections_manifest.jsonl`
- writing guidance now lives in `references/` instead of being encoded primarily in the script

## Load Order

Always read:
- `references/overview.md`
- `references/paragraph_jobs.md`
- `references/bootstrap_assembly.md` when reasoning about compatibility-mode bootstrap behavior

Read as needed:
- `references/opener_catalog.md` when paragraph 1 sounds generic or narrated
- `references/contrast_moves.md` when building A-vs-B comparison paragraphs
- `references/eval_anchor_patterns.md` when making performance / robustness / benchmark claims
- `references/limitation_moves.md` when adding caveats or local conclusions
- `references/examples_good.md` and `references/examples_bad.md` for calibration only

Machine-readable contract:
- `assets/subsection_writer_context.schema.json`
- `assets/bootstrap_paragraph_templates.json`

## Inputs

Required:
- `DECISIONS.md` (must include `Approve C2`)
- `outline/outline.yml`
- `outline/writer_context_packs.jsonl` (preferred)
- `citations/ref.bib`

Optional but useful:
- `outline/subsection_briefs.jsonl`
- `outline/evidence_drafts.jsonl`
- `outline/evidence_bindings.jsonl`
- `outline/anchor_sheet.jsonl`
- `outline/chapter_briefs.jsonl`

## Outputs

Keep the current contract:
- `sections/abstract.md`
- `sections/discussion.md`
- `sections/conclusion.md`
- `sections/S<sec_id>.md` for H2-without-H3 bodies
- `sections/S<sec_id>_lead.md` for H2 lead blocks
- `sections/S<sub_id>.md` for H3 bodies
- `sections/sections_manifest.jsonl`

## Writer policy

The active rule is move coverage, not paragraph quota.
A subsection should cover the necessary argument moves the pack supports; do not pad to a fixed count when the evidence does not justify it.

Opener / ending policy:
- generate 2-4 opener candidates from the pack's actual tension, contrast, protocol, or limitation signals; keep the most content-bearing option instead of reusing one stock stem everywhere
- let subsection endings emerge from evidence-bearing comparison / limitation material; do not append a fixed “safest synthesis / decision rule” closer just to make the paragraph feel finished

## Script boundary

Use `scripts/run.py` as a helper only:
- it may bootstrap missing H3 files and refresh the manifest
- it must not be treated as the canonical source of prose shape or voice policy

## Quick Start

- `python .codex/skills/subsection-writer/scripts/run.py --workspace workspaces/<ws>`

## Troubleshooting

- If the pack is thin, stop and route upstream instead of padding prose.
- If the subsection sounds narrated, reload `references/opener_catalog.md` and `references/examples_bad.md`.
- If a claim lacks protocol context, reload `references/eval_anchor_patterns.md` before rewriting.


## Execution notes

When running in compatibility mode, `scripts/run.py` currently consumes:
- `DECISIONS.md` for `Approve C2`
- `outline/outline.yml` to enumerate chapter / subsection files
- `outline/writer_context_packs.jsonl` as the primary drafting input
- `citations/ref.bib` for in-scope citations
- `outline/subsection_briefs.jsonl`, `outline/evidence_drafts.jsonl`, `outline/evidence_bindings.jsonl`, `outline/anchor_sheet.jsonl`, and `outline/chapter_briefs.jsonl` as optional enrichment sources

## Script

### Quick Start

- `python .codex/skills/subsection-writer/scripts/run.py --workspace <workspace_dir>`

### All Options

- `--workspace <dir>`
- `--unit-id <id>`
- `--inputs <a;b;...>`
- `--outputs <a;b;...>`
- `--checkpoint <C*>`

### Examples

- `python .codex/skills/subsection-writer/scripts/run.py --workspace workspaces/<ws>`

## Troubleshooting

- If `DECISIONS.md` lacks `Approve C2`, stop and fix approval first.
- If `outline/writer_context_packs.jsonl` is thin, reroute upstream instead of padding prose.
- If citation scope looks wrong, re-check `citations/ref.bib` and the writer packs before editing output text.
