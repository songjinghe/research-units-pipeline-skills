# Graduate Paper Guide

> Languages: **English** | [简体中文](graduate-paper.zh-CN.md)
>
> Navigation: [Project README](../README.md) | [项目主页](../README.zh-CN.md)

## 1. What This Workflow Is For

`graduate-paper` is for restructuring an existing Chinese graduation thesis project into a coherent thesis-writing workflow.

It is not for:

- generating a thesis from scratch from a bare topic
- mechanically stitching a few papers into a thesis
- hiding structural problems behind late-stage polishing

Its actual logic is:

`question list -> material placement -> chapter reconstruction -> markdown alignment -> TeX writeback -> compile review -> issue writeback -> next iteration`

That means the first priority is not “write a full draft quickly”. The first priority is to turn scattered thesis materials into a stable, reviewable engineering process.

## 2. When To Use It

Use this workflow when you already have some thesis assets, such as:

- a university template
- an existing `main.tex`
- `chapters/*.tex`
- Overleaf drafts
- published or submitted paper PDFs
- figures, tables, experiments, or a BibTeX library

This workflow is especially useful when the thesis can already “sort of be written”, but still has issues like:

- weak overall storyline
- chapters that still read like transformed papers
- inconsistent terminology or metrics
- figure placement that does not support the chapter logic
- too much rewriting happening directly in TeX

Do not use it when:

- you only have a topic and no project materials yet
- you only want to polish one or two paragraphs
- you expect a one-prompt fully automated thesis PDF

## 3. How It Differs From The Survey Workflow

`graduate-paper` and `arxiv-survey` start from different assumptions:

| Dimension | Survey workflow | Graduate-paper workflow |
|---|---|---|
| Starting point | topic + retrieval | existing materials + existing thesis project |
| Core problem | how to build structure and evidence around a topic | how to reconstruct existing assets into a thesis |
| Main middle layer | outline, mapping, evidence packs | `codex_md/` question lists, role maps, chapter rewrites, terminology alignment, figure planning |
| Deliverable | review paper | Chinese graduation thesis |
| Main risks | retrieval bias, thin evidence | paper-style narration leakage, chapter-role imbalance, template/front-matter drift |

In one sentence:

- survey is retrieval-driven evidence writing
- graduate-paper is thesis-engineering reconstruction from existing materials

## 4. Key Inputs And Working Layers

The key input is not a single prompt. It is a bundle of existing thesis assets.

### 4.1 Required inputs

- university template or an existing thesis repository
- `main.tex`
- `chapters/*.tex` or another identifiable chapter entry layer
- basic metadata such as title, author, year, and institution

### 4.2 Strongly recommended inputs

- published/submitted PDFs under something like `pdf/`
- source drafts and revisions under something like `Overleaf_ref/`
- `references/*.bib` and style files
- figures, tables, experiment results, or system diagrams
- Chinese/English abstract drafts, appendix content, acknowledgements, achievements
- writing rules from the advisor or institution

### 4.3 Recommended working layers

This workflow assumes the thesis should be split into layers:

- `codex_md/`: thinking and reconstruction layer
- `claude_md/`: review and checking layer
- `tmp_layout/`, `tmp_layout2/`: temporary layout experiments
- `chapters/`: delivery layer for final chapter TeX

Typical core artifacts include:

- `codex_md/material_index.md`
- `codex_md/material_readiness.md`
- `codex_md/missing_info.md`
- `codex_md/question_list.md`
- `codex_md/00_thesis_outline.md`
- `codex_md/chapter_role_map.md`
- `codex_md/chapter_rewrite_rules.md`
- `codex_md/terminology_glossary.md`
- `codex_md/symbol_metric_table.md`
- `codex_md/figure_plan.md`
- `claude_md/review_checklist.md`
- `output/THESIS_BUILD_REPORT.md`

## 5. Stage Flow

The current pipeline design breaks the work into these stages:

| Stage | Purpose | Main outputs |
|---|---|---|
| `0` | initialize project and place materials | workspace skeleton, material index, readiness report |
| `1` | restore existing materials into the markdown middle layer | initial markdown materials, missing-info list |
| `1.5` | lock the current question list and scope | `codex_md/question_list.md` |
| `2` | map source materials into thesis roles | `codex_md/chapter_role_map.md` |
| `2.5` | reconstruct chapter logic around the thesis storyline | rewritten chapter markdown, rewrite rules |
| `3` | align terminology, structure, symbols, metrics, and evidence gaps | stable outline, glossary, symbol table |
| `3.5` | pre-plan figures and layouts | figure plan, layout mockups |
| `4` | write stable markdown content back into TeX | updated `chapters/*.tex`, first full `main.pdf` |
| `4.5` | synchronize front matter and non-body sections | abstracts, appendix, acknowledgements, achievements |
| `5` | strengthen and verify citations | citation enhancement and verification records |
| `6` | compile and review the full thesis | build report, review checklist |
| `7` | final style pass and de-AI smoothing | more natural final Chinese thesis prose |

