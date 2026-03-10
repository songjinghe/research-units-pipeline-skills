# Skills 重构蓝图

## 1. 文档目的

本文档定义本仓库 `.codex/skills/` 的整体重构方向，目标不是“把现有脚本修补得更顺”，而是把 skill 体系从 **script-heavy** 调整为 **instruction/reference-heavy**。

这份蓝图回答四个问题：

- skill 的第一性原理是什么；
- `SKILL.md`、`references/`、`assets/`、`scripts/` 分别应该承载什么；
- 当前仓库的问题主要集中在哪些模式；
- 应该按什么顺序逐步重构，才能在不打断现有流水线的前提下完成迁移。

---

## 2. 第一性原理

### 2.1 Skill 的本质

一个 skill 本质上不是“一个脚本目录”，而是：

- 一套触发条件；
- 一套工作流；
- 一组边界与 guardrails；
- 一份可按需加载的领域参考；
- 少量确定性工具。

也就是说，skill 的核心价值是：

- 让 agent 在某一类任务上拥有稳定的方法论；
- 让方法论可检查、可复用、可组合；
- 让领域知识显式存在，而不是埋在实现细节里。

### 2.2 对 `run.py` 的最低化定义

`run.py` 只应该做下面这些事情：

- 文件发现与读写；
- JSONL / CSV / YAML / Markdown 的确定性归一化；
- 结构化 sidecar 生成；
- 校验、lint、gate、manifest；
- 外部工具调用；
- 简单、可解释、可替换的排序/过滤。

`run.py` 不应该承担下面这些职责：

- 领域默认值；
- 大段 prose 模板；
- domain taxonomy 正文；
- 写作口吻；
- opener / lead / paragraph 的句式库；
- evidence 缺失时的 filler 文案；
- 最终用户视角下的判断逻辑本体。

### 2.3 对 `references/` 的定义

`references/` 是“让模型思考更正确”的地方，不是“脚本辅助文件”的地方。

应该放进 `references/` 的内容包括：

- 领域知识摘要；
- taxonomy / axes / wedge catalog；
- 好坏样例；
- 常见反模式；
- decision rubric；
- evidence quality policy；
- prompt-facing exemplars；
- persona-specific deliverable exemplars。

### 2.4 对 `assets/` 的定义

`assets/` 承载被脚本或产物直接消费的资源：

- JSON / YAML schema；
- output 模板骨架；
- 图规格模板；
- 机器可读 domain packs；
- palette / style resource；
- 示例输入输出样本。

### 2.5 对 `SKILL.md` 的定义

`SKILL.md` 应该保持精简，只保留：

- 这个 skill 什么时候触发；
- 解决什么问题；
- 输入/输出是什么；
- 工作流如何分步执行；
- 什么时候必须 block；
- 什么时候需要读取哪些 `references/`；
- 哪些 `assets/` 可复用；
- 哪些脚本只是黑箱工具，不应被全文读入。

---

## 3. 外部参考基线（Anthropic 风格）

本次重构的设计基线参考两类来源：

### 3.1 本地参考仓

可对照：

- `workspaces/_refs/anthropics-skills/skills/skill-creator/SKILL.md`
- `workspaces/_refs/anthropics-skills/skills/mcp-builder/SKILL.md`
- `workspaces/_refs/anthropics-skills/skills/webapp-testing/SKILL.md`

这组参考体现了几个明确原则：

- `SKILL.md` 是主入口；
- `scripts/` 用于 deterministic reliability；
- `references/` 用于按需加载的领域知识；
- `assets/` 用于模板与输出资源；
- 优先 progressive disclosure，而不是在脚本里内嵌大量语义。

### 3.2 官方公开实践

可参考：

- Anthropic 《The Complete Guide to Building Skill for Claude》
- Claude Prompting / Best Practices 文档中关于 examples、clear criteria、modular context 的建议

它们共同支持的结论是：

