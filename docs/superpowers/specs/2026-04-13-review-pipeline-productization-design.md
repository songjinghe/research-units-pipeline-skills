# Review Pipeline Productization Design

## Goal

Reframe three existing review-oriented workflows around user-facing jobs to be done:

- `research-brief` for fast topic understanding
- `paper-review` for single-paper assessment
- `evidence-review` for evidence synthesis with optional systematic rigor

The implementation should preserve current execution capabilities, keep legacy names working, and make the new names the only primary entrypoints in repo docs.

## Problem

The current execution boundaries are mostly sound, but the product layer is not:

- `lit-snapshot` is an internal name, not a user-facing task name.
- `peer-review` is too narrow for the broader paper-assessment use case.
- `systematic-review` is professionally precise but too specialized for the default front-door product label.

This creates avoidable friction at exactly the layer where a user decides "is this the thing I need?"

## Design

### 1. Keep three execution contracts, rename the products

Do not collapse these into one mega-pipeline. The input surfaces, checkpoints, and outputs are materially different.

Canonical product names:

- `research-brief`
- `paper-review`
- `evidence-review`

Legacy compatibility names:

- `lit-snapshot` -> alias of `research-brief`
- `peer-review` -> alias of `paper-review`
- `systematic-review` -> alias of `evidence-review`

### 2. Use thin alias pipeline files, not wrapper logic

Canonical pipelines get their own real contract files.

Legacy names remain as tiny `variant_of` files with:

- `docs_hidden: true`
- empty routing hints
- lower routing priority

This keeps execution compatibility while preventing old names from being shown in generated docs and top-level product copy.

### 3. Promote these three as first-class user workflows

README and workflow docs should present:

- `latex-survey`
- `research-brief`
- `paper-review`
- `evidence-review`
- `idea-brainstorm`
- `source-tutorial`
- `graduate-paper`

The old names should not appear as primary options in README tables or guides.

### 4. Keep deliverables stable for now

Do not rename internal output files in this pass.

Reason:

- Renaming outputs (`SNAPSHOT.md` -> `BRIEF.md`, etc.) would cascade into many skills, tests, and workspaces.
- The user-facing improvement comes mainly from product naming, routing, and docs.
- Output-file renaming can be a later compatibility-managed pass if still desired.

So:

- `research-brief` still produces `output/SNAPSHOT.md`
- `paper-review` still produces `output/REVIEW.md`
- `evidence-review` still produces `output/SYNTHESIS.md`

### 5. Upgrade the three pipelines to frontmatter-first contracts

The new canonical files should be `contract_model: pipeline.frontmatter/v1` where practical.

This gives:

- cleaner machine-readable validation
- better generated docs
- more consistent product contracts alongside `source-tutorial`, `idea-brainstorm`, and `arxiv-survey`

### 6. Keep router compatibility simple

Routing rules should point new user-language queries to the new names.

Examples:

- "brief", "rapid review", "topic overview", "research brief" -> `research-brief`
- "paper review", "paper critique", "assess this paper", "peer review", "referee" -> `paper-review`
- "evidence review", "systematic review", "PRISMA" -> `evidence-review`

`resolve_pipeline_spec_path()` and `scripts/pipeline.py` should normalize legacy names to new canonical names.

## Scope

### In scope

- new canonical pipeline files
- legacy alias pipeline files
- alias normalization updates
- README / guide updates
- router docs and runner docs
- generated skill dependency docs
- tests for canonical names and aliases

### Out of scope

- renaming internal skill names
- renaming output artifact filenames
- redesigning the thesis workflow
- introducing a single giant "review-studio" execution contract

## Validation

Required checks:

- new canonical pipelines load successfully
- legacy names still resolve to new canonical pipelines
- docs generation hides legacy aliases
- repo validation passes
- review pipeline tests pass on main branch

## File map

- Add:
  - `pipelines/research-brief.pipeline.md`
  - `pipelines/paper-review.pipeline.md`
  - `pipelines/evidence-review.pipeline.md`
  - `readme/research-brief.md`
  - `readme/research-brief.zh-CN.md`
  - `readme/paper-review.md`
  - `readme/paper-review.zh-CN.md`
  - `readme/evidence-review.md`
  - `readme/evidence-review.zh-CN.md`
  - `tests/test_review_pipeline_productization.py`
- Modify:
  - `pipelines/lit-snapshot.pipeline.md`
  - `pipelines/peer-review.pipeline.md`
  - `pipelines/systematic-review.pipeline.md`
  - `README.md`
  - `README.zh-CN.md`
  - `SKILL_INDEX.md`
  - `docs/PIPELINE_FLOWS.md`
  - `docs/SKILL_DEPENDENCIES.md`
  - `scripts/generate_skill_graph.py`
  - `scripts/pipeline.py`
  - `tooling/common.py`
  - `.codex/skills/pipeline-router/SKILL.md`
  - `.codex/skills/pipeline-router/scripts/run.py`
  - `.codex/skills/research-pipeline-runner/SKILL.md`
  - `tooling/pipeline_spec.py`

