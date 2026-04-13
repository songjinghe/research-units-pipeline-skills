# research-units-pipeline-skills

> Languages: **English** | [简体中文](README.zh-CN.md)

This project uses semantic skills to turn research workflows into reusable pipelines.

It is designed for the space between fragile prompting and overly rigid scripting. By organizing research tasks into staged pipelines with explicit artifacts, checkpoints, and guardrails, it makes complex work more reusable, inspectable, and iterative. The result is a workflow that can be resumed, audited, and continuously improved instead of being rebuilt from scratch each time.

## What This Repo Covers

The codebase currently centers on seven workflows:

| Workflow | Use it for | Default deliverable | English | 中文 |
|---|---|---|---|---|
| `latex-survey` | evidence-first literature surveys with optional LaTeX/PDF delivery | `output/DRAFT.md`, `latex/main.tex`, `latex/main.pdf` | [Guide](readme/latex-survey.md) | [说明](readme/latex-survey.zh-CN.md) |
| `research-brief` | fast topic understanding and reading-path briefs from a small paper set | `output/SNAPSHOT.md` | [Guide](readme/research-brief.md) | [说明](readme/research-brief.zh-CN.md) |
| `paper-review` | traceable single-paper critique, lab review, or referee-style assessment | `output/REVIEW.md` | [Guide](readme/paper-review.md) | [说明](readme/paper-review.zh-CN.md) |
| `evidence-review` | protocol-driven evidence synthesis with screening, extraction, and bounded conclusions | `output/SYNTHESIS.md` | [Guide](readme/evidence-review.md) | [说明](readme/evidence-review.zh-CN.md) |
| `idea-brainstorm` | literature-grounded research direction discovery and discussion memos | `output/REPORT.md` | [Guide](readme/idea-brainstorm.md) | [说明](readme/idea-brainstorm.zh-CN.md) |
| `source-tutorial` | transform multi-source materials into a reader-first tutorial with PDF and Beamer slides | `output/TUTORIAL.md`, `latex/main.pdf`, `latex/slides/main.pdf` | [Guide](readme/source-tutorial.md) | [说明](readme/source-tutorial.zh-CN.md) |
| `graduate-paper` | restructuring an existing Chinese graduation thesis project into a thesis engineering workflow | pipeline + thesis skill packages | [Guide](readme/graduate-paper.md) | [说明](readme/graduate-paper.zh-CN.md) |

These workflows share the same architecture:

- `pipelines/` defines stage contracts, artifact expectations, and required skills.
- `.codex/skills/` holds the reusable skills. (100 skills)
- `workspaces/` stores per-run artifacts and intermediate outputs.
- `readme/` contains feature-level documentation.

## Core Concepts

- `Pipeline`: the contract for a workflow. It defines stages, artifacts, checkpoints, and required skills.
- `Skill`: a reusable capability with explicit inputs, outputs, acceptance criteria, and guardrails.
- `Workspace`: the working directory for a single run under `workspaces/<name>/`, where generated artifacts are written.

The important design choice is artifact-first execution. The model is not expected to keep the whole workflow in memory; it writes intermediate structure, evidence, and review outputs to disk so later stages can build on them.

## When To Use Which Workflow

Use `latex-survey` when the goal is a serious review paper with explicit retrieval, structure review, evidence packs, writing loops, and optional PDF output.

Use `research-brief` when the goal is to understand a topic quickly, surface the key themes, and produce a reading path rather than a full survey.

Use `paper-review` when the input is a single paper or manuscript and the goal is to assess its claims, evidence, novelty, and risks.

Use `evidence-review` when the goal is to synthesize a candidate pool under an explicit protocol with screening, extraction, and bounded conclusions.

Use `idea-brainstorm` when the goal is to generate a literature-backed memo of candidate research directions for discussion, not to write a paper yet.

Use `source-tutorial` when you already have webpages, PDFs, notes, repo docs, or documentation sites and want to turn them into a reader-first tutorial rather than a survey or memo.

Use `graduate-paper` when you already have thesis materials such as a template, existing TeX, Overleaf drafts, PDFs, figures, or prior papers, and need to reorganize them into a Chinese degree thesis workflow. This path is currently the least automated of the four.

## How To Use The Repo

1. Start Codex in this repository.
2. Choose a workflow, or describe the outcome you want.
3. Let the selected pipeline write artifacts into a workspace.
4. Inspect the generated files at the relevant checkpoint before continuing.

