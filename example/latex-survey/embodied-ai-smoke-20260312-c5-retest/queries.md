# Queries

> 写检索式（关键词/时间窗/排除词），并记录每次检索的变体与原因。
> 标量默认值应由当前 pipeline contract materialize；这里保持通用空模板。

## Primary query
- keywords:
  - "Embodied AI survey"
  - "embodied AI survey"
  - "embodied AI review"
  - "embodied intelligence survey"
  - "embodied agent survey"
  - "robot foundation model survey"
  - "robot learning survey"
  - "robot manipulation survey"
  - "embodied robotics survey"
  - "vision-language-action survey"
  - "vision-language-action model"
  - "robot foundation model"
  - "generalist robot policy"
  - "world model robot"
- exclude:

# Retrieval + scaling knobs
- max_results: "1800"
- core_size: "300"
- per_subsection: ""

# Citation-scope flexibility
- global_citation_min_subsections: ""

# Writing contract
- draft_profile: ""

# Global citation target policy
- citation_target: ""

# Metadata enrichment
- enrich_metadata: ""

# Evidence strength
- evidence_mode: ""
- fulltext_max_papers: ""
- fulltext_max_pages: ""
- fulltext_min_chars: ""

# Optional time window
- time window:
  - from: "2018"
  - to: ""

## Notes
- (fill) scope decisions / dataset constraints
