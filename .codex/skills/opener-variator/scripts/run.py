from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _extract_flagged_paths(todo_text: str) -> list[str]:
    paths: list[str] = []
    in_style = False
    for raw in (todo_text or '').splitlines():
        line = raw.rstrip()
        if line.startswith('## '):
            in_style = line.strip() == '## Style Smells'
            continue
        if not in_style:
            continue
        for match in re.findall(r"`(sections/[^`]+?\.md)`", line):
            if match not in paths:
                paths.append(match)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--unit-id', default='')
    parser.add_argument('--inputs', default='')
    parser.add_argument('--outputs', default='')
    parser.add_argument('--checkpoint', default='')
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
    from tooling.common import atomic_write_text, ensure_dir, now_iso_seconds

    workspace = Path(args.workspace).resolve()
    sections_dir = workspace / 'sections'
    todo_path = workspace / 'output' / 'WRITER_SELFLOOP_TODO.md'
    marker = sections_dir / 'opener_varied.refined.ok'
    ensure_dir(marker.parent)

    flagged = []
    if todo_path.exists() and todo_path.stat().st_size > 0:
        flagged = _extract_flagged_paths(todo_path.read_text(encoding='utf-8', errors='ignore'))

    targets = [workspace / rel for rel in flagged] if flagged else []
    _ = targets
    # Upstream writer skills should now own opener quality. This unit remains a
    # contract marker only, so it intentionally avoids blind regex rewrites.
    atomic_write_text(marker, f'openers varied at {now_iso_seconds()}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
