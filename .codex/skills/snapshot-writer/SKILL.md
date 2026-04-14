---
name: snapshot-writer
description: |
  Use when a `research-brief` workspace has a small paper set plus outline and needs a compact reader-facing briefing instead of a full survey.
  **Trigger**: snapshot, literature snapshot, 速览, 48h snapshot, one-page snapshot, SNAPSHOT.md.
  **Use when**: 你要在 `research-brief` 流程里 24-48h 内交付一个“可读的研究速览”（bullet-first，含关键引用），而不是完整 survey。
  **Skip if**: 你已经进入 evidence-first survey 写作（有 `outline/evidence_drafts.jsonl` / `citations/ref.bib` / `output/DRAFT.md`），应改用 `subsection-writer`/`prose-writer`。
  **Network**: none.
  **Guardrail**: 不发明论文/引用；引用只来自 `papers/core_set.csv`（或同 workspace 的候选池）；不写长段落（避免“像综述生成器”）。
---

# Snapshot Writer

Transforms a small core set plus a bullets-only outline into the final `research-brief` deliverable.

## Inputs

Required:
- `outline/outline.yml`
- `papers/core_set.csv`

Optional:
- `queries.md`
- `papers/papers_dedup.jsonl`

## Output

- `output/SNAPSHOT.md`

## Script boundary

`scripts/run.py` should stay a thin adapter over shared review tooling:
- read outline/core-set inputs
- build a compact pointer-heavy briefing
- write `output/SNAPSHOT.md`

Do not move topic-specific ranking rules or deep parsing logic into this script.

## Contract

The output should:
- read like a briefing, not a survey draft
- stay bullets-first and compact
- define the topic boundary
- surface key themes
- include explicit paper pointers in a stable format

## Acceptance

- `output/SNAPSHOT.md` exists
- includes `## Scope` and `## What to read first`
- includes explicit paper pointers from the workspace paper set

## Non-goals

- full evidence synthesis
- protocol / screening / extraction
- monolithic long-form survey writing
