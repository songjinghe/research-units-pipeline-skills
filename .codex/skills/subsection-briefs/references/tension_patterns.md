# Tension Patterns

`tension_statement` should be concrete enough to open paragraph 1 later, while remaining NO NEW FACTS at brief time.

Requirements:

- one sentence
- names a real trade-off, not a topic label
- avoids abstract meta-language like “highlights a tension around …” when a sharper contrast exists
- falls back to axis-based wording when no domain rule matches cleanly

The machine-readable source of truth is:

- `assets/domain_packs/generic.json` → generic tension rules + fallback

Current compatibility families:

- capability vs safety
- coverage vs comparability
- adaptability vs stability
- specialization vs coordination
- deliberation depth vs cost
- persistence vs freshness
- expressivity vs control

If none of these fit, use the generic fallback based on the leading axes.
