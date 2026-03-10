from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _count_shortlist(md: str) -> int:
    return len(re.findall(r'(?m)^###\s+Direction\s+\d+\.', md or ''))


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
    signal_table = workspace / 'output' / 'trace' / 'IDEA_SIGNAL_TABLE.md'
    pool = workspace / 'output' / 'trace' / 'IDEA_DIRECTION_POOL.md'
    screening = workspace / 'output' / 'trace' / 'IDEA_SCREENING_TABLE.md'
    shortlist = workspace / 'output' / 'trace' / 'IDEA_SHORTLIST.md'
    report_md = workspace / 'output' / 'REPORT.md'
    appendix = workspace / 'output' / 'APPENDIX.md'
    report_json = workspace / 'output' / 'REPORT.json'
    report = workspace / 'output' / 'DELIVERABLE_SELFLOOP_TODO.md'
    ensure_dir(report.parent)

    issues: list[str] = []
    for path in [signal_table, pool, screening, shortlist, report_md, appendix, report_json]:
        if not path.exists() or path.stat().st_size <= 0:
            issues.append(f'Missing `{path.relative_to(workspace)}`.')

    shortlist_text = shortlist.read_text(encoding='utf-8', errors='ignore') if shortlist.exists() else ''
    report_text = report_md.read_text(encoding='utf-8', errors='ignore') if report_md.exists() else ''
    appendix_text = appendix.read_text(encoding='utf-8', errors='ignore') if appendix.exists() else ''

    shortlist_n = _count_shortlist(shortlist_text)
    if shortlist_text and not (3 <= shortlist_n <= 5):
        issues.append(f'Shortlist size should be 3-5 (found {shortlist_n}).')

    required_sections = [
        '## 1. Big-picture takeaways',
        '## 2. Top directions at a glance',
        '## 6. Other promising but not prioritized directions',
        '## 7. Cross-cutting discussion questions',
        '## 8. Uncertainty and disagreement',
    ]
    for section in required_sections:
        if report_text and section not in report_text:
            issues.append(f'`output/REPORT.md` is missing `{section}`.')
    if report_text and '## 3. Direction 1' not in report_text:
        issues.append('`output/REPORT.md` should expand the top directions into memo sections.')
    if appendix_text and not all(token in appendix_text for token in ['Anchor paper', 'Why read now', 'What to extract', 'Kill signal']):
        issues.append('`output/APPENDIX.md` should expose paper-specific reading-guide tables.')
    for phrase in ['reports a meaningful gain', 'Sharper mechanism question;', 'read it to extract what it really attributes gains to']:
        if phrase in report_text or phrase in appendix_text:
            issues.append(f'Found templated memo language: `{phrase}`.')

    status = 'PASS' if not issues else 'FAIL'
    lines = [
        '# Deliverable self-loop',
        '',
        f'- Status: {status}',
        '- Deliverable: brainstorm memo bundle (`IDEA_SIGNAL_TABLE` -> `IDEA_DIRECTION_POOL` -> `IDEA_SCREENING_TABLE` -> `IDEA_SHORTLIST` -> `REPORT`)',
        '',
        '## Summary',
        '- The ideation deliverable is evaluated as a memo bundle with a supporting trace chain, not as a symmetric top-3 proposal pack.',
        '',
        '## Changes made',
        '- Checked trace presence, shortlist size, and core memo sections for the final `REPORT.md` deliverable.',
        '',
    ]
    if issues:
        lines.extend(['## Remaining blockers (if FAIL)'])
        lines.extend([f'- {it}' for it in issues])
        lines.extend(['', '## Next step', '- Fix the missing or thin memo artifacts and rerun this unit.'])
        atomic_write_text(report, '\n'.join(lines).rstrip() + '\n')
        return 2
    lines.extend(['## Remaining blockers (if FAIL)', '- (none)', '', '## Next step', '- Proceed to the next unit.'])
    atomic_write_text(report, '\n'.join(lines).rstrip() + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
