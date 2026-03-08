from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _rewrite(text: str) -> str:
    rules = [
        (r'(?im)^This subsection\s+', ''),
        (r'(?im)^In this subsection,\s*', ''),
        (r'(?im)^This section\s+', ''),
        (r'(?im)^Two limitations\b', 'A recurring limitation'),
        (r'(?im)^Three limitations\b', 'Several limitations'),
    ]
    out = text
    for pat, repl in rules:
        out = re.sub(pat, repl, out)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--unit-id', default='')
    parser.add_argument('--inputs', default='')
    parser.add_argument('--outputs', default='')
    parser.add_argument('--checkpoint', default='')
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root))
    from tooling.common import atomic_write_text, ensure_dir, now_iso_seconds

    workspace = Path(args.workspace).resolve()
    sections_dir = workspace / 'sections'
    marker = sections_dir / 'style_harmonized.refined.ok'
    ensure_dir(marker.parent)
    for path in sorted(sections_dir.glob('S*.md')):
        if path.name.endswith('_lead.md'):
            continue
        text = path.read_text(encoding='utf-8', errors='ignore') if path.exists() else ''
        if text:
            atomic_write_text(path, _rewrite(text))
    atomic_write_text(marker, f'style harmonized at {now_iso_seconds()}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
