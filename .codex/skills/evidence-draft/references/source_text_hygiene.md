# Source Text Hygiene

## Purpose

`evidence-draft` is the earliest point where snippet quality can still be fixed cheaply.
If raw source wrappers stay in `evidence_snippets`, later packs and writing stages will keep inheriting them.

## Filter or rewrite upstream

- paper self-narration (`we present`, `this paper studies`, `our survey aims`)
- ordinal scaffolding (`first:`, `third:`, `finally:`)
- evaluation-result wrappers (`extensive experimental results demonstrate ...`, `evaluations across simulation and real-world validate ...`)
- artifact-capability wrappers that are still method-like rather than evidential (`X enables: ...`, `our framework features ...`)
- repository / dataset availability lines
- survey-meta sentences that summarize a field instead of stating subsection-relevant evidence
- positive gap-closing sentences that only mention improvement (`... improves policy learning while narrowing the gap ...`) when the pack slot expects a limitation or failure mode
- benchmark-positioning / field-orientation sentences that are useful context in an abstract but weak as H3 evidence (`Traditional imitation learning benchmarks are unsuitable ...`, `While deep learning on large and diverse datasets has shown promise ...`, `Recent work on high-capacity models ...`)
- field-wide challenge lines that are too broad to anchor one H3 by themselves (`Training vision-based manipulation policies ... remains an unresolved challenge`, `Learning to control robots directly based on images is a primary challenge in robotics`, `Vision-language-action (VLA) models have advanced generalist robotic learning ...`)

## Keep when possible

- artifact-named result clauses after wrapper cleanup
- concrete benchmark / metric / deployment statements
- limitation / failure evidence tied to cited papers

## Boundary

The hygiene policy belongs in `assets/source_text_hygiene.json`.
`scripts/run.py` should only apply it deterministically and do the smallest necessary artifact-name repair after stripping wrappers.
