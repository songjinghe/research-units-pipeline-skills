# Paper Notes — Note Schema Reference

## Required Fields (every paper)

| Field | Type | Description |
|---|---|---|
| `paper_id` | string | Stable identifier from `papers/core_set.csv` |
| `title` | string | Paper title |
| `year` | int/string | Publication year |
| `bibkey` | string | Citation key for BibTeX |
| `evidence_level` | string | One of: `fulltext`, `abstract`, `title` |
| `priority` | string | One of: `high`, `normal` |
| `summary_bullets` | array[string] | 3–6 bullet summaries (high-priority); 1–5 (normal) |
| `limitations` | array[string] | Paper-specific limitations (see `limitation_taxonomy.md`) |

## Required for High-Priority Papers

| Field | Type | Description |
|---|---|---|
| `method` | string | What the paper proposes and how it differs from baselines |
| `key_results` | array[string] | Concrete evaluation results with task + metric + numbers when available |

## Optional but Recommended

| Field | Type |
|---|---|
| `authors` | array[string] |
| `abstract` | string |
| `arxiv_id` | string |
| `pdf_url` | string |
| `fulltext_path` | string |
| `mapped_sections` | array[string] |
| `primary_category` | string |
| `categories` | array[string] |

## Evidence Level Semantics

- **fulltext**: extracted text available in `papers/fulltext/`; highest confidence
- **abstract**: metadata includes abstract; moderate confidence
- **title**: only the title is available; lowest confidence — do not infer method/results beyond what the title states
