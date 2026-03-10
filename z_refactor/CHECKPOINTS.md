# Checkpoints

## C0 - Repo refactor contract ready
- [x] `STATUS.md` / `UNITS.csv` / `DECISIONS.md` / `CHECKPOINTS.md` created
- [x] pipeline/template/skills aligned to the new brainstorm-memo contract

## C1 - Pipeline contract rebuilt
Criteria:
- [x] pipeline spec reflects the new terminal artifact and stages
- [x] units template matches the pipeline stages and outputs

## C2 - Skills rebuilt
Criteria:
- [x] signal generation skill exists
- [x] direction generation skill exists
- [x] memo writer skill exists
- [x] old top-3 expansion path removed from the active contract

## C3 - Quality gates rebuilt
Criteria:
- [x] quality gates validate `REPORT.md` / `APPENDIX.md` / `REPORT.json`
- [x] self-loop validates the memo-style deliverable rather than mini proposals

## C4 - Validation
Criteria:
- [x] focused validation of the new pipeline path passes
- [x] no stale `idea-finder` contract remains in active entrypoints

## C5 - Phase 0 foundations
Criteria:
- [x] repo-wide skill auditor exists and covers the major smell classes
- [x] reference-first template skill exists under `.codex/skills/_template_reference_first/`
- [x] `SKILLS_STANDARD.md` codifies `SKILL.md` / `references/` / `assets/` / `scripts/` responsibilities
- [x] multi-agent Phase 0 review confirms the outputs align with the blueprint docs

## C6 - First P0 skill kickoff completed
Criteria:
- [x] at least one P0 writer/planner skill has begun migration to reference-first structure
- [x] the kickoff preserves current pipeline compatibility and is documented by a review artifact

## C7 - Remaining P0 writer/planner batch
Criteria:
- [x] `subsection-writer` migrated to reference-first structure
- [x] `chapter-lead-writer` migrated to reference-first structure
- [x] `subsection-briefs` migrated to reference-first structure
- [x] `taxonomy-builder` migrated to reference-first structure
- [x] batch accepted by multi-agent review and local smoke validation

## C7R - Earlier-task remediation pass
Criteria:
- [x] `front-matter-writer` compatibility debt is reduced and its key checklist drift is reconciled or explicitly documented
- [x] earlier milestone evidence paths are normalized into durable workspace-linked references
- [x] migrated P0 skill checklist drift is audited and recorded in a single remediation review artifact
- [x] stale ideation compatibility aliases are either removed or explicitly documented as intentional compatibility shims

## C8 - P1/P2 next batch
Criteria:
- [x] `outline-builder` migrated to reference-first structure
- [ ] `evidence-draft` migrated to reference-first structure
- [ ] `paper-notes` migrated to reference-first structure
- [ ] `survey-visuals` migrated to reference-first structure
- [ ] `idea-memo-writer` migrated to reference-first structure
- [ ] retrieval/ranking domain logic externalized into explicit packs

## C4R - Ideation content-thickening pass
Criteria:
- [x] ideation skills encode distinct thesis lines, explicit rank logic, quick kill criteria, and appendix reading-guide requirements
- [x] smoke rerun passes `deliverable-selfloop` and `artifact-contract-auditor`
