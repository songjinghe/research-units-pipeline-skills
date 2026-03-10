# Skills 全量审计发现

## 1. 文档目的

本文档汇总针对 `.codex/skills/**` 的一轮全量审计结果，覆盖：

- `SKILL.md`
- `scripts/*.py`
- `assets/`
- 目录结构

重点关注四类问题：

- 领域硬编码
- 话术/模板硬编码
- 占位符/截断符输出风险
- script-heavy / reference-empty 的结构性问题

---

## 2. 结构级发现

### 2.1 总体统计

当前 `.codex/skills/`（审计当时的非隐藏目录快照）概况：

- skills 总数：`88`
- 带 `scripts/` 的 skills：`60`
- 带 `references/reference/ref/refs` 的 skills：`0`
- 带 `assets/examples/templates` 的 skills：极少

### 2.2 结构结论

这说明当前 skill 体系存在明显失衡：

- 语义和行为过多沉入脚本；
- references 层几乎为空；
- 模型若想真正理解某个 skill 的方法论，往往需要读 Python；
- 这与 reference-first 的理想结构相反。

---

## 3. A 类问题：generic skill 中的领域硬编码

### 3.1 `front-matter-writer`

- 默认目标回退成 `LLM agents`：
  - `.codex/skills/front-matter-writer/scripts/run.py:48`
  - `.codex/skills/front-matter-writer/scripts/run.py:50`
- 固定 LLM-agent 领域 intro/related/abstract/discussion/conclusion prose：
  - `.codex/skills/front-matter-writer/scripts/run.py:155`
  - `.codex/skills/front-matter-writer/scripts/run.py:166`
  - `.codex/skills/front-matter-writer/scripts/run.py:180`
  - `.codex/skills/front-matter-writer/scripts/run.py:196`

### 3.2 `taxonomy-builder`

- generic taxonomy builder 内嵌 tool-using LLM agents taxonomy：
  - `.codex/skills/taxonomy-builder/scripts/run.py:170`
  - `.codex/skills/taxonomy-builder/scripts/run.py:188`
  - `.codex/skills/taxonomy-builder/scripts/run.py:193`
  - `.codex/skills/taxonomy-builder/scripts/run.py:210`
  - `.codex/skills/taxonomy-builder/scripts/run.py:214`
  - `.codex/skills/taxonomy-builder/scripts/run.py:231`
  - `.codex/skills/taxonomy-builder/scripts/run.py:248`

### 3.3 `subsection-briefs`

- LLM-agent domain detection：
  - `.codex/skills/subsection-briefs/scripts/run.py:472`
- domain-specific axes / bridge logic：
  - `.codex/skills/subsection-briefs/scripts/run.py:477`

### 3.4 retrieval / ranking 链

- `arxiv-search` 的 LLM-agent special-case query：
  - `.codex/skills/arxiv-search/scripts/run.py:498`
  - `.codex/skills/arxiv-search/scripts/run.py:524`
  - `.codex/skills/arxiv-search/scripts/run.py:529`
- `literature-engineer` 的 classics/surveys pinning：
  - `.codex/skills/literature-engineer/scripts/run.py:1228`
  - `.codex/skills/literature-engineer/scripts/run.py:1233`
- `dedupe-rank` 的 agent classics pinning：
  - `.codex/skills/dedupe-rank/scripts/run.py:363`

---

## 4. B 类问题：脚本中直接内嵌 prose / 模板骨架

### 4.1 `front-matter-writer`

- 直接在脚本中生成大段 reader-facing prose：
  - `.codex/skills/front-matter-writer/scripts/run.py:154`
  - `.codex/skills/front-matter-writer/scripts/run.py:165`
  - `.codex/skills/front-matter-writer/scripts/run.py:178`
  - `.codex/skills/front-matter-writer/scripts/run.py:187`
  - `.codex/skills/front-matter-writer/scripts/run.py:194`

### 4.2 `subsection-writer`

- 第一段固定骨架：
  - `.codex/skills/subsection-writer/scripts/run.py:117`
- 总结/收束固定骨架：
  - `.codex/skills/subsection-writer/scripts/run.py:135`
- 强制补到 10 段：
  - `.codex/skills/subsection-writer/scripts/run.py:143`

### 4.3 `chapter-lead-writer`

- 固定 lead block 模板：
  - `.codex/skills/chapter-lead-writer/scripts/run.py:103`
  - `.codex/skills/chapter-lead-writer/scripts/run.py:104`
  - `.codex/skills/chapter-lead-writer/scripts/run.py:107`

