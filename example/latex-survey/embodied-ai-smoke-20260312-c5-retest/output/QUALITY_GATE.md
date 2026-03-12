# Quality gate log

- Append-only report sink for strict-mode unit checks (PASS/FAIL + next actions).
- When a unit is BLOCKED due to quality gate, read the latest entry here.

---

# Quality gate report

- Timestamp: `2026-03-11T17:22:29`
- Unit: `U001`
- Skill: `workspace-init`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:22:30`
- Unit: `U002`
- Skill: `pipeline-router`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:24:11`
- Unit: `U010`
- Skill: `literature-engineer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:24:12`
- Unit: `U020`
- Skill: `dedupe-rank`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:24:12`
- Unit: `U030`
- Skill: `taxonomy-builder`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:24:12`
- Unit: `U035`
- Skill: `chapter-skeleton`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:24:12`
- Unit: `U037`
- Skill: `section-bindings`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:24:12`
- Unit: `U038`
- Skill: `section-briefs`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:24:13`
- Unit: `U040`
- Skill: `outline-builder`

## Status

- FAIL

## Issues

- `outline_too_many_subsections`: Outline has too many subsections for survey-quality writing (12). Prefer <= 10 H3 subsections for this draft profile (fewer, thicker sections). Merge/simplify the taxonomy/outline so each H3 can sustain deeper evidence-first prose. Fix (skills-first): run `outline-budgeter` (NO PROSE) to merge adjacent H3s, then rerun `section-mapper` → `outline-refiner`.

## Next action

- Edit `outline/outline.yml`: rewrite every `TODO` bullet into topic-specific, checkable bullets (axes, comparisons, evaluation setups, failure modes).
- Keep it bullets-only (no prose paragraphs).
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/outline-builder/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U040` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U040 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-11T17:26:12`
- Unit: `U040`
- Skill: `outline-builder`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:26:13`
- Unit: `U050`
- Skill: `section-mapper`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:26:13`
- Unit: `U051`
- Skill: `outline-refiner`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:26:13`
- Unit: `U052`
- Skill: `pipeline-router`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:26:13`
- Unit: `U058`
- Skill: `pdf-text-extractor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:26:14`
- Unit: `U060`
- Skill: `paper-notes`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:26:14`
- Unit: `U075`
- Skill: `subsection-briefs`

## Status

- FAIL

## Issues

- `subsection_briefs_generic_axes`: `outline/subsection_briefs.jsonl` has subsection briefs dominated by generic axes (e.g., 3.3, 5.3); add subsection-specific mechanism/protocol/risk axes before writing.
- `subsection_briefs_repeated_tension`: `outline/subsection_briefs.jsonl` contains repeated `tension_statement` across subsections (e.g., 3.3,5.3,6.3). Rewrite tensions to be subsection-specific (this prevents repeated H3 openers / generator voice in C5).

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/subsection-briefs/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U075` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U075 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-11T17:30:14`
- Unit: `U075`
- Skill: `subsection-briefs`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:30:14`
- Unit: `U076`
- Skill: `chapter-briefs`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:30:14`
- Unit: `U090`
- Skill: `citation-verifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:30:14`
- Unit: `U091`
- Skill: `evidence-binder`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:15`
- Unit: `U092`
- Skill: `evidence-draft`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:15`
- Unit: `U0925`
- Skill: `table-schema`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:15`
- Unit: `U093`
- Skill: `anchor-sheet`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:15`
- Unit: `U0926`
- Skill: `table-filler`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:15`
- Unit: `U0927`
- Skill: `appendix-table-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:16`
- Unit: `U0935`
- Skill: `schema-normalizer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:16`
- Unit: `U099`
- Skill: `writer-context-pack`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:16`
- Unit: `U0995`
- Skill: `evidence-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:16`
- Unit: `U094`
- Skill: `claim-matrix-rewriter`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:17`
- Unit: `U095`
- Skill: `front-matter-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:17`
- Unit: `U096`
- Skill: `chapter-lead-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:17`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:18`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:18`
- Unit: `U102`
- Skill: `section-logic-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:19`
- Unit: `U1025`
- Skill: `argument-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:19`
- Unit: `U1026`
- Skill: `paragraph-curator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:19`
- Unit: `U1006`
- Skill: `style-harmonizer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:19`
- Unit: `U1007`
- Skill: `opener-variator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:19`
- Unit: `U098`
- Skill: `transition-weaver`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:19`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:20`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:20`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:20`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:31:20`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- FAIL

