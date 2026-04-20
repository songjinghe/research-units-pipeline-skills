# research-units-pipeline-skills

> Languages: [English](README.md) | **简体中文** | [Español](README.es.md) | [Português (Brasil)](README.pt-BR.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

> **一句话**：构建能够“带人 / 带模型”完成研究工作的 pipeline——不是一堆脚本，而是一组**语义化的 skills**；每个 skill 都明确知道“该做什么、怎么做、做到什么程度，以及不能做什么”。

Skills index: [`SKILL_INDEX.md`](SKILL_INDEX.md).  
Skill/Pipeline standard: [`SKILLS_STANDARD.md`](SKILLS_STANDARD.md).

## 核心设计：Skills-First + 可恢复 Units + 证据优先

研究工作流很容易滑向两个极端：
- **只有脚本**：能跑，但像黑盒，出了问题很难调试或改进；
- **只有文档**：看起来合理，但执行时仍依赖临场判断，容易漂移。

这个仓库把“写一篇 survey”拆成**小而可审计、可恢复的步骤**，并在每一步把中间产物写到磁盘上。

1) **Skill = 可执行的操作手册**
- 每个 skill 都会定义 `inputs / outputs / acceptance / guardrails`（例如 C2–C4 强制 **NO PROSE**）。

2) **Unit = 可恢复的一步**
- 每个 unit 都对应 `UNITS.csv` 中的一行（依赖 + 输入/输出 + DONE 标准）。
- 如果某个 unit 变成 `BLOCKED`，你只需要修复对应工件，然后从该 unit 继续，不必整条链路重跑。

3) **证据优先**
- C1 先检索文献；C2 搭结构并给每个小节分配论文池；C3/C4 把它们整理成可写的证据与引用；C5 再开始写作并输出最终草稿 / PDF。

快速定位（先看哪里）：

| 如果你需要…… | 先看 | 常见修复方式 |
|---|---|---|
| 扩大覆盖面 / 找更多论文 | `queries.md` + `papers/retrieval_report.md` | 增加关键词桶、提高 `max_results`、导入离线集合、做 snowballing |
| 修 outline 或薄弱的小节池 | `outline/outline.yml` + `outline/mapping.tsv` | 合并/重排小节、提高 `per_subsection`、重跑 mapping |
| 解决“证据太薄导致写作空洞” | `papers/paper_notes.jsonl` + `outline/evidence_drafts.jsonl` | 先补 notes / packs，再写正文 |
| 降低模板腔 / 冗余 | `output/WRITER_SELFLOOP_TODO.md` + `output/PARAGRAPH_CURATION_REPORT.md` + `sections/*` | 定点重写 + best-of-N 候选 + 段落融合，然后重跑 gates |
| 提高全局 unique citations | `output/CITATION_BUDGET_REPORT.md` + `citations/ref.bib` | 按 in-scope 范围注入引用（NO NEW FACTS） |

## Codex 参考配置

```toml

[sandbox_workspace_write]
network_access = true

[features]
unified_exec = true
shell_snapshot = true
steer = true
```

## 30 秒快速上手（从 0 到 PDF）

1) 在这个仓库目录启动 Codex：

```bash
codex --sandbox workspace-write --ask-for-approval never
```

2) 在聊天里说一句话，例如：

> Write a survey about LLM agents and output a PDF (show me the outline first)

3) 然后会发生什么（直白版）：
- 它会在 `workspaces/` 下创建一个带时间戳的新目录，并把所有工件放进去。
- 它会先准备 outline 和按 section 划分的阅读列表，然后停下来等你确认。
- 你回复 “Looks good. Continue.” 后，它才会开始写正文并生成 PDF。

4) 你最常打开的 3 个文件：
- Markdown 草稿：`workspaces/<...>/output/DRAFT.md`
- PDF：`workspaces/<...>/latex/main.pdf`
- QA 报告：`workspaces/<...>/output/AUDIT_REPORT.md`

5) 如果流程意外停住，先看：
- `workspaces/<...>/output/QUALITY_GATE.md`（为什么停、下一步修什么）
- `workspaces/<...>/output/RUN_ERRORS.md`（运行 / 脚本错误）

可选（更可控）：
- 你可以显式指定 pipeline：`pipelines/arxiv-survey-latex.pipeline.md`（如果你想要 PDF，就用它）
- 如果你想从头跑到尾、不要停在 outline 审批处，可以在第一句 prompt 里直接说明 “auto-approve the outline”。

简短术语表（只需要记住 3 个）：
- workspace：一次 run 的输出目录（`workspaces/<name>/`）
- C2：outline 审批关卡；没通过审批就不会写 prose
- strict：打开质量门；只要失败就会停下并在 `output/QUALITY_GATE.md` 里给报告

