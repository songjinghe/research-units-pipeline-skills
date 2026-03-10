# C7R Ideation Alias Review

## Scope

Unit: `U028`

Goal:
- resolve the remaining `idea-finder` runtime aliases without reviving it as an active contract
- either remove the aliases or explicitly document them as intentional legacy compatibility shims

## Findings

Runtime alias hits before this remediation existed only in:
- `scripts/pipeline.py`
- `.codex/skills/pipeline-router/scripts/run.py`

Other `idea-finder` mentions are historical/governance records and should remain:
- `DECISIONS.md`
- old workspace artifacts and old workspace lock/status files

## Decision

The active contract remains `idea-brainstorm`.

`idea-finder` is retained only as a legacy compatibility shim because archived workspaces still contain old lock paths such as:
- `workspaces/idea-brainstorm/llm-agent-ideas-20260308/PIPELINE.lock.md`

Removing the alias outright was deferred to avoid unnecessary breakage for legacy CLI invocations and old workspace replay.

## Implementation

- centralized alias normalization in `scripts/pipeline.py`
- centralized alias normalization in `.codex/skills/pipeline-router/scripts/run.py`
- removed duplicated ad hoc string checks and replaced them with explicit normalization helpers
- kept behavior unchanged for legacy inputs while making the shim visible and auditable

## Validation

- `python3 -m py_compile scripts/pipeline.py`
- `python3 -m py_compile .codex/skills/pipeline-router/scripts/run.py`
- direct normalization check for:
  - `idea-finder`
  - `idea-finder.pipeline.md`
  - `pipelines/idea-finder.pipeline.md`
- repo grep confirms no remaining stale active contract reference outside:
  - governance/history docs
  - archived workspace artifacts
  - this remediation record

## Future deletion condition

Delete the shim once both are true:
- no supported workflow or user habit still depends on `idea-finder`
- archived workspaces no longer need ideation-specific behavior from legacy lock values