## Issues

- `draft_repeated_lines`: Draft contains repeated template-like lines (12×), e.g., `additional in-scope evidence for this comparison appears in , in , in , and in ....`; rewrite to be section-specific.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/draft-polisher/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U105` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U105 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-11T17:35:48`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:35:48`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:35:49`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:36:32`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:36:32`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:36:33`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:38:04`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:38:05`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:38:05`
- Unit: `U102`
- Skill: `section-logic-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:38:05`
- Unit: `U1025`
- Skill: `argument-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:38:06`
- Unit: `U1026`
- Skill: `paragraph-curator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:38:06`
- Unit: `U1006`
- Skill: `style-harmonizer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:38:06`
- Unit: `U1007`
- Skill: `opener-variator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:38:06`
- Unit: `U098`
- Skill: `transition-weaver`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:38:06`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:38:06`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:38:07`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:38:07`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:38:07`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:38:08`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:25`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:26`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:26`
- Unit: `U102`
- Skill: `section-logic-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:26`
- Unit: `U1025`
- Skill: `argument-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:26`
- Unit: `U1026`
- Skill: `paragraph-curator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:26`
- Unit: `U1006`
- Skill: `style-harmonizer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:27`
- Unit: `U1007`
- Skill: `opener-variator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:27`
- Unit: `U098`
- Skill: `transition-weaver`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:27`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:27`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:27`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:28`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:28`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:29`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:29`
- Unit: `U109`
- Skill: `pipeline-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:29`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T17:42:29`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T21:36:10`
- Unit: `U095`
- Skill: `front-matter-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T21:36:10`
- Unit: `U096`
- Skill: `chapter-lead-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T21:36:10`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T21:36:12`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_missing_contrast`: `sections/S3_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_1.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S6_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-11T21:42:46`
- Unit: `U095`
- Skill: `front-matter-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T21:42:46`
- Unit: `U096`
- Skill: `chapter-lead-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T21:42:47`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T21:42:48`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_missing_contrast`: `sections/S3_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_1.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S6_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-11T21:43:49`
- Unit: `U095`
- Skill: `front-matter-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T21:43:49`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T21:43:50`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_missing_contrast`: `sections/S3_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_1.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S6_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-11T21:44:45`
- Unit: `U095`
- Skill: `front-matter-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T21:44:45`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T21:44:46`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_missing_contrast`: `sections/S3_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_1.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S6_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-11T21:48:52`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_narration_template_opener`: `sections/S3_1.md` starts with narration-style template phrasing (e.g., 'This subsection ...'). Rewrite paragraph 1 as a content claim (tension/decision/lens) and end with the thesis.
- `sections_h3_narration_template_opener`: `sections/S3_2.md` starts with narration-style template phrasing (e.g., 'This subsection ...'). Rewrite paragraph 1 as a content claim (tension/decision/lens) and end with the thesis.
- `sections_h3_missing_contrast`: `sections/S3_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_1.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S5_1.md` lacks explicit contrast phrasing (need >= 2; found 0). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S5_2.md` lacks explicit contrast phrasing (need >= 2; found 0). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S6_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-11T22:05:08`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:05:18`
- Unit: `U102`
- Skill: `section-logic-polisher`

## Status

- FAIL

## Issues

