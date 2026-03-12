# V2 Revision Notes

## Highest-priority edits

### 1. Replace the top summary table
- Convert `Top directions at a glance` into either:
  - 3 compact decision cards, or
  - a much shorter table with only `Direction / Why now / Fast kill signal`
- Reason: the current table is visibly clipped and therefore fails at the most important scan point.
- Target: `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:18`

### 2. Fix Direction 2 control language
- Rewrite the intervention so it does not say “vary action-space design while holding action-vocabulary/interface design fixed.”
- Suggested correction: define one concrete intervention variable such as `action vocabulary granularity` or `interface ergonomic cleanup`, then explicitly hold the others fixed.
- Target: `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:74`

### 3. Strengthen or prune weak anchor rows
- Do not let survey-definition text act as if it were decisive empirical evidence.
- Either:
  - downgrade those rows to background-only anchors, or
  - replace them with more empirical anchors from the core set.
- Targets: `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/APPENDIX.md:26`, `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/APPENDIX.md:35`

### 4. Make novelty risk more explicit
- Add one small line per lead direction:
  - `What existing result would immediately collapse this idea?`
  - `What result would only narrow it, not kill it?`
- This would improve both PI usefulness and reviewer credibility.
- Targets: `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:42`, `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:73`, `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:104`

### 5. Add a front-loaded PI decision block
- Right after framing, add a short block like:
  - `Current #1: ...`
  - `Read first: ...`
  - `Kill fast if: ...`
  - `Rerank if: ...`
- This helps senior readers who will not read the full memo front-to-back.
- Targets: `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:3`, `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:137`

### 6. Decide whether to keep the current narrow top 3
- Current tradeoff:
  - gain: stronger focus in one planning/agent-loop neighborhood
  - loss: less breadth across memory / retrieval / RAG-style idea families
- Decision needed:
  - keep the narrow lead set, or
  - bring back one more distinct memory / retrieval direction as a truer third program
- Targets: `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/REPORT.md:119`, `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun-v2/output/APPENDIX.md:11`

## Suggested next edit order

1. Fix clipped / broken presentation
2. Fix Direction 2 intervention definition
3. Clean weak appendix anchors
4. Add `collapse vs narrow` novelty lines
5. Re-evaluate whether the top 3 are distinct enough
