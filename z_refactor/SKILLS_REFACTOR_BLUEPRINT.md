# Skills Refactor Blueprint

## 1. Purpose

This document defines the current target state for the repo.

The active target is a repo where:

- skills are reference-first and script-thin
- pipelines are metadata-first and single-source
- helpers only materialize contracts instead of inventing them
- validation is strict enough to catch drift before it reaches user-facing artifacts

## 2. Core model

### 2.1 Skill contract

A skill is a layered package:

- `SKILL.md`: activation rule, workflow, guardrails, routing to references/assets
- `references/`: method, rubric, good/bad examples, domain reasoning
- `assets/`: machine-readable schemas, packs, templates, threshold tables
- `scripts/`: deterministic IO, normalization, validation, manifests, external tool calls

`run.py` is not the place for:

- reader-facing prose templates
- domain defaults
- hidden writer logic
- hidden fallback policy

### 2.2 Pipeline contract

A pipeline is also layered.

- frontmatter: machine-readable contract
- body prose: workflow explanation
- `UNITS.csv`: execution contract
- skill assets/references: fine-grained domain and probe logic

For the active refactor standard, the parse boundary is:

- machine-readable pipeline contract lives in frontmatter only
- machine-readable stage contract lives in a structured frontmatter field, not in Markdown prose
- Markdown body remains explanatory and may not be the only home of behavior-changing logic

If a value changes behavior, gate thresholds, retrieval width, writing depth, or deliverable shape, it belongs in machine-readable contract data, not only in prose.

### 2.3 Helper contract

Repo helpers may:

- read the active contract
- materialize it into workspace files
- normalize and validate inputs

Repo helpers may not:

- silently replace pipeline defaults
- carry their own domain policy
- create hidden survey/idea behavior that bypasses frontmatter and assets

### 2.4 Precedence model

The active precedence order is:

1. pipeline frontmatter defines the canonical default contract
2. `queries.md` is the workspace override surface, but only for fields the pipeline explicitly allows to be overridden
3. helpers may materialize frontmatter defaults into workspace files, but may not invent values
4. skill assets may further constrain or validate behavior, but may not silently broaden or replace the pipeline contract

## 3. Active standards

### 3.1 Metadata-first, not prose-first

Pipeline prose may explain:

- why a stage exists
- when to reroute or block
- what a checkpoint means

Pipeline prose may not be the only home for:

- `core_size`
- `per_subsection`
- `draft_profile`
- `evidence_mode`
- citation targets
- probe/fallback behavior
- variant behavior

### 3.2 Single-source, not duplicated siblings

If one pipeline is mostly another pipeline plus a small deliverable delta, it must be modeled as:

- base contract
- explicit variant override

It must not be maintained as two near-identical full specs and two near-identical units templates.

### 3.3 Explicit probe/fallback

Probe-like behavior is allowed when it is necessary, but it must be explicit.

Acceptable homes:

- pipeline contract fields
- stage outputs and unit acceptance
- skill `assets/` schemas and rubrics

Unacceptable homes:

- helper heuristics
- narrative notes
- hidden script fallbacks

### 3.4 Latest-active-only governance

`z_refactor` should only describe:

- the current standard
- the current open work
- the current execution order

It should not carry historical closed work as if it were still active.

## 4. Current open workstreams

Detailed design inputs that remain intentionally separate:

- `ANTHROPIC_SKILLS_DESIGN_PRINCIPLES.md`
- `SURVEY_PIPELINE_STRUCTURE_DESIGN.md`
- `SURVEY_PIPELINE_DESIGN_REVIEW.md`
- `SURVEY_PIPELINE_CONTRACT_CROSSWALK.md`

Ownership split for those survey docs:

- structure design owns the target workflow model
- design review owns risks and migration cautions
- contract crosswalk owns keep / move / replace / derive decisions for retained artifacts and migration cutovers

Redundant planning/checklist docs should be removed once their key points are absorbed into:

- this blueprint
- `STATUS.md`
- `UNITS.csv`
- `CHECKPOINTS.md`
- `DECISIONS.md`

### 4.1 Pipeline contract normalization

Needed because the current repo still spreads behavior across:

- pipeline prose
- `UNITS.csv` acceptance text
- helper fallbacks
- skill-level fallback logic

Target:

- machine-readable pipeline defaults
- machine-readable quality and stage contracts
- validator support for those fields

### 4.2 Survey base + LaTeX variant deduplication

Historical problem: `arxiv-survey-latex` used to be structurally a duplicate survey contract with a small PDF delta.

Target:

- one survey base contract
- one explicit LaTeX override

Current state:

- this is implemented; `arxiv-survey-latex` now resolves through `variant_of` + `variant_overrides`
- remaining work is validation and cleanup around the normalized contract, not variant dedup itself

Minimum schema expectation:

- `variant_of` points to the base pipeline
- `variant_overrides` contains the only allowed delta
- scalar and list fields replace
- mapping fields deep-merge unless explicitly replace-only

### 4.3 Helper policy externalization

Needed because generic helpers still carry survey/ideation policy.

Target:

- helpers read the active pipeline contract or skill assets
- helpers stop inventing defaults such as retrieval width or core size

### 4.4 Remaining compatibility debt

Still open:

- writer-side prose assembly in compatibility writers
- audit noise in `audit_skills.py`
- workspace-contract drift in `agent-survey-corpus`

## 5. Anti-patterns

The following are currently forbidden by the active standard:

- prose-only defaults for active pipelines
- duplicated variant pipelines maintained by hand
- helper-owned survey/idea defaults
- reader-facing prose materialized by deterministic scripts when the skill is supposed to be reference-first
- open findings docs that are not scoped to the current active backlog

## 6. Success condition

The refactor is considered complete only when all of the following are true:

- active pipelines use machine-readable contracts for behavior-critical defaults
- `arxiv-survey-latex` is a true variant instead of a duplicate sibling
- helpers no longer own pipeline policy
- remaining compatibility writers stop assembling reader-facing prose in `run.py`
- `audit_skills.py` is reliable enough to enforce the standard
- smoke validation confirms the normalized survey contract works on representative topics
