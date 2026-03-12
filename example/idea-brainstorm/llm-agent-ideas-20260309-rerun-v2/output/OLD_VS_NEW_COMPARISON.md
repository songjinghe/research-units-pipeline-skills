# Old vs New Ideation Memo Comparison

## Summary

- Verdict: the new rerun is clearly stronger as a **research-discussion / pruning memo** than the old rerun.
- The biggest gains are:
  - clearer ranking logic
  - more distinct program framing
  - explicit quick-kill criteria
  - a real appendix reading guide
- The biggest new problems are:
  - over-compressed summary tables
  - a few wording / control-definition bugs
  - thinner-than-desired prior-work differentiation across the top 3

## Objective changes

- Old report lines: 181
- New report lines: 146
- Old appendix lines: 30
- New appendix lines: 44
- Old lead-set titles:
  - `Observability before planner depth? for Agent loop and action spaces`
  - `How much of planning quality is really search depth?`
  - `When retrieval policy becomes the hidden variable for Memory and retrieval (RAG)`
- New lead-set titles:
  - `Observability granularity vs planner depth`
  - `Action-space design or agent competence?`
  - `Search depth or compute budget?`
- Old `Quick kill criteria` blocks: 0
- New `Quick kill criteria` blocks: 3
- Old appendix reading-guide tables: 0
- New appendix reading-guide tables: 3
- Old generic phrase hits (`reports a meaningful gain` / `Sharper mechanism question;` / `read it to extract...`): 21
- New generic phrase hits: 0

## Clear improvements

- Ranking logic is now front-and-center instead of hidden behind generic `Sharper mechanism question` phrasing. Compare `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun/output/REPORT.md:13` with `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:13`.
- The top 3 now feel like different research programs rather than three near-identical hidden-variable cards. See `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:13` and `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:22`.
- Per-direction sections now expose the missing control, expected contribution shape, and explicit kill conditions instead of generic “missing piece / probe” language. Compare `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun/output/REPORT.md:33` with `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:35` and `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:49`.
- The appendix is now a usable reading guide rather than a reminder list. Compare `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun/output/APPENDIX.md:15` with `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/APPENDIX.md:17`.
- Closing guidance is more actionable: the new memo names what to read first and when to rerank. Compare `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun/output/REPORT.md:172` with `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:137`.

## Regressions / new issues

- The lead set is narrower: retrieval-policy / memory left the top 3 and moved to deferred status, so breadth is lower even though focus is higher. Compare `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun/output/REPORT.md:111` with `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:119`.
- The summary table is over-compressed and visibly clipped, making the most important overview harder to use. See `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:18`.
- A few lines are awkward or self-undermining:
  - clipped contribution / summary cells in the top table at `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:22`
  - Direction 2 control-language bug at `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:81`
  - unfinished / weak deferred appendix prose at `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/APPENDIX.md:11`
- Some anchors are still too weak to carry reviewer-grade weight, especially survey-definition rows being treated like result hooks. See `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/APPENDIX.md:26`.

## Net assessment

- Keep:
  - explicit ranking logic
  - quick-kill framing
  - paper-specific reading-guide tables
- Fix:
  - clipped overview table
  - Direction 2 intervention wording
  - weak / non-empirical anchor rows
- Reconsider:
  - whether the top 3 should remain this narrow, or whether one memory / retrieval line deserves to return as a more distinct third program