### 4.4 `subsection-briefs`

- thesis 句式选项库内置在代码：
  - `.codex/skills/subsection-briefs/scripts/run.py:303`
- tension 句式库内置在代码：
  - `.codex/skills/subsection-briefs/scripts/run.py:333`

### 4.5 `idea-top3-expander`

- 固定 hypothesis：
  - `.codex/skills/idea-top3-expander/scripts/run.py:54`
- 固定 first-week plan：
  - `.codex/skills/idea-top3-expander/scripts/run.py:64`
  - `.codex/skills/idea-top3-expander/scripts/run.py:66`

---

## 5. C 类问题：filler 掩盖 evidence 不足

### 5.1 `paper-notes`

- 按 evidence level 注入统一 limitation prose：
  - `.codex/skills/paper-notes/scripts/run.py:410`
  - `.codex/skills/paper-notes/scripts/run.py:420`
  - `.codex/skills/paper-notes/scripts/run.py:424`

### 5.2 `evidence-draft`

- evidence sparse 时补统一 caution bullets：
  - `.codex/skills/evidence-draft/scripts/run.py:816`
  - `.codex/skills/evidence-draft/scripts/run.py:818`
- 通过 filler 达到 gate 下限：
  - `.codex/skills/evidence-draft/scripts/run.py:892`
  - `.codex/skills/evidence-draft/scripts/run.py:905`

---

## 6. D 类问题：pipeline 话术与最终读者产物污染

### 6.1 `front-matter-writer`

- 直接输出 `this pipeline aims`：
  - `.codex/skills/front-matter-writer/scripts/run.py:198`
- 与自身 guardrail 冲突：
  - `.codex/skills/front-matter-writer/SKILL.md:9`

### 6.2 相关观察

若不建立 reader-facing hygiene gate，类似下面这些词会继续泄漏到最终文档：

- `pipeline`
- `workspace`
- `stage C*`
- `evidence pack`
- `writer context pack`

---

## 7. E 类问题：占位/截断符输出风险

### 7.1 明显高风险命中

- `.codex/skills/literature-engineer/scripts/run.py:877`
- `.codex/skills/literature-engineer/scripts/run.py:883`
- `.codex/skills/schema-normalizer/scripts/run.py:309`

这些不是检测器里的字符串，而是可能进入 report 的输出逻辑。

### 7.2 中低风险命中

仓库内还有大量 `...` / `…`，但不少属于：

- 注释
- 检测规则描述
- anti-pattern 示例
- 调试辅助文本

这些应与 reader-facing 风险分开处理。

---

## 8. F 类问题：`SKILL.md` 与脚本职责冲突

### 8.1 `front-matter-writer`

- `SKILL.md` 要求：
  - no pipeline jargon：`.codex/skills/front-matter-writer/SKILL.md:9`
  - 避免 `This survey ...` 作为默认 opener：`.codex/skills/front-matter-writer/SKILL.md:151`
- 实际脚本却直接输出固定 survey/pipeline prose。

### 8.2 `chapter-lead-writer`

- `SKILL.md` guardrail：
  - no narration templates：`.codex/skills/chapter-lead-writer/SKILL.md:9`
- 实际脚本直接生成 narration-like templates。

### 8.3 `subsection-writer`

- `SKILL.md` 倾向 paragraph jobs / evidence-bounded writing
- 实际脚本用固定骨架 + 段落数补齐

---

## 9. G 类问题：缺少显式的 `references/` 层

### 当前事实

- script-heavy skills 很多
- `references/` 为零
- 大量本应进入 reference 的内容出现在脚本中：
  - taxonomy
  - axes
  - opener catalog
  - thesis/tension patterns
  - ideation operator logic
  - deliverable shape logic

### 直接后果

- 维护成本高
- skill 行为不可读
- agent 想理解方法论必须读 Python
- 修改领域逻辑必须改代码而不是改文档/配置

---

## 10. 结论

这轮审计表明：

- 当前问题不是“个别脚本写得不优雅”；
- 而是整个 skill 体系在架构上把太多知识、风格和判断逻辑压进了 `run.py`；
- 因此最正确的下一步不是继续 patch script，而是大规模补齐 `references/` / `assets/`，让 scripts 回到确定性执行层。

与这份审计配套的规划文档：

- `SKILLS_REFACTOR_BLUEPRINT.md`
- `SKILLS_REFACTOR_P0_P1_CHECKLIST.md`
- `SKILLS_REFACTOR_EXECUTION_PLAN.md`

