# Evidence Review 说明

> 语言： [English](evidence-review.md) | **简体中文**
>
> 导航： [项目主页](../README.zh-CN.md) | [Project README](../README.md)

## 1. 这条流程是做什么的

`evidence-review` 用来对一批候选研究做 protocol 驱动的证据综述。

它适合回答的问题是：

- 现有证据到底支持什么？
- screening 和 extraction 之后还剩下什么？
- 偏倚和异质性把结论限制在什么范围？

主要输出是：

- `output/SYNTHESIS.md`

## 2. 为什么它不只是“更长一点的 brief”

这条流程比 `research-brief` 重得多，而且是刻意如此。

它的合同里明确包含：

- protocol
- 候选池可审计性
- screening log
- extraction table
- bias assessment
- bounded synthesis

所以它必须保持独立执行合同，而不是被折叠成轻量 briefing 路径。

## 3. 什么时候该用它

当：

- 你需要一个可审计的 review question
- 你需要明确 inclusion/exclusion 规则
- 你需要在 prose 前先过 screening 和 extraction
- 你希望结论显式受 bias 和 heterogeneity 约束

就该用它。

不要在下面这些情况用它：

- 你只需要一份快速入门 memo
- 你评估的是一篇单独 paper，而不是一个候选池

## 4. 阶段流

| 阶段 | 目的 | 主要产物 |
|---|---|---|
| `C0` | 初始化 workspace 和 review question | `STATUS.md`、`UNITS.csv`、`DECISIONS.md`、`queries.md` |
| `C1` | 写 protocol 并完成批准 | `output/PROTOCOL.md` |
| `C2` | 建立可审计的 candidate pool | `papers/papers_raw.jsonl`、`papers/papers_dedup.jsonl`、`papers/core_set.csv` |
| `C3` | 按 protocol 条款做 screening | `papers/screening_log.csv` |
| `C4` | 提取研究字段和 bias 数据 | `papers/extraction_table.csv` |
| `C5` | 写 synthesis 并做成品自检 | `output/SYNTHESIS.md`、`output/DELIVERABLE_SELFLOOP_TODO.md` |

## 5. 质量目标

这份 synthesis 应该：

- 每个主要结论都能回指到 extraction table
- 清楚区分“支持充分”和“证据不足”
- 显式交代限制与偏倚
- 不要退化成普通长摘要

## 6. 推荐 Prompt

```text
Use the evidence-review workflow to run a PRISMA-style review on LLM agents for education, with protocol, screening, extraction, and a bounded synthesis.
```
