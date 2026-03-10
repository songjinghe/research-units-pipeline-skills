# Taxonomy Principles

## 1) Optimize for reader questions, not keyword buckets

Good top-level nodes read like chapter titles in a survey.
Bad top-level nodes read like bag-of-words clusters.

## 2) Prefer fewer, thicker top-level buckets

A paper-like survey usually wants a small number of chapter-driving buckets.
If every recurring term becomes a top-level node, downstream outline and writing quality collapse.

## 3) Make leaves mappable

A leaf should plausibly absorb multiple papers.
Tiny or one-off leaves usually belong as comparison axes inside a subsection, not as taxonomy nodes.

## 4) Encode scope in the description

A good node description says what belongs here and what kind of comparison the bucket supports.
It should help `section-mapper` and later writers avoid scope drift.

## 5) Separate mechanism / evaluation / risk when the corpus supports it

If a topic mixes system design, benchmarking, and safety into one bucket, mapping becomes ambiguous.
Split only when the split is meaningful to readers and mappable to papers.

## 6) Avoid generic placeholders

Avoid node names like:
- `Overview`
- `Representative Approaches`
- `Benchmarks`
- `Open Problems`
- `Misc` / `Other`

These are usually signs that the taxonomy is dodging the real organizing question.

## 7) Keep descriptions concrete

Prefer descriptions that mention:
- what design/evaluation question the bucket covers
- what assumptions or constraints matter there
- representative paper IDs when available

## 8) Treat domain packs as explicit support, not hidden bias

If a domain needs a curated taxonomy shape, put it in `assets/domain_packs/<domain>.yaml` and document it in `references/domain_pack_<domain>.md`.
Do not hide domain chapter structure as Python strings.
