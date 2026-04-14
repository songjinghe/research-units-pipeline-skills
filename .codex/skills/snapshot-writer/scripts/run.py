from __future__ import annotations

import argparse
import csv
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

    repo_root = Path(__file__).resolve()
    for _ in range(10):
        if (repo_root / "AGENTS.md").exists():
            break
        parent = repo_root.parent
        if parent == repo_root:
            break
        repo_root = parent
    sys.path.insert(0, str(repo_root))

    from tooling.review_artifacts import summarize_outline, write_text
    from tooling.review_render import render_research_brief_markdown

    workspace = Path(args.workspace).resolve()
    outline_path = workspace / "outline" / "outline.yml"
    core_path = workspace / "papers" / "core_set.csv"
    if not outline_path.exists() or not core_path.exists():
        raise SystemExit("snapshot-writer requires `outline/outline.yml` and `papers/core_set.csv`.")

    sections, bullets = summarize_outline(outline_path)
    with core_path.open("r", encoding="utf-8", newline="") as handle:
        papers = [dict(row) for row in csv.DictReader(handle)]
    if not papers:
        raise SystemExit("`papers/core_set.csv` is empty.")

    pointers = []
    for idx, paper in enumerate(papers, start=1):
        paper_id = str(paper.get("paper_id") or f"P{idx:04d}").strip()
        title = str(paper.get("title") or f"Paper {idx}").strip()
        url = str(paper.get("url") or "").strip()
        pointer = f"{paper_id} - {title}" + (f" ({url})" if url else "")
        pointers.append(pointer)

    text = render_research_brief_markdown(sections=sections, bullets=bullets, pointers=pointers, paper_count=len(papers))
    write_text(workspace / "output" / "SNAPSHOT.md", text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
