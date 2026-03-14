# Overview

`evidence-draft` turns subsection briefs plus paper notes into evidence packs that later writing can trust.

## Core rule

Thin evidence should stay visibly thin.

That means:
- use snippet-backed claims only
- emit `blocking_missing` when drafting should stop
- emit downgrade signals when claims must stay conservative
- emit `verify_fields` when stronger protocol detail is still needed

## What success looks like

A good pack gives downstream writing:
- addressable snippets with provenance
- real A-vs-B comparisons grounded in clusters/snippets
- protocol-aware evaluation anchors
- failure/limitation evidence without padding

It should also keep raw source sentences under control:
- strip paper self-narration before snippets become claim candidates
- keep artifact/result payloads when possible, but drop scaffolding wrappers
- avoid passing `we validate ...`, `third: ...`, or `extensive experimental results ...` sentences downstream as if they were ready-made prose
