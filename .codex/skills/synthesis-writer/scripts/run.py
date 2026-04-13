from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--unit-id", default="")
    parser.add_argument("--inputs", default="")
    parser.add_argument("--outputs", default="")
    parser.add_argument("--checkpoint", default="")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve()
    for _ in range(10):
        if (repo_root / "AGENTS.md").exists():
            break
        parent = repo_root.parent
        if parent == repo_root:
            break
        repo_root = parent
    sys.path.insert(0, str(repo_root))

    from tooling.review_workflows import read_csv_rows, write_text

    workspace = Path(args.workspace).resolve()
    table_path = workspace / "papers" / "extraction_table.csv"
    rows = read_csv_rows(table_path)
    if not rows:
        raise SystemExit("synthesis-writer requires `papers/extraction_table.csv`.")

    years = [int(row["year"]) for row in rows if str(row.get("year") or "").isdigit()]
    tasks = [str(row.get("task") or "").strip() for row in rows if str(row.get("task") or "").strip()]
    rob_counts = Counter(str(row.get("rob_overall") or "unclear").strip() or "unclear" for row in rows)
    year_span = f"{min(years)}-{max(years)}" if years else "unknown"
    task_summary = ", ".join(sorted(set(tasks))) if tasks else "mixed tasks with sparse deterministic labels"

    lines = [
        "# Evidence Review Synthesis",
        "",
        "## Research questions + scope",
        "- This synthesis follows the current protocol and only reports what the extraction table supports.",
        "",
        "## Included studies summary",
        f"- Included studies: {len(rows)}",
        f"- Year span: {year_span}",
        f"- Task coverage: {task_summary}",
        "",
        "## Findings by theme",
        f"- The current extracted evidence clusters around {task_summary}.",
        "- The deterministic pass keeps findings conservative and avoids claiming effects not present in the table.",
        "",
        "## Risk of bias",
        f"- Overall RoB counts: low={rob_counts.get('low', 0)}, unclear={rob_counts.get('unclear', 0)}, high={rob_counts.get('high', 0)}.",
        "- Protocol detail and confounding control remain the main reasons to keep conclusions bounded.",
        "",
        "## Supported conclusions",
        "- The extracted evidence supports descriptive conclusions about the included study pool and its reported tasks/metrics.",
        "",
        "## Needs more evidence",
        "- Strong comparative or causal claims still need richer extraction fields, stronger protocol detail, or more complete reporting.",
        "",
    ]
    write_text(workspace / "output" / "SYNTHESIS.md", "\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
