# Research Idea Brainstorm Memo

## 0. Scope and framing

- Topic: Reliable LLM agent evaluation ideas
- Intended readers: PI / PhD
- Goal: surface a small number of discussion-worthy research directions rather than force a final project choice.
- Current evidence basis: abstract-first notes unless otherwise stated.
- What this memo is not: not a final project spec, not a survey draft, and not a symmetric top-3 proposal pack.

## 1. Big-picture takeaways

- The strongest directions are the ones most likely to change how existing results are interpreted, not just add another benchmark win.
- The current rank order reflects a tradeoff between time-to-clarity, thesis-sized payoff, and how concrete the nearest prior-work gap already looks.
- The lead set is intentionally not one confound template repeated three times: it spans causal attribution, interface normalization, budget-normalized mechanism rather than a single explanatory mold.
- Most anchors are still abstract-first, so the memo is best used to decide the next reading and falsification pass rather than to lock a project immediately.

## 2. Top directions at a glance

| Rank | Direction | Why now | If it survives | Fast kill signal |
| --- | --- | --- | --- | --- |
| 1 | Observability granularity vs planner depth | Leads because it offers the fastest path to a decisive causal attribution result in agent lo | Could yield a causal-attribution result plus a reporting rule for agent-loop papers: claims abou | Kill quickly if an anchor paper already fixes observation access while varying planner quality |
| 2 | Action-space design or agent competence? | Ranks behind Observability granularity vs planner depth because isolating the shape of the a | Could produce an action-space normalization protocol and a clearer account of which agent claims | Kill quickly if the key anchor papers already normalize action vocabularies or API surfaces an |
| 3 | Search depth or compute budget? | Stays in the lead set because it opens a distinct budget-normalized mechanism wedge, but it | Could produce a compute-normalized planning benchmark slice and a regime map for when search dep | Kill quickly if the anchor papers already normalize token or wall-clock budget and the depth a |

## 3. Direction 1 — Observability granularity vs planner depth

### One-line thesis
- Several agent-loop gains remain hard to interpret because papers often improve observation access at the same time they improve the planner; before crediting planner depth, we should ask what the system was allowed to see.

### Why it belongs in the lead set
- Leads because it offers the fastest path to a decisive causal attribution result in agent loop and action spaces, and because it has the clearest path to a thesis-sized contribution if the control holds.
- Time to clarity: fast

### What the current literature actually shows
- ReAct: Synergizing Reasoning and Acting in Language Models: ALFWorld/WebShop: 34%/10% success-rate gains over imitation/RL baselines. Open gap: observability granularity still moves with planner quality and broader agent competence.
- Tree of Thoughts: Deliberate Problem Solving with Large Language Models: reported setting: 4%/74% success-rate gains in the reported comparison. Open gap: observability granularity still moves with planner quality and broader agent competence.
- Across the anchor papers, the live question is whether observability granularity changes interpretation itself or merely rides along with planner quality and broader agent competence, especially on ALFWorld/WebShop.

### Closest prior work and remaining gap
- ReAct: Synergizing Reasoning and Acting in Language Models is the closest prior anchor because it already reports concrete behavior on ALFWorld/WebShop.
- The novelty test here is narrow, not rhetorical: if a strong anchor paper already runs that single-variable control, this direction should collapse quickly rather than stay alive as a vague confound story.
- Missing piece: What is missing is a fixed-interface, fixed-budget comparison that varies only observation access and tracks whether the failure taxonomy—not just average score—changes.

### If this direction is right, what contribution emerges
- Could yield a causal-attribution result plus a reporting rule for agent-loop papers: claims about planning quality should specify and control observation access.
- A convincing result would not just move aggregate score.

### Smallest decisive probe
- Intervention: vary observability granularity while holding planner quality and broader agent competence as fixed as possible on ALFWorld/WebShop.
- Prior-work audit: inspect ReAct: Synergizing Reasoning and Acting in Language Models for any ablation that already fixes planner quality and broader agent competence, and if the conclusion survives, demote this direction

### Quick kill criteria
- Kill quickly if an anchor paper already fixes observation access while varying planner quality and the main conclusion still survives.
- Kill if the first controlled probe leaves both the reported benchmark metric plus failure-type shifts and the failure taxonomy essentially unchanged.

## 4. Direction 2 — Action-space design or agent competence?

### One-line thesis
- Some agent-loop gains may be interface gains in disguise: when action vocabularies become cleaner or narrower, papers can attribute robustness to reasoning improvements that partly come from action-space design.

### Why it belongs in the lead set
- Ranks behind Observability granularity vs planner depth because isolating the shape of the action vocabulary and interface design is slower or harder to defend, but it still stays high because the payoff remains thesis-sized if the control survives.
- Time to clarity: medium

### What the current literature actually shows
- ReAct: Synergizing Reasoning and Acting in Language Models: ALFWorld/WebShop: 34%/10% success-rate gains over imitation/RL baselines. Open gap: action-space design still moves with the shape of the action vocabulary and interface design.
- Tree of Thoughts: Deliberate Problem Solving with Large Language Models: reported setting: 4%/74% success-rate gains in the reported comparison. Open gap: action-space design still moves with the shape of the action vocabulary and interface design.
- Across the anchor papers, the live question is whether action-space design changes interpretation itself or merely rides along with the shape of the action vocabulary and interface design, especially on ALFWorld/WebShop.

