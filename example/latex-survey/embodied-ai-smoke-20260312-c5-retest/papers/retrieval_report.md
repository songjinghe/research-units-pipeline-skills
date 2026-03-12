# Retrieval report

- Workspace: `/home/rjs/Workspace/codebase/research-units-pipeline-skills/workspaces/arxiv-survey/embodied-ai-smoke-20260311-r1`
- queries.md: `/home/rjs/Workspace/codebase/research-units-pipeline-skills/workspaces/arxiv-survey/embodied-ai-smoke-20260311-r1/queries.md`
- Keywords: `14`
- Excludes: `0`
- Time window: `2018`..``
- Online retrieval (best-effort): `OK`

## Summary

- Imported/collected records (pre-dedupe): `1807`
- Deduped records (output): `1800`
- Preserved previous non-empty output after zero-result rerun: `no`
- Online error: (none)
- Missing stable ID (arxiv_id/doi/url all empty): `0`
- Missing abstract: `0`
- Missing authors: `0`

## Sources

- Offline inputs: `0`
- Snowball inputs: `0`

## Coverage buckets (by route)

| route | unique_papers |
|---|---:|
| arxiv_query:(((all:embodied OR all:robot OR all:robotic) AND (all:"vision-language-action" OR all:vla OR all:policy OR all:"foundation model" OR all:"world model" OR all:manipulation OR all:navigation)) AND (all:survey OR all:review OR all:"generalist robot" OR all:"robot learning" OR all:"mobile manipulation")) | 1797 |
| pinned_arxiv_id:2212.06817v2 | 1 |
| pinned_arxiv_id:2307.15818v1 | 1 |
| pinned_arxiv_id:2405.12213v2 | 1 |
| pinned_arxiv_id:2405.14093v7 | 1 |
| pinned_arxiv_id:2406.09246v3 | 1 |
| pinned_arxiv_id:2505.20503v2 | 1 |
| pinned_arxiv_id:2508.05294v4 | 1 |

## Next actions

- If the pool is too small: add more exports under `papers/imports/` (multi-route) or enable network and rerun with `--online`.
- If cite coverage is poor later: increase candidate pool size and run snowballing (provide exports under `papers/snowball/`).
- If many abstracts are missing: provide richer exports or rerun online enrichment.
