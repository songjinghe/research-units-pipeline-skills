from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _topic_tokens(topic: str) -> list[str]:
    toks = [t for t in re.findall(r"[A-Za-z0-9]+", str(topic or "")) if t]
    return toks[:6] if toks else ["research", "ideas"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--unit-id", default="")
    parser.add_argument("--inputs", default="")
    parser.add_argument("--outputs", default="")
    parser.add_argument("--checkpoint", default="")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root))

    from tooling.common import atomic_write_text, ensure_dir, parse_semicolon_list
    from tooling.ideation import DEFAULT_IDEA_RUBRIC, extract_goal_from_goal_md

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ["output/IDEA_BRIEF.md", "queries.md", "DECISIONS.md"]
    brief_rel = next((x for x in outputs if x.endswith("IDEA_BRIEF.md")), "output/IDEA_BRIEF.md")
    queries_rel = next((x for x in outputs if x.endswith("queries.md")), "queries.md")
    decisions_rel = next((x for x in outputs if x.endswith("DECISIONS.md")), "DECISIONS.md")

    brief_path = workspace / brief_rel
    queries_path = workspace / queries_rel
    decisions_path = workspace / decisions_rel
    ensure_dir(brief_path.parent)
    ensure_dir(queries_path.parent)
    ensure_dir(decisions_path.parent)

    topic = extract_goal_from_goal_md(workspace / "GOAL.md")
    toks = _topic_tokens(topic)
    query_buckets = [
        f"{' '.join(toks)} evaluation reliability benchmark",
        f"{' '.join(toks)} failure mode protocol",
        f"{' '.join(toks)} safety governance auditability",
        f"{' '.join(toks)} system constraints latency cost permissions",
    ]
    brief_lines = [
        "# IDEA_BRIEF",
        "",
        "## Goal",
        f"- Topic: {topic}",
        "- Deliverable: `output/IDEA_SHORTLIST.md` + `output/IDEA_TOP3_REPORT.md`",
        "- Objective: produce a small set of feasible, evidence-anchored research ideas rather than a full survey draft",
        "",
        "## Scope",
        "- In scope:",
        f"  - research ideas directly related to {topic}",
        "  - evaluation, failure modes, interventions, and system constraints that can be tested with modest resources",
        "- Out of scope:",
        "  - ideas requiring proprietary telemetry by default",
        "  - open-ended platform building without a bounded first experiment",
        "",
        "## Constraints",
        "- Timebox: 1 week for the first smoke-test experiment",
        "- Team size: 1-2 people",
        "- Compute: modest",
        "- Evidence mode: abstract by default unless fulltext is explicitly requested",
        "",
        "## Rubric",
        "| criterion | weight | note |",
        "|---|---:|---|",
    ]
    for name, weight, note in DEFAULT_IDEA_RUBRIC:
        brief_lines.append(f"| {name} | {weight:.2f} | {note} |")
    brief_lines.extend(
        [
            "",
            "## Targets",
            "- Candidate retrieval pool: >=800",
            "- Core set size: 100",
            "- Opportunity rows: >=16",
            "- Idea pool size: 60-80",
            "- Screened candidates: 12-18",
            "- Final shortlist size: 5-7",
            "- Top-3 report size: 3",
            "",
            "## Query Buckets",
        ]
    )
    for idx, q in enumerate(query_buckets, start=1):
        brief_lines.append(f"{idx}. {q}")
    brief_lines.extend(
        [
            "",
            "## Exclusions",
            "- robotics",
            "- purely inspirational future-work lists",
            "- hidden enterprise telemetry",
            "",
            "## Table Policy",
            "- Use tables for opportunity mapping, screening, and cross-idea comparison.",
            "- Use cards only for the final shortlist and top-3 expansion.",
            "",
            "## Open Questions",
            "- None by default; refine interactively when the user provides extra constraints.",
            "",
        ]
    )
    atomic_write_text(brief_path, "\n".join(brief_lines).rstrip() + "\n")

    query_lines = [
        "# queries",
        "",
        '- draft_profile: "idea_finder"',
        '- max_results: "1800"',
        '- core_size: "100"',
        '- idea_pool_min: "60"',
        '- idea_pool_max: "80"',
        '- idea_screen_top_n: "15"',
        '- idea_shortlist_size: "7"',
        '- idea_top3_size: "3"',
        '- evidence_mode: "abstract"',
        '- keywords:',
    ]
    for q in query_buckets:
        query_lines.append(f"  - {q}")
    query_lines.extend([
        '- exclude:',
        '  - robotics',
        '  - embodied navigation',
        '  - proprietary telemetry',
        '  - react hooks',
        '',
    ])
    atomic_write_text(queries_path, "\n".join(query_lines).rstrip() + "\n")

    if not decisions_path.exists() or decisions_path.stat().st_size == 0:
        atomic_write_text(
            decisions_path,
            "\n".join(
                [
                    "# Decisions log",
                    "",
                    "## Approvals (check to unblock)",
                    "- [ ] Approve C0 (kickoff: scope/sources/time window/constraints)",
                    "- [ ] Approve C2 (focus clusters + exclusions)",
                    "",
                ]
            )
            + "\n",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
