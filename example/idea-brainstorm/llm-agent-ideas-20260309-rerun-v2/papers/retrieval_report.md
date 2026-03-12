# Retrieval report

- Workspace: `/home/rjs/Workspace/codebase/research-units-pipeline-skills/workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun`
- queries.md: `/home/rjs/Workspace/codebase/research-units-pipeline-skills/workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun/queries.md`
- Keywords: `4`
- Excludes: `3`
- Time window: ``..``
- Online retrieval (best-effort): `OK`

## Summary

- Imported/collected records (pre-dedupe): `9`
- Deduped records (output): `9`
- Online error: `Semantic Scholar: SystemExit: Semantic Scholar request failed after 5 retries: None`
- Missing stable ID (arxiv_id/doi/url all empty): `0`
- Missing abstract: `0`
- Missing authors: `0`

## Sources

- Offline inputs: `0`
- Snowball inputs: `0`

## Coverage buckets (by route)

| route | unique_papers |
|---|---:|
| pinned_arxiv_id:2210.03629v3 | 1 |
| pinned_arxiv_id:2302.04761v1 | 1 |
| pinned_arxiv_id:2303.11366v4 | 1 |
| pinned_arxiv_id:2305.10601v2 | 1 |
| pinned_arxiv_id:2305.16291v2 | 1 |
| pinned_arxiv_id:2308.11432v7 | 1 |
| pinned_arxiv_id:2411.18279v12 | 1 |
| pinned_arxiv_id:2503.21460v1 | 1 |
| pinned_arxiv_id:2503.23037v3 | 1 |

## Next actions

- If the pool is too small: add more exports under `papers/imports/` (multi-route) or enable network and rerun with `--online`.
- If cite coverage is poor later: increase candidate pool size and run snowballing (provide exports under `papers/snowball/`).
- If many abstracts are missing: provide richer exports or rerun online enrichment.
