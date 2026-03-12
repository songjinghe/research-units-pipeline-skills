# Writer self-loop

- Timestamp: `2026-03-12T14:15:24`
- Status: FAIL

## Failing files

- `sections/S4_1.md`
  - kind: `h3` id: `4.1` title: Vision-language-action and policy backbones
  - rq: Which design choices in Vision-language-action and policy backbones drive the major trade-offs, and how are those trade-offs measured?
  - axes: policy backbone and action representation, language / vision grounding into robot actions, latency and execution stability, core mechanism / architecture, evaluation protocol (datasets, metrics, human eval)
  - paragraph_plan: 10 (intent sketch)
    - p1: Define scope, setup, and the subsection thesis (no pipeline jargon).
    - p2: Explain cluster A: core mechanism and system architecture and the core approach it takes.
    - p3: Cluster A implementation details: methodology and data signals and design trade-offs that constrain behavior.
    - p4: Cluster A evaluation/trade-offs: where it works, costs (compute/latency), and typical failure modes.
    - p5: Explain cluster B (contrast with A): core mechanism and system architecture and what it optimizes for.
    - p6: Cluster B implementation details: methodology and data and design assumptions (mirror A for comparability).
    - p7: Cluster B evaluation/trade-offs: where it works, costs, and failure modes (mirror A).
    - p8: Cross-paper synthesis: compare clusters along the main axes (include >=2 citations in one paragraph).
  - must_use: anchors>=5 comparisons>=5 limitations>=3
  - pack_stats: anchors_kept=10 comparisons_kept=7 eval_kept=6 limitation_kept=8
  - `sections_h3_too_short`: `sections/S4_1.md` looks too short (4212 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections/S4_2.md`
  - kind: `h3` id: `4.2` title: World models, planning, and reasoning
  - rq: Which design choices in World models, planning, and reasoning drive the major trade-offs, and how are those trade-offs measured?
  - axes: planning / world-model role, long-horizon state handling, failure recovery under partial observability, control-loop design (planner / executor), deliberation / search method
  - paragraph_plan: 10 (intent sketch)
    - p1: Define scope, setup, and the subsection thesis (no pipeline jargon).
    - p2: Explain cluster A: core mechanism and system architecture and the core approach it takes.
    - p3: Cluster A implementation details: methodology and data signals and design trade-offs that constrain behavior.
    - p4: Cluster A evaluation/trade-offs: where it works, costs (compute/latency), and typical failure modes.
    - p5: Explain cluster B (contrast with A): core mechanism and system architecture and what it optimizes for.
    - p6: Cluster B implementation details: methodology and data and design assumptions (mirror A for comparability).
    - p7: Cluster B evaluation/trade-offs: where it works, costs, and failure modes (mirror A).
    - p8: Cross-paper synthesis: compare clusters along the main axes (include >=2 citations in one paragraph).
  - must_use: anchors>=5 comparisons>=5 limitations>=3
  - pack_stats: anchors_kept=10 comparisons_kept=7 eval_kept=6 limitation_kept=8
  - `sections_h3_sparse_citations`: `sections/S4_2.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
  - `sections_h3_too_short`: `sections/S4_2.md` looks too short (3430 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections/S4_3.md`
  - kind: `h3` id: `4.3` title: Transfer across embodiments and viewpoints
  - rq: Which design choices in Transfer across embodiments and viewpoints drive the major trade-offs, and how are those trade-offs measured?
  - axes: transfer target (embodiment / viewpoint / environment), adaptation mechanism and invariance, cross-embodiment generalization limits, core mechanism / architecture, evaluation protocol (datasets, metrics, human eval)
  - paragraph_plan: 10 (intent sketch)
    - p1: Define scope, setup, and the subsection thesis (no pipeline jargon).
    - p2: Explain cluster A: core mechanism and system architecture and the core approach it takes.
    - p3: Cluster A implementation details: methodology and data signals and design trade-offs that constrain behavior.
    - p4: Cluster A evaluation/trade-offs: where it works, costs (compute/latency), and typical failure modes.
    - p5: Explain cluster B (contrast with A): core mechanism and system architecture and what it optimizes for.
    - p6: Cluster B implementation details: methodology and data and design assumptions (mirror A for comparability).
    - p7: Cluster B evaluation/trade-offs: where it works, costs, and failure modes (mirror A).
    - p8: Cross-paper synthesis: compare clusters along the main axes (include >=2 citations in one paragraph).
  - must_use: anchors>=5 comparisons>=5 limitations>=3
  - pack_stats: anchors_kept=10 comparisons_kept=7 eval_kept=6 limitation_kept=8
  - `sections_h3_too_short`: `sections/S4_3.md` looks too short (4830 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections/S5_1.md`
  - kind: `h3` id: `5.1` title: Pretraining data and supervision
  - rq: Which design choices in Pretraining data and supervision drive the major trade-offs, and how are those trade-offs measured?
  - axes: data source and supervision, pretraining versus post-training, adaptation and transfer across embodiments, core mechanism / architecture, evaluation protocol (datasets, metrics, human eval)
  - paragraph_plan: 10 (intent sketch)
    - p1: Define scope, setup, and the subsection thesis (no pipeline jargon).
    - p2: Explain cluster A: core mechanism and system architecture and the core approach it takes.
    - p3: Cluster A implementation details: methodology and data signals and design trade-offs that constrain behavior.
    - p4: Cluster A evaluation/trade-offs: where it works, costs (compute/latency), and typical failure modes.
    - p5: Explain cluster B (contrast with A): core mechanism and system architecture and what it optimizes for.
    - p6: Cluster B implementation details: methodology and data and design assumptions (mirror A for comparability).
    - p7: Cluster B evaluation/trade-offs: where it works, costs, and failure modes (mirror A).
    - p8: Cross-paper synthesis: compare clusters along the main axes (include >=2 citations in one paragraph).
  - must_use: anchors>=5 comparisons>=5 limitations>=3
  - pack_stats: anchors_kept=10 comparisons_kept=7 eval_kept=6 limitation_kept=8
  - `sections_h3_too_short`: `sections/S5_1.md` looks too short (4089 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections/S5_3.md`
  - kind: `h3` id: `5.3` title: Data quality, scaling, and distribution shift
  - rq: Which design choices in Data quality, scaling, and distribution shift drive the major trade-offs, and how are those trade-offs measured?
  - axes: data quality and coverage bias, scaling efficiency versus data fidelity, distribution shift and robustness limits, core mechanism / architecture, evaluation protocol (datasets, metrics, human eval)
  - paragraph_plan: 10 (intent sketch)
    - p1: Define scope, setup, and the subsection thesis (no pipeline jargon).
    - p2: Explain cluster A: core mechanism and system architecture and the core approach it takes.
    - p3: Cluster A implementation details: methodology and data signals and design trade-offs that constrain behavior.
    - p4: Cluster A evaluation/trade-offs: where it works, costs (compute/latency), and typical failure modes.
    - p5: Explain cluster B (contrast with A): core mechanism and system architecture and what it optimizes for.
    - p6: Cluster B implementation details: methodology and data and design assumptions (mirror A for comparability).
    - p7: Cluster B evaluation/trade-offs: where it works, costs, and failure modes (mirror A).
    - p8: Cross-paper synthesis: compare clusters along the main axes (include >=2 citations in one paragraph).
  - must_use: anchors>=5 comparisons>=5 limitations>=3
  - pack_stats: anchors_kept=10 comparisons_kept=7 eval_kept=6 limitation_kept=8
  - `sections_h3_sparse_citations`: `sections/S5_3.md` has <12 unique citations (10); each H3 should be evidence-first for survey-quality runs.

## Loop

1) Fix only the failing `sections/*.md` files above (follow `.codex/skills/writer-selfloop/SKILL.md`).
2) Recheck:

```bash
python .codex/skills/writer-selfloop/scripts/run.py --workspace /home/rjs/Workspace/codebase/research-units-pipeline-skills/workspaces/arxiv-survey/embodied-ai-smoke-20260312-c5-retest
```

Optional: after large edits, rerun `subsection-writer` to refresh `sections/sections_manifest.jsonl` for auditability.
