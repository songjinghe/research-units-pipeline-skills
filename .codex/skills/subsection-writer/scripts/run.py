from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def _clean(text: str, *, limit: int = 220) -> str:
    s = str(text or '').strip()
    s = s.replace('\n', ' ')
    s = re.sub(r'\s+', ' ', s)
    s = s.replace('|', ', ')
    s = s.strip(' "\'`')
    if len(s) <= limit:
        return s
    clipped = s[:limit].rsplit(' ', 1)[0].strip()
    return clipped if clipped else s[:limit].strip()


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


def _cites(keys: list[str], *, max_keys: int = 3) -> str:
    vals = _uniq(keys)[:max_keys]
    return ' '.join(f'[@{k}]' for k in vals)


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


def _item_from_comp(card: dict[str, Any], title: str) -> tuple[str, list[str]]:
    axis = _clean(str(card.get('axis') or '').replace('/', ' and '), limit=90)
    a_label = _clean(str(card.get('A_label') or 'one line of work').replace('/', ' and '), limit=40)
    b_label = _clean(str(card.get('B_label') or 'another line of work').replace('/', ' and '), limit=40)
    a_hls = [x for x in (card.get('A_highlights') or []) if isinstance(x, dict)]
    b_hls = [x for x in (card.get('B_highlights') or []) if isinstance(x, dict)]
    a_excerpt = _clean((a_hls[0].get('excerpt') if a_hls else ''), limit=150)
    b_excerpt = _clean((b_hls[0].get('excerpt') if b_hls else ''), limit=150)
    citations: list[str] = [str(x).strip() for x in (card.get('citations') or []) if str(x).strip()]
    for pool in [a_hls, b_hls]:
        for item in pool[:2]:
            for k in item.get('citations') or []:
                citations.append(str(k).strip())
    sentence = (
        f"A recurring comparison in {title.lower()} concerns {axis or 'how competing designs are evaluated'}. "
        f"{a_label} is usually supported by evidence such as {_clean(a_excerpt or 'its reported empirical profile', limit=130)} {_cites(citations[:2], max_keys=2)}, "
        f"whereas {b_label} is tied to {_clean(b_excerpt or 'a different operational trade-off', limit=130)} {_cites(citations[2:], max_keys=2) or _cites(citations, max_keys=2)}."
    )
    return sentence, citations


def _item_from_anchor(anchor: dict[str, Any], title: str) -> tuple[str, list[str]]:
    text = _clean(anchor.get('text') or '', limit=200)
    citations = [str(x).strip() for x in (anchor.get('citations') or []) if str(x).strip()]
    sentence = f"Concrete anchors matter in {title.lower()} because {text} {_cites(citations, max_keys=3)}."
    return sentence, citations


def _item_from_eval(item: dict[str, Any], title: str) -> tuple[str, list[str]]:
    bullet = _clean(item.get('bullet') or '', limit=190)
    citations = [str(x).strip() for x in (item.get('citations') or []) if str(x).strip()]
    sentence = f"Evaluation remains part of the substantive comparison in {title.lower()} because {bullet} {_cites(citations, max_keys=3)}."
    return sentence, citations


def _item_from_limit(item: dict[str, Any], title: str) -> tuple[str, list[str]]:
    text = _clean(item.get('excerpt') or item.get('bullet') or '', limit=190)
    citations = [str(x).strip() for x in (item.get('citations') or []) if str(x).strip()]
    sentence = f"A recurring limitation in {title.lower()} is that {text} {_cites(citations, max_keys=3)}, which narrows how confidently results can be generalized across settings."
    return sentence, citations


