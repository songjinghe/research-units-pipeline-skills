# Appendix to the Research Idea Brainstorm Memo

## A. Deferred but still promising directions

### Verification or just expensive redundancy?
- One-line thesis: Verification-heavy pipelines may look stronger because they retry, re-check, or filter more often, not necessarily because they add a distinct reasoning mechanism.
- Program kind: verification audit
- Why interesting: This is not just another benchmark wedge. It opens a verification audit line around verification loop: whether verification contributes a distinct reasoning mechanism or mostly acts as expensive redundancy.
- Why not prioritized now: sits in a cluster already represented in the lead set, while its first decisive control currently looks slower.

### Retrieval policy or memory content?
- One-line thesis: Reported memory gains are often hard to interpret because memory content and retrieval triggers move together;
- Program kind: protocol sensitivity
- Why interesting: This is not just another benchmark wedge.
- Why not prioritized now: is still promising, but the literature anchor is too abstract-first for lead-set rank right now.

## B. Anchor papers and what to extract

### Observability granularity vs planner depth
- Program kind: causal attribution
- Lead-set reason: Leads because it offers the fastest path to a decisive causal attribution result in agent loop and action spaces, and because it has the clearest path to a thesis-sized contribution if the control holds.
| Anchor paper | Why read now | What to extract | Current evidence hook | Kill signal |
| --- | --- | --- | --- | --- |
| ReAct: Synergizing Reasoning and Acting in Language Models | Closest agent loop and action spaces anchor with a concrete result hook on ALFWorld/WebShop: ALFWorld/WebShop: 34%/10% success-rate gains over imitation/RL baselines. | Extract the metric and comparator, then check whether what the agent sees at each step, which ablations vary planner depth, and whether the action interface stays fixed. | ALFWorld/WebShop: 34%/10% success-rate gains over imitation/RL baselines. | Weaken this direction if the paper already shows an anchor paper already fixes observation access while varying planner quality and the main conclusion still survives. |
| Tree of Thoughts: Deliberate Problem Solving with Large Language Models | Closest agent loop and action spaces anchor with a concrete result hook on ALFWorld/WebShop: reported setting: 4%/74% success-rate gains in the reported comparison. | Extract the metric and comparator, then check whether what the agent sees at each step, which ablations vary planner depth, and whether the action interface stays fixed. | reported setting: 4%/74% success-rate gains in the reported comparison. | Weaken this direction if the paper already shows an anchor paper already fixes observation access while varying planner quality and the main conclusion still survives. |
| Agentic Large Language Models, a survey | Closest agent loop and action spaces anchor with a concrete result hook on ALFWorld/WebShop: Methods: Agentic LLMs are LLMs that (1) reason, (2) act, and (3) interact. | Extract the metric and comparator, then check whether what the agent sees at each step, which ablations vary planner depth, and whether the action interface stays fixed. | Methods: Agentic LLMs are LLMs that (1) reason, (2) act, and (3) interact. | Weaken this direction if the paper already shows an anchor paper already fixes observation access while varying planner quality and the main conclusion still survives. |

### Action-space design or agent competence?
- Program kind: interface normalization
- Lead-set reason: Ranks behind Observability granularity vs planner depth because isolating the shape of the action vocabulary and interface design is slower or harder to defend, but it still stays high because the payoff remains thesis-sized if the control survives.
| Anchor paper | Why read now | What to extract | Current evidence hook | Kill signal |
| --- | --- | --- | --- | --- |
| ReAct: Synergizing Reasoning and Acting in Language Models | Closest agent loop and action spaces anchor with a concrete result hook on ALFWorld/WebShop: ALFWorld/WebShop: 34%/10% success-rate gains over imitation/RL baselines. | Extract the metric and comparator, then check whether how many actions are available, how semantically aligned the actions are, and whether interface cleanup happens together with reasoning changes. | ALFWorld/WebShop: 34%/10% success-rate gains over imitation/RL baselines. | Weaken this direction if the paper already shows the key anchor papers already normalize action vocabularies or API surfaces and still see the same ordering. |
| Tree of Thoughts: Deliberate Problem Solving with Large Language Models | Closest agent loop and action spaces anchor with a concrete result hook on ALFWorld/WebShop: reported setting: 4%/74% success-rate gains in the reported comparison. | Extract the metric and comparator, then check whether how many actions are available, how semantically aligned the actions are, and whether interface cleanup happens together with reasoning changes. | reported setting: 4%/74% success-rate gains in the reported comparison. | Weaken this direction if the paper already shows the key anchor papers already normalize action vocabularies or API surfaces and still see the same ordering. |
| Agentic Large Language Models, a survey | Closest agent loop and action spaces anchor with a concrete result hook on ALFWorld/WebShop: Methods: Agentic LLMs are LLMs that (1) reason, (2) act, and (3) interact. | Extract the metric and comparator, then check whether how many actions are available, how semantically aligned the actions are, and whether interface cleanup happens together with reasoning changes. | Methods: Agentic LLMs are LLMs that (1) reason, (2) act, and (3) interact. | Weaken this direction if the paper already shows the key anchor papers already normalize action vocabularies or API surfaces and still see the same ordering. |

### Search depth or compute budget?
- Program kind: budget-normalized mechanism
- Lead-set reason: Stays in the lead set because it opens a distinct budget-normalized mechanism wedge, but it trails the first two because the literature anchor is still abstract-first and the time-to-clarity is medium.
| Anchor paper | Why read now | What to extract | Current evidence hook | Kill signal |
| --- | --- | --- | --- | --- |
| Tree of Thoughts: Deliberate Problem Solving with Large Language Models | Closest planning and reasoning loops anchor with a concrete result hook on ALFWorld/WebShop: reported setting: 4%/74% success-rate gains in the reported comparison. | Extract the metric and comparator, then check whether the reported depth or branching settings, the effective compute budget, and whether shallow baselines were budget-matched. | reported setting: 4%/74% success-rate gains in the reported comparison. | Weaken this direction if the paper already shows the anchor papers already normalize token or wall-clock budget and the depth advantage remains intact. |
| ReAct: Synergizing Reasoning and Acting in Language Models | Closest planning and reasoning loops anchor with a concrete result hook on ALFWorld/WebShop: ALFWorld/WebShop: 34%/10% success-rate gains over imitation/RL baselines. | Extract the metric and comparator, then check whether the reported depth or branching settings, the effective compute budget, and whether shallow baselines were budget-matched. | ALFWorld/WebShop: 34%/10% success-rate gains over imitation/RL baselines. | Weaken this direction if the paper already shows the anchor papers already normalize token or wall-clock budget and the depth advantage remains intact. |
| Reflexion: Language Agents with Verbal Reinforcement Learning | Closest planning and reasoning loops anchor with a concrete result hook on ALFWorld/WebShop: HumanEval/API: 91% pass@1 vs 80% in the reported comparison. | Extract the metric and comparator, then check whether the reported depth or branching settings, the effective compute budget, and whether shallow baselines were budget-matched. | HumanEval/API: 91% pass@1 vs 80% in the reported comparison. | Weaken this direction if the paper already shows the anchor papers already normalize token or wall-clock budget and the depth advantage remains intact. |