Typical prompts:

```text
Write a LaTeX survey about embodied AI and show me the outline first.
```

```text
Use the research-brief workflow to give me a one-page briefing on test-time adaptation for robotics.
```

```text
Use the paper-review workflow to critique this manuscript and give me a lab-style review.
```

```text
Use the evidence-review workflow to run a PRISMA-style review on LLM agents for education.
```

```text
Brainstorm literature-grounded research ideas around embodied agents for home robotics.
```

```text
Use the source-tutorial pipeline to turn webpages and repo docs about robot learning into a tutorial with PDF and slides.
```

```text
Use the graduate-paper workflow to reorganize my Chinese thesis materials before rewriting chapters.
```

If you want tighter control, pin the pipeline directly:

- [pipelines/arxiv-survey.pipeline.md](pipelines/arxiv-survey.pipeline.md)
- [pipelines/arxiv-survey-latex.pipeline.md](pipelines/arxiv-survey-latex.pipeline.md)
- [pipelines/research-brief.pipeline.md](pipelines/research-brief.pipeline.md)
- [pipelines/paper-review.pipeline.md](pipelines/paper-review.pipeline.md)
- [pipelines/evidence-review.pipeline.md](pipelines/evidence-review.pipeline.md)
- [pipelines/idea-brainstorm.pipeline.md](pipelines/idea-brainstorm.pipeline.md)
- [pipelines/source-tutorial.pipeline.md](pipelines/source-tutorial.pipeline.md)
- [pipelines/graduate-paper-pipeline.md](pipelines/graduate-paper-pipeline.md)

## Recommended Reading Path

1. Read this file for the repo-level picture.
2. Open the feature guide that matches your task and language.
3. Open the matching pipeline contract under `pipelines/`.
4. Inspect the relevant skills under `.codex/skills/` if you need to change behavior rather than just run it.

## Documentation Map

Feature guides:

| Workflow | English | 中文 |
|---|---|---|
| `latex-survey` | [readme/latex-survey.md](readme/latex-survey.md) | [readme/latex-survey.zh-CN.md](readme/latex-survey.zh-CN.md) |
| `research-brief` | [readme/research-brief.md](readme/research-brief.md) | [readme/research-brief.zh-CN.md](readme/research-brief.zh-CN.md) |
| `paper-review` | [readme/paper-review.md](readme/paper-review.md) | [readme/paper-review.zh-CN.md](readme/paper-review.zh-CN.md) |
| `evidence-review` | [readme/evidence-review.md](readme/evidence-review.md) | [readme/evidence-review.zh-CN.md](readme/evidence-review.zh-CN.md) |
| `idea-brainstorm` | [readme/idea-brainstorm.md](readme/idea-brainstorm.md) | [readme/idea-brainstorm.zh-CN.md](readme/idea-brainstorm.zh-CN.md) |
| `source-tutorial` | [readme/source-tutorial.md](readme/source-tutorial.md) | [readme/source-tutorial.zh-CN.md](readme/source-tutorial.zh-CN.md) |
| `graduate-paper` | [readme/graduate-paper.md](readme/graduate-paper.md) | [readme/graduate-paper.zh-CN.md](readme/graduate-paper.zh-CN.md) |

Project references:

- [SKILL_INDEX.md](SKILL_INDEX.md)
- [SKILLS_STANDARD.md](SKILLS_STANDARD.md)

Legacy language-specific copies of the older survey-focused README still live under `readme/README.*.md`. They are reference material, not the primary entrypoint.

## Current Status

- `latex-survey` is the most complete writing pipeline in the repo and the main path when the deliverable is a survey paper or PDF.
- `research-brief`, `paper-review`, and `evidence-review` now form the review-oriented product family: quick understanding, single-paper assessment, and protocol-driven synthesis.
- `idea-brainstorm` is structured and executable, but optimized for discussion-ready idea memos rather than paper drafting.
- `source-tutorial` is now the canonical tutorial path: source-grounded, tutorial-first, with article PDF and Beamer slides as first-class delivery artifacts.
- `graduate-paper` now has a clearer pipeline design and a first batch of thesis-oriented skills, but it should currently be treated as a guided workflow framework rather than a fully automated thesis runner.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WILLOSCAR/research-units-pipeline-skills&type=Date)](https://star-history.com/#WILLOSCAR/research-units-pipeline-skills&Date)
