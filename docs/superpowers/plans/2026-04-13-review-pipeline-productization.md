# Review Pipeline Productization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the old user-facing names `lit-snapshot`, `peer-review`, and `systematic-review` with canonical product names `research-brief`, `paper-review`, and `evidence-review`, while preserving backward compatibility.

**Architecture:** Keep three independent execution contracts and introduce thin legacy alias pipeline files. Update the product layer, routing layer, and generated docs so only the new names are presented as primary workflows.

**Tech Stack:** Markdown pipeline specs, Python routing/validation utilities, unittest, generated Mermaid docs

---

### Task 1: Lock compatibility with failing tests

**Files:**
- Create: `tests/test_review_pipeline_productization.py`
- Modify: none
- Test: `tests/test_review_pipeline_productization.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tooling.common import resolve_pipeline_spec_path
from tooling.pipeline_spec import PipelineSpec

REPO_ROOT = Path(__file__).resolve().parents[1]


class ReviewPipelineProductizationTests(unittest.TestCase):
    def test_research_brief_pipeline_spec_loads(self) -> None:
        path = resolve_pipeline_spec_path(repo_root=REPO_ROOT, pipeline_value="research-brief")
        self.assertIsNotNone(path)
        spec = PipelineSpec.load(path)
        self.assertEqual(spec.name, "research-brief")

    def test_paper_review_pipeline_spec_loads(self) -> None:
        path = resolve_pipeline_spec_path(repo_root=REPO_ROOT, pipeline_value="paper-review")
        self.assertIsNotNone(path)
        spec = PipelineSpec.load(path)
        self.assertEqual(spec.name, "paper-review")

    def test_evidence_review_pipeline_spec_loads(self) -> None:
        path = resolve_pipeline_spec_path(repo_root=REPO_ROOT, pipeline_value="evidence-review")
        self.assertIsNotNone(path)
        spec = PipelineSpec.load(path)
        self.assertEqual(spec.name, "evidence-review")

    def test_legacy_names_resolve_to_new_canonical_pipelines(self) -> None:
        self.assertEqual(resolve_pipeline_spec_path(repo_root=REPO_ROOT, pipeline_value="lit-snapshot").name, "research-brief.pipeline.md")
        self.assertEqual(resolve_pipeline_spec_path(repo_root=REPO_ROOT, pipeline_value="peer-review").name, "paper-review.pipeline.md")
        self.assertEqual(resolve_pipeline_spec_path(repo_root=REPO_ROOT, pipeline_value="systematic-review").name, "evidence-review.pipeline.md")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_review_pipeline_productization -v`
Expected: FAIL because the new canonical pipeline files do not exist yet and legacy names still resolve to old files.

- [ ] **Step 3: Write minimal implementation**

Create the new canonical pipeline files and alias mappings only after seeing the failure.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_review_pipeline_productization -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_review_pipeline_productization.py pipelines tooling scripts
git commit -m "test: cover review pipeline productization aliases"
```

### Task 2: Introduce canonical review pipelines and legacy aliases

**Files:**
- Create: `pipelines/research-brief.pipeline.md`
- Create: `pipelines/paper-review.pipeline.md`
- Create: `pipelines/evidence-review.pipeline.md`
- Modify: `pipelines/lit-snapshot.pipeline.md`
- Modify: `pipelines/peer-review.pipeline.md`
- Modify: `pipelines/systematic-review.pipeline.md`
- Modify: `tooling/common.py`
- Modify: `scripts/pipeline.py`
- Modify: `tooling/pipeline_spec.py`
- Test: `tests/test_review_pipeline_productization.py`

- [ ] **Step 1: Update alias resolution tables**

```python
_LEGACY_PIPELINE_ALIASES = {
    "idea-finder": "idea-brainstorm",
    "idea-finder.pipeline.md": "idea-brainstorm",
    "pipelines/idea-finder.pipeline.md": "idea-brainstorm",
    "tutorial": "source-tutorial",
    "lit-snapshot": "research-brief",
    "peer-review": "paper-review",
    "systematic-review": "evidence-review",
}
```

- [ ] **Step 2: Add canonical frontmatter-first pipeline files**

Use the current contracts as the source of truth and encode them under:

```yaml
---
name: research-brief
version: 1.0
profile: research-brief
units_template: templates/UNITS.lit-snapshot.csv
contract_model: pipeline.frontmatter/v1
...
---
```

Repeat for `paper-review` and `evidence-review`, preserving current outputs and checkpoints.

- [ ] **Step 3: Convert old pipeline files into hidden aliases**

Example shape:

```yaml
---
name: lit-snapshot
version: 3.0
variant_of: research-brief
variant_overrides:
  docs_hidden: true
  routing_hints:
    __replace__: []
  routing_priority: -100
