# Idea Brief Method

`idea-brief` is the ideation pipeline's contract-locking step.

It should do four things only:

1. turn a fuzzy topic into a bounded brainstorm target
2. define the memo shape and discussion standard
3. materialize replayable query buckets and exclusions
4. leave a clean handoff for C1-C5 without starting retrieval

## What belongs in the brief

- topic
- audience
- scope and exclusions
- evaluation rubric for directions
- query buckets
- target artifact shape
- focus placeholder for later C2 approval

## What does not belong here

- retrieved papers
- proposal prose
- execution plans
- survey writing

## Query-bucket rule

Query buckets should be broad enough to expose tensions and missing pieces, not so narrow that they pre-commit to one thesis.

Good buckets usually probe:

- evaluation reliability
- failure modes
- planning / adaptation / memory
- governance / risk / benchmark framing

## Exclusion rule

Default exclusions should remove obvious non-research or non-academic drift, but should stay editable by the human.

The brief should not silently lock controversial exclusions.

## Render rule

`scripts/run.py` should only:

- read the active pipeline contract
- render the brief markdown
- render `queries.md`
- initialize `DECISIONS.md` if missing

Method text, bucket templates, exclusions, and rubric rows should live in `assets/`, not in Python.
