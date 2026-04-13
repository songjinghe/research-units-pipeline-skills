# research-units-pipeline-skills

> 语言： [English](README.md) | **简体中文**

这个项目使用语义化 skills，把研究工作流组织成可复用的 pipelines。

它面向的是“脆弱的 prompting”和“过于僵硬的 scripting”之间的那一段空间。通过把研究任务组织成带有明确工件、检查点和 guardrails 的分阶段 pipeline，它让复杂工作更容易复用、更容易检查，也更适合迭代推进。最终得到的不是每次都要从头重搭的一次性流程，而是一套可以恢复、可以审计、也可以持续改进的工作方式。

## 这个仓库当前覆盖什么

目前代码库主要围绕 4 条工作流展开：

| 工作流 | 适用场景 | 默认交付物 | English | 中文 |
|---|---|---|---|---|
| `latex-survey` | 证据优先的文献综述写作，可选 LaTeX/PDF 交付 | `output/DRAFT.md`、`latex/main.tex`、`latex/main.pdf` | [Guide](readme/latex-survey.md) | [说明](readme/latex-survey.zh-CN.md) |
| `idea-brainstorm` | 基于文献的研究方向发现与讨论备忘录 | `output/REPORT.md` | [Guide](readme/idea-brainstorm.md) | [说明](readme/idea-brainstorm.zh-CN.md) |
| `source-tutorial` | 把网页/PDF/笔记/repo docs 等多源资料重构成 reader-first tutorial，并输出 PDF 与 Beamer slides | `output/TUTORIAL.md`、`latex/main.pdf`、`latex/slides/main.pdf` | [Guide](readme/source-tutorial.md) | [说明](readme/source-tutorial.zh-CN.md) |
| `graduate-paper` | 将现有中文毕业论文材料重构为论文工程流程 | pipeline + thesis skills | [Guide](readme/graduate-paper.md) | [说明](readme/graduate-paper.zh-CN.md) |

这四条工作流共享同一套基本架构：

- `pipelines/` 定义阶段合同、目标工件和所需 skills。
- `.codex/skills/` 存放可复用 skills。（100 个 skills）
- `workspaces/` 存放每次 run 的输出和中间产物。
- `readme/` 存放按功能拆分的说明文档。

## 核心概念

- `Pipeline`：工作流合同，定义阶段、工件、检查点和所需 skills。
- `Skill`：可复用能力，带有明确的输入、输出、验收条件和 guardrails。
- `Workspace`：一次 run 的工作目录，位于 `workspaces/<name>/`，所有生成工件都写在这里。

这个仓库最重要的设计选择是 artifact-first。模型不是靠“记住整个流程”在工作，而是把中间结构、证据和 review 结果落盘，让后续阶段可以在这些工件上继续推进。

## 什么时候该用哪条工作流

当目标是写一篇严肃综述，并且需要显式检索、结构审阅、evidence packs、写作自循环以及可选 PDF 输出时，用 `latex-survey`。

当目标还不是写论文，而是把一个主题转成“适合和导师/PI 讨论的、由文献支撑的研究方向备忘录”时，用 `idea-brainstorm`。

当你已经有网页、PDF、笔记、repo docs 或文档站点，想把这些材料重构成一个更适合阅读和讲解的教程时，用 `source-tutorial`。

旧的 `tutorial` 名称仍然可以作为兼容 alias 使用，但现在的 canonical pipeline 名称已经是 `source-tutorial`。

当你已经有毕业论文模板、现有 TeX、Overleaf 草稿、PDF、图表或已有 paper，需要把这些材料重组成一条中文学位论文工作流时，用 `graduate-paper`。这条路径目前也是四者里自动化程度最低的一条。

## 怎么使用这个仓库

1. 在这个仓库里启动 Codex。
2. 选择一条工作流，或者直接描述你想要的结果。
3. 让对应 pipeline 把工件写入一个 workspace。
4. 在关键 checkpoint 打开对应文件检查，再决定是否继续。

典型 prompt：

```text
Write a LaTeX survey about embodied AI and show me the outline first.
```

```text
Brainstorm literature-grounded research ideas around embodied agents for home robotics.
```

```text
使用 source-tutorial pipeline，把关于 robot learning 的网页和 repo docs 重构成一个 tutorial，并输出 PDF 与 slides。
```

```text
Use the graduate-paper workflow to reorganize my Chinese thesis materials before rewriting chapters.
```

如果你想更明确地控制流程，也可以直接钉住 pipeline：

- [pipelines/arxiv-survey.pipeline.md](pipelines/arxiv-survey.pipeline.md)
- [pipelines/arxiv-survey-latex.pipeline.md](pipelines/arxiv-survey-latex.pipeline.md)
- [pipelines/idea-brainstorm.pipeline.md](pipelines/idea-brainstorm.pipeline.md)
- [pipelines/source-tutorial.pipeline.md](pipelines/source-tutorial.pipeline.md)
- [pipelines/graduate-paper-pipeline.md](pipelines/graduate-paper-pipeline.md)

## 推荐阅读路径

1. 先看这个首页，理解仓库级别的定位。
2. 再打开与你任务和语言对应的功能说明。
3. 然后去看 `pipelines/` 下对应的 pipeline 合同。
4. 如果你要改行为而不是只运行，再去看 `.codex/skills/` 里的相关 skills。

## 文档导航

功能说明：

| 工作流 | English | 中文 |
|---|---|---|
| `latex-survey` | [readme/latex-survey.md](readme/latex-survey.md) | [readme/latex-survey.zh-CN.md](readme/latex-survey.zh-CN.md) |
| `idea-brainstorm` | [readme/idea-brainstorm.md](readme/idea-brainstorm.md) | [readme/idea-brainstorm.zh-CN.md](readme/idea-brainstorm.zh-CN.md) |
| `source-tutorial` | [readme/source-tutorial.md](readme/source-tutorial.md) | [readme/source-tutorial.zh-CN.md](readme/source-tutorial.zh-CN.md) |
| `graduate-paper` | [readme/graduate-paper.md](readme/graduate-paper.md) | [readme/graduate-paper.zh-CN.md](readme/graduate-paper.zh-CN.md) |

项目参考：

- [SKILL_INDEX.md](SKILL_INDEX.md)
- [SKILLS_STANDARD.md](SKILLS_STANDARD.md)

更早那套偏 survey 的多语言 README 仍保存在 `readme/README.*.md` 下，现在更适合作为历史参考，而不是新的主入口。

## 当前状态

- `latex-survey` 是当前最完整的写作 pipeline，也是需要综述或 PDF 交付时的主路径。
- `idea-brainstorm` 已经结构化并可执行，但它面向的是讨论型 idea memo，不是论文草稿。
- `source-tutorial` 现在是教程类任务的 canonical 路径：以 source-grounded 的 reader-first tutorial 为主产品，同时把 article PDF 和 Beamer slides 作为正式交付层。
- `graduate-paper` 现在已经有更清晰的 pipeline 设计和第一批 thesis skills，但目前更适合作为引导式工作流框架，而不是一键全自动毕业论文生成器。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WILLOSCAR/research-units-pipeline-skills&type=Date)](https://star-history.com/#WILLOSCAR/research-units-pipeline-skills&Date)