### 5.1 The four fixed loops

This should not be treated as a linear SOP. At least four loops are built into the design:

- structure loop: outline -> chapter markdown -> structural imbalance -> back to outline/question list
- content loop: source materials -> extraction -> reconstruction -> still too paper-like -> reconstruct again
- layout loop: TeX -> compile -> warnings / figure placement / cross-reference issues -> back to TeX or layout planning
- style loop: stable body -> polish -> template voice or AI smell remains -> back to upstream writing rules

## 6. The 11 Thesis Skills

The graduate-paper path is currently expressed through 11 thesis-specific skills.

### 6.1 Control layer

| Skill | Role |
|---|---|
| `thesis-workspace-init` | initialize the thesis workspace, surface missing materials, and create the basic working layer |
| `thesis-question-list` | maintain the question list, priorities, scope, and acceptance targets for the current round |

### 6.2 Main reconstruction chain

| Skill | Role |
|---|---|
| `thesis-source-role-mapper` | map source materials into thesis roles rather than only `paper -> chapter` |
| `thesis-chapter-reconstructor` | reconstruct paper-style narration into thesis-style chapter logic |
| `thesis-markdown-aligner` | unify storyline, terminology, symbols, metrics, and chapter boundaries in markdown |
| `thesis-tex-writeback` | write stable markdown content back to `chapters/*.tex` and sync figures, equations, and references |
| `thesis-compile-review` | compile, triage warnings, check template usage, and write issues back into the loop |
| `thesis-style-polisher` | polish the final Chinese thesis voice only after structure and evidence are stable |

### 6.3 Parallel support skills

| Skill | Role |
|---|---|
| `thesis-visual-layout-planner` | plan figures, Mermaid sketches, and temporary layout experiments |
| `thesis-frontmatter-sync` | keep abstracts, appendix, acknowledgements, and other non-body parts aligned with the main body |
| `thesis-citation-enhance-review` | strengthen and verify citation support for claims, definitions, and factual statements |

Recommended main chain:

`thesis-workspace-init -> thesis-question-list -> thesis-source-role-mapper -> thesis-chapter-reconstructor -> thesis-markdown-aligner -> thesis-tex-writeback -> thesis-compile-review -> thesis-style-polisher`

The three most important roles are:

- `thesis-question-list`: control surface
- `thesis-chapter-reconstructor`: core reconstruction surface
- `thesis-compile-review`: quality-closure surface

## 7. Current Support Boundary

This is the most important caveat.

`graduate-paper` is currently a strong method framework with thesis-oriented skill packages, but it is not yet a mature one-click end-to-end automated thesis runner.

What already exists:

- a clearer staged pipeline design
- 11 dedicated thesis skills
- explicit references and machine-readable contracts for those skills
- a clear separation between thinking layer, middle layer, and TeX delivery layer

What does not yet fully exist:

- a stable end-to-end automated runner for the whole thesis path
- full script implementations for every thesis skill
- a complete UNITS-style executable contract for this workflow

Current practical maturity:

- `thesis-workspace-init` has a script and can initialize the workspace/material surface
- `thesis-question-list` has a script and can scaffold or maintain the issue list
- the other thesis skills are currently mostly reference-first skill packages, not heavy deterministic executors

So the right interpretation today is:

`graduate-paper` can already support a guided, staged thesis reconstruction process with agent + human collaboration, but it should not yet be presented as a fully automated thesis generator.

## 8. Recommended Usage Pattern

The wrong way to use this workflow is:

- directly patch `chapters/*.tex` first
- start with style polishing
- hide structure issues under local edits
- skip the question list and chapter-role mapping

The recommended path is:

1. initialize the workspace and place materials
2. lock the question list for the current round
3. map the role of each source material in the thesis
4. reconstruct chapters one by one in markdown
5. align the full thesis in the markdown middle layer
6. in parallel, plan visuals, synchronize front matter, and strengthen citations
7. only then write stable content back to TeX
8. compile, review, and route issues back upstream
9. polish style only after structure, evidence, and data are already stable

The best collaboration model right now is:

- humans provide template, drafts, PDFs, figures, and local writing constraints
- the agent maintains the intermediate artifacts, question lists, role maps, and reconstruction proposals
- structural decisions are made in markdown first
- TeX remains the delivery layer, not the primary reasoning layer
