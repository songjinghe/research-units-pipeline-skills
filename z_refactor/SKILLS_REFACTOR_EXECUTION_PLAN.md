# Skills 重构执行计划

## 1. 文档目标

本文档把以下两份规划文档继续向前推进到“可执行计划”层：

- `SKILLS_REFACTOR_BLUEPRINT.md`
- `SKILLS_REFACTOR_P0_P1_CHECKLIST.md`

本计划回答的问题是：

- 应该先改什么，后改什么；
- 每一轮改造的目标、依赖、风险是什么；
- 哪些改造可以并行，哪些必须串行；
- 每个阶段完成后，如何知道它真的变好了。

---

## 2. 总体策略

### 2.1 总原则

执行顺序遵循四条原则：

1. **先建约束，再改行为**
   - 先把 lint / gate / package structure 约束立起来，避免一边改一边继续长出新的脚本硬编码。

2. **先改最影响最终质量的 writer 类 skill**
   - 因为这些最容易把 pipeline voice、模板味和领域默认值直接暴露给最终读者。

3. **先抽出 references，再瘦脚本**
   - 否则脚本一删，skill 就会短时间失去“知识承载层”。

4. **先解决 generic skill 的领域污染，再处理显式 domain pack**
   - generic skill 必须先恢复通用性，之后再把领域支持显式外置化。

### 2.2 工作流模式

每个 skill 的改造统一采用下面的顺序：

1. 审核现有 `SKILL.md`
2. 列出脚本中不该存在的语义逻辑
3. 增补 `references/` 与 `assets/`
4. 修改 `SKILL.md` 让其索引 references
5. 瘦身 `run.py`
6. 加静态检查
7. 用最小回归样例验证

---

## 3. 分期安排

## Phase 0：建立基础约束

### 目标

让后续的每次 skill 改造都有统一的工程约束与验收方式。

### 要做的事

#### 0.1 新增 repo-wide 审计器

建议新增：

- `scripts/audit_skills.py`
- `docs/SKILL_AUDIT_RULES.md`

初版至少检查：

- generic skill 脚本中是否出现领域默认值
- 是否出现 `LLM agents` / `Large language model agents`
- 是否出现 `this pipeline aims`
- 是否出现 `while len(paragraphs) <`
- 是否出现 reader-facing `...` / `…` / `... (N more)`
- 是否是 script-heavy but no references
- `SKILL.md` 是否过重（超长 / 语义堆叠）
- `SKILL.md` 是否明确说明何时读取哪些 `references/`

#### 0.2 建立 reference-first 模板 skill

建议新增：

- `.codex/skills/_template_reference_first/SKILL.md`
- `.codex/skills/_template_reference_first/references/overview.md`
- `.codex/skills/_template_reference_first/references/examples_good.md`
- `.codex/skills/_template_reference_first/references/examples_bad.md`
- `.codex/skills/_template_reference_first/assets/schema.json`
- `.codex/skills/_template_reference_first/scripts/run.py`

用途：

- 后续新 skill 直接从这个模板出发；
- 后续旧 skill 重构也有统一形态可参考。
- 该模板目录应被 discovery/validation 工具视为内部模板而非正式 skill。

#### 0.3 更新规范文档

需要修改：

- `SKILLS_STANDARD.md`
- `SKILL_INDEX.md`

补充内容：

- `references/` 的职责与最低要求
- `run.py` 的 allowed responsibilities
- generic skill 禁止事项
- domain pack 命名与装配方式
- reader-facing hygiene 规则

### 依赖

- 无前置依赖，可先独立完成。

### 完成定义

- 仓库中有一个可运行的 `audit_skills.py`
- 有一个 reference-first skill 模板
- `SKILLS_STANDARD.md`、`SKILL_INDEX.md`、`docs/SKILL_AUDIT_RULES.md` 已更新
- `scripts/new_skill.py` 与 `scripts/validate_repo.py` 已兼容 reference-first 结构
- 审计规则先以 warn-only / 基线报告方式落地，对全仓不立即作为 blocking gate

