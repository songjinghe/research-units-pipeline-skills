# Research Brief Guide

> Languages: **English** | [简体中文](research-brief.zh-CN.md)
>
> Navigation: [Project README](../README.md) | [项目主页](../README.zh-CN.md)

## 1. What This Workflow Is For

`research-brief` is for understanding a topic quickly and producing a compact, high-signal briefing instead of a full survey.

The core question is:

`What should I understand first, and what should I read first?`

The output stays intentionally light:

- `output/SNAPSHOT.md`

## 2. When To Use It

Use `research-brief` when:

- you need a one-page orientation before a meeting or reading session
- you want a reading path, not a publication-grade survey
- you have a topic or a small paper pool, but not a full evidence program

Do not use it when:

- you need protocol + screening + extraction
- you need a full survey draft or PDF paper
- you are evaluating a single manuscript in depth

## 3. How It Differs From Adjacent Workflows

| Workflow | Main question |
|---|---|
| `research-brief` | What is this area, and what should I read first? |
| `paper-review` | Is this single paper sound, novel, and worth following? |
| `evidence-review` | What does the full candidate pool support under an auditable protocol? |
| `latex-survey` | Can I turn this evidence base into a serious review paper? |

## 4. Stage Flow

| Stage | Purpose | Main outputs |
|---|---|---|
| `C0` | initialize workspace and seed queries | `STATUS.md`, `UNITS.csv`, `DECISIONS.md`, `queries.md` |
| `C1` | retrieve a small, usable core set | `papers/papers_raw.jsonl`, `papers/core_set.csv` |
| `C2` | lock topic boundary and bullets-only outline | `outline/taxonomy.yml`, `outline/outline.yml` |
| `C3` | write and self-check the briefing | `output/SNAPSHOT.md`, `output/DELIVERABLE_SELFLOOP_TODO.md` |

## 5. Quality Bar

The brief should:

- define the topic boundary clearly
- surface the key themes as claims, not generic section narration
- point the reader to what to read first
- stay compact and pointer-heavy

## 6. Recommended Prompt

```text
Use the research-brief workflow to give me a one-page briefing on robot test-time adaptation, with key themes and what to read first.
```
