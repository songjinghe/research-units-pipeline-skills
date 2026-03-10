# LLM-Agent Axis Catalog

Use this catalog when the subsection is about agent systems, tool use, planning, memory, coordination, safety, or closely related evaluation topics.

Current compatibility buckets:

- agent loop / action spaces
- planning / reasoning / search
- tool interfaces / orchestration / MCP / APIs
- memory / retrieval / long-horizon state
- multi-agent coordination
- training / alignment / feedback loops
- evaluation / benchmark suites
- safety / security / threat models

Typical axes contributed by the pack include:

- action representation, observation fidelity, recovery policy
- planner/executor design, deliberation method, action grounding
- tool schemas, routing policy, sandboxing, execution contract
- memory type, retrieval source, write/update/forgetting policy
- communication protocol, aggregation, stability risks
- threat model, defense surface, security evaluation protocol

Machine-readable source:

- `assets/domain_packs/llm_agents.json`

Compatibility note: the script still preserves legacy text-to-image axes via a separate asset pack, but this reference focuses on the LLM-agent branch requested in P0.
