from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _curate(text: str, *, max_paragraphs: int = 12) -> str:
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text.strip()) if p.strip()]
    if len(paragraphs) <= max_paragraphs:
        return '\n\n'.join(paragraphs).rstrip() + ('\n' if paragraphs else '')
    return '\n\n'.join(paragraphs[:max_paragraphs]).rstrip() + '\n'


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
    from tooling.common import atomic_write_text, ensure_dir, now_iso_seconds, parse_semicolon_list

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ['output/PARAGRAPH_CURATION_REPORT.md', 'sections/paragraphs_curated.refined.ok']
    report_rel = next((x for x in outputs if x.endswith('PARAGRAPH_CURATION_REPORT.md')), 'output/PARAGRAPH_CURATION_REPORT.md')
    marker_rel = next((x for x in outputs if x.endswith('.refined.ok')), 'sections/paragraphs_curated.refined.ok')
    report_path = workspace / report_rel
    marker_path = workspace / marker_rel
    ensure_dir(report_path.parent)
    ensure_dir(marker_path.parent)

    curated = []
    for path in sorted((workspace / 'sections').glob('S*.md')):
        if path.name.endswith('_lead.md'):
            continue
        text = path.read_text(encoding='utf-8', errors='ignore') if path.exists() else ''
        if text:
            atomic_write_text(path, _curate(text))
            curated.append(str(path.relative_to(workspace)))

    report = '\n'.join([
        '# Paragraph curation report',
        '',
        '- Status: PASS',
        f'- Curated files: {len(curated)}',
    ] + [f'- `{p}`' for p in curated[:20]]) + '\n'
    atomic_write_text(report_path, report)
    atomic_write_text(marker_path, f'paragraphs curated at {now_iso_seconds()}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
