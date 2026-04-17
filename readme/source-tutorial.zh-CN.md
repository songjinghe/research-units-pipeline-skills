# Source Tutorial 说明

> 语言： [English](source-tutorial.md) | **简体中文**
>
> 导航： [项目主页](../README.zh-CN.md) | [Project README](../README.md)

## 1. 这条流程是做什么的

`source-tutorial` 用来把多源资料重构成一个更适合阅读、学习和讲解的教程。

输入不是一个裸 topic，而是一组资料：

- 网页
- PDF
- 本地 Markdown / 文本笔记
- GitHub repo 的 README / docs
- 文档站点
- 带 transcript / subtitle 的视频

输出仍然以 tutorial 为主：

- `output/TUTORIAL.md`
- `latex/main.pdf`
- `latex/slides/main.pdf`

## 2. 它和一般教程生成器的区别

它不是：

- 一句 prompt 直接写教程
- LMS / course platform
- 只会出 deck 的 slides 生成器
- 录屏式 SOP 流程文档工具

它的核心合同是：

`多源输入 -> ingest/归一化 -> 教学化重构 -> tutorial -> PDF/slides`

对视频输入，这条线采用 transcript-first 合同。单纯的视频播放页不会被当作有效教学文本。

实操上：
- YouTube：建议显式提供 `transcript_locator`
- Bilibili：如果公开视频本身有 subtitle，可尝试自动拉取

## 3. 阶段流

| 阶段 | 目的 | 主要产物 |
|---|---|---|
| `C0` | 初始化 workspace，并锁定 source intake 意图 | `STATUS.md`、`UNITS.csv`、`DECISIONS.md`、`queries.md` |
| `C1` | 收集并 ingest sources | `sources/manifest.yml`、`sources/index.jsonl`、`sources/provenance.jsonl` |
| `C2` | 锁定 learner profile 和教程结构 | `output/TUTORIAL_SPEC.md`、`outline/concept_graph.yml`、`outline/module_plan.yml`、`outline/source_coverage.jsonl`、`outline/tutorial_context_packs.jsonl` |
| `C3` | 写 tutorial 并跑教程专用 QA | `output/TUTORIAL.md`、`output/TUTORIAL_SELFLOOP_TODO.md` |
| `C4` | 生成 article/slides 交付层并审计合同 | `latex/main.pdf`、`latex/slides/main.pdf`、build reports、`output/CONTRACT_REPORT.md` |

## 4. 质量目标

这个 tutorial 应该：

- 明确写出受众与先修
- 不照搬 source 顺序，而是主动降低理解跳跃
- 有具体示例和常见误区
- 有可验证的 learner checkpoint
- 保留轻量但可见的 source grounding

slides 应该：

- 和 tutorial 模块结构对齐
- 适合讲授
- 单独阅读时也能看懂核心内容
