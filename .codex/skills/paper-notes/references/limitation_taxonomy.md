# Paper Notes — Limitation Taxonomy

## Purpose

Limitations in paper notes must be **paper-specific** and **checkable**.
This reference defines the limitation categories and anti-patterns.

## Limitation Categories (use as tags, not as prose templates)

1. **Evaluation gap**: missing ablations, narrow benchmark selection, no human evaluation
2. **Protocol mismatch**: claimed generality but tested only on one domain/language/modality
3. **Scalability concern**: demonstrated on small scale only, cost/latency not reported
4. **Threat model gap**: security/safety claims without adversarial evaluation
5. **Reproducibility issue**: key details missing (hyperparameters, prompts, API versions)
6. **Data limitation**: training/test data overlap, synthetic-only evaluation, no real-world deployment
7. **Comparison gap**: missing comparison with key baselines or contemporaneous work

## Evidence-Level Caveats

When evidence depth is limited, note the limitation of the *evidence*, not the paper:

| Evidence Level | Appropriate Caveat |
|---|---|
| `fulltext` | Focus on paper-specific gaps found in the full text |
| `abstract` | Flag that evaluation details need verification from the full paper |
| `title` | Flag that no method/result claims should be made from title alone |

> **Key rule**: evidence-level caveats should appear **at most once per note**.
> They are metadata about the note quality, not about the paper's research quality.

## Anti-Patterns (forbidden)

- ❌ Generic "may not generalize" without specifying what won't generalize and why
- ❌ Copy-pasting the same limitation across 10+ papers
- ❌ "Future work should explore X" as a limitation (that's the paper's roadmap, not a limitation)
- ❌ Inventing limitations not supported by the available evidence
- ❌ Multiple overlapping evidence-level caveats in the same note

## Good Examples

```
✅ "Evaluated only on ALFWorld and WebShop; no multi-hop reasoning benchmarks tested."
✅ "Tool-call grounding assumes a fixed schema; dynamic API discovery is not addressed."
✅ "Reports GSM8K accuracy but does not control for prompt sensitivity (no temperature sweep)."
```

## Bad Examples

```
❌ "This approach may not generalize to other domains."
❌ "More experiments are needed."
❌ "Evidence level: abstract — validate assumptions in the full paper." (repeated 200 times)
```
