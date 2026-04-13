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
    gaps_path = workspace / "output" / "MISSING_EVIDENCE.md"
    matrix_path = workspace / "output" / "NOVELTY_MATRIX.md"
    if not claims_path.exists() or not gaps_path.exists():
        raise SystemExit("rubric-writer requires `output/CLAIMS.md` and `output/MISSING_EVIDENCE.md`.")

    claims = parse_item_blocks(claims_path.read_text(encoding="utf-8", errors="ignore"))
    gaps = parse_item_blocks(gaps_path.read_text(encoding="utf-8", errors="ignore"))
    major = [gap for gap in gaps if str(gap.get("severity") or "").strip().lower() == "major"]
    novelty_note = "Novelty was assessed conservatively from the available novelty matrix." if matrix_path.exists() else "Novelty matrix was unavailable; novelty is therefore conservative."
    recommendation = "weak_reject" if major else ("borderline" if gaps else "weak_accept")

    lines = [
        "# Review",
        "",
        "### Summary",
        f"- The paper claims {len(claims)} main contribution(s) and is reviewed through explicit claim and gap extraction.",
        "",
        "### Novelty",
        f"- {novelty_note}",
        "",
        "### Soundness",
        f"- The review surfaced {len(major)} major and {max(0, len(gaps) - len(major))} minor evidence issues.",
        "",
        "### Clarity",
        "- The main clarity risk is whether each top claim states its protocol, metric, and boundary explicitly.",
        "",
        "### Impact",
        "- If the major issues are fixed, the work could become easier to compare and reproduce.",
        "",
        "### Major Concerns",
    ]
    if major:
        for gap in major:
            lines.extend(
                [
                    f"- Problem: {gap.get('gap___concern', gap.get('gap_concern', gap.get('gap','')))}",
                    "- Why it matters: the current evidence chain is not strong enough for a confident acceptance decision.",
                    f"- Minimal fix: {gap.get('minimal_fix', '')}",
                ]
            )
    else:
        lines.append("- (none)")

    lines.extend(["", "### Minor Comments"])
    for gap in gaps[:3]:
        lines.append(f"- {gap.get('minimal_fix', gap.get('gap___concern', 'Clarify the supporting evidence.'))}")
    if not gaps:
        lines.append("- (none)")

    lines.extend(
        [
            "",
            "### Recommendation",
            f"- {recommendation}",
        ]
    )

    write_text(workspace / "output" / "REVIEW.md", "\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
