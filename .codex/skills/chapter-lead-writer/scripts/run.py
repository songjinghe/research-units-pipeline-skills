from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not path.exists() or path.stat().st_size <= 0:
        return out
    import json

    for raw in path.read_text(encoding='utf-8', errors='ignore').splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = json.loads(raw)
        except Exception:
            continue
        if isinstance(rec, dict):
            out.append(rec)
    return out


def _load_json_asset(path: Path) -> dict[str, Any]:
    if not path.exists() or path.stat().st_size <= 0:
        return {}
    try:
        data = json.loads(path.read_text(encoding='utf-8', errors='ignore'))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


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


def _cite(keys: list[str], n: int = 3) -> str:
    return ' '.join(f'[@{k}]' for k in _uniq(keys)[:n])


def _clean_phrase(text: str) -> str:
    s = str(text or '').strip().replace('/', ' and ')
    s = ' '.join(s.split())
    return s.rstrip(' .;:，；。')


def _skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _compatibility_defaults() -> dict[str, Any]:
    asset_path = _skill_root() / 'assets' / 'lead_block_compatibility_defaults.json'
    data = _load_json_asset(asset_path)
    defaults: dict[str, Any] = {
        'default_archetype': 'lens-first',
        'limits': {
            'throughline_items': 2,
            'contrast_items': 3,
            'subsection_preview_items': 3,
        },
        'joiners': {
            'throughline': '; ',
            'contrasts': ', ',
            'subsection_preview': ', ',
        },
        'fallbacks': {
            'section_title': 'chapter {section_id}',
            'comparison_problem': 'adjacent subsections resolving the same system tension',
            'recurring_contrasts': 'protocol assumptions, resource constraints, and evaluation scope',
            'subsection_preview': 'the chapter subsections',
        },
        'templates': {
            'lens-first': {
                'paragraph_1': 'What holds {section_title} together is a shared comparison problem: {comparison_problem}{citation}.',
                'paragraph_2': 'Across {subsection_preview}, the recurring contrasts are {recurring_contrasts}, so each subsection sharpens a different part of the same argument{citation}.',
                'paragraph_3': 'That progression moves from {lead_start} toward {lead_end}, keeping the chapter comparative without collapsing distinct design choices into a single architecture label{citation}.',
            }
        },
    }

    if not data:
        return defaults

    merged = dict(defaults)
    for key in ['limits', 'joiners', 'fallbacks', 'templates']:
        base = defaults.get(key) or {}
        override = data.get(key) or {}
        if isinstance(base, dict) and isinstance(override, dict):
            merged[key] = dict(base) | dict(override)
        else:
            merged[key] = override or base
    merged['default_archetype'] = str(data.get('default_archetype') or defaults['default_archetype']).strip() or defaults['default_archetype']
    return merged


def _limit(value: Any, *, fallback: int) -> int:
    try:
        num = int(value)
    except Exception:
        return fallback
    return num if num > 0 else fallback


def _join_nonempty(items: list[str], *, sep: str, limit: int, fallback: str) -> str:
    vals = [str(item).strip() for item in items if str(item).strip()]
    joined = sep.join(vals[:limit]).strip()
    return joined or fallback


def _citation_suffix(keys: list[str], n: int = 3) -> str:
    cite = _cite(keys, n)
    return f' {cite}' if cite else ''