下面的“详细 walkthrough”会解释中间工件和写作迭代是怎么运作的。

## 详细 walkthrough：从 0 到 PDF

在聊天里，你通常会这样说：

> Write a LaTeX survey about LLM agents (strict; show me the outline first)

然后它会按阶段推进（所有内容都会写进同一个 workspace；默认在 C2 暂停）：

### [C0] 初始化一次 run（no prose）

- 在 `workspaces/` 下创建一个带时间戳的目录，并把所有工件都写进去。
- 写入基础的运行契约 / 配置（`UNITS.csv`、`DECISIONS.md`、`queries.md`），确保整个 run 可审计、可恢复。

### [C1] 找论文（先把 paper pool 做扎实）

- 目标：先检索到足够大的候选池（每个 query bucket 默认 `max_results=1800`；去重后目标 `>=1200`），再选出一个 core set（默认 `300` 篇，写入 `papers/core_set.csv`）。
- 方法（简述）：把主题拆成多个 query bucket（同义词 / 缩写 / 子主题），分别检索，然后合并 + 去重。
  - 如果覆盖度不够：增加 bucket（例如 “tool use / planning / memory / reflection / evaluation”）或提高 `max_results`。
  - 如果噪声过大：改写关键词并加入 exclusions，然后重跑。
- 关键产物：`papers/core_set.csv` + `papers/retrieval_report.md`

### [C2] 审阅 outline（no prose；默认会在这里暂停）

你主要会看：
- `outline/outline.yml`
- `outline/mapping.tsv`（默认每个 subsection 映射 `28` 篇论文）
- （可选）`outline/coverage_report.md`（覆盖率 / 复用预警）

通常只要快速检查两件事：
1) outline 是否“节数少但每节够厚”，没有被切得过碎？
2) 每个 subsection 是否都分到了足够多的论文，后面能支撑 in-scope 引用和写作？

### [C3–C4] 把论文变成“可写材料”（no prose）

- 目标很简单：把“读论文”变成“可以直接写进正文的证据”，但此时仍然**不写叙述性段落**。
- `papers/paper_notes.jsonl`：每篇论文做了什么 / 发现了什么 / 有什么局限
- `citations/ref.bib`：参考文献表（里面的 key 才能在正文里用）
- `outline/writer_context_packs.jsonl`：按 section 划分的写作包（写什么对比点、允许用哪些引用）
- （表格）`outline/tables_index.md` 是内部表；`outline/tables_appendix.md` 是读者可见的附录表

### [C5] 写作与输出（所有迭代都发生在这里）

1) 先写按小节拆分的文件：`sections/*.md`
   - 先把正文写出来，再回头改开头：这样可以避免整篇文章被模板式 opener 牵着走。
   - 通常会包含：front matter + chapter leads + subsection bodies

2) 通过四类“检查 + 收敛” gate（只修失败项）：
   - 写作 gate：`output/WRITER_SELFLOOP_TODO.md`（补 thesis / contrasts / eval anchors / limitations；去模板话）
   - 段落逻辑 gate：`output/SECTION_LOGIC_REPORT.md`（桥接 + 顺序调整；消灭“段落孤岛”）
   - 论证 / 一致性 gate：`output/ARGUMENT_SELFLOOP_TODO.md`（单一真相源：`output/ARGUMENT_SKELETON.md`）
   - 段落策展 gate：`output/PARAGRAPH_CURATION_REPORT.md`（best-of-N → 选择 / 融合；防止“越写越长”）

3) 去模板化（在收敛之后做）：`style-harmonizer` + `opener-variator`（best-of-N）

4) 合并成最终草稿并跑最终检查：`output/DRAFT.md`
   - 如果引用不足：`output/CITATION_BUDGET_REPORT.md` → `output/CITATION_INJECTION_REPORT.md`
   - 最终审计：`output/AUDIT_REPORT.md`
   - LaTeX pipeline 还会编译：`latex/main.pdf`

目标：
- 全局 unique citations 推荐 `>=165`

如果它被拦住了：
- strict 模式下：看 `output/QUALITY_GATE.md`
- 运行 / 脚本错误：看 `output/RUN_ERRORS.md`

恢复方法：
- 修复报告里提到的文件，然后说 “continue” → 就会从被卡住的步骤继续，不需要整条链路重来

**关键原则**：C2–C4 强制 **NO PROSE**——先把 evidence base 搭起来；C5 才开始写 prose；一旦失败，可以定点修复。

## 示例工件（v0.1：一条完整端到端参考 run）

这是一个完整跑通的示例目录：找论文 → 出 outline → 整理 evidence + references → 按 section 写作 → 合并 → 编译 PDF。  
你可以把它当作“参考答案”：当你自己的 run 卡住时，对照同名文件 / 目录通常是最快的排查方式。

