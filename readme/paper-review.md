# Paper Review Guide

> Languages: **English** | [简体中文](paper-review.zh-CN.md)
>
> Navigation: [Project README](../README.md) | [项目主页](../README.zh-CN.md)

## 1. What This Workflow Is For

`paper-review` is for evaluating a single paper or manuscript in a traceable way.

It is broader than formal peer review. It also covers:

- lab reading-group review
- paper triage
- reproduce-or-skip decisions
- referee-style critique

The output is:

- `output/REVIEW.md`

## 2. The Core Contract

`paper/manuscript -> full text ingest -> claims -> evidence gaps + novelty -> review`

The key idea is that critique must stay attached to identifiable claims, not float as generic advice.

## 3. When To Use It

Use `paper-review` when:

- the input is a single paper or manuscript
- you want to know whether the main claims hold up
- you need novelty, soundness, clarity, and impact assessed together

Do not use it when:

- you are trying to understand an entire topic area quickly
- you need a screened evidence synthesis across many studies

## 4. Stage Flow

| Stage | Purpose | Main outputs |
|---|---|---|
| `C0` | initialize workspace and review constraints | `STATUS.md`, `UNITS.csv`, `DECISIONS.md` |
| `C1` | ingest manuscript text and extract explicit claims | `output/PAPER.md`, `output/CLAIMS.md` |
| `C2` | audit evidence and novelty positioning | `output/MISSING_EVIDENCE.md`, `output/NOVELTY_MATRIX.md` |
| `C3` | write and self-check the review | `output/REVIEW.md`, `output/DELIVERABLE_SELFLOOP_TODO.md` |

## 5. Quality Bar

The review should:

- trace every major criticism back to an explicit claim or gap
- separate novelty, soundness, clarity, and impact
- prefer concrete next actions over vague complaints
- stay useful for both lab-internal review and referee-style review

## 6. Recommended Prompt

```text
Use the paper-review workflow to assess this manuscript and give me a lab-style review with explicit claims, evidence gaps, and novelty concerns.
```