- `section_logic_report_not_pass`: `output/SECTION_LOGIC_REPORT.md` is not PASS; fix paragraph-1 thesis / template-opener issues in the flagged H3 files and rerun `section-logic-polisher`.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/section-logic-polisher/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U102` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U102 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-11T22:06:19`
- Unit: `U102`
- Skill: `section-logic-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:06:19`
- Unit: `U1025`
- Skill: `argument-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:06:19`
- Unit: `U1026`
- Skill: `paragraph-curator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:06:20`
- Unit: `U1006`
- Skill: `style-harmonizer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:06:20`
- Unit: `U1007`
- Skill: `opener-variator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:06:20`
- Unit: `U098`
- Skill: `transition-weaver`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:06:20`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:06:20`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:06:21`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:06:21`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:06:21`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:06:22`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:10:53`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:10:53`
- Unit: `U109`
- Skill: `pipeline-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:10:53`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:10:53`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:11:43`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:11:43`
- Unit: `U109`
- Skill: `pipeline-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:11:43`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:11:43`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:14:04`
- Unit: `U1006`
- Skill: `style-harmonizer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:14:04`
- Unit: `U1007`
- Skill: `opener-variator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:14:04`
- Unit: `U098`
- Skill: `transition-weaver`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:14:04`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:14:04`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:14:05`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:14:05`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:14:05`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:14:06`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:15:29`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:15:30`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:15:31`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:15:31`
- Unit: `U109`
- Skill: `pipeline-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:15:31`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:15:31`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:18:35`
- Unit: `U140`
- Skill: `latex-scaffold`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:18:44`
- Unit: `U150`
- Skill: `latex-compile-qa`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:20:31`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:20:31`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:20:31`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:20:32`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- FAIL

## Issues

- `citation_injection_failed`: `output/CITATION_INJECTION_REPORT.md` is not PASS; add more in-scope unused citations (or expand C1/C2 mapping), then rerun citation injection.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/citation-injector/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1045` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1045 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-11T22:21:49`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:21:49`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:21:50`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:21:50`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- FAIL

## Issues

- `citation_injection_failed`: `output/CITATION_INJECTION_REPORT.md` is not PASS; add more in-scope unused citations (or expand C1/C2 mapping), then rerun citation injection.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/citation-injector/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1045` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1045 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-11T22:22:34`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:22:34`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:22:35`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:22:35`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- FAIL

## Issues

- `citation_injection_failed`: `output/CITATION_INJECTION_REPORT.md` is not PASS; add more in-scope unused citations (or expand C1/C2 mapping), then rerun citation injection.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/citation-injector/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1045` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1045 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-11T22:23:46`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:23:47`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:23:47`
- Unit: `U109`
- Skill: `pipeline-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:23:48`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- FAIL

## Issues

- `contract_report_not_pass`: `output/CONTRACT_REPORT.md` is not PASS (or pipeline not complete). Fix missing artifacts / unit statuses and rerun `artifact-contract-auditor`.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/artifact-contract-auditor/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U130` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U130 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-11T22:24:37`
- Unit: `U140`
- Skill: `latex-scaffold`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:24:43`
- Unit: `U150`
- Skill: `latex-compile-qa`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:24:43`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-11T22:24:44`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T00:33:58`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T00:33:58`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T00:33:58`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T00:33:59`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T00:34:30`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T00:34:30`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T00:34:30`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T00:34:31`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T00:35:08`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T00:35:09`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T00:35:35`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:45:14`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:45:15`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_missing_contrast`: `sections/S3_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_1.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S6_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T10:48:10`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:48:10`
- Unit: `U102`
- Skill: `section-logic-polisher`

## Status

- FAIL

## Issues

- `section_logic_report_not_pass`: `output/SECTION_LOGIC_REPORT.md` is not PASS; fix paragraph-1 thesis / template-opener issues in the flagged H3 files and rerun `section-logic-polisher`.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/section-logic-polisher/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U102` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U102 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T10:48:51`
- Unit: `U102`
- Skill: `section-logic-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:48:51`
- Unit: `U1025`
- Skill: `argument-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:48:51`
- Unit: `U1026`
- Skill: `paragraph-curator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:48:51`
- Unit: `U1006`
- Skill: `style-harmonizer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:48:52`
- Unit: `U1007`
- Skill: `opener-variator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:48:52`
- Unit: `U098`
- Skill: `transition-weaver`

## Status

- FAIL

## Issues

- `transitions_too_short`: `outline/transitions.md` has too few within-chapter H3→H3 transitions (found=0, expected>=8 from `outline/outline.yml`).

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/transition-weaver/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U098` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U098 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T10:49:04`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:49:05`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:49:05`
- Unit: `U102`
- Skill: `section-logic-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:49:05`
- Unit: `U1025`
- Skill: `argument-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:49:06`
- Unit: `U1026`
- Skill: `paragraph-curator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:49:06`
- Unit: `U1006`
- Skill: `style-harmonizer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:49:06`
- Unit: `U1007`
- Skill: `opener-variator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:49:06`
- Unit: `U098`
- Skill: `transition-weaver`

