# Paper Notes — Result Extraction Examples

## Good Examples (specific, checkable, include context)

```
✅ "Achieves 78.3% success rate on ALFWorld (6 tasks, 134 environments), outperforming ReAct baseline by 12.5 points."
✅ "GSM8K accuracy: 92.0% (GPT-4 + self-consistency, k=40), vs 87.1% for chain-of-thought alone."
✅ "Human evaluation (n=50 annotators): 4.2/5 helpfulness rating, but only 2.8/5 for factual accuracy."
```

## Bad Examples (vague, missing context)

```
❌ "Achieves state-of-the-art results." (which benchmark? what metric? compared to what?)
❌ "Outperforms baselines." (which baselines? by how much?)
❌ "Shows promising results on several tasks." (which tasks? what numbers?)
❌ "This survey provides a comprehensive overview of ..." (review-roadmap sentence, not a result)
❌ "In this survey, we present ..." (paper self-description, not evidence)
❌ "Project page: https://..." (artifact availability, not a result)
```

## Extraction Rules

1. **Always include**: task/benchmark name + metric + number (when available)
2. **Always include**: comparison baseline (when the paper claims improvement)
3. **Prefer**: sentences from the abstract that contain numeric values
4. **Fallback**: if no numbers in abstract, use the final "conclusion" sentence
5. **Never**: invent numbers or benchmarks not mentioned in available evidence
6. **Never**: treat survey organization, roadmap, or availability lines as `key_results`