---
```

Repeat for `peer-review` and `systematic-review`.

- [ ] **Step 4: Run tests**

Run: `python -m unittest tests.test_review_pipeline_productization -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pipelines/research-brief.pipeline.md pipelines/paper-review.pipeline.md pipelines/evidence-review.pipeline.md pipelines/lit-snapshot.pipeline.md pipelines/peer-review.pipeline.md pipelines/systematic-review.pipeline.md tooling/common.py scripts/pipeline.py tooling/pipeline_spec.py
git commit -m "feat: add canonical review pipeline names"
```

### Task 3: Rework product docs and routing docs

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Create: `readme/research-brief.md`
- Create: `readme/research-brief.zh-CN.md`
- Create: `readme/paper-review.md`
- Create: `readme/paper-review.zh-CN.md`
- Create: `readme/evidence-review.md`
- Create: `readme/evidence-review.zh-CN.md`
- Modify: `.codex/skills/pipeline-router/SKILL.md`
- Modify: `.codex/skills/research-pipeline-runner/SKILL.md`

- [ ] **Step 1: Rewrite the user-facing workflow table in README**

Document the new names as primary workflows and remove the old names from top-level user-facing tables.

- [ ] **Step 2: Add dedicated guides**

Each guide must answer:
- what user job this workflow serves
- when to use it
- what the inputs are
- what the outputs are
- how it differs from the adjacent workflows

- [ ] **Step 3: Update router and runner docs**

Document the new routing choices:
- `research-brief`
- `paper-review`
- `evidence-review`

and mention the legacy names only as compatibility notes, not as first-class product names.

- [ ] **Step 4: Smoke-check docs**

Run: `rg -n "lit-snapshot|peer-review|systematic-review" README.md README.zh-CN.md readme .codex/skills/pipeline-router/SKILL.md .codex/skills/research-pipeline-runner/SKILL.md`
Expected: old names appear only in legacy-compatibility contexts.

- [ ] **Step 5: Commit**

```bash
git add README.md README.zh-CN.md readme/research-brief.md readme/research-brief.zh-CN.md readme/paper-review.md readme/paper-review.zh-CN.md readme/evidence-review.md readme/evidence-review.zh-CN.md .codex/skills/pipeline-router/SKILL.md .codex/skills/research-pipeline-runner/SKILL.md
git commit -m "docs: present review workflows with product-facing names"
```

### Task 4: Regenerate dependency docs and refresh index surfaces

**Files:**
- Modify: `SKILL_INDEX.md`
- Modify: `docs/PIPELINE_FLOWS.md`
- Modify: `docs/SKILL_DEPENDENCIES.md`
- Modify: `scripts/generate_skill_graph.py`

- [ ] **Step 1: Hide legacy aliases from generated dependency docs**

Use `docs_hidden` in the generator so alias pipelines do not appear as primary graphs.

- [ ] **Step 2: Update workflow naming in index docs**

Replace old product labels in `SKILL_INDEX.md` and `docs/PIPELINE_FLOWS.md` with the new names.

- [ ] **Step 3: Regenerate graph docs**

Run: `python scripts/generate_skill_graph.py`
Expected: `docs/SKILL_DEPENDENCIES.md` lists `research-brief`, `paper-review`, and `evidence-review`, but not the hidden aliases as top-level sections.

- [ ] **Step 4: Commit**

```bash
git add SKILL_INDEX.md docs/PIPELINE_FLOWS.md docs/SKILL_DEPENDENCIES.md scripts/generate_skill_graph.py
git commit -m "docs: regenerate review workflow dependency docs"
```

### Task 5: Final verification and cleanup

**Files:**
- Modify: none expected
- Test: `tests/test_review_pipeline_productization.py`
- Test: `tests/test_source_tutorial_pipeline.py`

- [ ] **Step 1: Run targeted tests**

Run: `python -m unittest tests.test_review_pipeline_productization tests.test_source_tutorial_pipeline -v`
Expected: all tests pass

- [ ] **Step 2: Run repo validation**

Run: `python scripts/validate_repo.py --no-check-quality`
Expected: `0 error(s), 0 warning(s)`

- [ ] **Step 3: Review working tree**

Run: `git status --short`
Expected: clean or only intended generated docs before final commit

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "feat: productize review-oriented pipelines"
```