## Status

- FAIL

## Issues

- `transitions_too_short`: `outline/transitions.md` has too few within-chapter H3→H3 transitions (found=0, expected>=8 from `outline/outline.yml`).

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/transition-weaver/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U098` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U098 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T10:49:58`
- Unit: `U098`
- Skill: `transition-weaver`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:49:58`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:49:58`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:49:58`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:49:59`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- FAIL

## Issues

- `citation_injection_failed`: `output/CITATION_INJECTION_REPORT.md` is not PASS; add more in-scope unused citations (or expand C1/C2 mapping), then rerun citation injection.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/citation-injector/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1045` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1045 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T10:50:30`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:50:31`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:50:31`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:50:32`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:51:29`
- Unit: `U096`
- Skill: `chapter-lead-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:51:30`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:51:30`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:51:31`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:51:31`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:51:31`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:51:32`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:51:32`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:52:08`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:52:08`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- FAIL

## Issues

- `post_merge_planner_talk_remaining_uncertainty`: planner-talk transition stem ('the remaining uncertainty is...') (source: draft)

## Next action

- Open `output/POST_MERGE_VOICE_REPORT.md` and fix the earliest responsible artifact it points to.
- If the report says `source: transitions`: rewrite `outline/transitions.md` as content-bearing argument bridges (no planner talk, no A/B/C slash labels), then rerun `section-merger` and this gate.
- If the report says `source: draft`: route to `writer-selfloop` / `subsection-polisher` / `draft-polisher` for the flagged section, then rerun `section-merger` and this gate.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/post-merge-voice-gate/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U103` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U103 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T10:52:24`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:52:25`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_missing_contrast`: `sections/S3_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_1.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S6_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T10:53:46`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_missing_contrast`: `sections/S3_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_1.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S6_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T10:54:09`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:54:10`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:54:10`
- Unit: `U102`
- Skill: `section-logic-polisher`

## Status

- FAIL

## Issues

- `section_logic_report_not_pass`: `output/SECTION_LOGIC_REPORT.md` is not PASS; fix paragraph-1 thesis / template-opener issues in the flagged H3 files and rerun `section-logic-polisher`.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/section-logic-polisher/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U102` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U102 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T10:54:18`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:54:19`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:54:19`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:54:20`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:54:20`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:55:03`
- Unit: `U109`
- Skill: `pipeline-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:55:03`
- Unit: `U140`
- Skill: `latex-scaffold`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:55:10`
- Unit: `U150`
- Skill: `latex-compile-qa`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:55:10`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:55:10`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:55:51`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:55:51`
- Unit: `U102`
- Skill: `section-logic-polisher`

## Status

- FAIL

## Issues

- `section_logic_report_not_pass`: `output/SECTION_LOGIC_REPORT.md` is not PASS; fix paragraph-1 thesis / template-opener issues in the flagged H3 files and rerun `section-logic-polisher`.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/section-logic-polisher/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U102` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U102 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T10:56:16`
- Unit: `U102`
- Skill: `section-logic-polisher`

## Status

- FAIL

## Issues

- `section_logic_report_not_pass`: `output/SECTION_LOGIC_REPORT.md` is not PASS; fix paragraph-1 thesis / template-opener issues in the flagged H3 files and rerun `section-logic-polisher`.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/section-logic-polisher/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U102` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U102 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:25`
- Unit: `U096`
- Skill: `chapter-lead-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:25`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:27`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:27`
- Unit: `U102`
- Skill: `section-logic-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:27`
- Unit: `U1025`
- Skill: `argument-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:27`
- Unit: `U1026`
- Skill: `paragraph-curator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:27`
- Unit: `U1006`
- Skill: `style-harmonizer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:27`
- Unit: `U1007`
- Skill: `opener-variator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:28`
- Unit: `U098`
- Skill: `transition-weaver`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:28`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:28`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:28`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:29`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:29`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:57:30`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:58:16`
- Unit: `U102`
- Skill: `section-logic-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:58:16`
- Unit: `U1025`
- Skill: `argument-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:58:16`
- Unit: `U1026`
- Skill: `paragraph-curator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:58:17`
- Unit: `U1006`
- Skill: `style-harmonizer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:58:17`
- Unit: `U1007`
- Skill: `opener-variator`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:58:17`
- Unit: `U098`
- Skill: `transition-weaver`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:58:17`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:58:17`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:58:18`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:58:18`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:58:19`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:58:19`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:59:08`
- Unit: `U109`
- Skill: `pipeline-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:59:08`
- Unit: `U140`
- Skill: `latex-scaffold`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:59:10`
- Unit: `U150`
- Skill: `latex-compile-qa`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:59:10`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T10:59:10`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:00:23`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_missing_contrast`: `sections/S3_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S4_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S6_3.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T11:00:55`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:00:55`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:00:55`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:00:56`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- FAIL

