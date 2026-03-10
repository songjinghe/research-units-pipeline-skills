# Good Examples

## Good top-level node

```yaml
- name: Foundations & Interfaces
  description: Problem formulation and interface design for tool-using LLM agents: the agent loop, action spaces, and the tool/environment boundary that constrains reliability. Representative paper_id(s): P0276, P0013.
  children:
    - name: Agent loop and action spaces
      description: Agent loop abstractions (state → decide → act → observe), action representations, environment/tool modeling, and failure recovery assumptions.
```

Why it works:
- chapter-like title
- clear scope cue in the description
- mappable child node
- representative papers are supplementary, not the whole description

## Good generic fallback node

```yaml
- name: Evaluation Protocols
  description: How the field compares systems: benchmark/task design, metrics, human evaluation, and where protocol differences make results hard to compare.
  children:
    - name: Shared-task comparisons
      description: Use this bucket when papers report comparable tasks/metrics and the reader can make head-to-head comparisons.
```

Why it works:
- focuses on a reader question
- descriptions explain when the bucket should be used
- avoids empty placeholder wording
