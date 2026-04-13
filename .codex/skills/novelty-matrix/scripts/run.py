from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _extract_related_works(paper_text: str) -> list[str]:
    lines = (paper_text or "").splitlines()
    in_refs = False
    works: list[str] = []
    for raw in lines:
        line = raw.strip()
        if line.lower().startswith("## references") or line.lower().startswith("# references"):
            in_refs = True
            continue
        if in_refs and line.startswith("## "):
            break
        if in_refs and line.startswith("- "):
            works.append(line[2:].strip())
    return works


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

    from tooling.review_workflows import parse_item_blocks, write_text

    workspace = Path(args.workspace).resolve()
    claims_path = workspace / "output" / "CLAIMS.md"
    paper_path = workspace / "output" / "PAPER.md"
    if not claims_path.exists():
        raise SystemExit("novelty-matrix requires `output/CLAIMS.md`.")

    claims = parse_item_blocks(claims_path.read_text(encoding="utf-8", errors="ignore"))
    paper_text = paper_path.read_text(encoding="utf-8", errors="ignore") if paper_path.exists() else ""
    works = _extract_related_works(paper_text)

    lines = [
        "# Novelty Matrix",
        "",
        "| Claim ID | Claim | Closest related work | Overlap | Delta | Evidence |",
        "|---|---|---|---|---|---|",
    ]
    if not works:
        for claim in claims:
            lines.append(
                f"| {claim.get('id','')} | {claim.get('claim','')} | related works unavailable | unavailable | unavailable | no reference list found in `output/PAPER.md` |"
            )
    else:
        for claim in claims:
            for work in works[:5]:
                lines.append(
                    f"| {claim.get('id','')} | {claim.get('claim','')} | {work} | adjacent problem setting | claimed method delta requires verification | manuscript claim + cited related work |"
                )

    write_text(workspace / "output" / "NOVELTY_MATRIX.md", "\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
