# Coverage report (planner pass)

- Guardrail: NO PROSE; this is a diagnostic artifact, not survey writing.
- Sections (H2): 6
- Chapters with subsections (H2 with H3): 4
- Subsections (H3): 12
- H3 per H2 chapter (min/median/max): 3/3.0/3
- Mapping rows: 336
- Unique mapped papers: 208
- Most reused papers: P0265×6, P0266×6, P0006×3, P0008×3, P0030×3, P0032×3

## Per-subsection summary

| Subsection | #papers | Evidence levels | Axes (specific/generic) | Max reuse |
|---|---:|---|---:|---:|
| 3.1 Manipulation, navigation, and task scope | 28 | fulltext=0, abstract=28, title=0 | 5/0 | 6 |
| 3.2 Observation, action, and embodiment interfaces | 28 | fulltext=0, abstract=28, title=0 | 5/0 | 6 |
| 3.3 Task diversity, environment realism, and transfer constraints | 28 | fulltext=0, abstract=28, title=0 | 5/0 | 6 |
| 4.1 Vision-language-action and policy backbones | 28 | fulltext=0, abstract=28, title=0 | 5/0 | 6 |
| 4.2 World models, planning, and reasoning | 28 | fulltext=0, abstract=28, title=0 | 5/0 | 6 |
| 4.3 Transfer across embodiments and viewpoints | 28 | fulltext=0, abstract=28, title=0 | 5/0 | 6 |
| 5.1 Pretraining data and supervision | 28 | fulltext=0, abstract=28, title=0 | 5/0 | 6 |
| 5.2 Post-training, feedback, and continual improvement | 28 | fulltext=0, abstract=28, title=0 | 5/0 | 6 |
| 5.3 Data quality, scaling, and distribution shift | 28 | fulltext=0, abstract=28, title=0 | 5/0 | 6 |
| 6.1 Benchmarks, metrics, and generalization | 28 | fulltext=0, abstract=28, title=0 | 5/0 | 6 |
| 6.2 Safety, reliability, and real-world deployment | 28 | fulltext=0, abstract=28, title=0 | 5/0 | 6 |
| 6.3 Failure analysis, robustness, and stress testing | 28 | fulltext=0, abstract=28, title=0 | 5/0 | 6 |

## Per-chapter sizing (H2)

| Chapter | #H3 |
|---|---:|
| 1 Introduction | 0 |
| 2 Related Work | 0 |
| 3 Problem Settings & Embodiment | 3 |
| 4 Model & Policy Architectures | 3 |
| 5 Data, Training & Post-Training | 3 |
| 6 Evaluation, Safety & Deployment | 3 |

## Flags (actionable)

- Mapping shows high reuse hotspots (a paper reused >=6× within a subsection set): 3.1, 3.2, 3.3, 4.1, 4.2, 4.3

## Suggested next actions (still NO PROSE)
- If reuse hotspots are high: expand `core_set.csv` (increase core size) or rerun `section-mapper` with stronger diversity penalty.
- If axes are generic: regenerate `subsection_briefs.jsonl` after improving notes/evidence bank; avoid copying outline scaffold bullets.
- If evidence is mostly abstract-only: consider `evidence_mode: fulltext` for a smaller subset to strengthen key comparisons.
