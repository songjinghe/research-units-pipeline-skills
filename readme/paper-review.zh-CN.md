# Paper Review 说明

> 语言： [English](paper-review.md) | **简体中文**
>
> 导航： [项目主页](../README.zh-CN.md) | [Project README](../README.md)

## 1. 这条流程是做什么的

`paper-review` 用来对单篇 paper / manuscript 做可追溯的评估。

它不只等于正式审稿，也适用于：

- 组会 paper review
- 论文 triage
- reproduce 前的 worth-it 判断
- referee-style critique

输出是：

- `output/REVIEW.md`

## 2. 核心合同

`paper/manuscript -> 全文 ingest -> claims -> evidence gaps + novelty -> review`

核心思想是：所有 critique 都要挂到明确 claim 上，而不是漂浮的泛泛建议。

## 3. 什么时候该用它

当：

- 输入是一篇单独的 paper / manuscript
- 你想知道它的主张是否站得住
- 你想一起看 novelty、soundness、clarity、impact

就该用它。

不要在下面这些情况用它：

- 你是在快速理解整个方向
- 你要做多篇文献上的 screened evidence synthesis

## 4. 阶段流

| 阶段 | 目的 | 主要产物 |
|---|---|---|
| `C0` | 初始化 workspace 和 review 约束 | `STATUS.md`、`UNITS.csv`、`DECISIONS.md` |
| `C1` | ingest 全文并抽取明确 claims | `output/PAPER.md`、`output/CLAIMS.md` |
| `C2` | 做 evidence 审计和 novelty 定位 | `output/MISSING_EVIDENCE.md`、`output/NOVELTY_MATRIX.md` |
| `C3` | 写 review 并做成品自检 | `output/REVIEW.md`、`output/DELIVERABLE_SELFLOOP_TODO.md` |

## 5. 质量目标

这份 review 应该：

- 每个主要批评都能回指到明确 claim 或 evidence gap
- 清楚区分 novelty、soundness、clarity、impact
- 尽量给出具体可执行建议，而不是泛泛批评
- 同时适用于组会内部 review 和 referee-style review

## 6. 推荐 Prompt

```text
Use the paper-review workflow to assess this manuscript and give me a lab-style review with explicit claims, evidence gaps, and novelty concerns.
```