### Closest prior work and remaining gap
- ReAct: Synergizing Reasoning and Acting in Language Models is the closest prior anchor because it already reports concrete behavior on ALFWorld/WebShop.
- The novelty test here is narrow, not rhetorical: if a strong anchor paper already runs that single-variable control, this direction should collapse quickly rather than stay alive as a vague confound story.
- Missing piece: What is missing is an action-space-normalized comparison that keeps planner prompts fixed while changing only interface granularity and affordances.

### If this direction is right, what contribution emerges
- Could produce an action-space normalization protocol and a clearer account of which agent claims survive once interface ergonomics are controlled.
- A useful result would show whether the same nominal planner still behaves very differently once the action space is widened, normalized, or made less ergonomic.

### Smallest decisive probe
- Intervention: vary action-space design while holding the shape of the action vocabulary and interface design as fixed as possible on ALFWorld/WebShop.
- Prior-work audit: inspect ReAct: Synergizing Reasoning and Acting in Language Models for any ablation that already fixes the shape of the action vocabulary and interface design, and if the conclusion survives, demote thi

### Quick kill criteria
- Kill quickly if the key anchor papers already normalize action vocabularies or API surfaces and still see the same ordering.
- Kill if the first controlled probe leaves both the reported benchmark metric plus failure-type shifts and the failure taxonomy essentially unchanged.

## 5. Direction 3 — Search depth or compute budget?

### One-line thesis
- Many planning results still bundle depth with budget: deeper search often spends more tokens, branches, or retries, so it remains unclear whether depth changes reasoning quality or just buys more recovery opportunities.

### Why it belongs in the lead set
- Stays in the lead set because it opens a distinct budget-normalized mechanism wedge, but it trails the first two because the literature anchor is still abstract-first and the time-to-clarity is medium.
- Time to clarity: medium

### What the current literature actually shows
- Tree of Thoughts: Deliberate Problem Solving with Large Language Models: reported setting: 4%/74% success-rate gains in the reported comparison. Open gap: search depth still moves with inference-time compute budget.
- ReAct: Synergizing Reasoning and Acting in Language Models: ALFWorld/WebShop: 34%/10% success-rate gains over imitation/RL baselines. Open gap: search depth still moves with inference-time compute budget.
- Across the anchor papers, the live question is whether search depth changes interpretation itself or merely rides along with inference-time compute budget, especially on ALFWorld/WebShop.

### Closest prior work and remaining gap
- Tree of Thoughts: Deliberate Problem Solving with Large Language Models is the closest prior anchor because it already reports concrete behavior on a small public task slice.
- The novelty test here is narrow, not rhetorical: if a strong anchor paper already runs that single-variable control, this direction should collapse quickly rather than stay alive as a vague confound story.
- Missing piece: What is missing is a compute-normalized study that holds token or wall-clock budget fixed while varying depth or branching, then checks whether failure modes actually change.

### If this direction is right, what contribution emerges
- Could produce a compute-normalized planning benchmark slice and a regime map for when search depth matters beyond extra inference budget.
- A convincing result would show whether depth changes the nature of planning failures under a matched budget, rather than merely delaying failure by spending more compute.

### Smallest decisive probe
- Intervention: vary search depth while holding inference-time compute budget as fixed as possible on ALFWorld/WebShop. Readout: pass@1 plus failure-type shifts.
- Prior-work audit: inspect Tree of Thoughts: Deliberate Problem Solving with Large Language Models for any ablation that already fixes inference-time compute budget, and if the conclusion survives, demote this direction.

### Quick kill criteria
- Kill quickly if the anchor papers already normalize token or wall-clock budget and the depth advantage remains intact.
- Kill if the first controlled probe leaves both pass@1 plus failure-type shifts and the failure taxonomy essentially unchanged.

## 6. Other promising but not prioritized directions

- **Verification or just expensive redundancy?** — Verification-heavy pipelines may look stronger because they retry, re-check, or filter more often, not necessarily because they add a distinct reasoning mechanism. (why not prioritized now: sits in a cluster already represented in the lead set, while its first decisive control currently looks slower.)
- **Retrieval policy or memory content?** — Reported memory gains are often hard to interpret because memory content and retrieval triggers move together; (why not prioritized now: is still promising, but the literature anchor is too abstract-first for lead-set rank right now.)

## 7. Cross-cutting discussion questions

- Which direction still survives once we ask for a single-variable control rather than a suggestive confound story?
- Which lead direction would still matter if the nearest prior work already addressed the obvious control we are worried about?
- Which candidate could plausibly turn into a thesis line with a reusable method, protocol, or regime map rather than a one-off empirical note?
- Which ranking would change most after one full-paper reading pass on the anchor set?

## 8. Uncertainty and disagreement

- The main remaining risk is novelty risk, not idea scarcity: closer reading may reveal that one lead direction is already settled by an existing control or ablation.
- Evidence confidence is still bounded by abstract-first notes for part of the lead set, so paper-specific details could either strengthen or kill a direction quickly.
- The memo is more reliable as a discussion and triage artifact than as a final commitment on exact project order.

## 9. Suggested next reading / next discussion step

- Start with Observability granularity vs planner depth: read ReAct: Synergizing Reasoning and Acting in Language Models looking specifically for whether observability granularity is already isolated against planner quality and broader agent competence.
- Intervention: vary observability granularity while holding planner quality and broader agent competence as fixed as possible on ALFWorld/WebShop.
- Re-rank only after checking the quick kill criteria for Observability granularity vs planner depth and at least one competing direction in the lead set.

## 10. Appendix guide

- `output/APPENDIX.md` for anchor-paper reading notes and deferred directions.
- `output/REPORT.json` for the structured version of this memo.
