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

    from tooling.common import atomic_write_text, ensure_dir, parse_semicolon_list, upsert_checkpoint_block
    from tooling.tutorial_workflows import render_source_tutorial_markdown

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ["output/TUTORIAL.md"]
    out_path = workspace / outputs[0]
    ensure_dir(out_path.parent)

    try:
        text = render_source_tutorial_markdown(workspace)
    except PermissionError:
        decisions_path = workspace / "DECISIONS.md"
        block = "\n".join(
            [
                "## C3 tutorial writing request",
                "",
                "- This unit writes `output/TUTORIAL.md` from the approved module packs.",
                "- Please tick `Approve C2` in `DECISIONS.md`, then rerun this unit.",
                "",
            ]
        )
        upsert_checkpoint_block(decisions_path, "C3", block)
        return 2

    atomic_write_text(out_path, text.rstrip() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
