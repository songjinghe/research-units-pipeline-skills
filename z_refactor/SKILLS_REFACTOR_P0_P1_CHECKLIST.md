# Skills 重构 P0 / P1 文件级改造清单

## 1. 文档用途

本文档是《`SKILLS_REFACTOR_BLUEPRINT.md`》的执行版清单。

它不再讨论抽象原则，而是逐 skill 给出：

- 现有问题
- 需要新增的 `references/` / `assets/`
- 需要迁移/删除/瘦身的 `run.py` 逻辑
- 建议新增的 sidecar / lint / gate
- 优先级与验收标准

---

## 2. P0：必须先改的一组

### P0-1 `front-matter-writer`

**涉及文件**
- `.codex/skills/front-matter-writer/SKILL.md`
- `.codex/skills/front-matter-writer/scripts/run.py`

**当前问题**
- 默认领域回退：`run.py:48`, `run.py:50`
- 固定 intro 模板：`run.py:154`
- 固定 related-work 模板：`run.py:165`
- 固定 abstract 模板：`run.py:178`
- 固定 discussion / conclusion 模板：`run.py:187`, `run.py:194`
- pipeline voice：`run.py:198`
- 与 guardrail 冲突：`SKILL.md:9`

**新增目录/文件**
- `.codex/skills/front-matter-writer/references/overview.md`
- `.codex/skills/front-matter-writer/references/abstract_archetypes.md`
- `.codex/skills/front-matter-writer/references/introduction_jobs.md`
- `.codex/skills/front-matter-writer/references/related_work_positioning.md`
- `.codex/skills/front-matter-writer/references/discussion_conclusion_patterns.md`
- `.codex/skills/front-matter-writer/references/forbidden_stems.md`
- `.codex/skills/front-matter-writer/references/examples_good.md`
- `.codex/skills/front-matter-writer/references/examples_bad.md`
- `.codex/skills/front-matter-writer/assets/front_matter_context_schema.json`

**`SKILL.md` 改造**
- 增加“何时读取哪个 reference”的指引
- 明确 `run.py` 仅负责 context materialization，不负责 prose writing
- 将当前过长的写作范式说明精简为索引，并外链到 `references/`

**`run.py` 改造**
- 删除默认 `LLM agents` 兜底
- 删除直接写 intro/related/abstract/discussion/conclusion prose 的逻辑
- 保留：
  - 读取 outline / goal / retrieval stats / citation pools
  - 生成 `output/FRONT_MATTER_CONTEXT.json`
  - 生成 `output/FRONT_MATTER_REPORT.md`
- 增加 reader-facing prose lint：禁止 `pipeline`, `workspace`, `stage C*`

**建议新增 sidecar**
- `output/FRONT_MATTER_CONTEXT.json`

**验收标准**
- `run.py` 中不再出现 `LLM agents`
- `run.py` 中不再直接拼整段 front matter prose
- `SKILL.md` 能清楚指引模型读取 `references/`

---

### P0-2 `subsection-writer`

**涉及文件**
- `.codex/skills/subsection-writer/SKILL.md`
- `.codex/skills/subsection-writer/scripts/run.py`

**当前问题**
- 固定开场骨架：`run.py:117`
- 固定收束骨架：`run.py:135`
- 强制补到 10 段：`run.py:143`
- 风格/论证动作被脚本决定，而不是被 references/examples 决定

**新增目录/文件**
- `.codex/skills/subsection-writer/references/overview.md`
- `.codex/skills/subsection-writer/references/paragraph_jobs.md`
- `.codex/skills/subsection-writer/references/opener_catalog.md`
- `.codex/skills/subsection-writer/references/contrast_moves.md`
- `.codex/skills/subsection-writer/references/eval_anchor_patterns.md`
- `.codex/skills/subsection-writer/references/limitation_moves.md`
- `.codex/skills/subsection-writer/references/examples_good.md`
- `.codex/skills/subsection-writer/references/examples_bad.md`
- `.codex/skills/subsection-writer/assets/section_context_schema.json`

**`SKILL.md` 改造**
- 明确 paragraph job-based drafting，而不是 paragraph-count drafting
- 明确需要读取 `paragraph_jobs.md` 和 `examples_*`
- 加入“当 evidence 薄时必须 reroute 到 `evidence-selfloop`”的明确说明

**`run.py` 改造**
- 删除固定 prose 模板
- 删除 `while len(paragraphs) < 10`
- 改为：
  - 组装 `section_context.json`
  - 记录 required moves 是否齐全
  - 写 manifest 与 validation report

**替代 gate**
- 新 rule：
  - thesis move 存在
  - contrast move >= 2
  - evaluation anchor >= 1
  - limitation move >= 1
