# Overview

Use this skill to turn each H3 subsection into a deterministic brief card that downstream writers can execute without copying scaffold bullets.

Compatibility mode goals:

- preserve the current `outline/subsection_briefs.jsonl` field contract
- preserve current downstream expectations (`transition-weaver`, `writer-context-pack`, `subsection-writer`)
- move phrase/domain inventories into `assets/` instead of keeping them as Python string lists
- move bridge/contrast routing and emergency fallbacks into machine-readable packs where compatibility allows

Suggested read order:

1. `thesis_patterns.md`
2. `tension_patterns.md`
3. `axis_catalog_generic.md`
4. `axis_catalog_llm_agents.md` when the topic is agent/tool-use oriented
5. `bridge_terms.md` when transition handles are weak
6. `examples_good.md` for calibration

The script should stay deterministic: read inputs, load packs, choose stable phrases/axes, and write JSONL. It should not invent papers, citations, or reader-facing prose.

Cluster quality still matters upstream:
- contrast clusters should remain disjoint after removing bridge papers
- each side should retain enough unique papers to support later A-vs-B cards
- `bridge_terms` should preserve concrete lexical hooks for later evidence matching, not just polished abstract nouns
- when a domain pack can express subsection-specific clusters, that asset should lead and the generic bootstrap should only be the fallback