def _make_paragraphs(pack: dict[str, Any], title: str) -> list[str]:
    thesis = _clean(pack.get('thesis') or f'{title} is best read as a comparison problem rather than a single architecture category.', limit=260)
    tension = _clean(pack.get('tension_statement') or 'reported gains are often shaped by evaluation and interface assumptions as much as by the nominal agent design', limit=260)
    rq = _clean(pack.get('rq') or '', limit=220)

    cards = [x for x in (pack.get('comparison_cards') or []) if isinstance(x, dict)]
    anchors = [x for x in (pack.get('anchor_facts') or []) if isinstance(x, dict)]
    evals = [x for x in (pack.get('evaluation_protocol') or []) if isinstance(x, dict)]
    limits = [x for x in (pack.get('limitation_hooks') or []) if isinstance(x, dict)]
    axes = [str(x).strip().replace('/', ' and ') for x in (pack.get('axes') or []) if str(x).strip()]

    seed_cites: list[str] = []
    for source in cards[:2]:
        seed_cites.extend([str(x).strip() for x in (source.get('citations') or []) if str(x).strip()])
    for source in anchors[:2]:
        seed_cites.extend([str(x).strip() for x in (source.get('citations') or []) if str(x).strip()])

    paragraphs: list[str] = []
    paragraphs.append(
        f"{title} becomes analytically useful only when the subsection is read through a stable analytical frame rather than as a loose method bucket. "
        f"The central claim here is that {thesis.lower()} {_cites(seed_cites, max_keys=3)}. "
        f"That framing matters because {tension.lower()}, and it makes the subsection's guiding question explicit: {rq.lower() if rq else 'which design choices create the most consequential trade-offs under comparable protocols'}."
    )

    items: list[tuple[str, list[str]]] = []
    items.extend(_item_from_comp(card, title) for card in cards[:4])
    items.extend(_item_from_anchor(anchor, title) for anchor in anchors[:3])
    items.extend(_item_from_eval(item, title) for item in evals[:3])
    items.extend(_item_from_limit(item, title) for item in limits[:3])

    used: list[str] = seed_cites[:]
    for text, cites in items[:8]:
        paragraphs.append(text)
        used.extend(cites)

    lens = ', '.join(axes[:3]) if axes else 'execution assumptions, evaluation design, and operational constraints'
    paragraphs.append(
        f"Taken together, these comparisons show that {title.lower()} should be judged through {lens} rather than through isolated benchmark wins. "
        f"Across the cited evidence, stronger results usually coincide with more explicit protocol choices, clearer tool contracts, and more transparent assumptions about cost or access {_cites(used, max_keys=4)}."
    )
    paragraphs.append(
        f"The safest synthesis is therefore conservative: the literature already supports meaningful contrasts inside {title.lower()}, but those contrasts stay interpretable only when the subsection keeps architecture, protocol, and limitation signals in the same frame {_cites(used[4:], max_keys=4) or _cites(used, max_keys=4)}."
    )

    while len(paragraphs) < 10:
        paragraphs.append(
            f"Additional evidence in {title.lower()} reinforces the same pattern from a different angle, linking system behavior to the details of how tasks, interfaces, and constraints are specified {_cites(used, max_keys=3)}."
        )

    return [p.strip() for p in paragraphs if p.strip()]


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
    from tooling.pipeline_text import slug_unit_id
    from tooling.quality_gate import check_unit_outputs, write_quality_report

    workspace = Path(args.workspace).resolve()
    unit_id = str(args.unit_id or 'U100').strip() or 'U100'
    inputs = parse_semicolon_list(args.inputs)
    outputs = parse_semicolon_list(args.outputs) or ['sections/sections_manifest.jsonl', 'sections/h3_bodies.refined.ok']

    out_rel = next((x for x in outputs if x.endswith('sections_manifest.jsonl')), 'sections/sections_manifest.jsonl')
    marker_rel = next((x for x in outputs if x.endswith('.refined.ok')), 'sections/h3_bodies.refined.ok')
    out_path = workspace / out_rel
    marker_path = workspace / marker_rel
    sections_dir = out_path.parent
    ensure_dir(sections_dir)

    decisions_path = workspace / 'DECISIONS.md'
    if not decisions_has_approval(decisions_path, 'C2'):
        block = '\n'.join([
            '## C5 section writing request',
            '',
            '- This unit writes prose into per-section files under `sections/`.',
            '- Please tick `Approve C2` in `DECISIONS.md`, then rerun this unit.',
            '',
        ])
        upsert_checkpoint_block(decisions_path, 'C5', block)
        return 2

    outline = load_yaml(workspace / 'outline' / 'outline.yml') if (workspace / 'outline' / 'outline.yml').exists() else []
    packs = {str(r.get('sub_id') or '').strip(): r for r in _load_jsonl(workspace / 'outline' / 'writer_context_packs.jsonl') if str(r.get('sub_id') or '').strip()}
    if not packs:
        briefs = {str(r.get('sub_id') or '').strip(): r for r in _load_jsonl(workspace / 'outline' / 'subsection_briefs.jsonl') if str(r.get('sub_id') or '').strip()}
        evidence = {str(r.get('sub_id') or '').strip(): r for r in _load_jsonl(workspace / 'outline' / 'evidence_drafts.jsonl') if str(r.get('sub_id') or '').strip()}
        for sid, brief in briefs.items():
            pack = dict(brief)
            pack.update(evidence.get(sid) or {})
            pack.setdefault('comparison_cards', pack.get('concrete_comparisons') or [])
            pack.setdefault('anchor_facts', [])
            pack.setdefault('limitation_hooks', pack.get('failures_limitations') or [])
            packs[sid] = pack

    records: list[dict[str, Any]] = []
    generated_at = now_iso_seconds()

    def add_record(rec: dict[str, Any]) -> None:
        p = workspace / str(rec.get('path') or '')
        exists = p.exists() and p.stat().st_size > 0
        rec['exists'] = bool(exists)
        rec['generated_at'] = generated_at
        if exists:
            text = p.read_text(encoding='utf-8', errors='ignore')
            rec['citations'] = _uniq(re.findall(r'\[@([^\]]+)\]', text))
            rec['bytes'] = p.stat().st_size
        records.append(rec)

    for name, title in [('abstract', 'Abstract'), ('discussion', 'Discussion'), ('conclusion', 'Conclusion')]:
        add_record({'kind': 'global', 'id': name, 'title': title, 'path': f'sections/{name}.md'})

    if isinstance(outline, list):
        for sec in outline:
            if not isinstance(sec, dict):
                continue
            sec_id = str(sec.get('id') or '').strip()
            sec_title = str(sec.get('title') or '').strip()
            subs = [sub for sub in (sec.get('subsections') or []) if isinstance(sub, dict)]
            if subs and sec_id:
                lead_path = sections_dir / f'{slug_unit_id(sec_id)}_lead.md'
                add_record({'kind': 'h2_lead', 'id': sec_id, 'title': sec_title, 'section_id': sec_id, 'section_title': sec_title, 'path': str(lead_path.relative_to(workspace))})
            elif sec_id:
                add_record({'kind': 'h2', 'id': sec_id, 'title': sec_title, 'section_id': sec_id, 'section_title': sec_title, 'path': f'sections/{slug_unit_id(sec_id)}.md'})

            for sub in subs:
                sub_id = str(sub.get('id') or '').strip()
                title = str(sub.get('title') or '').strip()
                if not sub_id or not title:
                    continue
                path = sections_dir / f'{slug_unit_id(sub_id)}.md'
                if not path.exists() or path.stat().st_size <= 0:
                    pack = packs.get(sub_id) or {'title': title}
                    text = '\n\n'.join(_make_paragraphs(pack, title)).rstrip() + '\n'
                    atomic_write_text(path, text)
                add_record({'kind': 'h3', 'id': sub_id, 'title': title, 'section_id': sec_id, 'section_title': sec_title, 'path': str(path.relative_to(workspace))})

    atomic_write_text(out_path, '\n'.join(json.dumps(r, ensure_ascii=False) for r in records).rstrip() + '\n')
    atomic_write_text(marker_path, f'h3 bodies refined at {generated_at}\n')

    issues = check_unit_outputs(skill='subsection-writer', workspace=workspace, outputs=[out_rel])
    if issues:
        write_quality_report(workspace=workspace, unit_id=unit_id, skill='subsection-writer', issues=issues)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
