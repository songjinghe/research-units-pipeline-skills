# Good Examples

Minimal good brief fragment:

```json
{
  "sub_id": "3.2",
  "title": "Planning and reasoning loops",
  "thesis": "Design choices in Planning and reasoning loops create decision-relevant trade-offs—especially in control loop design (planner / executor, search) and deliberation method (CoT / ToT / MCTS)—and meaningful comparisons depend on consistent evaluation protocols.",
  "axes": [
    "control loop design (planner / executor, search)",
    "deliberation method (CoT / ToT / MCTS)",
    "action grounding (tool calls vs environment actions)",
    "evaluation protocol",
    "failure modes and limitations"
  ],
  "bridge_terms": ["planner/executor", "search", "deliberation", "benchmarks/metrics", "latency budget"],
  "tension_statement": "In Planning and reasoning loops, a recurring tension is deliberation depth versus cost: more planning can improve reliability but increases latency and budget sensitivity."
}
```

Why this is good:

- thesis is execution-oriented, not narration
- axes are atomic and checkable
- bridge terms are compact handles with lexical value for later evidence matching
- tension states a real trade-off without inventing results
- later clusters should still retain unique paper pools on both sides after bridge-paper removal
