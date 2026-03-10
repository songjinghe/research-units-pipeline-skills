# C7R P0 Drift Audit

## Scope

Unit: `U027`

Goal:
- compare the migrated P0 skill packages against the file-level expectations in `SKILLS_REFACTOR_P0_P1_CHECKLIST.md`
- record which checklist-to-filesystem deviations have already been reconciled
- separate intentional compatibility-mode deviations from open follow-up debt

This is a remediation audit for `C7R`, not a retroactive failure of `C7`.

## Method

Compared these migrated P0 packages against the P0 checklist sections:
- `.codex/skills/front-matter-writer/`
- `.codex/skills/subsection-writer/`
- `.codex/skills/chapter-lead-writer/`
- `.codex/skills/subsection-briefs/`
- `.codex/skills/taxonomy-builder/`

Evidence sources:
- `SKILLS_REFACTOR_P0_P1_CHECKLIST.md`
- `docs/FRONT_MATTER_P0_KICKOFF_REVIEW.md`
- `docs/SKILLS_P0_WRITER_BATCH_REVIEW.md`
- current package trees and `SKILL.md` / `scripts/run.py` surfaces

## Summary Table

| Skill | Checklist expectation | Actual package state | Disposition | Follow-up |
| --- | --- | --- | --- | --- |
| `front-matter-writer` | missing reference + schema alias should exist; `run.py` should stop owning prose writing | missing files now reconciled; `run.py` still materializes prose in compatibility mode | partly reconciled + intentional compatibility-mode deviation | deeper script-thinning remains open |
| `subsection-writer` | reference pack + `section_context_schema.json`; no paragraph-skeleton bootstrap | reference pack present; schema filename differs; compatibility bootstrap still active | open follow-up | later script-thinning / schema normalization |
| `chapter-lead-writer` | `chapter_lead_context_schema.json`; `chapter_lead_context.jsonl`; no direct prose templates | package shape present, but schema/context artifacts use different names and prose output path remains active | open follow-up | later context-sidecar alignment |
| `subsection-briefs` | YAML domain pack + `brief_schema.json`; phrase logic externalized | phrase/domain logic externalized, but via JSON packs; `brief_schema.json` missing | mixed: intentional deviation + open follow-up | record JSON-pack choice; add or defer schema |
| `taxonomy-builder` | domain pack loader + externalized taxonomy prose | checklist target substantially met; extra `gen_image` pack extends beyond checklist | reconciled + acceptable extension | generic fallback builder still open debt |

## Per-skill Findings

### `front-matter-writer`

**Reconciled**
- checklist expected `references/discussion_conclusion_patterns.md`; the package now has it
- checklist expected `assets/front_matter_context_schema.json`; the package now has a compatibility alias alongside the existing dotted filename
- reader-facing lint requested by the checklist is now enforced in `scripts/run.py`

**Intentional compatibility-mode deviation**
- checklist end-state wanted `run.py` to stop directly materializing intro/related/abstract/discussion/conclusion prose
- current package still renders prose from the externalized asset bank in order to preserve the active pipeline contract

**Open follow-up**
- split the large compatibility template bank into smaller packs/archetypes, as already noted in `docs/SKILLS_P0_WRITER_BATCH_REVIEW.md`

### `subsection-writer`

**Reconciled**
- expected references such as `paragraph_jobs.md`, `opener_catalog.md`, `contrast_moves.md`, `eval_anchor_patterns.md`, and `limitation_moves.md` are present and routed from `SKILL.md`

**Intentional compatibility-mode deviation**
- package includes `references/bootstrap_assembly.md`, which was not named in the original checklist but supports the accepted compatibility path

**Open follow-up**
- checklist expected `assets/section_context_schema.json`; current package uses `assets/subsection_writer_context.schema.json`
- checklist end-state wanted `run.py` to move toward `section_context.json` + manifest/validation and stop directly assembling paragraph skeletons; current script still bootstraps H3 body files in compatibility mode

### `chapter-lead-writer`

**Reconciled**
- reference pack shape is present: overview, archetypes, throughline patterns, bridge examples, and bad narration examples

**Open follow-up**
- checklist expected `assets/chapter_lead_context_schema.json`; current package instead exposes `assets/lead_block_contract.json` and `assets/lead_block_compatibility_defaults.json`
- checklist expected `run.py` to generate `chapter_lead_context.jsonl`; current script still writes lead prose files plus a report
- minor hygiene drift remains in older CLI placeholder text inside `SKILL.md`

### `subsection-briefs`

**Reconciled**
- thesis/tension/domain/bridge logic has materially moved out of hardcoded Python prose and into asset packs plus references

**Intentional compatibility-mode deviation**
- checklist described YAML domain packs; the current accepted package uses JSON packs instead
- this is a format drift, but the direction of externalization is consistent with the checklist intent

**Open follow-up**
- checklist expected `assets/brief_schema.json`; current package does not include that schema file
- phrase/domain assets remain implementation-specific (`phrase_packs/*.json`, `domain_packs/*.json`) rather than normalized to the checklist naming

### `taxonomy-builder`

**Reconciled**
- checklist target is largely met: references, `assets/domain_packs/llm_agents.yaml`, and `assets/taxonomy_schema.json` are present
- named domain taxonomies now load from asset packs rather than inline Python prose

**Intentional compatibility-mode deviation**
- package includes an additional `gen_image` domain pack and companion reference beyond the original checklist; this is an acceptable extension, not a blocker

**Open follow-up**
- the generic fallback builder remains in Python, which matches the non-blocking follow-up already recorded in `docs/SKILLS_P0_WRITER_BATCH_REVIEW.md`
- minor CLI placeholder hygiene remains in `SKILL.md`

## Disposition Buckets

### Reconciled
- `front-matter-writer` missing reference / schema alias drift
- `subsection-writer` core reference-pack presence
- `taxonomy-builder` core checklist package shape

### Intentional compatibility-mode deviations
- `front-matter-writer` still writes prose from an externalized asset bank
- `subsection-writer` keeps a bootstrap assembly reference for compatibility
- `subsection-briefs` uses JSON packs instead of YAML packs
- `taxonomy-builder` ships an extra accepted domain pack (`gen_image`)

### Open follow-up
- `subsection-writer` schema/context naming and deeper script thinning
- `chapter-lead-writer` context-schema/context-jsonl alignment
- `subsection-briefs` missing `brief_schema.json`
- `taxonomy-builder` generic fallback builder still in Python

## Conclusion

The migrated P0 batch remains valid as a `C7` milestone.

This audit shows that the remaining checklist-to-filesystem gaps are mostly of three kinds:
- already reconciled by later remediation (`front-matter-writer`)
- compatibility-mode deviations that were intentionally accepted in the `C7` milestone
- open follow-up debt that should not be mistaken for retroactive failure of the P0 batch
