# Overview

`outline-builder` converts `outline/taxonomy.yml` into a bullets-only `outline/outline.yml` that downstream mapping, evidence, and writing skills can audit.

## What this skill owns

- adding the paper-like front structure (`Introduction`, `Related Work`)
- translating taxonomy nodes into chapter titles and H3 subsections
- enforcing the Stage A bullet contract for each H3
- emitting comparison-oriented, auditable bullets rather than prose paragraphs

## Reference-first split

- `SKILL.md`: router + workflow + compatibility notes
- `references/`: judgment rules, structure guidance, good/bad examples
- `assets/`: machine-readable defaults and routing rules
- `scripts/`: deterministic outline materialization only

## Compatibility mode

This migration preserves the current output contract:
- same output path: `outline/outline.yml`
- same top-level shape: Intro + Related Work + taxonomy-driven chapters
- same Stage A bullet fields for H3s
- same placeholder protection (do not overwrite non-placeholder user work)

## Load order

1. `references/intro_related_patterns.md`
2. `references/stage_a_contract.md`
3. `references/examples_good.md`
4. `references/examples_bad.md`

## Non-goals

- do not draft prose paragraphs
- do not rebudget an already-fragmented outline; use `outline-budgeter` for that
- do not inject new domain framing directly in Python
