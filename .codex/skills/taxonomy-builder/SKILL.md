---
name: taxonomy-builder
description: |
  Build a 2+ level taxonomy (`outline/taxonomy.yml`) from a core paper set and scope constraints, with short descriptions per node.
  **Trigger**: taxonomy, taxonomy builder, 分类, 主题树, taxonomy.yml.
  **Use when**: survey/snapshot 的结构阶段（NO PROSE），已有 `papers/core_set.csv`，需要生成可映射且读者友好的主题结构。
  **Skip if**: 已经有批准过且可映射的 taxonomy（不要无意义重构）。
  **Network**: none.
  **Guardrail**: 避免泛化占位桶；保持 2+ 层且每节点有具体描述。
---

# Taxonomy Builder (router, compatibility mode)

Build `outline/taxonomy.yml` from `papers/core_set.csv`.

P0 compatibility note:
- The output contract stays the same (`outline/taxonomy.yml`, YAML list, >=2 levels, concrete descriptions).
- Curated domain taxonomies now live in `assets/domain_packs/*.yaml` instead of Python prose.
- `scripts/run.py` stays a deterministic scaffold/helper: detect domain pack -> load pack when available -> otherwise fall back to the generic builder.

## Read in this order

1. `references/overview.md`
2. `references/taxonomy_principles.md`
3. If a domain pack applies, read its `references/domain_pack_<domain>.md` and `assets/domain_packs/<domain>.yaml`
4. Otherwise read `references/archetypes_generic.md`
5. Calibrate naming/description quality with `references/examples_good.md` and `references/examples_bad.md`

Current compatibility packs:
- `llm_agents`
- `gen_image`

## Inputs

- `papers/core_set.csv` (required)
- Optional: `papers/papers_dedup.jsonl`
- Optional: `DECISIONS.md`, `GOAL.md`, `queries.md`

## Outputs

- `outline/taxonomy.yml`

## Asset contract

- `assets/taxonomy_schema.json`: machine-readable shape for domain packs / output expectations
- `assets/domain_packs/*.yaml`: compatibility domain packs for supported domains

## Script role

Use `scripts/run.py` only for deterministic help:
- never overwrite non-placeholder user taxonomy
- preserve current CLI flags / output path
- load supported domain taxonomies from assets instead of hard-coded Python prose
- keep the generic fallback builder for non-packed domains

## When to refine manually

Refine the generated taxonomy before marking the unit `DONE` if:
- top-level buckets feel like keyword clusters instead of chapter-level questions
- leaf names are generic (`Overview`, `Benchmarks`, `Open Problems`, `Misc`)
- descriptions lack scope cues or representative paper anchors
- domain detection chose the wrong pack

## Quick start

- `python .codex/skills/taxonomy-builder/scripts/run.py --help`
- `python .codex/skills/taxonomy-builder/scripts/run.py --workspace <workspace_dir>`


## Execution notes

When running in compatibility mode, `scripts/run.py` currently reads:
- `papers/core_set.csv` as the required corpus input
- `papers/papers_dedup.jsonl` when present for extra title/abstract signals
- `GOAL.md`, `queries.md`, and `DECISIONS.md` as optional domain/profile hints during pack selection

## Script

### Quick Start

- `python .codex/skills/taxonomy-builder/scripts/run.py --workspace <workspace_dir>`

### All Options

- `--workspace <dir>`
- `--top-k <int>`
- `--min-freq <int>`
- `--unit-id <id>`
- `--inputs <a;b;...>`
- `--outputs <a;b;...>`
- `--checkpoint <C*>`

### Examples

- `python .codex/skills/taxonomy-builder/scripts/run.py --workspace workspaces/<ws>`

## Troubleshooting

- If the wrong domain pack is chosen, inspect `GOAL.md`, `queries.md`, and the pack `detect` rules before changing Python.
- If `outline/taxonomy.yml` already contains a real non-placeholder taxonomy, the script intentionally returns without overwriting it.
- If no pack matches, the script falls back to the generic builder.