---

## Phase 1：清理 writer 类 skill（P0 第一批）

### 目标

先解决最直接影响最终产物质量的技能。

### 1.1 `front-matter-writer`

**优先级**：最高

**为什么先做**
- 它直接面向读者写 front matter；
- 目前存在领域硬编码、固定句式、pipeline 话术泄漏；
- 还与自己的 guardrail 直接冲突。

**改造结果目标**
- `run.py` 只产 context / report
- 真正的写法范式迁入 `references/`
- pipeline voice 被彻底清除

### 1.2 `subsection-writer`

**优先级**：最高

**为什么先做**
- 它是正文生成的主通道；
- 固定骨架与固定段落数会把模板味扩散到整篇草稿。

**改造结果目标**
- paragraph jobs 替代 paragraph counts
- 通过 references/examples 约束写法，而不是脚本内置句式

### 1.3 `chapter-lead-writer`

**优先级**：高

**为什么先做**
- H2 lead 的模板味会显著影响 paper voice；
- 目前脚本与 `SKILL.md` 的 “no narration templates” 明显冲突。

### 1.4 `subsection-briefs`

**优先级**：高

**为什么先做**
- 它是 writer 之前的上游 planning layer；
- 如果 thesis/tension/axes 仍然写死在脚本里，下游再 clean 也会继续长出同样的节奏。

### 1.5 `taxonomy-builder`

**优先级**：高

**为什么先做**
- 它决定了整个 survey 的组织框架；
- 当前 generic skill 中的 LLM-agent taxonomy 硬编码会污染大量后续 skill。

### 建议并行关系

可分为两个并行组：

- 组 A：`front-matter-writer` + `chapter-lead-writer`
- 组 B：`subsection-writer` + `subsection-briefs`
- `taxonomy-builder` 建议单独改，因为它会影响若干后续 skill 的 domain pack 设计。

### 阶段验收

这一阶段完成后应满足：

- writer 类核心 skills 都已有 `references/`
- writer 类脚本中不再直接拼读者可见的完整 prose 模板
- 不再出现固定段落数补齐
- 不再有 `LLM agents` 默认回退

---

## Phase 2：清理 planner / evidence 层（P1 第二批）

### 目标

防止“上游 planning/evidence 层带着模板化 bias 进入下游”。

### 2.1 `outline-builder`

**问题本质**
- 把 domain framing 塞进 outline skeleton。

**目标**
- intro/related 模式外置到 references / assets
- 脚本只生成 outline 结构

### 2.2 `evidence-draft`

**问题本质**
- 用 filler bullets 掩盖 evidence 稀薄。

**目标**
- sparse evidence 时输出 blocker / confidence / reroute，而不是补文字。

### 2.3 `paper-notes`

**问题本质**
- limitations 通过统一 prose 注入，而不是 structured annotation。

**目标**
- limitation taxonomy 外置
- script 只做 extraction + tagging

### 2.4 `survey-visuals`

**问题本质**
- 图规格被写死成 pipeline/taxonomy 图。

**目标**
- figure archetype 外置
- script 只负责 materialize spec

### 阶段验收

- evidence/planning 类 skills 都能在 references 中看到 rubric 与 examples
- sparse evidence 时不再靠 filler 过 gate
- generic visual skill 不再默认讲某一条 pipeline 的故事

---

## Phase 3：清理 ideation 与 retrieval/ranking（P1 第三批）

### 目标

解决 ideation / retrieval 层的领域 pinning 与对称模板化问题。

### 3.1 `idea-shortlist-curator`
### 3.2 `idea-memo-writer`

**目标**
- 保持 active `idea-brainstorm` 合同不回退：终态仍是 `REPORT.md` / `APPENDIX.md` / `REPORT.json`
- rationale、persona view、deliverable shape 外置到 references
- script 只处理 shortlist 结构、memo synthesis context、materialization

