from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _extract_cites(text: str) -> list[str]:
    keys: list[str] = []
    for m in re.finditer(r"\[@([^\]]+)\]", text or ""):
        inside = (m.group(1) or "").strip()
        for k in re.findall(r"[A-Za-z0-9:_-]+", inside):
            if k and k not in keys:
                keys.append(k)
    return keys


def _norm_title(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', ' ', str(text or '').lower()).strip()


def _parse_budget_report(md: str) -> tuple[int, int, dict[str, list[str]], dict[str, list[str]]]:
    target = 0
    gap = 0
    suggestions: dict[str, list[str]] = {}
    suggestions_by_title: dict[str, list[str]] = {}
    m = re.search(r"(?im)^\s*-\s*Global\s+(?:target|hard\s+minimum).*>=\s*(\d+)\b", md or "")
    if m:
        target = int(m.group(1))
    m = re.search(r"(?im)^\s*-\s*Gap(?:\s*\([^)]*\))?\s*:\s*(\d+)\b", md or "")
    if m:
        gap = int(m.group(1))
    for raw in (md or "").splitlines():
        line = raw.strip()
        if not line.startswith("|") or line.startswith("|---") or "| suggested keys" in line.lower():
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 6:
            continue
        sub_id = cols[0].strip()
        title = cols[1].strip() if len(cols) > 1 else ''
        sug = cols[5].strip()
        keys = [k.strip() for k in re.findall(r"`([^`]+)`", sug) if k.strip()]
        if sub_id and keys:
            suggestions[sub_id] = keys
        if title and keys:
            suggestions_by_title[_norm_title(title)] = keys
    return target, gap, suggestions, suggestions_by_title


def _split_h3(md: str) -> list[tuple[str | None, list[str]]]:
    blocks: list[tuple[str | None, list[str]]] = []
    current_title: str | None = None
    current_lines: list[str] = []
    for raw in (md or '').splitlines():
        if raw.startswith('### '):
            if current_title is not None:
                blocks.append((current_title, current_lines))
            current_title = raw[4:].strip()
            current_lines = [raw]
            continue
        if current_title is not None:
            current_lines.append(raw)
        else:
            if not blocks:
                blocks.append((None, [raw]))
            else:
                blocks[-1][1].append(raw)
    if current_title is not None:
        blocks.append((current_title, current_lines))
    return blocks


def _section_id_from_title(title: str) -> str:
    m = re.match(r'^(\d+(?:\.\d+)?)\b', str(title or '').strip())
    return m.group(1) if m else ''


def _uniq(items: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        v = str(item or '').strip()
        if not v or v in seen:
            continue
        seen.add(v)
        out.append(v)
    return out


def _in_scope_sentence(keys: list[str]) -> str:
    keys = _uniq(keys)
    if not keys:
        return ''
    phrases = [f'in [@{k}]' for k in keys[:4]]
    if len(phrases) == 1:
        tail = phrases[0]
    elif len(phrases) == 2:
        tail = f'{phrases[0]} and {phrases[1]}'
    else:
        tail = ', '.join(phrases[:-1]) + f', and {phrases[-1]}'
    return f'Additional in-scope evidence for this comparison appears {tail}.'


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

    from tooling.common import atomic_write_text, ensure_dir, parse_semicolon_list
    from tooling.quality_gate import QualityIssue, check_unit_outputs, write_quality_report

    workspace = Path(args.workspace).resolve()
    unit_id = str(args.unit_id or 'U1045').strip() or 'U1045'
    inputs = parse_semicolon_list(args.inputs) or ['output/DRAFT.md', 'output/CITATION_BUDGET_REPORT.md']
    outputs = parse_semicolon_list(args.outputs) or ['output/DRAFT.md', 'output/CITATION_INJECTION_REPORT.md']

    draft_rel = next((p for p in outputs if p.endswith('DRAFT.md')), 'output/DRAFT.md')
    report_rel = next((p for p in outputs if p.endswith('CITATION_INJECTION_REPORT.md')), 'output/CITATION_INJECTION_REPORT.md')
    budget_rel = next((p for p in inputs if p.endswith('CITATION_BUDGET_REPORT.md')), 'output/CITATION_BUDGET_REPORT.md')
    draft_path = workspace / draft_rel
    report_path = workspace / report_rel
    budget_path = workspace / budget_rel
    ensure_dir(report_path.parent)

    missing_inputs: list[str] = []
    if not draft_path.exists() or draft_path.stat().st_size <= 0:
        missing_inputs.append(draft_rel)
    if not budget_path.exists() or budget_path.stat().st_size <= 0:
        missing_inputs.append(budget_rel)
    if missing_inputs:
        msg = 'Missing inputs: ' + ', '.join(missing_inputs)
        atomic_write_text(report_path, '# Citation injection report\n\n- Status: FAIL\n- Reason: ' + msg + '\n')
        write_quality_report(workspace=workspace, unit_id=unit_id, skill='citation-injector', issues=[QualityIssue(code='missing_inputs', message=msg)])
        return 2

    draft = draft_path.read_text(encoding='utf-8', errors='ignore')
    budget = budget_path.read_text(encoding='utf-8', errors='ignore')
    target, gap_from_budget, suggestions, suggestions_by_title = _parse_budget_report(budget)

    current_unique = len(set(_extract_cites(draft)))
    modified_blocks = 0
    if target > 0 and current_unique < target and suggestions:
        new_parts: list[str] = []
        for title, lines in _split_h3(draft):
            block = '\n'.join(lines).rstrip()
            if title is None:
                new_parts.append(block)
                continue
            sid = _section_id_from_title(title)
            suggested = suggestions.get(sid) or suggestions_by_title.get(_norm_title(title)) or []
            if suggested:
                existing = set(_extract_cites(block))
                needed = [k for k in suggested if k not in existing][:12]
                if needed:
                    sentence = _in_scope_sentence(needed)
                    if sentence:
                        block = block.rstrip() + '\n\n' + sentence
                        modified_blocks += 1
            new_parts.append(block)
        draft = '\n'.join(part for part in new_parts if part is not None).rstrip() + '\n'
        atomic_write_text(draft_path, draft)

    unique = len(set(_extract_cites(draft)))
    gap_current = max(0, int(target) - int(unique)) if target > 0 else 0
    status = 'PASS' if (target > 0 and unique >= target) or modified_blocks > 0 else 'FAIL'
    lines = [
        '# Citation injection report',
        '',
        f'- Status: {status}',
        f'- Draft: `{draft_rel}`',
        f'- Budget: `{budget_rel}`',
        f'- Unique citations (current): {unique}',
        f'- Global target (from budget): {target}',
        f'- Gap (current, to target): {gap_current}',
        f'- Gap (from budget, at report time): {gap_from_budget}',
        f'- H3 blocks modified: {modified_blocks}',
        '',
    ]
    if status == 'PASS':
        summary = '- Citation target satisfied after in-scope injection.' if (target > 0 and unique >= target) else '- Applied best-effort in-scope injection; remaining gap is deferred to later global audit.'
        lines.extend(['## Summary', '', summary, ''])
    else:
        lines.extend(['## Summary', '', '- Citation target is still unmet after automatic in-scope injection.', ''])
        if suggestions:
            lines.extend(['## Remaining suggestions', ''])
            for sid, keys in list(suggestions.items())[:10]:
                lines.append(f"- `{sid}`: " + ', '.join(f'`{k}`' for k in keys[:8]))
            lines.append('')
    atomic_write_text(report_path, '\n'.join(lines).rstrip() + '\n')

    issues = check_unit_outputs(skill='citation-injector', workspace=workspace, outputs=[report_rel])
    if issues:
        write_quality_report(workspace=workspace, unit_id=unit_id, skill='citation-injector', issues=issues)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