## Issues

- `citation_injection_failed`: `output/CITATION_INJECTION_REPORT.md` is not PASS; add more in-scope unused citations (or expand C1/C2 mapping), then rerun citation injection.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/citation-injector/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1045` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1045 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T11:02:04`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:02:04`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:02:05`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:03:03`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:03:03`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:03:03`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- FAIL

## Issues

- `citation_anchoring_drift`: Citation anchoring drift in H3 `Benchmarks, metrics, and generalization`: removed {Dalal2025Unlocking, Gao2024Vision, Liu2026Adaptation, Rubavicius2024Secure, Schmidgall2024General, Zhang2025Agentworld}, added {}. Polishing must not move citations across subsections; keep cite keys in the same H3, or delete `output/citation_anchors.prepolish.jsonl` to intentionally reset.
- `citation_anchoring_drift`: Citation anchoring drift in H3 `Manipulation, navigation, and task scope`: removed {Li2025Embodiment, Shaji2026From, Sridhar2025Ricl, Vo2025Clutter, Ye2026St4Vla, Yenamandra2023Homerobot}, added {}. Polishing must not move citations across subsections; keep cite keys in the same H3, or delete `output/citation_anchors.prepolish.jsonl` to intentionally reset.
- `citation_anchoring_drift`: Citation anchoring drift in H3 `Observation, action, and embodiment interfaces`: removed {Piergiovanni2018Learning, Zhang2025Safevla}, added {}. Polishing must not move citations across subsections; keep cite keys in the same H3, or delete `output/citation_anchors.prepolish.jsonl` to intentionally reset.
- `citation_anchoring_drift`: Citation anchoring drift in H3 `Post-training, feedback, and continual improvement`: removed {Fu2025Metis, Hou2025Visual, Sanghai2024Advances, Sharma2026World, Su2026Interaction, Yao2023Bridging}, added {}. Polishing must not move citations across subsections; keep cite keys in the same H3, or delete `output/citation_anchors.prepolish.jsonl` to intentionally reset.
- `citation_anchoring_drift`: Citation anchoring drift in H3 `Pretraining data and supervision`: removed {Gong2025Anytask, Gu2025Igen, Spiridonov2025Generalist, Wu2026Pragmatic, Zhang2025Robowheel, Zhao2025Framework}, added {}. Polishing must not move citations across subsections; keep cite keys in the same H3, or delete `output/citation_anchors.prepolish.jsonl` to intentionally reset.
- `citation_anchoring_drift`: Citation anchoring drift in H3 `Safety, reliability, and real-world deployment`: removed {Agia2024Unpacking, Etukuru2024Robot, Fang2025Saga, Jiang2025Galaxea, Kawaharazuka2024Real, Li2025Worldeval}, added {}. Polishing must not move citations across subsections; keep cite keys in the same H3, or delete `output/citation_anchors.prepolish.jsonl` to intentionally reset.
- `citation_anchoring_drift`: Citation anchoring drift in H3 `Vision-language-action and policy backbones`: removed {Adang2025Singer, Heo2026Anycamvla, Liu2025Faster, Ma2024Survey, Team2025Gigabrain, Wu2025Momanipvla}, added {}. Polishing must not move citations across subsections; keep cite keys in the same H3, or delete `output/citation_anchors.prepolish.jsonl` to intentionally reset.
- `citation_anchoring_drift`: Citation anchoring drift in H3 `World models, planning, and reasoning`: removed {Da2025Survey, Lee2026Roboreward, Stone2023Open, Wang2025Odyssey, Yang2023Foundation, Yue2024Deer}, added {}. Polishing must not move citations across subsections; keep cite keys in the same H3, or delete `output/citation_anchors.prepolish.jsonl` to intentionally reset.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/draft-polisher/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U105` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U105 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T11:03:04`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:03:04`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:03:05`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:03:05`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:03:06`
- Unit: `U109`
- Skill: `pipeline-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:03:06`
- Unit: `U140`
- Skill: `latex-scaffold`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:03:12`
- Unit: `U150`
- Skill: `latex-compile-qa`

