---
name: paper-review
version: 1.0
profile: paper-review
routing_hints: [paper review, paper critique, critique this paper, assess this paper, assess manuscript, referee report, peer review, 审稿, 论文评估]
routing_priority: 33
routing_default: false
target_artifacts:
  - STATUS.md
  - UNITS.csv
  - CHECKPOINTS.md
  - DECISIONS.md
  - GOAL.md
  - queries.md
  - output/PAPER.md
  - output/CLAIMS.md
  - output/MISSING_EVIDENCE.md
  - output/NOVELTY_MATRIX.md
  - output/REVIEW.md
  - output/DELIVERABLE_SELFLOOP_TODO.md
  - output/QUALITY_GATE.md
  - output/RUN_ERRORS.md
  - output/CONTRACT_REPORT.md
default_checkpoints: [C0,C1,C2,C3]
units_template: templates/UNITS.peer-review.csv
contract_model: pipeline.frontmatter/v1
query_defaults:
  review_style: lab_review
  traceability_required: true
overridable_query_fields:
  - review_style
quality_contract:
  review_policy:
    primary_deliverable: output/REVIEW.md
    traceability_required: true
    required_axes: [novelty, soundness, clarity, impact]
stages:
  C0:
    title: Init
    checkpoint: C0
    mode: no_prose
    required_skills: [workspace-init, pipeline-router]
    optional_skills: []
    produces: [STATUS.md, UNITS.csv, CHECKPOINTS.md, DECISIONS.md, GOAL.md, queries.md, output/QUALITY_GATE.md, output/RUN_ERRORS.md]
  C1:
    title: Manuscript ingest + claims
    checkpoint: C1
    mode: no_prose
    required_skills: [manuscript-ingest, claims-extractor]
    optional_skills: []
    produces: [output/PAPER.md, output/CLAIMS.md]
  C2:
    title: Evidence audit
    checkpoint: C2
    mode: no_prose
    required_skills: [evidence-auditor, novelty-matrix]
    optional_skills: []
    produces: [output/MISSING_EVIDENCE.md, output/NOVELTY_MATRIX.md]
  C3:
    title: Review write-up
    checkpoint: C3
    mode: prose_allowed
    required_skills: [rubric-writer, deliverable-selfloop, artifact-contract-auditor]
    optional_skills: []
    produces: [output/REVIEW.md, output/DELIVERABLE_SELFLOOP_TODO.md, output/CONTRACT_REPORT.md]
---

# Pipeline: paper-review

Goal: produce a traceable assessment of a single paper or manuscript, grounded in its explicit claims, evidence gaps, and novelty positioning.