- 复杂行为应被拆成“明确的 instructions + examples + lightweight tooling”；
- 不要把本该被模型阅读的知识，藏进脚本常量里；
- scripts 应服务于稳定执行，而不是替代思考与示例。

---

## 4. 当前仓库的系统性问题

### 4.1 结构失衡

当前 `.codex/skills/` 的总体状态：

- 非隐藏 skills 数量：`88`
- 带 `scripts/` 的 skill：`60`
- 带 `references/reference/ref/refs` 的 skill：`0`
- 带 `assets/examples/templates` 的 skill：极少

这意味着目前整体上是：

- 过度依赖脚本；
- 几乎没有显式领域参考层；
- `SKILL.md` 与脚本之间的角色分工不清；
- 很多知识实际上只能通过读 Python 才看得到。

### 4.2 主要坏味道模式

#### A. 领域硬编码

generic skill 残留 LLM-agent 领域默认值、taxonomy、retrieval pinning、query override。

典型例子：

- `front-matter-writer` 默认 `LLM agents`
- `taxonomy-builder` 内置 tool-using LLM agents taxonomy
- `subsection-briefs` 内置 `is_agent_domain` 和 domain-specific axes
- `arxiv-search` / `literature-engineer` / `dedupe-rank` 内置 agent classics / survey pinning

#### B. 写作模板内嵌在脚本里

典型例子：

- `front-matter-writer` 在脚本中直接写 intro/abstract/discussion prose
- `subsection-writer` 在脚本中直接生成 paragraph skeleton
- `chapter-lead-writer` 在脚本中直接写 lead block 模板

#### C. 用 filler 掩盖 evidence 稀薄

典型例子：

- `evidence-draft` 为满足门槛补统一 caution bullets
- `paper-notes` 为不同 evidence_level 注入统一 limitation prose

这会让系统“看起来更完整”，但也降低了对真实证据缺口的敏感性。

#### D. pipeline / workspace 话术泄漏

reader-facing prose 中不应出现：

- `this pipeline aims`
- `workspace`
- `evidence pack`
- `stage C2/C3`

#### E. 占位/截断符写进产物

例如：

- `...`
- `…`
- `... (N more)`

这类在检测器/调试输出里可以存在，但不应出现在最终交付给读者的 artifact 中。

---

## 5. 目标 skill 结构

建议逐步把 skill 包统一成下面的结构：

```text
skill-name/
├── SKILL.md
├── references/
│   ├── overview.md
│   ├── rubrics.md
│   ├── examples_good.md
│   ├── examples_bad.md
│   └── domain_pack_<domain>.md
├── assets/
│   ├── schema.json
│   ├── templates/
│   ├── examples/
│   └── domain_pack_<domain>.yaml
└── scripts/
    ├── run.py
    └── validate.py
```

### 最低落地要求

对于所有 **script-heavy 且语义/读者导向明显** 的 skill：

- 默认应新增 `references/`（除非能明确说明为什么不需要）
- 至少把一类“判断规则 / exemplars / 领域知识”从脚本迁出去
- 如果 skill 会稳定产出 reader-facing 文本，强烈建议提供 `examples_good.md` 和 `examples_bad.md`

---

## 6. 重构策略总览

### 6.1 先抽知识层，再瘦脚本层

重构顺序必须是：

1. 先把领域知识、rubric、写法范式整理进 `references/`
2. 再让 `SKILL.md` 显式指向这些 reference
3. 再瘦身 `run.py`
4. 最后补 lint / gate / regression check

不能反过来先删脚本逻辑，否则 skill 会短期失去稳定性。

### 6.2 generic skill 与 domain pack 分离

generic skill 不再硬编码某个领域。

如果某个领域确实需要专门支持，应改成显式的 domain pack：

- `references/domain_pack_llm_agents.md`
- `assets/domain_pack_llm_agents.yaml`

由 `SKILL.md` 或 `run.py` 根据输入条件显式选择，而不是把文案和 axes 直接写死在 Python 中。

### 6.3 persona-aware 最终交付物

