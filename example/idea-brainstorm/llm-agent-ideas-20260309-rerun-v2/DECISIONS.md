# Decisions log

## Approvals (check to unblock)
- [x] Approve C0 (kickoff: scope/sources/time window/constraints)
- [x] Approve C2 (scope + outline)


> 这里是 HITL 的“签字页”：当 pipeline 声明 human checkpoint 时，把问题与结论记录在这里。
> 执行器会根据 `UNITS.csv` 中 `owner=HUMAN` 的行，自动生成/检查 `## Approvals` 勾选项。

## (example) 2026-01-04
- Decision: Approve scope + outline (C2)
- Approved sections: 1-5
- Notes: keep focus on X; exclude Y
- Signed by: <HUMAN_NAME>

<!-- BEGIN CHECKPOINT:C0 -->
## Kickoff — Reliable LLM agent evaluation ideas

- Pipeline: `pipelines/idea-brainstorm.pipeline.md`
- Workspace: `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun`
- Workspace name: `llm-agent-ideas-20260309-rerun`

Optional: confirm constraints (or reply "你自己决定" and we will proceed with best-effort defaults):
- Deliverable: language (中文/英文), target length, audience, format (Markdown/LaTeX/PDF).
- Evidence mode: `abstract` (no PDF download) vs `fulltext` (download+extract snippets).
- Scope:
  - In-scope.
  - Out-of-scope.
- Time window: from/to year (or no limit).
- Search constraints: must-include systems/papers/keywords; hard excludes.
- Human sign-off: who will approve required checkpoints in this file.

Note:
- The pipeline will pause at HUMAN checkpoints (see the Approvals checklist) and resume after approval.
<!-- END CHECKPOINT:C0 -->

<!-- BEGIN CHECKPOINT:C2 -->
## C2 focus — pick idea map clusters (NO PROSE)

- taxonomy: top-level=4, leaf-nodes=8
- Brief: (missing) `output/IDEA_BRIEF.md`

### Candidate clusters (top-level)
- Foundations & Interfaces (children=2)
- Core Components (Planning + Memory) (children=2)
- Learning, Adaptation & Coordination (children=2)
- Evaluation & Risks (children=2)

Decision:
- Choose 1-2 focus clusters (by name) and 2-5 hard excludes.
- Optionally update `output/IDEA_BRIEF.md` to reflect the chosen focus.
- Tick `Approve C2` above to proceed (notes → idea pool → shortlist).
<!-- END CHECKPOINT:C2 -->
