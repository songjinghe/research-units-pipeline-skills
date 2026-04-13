from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--approve", default="true")
    parser.add_argument("--unit-id", default="")
    parser.add_argument("--inputs", default="")
    parser.add_argument("--outputs", default="")
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

    from tooling.common import set_decisions_approval

    workspace = Path(args.workspace).resolve()
    checkpoint = str(args.checkpoint or "").strip()
    approved = str(args.approve or "true").strip().lower() not in {"false", "0", "no"}
    set_decisions_approval(workspace / "DECISIONS.md", checkpoint, approved=approved)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