## Status

- FAIL

## Issues

- `latex_float_too_large`: LaTeX build still has `Float too large for page` warnings; shrink or split oversized tables/figures and recompile.

## Next action

- Open `output/LATEX_BUILD_REPORT.md` and fix the first compile error (missing package, missing bib, bad cite key).
- Ensure `latexmk` is installed and `latex/main.tex` references `../citations/ref.bib`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/latex-compile-qa/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U150` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U150 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T11:03:23`
- Unit: `U150`
- Skill: `latex-compile-qa`

## Status

- FAIL

## Issues

- `latex_float_too_large`: LaTeX build still has `Float too large for page` warnings; shrink or split oversized tables/figures and recompile.

## Next action

- Open `output/LATEX_BUILD_REPORT.md` and fix the first compile error (missing package, missing bib, bad cite key).
- Ensure `latexmk` is installed and `latex/main.tex` references `../citations/ref.bib`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/latex-compile-qa/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U150` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U150 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T11:04:59`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:04:59`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:04:59`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:05:00`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:05:00`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:05:01`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:05:01`
- Unit: `U109`
- Skill: `pipeline-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:05:01`
- Unit: `U140`
- Skill: `latex-scaffold`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:05:06`
- Unit: `U150`
- Skill: `latex-compile-qa`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:05:06`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:05:06`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:05:08`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:05:52`
- Unit: `U140`
- Skill: `latex-scaffold`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:05:53`
- Unit: `U150`
- Skill: `latex-compile-qa`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:05:53`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:05:53`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:27:51`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T11:39:16`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_intro_too_short`: `sections/S1.md` (Introduction) looks too short (2576 chars after removing citations; min=3200). Expand motivation/scope/contributions and keep claims citation-grounded. Fix: expand motivation + scope boundary + one evidence-policy paragraph + organization preview; keep paper voice (avoid outline narration like 'This subsection...').
- `sections_related_work_sparse_citations`: `sections/S2.md` (Related Work) cites too few unique papers (48; min=50). Increase concrete, cite-grounded positioning and coverage. Fix: expand positioning vs adjacent lines of work + survey coverage + one evidence-policy paragraph + organization preview; avoid a dedicated 'Prior Surveys' mini-section by default; keep third-person academic voice (avoid 'this/current survey' deictic phrasing).
- `sections_related_work_too_short`: `sections/S2.md` (Related Work) looks too short (2752 chars after removing citations; min=3800). Expand motivation/scope/contributions and keep claims citation-grounded. Fix: expand positioning vs adjacent lines of work + survey coverage + one evidence-policy paragraph + organization preview; avoid a dedicated 'Prior Surveys' mini-section by default; keep third-person academic voice (avoid 'this/current survey' deictic phrasing).

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T11:46:33`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_intro_too_short`: `sections/S1.md` (Introduction) looks too short (2288 chars after removing citations; min=3200). Expand motivation/scope/contributions and keep claims citation-grounded. Fix: expand motivation + scope boundary + one evidence-policy paragraph + organization preview; keep paper voice (avoid outline narration like 'This subsection...').
- `sections_related_work_sparse_citations`: `sections/S2.md` (Related Work) cites too few unique papers (48; min=50). Increase concrete, cite-grounded positioning and coverage. Fix: expand positioning vs adjacent lines of work + survey coverage + one evidence-policy paragraph + organization preview; avoid a dedicated 'Prior Surveys' mini-section by default; keep third-person academic voice (avoid 'this/current survey' deictic phrasing).
- `sections_related_work_too_short`: `sections/S2.md` (Related Work) looks too short (2532 chars after removing citations; min=3800). Expand motivation/scope/contributions and keep claims citation-grounded. Fix: expand positioning vs adjacent lines of work + survey coverage + one evidence-policy paragraph + organization preview; avoid a dedicated 'Prior Surveys' mini-section by default; keep third-person academic voice (avoid 'this/current survey' deictic phrasing).
- `sections_related_work_too_few_paragraphs`: `sections/S2.md` (Related Work) has too few substantive paragraphs (8; min=10). Avoid bullet-only structure; write full paragraphs with citations. Fix: expand positioning vs adjacent lines of work + survey coverage + one evidence-policy paragraph + organization preview; avoid a dedicated 'Prior Surveys' mini-section by default; keep third-person academic voice (avoid 'this/current survey' deictic phrasing).

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T11:47:59`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_intro_too_short`: `sections/S1.md` (Introduction) looks too short (2721 chars after removing citations; min=3200). Expand motivation/scope/contributions and keep claims citation-grounded. Fix: expand motivation + scope boundary + one evidence-policy paragraph + organization preview; keep paper voice (avoid outline narration like 'This subsection...').
- `sections_related_work_too_short`: `sections/S2.md` (Related Work) looks too short (2848 chars after removing citations; min=3800). Expand motivation/scope/contributions and keep claims citation-grounded. Fix: expand positioning vs adjacent lines of work + survey coverage + one evidence-policy paragraph + organization preview; avoid a dedicated 'Prior Surveys' mini-section by default; keep third-person academic voice (avoid 'this/current survey' deictic phrasing).
- `sections_related_work_too_few_paragraphs`: `sections/S2.md` (Related Work) has too few substantive paragraphs (9; min=10). Avoid bullet-only structure; write full paragraphs with citations. Fix: expand positioning vs adjacent lines of work + survey coverage + one evidence-policy paragraph + organization preview; avoid a dedicated 'Prior Surveys' mini-section by default; keep third-person academic voice (avoid 'this/current survey' deictic phrasing).

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T12:13:21`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_intro_too_short`: `sections/S1.md` (Introduction) looks too short (2213 chars after removing citations; min=3200). Expand motivation/scope/contributions and keep claims citation-grounded. Fix: expand motivation + scope boundary + one evidence-policy paragraph + organization preview; keep paper voice (avoid outline narration like 'This subsection...').
- `sections_intro_too_few_paragraphs`: `sections/S1.md` (Introduction) has too few substantive paragraphs (7; min=8). Avoid bullet-only structure; write full paragraphs with citations. Fix: expand motivation + scope boundary + one evidence-policy paragraph + organization preview; keep paper voice (avoid outline narration like 'This subsection...').
- `sections_related_work_too_short`: `sections/S2.md` (Related Work) looks too short (2655 chars after removing citations; min=3800). Expand motivation/scope/contributions and keep claims citation-grounded. Fix: expand positioning vs adjacent lines of work + survey coverage + one evidence-policy paragraph + organization preview; avoid a dedicated 'Prior Surveys' mini-section by default; keep third-person academic voice (avoid 'this/current survey' deictic phrasing).
- `sections_related_work_too_few_paragraphs`: `sections/S2.md` (Related Work) has too few substantive paragraphs (8; min=10). Avoid bullet-only structure; write full paragraphs with citations. Fix: expand positioning vs adjacent lines of work + survey coverage + one evidence-policy paragraph + organization preview; avoid a dedicated 'Prior Surveys' mini-section by default; keep third-person academic voice (avoid 'this/current survey' deictic phrasing).

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T12:35:56`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_sparse_citations`: `sections/S3_1.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S3_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S3_2.md` has <12 unique citations (9); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S3_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S3_3.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S3_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S4_1.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S4_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S4_2.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S4_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S4_3.md` has <12 unique citations (7); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S4_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S5_1.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S5_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S5_2.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S5_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S5_3.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S5_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S6_1.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S6_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S6_2.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S6_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S6_3.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S6_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T12:36:16`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_sparse_citations`: `sections/S3_1.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S3_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S3_2.md` has <12 unique citations (9); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S3_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S3_3.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S3_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S4_1.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S4_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S4_2.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S4_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S4_3.md` has <12 unique citations (7); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S4_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S5_1.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S5_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S5_2.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S5_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S5_3.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S5_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S6_1.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S6_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S6_2.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S6_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S6_3.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S6_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T12:38:07`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_intro_sparse_citations`: `sections/S1.md` (Introduction) cites too few unique papers (0; min=35). Increase concrete, cite-grounded positioning and coverage. Fix: expand motivation + scope boundary + one evidence-policy paragraph + organization preview; keep paper voice (avoid outline narration like 'This subsection...').
- `sections_related_work_sparse_citations`: `sections/S2.md` (Related Work) cites too few unique papers (0; min=50). Increase concrete, cite-grounded positioning and coverage. Fix: expand positioning vs adjacent lines of work + survey coverage + one evidence-policy paragraph + organization preview; avoid a dedicated 'Prior Surveys' mini-section by default; keep third-person academic voice (avoid 'this/current survey' deictic phrasing).
- `sections_h3_sparse_citations`: `sections/S3_1.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S3_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S3_2.md` has <12 unique citations (9); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S3_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S3_3.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S3_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S4_1.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S4_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S4_2.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S4_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S4_3.md` has <12 unique citations (7); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S4_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S5_1.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S5_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S5_2.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S5_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S5_3.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S5_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S6_1.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S6_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S6_2.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S6_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S6_3.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S6_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T12:39:23`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_sparse_citations`: `sections/S3_1.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S3_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S3_2.md` has <12 unique citations (9); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S3_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S3_3.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S3_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S4_1.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S4_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S4_2.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S4_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S4_3.md` has <12 unique citations (7); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S4_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S5_1.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S5_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S5_2.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S5_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S5_3.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S5_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S6_1.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S6_1.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S6_2.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S6_2.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.
- `sections_h3_sparse_citations`: `sections/S6_3.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_few_paragraphs`: `sections/S6_3.md` has too few paragraphs (9); aim for 10–12 paragraphs per H3 for this draft profile.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T12:40:11`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_sparse_citations`: `sections/S3_1.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S3_2.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S3_3.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S4_1.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S4_2.md` has <12 unique citations (9); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S4_3.md` has <12 unique citations (8); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S5_1.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S5_2.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S5_3.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S6_2.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S6_3.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T12:41:21`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_sparse_citations`: `sections/S3_2.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S3_3.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S4_1.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S4_2.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S4_3.md` has <12 unique citations (9); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S5_1.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S5_2.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S5_3.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S6_3.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T12:44:55`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_sparse_citations`: `sections/S4_1.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_sparse_citations`: `sections/S4_2.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T12:46:04`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_sparse_citations`: `sections/S4_1.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T12:47:23`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- FAIL

## Issues

- `post_merge_planner_talk_comparison_lens`: meta phrase 'comparison lens' (often reads like planning) (source: draft)

## Next action

- Open `output/POST_MERGE_VOICE_REPORT.md` and fix the earliest responsible artifact it points to.
- If the report says `source: transitions`: rewrite `outline/transitions.md` as content-bearing argument bridges (no planner talk, no A/B/C slash labels), then rerun `section-merger` and this gate.
- If the report says `source: draft`: route to `writer-selfloop` / `subsection-polisher` / `draft-polisher` for the flagged section, then rerun `section-merger` and this gate.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/post-merge-voice-gate/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U103` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U103 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-03-12T12:52:31`
- Unit: `U999`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T13:53:22`
- Unit: `U999`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-03-12T14:15:24`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_too_short`: `sections/S4_1.md` looks too short (4212 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_sparse_citations`: `sections/S4_2.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_short`: `sections/S4_2.md` looks too short (3430 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_too_short`: `sections/S4_3.md` looks too short (4830 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_too_short`: `sections/S5_1.md` looks too short (4089 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_sparse_citations`: `sections/S5_3.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).