### 3.3 `arxiv-search`
### 3.4 `literature-engineer`
### 3.5 `dedupe-rank`

**目标**
- 把 LLM-agent special-case query / pinning / seed set 全部外置到 domain packs
- 保留“有条件启用”的能力，但不再写死在脚本里

### 阶段验收

- ideation 最终产物的人设与目标更清晰
- retrieval/ranking 逻辑对领域 pinning 变成 data-driven
- reports 中不再输出 `...`

---

## Phase 4：系统回归与规范固化

### 目标

把本轮重构从“局部修复”变成 repo 的新基线。

### 要做的事

#### 4.1 把 `audit_skills.py` 接入日常流程

建议：

- 作为本地维护脚本
- 作为 CI/预提交检查的一部分（如果后续要接）

#### 4.2 回归样例

建议为核心 P0 / P1 skills 建立最小 regression fixtures，至少覆盖：

- 不再出现领域默认值
- 不再出现 reader-facing ellipsis
- 不再出现 pipeline voice
- 不再出现固定段落数补齐

#### 4.3 规范固化

把 reference-first 原则写进：

- `SKILLS_STANDARD.md`
- skill 模板
- 新增 skill 的审核 checklist

---

## 4. 风险与缓解

### 风险 1：脚本删太快，skill 短期失去稳定性

**缓解**
- 先新增 `references/` 和 `assets/`
- 再删脚本语义逻辑
- 每次只替换一个层面的语义

### 风险 2：references 变多，`SKILL.md` 反而失去可读性

**缓解**
- `SKILL.md` 只作为目录和导航，不复制 reference 内容
- 每个 skill 最多 1 个 `overview.md` + 若干专题文件

### 风险 3：domain pack 外置后，能力暂时变弱

**缓解**
- 先把已有领域逻辑“原样迁到 YAML/MD”，确保行为一致
- 第二步再做抽象化和清洗

### 风险 4：reader-facing 质量门过严，阻塞现有 pipelines

**缓解**
- Phase 1 先对新重构 skills 开启严格门
- 旧 skill 逐步迁移，不一次性全仓切换

---

## 5. 建议的执行角色划分

如果要并行推进，建议按“关注点”而不是按 pipeline 划分：

### 角色 A：writer / voice 清理

负责：
- `front-matter-writer`
- `subsection-writer`
- `chapter-lead-writer`
- `survey-visuals`

### 角色 B：planner / evidence 结构化

负责：
- `subsection-briefs`
- `taxonomy-builder`
- `outline-builder`
- `evidence-draft`
- `paper-notes`

### 角色 C：ideation / retrieval 外置化

负责：
- `idea-*`
- `arxiv-search`
- `literature-engineer`
- `dedupe-rank`

### 角色 D：规范与工具链

负责：
- `audit_skills.py`
- `SKILLS_STANDARD.md`
- reference-first 模板 skill
- regression fixtures

---

## 6. 建议的里程碑

### Milestone A
- Phase 0 完成
- 有统一模板与静态审计器

### Milestone B
- writer 类 P0 skills 全部 reference-first 化
- 前台 prose 质量显著改善

### Milestone C
- evidence / planning 层不再靠 filler 维持完整性
- taxonomy / axes 已可通过 domain pack 配置

### Milestone D
- ideation / retrieval 层的领域 pinning 外置完成
- 终态输出更 persona-aware

### Milestone E
- skill 审计规则固化
- 后续新 skill 默认走 reference-first 模式

---

## 7. 完成定义

这份执行计划完成，不代表重构完成。

当下面这几件事同时成立时，才算整个 refactor 成功：

- repo 中核心 script-heavy skills 全部具备 `references/`
- writer 类脚本不再内嵌完整 prose 模板
- generic skills 不再默认回退到 LLM-agent 领域
- ideation / retrieval 的领域规则全部外置为 domain packs
- 最终读者可见 artifact 中无 pipeline voice、ellipsis、模板性 filler
- 新 skill 可以直接按 reference-first 模板创建

