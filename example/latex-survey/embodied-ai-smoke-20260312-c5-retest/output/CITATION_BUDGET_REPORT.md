# Citation budget report

- Status: FAIL
- Draft: `output/DRAFT.md`
- Bib entries: 300
- Draft unique citations: 153
- Draft profile: `survey`
- Citation target policy: `recommended`

- Global target (policy; blocking): >= 203 (struct=203, hard_frac=150, bib=300)
- Gap: 50
- Global hard minimum: >= 203 (struct=203, hard_frac=150, bib=300)
- Global recommended target: >= 203 (rec_frac=165, bib=300)
- Gap to recommended: 50
- Suggested keys per H3 (sizing): 6

## Per-H3 suggestions (unused global keys, in-scope)

| H3 | title | unique cites | unused in selected | unused in mapped | suggested keys (add 6-6) |
|---|---|---:|---:|---:|---|
| 3.1 | Manipulation, navigation, and task scope | 16 | 0 | 0 | `Ze2023Gnfactor`, `Zhang2025Safevla`, `Piergiovanni2018Learning` |
| 3.2 | Observation, action, and embodiment interfaces | 18 | 1 | 0 | `Zhang2025Safevla`, `Ze2023Gnfactor`, `Piergiovanni2018Learning` |
| 3.3 | Task diversity, environment realism, and transfer constraints | 17 | 1 | 0 | `Ze2023Gnfactor`, `Zhang2025Safevla`, `Piergiovanni2018Learning` |
| 4.1 | Vision-language-action and policy backbones | 15 | 9 | 4 | `Ma2024Survey`, `Liu2025Faster`, `Heo2026Anycamvla`, `Wu2025Momanipvla`, `Adang2025Singer`, `Team2025Gigabrain` |
| 4.2 | World models, planning, and reasoning | 15 | 6 | 2 | `Lee2026Roboreward`, `Wang2025Odyssey`, `Yang2023Foundation`, `Stone2023Open`, `Etukuru2024Robot`, `He2025Scaling` |
| 4.3 | Transfer across embodiments and viewpoints | 16 | 8 | 1 | `Haldar2026Point`, `Shenavarmasouleh2021Embodied`, `Team2024Octo`, `Batra2025Zero`, `Xiao2023Robot`, `Wang2026Mobilemanibench` |
| 5.1 | Pretraining data and supervision | 16 | 2 | 2 | `Gong2025Anytask`, `Gu2025Igen`, `Zhao2025Framework`, `Guan2025Efficient`, `Celemin2022Interactive`, `Garg2021Semantics` |
| 5.2 | Post-training, feedback, and continual improvement | 17 | 2 | 3 | `Yao2023Bridging`, `Su2026Interaction`, `Sharma2026World`, `Hu2023Toward`, `Katara2023Gen2Sim`, `Li2024Llara` |
| 5.3 | Data quality, scaling, and distribution shift | 16 | 3 | 6 | `Tang2024Kalie`, `Long2026Scaling`, `Zhu2026Beyond`, `Hu2023Toward`, `Li2024Llara`, `He2025Scaling` |
| 6.1 | Benchmarks, metrics, and generalization | 19 | 5 | 3 | `Zhang2025Agentworld`, `Schmidgall2024General`, `Dalal2025Unlocking`, `Rubavicius2024Secure`, `Ahn2024Autort`, `Han2025Multimodal` |
| 6.2 | Safety, reliability, and real-world deployment | 19 | 4 | 4 | `Li2025Worldeval`, `Kawaharazuka2024Real`, `Kumar2023Robohive`, `Li2023Transformer`, `Ren2024Infiniteworld`, `Yao2025Advancing` |
| 6.3 | Failure analysis, robustness, and stress testing | 18 | 6 | 4 | `Zhang2022Robotic`, `Hu2023Toward`, `Han2025Multimodal`, `Ren2024Infiniteworld`, `Li2023Transformer`, `Ahn2024Autort` |

## How to apply (NO NEW FACTS)

- Prefer cite-embedding edits that do not change claims (paraphrase; avoid repeated stems):
  - Axis-anchored exemplars: `... as seen in X [@a] and Y [@b] ...; Z [@c] illustrates a contrasting design point.`
  - Parenthetical grounding (low risk): `... (e.g., X [@a], Y [@b], Z [@c]).`
  - Contrast pointer: `While some systems emphasize <A> (X [@a]; Y [@b]), others emphasize <B> (Z [@c]).`
- Avoid budget-dump voice (high-signal automation tells): `Representative systems include ...`, `Notable lines of work include ...`.
- Keep additions inside the same H3 (no cross-subsection citation drift).
- Apply via `citation-injector` (LLM-first) and then rerun: `draft-polisher` → `global-reviewer` → `pipeline-auditor`.