- 示例路径：`example/e2e-agent-survey-latex-verify-<TIMESTAMP>/`（对应 pipeline：`pipelines/arxiv-survey-latex.pipeline.md`）
- 在开始写任何 prose 之前，它会先停在 **C2（outline review）**
- 默认姿态（A150++）：300 篇 core papers、每个 subsection 映射 28 篇、默认使用 abstract-level evidence；目标是让整篇 draft 的 citation coverage 保持足够高
- 推荐：`draft_profile: survey`（默认交付形态）；如果想更严格，可以用 `draft_profile: deep`

建议的阅读入口（按这个顺序打开）：
- `example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/output/AUDIT_REPORT.md`：PASS / FAIL + 核心指标（citations、模板腔、缺失 section 等）
- `example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/latex/main.pdf`：最终 PDF（LaTeX pipeline）
- `example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/output/DRAFT.md`：合并后的草稿（与 PDF 内容对应）

如果你想看写作是如何逐步收敛的：
- 原始分节 prose 在 `sections/`（便于逐个 unit 修）
- 每轮迭代报告都在 `output/`（例如 `WRITER_SELFLOOP_TODO.md`、`SECTION_LOGIC_REPORT.md`、`ARGUMENT_SELFLOOP_TODO.md`、`PARAGRAPH_CURATION_REPORT.md`）

目录速览（每个文件夹用来干什么）：

```text
example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/
  STATUS.md           # 进度和运行日志（当前 checkpoint）
  UNITS.csv           # 执行契约（依赖 / 验收 / 输出）
  DECISIONS.md        # 人类 checkpoint（最重要的是：C2 outline approval）
  CHECKPOINTS.md      # checkpoint 规则
  PIPELINE.lock.md    # 选中的 pipeline（单一真相源）
  GOAL.md             # 目标 / 范围 seed
  queries.md          # 检索 + 写作档位配置（例如 core_size / per_subsection）
  papers/             # 检索结果 + paper / evidence base
  outline/            # 结构 + 可写材料（outline / mapping + briefs + evidence packs + tables）
  citations/          # BibTeX + verification records
  sections/           # 按 section 拆分的草稿（便于定点修）
  output/             # 合并后的草稿 + QA 报告（gates / audits / citation budget…）
  latex/              # LaTeX scaffold + 编译后的 PDF（只有 LaTeX pipeline 才有）
```

注：`outline/tables_index.md` 是内部索引表（中间工件）；`outline/tables_appendix.md` 是读者可见的附录表。

Pipeline 视图（各目录之间如何衔接）：

```mermaid
flowchart LR
  WS["workspaces/{run}/"]
  WS --> RAW["papers/papers_raw.jsonl"]
  RAW --> DEDUP["papers/papers_dedup.jsonl"]
  DEDUP --> CORE["papers/core_set.csv"]
  CORE --> STRUCT["outline/outline.yml + outline/mapping.tsv"]
  STRUCT -->|Approve C2| EVID["C3-C4: paper_notes + evidence packs"]
  EVID --> PACKS["C4: writer_context_packs.jsonl + citations/ref.bib"]
  PACKS --> SECS["sections/ (per-section drafts)"]
  SECS --> G["C5 gates (writer/logic/argument/style)"]
  G --> DRAFT["output/DRAFT.md"]
  DRAFT --> AUDIT["output/AUDIT_REPORT.md"]
  AUDIT --> PDF["latex/main.pdf (optional)"]

  G -.->|"FAIL → back to sections/"| SECS
  AUDIT -.->|"FAIL → back to sections/"| SECS
```

交付时，优先看**最新时间戳**的 example 目录（保留 2–3 个更早的 run 用于回归对比）：

- 草稿（Markdown）：`example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/output/DRAFT.md`
- PDF 输出：`example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/latex/main.pdf`
- QA / audit 报告：`example/e2e-agent-survey-latex-verify-<LATEST_TIMESTAMP>/output/AUDIT_REPORT.md`

## 欢迎提 Issues（一起继续改进写作工作流）

## 路线图（WIP）
1. 增加 multi-CLI collaboration 和 multi-agent design（把不同 API 接到合适阶段，替代或分担 Codex 的执行负载）。
2. 持续打磨 writing skills，进一步抬高写作质量的下限和上限。
3. 补完剩余 pipelines，并在 `example/` 下增加更多示例。
4. 按奥卡姆剃刀原则，减少 pipeline 里冗余的中间内容：非必要不引入额外实体。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WILLOSCAR/research-units-pipeline-skills&type=Date)](https://star-history.com/#WILLOSCAR/research-units-pipeline-skills&Date)
