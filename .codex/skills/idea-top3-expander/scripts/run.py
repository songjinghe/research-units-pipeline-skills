from __future__ import annotations

import argparse
import sys
from pathlib import Path


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

    from tooling.common import parse_semicolon_list
    from tooling.ideation import read_jsonl, write_markdown

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ["output/IDEA_TOP3_REPORT.md"]
    out_rel = outputs[0] if outputs else "output/IDEA_TOP3_REPORT.md"
    out_path = workspace / out_rel

    items = [r for r in read_jsonl(workspace / 'output' / 'IDEA_SHORTLIST.jsonl') if isinstance(r, dict)][:3]
    lines = [
        '# IDEA_TOP3_REPORT',
        '',
        '## Executive Summary',
        '',
        '- This report expands the strongest shortlist items into mini-proposals with explicit wedges, confounds, and kill criteria.',
        '',
        '## Cross-Idea Comparison',
        '',
        '| Rank | Idea | Cluster | Why it survives | Main risk | First artifact |',
        '|---|---|---|---|---|---|',
    ]
    for item in items:
        lines.append(
            f"| {item.get('rank')} | {item.get('title')} | {item.get('cluster')} | {item.get('strong_positive_signal')} | {item.get('main_confound')} | {item.get('minimal_artifact')} |"
        )
    lines.append('')
    for item in items:
        lines.extend([
            f"## Top {item.get('rank')}. {item.get('title')}",
            '',
            f"- Cluster: {item.get('cluster')}",
            f"- Idea type: {item.get('idea_type')}",
            f"- Why now: {item.get('why_now')}",
            f"- Sharp gap: {item.get('sharp_gap') or item.get('problem')}",
            f"- Hypothesis: If the proposed intervention isolates the right variable, outcome rankings or failure diagnosis should change in a stable and interpretable way.",
            f"- Concrete testbed: {item.get('concrete_testbed')}",
            f"- Minimal artifact for week 1: {item.get('minimal_artifact')}",
            f"- Strong positive signal: {item.get('strong_positive_signal')}",
            f"- Interesting negative result: {item.get('interesting_negative_result')}",
            f"- Main confound: {item.get('main_confound')}",
            f"- Kill criteria: {item.get('kill_criterion')}",
            f"- Closest prior work: " + ', '.join(f"`{x}`" for x in (item.get('closest_3') or [])),
            f"- Evidence hooks: " + ', '.join(f"`{x}`" for x in (item.get('evidence_anchors') or [])),
            '',
            '### First-week plan',
            '',
            '- Day 1-2: finalize exact task slice and baseline harness.',
            '- Day 3-4: build the minimal artifact and run the first controlled comparison.',
            '- Day 5-7: analyze whether the proposed variable changes conclusions enough to justify a longer project.',
            '',
        ])
    write_markdown(out_path, '\n'.join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
