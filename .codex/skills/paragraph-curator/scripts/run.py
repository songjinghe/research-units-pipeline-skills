from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _sans_citations(text: str) -> str:
    return re.sub(r"\[@[^\]]+\]", "", text or "")




def _sentence_count(text: str) -> int:
    return len([s for s in re.split(r'(?<=[.!?])\s+', (text or '').strip()) if s.strip()])


def _merge_short_body_paragraphs(paragraphs: list[str], *, min_chars: int = 260, min_sentences: int = 3) -> list[str]:
    if len(paragraphs) <= 2:
        return paragraphs

    lead = paragraphs[:1]
    tail = paragraphs[1:]
    merged: list[str] = []
    pending = ''
    for para in tail:
        clean = para.strip()
        if not clean:
            continue
        pending = clean if not pending else (pending.rstrip() + ' ' + clean)
        if len(_sans_citations(pending)) >= int(min_chars) or _sentence_count(pending) >= int(min_sentences):
            merged.append(pending.strip())
            pending = ''
    if pending:
        if merged:
            merged[-1] = merged[-1].rstrip() + ' ' + pending.strip()
        else:
            merged.append(pending.strip())
    return lead + merged

def _curate(text: str, *, max_paragraphs: int = 14, tail_keep: int = 3, min_chars: int = 5200) -> str:
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text.strip()) if p.strip()]
    paragraphs = _merge_short_body_paragraphs(paragraphs)
    if len(paragraphs) <= max_paragraphs:
        return '\n\n'.join(paragraphs).rstrip() + ('\n' if paragraphs else '')

    tail_keep = max(0, min(int(tail_keep), max(0, len(paragraphs) - 1)))
    head_keep = max(1, int(max_paragraphs) - tail_keep)

    kept = paragraphs[:head_keep]
    tail = paragraphs[-tail_keep:] if tail_keep else []

    # Preserve the closing synthesis/conclusion paragraphs instead of truncating them away.
    curated = kept + tail

    middle_idx = head_keep
    middle_stop = max(head_keep, len(paragraphs) - tail_keep)
    while middle_idx < middle_stop and len(_sans_citations('\n\n'.join(curated))) < int(min_chars):
        curated.insert(len(curated) - tail_keep if tail_keep else len(curated), paragraphs[middle_idx])
        middle_idx += 1

    return '\n\n'.join(curated).rstrip() + '\n'


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
