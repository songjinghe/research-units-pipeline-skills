# Bridge Terms

`bridge_terms` are short transition handles for later use by `transition-weaver`.

Requirements:

- 3-6 short handles
- noun-phrase or compact label, not a reusable sentence
- NO NEW FACTS
- should help connect subsections without sounding like slide narration

Good handles:

- `planner/executor`
- `function calling`
- `threat model`
- `benchmarks/metrics`
- `compute`

Avoid:

- `Next, we compare`
- `This subsection examines`
- long clause-like connectors that a writer will copy verbatim

Compatibility note: bridge terms and contrast-hook routing are now primarily pack-driven; Python keeps only normalization, deduplication, and a minimal last-resort fallback.

Machine-readable sources:

- `assets/domain_packs/generic.json`
- `assets/domain_packs/llm_agents.json`
- `assets/domain_packs/text_to_image.json`
- `assets/phrase_packs/bridge_contrast.json`
