# Skills Phase 0 Review

- Status: PASS (with follow-up items)
- Scope: Phase 0 foundations for the repo-wide skills refactor
- Inputs reviewed:
  - `SKILLS_REFACTOR_BLUEPRINT.md`
  - `SKILLS_REFACTOR_P0_P1_CHECKLIST.md`
  - `SKILLS_REFACTOR_EXECUTION_PLAN.md`
  - `SKILLS_AUDIT_FINDINGS.md`
  - `SKILLS_STANDARD.md`
  - `SKILL_INDEX.md`
  - `scripts/audit_skills.py`
  - `docs/SKILL_AUDIT_RULES.md`
  - `.codex/skills/_template_reference_first/`
  - `scripts/new_skill.py`
  - `scripts/validate_repo.py`
  - `scripts/generate_skill_graph.py`

## 1. Outputs delivered in Phase 0

### Planning / governance docs
- `SKILLS_REFACTOR_BLUEPRINT.md`
- `SKILLS_REFACTOR_P0_P1_CHECKLIST.md`
- `SKILLS_REFACTOR_EXECUTION_PLAN.md`
- `SKILLS_AUDIT_FINDINGS.md`

### Standards / discoverability
- `SKILLS_STANDARD.md`
- `SKILL_INDEX.md`

### Tooling
- `scripts/audit_skills.py`
- `docs/SKILL_AUDIT_RULES.md`
- `scripts/new_skill.py` (reference-first skeleton)
- `scripts/validate_repo.py` (ignore `_template_*` directories)
- `scripts/generate_skill_graph.py` (ignore `_template_*` directories)

### Template skill
- `.codex/skills/_template_reference_first/`

## 2. Review process

This phase used parallel workstreams plus cross-review to reduce single-agent bias:

- Workstream A: audit tool + rule doc
- Workstream B: reference-first template skill
- Workstream C: standards / index update
- Workstream D: internal consistency review of the four planning docs
- Workstream E: external-practice cross-check against Anthropic-style skill design principles

## 3. Validation performed

### 3.1 Tooling validation
- `python -m py_compile scripts/audit_skills.py`
- `python -m py_compile scripts/new_skill.py`
- `python -m py_compile scripts/validate_repo.py`
- `python -m py_compile scripts/generate_skill_graph.py`

### 3.2 Template skill validation
- `python .codex/skills/_template_reference_first/scripts/run.py --strict`
  - Result: PASS

### 3.3 Audit baseline
- `python scripts/audit_skills.py --fail-on NONE`
  - Current baseline after excluding `_template_*` directories:
    - skills scanned: `85`
    - findings: `282`
    - severity split: `ERROR=1, WARN=63, INFO=218`
  - Interpretation:
    - the auditor is functioning as intended,
    - the repo still contains significant pre-existing issues,
    - enforcement should remain warn-only globally during Phase 0 / early Phase 1.

### 3.4 Repo compatibility smoke check
- `python scripts/validate_repo.py --report docs/SKILLS_PHASE0_VALIDATE_REPO.md`
  - Result: not clean yet
  - Key interpretation:
    - the Phase 0 tooling changes themselves are compatible,
    - the repo still has pre-existing skill-doc quality issues unrelated to the template bootstrap,
    - those issues remain migration backlog, not Phase 0 blockers.

## 4. Cross-review conclusions

### 4.1 What is now solid
- The repo now has a written, explicit reference-first refactor doctrine.
- The standards doc now encodes the responsibility split between `SKILL.md`, `references/`, `assets/`, and `scripts/`.
- A reusable template skill exists and demonstrates the target structure.
- The repo now has a dedicated skill-audit tool rather than relying on ad hoc grep-only checks.
- Discovery/validation tooling no longer treats `_template_*` directories as normal skills.
- `new_skill.py` now defaults to generating a reference-first skeleton.

### 4.2 What we intentionally did **not** do in Phase 0
- We did not yet migrate existing writer/evidence/ideation skills off their current scripts.
- We did not yet make `audit_skills.py` globally blocking.
- We did not yet replace old domain heuristics in retrieval/ranking with external domain packs.

## 5. Follow-up items (non-blocking for Phase 0)

### F1. Reader-facing classification
The audit rules should later distinguish:
- reader-facing outputs
- trace/internal outputs
- examples/anti-pattern strings

This matters because ellipsis and template-phrase detection is still intentionally heuristic.

### F2. Contract-preservation rule during Phase 1
When refactoring a skill that is currently active in a pipeline:
- either preserve its current outputs,
- or update `pipelines/*.pipeline.md`, `templates/UNITS.*.csv`, and validators in the same patch.

### F3. Touched-skill enforcement
Recommended rollout:
- warn-only globally,
- stricter enforcement for touched / newly migrated skills,
- eventual stricter repo-wide gate only after more migrations land.

### F4. Ideation docs must remain aligned to active `idea-brainstorm` contract
Future skill changes in ideation should follow:
- `output/REPORT.md`
- `output/APPENDIX.md`
- `output/REPORT.json`

and should not regress to legacy `Top-3` terminal artifacts.

## 6. Phase 0 verdict

Phase 0 is accepted because the required foundations now exist:

- repo-wide auditor: yes
- audit rules doc: yes
- reference-first template skill: yes
- standards/index update: yes
- toolchain compatibility update: yes
- multi-agent review + cross-check: yes

## 7. Recommended next step

Proceed to Phase 1 / P0 migration with a compatibility-preserving first target:

- `front-matter-writer`

Reason:
- highest user-visible payoff
- clear domain/prose hardcoding problems
- direct conflict between script behavior and current guardrails
- bounded enough to migrate incrementally
