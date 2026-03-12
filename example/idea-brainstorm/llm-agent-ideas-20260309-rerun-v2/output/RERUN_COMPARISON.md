# RERUN_COMPARISON

- Immediate previous round: `workspaces/idea-brainstorm/llm-agent-ideas-20260309/output/REPORT.md`
- Current rerun: `workspaces/idea-brainstorm/llm-agent-ideas-20260309-rerun/output/REPORT.md`
- Older pre-memo baseline: `workspaces/idea-brainstorm/llm-agent-ideas-20260308/output/IDEA_TOP3_REPORT.md`

## Bottom line

This rerun confirms that the newer, insight-thickened brainstorm pipeline is now **stable** at the level of:
- terminal artifact shape,
- lead-direction ranking,
- discussion-question framing,
- uncertainty handling,
- and appendix structure.

Compared with the immediate previous round (`20260309`), the rerun is mostly a **stability check**, not a radical content shift.

Compared with the older pre-memo baseline (`20260308`), the rerun still represents a large qualitative improvement in both artifact type and discussion value.

## 1) Immediate previous round vs current rerun

### What stayed the same

- The terminal artifact remained `output/REPORT.md` rather than falling back to a top-3 proposal-style report.
- The same top 3 lead directions survived:
  - observability vs planner-depth style question,
  - search-depth planning question,
  - retrieval-policy hidden-variable question.
- The memo kept the same high-level discussion structure:
  - big-picture takeaways,
  - snapshot table,
  - three lead directions,
  - deferred directions,
  - cross-cutting questions,
  - uncertainty,
  - next reading / next discussion steps.
- The added insight-oriented fields survived the rerun:
  - `Why this ranks here`
  - `Closest prior work and why it does not settle the question`
  - `What would count as actual insight`
  - `What would change our mind`

### What changed

The rerun produced only a **minor shortlist variation**:
- one deferred direction changed from a `verification loop`-style candidate
- to a `tool/environment boundary`-style candidate

This suggests the new pipeline is relatively stable on the lead directions while still allowing small movements in the deferred tail.

### Interpretation

This is a good sign.

It means the new pipeline is no longer wildly unstable at the terminal artifact level.
The biggest ideas are not changing arbitrarily from run to run.

## 2) Compared with the pre-memo baseline (`20260308`)

The rerun remains much better than the old `IDEA_TOP3_REPORT.md` along the dimensions that motivated the redesign.

### Better artifact class

Old:
- proposal-like top-3 expansion
- too symmetric
- too close to internal pipeline cards

Current rerun:
- discussion-ready brainstorm memo
- clearer PI/PhD reading path
- trace artifacts clearly separated from the main memo

### Better uncertainty handling

Old:
- uncertainty mostly appeared as repeated per-idea caveat text

Current rerun:
- uncertainty is elevated into an explicit memo section
- the memo reads more honestly and is easier to discuss as an academic artifact

### Better insight framing

Old:
- directions were mostly shaped as “swap protocol / metric / budget assumptions” mini-proposals

Current rerun:
- directions are framed more as explanatory questions:
  - what variable is confounded with what,
  - what current papers fail to isolate,
  - what would count as actual insight,
  - and what would change our mind.

### Better appendix role

Old:
- the main artifact tried to do too much itself

Current rerun:
- the appendix now plays a clearer supporting role
- and at least starts to function as a reading guide rather than only a trace dump

## 3) What improved in this rerun specifically

Relative to the immediate previous round, the biggest gain is not the ranking itself.
It is the **content density inside each lead direction**.

The current rerun now carries stronger intellectual scaffolding through:
- clearer ranking rationale,
- stronger “closest prior work does not settle this” framing,
- explicit statements of what would count as insight,
- and a more explicit “what would change our mind” layer.

That means the memo is now less likely to be read as:
- a list of interesting lenses,

and more likely to be read as:
- a set of candidate explanatory arguments worth serious discussion.

## 4) What still remains weak

Even after the rerun, a few weaknesses remain:

### A) Snapshot table still over-compresses
The table at the top is still too aggressively compressed, so some cells remain visibly clipped.
That means the body now carries more insight than the summary layer.

### B) Evidence is still abstract-first
The memo is now better argued, but the underlying substrate is still abstract-level.
So the memo is stronger as a discussion artifact than as a high-confidence prioritization artifact.

### C) A few direction sections are still more “strongly framed” than “deeply evidenced”
The explanatory framing is noticeably improved, but the paper-level grounding still needs one more step to feel fully earned.

### D) Appendix is better, but not yet a full reading guide
It is now more useful than before, but it still does not fully say:
- what exact passage/result to extract,
- what contradiction to look for,
- or what paper would most strongly falsify the current direction.

## 5) Practical conclusion

This rerun is valuable because it shows two things at once:

1. The new memo-style pipeline is **stable enough to reproduce**.
2. The recent changes did, in fact, thicken the memo’s content rather than only changing surface formatting.

So the current state is:
- better than the previous round,
- much better than the older pre-memo baseline,
- but still one more pass away from a truly strong final brainstorm memo.

## 6) Recommended next move

Do **not** redesign the pipeline again right now.

The pipeline shape is now good enough.
The main remaining work is one more content-focused pass on:
- paper-to-paper tension,
- summary-table clarity,
- appendix reading-guide usefulness,
- and stronger distinction among the top directions.
