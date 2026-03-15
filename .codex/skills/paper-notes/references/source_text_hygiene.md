# Paper Notes — Source Text Hygiene

## Purpose

`paper_notes.jsonl` is upstream evidence, not prose.
But if note fields preserve raw author-result wrappers, those wrappers survive into `evidence-draft`, `writer-context-pack`, and finally the survey draft.

## What to clean in notes

Especially for `key_results` and `limitations`, drop or rewrite:
- `Through simulated and real-world experiments, we show ...`
- `We also devise ...`
- `We deploy ... and find that ...`
- `We apply ... and show that it ...`
- `Our model features three carefully crafted designs ...`
- `Through extensive benchmarking ... we demonstrate ...`
- `Our results suggest ...`
- `In this work, we aim to ...`
- `As an endeavor towards this end, we introduce ...`
- `X enables: (1) ...`
- `Our framework features the following benefits: ...`
- `X offers a promising step toward ...`
- broad field-motivation or benchmark-positioning lines that are not actually results:
  - `Generalist robot policies, trained on large and diverse datasets ...`
  - `While deep learning on large and diverse datasets has shown promise ...`
  - `Traditional imitation learning benchmarks are unsuitable ...`
  - `Critical to this is ...`
  - `Training vision-based manipulation policies ... remains an important and unresolved challenge ...`
  - `Learning to control robots directly based on images is a primary challenge in robotics.`
  - `Vision-language-action (VLA) models have advanced generalist robotic learning ...`

## What should remain

- result clauses with benchmark / metric / constraint context
- failure or boundary statements that actually change interpretation
- compact method descriptions when they are needed for later synthesis
- reported results, not artifact introductions masquerading as results

## Field-specific rule

- `summary_bullets`: light cleanup only; they can still describe setup or motivation
- `method`: keep neutral method descriptions, not first-person paper narration
- `key_results`: prefer neutral result clauses; drop artifact-introduction lines, capability lists, and promotional roadmap sentences
- `limitations`: keep negative / boundary / constraint statements; drop positive result statements that only look like “interesting facts”

## Boundary

The cleanup policy belongs in `assets/source_text_hygiene.json`.
`run.py` should apply it deterministically during note inference and backfill.
