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

    from tooling.review_workflows import summarize_outline, title_tokens, write_text

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

    chosen = pointers[: min(12, len(pointers))]
    scope_bullets = bullets[:3] or [f"Focus on {sections[0]}." if sections else "Focus on the target topic."]
    theme_bullets = bullets[3:9] or bullets[:6] or [f"The literature clusters around {sections[0]}." if sections else "The literature has a small set of recurring themes."]

    lines = [
        "# Research Brief",
        "",
        "## Scope",
    ]
    for idx, bullet in enumerate(scope_bullets, start=1):
        pointer = chosen[(idx - 1) % len(chosen)]
        lines.append(f"- {bullet.rstrip('.')} with concrete anchors in {pointer}.")
    lines.extend(
        [
            "",
            "## Evidence policy",
            f"- This brief uses {len(papers)} papers from `papers/core_set.csv` and stays pointer-heavy rather than narrative-heavy.",
            "",
            "## Taxonomy",
        ]
    )
    for title in sections[:6]:
        lines.append(f"- {title}")

    lines.extend(["", "## Key themes"])
    for idx, bullet in enumerate(theme_bullets[:6], start=1):
        a = chosen[(idx - 1) % len(chosen)]
        b = chosen[idx % len(chosen)] if len(chosen) > 1 else a
        lines.append(f"- {bullet.rstrip('.')} This is easiest to contrast through {a} versus {b}.")

    lines.extend(["", "## What to read first"])
    for pointer in chosen:
        lines.append(f"- {pointer}")

    lines.extend(
        [
            "",
            "## Open problems / risks",
            f"- The current paper set still leaves open questions around {sections[-1] if sections else 'evaluation scope'} and transferability.",
            "- Several themes need stronger benchmark alignment before they can support survey-grade claims.",
        ]
    )

    write_text(workspace / "output" / "SNAPSHOT.md", "\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
