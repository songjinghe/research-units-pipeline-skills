# U017 Outline Builder Review

## Scope

Unit: `U017`

Goal:
- migrate `outline-builder` to a reference-first package shape
- externalize `Introduction` / `Related Work` defaults and comparison-axis routing into inspectable assets/references
- preserve the visible contract: `outline/taxonomy.yml` -> `outline/outline.yml`

## Inputs reviewed

- `SKILLS_REFACTOR_BLUEPRINT.md`
- `SKILLS_REFACTOR_P0_P1_CHECKLIST.md`
- `SKILLS_REFACTOR_EXECUTION_PLAN.md`
- `SKILLS_AUDIT_FINDINGS.md`
- `SKILLS_STANDARD.md`
- `docs/SKILL_AUDIT_RULES.md`

## Implementation summary

Changed files:
- `.codex/skills/outline-builder/SKILL.md`
- `.codex/skills/outline-builder/scripts/run.py`
- `.codex/skills/outline-builder/assets/outline_defaults.yaml`
- `.codex/skills/outline-builder/references/overview.md`
- `.codex/skills/outline-builder/references/intro_related_patterns.md`
- `.codex/skills/outline-builder/references/stage_a_contract.md`
- `.codex/skills/outline-builder/references/examples_good.md`
- `.codex/skills/outline-builder/references/examples_bad.md`

Key changes:
- turned `SKILL.md` into a lean router with explicit reference/asset loading guidance
- moved front-section defaults and comparison-axis packs into `assets/outline_defaults.yaml`
- removed domain-pinned `Related Work` defaults from Python
- kept `run.py` as deterministic materializer plus placeholder-safe overwrite guard
- corrected misrouting risk in comparison-axis selection by moving matching rules into ordered asset packs

## Review / validation

### Multi-agent input

- compliance review checked package shape, audit expectations, and reference-first responsibilities before implementation
- implementation planning converged on the same target file set across the main agent and a worker agent
- two late-stage review requests were interrupted, so the final verdict relies on the completed planning reviews above plus deterministic validation below

### Deterministic checks

1. Syntax check
- `python3 -m py_compile .codex/skills/outline-builder/scripts/run.py`
- result: PASS

2. Smoke generation
- workspace: `workspaces/_tmp/u017-outline-builder-smoke-1773022278`
- command: `python3 .codex/skills/outline-builder/scripts/run.py --workspace <smoke-workspace>`
- result: PASS
- observed contract preserved:
  - `Introduction` and `Related Work` remain the first two H2 sections
  - H3 subsections still carry `Intent:` / `RQ:` / `Evidence needs:` / `Expected cites:` bullets
  - output remains bullets-only YAML

3. Targeted skill audit
- command: `python3 scripts/audit_skills.py --format json --fail-on NONE`
- filtered result for `outline-builder`: `0` findings

4. Repo validator
- command: `python3 scripts/validate_repo.py --report workspaces/_tmp/u017-validate-repo-1773022404.md`
- result: no repo errors; warnings were unrelated pre-existing gaps in other skills

## Verdict

PASS for `U017`.

Acceptance satisfied:
- `outline-builder` now has `references/` and `assets/`
- `SKILL.md` explicitly routes to them
- intro/related defaults and comparison-axis framing are assetized
- output contract remains compatible
- no targeted audit regressions were introduced

## Remaining scope

Not part of `U017`:
- `evidence-draft`
- `paper-notes`
- `survey-visuals`
- `idea-memo-writer`
- retrieval/ranking domain-pack externalization
