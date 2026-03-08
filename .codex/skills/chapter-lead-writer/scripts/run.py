from __future__ import annotations

import argparse
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
            sec_title = str(sec.get('title') or '').strip()
            if not sec_id:
                continue
            brief = briefs.get(sec_id) or {}
            throughline = [_clean_phrase(x) for x in (brief.get('throughline') or []) if _clean_phrase(x)]
            contrasts = [_clean_phrase(x) for x in (brief.get('key_contrasts') or []) if _clean_phrase(x)]
            lead_plan = [_clean_phrase(x) for x in (brief.get('lead_paragraph_plan') or []) if _clean_phrase(x)]
            sub_titles = [str(x.get('title') or '').strip() for x in subs if str(x.get('title') or '').strip()]
            cites = cites_by_sec.get(sec_id) or []
            paragraphs = [
                f"{sec_title} is organized around a shared comparison problem rather than a list of isolated techniques: {'; '.join(throughline[:2]) or 'the chapter asks how adjacent subsections resolve the same system tension'} {_cite(cites, 3)}.",
                f"The chapter links {'; '.join(sub_titles[:3])} by holding fixed the contrasts around {', '.join(contrasts[:3]) or 'protocol assumptions, resource constraints, and evaluation scope'}, so each subsection sharpens a different part of the same argument {_cite(cites[3:], 3) or _cite(cites, 3)}.",
            ]
            if lead_plan:
                paragraphs.append(f"Read together, these subsections move from {lead_plan[0].lower()} toward {lead_plan[-1].lower()}, which keeps the chapter comparative without collapsing distinct design choices into a single architecture label {_cite(cites[6:], 2) or _cite(cites, 2)}.")
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
