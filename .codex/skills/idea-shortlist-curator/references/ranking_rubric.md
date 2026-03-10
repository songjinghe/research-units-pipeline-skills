# Ranking Rubric

## Risk assessment signals

The script maps evidence confidence and program shape into risk notes:

| Condition | Risk note |
|---|---|
| `evidence_confidence` starts with "low" | literature anchor is still abstract-first |
| `program_kind` contains "protocol" | decisive test is protocol-sensitive |
| `program_kind` contains "budget" | normalizing the main confound needs a heavier control argument |
| fallback | main risk is whether the confound has already been controlled |

## Deferral reasons

Directions outside the lead set get one of:

| Condition | Reason pattern |
|---|---|
| same `program_kind` as a lead | overlaps the lead set's wedge, weaker prior-work gap |
| same `cluster` as a lead | cluster already represented, slower first control |
| low evidence confidence | literature anchor too abstract-first for lead rank |
| fallback | slower to turn into a decisive first reading/probe cycle |

## When to customize

- If all directions come from the same cluster, the diversity pass may not help — consider running more direction generation first.
- If risk notes sound too generic for your domain, write domain-specific risk phrases here and reference them from the SKILL.md workflow.