特别是 ideation 相关 skills：

最终产物应支持 persona-adaptive rendering，而不是继续用单一对称报告。

内部保留统一 structured schema；外部视图根据 persona 渲染成：

- PI 视角：decision memo
- 博士生视角：thesis brief
- RA 视角：starter project picker
- applied scientist 视角：next experiment memo

---

## 7. repo 级规则（强制）

### 7.1 Generic skill 禁止事项

generic skill 的脚本中禁止：

- 默认回退为具体领域名
- 写死大段 prose 模板
- 写死 taxonomy 正文
- 强制段落数（如 `while len(paragraphs) < 10`）
- 用 filler 句达到 gate 下限
- 输出 `this pipeline aims` 等 pipeline 话术
- 在最终 reader-facing 报告中输出 `...` / `…`

### 7.2 强制新增静态审计

建议新增一个 repo-wide skill audit / lint，至少检查：

- `LLM agents` / `Large language model agents` 等默认值
- `while len(paragraphs) <`
- `this pipeline aims`
- `... (N more)`
- reader-facing 产物里是否包含 `workspace`, `stage C*`, `evidence pack`
- 哪些 skill 带 `scripts/` 但没有 `references/`

### 7.3 output hygiene gate

所有 reader-facing artifact 统一增加 hygiene 规则：

- 禁止 ellipsis
- 禁止 TODO/scaffold 泄漏
- 禁止 pipeline jargon
- 禁止 raw internal ids 直接面对最终用户（除非是内部附录）

---

## 8. 重构分期

### Phase 0：建立公共约束

目标：先让后续改造有统一落脚点。

动作：

- 为 P0 / P1 skill 补 `references/` 目录
- 建立 repo 级静态扫描规则
- 建立 `domain_pack` 命名约定
- 约定 `run.py` 的 allowed responsibilities

产出：

- 本文档
- 文件级 P0/P1 清单
- 初版 lint 规则

### Phase 1：writer/planner 类去模板化

目标：先清理最影响最终质量、最容易出现 reader-facing 污染的一组。

重点：

- `front-matter-writer`
- `subsection-writer`
- `chapter-lead-writer`
- `subsection-briefs`
- `taxonomy-builder`

### Phase 2：evidence / ideation / retrieval 去领域内嵌

重点：

- `evidence-draft`
- `paper-notes`
- `survey-visuals`
- `idea-*`
- `arxiv-search`
- `literature-engineer`
- `dedupe-rank`

### Phase 3：回归验证与规范固化

重点：

- 新增 repo-wide audit skill / lint
- 给关键 skills 增加 regression fixtures
- 把 `references/` 的约束写入 `SKILLS_STANDARD.md`

---

## 9. 验收标准

当以下条件满足时，可认为本轮重构达到目标：

### 结构层

- script-heavy 的核心技能均已有 `references/`
- generic skills 的领域支持通过 `domain_pack` 显式加载
- `SKILL.md` 不再承担大量领域正文

### 代码层

- P0 writer 类 skill 不再在脚本中直接写完整 prose 模板
- 不再出现强制补段落数的逻辑
- 不再依靠 filler bullets 达到 gate 下限

### 输出层

- 最终读者可见 artifact 中无 pipeline voice
- 最终读者可见 artifact 中无 ellipsis / truncation markers
- 最终产物的人设和 job-to-be-done 更清晰

### 维护层

- skill 的语义逻辑可通过 `SKILL.md + references/` 理解，而不必通读 Python
- 新 skill 优先按 `reference-first` 模式设计

---

## 10. 一句话总结

这次重构要把仓库从：

- “很多技能 = 很多脚本”

改成：

- “很多技能 = 清晰工作流 + 可读 reference + 少量确定性脚本”

`run.py` 负责执行，`references/` 负责知识，`SKILL.md` 负责方法，`assets/` 负责模板。

只有这样，skills 才真正符合第一性原理，也更接近 Anthropic 风格的可复用、可组合、可审计设计。
