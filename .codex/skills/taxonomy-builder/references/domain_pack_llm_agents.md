# Domain Pack: LLM Agents

This pack targets **tool-using LLM agents / agentic systems**, not all LLM papers.

## Scope cues

In scope:
- tool use / function calling / environment interaction
- planning / reasoning loops tied to action selection
- memory / retrieval as agent state
- self-improvement / reflection / adaptation for agents
- multi-agent coordination
- evaluation and risk for deployed agents

Usually out of scope unless central to agent behavior:
- pure prompt engineering without an agent loop
- generic pretrained LLM capability papers with no tool/environment interaction
- application-only buckets that do not change the organizing system question

## Why these four top-level chapters

- **Foundations & Interfaces**: defines the loop, action space, and tool boundary
- **Core Components (Planning + Memory)**: core capability levers for long-horizon behavior
- **Learning, Adaptation & Coordination**: how agents improve or distribute work
- **Evaluation & Risks**: how claims are validated and where deployment risk enters

This shape is intentionally paper-like and avoids an over-fragmented taxonomy.

## Representative-paper policy

Top-level descriptions may append representative `paper_id`s when the core set contains strong title matches.
This is a mapping aid, not a claim of canonical status.
