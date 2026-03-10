# Overview

`taxonomy-builder` converts a paper set into a survey-grade taxonomy that later skills can map, budget, and write against.

## What this skill owns

- Choosing chapter-like top-level buckets
- Choosing mappable leaf buckets
- Writing node descriptions with clear scope cues
- Keeping structure non-prose and compatible with `outline/taxonomy.yml`

## Reference-first split

- `SKILL.md`: router + workflow + contract
- `references/`: judgment-heavy guidance and examples
- `assets/`: machine-readable packs / schemas
- `scripts/`: deterministic execution only

## Compatibility mode (P0)

This migration preserves the current output contract.
The notable implementation change is that built-in domain taxonomies are loaded from `assets/domain_packs/*.yaml`, so maintainers can change supported domain wording/structure without editing Python.

## Load order

1. Read `references/taxonomy_principles.md`
2. If the corpus matches a supported pack, read the corresponding `references/domain_pack_<domain>.md`
3. Otherwise read `references/archetypes_generic.md`
4. Calibrate with `references/examples_good.md` / `references/examples_bad.md`
