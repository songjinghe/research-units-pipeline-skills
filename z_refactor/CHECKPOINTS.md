# Checkpoints

## C0 - z_refactor baseline rewritten
Criteria:
- [x] `STATUS.md`, `UNITS.csv`, `CHECKPOINTS.md`, and `DECISIONS.md` describe the current workstream rather than historical closed work
- [x] the governance surface only tracks current standards and current open work

## C1 - Latest-standard contract boundaries locked
Criteria:
- [x] the docs clearly distinguish pipeline frontmatter vs `UNITS.csv` vs skill `assets/references`
- [x] pipeline specs are treated as first-class contract surfaces
- [x] Anthropic skill-design principles are summarized locally as an input to the current refactor standard

## C2 - Active backlog aligned
Criteria:
- [x] only currently open workstreams remain in `UNITS.csv`
- [x] remaining units map to the current standards in the governing docs

## C3 - Metadata-first pipeline contract implemented
Criteria:
- [x] retrieval-informed survey structure is documented in `z_refactor/SURVEY_PIPELINE_STRUCTURE_DESIGN.md` as the target model for the next contract migration batch
- [x] the proposed structure has a written design review (`z_refactor/SURVEY_PIPELINE_DESIGN_REVIEW.md`) that identifies the minimum contract changes and the highest-risk migration steps before implementation starts
- [x] the survey contract crosswalk (`z_refactor/SURVEY_PIPELINE_CONTRACT_CROSSWALK.md`) closes keep/insert/replace/derive ambiguity for the retained structure artifacts before code changes start
- [x] parse boundary, precedence model, variant model, checkpoint placement, and stable-H3 cutover are explicit in the governing docs before `U130/U140/U150/U155`
- [x] pipeline frontmatter exposes machine-readable defaults, quality contract, and stage contract fields
- [x] `tooling/pipeline_spec.py` and `scripts/validate_repo.py` parse and validate those fields

## C4 - Defaults normalization and ideation tightening still pending
Criteria:
- [x] `arxiv-survey-latex` is an explicit variant of the survey base contract with only a small latex/pdf delta rather than a copy-on-write full-list override block
- [ ] survey and idea helpers no longer invent defaults that can drift from the active contract
- [x] `idea-brief` is packaged reference-first, with reusable method in `references/` and machine-readable kickoff contract in `assets/`
- [x] ideation runtime and QA consume only explicit contract surfaces rather than hidden scoring/selection policy or duplicate local rules
- [x] the section-first survey layer is inserted before subsection mapping and before downstream writer cleanup begins
- [x] chapter-level section binding outcomes fail closed: `hold_or_merge` materializes as structured `REROUTE` rather than silently advancing as `PASS`

## C5 - Remaining Anthropic cleanup validated
Criteria:
- [x] `section-logic-polisher` acceptance and runtime gating agree on whether a `FAIL` report should block the run
- [ ] writer-side prose assembly is removed from the remaining compatibility writers
- [ ] reader-visible survey previews are only treated as validated when upstream writer changes still leave `WRITER_SELFLOOP_TODO.md` and `AUDIT_REPORT.md` in PASS, not merely when LaTeX compiles
- [ ] `audit_skills.py` is trustworthy enough to act as a strict gate
- [ ] workspace-contract drift is removed from `agent-survey-corpus`
- [x] representative survey smoke runs pass under the normalized contract
