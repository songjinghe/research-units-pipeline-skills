# Sparse Evidence Examples

## Good thin-evidence pack behavior

- `blocking_missing` includes:
  - `title-only evidence for this subsection (need abstracts or full text)`
  - `too few concrete comparisons (need >= 7 grounded comparisons backed by clusters/snippets)` for survey mode, or the higher deep-profile threshold when enabled
- `downgrade_signals` includes:
  - `limitations/failure-mode evidence is sparse for this subsection; keep comparative claims conservative and prioritize richer extraction upstream.`
- `verify_fields` includes:
  - `named benchmarks/datasets used`
  - `metrics/human-eval protocol`
  - `failure modes / known limitations`

## Bad thin-evidence pack behavior

- filling `evaluation_protocol` with generic cautions so the pack looks complete
- padding `failures_limitations` with stock caveat bullets unrelated to extracted evidence
- generating fake `Approach A` vs `Approach B` comparison cards with no grounded grouping
- admitting raw source wrappers such as `Our extensive evaluation shows ...`, `Third: ...`, or `To enhance reliability, we introduce ...` as reusable evidence sentences
- letting a 5-card pack drift into C5 with only warning-level language when the downstream writer contract expects a denser comparison pool
