---
name: deliverable-selfloop
description: |
  Use when a reader-facing deliverable exists and needs a deterministic PASS/FAIL quality gate.
  **Trigger**: self loop, self-loop, polish deliverable, quality gate, fix-on-fail, 收敛, 自循环, 质量门.
  **Use when**: A pipeline has produced a reader-facing deliverable (`output/*.md`) and you want deterministic convergence to PASS.
  **Skip if**: You are still pre-approval for prose or the upstream evidence/structure artifacts are missing.
  **Network**: none.
  **Guardrail**: Do not invent papers/citations/results. Only use in-scope inputs already present in the workspace.
---

# Deliverable Self-Loop

Runs the final quality gate for a reader-facing deliverable and always writes a PASS/FAIL report.

## Inputs

Primary input depends on the active pipeline contract:
- brief deliverable
- paper-review deliverable
- evidence-review deliverable
- idea memo bundle
- tutorial deliverable

## Output

- `output/DELIVERABLE_SELFLOOP_TODO.md`

## Dispatch rule

The gate should dispatch by pipeline contract first:
- `quality_contract.deliverable_kind`

Only fall back to legacy profile-name checks when contract metadata is missing.

## Script boundary

`scripts/run.py` should:
- detect the active deliverable contract
- run the matching evaluator
- always write a report

It should not mutate the deliverable itself.

## Acceptance

- report exists
- report contains `- Status: PASS` or `- Status: FAIL`
- PASS only when the active deliverable satisfies its minimum section / artifact contract

## Non-goals

- rewriting the deliverable
- choosing upstream fixes beyond pointing to the missing contract items