def _render(template: str, **kwargs: str) -> str:
    text = template.format(**kwargs)
    text = ' '.join(text.split())
    text = text.replace(' .', '.').replace(' ,', ',').replace(' ;', ';').replace(' :', ':')
    return text


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

    from tooling.common import atomic_write_text, ensure_dir, load_yaml, now_iso_seconds
    from tooling.pipeline_text import slug_unit_id

    workspace = Path(args.workspace).resolve()
    compat = _compatibility_defaults()
    limits = compat.get('limits') if isinstance(compat.get('limits'), dict) else {}
    joiners = compat.get('joiners') if isinstance(compat.get('joiners'), dict) else {}
    fallbacks = compat.get('fallbacks') if isinstance(compat.get('fallbacks'), dict) else {}
    templates = compat.get('templates') if isinstance(compat.get('templates'), dict) else {}
    archetype = str(compat.get('default_archetype') or 'lens-first').strip() or 'lens-first'
    template_pack = templates.get(archetype) if isinstance(templates.get(archetype), dict) else {}
    sections_dir = workspace / 'sections'
    ensure_dir(sections_dir)
    report_path = workspace / 'output' / 'CHAPTER_LEADS_REPORT.md'
    ensure_dir(report_path.parent)

    outline = load_yaml(workspace / 'outline' / 'outline.yml') if (workspace / 'outline' / 'outline.yml').exists() else []
    briefs = {str(r.get('section_id') or '').strip(): r for r in _load_jsonl(workspace / 'outline' / 'chapter_briefs.jsonl') if str(r.get('section_id') or '').strip()}
    packs = _load_jsonl(workspace / 'outline' / 'writer_context_packs.jsonl')
    cites_by_sec: dict[str, list[str]] = {}
    for rec in packs:
        sec_id = str(rec.get('section_id') or '').strip()
        if not sec_id:
            continue
        bucket = cites_by_sec.setdefault(sec_id, [])
        for field in ['allowed_bibkeys_selected', 'allowed_bibkeys_chapter']:
            for key in rec.get(field) or []:
                bucket.append(str(key).strip())

    written: list[str] = []
    if isinstance(outline, list):
        for sec in outline:
            if not isinstance(sec, dict):
                continue
            subs = [x for x in (sec.get('subsections') or []) if isinstance(x, dict)]
            if not subs:
                continue
            sec_id = str(sec.get('id') or '').strip()
            sec_title = str(sec.get('title') or '').strip() or str(fallbacks.get('section_title') or 'chapter {section_id}').format(section_id=sec_id)
            if not sec_id:
                continue
            brief = briefs.get(sec_id) or {}
            throughline = [_clean_phrase(x) for x in (brief.get('throughline') or []) if _clean_phrase(x)]
            contrasts = [_clean_phrase(x) for x in (brief.get('key_contrasts') or []) if _clean_phrase(x)]
            lead_plan = [_clean_phrase(x) for x in (brief.get('lead_paragraph_plan') or []) if _clean_phrase(x)]
            sub_titles = [str(x.get('title') or '').strip() for x in subs if str(x.get('title') or '').strip()]
            cites = cites_by_sec.get(sec_id) or []
            comparison_problem = _join_nonempty(
                throughline,
                sep=str(joiners.get('throughline') or '; '),
                limit=_limit(limits.get('throughline_items'), fallback=2),
                fallback=str(fallbacks.get('comparison_problem') or 'adjacent subsections resolving the same system tension'),
            )
            recurring_contrasts = _join_nonempty(
                contrasts,
                sep=str(joiners.get('contrasts') or ', '),
                limit=_limit(limits.get('contrast_items'), fallback=3),
                fallback=str(fallbacks.get('recurring_contrasts') or 'protocol assumptions, resource constraints, and evaluation scope'),
            )
            subsection_preview = _join_nonempty(
                sub_titles,
                sep=str(joiners.get('subsection_preview') or ', '),
                limit=_limit(limits.get('subsection_preview_items'), fallback=3),
                fallback=str(fallbacks.get('subsection_preview') or 'the chapter subsections'),
            )
            paragraphs = [
                _render(
                    str(template_pack.get('paragraph_1') or 'What holds {section_title} together is a shared comparison problem: {comparison_problem}{citation}.'),
                    section_title=sec_title,
                    comparison_problem=comparison_problem,
                    citation=_citation_suffix(cites, 3),
                ),
                _render(
                    str(template_pack.get('paragraph_2') or 'Across {subsection_preview}, the recurring contrasts are {recurring_contrasts}, so each subsection sharpens a different part of the same argument{citation}.'),
                    subsection_preview=subsection_preview,
                    recurring_contrasts=recurring_contrasts,
                    citation=_citation_suffix(cites[3:], 3) or _citation_suffix(cites, 3),
                ),
            ]
            if lead_plan:
                paragraphs.append(
                    _render(
                        str(template_pack.get('paragraph_3') or 'That progression moves from {lead_start} toward {lead_end}, keeping the chapter comparative without collapsing distinct design choices into a single architecture label{citation}.'),
                        lead_start=lead_plan[0].lower(),
                        lead_end=lead_plan[-1].lower(),
                        citation=_citation_suffix(cites[6:], 2) or _citation_suffix(cites, 2),
                    )
                )
            path = sections_dir / f"{slug_unit_id(sec_id)}_lead.md"
            atomic_write_text(path, '\n\n'.join(paragraphs).rstrip() + '\n')
            written.append(str(path.relative_to(workspace)))

    report = '\n'.join([
        '# Chapter leads report',
        '',
        '- Status: PASS',
        f'- Generated at: `{now_iso_seconds()}`',
    ] + [f'- `{p}`' for p in written]) + '\n'
    atomic_write_text(report_path, report)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