- 不再用“段落数达到下限”做质量门

**验收标准**
- `run.py` 不再直接拼 paragraph skeleton
- 不再出现固定段落数下限
- `SKILL.md` 和 `references/` 构成可读的写作方法系统

---

### P0-3 `chapter-lead-writer`

**涉及文件**
- `.codex/skills/chapter-lead-writer/SKILL.md`
- `.codex/skills/chapter-lead-writer/scripts/run.py`

**当前问题**
- 固定 chapter lead 模板：`run.py:103`, `run.py:104`, `run.py:107`
- 与 `SKILL.md` 中的 “no narration templates” 冲突：`SKILL.md:9`

**新增目录/文件**
- `.codex/skills/chapter-lead-writer/references/overview.md`
- `.codex/skills/chapter-lead-writer/references/lead_block_archetypes.md`
- `.codex/skills/chapter-lead-writer/references/throughline_patterns.md`
- `.codex/skills/chapter-lead-writer/references/bridge_examples.md`
- `.codex/skills/chapter-lead-writer/references/bad_narration_examples.md`
- `.codex/skills/chapter-lead-writer/assets/chapter_lead_context_schema.json`

**`run.py` 改造**
- 删除直接写固定 lead prose 的逻辑
- 改为生成 `chapter_lead_context.jsonl`
- 保留 citation collection 与 file routing

**验收标准**
- `run.py` 中不再直接存在 chapter lead prose 模板
- `SKILL.md` 明确引用 `references/` 中的 lead archetypes

---

### P0-4 `subsection-briefs`

**涉及文件**
- `.codex/skills/subsection-briefs/SKILL.md`
- `.codex/skills/subsection-briefs/scripts/run.py`

**当前问题**
- thesis 句式选项在代码里：`run.py:303`
- tension 句式在代码里：`run.py:333`
- agent-domain 判定与 axes 写死：`run.py:472`
- 这类内容应为 reference / domain pack，而不是 Python 常量

**新增目录/文件**
- `.codex/skills/subsection-briefs/references/overview.md`
- `.codex/skills/subsection-briefs/references/thesis_patterns.md`
- `.codex/skills/subsection-briefs/references/tension_patterns.md`
- `.codex/skills/subsection-briefs/references/axis_catalog_generic.md`
- `.codex/skills/subsection-briefs/references/axis_catalog_llm_agents.md`
- `.codex/skills/subsection-briefs/references/bridge_terms.md`
- `.codex/skills/subsection-briefs/references/examples_good.md`
- `.codex/skills/subsection-briefs/assets/domain_packs/llm_agents.yaml`
- `.codex/skills/subsection-briefs/assets/brief_schema.json`

**`run.py` 改造**
- domain 判定逻辑保留为“选择某个 domain pack”，不再内嵌 domain 文案
- thesis/tension options 从 `references/` 或 `assets/*.yaml` 读取
- 代码只做：
  - evidence summary
  - domain trigger match
  - structure fill
  - validation

**验收标准**
- domain-specific prose 不再硬编码在 Python 中
- axes catalog 通过 domain pack 显式加载

---

### P0-5 `taxonomy-builder`

**涉及文件**
- `.codex/skills/taxonomy-builder/SKILL.md`
- `.codex/skills/taxonomy-builder/scripts/run.py`

**当前问题**
- generic taxonomy builder 直接切换到 `_llm_agent_taxonomy`
- 内嵌完整 tool-using LLM agents taxonomy：`run.py:170+`

**新增目录/文件**
- `.codex/skills/taxonomy-builder/references/overview.md`
- `.codex/skills/taxonomy-builder/references/taxonomy_principles.md`
- `.codex/skills/taxonomy-builder/references/archetypes_generic.md`
- `.codex/skills/taxonomy-builder/references/domain_pack_llm_agents.md`
- `.codex/skills/taxonomy-builder/references/examples_good.md`
- `.codex/skills/taxonomy-builder/references/examples_bad.md`
- `.codex/skills/taxonomy-builder/assets/domain_packs/llm_agents.yaml`
- `.codex/skills/taxonomy-builder/assets/taxonomy_schema.json`

**`run.py` 改造**
- 删除内嵌 taxonomy 正文
- 改为：
  - generic builder + optional domain pack loader
  - 领域 pack 通过 YAML/JSON 驱动

**验收标准**
- `run.py` 不再含完整 LLM-agent taxonomy prose
- taxonomy 文案可通过 `references/` / `assets/` 修改而无需改代码

---

## 3. P1：紧接着改的一组

### P1-1 `outline-builder`

