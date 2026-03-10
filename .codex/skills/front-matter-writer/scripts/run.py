from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not path.exists() or path.stat().st_size <= 0:
        return out
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


def _load_json(path: Path) -> dict[str, Any]:
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


def _cites(keys: list[str], n: int) -> str:
    ks = _uniq(keys)[:n]
    return ' '.join(f'[@{k}]' for k in ks)


def _goal_text(path: Path) -> str:
    if not path.exists():
        return 'the approved survey topic'
    lines = [ln.strip() for ln in path.read_text(encoding='utf-8', errors='ignore').splitlines() if ln.strip() and not ln.startswith('#')]
    return lines[0] if lines else 'the approved survey topic'


def _parse_stats(retrieval_path: Path, core_path: Path, queries_path: Path) -> tuple[str, str, str]:
    time_window = 'recent years'
    candidate_pool = 'a large candidate pool'
    evidence_mode = 'abstract-level evidence'
    if retrieval_path.exists():
        text = retrieval_path.read_text(encoding='utf-8', errors='ignore')
        m = re.search(r'Imported/collected records .*?`(\d+)`', text)
        if m:
            candidate_pool = f"a candidate pool of {m.group(1)} records"
        m = re.search(r'Time window:\s*`([^`]*)`\.\.`([^`]*)`', text)
        if m:
            left = m.group(1).strip()
            right = m.group(2).strip()
            if left and right:
                time_window = f'{left}–{right}'
            elif left:
                time_window = f'since {left}'
    core_size = 'a 300-paper core set'
    if core_path.exists():
        rows = max(0, sum(1 for _ in core_path.open(encoding='utf-8', errors='ignore')) - 1)
        if rows > 0:
            core_size = f'a {rows}-paper core set'
    if queries_path.exists():
        q = queries_path.read_text(encoding='utf-8', errors='ignore')
        m = re.search(r'(?im)^-\s*evidence_mode\s*:\s*([^#\n]+)', q)
        if m:
            evidence_mode = m.group(1).strip()
    return time_window, candidate_pool, f'{core_size} with {evidence_mode}'


def _cite_range(keys: list[str], start: int, stop: int, n: int) -> str:
    return _cites(keys[start:stop], n)


def _detect_domain(workspace: Path) -> str | None:
    """Return a domain id if workspace text matches a domain template, else None."""
    package_root = Path(__file__).resolve().parents[1]
    domain_dir = package_root / 'assets' / 'domain_templates'
    if not domain_dir.is_dir():
        return None
    corpus_parts: list[str] = []
    for name in ('GOAL.md', 'queries.md'):
        p = workspace / name
        if p.exists():
            corpus_parts.append(p.read_text(encoding='utf-8', errors='ignore').lower())
    corpus = ' '.join(corpus_parts)
    if not corpus.strip():
        return None
    import glob as _glob
    for pack_path in sorted(Path(f) for f in _glob.glob(str(domain_dir / '*.json'))):
        pack = _load_json(pack_path)
        triggers = pack.get('topic_triggers') or {}
        group_a = [t.lower() for t in (triggers.get('trigger_group_a') or [])]
        group_b = [t.lower() for t in (triggers.get('trigger_group_b') or [])]
        if not group_a or not group_b:
            continue
        has_a = any(t in corpus for t in group_a)
        has_b = any(t in corpus for t in group_b)
        if has_a and has_b:
            return pack.get('domain_id') or pack_path.stem
    return None


def _load_domain_overlay(domain_id: str) -> dict[str, Any]:
    """Load a domain template overlay by id.  Returns {} if not found."""
    package_root = Path(__file__).resolve().parents[1]
    domain_path = package_root / 'assets' / 'domain_templates' / f'{domain_id}.json'
    return _load_json(domain_path)


