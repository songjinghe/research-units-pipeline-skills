from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _count_shortlist(md: str) -> int:
    return len(re.findall(r'(?m)^###\s+Idea\s+\d+\.', md or ''))


def _count_top3(md: str) -> int:
    return len(re.findall(r'(?m)^##\s+Top\s+\d+\.', md or ''))


def _count_pool_rows(md: str) -> int:
    return len([ln for ln in (md or '').splitlines() if ln.strip().startswith('|')]) - 2 if '| Idea ID |' in (md or '') else 0


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

    from tooling.common import atomic_write_text, ensure_dir

    workspace = Path(args.workspace).resolve()
    pool = workspace / 'output' / 'IDEA_POOL.md'
    screening = workspace / 'output' / 'IDEA_SCREENING_TABLE.md'
    shortlist = workspace / 'output' / 'IDEA_SHORTLIST.md'
    top3 = workspace / 'output' / 'IDEA_TOP3_REPORT.md'
    report = workspace / 'output' / 'DELIVERABLE_SELFLOOP_TODO.md'
    ensure_dir(report.parent)

    issues: list[str] = []
    if not pool.exists() or pool.stat().st_size <= 0:
        issues.append('Missing `output/IDEA_POOL.md`.')
    if not screening.exists() or screening.stat().st_size <= 0:
        issues.append('Missing `output/IDEA_SCREENING_TABLE.md`.')
    if not shortlist.exists() or shortlist.stat().st_size <= 0:
        issues.append('Missing `output/IDEA_SHORTLIST.md`.')
    if not top3.exists() or top3.stat().st_size <= 0:
        issues.append('Missing `output/IDEA_TOP3_REPORT.md`.')

    pool_text = pool.read_text(encoding='utf-8', errors='ignore') if pool.exists() else ''
    shortlist_text = shortlist.read_text(encoding='utf-8', errors='ignore') if shortlist.exists() else ''
    top3_text = top3.read_text(encoding='utf-8', errors='ignore') if top3.exists() else ''

    pool_rows = _count_pool_rows(pool_text)
    if pool_text and pool_rows < 60:
        issues.append(f'Idea pool is too small ({pool_rows}; expected >=60).')
    if pool_text and 'Operator' not in pool_text:
        issues.append('Idea pool is missing the operator column.')
    shortlist_n = _count_shortlist(shortlist_text)
    if shortlist_text and not (5 <= shortlist_n <= 7):
        issues.append(f'Shortlist size should be 5-7 (found {shortlist_n}).')
    if shortlist_text and 'Why now:' not in shortlist_text:
        issues.append('Shortlist cards are too thin; missing `Why now` fields.')
    top3_n = _count_top3(top3_text)
    if top3_text and top3_n != 3:
        issues.append(f'Top-3 report should contain exactly 3 expanded ideas (found {top3_n}).')

    status = 'PASS' if not issues else 'FAIL'
    lines = [
        '# Deliverable self-loop',
        '',
        f'- Status: {status}',
        '- Deliverable: ideation stack (`IDEA_POOL` -> `IDEA_SCREENING_TABLE` -> `IDEA_SHORTLIST` -> `IDEA_TOP3_REPORT`)',
        '',
        '## Summary',
        '- The ideation deliverable is evaluated as a layered artifact stack rather than a single shortlist file.',
        '',
        '## Changes made',
        '- Checked pool size, screening table presence, shortlist depth, and top-3 expansion completeness.',
        '',
    ]
    if issues:
        lines.extend(['## Remaining blockers (if FAIL)'])
        lines.extend([f'- {it}' for it in issues])
        lines.extend(['', '## Next step', '- Fix the missing or thin ideation artifacts and rerun this unit.'])
        atomic_write_text(report, '\n'.join(lines).rstrip() + '\n')
        return 2
    lines.extend(['## Remaining blockers (if FAIL)', '- (none)', '', '## Next step', '- Proceed to the next unit.'])
    atomic_write_text(report, '\n'.join(lines).rstrip() + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
