# Source Text Hygiene

## Purpose

`writer-context-pack` should pass forward reusable evidence, not raw paper self-narration.

The pack is a C4-to-C5 bridge.
If it forwards bad source sentences, the writer will either:
- copy paper self-description into prose,
- repeat generic summary lines across many H3s,
- or waste paragraphs cleaning up upstream noise instead of comparing evidence.

## What should be filtered upstream

Drop or aggressively sanitize:
- project / repository / website availability text
- paper self-narration (`we present`, `this paper studies`, `our survey aims`)
- ordinal / scaffolding wrappers (`first:`, `third:`, `finally:`) that survive note extraction but add no comparison value
- evaluation-result wrappers (`extensive experimental results demonstrate ...`, `evaluations across simulation and real-world validate ...`) when the useful payload is the result clause rather than the wrapper
- artifact-capability wrappers that still read like method cards rather than evidence (`X enables: ...`, `our framework features ...`, `X offers a promising step toward ...`)
- summary-style orientation lines (`benchmarks are crucial ...`, `recent work has advanced ...`)
- self-promotional result leads (`we can effectively fine-tune ...`, `the experiments also provide ...`) when they do not add a subsection-specific comparison handle
- artifact-introduction sentences that are useful as metadata but not as reader-facing evidence
- vague sentence fragments that only describe evaluation setup without a usable result or limitation
- note-level benchmark-positioning or field-motivation sentences that belong in paper reading notes, not in writer packs (`Traditional imitation learning benchmarks are unsuitable ...`, `While deep learning on large and diverse datasets has shown promise ...`, `Recent work on high-capacity models ...`)

## What should survive

Keep sentences that still carry at least one of these:
- a concrete result
- a failure mode
- a protocol constraint
- a deployment limitation
- a subsection-relevant comparison handle

## Ranking rule

When multiple candidate snippets are available, prefer:
1. subsection-relevant evidence
2. concrete protocol / metric / benchmark language
3. lower global reuse across H3 packs

Do not let a generic but clean sentence outrank a narrower and more useful one.

## Anti-patterns

Bad upstream pack items:
- `Benchmarks are crucial for evaluating progress in robotics and embodied AI.`
- `We benchmark our method against state-of-the-art models.`
- `This paper provides a comprehensive review ...`
- `Our repository is publicly available at ...`

Better upstream pack items:
- a benchmark result with scope
- a limitation tied to transfer / cost / latency / robustness
- a contrast-bearing claim that can be attached to one H3 axis
- an artifact-named result sentence after wrapper cleanup (`MOTIF significantly outperforms ...`, not `Evaluations across ... validate the superiority of MOTIF ...`)

## Script boundary

The script should execute hygiene deterministically.
The hygiene policy itself should live in:
- `assets/source_text_hygiene.json`

If the policy changes, update the asset first and keep code changes minimal.