def _merge_template_bank(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    """Overlay domain paragraphs onto a generic base template bank."""
    merged = dict(base)
    for key in ('introduction_paragraphs', 'related_work_paragraphs',
                'abstract_sentences', 'discussion_paragraphs', 'conclusion_paragraphs'):
        if key in overlay:
            merged[key] = overlay[key]
    return merged


def _template_values(*, goal: str, candidate_pool: str, evidence_note: str, time_window: str, all_keys: list[str]) -> dict[str, str]:
    return {
        'goal': goal,
        'candidate_pool': candidate_pool,
        'evidence_note': evidence_note,
        'time_window': time_window,
        'cite_0_4': _cite_range(all_keys, 0, 4, 4),
        'cite_4_8': _cite_range(all_keys, 4, 8, 4),
        'cite_8_12': _cite_range(all_keys, 8, 12, 4),
        'cite_0_5': _cite_range(all_keys, 0, 5, 5),
        'cite_5_10': _cite_range(all_keys, 5, 10, 5),
        'cite_10_15': _cite_range(all_keys, 10, 15, 5),
        'cite_15_20': _cite_range(all_keys, 15, 20, 5),
        'cite_20_25': _cite_range(all_keys, 20, 25, 5),
        'cite_25_30': _cite_range(all_keys, 25, 30, 5),
        'cite_30_35': _cite_range(all_keys, 30, 35, 5),
        'cite_35_40': _cite_range(all_keys, 35, 40, 5),
        'cite_0_6': _cite_range(all_keys, 0, 6, 6),
        'cite_6_12': _cite_range(all_keys, 6, 12, 6),
        'cite_12_18': _cite_range(all_keys, 12, 18, 6),
        'cite_18_24': _cite_range(all_keys, 18, 24, 6),
        'cite_24_30': _cite_range(all_keys, 24, 30, 6),
        'cite_30_36': _cite_range(all_keys, 30, 36, 6),
        'cite_36_42': _cite_range(all_keys, 36, 42, 6),
        'cite_42_48': _cite_range(all_keys, 42, 48, 6),
        'cite_48_54': _cite_range(all_keys, 48, 54, 6),
        'cite_54_60': _cite_range(all_keys, 54, 60, 6),
        'cite_12_16': _cite_range(all_keys, 12, 16, 4),
        'cite_16_20': _cite_range(all_keys, 16, 20, 4),
        'cite_20_24': _cite_range(all_keys, 20, 24, 4),
    }


def _render_lines(lines: list[str], values: dict[str, str]) -> list[str]:
    rendered: list[str] = []
    for raw in lines:
        text = str(raw or '').strip()
        if not text:
            continue
        rendered.append(text.format_map(values))
    return rendered


def _render_paragraph_section(*, heading: str, paragraphs: list[str], values: dict[str, str]) -> str:
    rendered = _render_lines(paragraphs, values)
    return heading + '\n\n' + '\n\n'.join(rendered).rstrip() + '\n'


def _render_sentence_section(*, heading: str, sentences: list[str], values: dict[str, str]) -> str:
    rendered = _render_lines(sentences, values)
    return heading + '\n\n' + ' '.join(rendered).strip() + '\n'


def _lint_reader_facing(*, label: str, text: str) -> None:
    checks = [
        (r"(?i)\bthis pipeline\b", "pipeline narration"),
        (r"(?i)\bacross the pipeline\b", "pipeline narration"),
        (r"(?i)\bworkspace\b", "workspace narration"),
        (r"(?i)\bstage\s*C\d+\b", "stage narration"),
        (r"(?i)\bapprove\s*C\d+\b", "approval narration"),
    ]
    for pattern, name in checks:
        if re.search(pattern, text):
            raise SystemExit(f"Reader-facing {label} contains forbidden {name}: {pattern}")


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

    from tooling.common import atomic_write_text, decisions_has_approval, ensure_dir, load_yaml, now_iso_seconds, parse_semicolon_list, upsert_checkpoint_block

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs)
    outputs = parse_semicolon_list(args.outputs)
    sections_dir = workspace / 'sections'
    ensure_dir(sections_dir)

    decisions_path = workspace / 'DECISIONS.md'
    if not decisions_has_approval(decisions_path, 'C2'):
        block = '\n'.join([
            '## C5 front matter request',
            '',
            '- This unit writes prose into `sections/`.',
            '- Please tick `Approve C2` in `DECISIONS.md`, then rerun this unit.',
            '',
        ])
        upsert_checkpoint_block(decisions_path, 'C5', block)
        return 2

    outline = load_yaml(workspace / 'outline' / 'outline.yml') if (workspace / 'outline' / 'outline.yml').exists() else []
    goal = _goal_text(workspace / 'GOAL.md')
    time_window, candidate_pool, evidence_note = _parse_stats(workspace / 'papers' / 'retrieval_report.md', workspace / 'papers' / 'core_set.csv', workspace / 'queries.md')

    packs = _load_jsonl(workspace / 'outline' / 'writer_context_packs.jsonl')
    all_keys: list[str] = []
    for rec in packs:
        for field in ['allowed_bibkeys_selected', 'allowed_bibkeys_chapter', 'allowed_bibkeys_global']:
            for key in rec.get(field) or []:
                all_keys.append(str(key).strip())
        for rec2 in rec.get('anchor_facts') or []:
            if isinstance(rec2, dict):
                for key in rec2.get('citations') or []:
                    all_keys.append(str(key).strip())
    all_keys = _uniq(all_keys)

    intro_id = '1'
    related_id = '2'
    if isinstance(outline, list):
        for sec in outline:
            if not isinstance(sec, dict):
                continue
            sid = str(sec.get('id') or '').strip()
            title = str(sec.get('title') or '').strip().lower()
            if sid and 'intro' in title:
                intro_id = sid
            if sid and 'related' in title:
                related_id = sid

    intro_path = sections_dir / f'S{intro_id}.md'
    related_path = sections_dir / f'S{related_id}.md'
    abstract_path = sections_dir / 'abstract.md'
    discussion_path = sections_dir / 'discussion.md'
    conclusion_path = sections_dir / 'conclusion.md'
    report_path = workspace / 'output' / 'FRONT_MATTER_REPORT.md'
    context_path = workspace / 'output' / 'FRONT_MATTER_CONTEXT.json'
    ensure_dir(report_path.parent)

    package_root = Path(__file__).resolve().parents[1]
    template_asset_path = package_root / 'assets' / 'front_matter_templates.json'
    template_bank = _load_json(template_asset_path)
    if not template_bank:
        raise SystemExit(f'Missing or invalid front-matter template asset: {template_asset_path}')

    domain_id = _detect_domain(workspace)
    if domain_id:
        overlay = _load_domain_overlay(domain_id)
        if overlay:
            template_bank = _merge_template_bank(template_bank, overlay)

    values = _template_values(
        goal=goal,
        candidate_pool=candidate_pool,
        evidence_note=evidence_note,
        time_window=time_window,
        all_keys=all_keys,
    )

    intro_paragraphs = _render_lines(list(template_bank.get('introduction_paragraphs') or []), values)
    related_paragraphs = _render_lines(list(template_bank.get('related_work_paragraphs') or []), values)
    headings = template_bank.get('headings') or {}
    abstract = _render_sentence_section(
        heading=str(headings.get('abstract') or '## Abstract'),
        sentences=list(template_bank.get('abstract_sentences') or []),
        values=values,
    )
    discussion = _render_paragraph_section(
        heading=str(headings.get('discussion') or '## Discussion'),
        paragraphs=list(template_bank.get('discussion_paragraphs') or []),
        values=values,
    )
    conclusion = _render_paragraph_section(
        heading=str(headings.get('conclusion') or '## Conclusion'),
        paragraphs=list(template_bank.get('conclusion_paragraphs') or []),
        values=values,
    )

    _lint_reader_facing(label='abstract', text=abstract)
    _lint_reader_facing(label='introduction', text='\n\n'.join(intro_paragraphs))
    _lint_reader_facing(label='related_work', text='\n\n'.join(related_paragraphs))
    _lint_reader_facing(label='discussion', text=discussion)
    _lint_reader_facing(label='conclusion', text=conclusion)

    atomic_write_text(abstract_path, abstract)
    atomic_write_text(intro_path, '\n\n'.join(intro_paragraphs).rstrip() + '\n')
    atomic_write_text(related_path, '\n\n'.join(related_paragraphs).rstrip() + '\n')
    atomic_write_text(discussion_path, discussion)
    atomic_write_text(conclusion_path, conclusion)

    context = {
        'goal': goal,
        'section_ids': {'intro': intro_id, 'related': related_id},
        'time_window': time_window,
        'candidate_pool': candidate_pool,
        'evidence_note': evidence_note,
        'sections': {
            'abstract': str(abstract_path.relative_to(workspace)),
            'introduction': str(intro_path.relative_to(workspace)),
            'related_work': str(related_path.relative_to(workspace)),
            'discussion': str(discussion_path.relative_to(workspace)),
            'conclusion': str(conclusion_path.relative_to(workspace)),
        },
        'reference_pack': template_bank.get('reference_pack') or [
            'references/overview.md',
            'references/abstract_archetypes.md',
            'references/introduction_jobs.md',
            'references/related_work_positioning.md',
            'references/discussion_conclusion_patterns.md',
            'references/forbidden_stems.md',
            'references/examples_good.md',
            'references/examples_bad.md',
        ],
        'asset_pack': [
            'assets/front_matter_context.schema.json',
            'assets/front_matter_context_schema.json',
            'assets/front_matter_templates.json',
        ],
        'template_asset': 'assets/front_matter_templates.json',
        'voice_hygiene': {
            'forbid_pipeline_voice': True,
            'forbid_domain_default_fallback': True,
            'methodology_note_max_occurrences': 1,
        },
        'citation_pool_size': len(all_keys),
    }
    atomic_write_text(context_path, json.dumps(context, indent=2, ensure_ascii=False) + '\n')

    report = '\n'.join([
        '# Front matter report',
        '',
        '- Status: PASS',
        f'- Generated at: `{now_iso_seconds()}`',
        f'- Abstract: `sections/abstract.md`',
        f'- Introduction: `sections/S{intro_id}.md`',
        f'- Related Work: `sections/S{related_id}.md`',
        f'- Context sidecar: `output/FRONT_MATTER_CONTEXT.json`',
        f'- Template asset: `assets/front_matter_templates.json`',
        '- Discussion: `sections/discussion.md`',
        '- Conclusion: `sections/conclusion.md`',
        '- Compatibility mode: prose outputs preserved; template bank externalized into assets.',
    ]) + '\n'
    atomic_write_text(report_path, report)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
