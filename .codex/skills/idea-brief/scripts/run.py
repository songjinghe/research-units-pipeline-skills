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
    outputs = parse_semicolon_list(args.outputs) or ["output/trace/IDEA_BRIEF.md", "queries.md", "DECISIONS.md"]
    brief_rel = next((x for x in outputs if x.endswith("IDEA_BRIEF.md")), "output/trace/IDEA_BRIEF.md")
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
        f"{' '.join(toks)} agent evaluation reliability",
        f"{' '.join(toks)} failure mode limitation",
        f"{' '.join(toks)} adaptation planning memory",
        f"{' '.join(toks)} benchmark risk governance",
    ]
    brief_lines = [
        "# IDEA_BRIEF",
        "",
        "## Goal",
        f"- Topic: {topic}",
        "- Deliverable: `output/REPORT.md` + `output/APPENDIX.md` + `output/REPORT.json`",
        "- Objective: produce a discussion-ready research idea brainstorm memo rather than a project execution spec",
        "",
        "## Scope",
        "- In scope:",
        f"  - research directions directly related to {topic}",
        "  - tensions, missing pieces, and academically meaningful axes suggested by the literature",
        "- Out of scope:",
        "  - full survey drafting",
        "  - rigid project management plans",
        "  - ideas that only work as benchmark-wrapper restatements",
        "",
        "## Audience",
        "- Primary readers: PI / PhD",
        "- Primary use: discussion, prioritization, and next-round reading / deeper thinking",
        "",
        "## Constraints",
        "- Evidence mode: abstract by default unless fulltext is explicitly requested",
        "- Discussion horizon: directions should be strong enough to discuss, not necessarily ready to execute immediately",
        "- Preference: fewer, sharper directions over a large templated pool",
        "- Memo contract: each lead direction must expose a distinct thesis line, an explicit rank basis, a quick kill criterion, and paper-specific reading notes",
        "",
        "## Exclusions",
        "- proprietary telemetry by default",
        "- pure product execution planning",
        "- inspirational future-work dumping without literature anchors",
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
            "- Signal table rows: 10-20",
            "- Direction pool size: 12-24",
            "- Screened directions: 8-12",
            "- Final shortlist size: 5",
            "- Memo lead directions: 3",
            "- Lead-set cluster diversity: >=2",
            "- Lead-set program-kind diversity: >=2",
            "- Reading-guide rows per lead direction: >=3 anchor papers",
            "",
            "## Focus lenses after C2",
            "- Focus clusters: (to be filled after C2 approval)",
            "",
            "## Query Buckets",
        ]
    )
    for idx, q in enumerate(query_buckets, start=1):
        brief_lines.append(f"{idx}. {q}")
    brief_lines.extend(
        [
            "",
            "## Table Policy",
            "- Use tables for signals, screening, and shortlist convergence.",
            "- Reserve prose for the final brainstorm memo and appendix only.",
            "- The appendix must function as a reading guide, not as a generic reminder list.",
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
        '- draft_profile: "idea_brainstorm"',
        '- max_results: "1800"',
        '- core_size: "100"',
        '- direction_pool_min: "12"',
        '- direction_pool_max: "24"',
        '- idea_screen_top_n: "10"',
        '- idea_shortlist_size: "5"',
        '- report_top_n: "3"',
        '- lead_set_cluster_diversity: "2"',
        '- lead_set_program_diversity: "2"',
        '- evidence_mode: "abstract"',
        '- keywords:',
    ]
    for q in query_buckets:
        query_lines.append(f"  - {q}")
    query_lines.extend([
        '- exclude:',
        '  - proprietary telemetry',
        '  - product roadmap',
        '  - inspirational future work',
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
                    "- [ ] Approve C0 (kickoff: topic / constraints / exclusions)",
                    "- [ ] Approve C2 (focus lenses + exclusions)",
                    "",
                ]
            )
            + "\n",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
