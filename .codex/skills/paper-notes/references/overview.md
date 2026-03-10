# Paper Notes — Reference-First Overview

## Purpose

This skill produces structured, searchable notes for each paper in the core set.
Notes feed downstream evidence binding, writing, and auditing.

## Key Principles

1. **Structured over narrative**: notes are bullet fields, not prose paragraphs.
2. **Paper-specific over boilerplate**: every limitation, method summary, and result must be checkable against the source paper.
3. **Evidence-level awareness**: notes should transparently reflect what evidence depth was available (title / abstract / fulltext).
4. **Deterministic scaffolding**: the script generates a conservative scaffold; LLM/human refinement is expected for high-priority papers.

## Load Order

When executing this skill, read these references in order:

1. `references/overview.md` (this file) — orientation
2. `references/note_schema.md` — field definitions and required/optional semantics
3. `references/limitation_taxonomy.md` — how to write paper-specific limitations
4. `references/result_extraction_examples.md` — good vs bad examples of key_results extraction

Machine-readable assets:
- `assets/note_schema.json` — JSON schema for note validation
- `assets/evidence_tags.json` — evidence bank tagging categories (externalized from script)
