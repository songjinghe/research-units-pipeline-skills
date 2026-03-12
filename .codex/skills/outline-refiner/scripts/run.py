from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def _sha1_text(text: str) -> str:
    return hashlib.sha1((text or '').encode('utf-8', errors='ignore')).hexdigest()


def _read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore') if path.exists() else ''


def _backup_existing(path: Path) -> None:
    from tooling.common import backup_existing

    backup_existing(path)

def _append_jsonl(path: Path, rec: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _generic_axis(x: str) -> bool:
    x = (x or '').strip().lower()
    x = ' '.join(x.split())
    generic = {
        'mechanism / architecture',
        'data / training setup',
        'evaluation protocol',
        'evaluation protocol (benchmarks / metrics / human)',
        'evaluation protocol (datasets / metrics / human)',
        'compute / efficiency',
        'efficiency / compute',
        'failure modes / limitations',
    }
    return x in generic


def _median_int(values: list[int]) -> float:
    if not values:
        return 0.0
    xs = sorted(values)
    mid = len(xs) // 2
    if len(xs) % 2 == 1:
        return float(xs[mid])
    return (xs[mid - 1] + xs[mid]) / 2.0


def _parse_section_binding_report(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for raw in (text or '').splitlines():
        line = raw.strip()
        if not line.startswith('|') or line.startswith('|---'):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if len(cells) < 4:
            continue
        if cells[0].lower() == 'section' and cells[2].lower() == 'status':
            continue
        rows.append(
            {
                'section': cells[0],
                'coverage': cells[1],
                'status': cells[2].upper(),
                'recommendation': cells[3],
            }
        )
    return rows


def _section_binding_status(rec: dict[str, Any]) -> str:
    for key in ('status', 'binding_status'):
        status = str(rec.get(key) or '').strip().upper()
        if status in {'PASS', 'BLOCKED', 'REROUTE'}:
            return status
    recommendation = str(rec.get('decomposition_recommendation') or '').strip().lower()
    gaps = rec.get('blocking_gaps') or []
    if isinstance(gaps, list) and gaps:
        return 'BLOCKED'
    if recommendation == 'decompose':
        return 'PASS'
    if recommendation:
        return 'REROUTE'
    return ''


def _prior_structure_reroutes(state_path: Path, *, read_jsonl_fn: Any) -> int:
    if not state_path.exists() or state_path.stat().st_size <= 0:
        return 0
    count = 0
    for rec in read_jsonl_fn(state_path):
        if not isinstance(rec, dict):
            continue
        phase = str(rec.get('structure_phase') or '').strip().lower()
        target = str(rec.get('reroute_target') or '').strip()
        if phase in {'binding_blocked', 'binding_reroute'} or target:
            count += 1
    return count


def _structure_cutover_fields(
    *,
    workspace: Path,
    state_path: Path,
    h3_total: int,
    mapping_rows: list[dict[str, Any]],
    read_jsonl_fn: Any,
    load_workspace_pipeline_spec_fn: Any,
) -> dict[str, Any]:
    section_layer_present = all(
        (workspace / rel).exists()
        for rel in (
            'outline/chapter_skeleton.yml',
            'outline/section_bindings.jsonl',
            'outline/section_binding_report.md',
            'outline/section_briefs.jsonl',
        )
    )

    section_binding_report = _read_text(workspace / 'outline' / 'section_binding_report.md')
    section_binding_recs = [
        rec for rec in read_jsonl_fn(workspace / 'outline' / 'section_bindings.jsonl') if isinstance(rec, dict)
    ]
    section_rows = _parse_section_binding_report(section_binding_report)
    section_briefs_recs = [r for r in read_jsonl_fn(workspace / 'outline' / 'section_briefs.jsonl') if isinstance(r, dict)]

    status_counts = {'pass': 0, 'blocked': 0, 'reroute': 0}
    invalid_statuses: list[str] = []
    nonpass_sections: list[dict[str, str]] = []
    report_status_by_id: dict[str, str] = {}
    for row in section_rows:
        label = str(row.get('section') or '').strip()
        section_id = label.split(' ', 1)[0].strip() if label else ''
        status = str(row.get('status') or '').strip().upper()
        if section_id and status:
            report_status_by_id[section_id] = status
        if status == 'PASS':
            status_counts['pass'] += 1
            continue
        if status == 'BLOCKED':
            status_counts['blocked'] += 1
            nonpass_sections.append(
                {
                    'section': label,
                    'status': 'blocked',
                    'recommendation': str(row.get('recommendation') or '').strip(),
                }
            )
            continue
        if status == 'REROUTE':
            status_counts['reroute'] += 1
            nonpass_sections.append(
                {
                    'section': label,
                    'status': 'reroute',
                    'recommendation': str(row.get('recommendation') or '').strip(),
                }
            )
            continue
        if status:
            invalid_statuses.append(status)

    json_status_counts = {'pass': 0, 'blocked': 0, 'reroute': 0}
    json_nonpass_sections: list[dict[str, str]] = []
    json_report_mismatch = False
    for rec in section_binding_recs:
        section_id = str(rec.get('section_id') or '').strip()
        section_title = str(rec.get('section_title') or '').strip()
        section_label = f"{section_id} {section_title}".strip()
        status = _section_binding_status(rec)
        recommendation = str(rec.get('decomposition_recommendation') or '').strip()
        if section_id and report_status_by_id.get(section_id) not in {'', status}:
            json_report_mismatch = True
        if status == 'PASS':
            json_status_counts['pass'] += 1
            continue
        if status == 'BLOCKED':
            json_status_counts['blocked'] += 1
            json_nonpass_sections.append(
                {
                    'section': section_label or section_id,
                    'status': 'blocked',
                    'recommendation': recommendation,
                }
            )
            continue
        if status == 'REROUTE':
            json_status_counts['reroute'] += 1
            json_nonpass_sections.append(
                {
                    'section': section_label or section_id,
                    'status': 'reroute',
                    'recommendation': recommendation,
                }
            )
            continue
        if status:
            invalid_statuses.append(status)

    if section_binding_recs:
        status_counts = json_status_counts
        nonpass_sections = json_nonpass_sections

    brief_blocked_sections: list[str] = []
    for rec in section_briefs_recs:
        gaps = rec.get('blocking_gaps') or []
        if not isinstance(gaps, list) or not gaps:
            continue
        label = str(rec.get('section_id') or rec.get('section_title') or '').strip()
        if label and label not in brief_blocked_sections:
            brief_blocked_sections.append(label)

    structure_phase = 'decomposed'
    h3_status = 'stable' if h3_total > 0 and mapping_rows else 'unstable'
    reroute_target = ''
    reroute_reason = ''
    section_binding_gate = 'pass'

    if not section_layer_present:
        structure_phase = 'h3_first_legacy'
        section_binding_gate = 'legacy'
    elif invalid_statuses or (section_binding_report.strip() and not section_rows):
        structure_phase = 'binding_reroute'
        h3_status = 'unstable'
        reroute_target = 'section-bindings'
        section_binding_gate = 'reroute'
        reroute_reason = (
            'section_binding_report has missing or invalid status rows'
            if not invalid_statuses
            else f"section_binding_report contains unsupported statuses: {', '.join(sorted(set(invalid_statuses)))}"
        )
    elif json_report_mismatch:
        structure_phase = 'binding_reroute'
        h3_status = 'unstable'
        reroute_target = 'section-bindings'
        section_binding_gate = 'reroute'
        reroute_reason = 'section_bindings.jsonl and section_binding_report.md disagree on PASS/BLOCKED/REROUTE status'
    elif status_counts['blocked'] > 0 or brief_blocked_sections:
        structure_phase = 'binding_blocked'
        h3_status = 'unstable'
        reroute_target = 'section-bindings'
        section_binding_gate = 'blocked'
        details = [f"{row['section']} ({row['recommendation'] or 'no recommendation'})" for row in nonpass_sections if row.get('status') == 'blocked']
        if brief_blocked_sections:
            details.append(f"section_briefs blocking_gaps: {', '.join(brief_blocked_sections[:4])}")
        reroute_reason = '; '.join(details[:4]) or 'section binding layer reported BLOCKED'
    elif status_counts['reroute'] > 0:
        structure_phase = 'binding_reroute'
        h3_status = 'unstable'
        reroute_target = 'section-bindings'
        section_binding_gate = 'reroute'
        details = [f"{row['section']} ({row['recommendation'] or 'no recommendation'})" for row in nonpass_sections if row.get('status') == 'reroute']
        reroute_reason = '; '.join(details[:4]) or 'section binding layer requested reroute'

    spec = load_workspace_pipeline_spec_fn(workspace)
    retry_budget_remaining: int | str = ''
    stage_budget: int | None = None
    if spec is not None:
        try:
            stage_budget = int(((spec.loop_policy or {}).get('stage_retry_budget') or {}).get('C2') or '')
        except Exception:
            stage_budget = None
    if stage_budget and stage_budget > 0:
        prior_reroutes = _prior_structure_reroutes(state_path, read_jsonl_fn=read_jsonl_fn)
        current_nonpass = 1 if section_binding_gate in {'blocked', 'reroute'} else 0
        retry_budget_remaining = max(0, int(stage_budget) - prior_reroutes - current_nonpass)

    human_approved = '- [x] Approve C2' in _read_text(workspace / 'DECISIONS.md')
    approval_status = 'approved' if human_approved and structure_phase == 'decomposed' and h3_status == 'stable' else 'pending'

    return {
        'structure_phase': structure_phase,
        'h3_status': h3_status,
        'approval_status': approval_status,
        'reroute_target': reroute_target,
        'retry_budget_remaining': retry_budget_remaining,
        'section_binding_gate': section_binding_gate,
        'section_binding_status_counts': status_counts,
        'section_binding_nonpass_sections': nonpass_sections[:8],
        'section_binding_report_sha1': _sha1_text(section_binding_report),
        'reroute_reason': reroute_reason,
    }


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

    from tooling.common import atomic_write_text, load_workspace_pipeline_spec, load_yaml, now_iso_seconds, parse_semicolon_list, read_jsonl, read_tsv

    workspace = Path(args.workspace).resolve()

    inputs = parse_semicolon_list(args.inputs) or [
        'outline/outline.yml',
        'outline/mapping.tsv',
        'papers/paper_notes.jsonl',
        'outline/subsection_briefs.jsonl',
        'GOAL.md',
    ]
    outputs = parse_semicolon_list(args.outputs) or ['outline/coverage_report.md', 'outline/outline_state.jsonl', 'output/REROUTE_STATE.json']

    outline_rel = inputs[0] if len(inputs) >= 1 else 'outline/outline.yml'
    mapping_rel = inputs[1] if len(inputs) >= 2 else 'outline/mapping.tsv'

    notes_rel = ''
    briefs_rel = ''
    goal_rel = ''
    for rel in inputs[2:]:
        rel = (rel or '').strip()
        if rel.endswith('papers/paper_notes.jsonl') or rel.endswith('paper_notes.jsonl'):
            notes_rel = rel
        elif rel.endswith('outline/subsection_briefs.jsonl') or rel.endswith('subsection_briefs.jsonl'):
            briefs_rel = rel
        elif rel.endswith('GOAL.md'):
            goal_rel = rel

    report_rel = outputs[0] if outputs else 'outline/coverage_report.md'
    state_rel = outputs[1] if len(outputs) >= 2 else 'outline/outline_state.jsonl'
    reroute_rel = outputs[2] if len(outputs) >= 3 else 'output/REROUTE_STATE.json'

    report_path = workspace / report_rel
    state_path = workspace / state_rel
    reroute_path = workspace / reroute_rel
    report_path.parent.mkdir(parents=True, exist_ok=True)
    reroute_path.parent.mkdir(parents=True, exist_ok=True)

    freeze_marker = report_path.with_name('coverage_report.refined.ok')
    report_frozen = report_path.exists() and report_path.stat().st_size > 0 and freeze_marker.exists()
    if report_path.exists() and report_path.stat().st_size > 0 and not report_frozen:
        _backup_existing(report_path)

    outline = load_yaml(workspace / outline_rel) if (workspace / outline_rel).exists() else []
    subsections: list[dict[str, str]] = []
    sections: list[dict[str, Any]] = []
    if isinstance(outline, list):
        for sec in outline:
            if not isinstance(sec, dict):
                continue
            sec_id = str(sec.get('id') or '').strip()
            sec_title = str(sec.get('title') or '').strip()
            sub_recs = []
            for sub in sec.get('subsections') or []:
                if not isinstance(sub, dict):
                    continue
                sid = str(sub.get('id') or '').strip()
                title = str(sub.get('title') or '').strip()
                if sid and title:
                    subsections.append({'sub_id': sid, 'title': title})
                    sub_recs.append({'sub_id': sid, 'title': title})
            if sec_id and sec_title:
                sections.append({'section_id': sec_id, 'title': sec_title, 'subsections': sub_recs})

    mapping_rows = read_tsv(workspace / mapping_rel) if (workspace / mapping_rel).exists() else []
    pids_by_sub: dict[str, list[str]] = {}
    for row in mapping_rows:
        if not isinstance(row, dict):
            continue
        sid = str(row.get('section_id') or '').strip()
        pid = str(row.get('paper_id') or '').strip()
        if not sid or not pid:
            continue
        pids_by_sub.setdefault(sid, [])
        if pid not in pids_by_sub[sid]:
            pids_by_sub[sid].append(pid)

    # Evidence levels from notes (best-effort).
    lvl_by_pid: dict[str, str] = {}
    if notes_rel and (workspace / notes_rel).exists():
        for rec in read_jsonl(workspace / notes_rel):
            if not isinstance(rec, dict):
                continue
            pid = str(rec.get('paper_id') or '').strip()
            lvl = str(rec.get('evidence_level') or '').strip().lower()
            if pid and lvl:
                lvl_by_pid[pid] = lvl

    # Axes specificity from briefs (best-effort).
    axes_by_sub: dict[str, list[str]] = {}
    if briefs_rel and (workspace / briefs_rel).exists():
        for rec in read_jsonl(workspace / briefs_rel):
            if not isinstance(rec, dict):
                continue
            sid = str(rec.get('sub_id') or '').strip()
            axes = rec.get('axes') or []
            if sid and isinstance(axes, list):
                axes_by_sub[sid] = [str(a).strip() for a in axes if str(a).strip()]

    usage: dict[str, int] = {}
    for sid, pids in pids_by_sub.items():
        for pid in pids:
            usage[pid] = usage.get(pid, 0) + 1

    top_reuse = sorted(usage.items(), key=lambda kv: (-kv[1], kv[0]))[:10]

    rows: list[dict[str, Any]] = []
    for sub in subsections:
        sid = sub['sub_id']
        title = sub['title']
        pids = pids_by_sub.get(sid) or []
        lvls = [lvl_by_pid.get(pid, '') for pid in pids]
        fulltext = sum(1 for x in lvls if x == 'fulltext')
        abstract = sum(1 for x in lvls if x == 'abstract')
        title_only = sum(1 for x in lvls if x == 'title')

        axes = axes_by_sub.get(sid) or []
        generic_n = sum(1 for a in axes if _generic_axis(a))
        specific_n = max(0, len(axes) - generic_n)

        rows.append(
            {
                'sub_id': sid,
                'title': title,
                'mapped_papers': len(pids),
                'unique_papers': len(set(pids)),
                'evidence_levels': {'fulltext': fulltext, 'abstract': abstract, 'title': title_only} if lvls else {},
                'axes_total': len(axes) if axes else 0,
                'axes_specific': specific_n if axes else 0,
                'axes_generic': generic_n if axes else 0,
                'reuse_max': max([usage.get(pid, 0) for pid in pids], default=0),
            }
        )

    # Render report (bullets + a small table).
    h2_total = len(sections)
    h2_with_h3 = sum(1 for s in sections if (s.get('subsections') or []))
    h3_total = len(subsections)
    h3_counts = [len(s.get('subsections') or []) for s in sections if (s.get('subsections') or [])]
    h3_min = min(h3_counts) if h3_counts else 0
    h3_med = _median_int(h3_counts) if h3_counts else 0.0
    h3_max = max(h3_counts) if h3_counts else 0

    lines: list[str] = [
        '# Coverage report (planner pass)',
        '',
        '- Guardrail: NO PROSE; this is a diagnostic artifact, not survey writing.',
        f"- Sections (H2): {h2_total}",
        f"- Chapters with subsections (H2 with H3): {h2_with_h3}",
        f"- Subsections (H3): {h3_total}",
        f"- H3 per H2 chapter (min/median/max): {h3_min}/{h3_med:.1f}/{h3_max}",
        f"- Mapping rows: {len(mapping_rows)}",
        f"- Unique mapped papers: {len(usage)}",
    ]

    if top_reuse:
        top_txt = ', '.join([f"{pid}×{cnt}" for pid, cnt in top_reuse[:6]])
        lines.append(f"- Most reused papers: {top_txt}")

    lines.extend(['', '## Per-subsection summary', ''])

    lines.append('| Subsection | #papers | Evidence levels | Axes (specific/generic) | Max reuse |')
    lines.append('|---|---:|---|---:|---:|')
    by_sid = {r['sub_id']: r for r in rows}
    for sub in subsections:
        r = by_sid.get(sub['sub_id']) or {}
        ev = r.get('evidence_levels') or {}
        ev_txt = '—'
        if isinstance(ev, dict) and ev:
            ev_txt = f"fulltext={ev.get('fulltext', 0)}, abstract={ev.get('abstract', 0)}, title={ev.get('title', 0)}"
        axes_txt = '—'
        if r.get('axes_total'):
            axes_txt = f"{r.get('axes_specific', 0)}/{r.get('axes_generic', 0)}"
        lines.append(
            f"| {sub['sub_id']} {sub['title']} | {r.get('mapped_papers', 0)} | {ev_txt} | {axes_txt} | {r.get('reuse_max', 0)} |"
        )

    lines.extend(['', '## Per-chapter sizing (H2)', ''])
    lines.append('| Chapter | #H3 |')
    lines.append('|---|---:|')
    for s in sections:
        sub_n = len(s.get('subsections') or [])
        lines.append(f"| {s.get('section_id')} {s.get('title')} | {sub_n} |")

    # Flags (bullets only).
    issues: list[str] = []
    if h2_total > 10:
        issues.append(
            f"Outline has many top-level sections (H2={h2_total}); paper-like surveys often stay around 6–8 H2 sections (see `ref/agent-surveys/STYLE_REPORT.md`)."
        )
    if h3_total > 12:
        issues.append(
            f"Outline has many subsections (H3={h3_total}); consider merging adjacent H3s to write fewer, thicker subsections (survey target: <=12)."
        )

    if h3_counts:
        too_many = [s for s in sections if len(s.get('subsections') or []) >= 5]
        if too_many:
            sample = ', '.join([str(s.get('section_id') or '') for s in too_many[:6]])
            issues.append(f"Some chapters have many H3 subsections (>=5): {sample} (risk: thin writing per subsection).")
        too_few = [s for s in sections if 0 < len(s.get('subsections') or []) < 3]
        if too_few:
            sample = ', '.join([str(s.get('section_id') or '') for s in too_few[:6]])
            issues.append(
                f"Some chapters are thin (<3 H3): {sample} (paper-like survey default is closer to ~3 substantive H3s per core chapter, unless scope is intentionally very tight)."
            )

    low_axes = [r for r in rows if int(r.get('axes_total') or 0) and int(r.get('axes_specific') or 0) < 2]
    if low_axes:
        sample = ', '.join([f"{r['sub_id']}" for r in low_axes[:6]])
        issues.append(f"Some H3 briefs still look generic (specific axes <2): {sample}")

    high_reuse = [r for r in rows if int(r.get('reuse_max') or 0) >= 6]
    if high_reuse:
        sample = ', '.join([f"{r['sub_id']}" for r in high_reuse[:6]])
        issues.append(f"Mapping shows high reuse hotspots (a paper reused >=6× within a subsection set): {sample}")

    if issues:
        lines.extend(['', '## Flags (actionable)', ''])
        for it in issues:
            lines.append(f"- {it}")
        lines.extend(
            [
                '',
                '## Suggested next actions (still NO PROSE)',
                '- If reuse hotspots are high: expand `core_set.csv` (increase core size) or rerun `section-mapper` with stronger diversity penalty.',
                '- If axes are generic: regenerate `subsection_briefs.jsonl` after improving notes/evidence bank; avoid copying outline scaffold bullets.',
                '- If evidence is mostly abstract-only: consider `evidence_mode: fulltext` for a smaller subset to strengthen key comparisons.',
            ]
        )

    if not report_frozen:
        atomic_write_text(report_path, "\n".join(lines).rstrip() + "\n")

    cutover_fields = _structure_cutover_fields(
        workspace=workspace,
        state_path=state_path,
        h3_total=h3_total,
        mapping_rows=mapping_rows,
        read_jsonl_fn=read_jsonl,
        load_workspace_pipeline_spec_fn=load_workspace_pipeline_spec,
    )

    state_rec = {
        'generated_at': now_iso_seconds(),
        'outline_sha1': _sha1_text(_read_text(workspace / outline_rel)),
        'mapping_sha1': _sha1_text(_read_text(workspace / mapping_rel)),
        'status': 'skipped_due_to_freeze_marker' if report_frozen else 'generated',
        'h2_sections': h2_total,
        'h2_with_h3': h2_with_h3,
        'h3_subsections': h3_total,
        'h3_per_h2': {'min': h3_min, 'median': h3_med, 'max': h3_max},
        'subsections': len(subsections),
        'mapping_rows': len(mapping_rows),
        'unique_papers': len(usage),
        'top_reuse': [{'paper_id': pid, 'count': cnt} for pid, cnt in top_reuse],
        'flags': issues,
        **cutover_fields,
    }
    _append_jsonl(state_path, state_rec)
    reroute_state = {
        'generated_at': state_rec['generated_at'],
        'structure_phase': state_rec['structure_phase'],
        'h3_status': state_rec['h3_status'],
        'approval_status': state_rec['approval_status'],
        'reroute_target': state_rec['reroute_target'],
        'retry_budget_remaining': state_rec['retry_budget_remaining'],
        'section_binding_gate': state_rec.get('section_binding_gate', ''),
        'section_binding_status_counts': state_rec.get('section_binding_status_counts', {}),
        'section_binding_nonpass_sections': state_rec.get('section_binding_nonpass_sections', []),
        'reroute_reason': state_rec.get('reroute_reason', ''),
        'status': (
            'BLOCKED'
            if state_rec['structure_phase'] == 'binding_blocked'
            else 'REROUTE'
            if state_rec['structure_phase'] == 'binding_reroute'
            else 'READY'
            if state_rec['structure_phase'] == 'decomposed' and state_rec['h3_status'] == 'stable'
            else 'INFO'
        ),
        'flags': issues,
    }
    atomic_write_text(reroute_path, json.dumps(reroute_state, ensure_ascii=False, indent=2).rstrip() + "\n")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
