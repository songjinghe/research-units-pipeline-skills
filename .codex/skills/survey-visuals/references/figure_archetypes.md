# Survey Visuals — Figure Archetypes

## Purpose

Common figure shapes for academic surveys. Use these as structural templates,
not as prose to copy verbatim into output.

## Archetype 1: Pipeline / Dataflow Diagram

- **Purpose**: help readers understand the end-to-end workflow and where evidence comes from
- **Elements**: labeled boxes for each stage, arrows showing data flow, input/output annotations
- **When to use**: when the survey covers a multi-stage process (e.g., retrieval → curation → synthesis)
- **Grounding**: each box should cite at least one representative work

## Archetype 2: Taxonomy / Design Space View

- **Purpose**: provide a navigable mental model of the design space before details
- **Elements**: two-level tree (chapters → subtopics), representative works per leaf, arrows for trade-offs
- **When to use**: when the survey defines a classification of approaches
- **Grounding**: each leaf should have 2–3 cited exemplars

## Archetype 3: Comparison Matrix

- **Purpose**: make quantitative or qualitative differences across works scannable
- **Elements**: rows = works, columns = comparison axes (e.g., method type, benchmark, key metric)
- **When to use**: when 5+ works share comparable evaluation dimensions
- **Grounding**: every cell should be traceable to a note or evidence snippet

## Archetype 4: Evolution / Timeline

- **Purpose**: show how the field has developed over time
- **Elements**: year-anchored milestones with citation markers, grouped by theme if needed
- **When to use**: when temporal progression is a key insight (paradigm shifts, capability jumps)
- **Grounding**: each milestone needs at least one `[@...]` citation

## Anti-Patterns

- ❌ Dumping every paper into the timeline (aim for 8–12 high-signal milestones, not 50)
- ❌ Figure specs that read like prose paragraphs (keep as draw-instructions)
- ❌ Figures without citation grounding (every element needs a paper reference)