**涉及文件**
- `.codex/skills/outline-builder/SKILL.md`
- `.codex/skills/outline-builder/scripts/run.py`

**当前问题**
- `Related Work` 默认夹带 agent/tool/RAG/security framing：`run.py:57`, `run.py:58`

**新增文件**
- `.codex/skills/outline-builder/references/intro_related_patterns.md`
- `.codex/skills/outline-builder/references/examples_good.md`
- `.codex/skills/outline-builder/assets/outline_defaults.yaml`

**改造方向**
- 将 intro/related 默认 bullet 模板外置
- 脚本只负责 skeleton materialization

---

### P1-2 `evidence-draft`

**涉及文件**
- `.codex/skills/evidence-draft/SKILL.md`
- `.codex/skills/evidence-draft/scripts/run.py`

**当前问题**
- sparse-evidence 时补统一 caution bullets：`run.py:816`
- 用 filler 满足 gate：`run.py:892`, `run.py:905`

**新增文件**
- `.codex/skills/evidence-draft/references/evidence_quality_policy.md`
- `.codex/skills/evidence-draft/references/evaluation_anchor_rules.md`
- `.codex/skills/evidence-draft/references/block_vs_downgrade.md`
- `.codex/skills/evidence-draft/references/examples_sparse_evidence.md`
- `.codex/skills/evidence-draft/assets/evidence_pack_schema.json`

**改造方向**
- filler 改为 confidence / blocker / route signal
- gate 允许“明确失败”，不鼓励“句子补齐”

---

### P1-3 `paper-notes`

**涉及文件**
- `.codex/skills/paper-notes/SKILL.md`
- `.codex/skills/paper-notes/scripts/run.py`

**当前问题**
- limitations 按 evidence_level 注入统一 prose：`run.py:410`, `run.py:420`, `run.py:424`

**新增文件**
- `.codex/skills/paper-notes/references/note_schema.md`
- `.codex/skills/paper-notes/references/limitation_taxonomy.md`
- `.codex/skills/paper-notes/references/result_extraction_examples.md`
- `.codex/skills/paper-notes/assets/note_schema.json`

**改造方向**
- limitation 变成 structured tags / flags
- 最终 prose 交给上游写作 skill 结合 references 决定

---

### P1-4 `survey-visuals`

**涉及文件**
- `.codex/skills/survey-visuals/SKILL.md`
- `.codex/skills/survey-visuals/scripts/run.py`

**当前问题**
- Figure 1/2 被写死为 pipeline + taxonomy 图：`run.py:320`, `run.py:325`

**新增文件**
- `.codex/skills/survey-visuals/references/figure_archetypes.md`
- `.codex/skills/survey-visuals/references/timeline_patterns.md`
- `.codex/skills/survey-visuals/assets/figure_spec_templates.yaml`

**改造方向**
- 用 archetype 机制替代写死 figure narratives
- 脚本只做 spec materialization

---

### P1-5 `idea-shortlist-curator`

**涉及文件**
- `.codex/skills/idea-shortlist-curator/SKILL.md`
- `.codex/skills/idea-shortlist-curator/scripts/run.py`

**当前问题**
- why-not 默认文案：`run.py:99`
- ranking explanation 仍偏统一句式

**新增文件**
- `.codex/skills/idea-shortlist-curator/references/pi_memo_examples.md`
- `.codex/skills/idea-shortlist-curator/references/project_brief_examples.md`
- `.codex/skills/idea-shortlist-curator/references/operator_catalog.md`
- `.codex/skills/idea-shortlist-curator/assets/shortlist_schema.json`

**改造方向**
- 原因解释外置为 rubric + examples
- 脚本只做 ranking/filter/materialization

---

### P1-6 `idea-memo-writer`

**涉及文件**
- `.codex/skills/idea-memo-writer/SKILL.md`
- `.codex/skills/idea-memo-writer/scripts/run.py`

**当前问题**
- 需要确保终态始终对齐当前 active `idea-brainstorm` 合同：`output/REPORT.md`、`output/APPENDIX.md`、`output/REPORT.json`
- persona-aware 展示与内部 trace 层之间的边界需要显式化

**新增文件**
- `.codex/skills/idea-memo-writer/references/final_deliverable_shapes.md`
- `.codex/skills/idea-memo-writer/references/persona_views.md`
- `.codex/skills/idea-memo-writer/references/report_examples_good.md`
- `.codex/skills/idea-memo-writer/references/report_examples_bad.md`
- `.codex/skills/idea-memo-writer/assets/report_schema.json`

