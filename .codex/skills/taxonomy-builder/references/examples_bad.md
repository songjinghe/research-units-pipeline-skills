# Bad Examples

## Bad placeholder taxonomy

```yaml
- name: Methods
  description: Papers and ideas centered on methods.
  children:
    - name: Overview
      description: Key aspects of methods.
    - name: Benchmarks
      description: Key aspects of benchmarks.
```

Problems:
- generic names with no chapter-level meaning
- descriptions are template boilerplate
- leaf buckets do not explain inclusion boundaries

## Bad over-fragmented taxonomy

```yaml
- name: Prompting
  description: Prompting papers.
- name: Tools
  description: Tool papers.
- name: Planning
  description: Planning papers.
- name: Memory
  description: Memory papers.
- name: Agents
  description: Agent papers.
```

Problems:
- too many thin top-level buckets
- keyword clustering instead of reader-oriented structure
- impossible to map cleanly into a paper-like outline later

## Bad reader-facing leakage

Avoid final descriptions containing:
- `TODO`
- `...` / `…`
- `Misc` / `Other`
- prose about pipeline stages or workspace mechanics
