# Decisions log

## 2026-03-08
- Decision: replace the old `idea-finder` terminal artifact (`IDEA_TOP3_REPORT.md`) with a single default `output/REPORT.md` brainstorm memo.
- Decision: optimize the ideation flow for PI/PhD discussion quality, not proposal-style execution cards.
- Decision: keep default evidence mode `abstract`, but strengthen note structure and memo grounding.
- Decision: apply a direct-cut migration rather than preserving the old top-3 contract.
- Decision: panel review of the new memo confirms the pipeline now ends in the right artifact class, but the memo still needs a stronger editorial/academic pass.

## 2026-03-09
- Decision: ideation skills should optimize for advisor-ready memo quality, which now explicitly includes distinct thesis lines, rank separation, quick kill criteria, and paper-specific appendix reading guides.
- Decision: add regression checks that reject generic ideation language (for example generic evidence summaries or generic appendix reminders) instead of only checking artifact presence.
- Decision: adopt a repo-wide `reference-first / script-thin` skill refactor as the next primary workstream.
- Decision: treat `SKILLS_REFACTOR_BLUEPRINT.md`, `SKILLS_REFACTOR_P0_P1_CHECKLIST.md`, `SKILLS_REFACTOR_EXECUTION_PLAN.md`, and `SKILLS_AUDIT_FINDINGS.md` as the governing design docs for this refactor.
- Decision: execute Phase 0 first: create a repo-wide skill auditor, create a reference-first template skill, and update `SKILLS_STANDARD.md` / `SKILL_INDEX.md` before starting P0 writer-skill migrations.
- Decision: use multi-agent implementation plus explicit cross-review to reduce single-agent bias during the refactor.
- Decision: start Phase 1 with `front-matter-writer` in compatibility mode rather than an immediate context-only rewrite, so current survey pipelines keep their existing output contract while the package is migrated.
- Decision: rerun confirms the memo-style ideation path is stable enough to reproduce; remaining problems are now mostly content-density issues rather than pipeline-shape issues.

- Decision: accept the P0 writer/planner batch (`front-matter-writer`, `subsection-writer`, `chapter-lead-writer`, `subsection-briefs`, `taxonomy-builder`) as a compatibility-preserving reference-first milestone, with remaining genericization/script-thinning work deferred to later phases.
- Decision: execute `U017` in compatibility-preserving mode: move `outline-builder` front-section defaults and comparison-axis routing into `assets/outline_defaults.yaml` plus `references/`, while preserving the `outline/taxonomy.yml` -> `outline/outline.yml` contract.
- Decision: pause after `U017` to remediate earlier-task drift before continuing the remaining C8 migrations; prioritize `front-matter-writer` compatibility debt, milestone evidence-path normalization, P0 checklist drift, and stale ideation aliases.
- Decision: keep `front-matter-writer` in compatibility mode during `U025`, but remediate the active template asset, add reader-facing lint, and reconcile the key checklist drift instead of attempting the full context-only rewrite in one patch.
- Decision: normalize earlier milestone evidence through a crosswalk doc and status-log links, while preserving generic `output/...` names in contract-level docs as generic artifact contracts rather than workspace-specific evidence.
- Decision: treat the remaining P0 checklist drift as a mix of reconciled items, intentional compatibility-mode deviations, and explicit follow-up debt, rather than as a retroactive failure of the accepted `C7` milestone.
- Decision: retain `idea-finder` only as an explicit legacy compatibility shim in `scripts/pipeline.py` and `pipeline-router`, with `idea-brainstorm` remaining the sole active ideation contract.
- Decision: the thickened ideation rerun (`rerun-v2`) is clearly stronger than the previous rerun as a pruning / reading-priority memo, but still needs another editorial pass before it becomes a project-commit or reviewer-grade memo.