**改造方向**
- 内部仍保留 shortlist / screening / trace 链
- 终态默认文档保持为 `REPORT.md` memo，而不是回退到旧 `Top-3` 合同
- persona-aware 视图通过 references / assets 外置，而不是用脚本硬编码同一套 narrative

---

### P1-7 `arxiv-search`

**涉及文件**
- `.codex/skills/arxiv-search/SKILL.md`
- `.codex/skills/arxiv-search/scripts/run.py`

**当前问题**
- LLM-agent special-case query：`run.py:498`
- names whitelist：`run.py:537`

**新增文件**
- `.codex/skills/arxiv-search/references/query_patterns.md`
- `.codex/skills/arxiv-search/assets/domain_query_overrides.yaml`

**改造方向**
- query override 外置
- 脚本只负责 apply override，不直接写死 domain rule

---

### P1-8 `literature-engineer`

**涉及文件**
- `.codex/skills/literature-engineer/SKILL.md`
- `.codex/skills/literature-engineer/scripts/run.py`

**当前问题**
- domain classics pinning：`run.py:1233`
- 截断符输出：`run.py:877`, `run.py:883`

**新增文件**
- `.codex/skills/literature-engineer/references/pinning_policy.md`
- `.codex/skills/literature-engineer/references/multi_route_retrieval.md`
- `.codex/skills/literature-engineer/assets/domain_seed_sets.yaml`

**改造方向**
- seed set 外置
- output report 不再使用 `...`
- 对大列表用 “showing first N of M” 或 sidecar list file

---

### P1-9 `dedupe-rank`

**涉及文件**
- `.codex/skills/dedupe-rank/SKILL.md`
- `.codex/skills/dedupe-rank/scripts/run.py`

**当前问题**
- LLM-agent classics pinning：`run.py:363`

**新增文件**
- `.codex/skills/dedupe-rank/references/ranking_policy.md`
- `.codex/skills/dedupe-rank/assets/pinning_policy.yaml`

**改造方向**
- pinning data-driven
- docs 中保留 policy rationale，脚本不内置具体领域 paper IDs

---

## 4. repo 级配套改动

### 4.1 新增规范文档/更新文档

**涉及文件**
- `SKILLS_STANDARD.md`
- `SKILL_INDEX.md`

**改造内容**
- 增加 `references/` 必选建议
- 明确 `run.py` 的 allowed responsibilities
- 增加 domain pack 规范
- 增加 reader-facing hygiene 规则

### 4.2 新增静态审计器

**建议新增文件**
- `scripts/audit_skills.py`
- `docs/SKILL_AUDIT_RULES.md`

**规则**
- 检查 generic skill 中的领域默认值
- 检查固定段落数模式
- 检查 `this pipeline aims`
- 检查 `...` / `…` / `... (N more)`
- 检查 script-heavy but no references
- 检查 `SKILL.md` 是否超重
- 检查 `SKILL.md` 是否显式导航到 `references/`

### 4.3 新增 reference-first 模板

**建议新增文件**
- `.codex/skills/_template_reference_first/SKILL.md`
- `.codex/skills/_template_reference_first/references/overview.md`
- `.codex/skills/_template_reference_first/references/examples_good.md`
- `.codex/skills/_template_reference_first/references/examples_bad.md`
- `.codex/skills/_template_reference_first/assets/schema.json`
- `.codex/skills/_template_reference_first/scripts/run.py`

**配套改动**
- `scripts/new_skill.py` 默认支持 reference-first 骨架
- `scripts/validate_repo.py` / `scripts/generate_skill_graph.py` 忽略 `_template_*` 目录

---

## 5. 推荐执行顺序

### Sprint 1
- Phase 0 foundations（`audit_skills.py` / template skill / standards / toolchain compatibility）
- `front-matter-writer`
- `subsection-writer`
- `chapter-lead-writer`

### Sprint 2
- `subsection-briefs`
- `taxonomy-builder`
- `outline-builder`
- `evidence-draft`
- `paper-notes`

### Sprint 3
- `idea-shortlist-curator`
- `idea-memo-writer`
- `survey-visuals`
- `arxiv-search`
- `literature-engineer`
- `dedupe-rank`

---

## 6. 完成定义

一个 skill 被视为完成 reference-first 重构，当且仅当：

- `SKILL.md` 明确说明何时加载 `references/`
- 关键领域知识已迁入 `references/` 或 `assets/`
- `run.py` 中不再包含大段 prose 模板或领域默认值
- reader-facing 输出通过 hygiene gate
- skill 行为可以通过读 `SKILL.md + references/` 理解，而不必通读 Python

---

## 7. 与本清单配套的主文档

- 总体原则与分期：`SKILLS_REFACTOR_BLUEPRINT.md`

