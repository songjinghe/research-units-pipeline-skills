# Source Tutorial Redesign

## Motivation

The old `tutorial` pipeline assumed a topic-first workflow:

`topic -> spec -> concept graph -> module plan -> tutorial`

That was too weak for the actual use case. Real tutorial authoring in this repo is usually source-driven:

- a set of webpages
- notes
- PDFs
- repo docs
- documentation sites

The missing step was not “more writing quality”. The missing step was **source-grounded pedagogical transformation**.

This redesign therefore makes the contract:

`multi-source inputs -> ingest -> distill -> pedagogical restructure -> tutorial -> article/slides delivery`

## Product Position

`source-tutorial` is a tutorial-authoring pipeline, not:

- a survey pipeline
- a course platform
- a slide-only generator
- a process-capture/SOP system

The canonical reader-facing artifact remains `output/TUTORIAL.md`.

Slides and PDF are delivery layers derived from the same teaching structure, not the primary product.

## Why One Pipeline

There is no value in splitting:

- tutorial writing
- tutorial + PDF/slides

into separate pipelines.

That split makes sense for survey because PDF is an optional delivery mode on top of a much heavier evidence-writing chain. For tutorial, the delivery layer is part of the product from the beginning:

- if the tutorial is reader-first, it should also compile as an article PDF
- if the tutorial is meant to be teachable, it should also have a deck

So the correct shape is one pipeline with multiple target artifacts.

## Naming

Chosen name: `source-tutorial`

Rejected alternatives:

- `tutorial`: too vague; hides the source-ingest contract
- `teaching-bundle`: too delivery-centric; implies the product is a package rather than a tutorial
- `grounded-tutorial`: good academically, but weaker than `source-tutorial` in telling the user what to provide

## External Benchmarks

The redesign borrows ideas from a few product categories:

- **NotebookLM**: validates multi-source grounding across docs, slides, PDFs, URLs, YouTube, audio
- **Mindsmith**: validates storyboard/objective-first lesson planning
- **Gamma**: validates import-to-deck expectations and delivery polish
- **Beamer**: remains the correct formal slide target for this repo

The redesign intentionally does **not** turn the repo into:

- an LMS
- a SCORM authoring system
- a screen-recording tutorial generator

## Pipeline Contract

### C0 Init

Purpose:
- initialize workspace
- route goal into source-tutorial
- capture source-collection constraints

### C1 Source intake

Purpose:
- collect source candidates into `sources/manifest.yml`
- ingest supported source kinds
- persist normalized text and provenance

Supported v1 source kinds:
- `webpage`
- `pdf`
- `markdown`
- `repo`
- `docs_site`
- `video` (transcript-first)

Deferred:
- direct YouTube watch-page transcript extraction in this environment
- deep code-aware repo explanation

### C2 Pedagogical structure

Purpose:
- define tutorial scope from ingested sources
- build concept graph
- build module plan
- audit module-to-source grounding
- create context packs

The main design choice here is that the tutorial structure is not allowed to drift beyond source support.

### C3 Tutorial writing

Purpose:
- write the tutorial
- run tutorial-specific self-loop

This stage changes the quality bar from “good prose” to “good teaching”.

### C4 Delivery

Purpose:
- scaffold article-style LaTeX
- compile article PDF
- scaffold Beamer deck
- compile slides PDF
- audit artifact contract

## Quality Contract

### Tutorial quality

The tutorial should be:

- audience-aware
- prerequisite-aware
- structurally progressive
- example-rich
- low-friction to read
- lightly grounded in visible source notes

This is what “more readable and more engaging” means operationally.

### Source grounding

The tutorial should not read like an academic citation dump.

Chosen policy:
- weak explicit grounding
- source notes / further reading at module end
- provenance stays strong internally

### Running example policy

Not every source set supports one stable running example.

Chosen rule:
- use one when the source set supports it
- otherwise state explicitly that the tutorial uses modular examples instead

### Slides quality

Slides must satisfy two jobs:

- help a speaker teach
- remain understandable when skimmed without the article

That means the deck cannot be a pure heading dump, but also cannot become a transcript.

## Implementation Notes

### Reused components

- `concept-graph`
- `module-planner`
- `exercise-builder`
- `latex-scaffold`
- `latex-compile-qa`
- `artifact-contract-auditor`

### New deterministic pieces

- `source-manifest`
- `source-ingest`
- `tutorial-selfloop`
- `beamer-scaffold`
- `beamer-compile-qa`

### New semantic/manual pieces

- `source-tutorial-spec`
- `module-source-coverage`
- `tutorial-context-pack`
- `source-tutorial-writer`

### Routing cleanup

- `source-tutorial` is the only active tutorial pipeline name
- the old `tutorial` alias has been removed from routing and tests
- docs and examples should reference `source-tutorial` directly

## Review Checklist

Reviewers should confirm:

1. The pipeline name and routing surface are unambiguous.
2. The source model is explicit and auditable.
3. The tutorial remains the main product.
4. The PDF and slides are first-class but subordinate to the tutorial contract.
5. No survey-only assumptions leak into the tutorial quality gates.
