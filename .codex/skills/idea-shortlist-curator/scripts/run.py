from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _group_candidates(
    screen_rows: list[dict[str, object]],
    *,
    pool_lookup: dict[str, dict[str, object]],
    shortlist_size: int,
) -> list[dict[str, object]]:
    chosen: list[dict[str, object]] = []
    used_clusters: set[str] = set()
    used_types: set[str] = set()
    used_programs: set[str] = set()
    used_ids: set[str] = set()
    diversity_target = min(3, shortlist_size)
    for row in screen_rows:
        direction_id = str(row.get('direction_id') or '').strip()
        card = pool_lookup.get(direction_id) or {}
        cluster = str(card.get('cluster') or row.get('cluster') or '').strip()
        direction_type = str(card.get('direction_type') or row.get('direction_type') or '').strip()
        program_kind = str(card.get('program_kind') or '').strip()
        if len(chosen) >= diversity_target:
            break
        if direction_id in used_ids:
            continue
        if (
            cluster not in used_clusters
            or direction_type not in used_types
            or (program_kind and program_kind not in used_programs)
        ):
            chosen.append(row)
            used_clusters.add(cluster)
            used_types.add(direction_type)
            if program_kind:
                used_programs.add(program_kind)
            used_ids.add(direction_id)
    for row in screen_rows:
        direction_id = str(row.get('direction_id') or '').strip()
        if direction_id in used_ids:
            continue
        chosen.append(row)
        used_ids.add(direction_id)
        if len(chosen) >= shortlist_size:
            break
    return chosen[:shortlist_size]


def _risk_note(card: dict[str, object]) -> str:
    evidence = str(card.get('evidence_confidence') or '')
    program_kind = str(card.get('program_kind') or '').lower()
    confound = str(card.get('main_confound') or 'the main confound')
    if evidence.startswith('low'):
        return 'the literature anchor is still abstract-first'
    if 'protocol' in program_kind:
        return 'the decisive test is still somewhat protocol-sensitive'
    if 'budget' in program_kind:
        return f'normalizing {confound} will take a heavier control argument'
    return f'the main risk is still whether {confound} has already been controlled by prior work'


def _rank_reason(idx: int, cards: list[dict[str, object]], card: dict[str, object]) -> str:
    title = str(card.get('title') or 'this direction')
    cluster = str(card.get('cluster') or 'this area').lower()
    program_kind = str(card.get('program_kind') or 'research')
    contribution_shape = str(card.get('contribution_shape') or card.get('academic_value') or 'a stronger research contribution').lower()
    main_confound = str(card.get('main_confound') or 'the main confound')
    time_to_clarity = str(card.get('time_to_clarity') or 'medium')
    risk_note = _risk_note(card)
    if idx == 0:
        return (
            f"Leads because it offers the fastest path to a decisive {program_kind} result in {cluster}, "
            f"and because it has the clearest path to a thesis-sized contribution if the control holds."
        )
    leader = cards[0]
    leader_title = str(leader.get('title') or 'the current #1 direction')
    if idx == 1:
        return (
            f"Ranks behind {leader_title} because isolating {main_confound} is slower or harder to defend, "
            f"but it still stays high because the payoff remains thesis-sized if the control survives."
        )
    return (
        f"Stays in the lead set because it opens a distinct {program_kind} wedge, "
        f"but it trails the first two because {risk_note} and the time-to-clarity is {time_to_clarity}."
    )


def _prioritized_reason(card: dict[str, object]) -> str:
    return f"kept in the lead set because {_risk_note(card).replace('the ', '').replace('still ', '')} is outweighed by its thesis upside."


def _deferred_reason(card: dict[str, object], leads: list[dict[str, object]]) -> str:
    lead_clusters = {str(item.get('cluster') or '').strip() for item in leads}
    lead_programs = {str(item.get('program_kind') or '').strip() for item in leads}
    cluster = str(card.get('cluster') or '').strip()
    program_kind = str(card.get('program_kind') or '').strip()
    evidence = str(card.get('evidence_confidence') or '')
    if program_kind and program_kind in lead_programs:
        return f"overlaps the current lead set's {program_kind} wedge, but with a weaker prior-work gap."
    if cluster and cluster in lead_clusters:
        return 'sits in a cluster already represented in the lead set, while its first decisive control currently looks slower.'
    if evidence.startswith('low'):
        return 'is still promising, but the literature anchor is too abstract-first for lead-set rank right now.'
    return 'is still promising, but it currently looks slower to turn into a decisive first reading/probe cycle.'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--unit-id", default="")
    parser.add_argument("--inputs", default="")
    parser.add_argument("--outputs", default="")
    parser.add_argument("--checkpoint", default="")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root))

    from tooling.common import parse_semicolon_list
    from tooling.ideation import parse_idea_brief, read_jsonl, shortlist_markdown, uniq_keep_order, write_jsonl, write_markdown

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ["output/trace/IDEA_SHORTLIST.md"]
    out_rel = outputs[0] if outputs else "output/trace/IDEA_SHORTLIST.md"
    out_path = workspace / out_rel
    jsonl_path = out_path.with_suffix('.jsonl')

    brief = parse_idea_brief(workspace / 'output' / 'trace' / 'IDEA_BRIEF.md')
    shortlist_size = int(brief.get('shortlist_size') or 5)
    pool = {str(r.get('direction_id') or ''): r for r in read_jsonl(workspace / 'output' / 'trace' / 'IDEA_DIRECTION_POOL.jsonl') if isinstance(r, dict)}
    screened = [r for r in read_jsonl(workspace / 'output' / 'trace' / 'IDEA_SCREENING_TABLE.jsonl') if isinstance(r, dict)]
    screened.sort(key=lambda r: (-float(r.get('total_score') or 0.0), str(r.get('direction_id') or '')))
    chosen = _group_candidates(screened, pool_lookup=pool, shortlist_size=shortlist_size)

    enriched: list[dict[str, object]] = []
    for row in chosen:
        did = str(row.get('direction_id') or '')
        card = dict(pool.get(did) or {})
        card['_screen_row'] = row
        enriched.append(card)

    records: list[dict[str, object]] = []
    for idx, card in enumerate(enriched, start=1):
        row = dict(card.get('_screen_row') or {})
        pids = uniq_keep_order(card.get('paper_ids') or [])[:4]
        record = {
            'rank': idx,
            'direction_id': card.get('direction_id'),
            'cluster': card.get('cluster'),
            'direction_type': card.get('direction_type'),
            'title': card.get('title'),
            'focus_axis': card.get('focus_axis'),
            'main_confound': card.get('main_confound'),
            'program_kind': card.get('program_kind'),
            'contribution_shape': card.get('contribution_shape') or card.get('academic_value'),
            'time_to_clarity': card.get('time_to_clarity') or 'medium',
            'one_line_thesis': card.get('one_line_thesis'),
            'why_interesting': card.get('why_interesting'),
            'literature_suggests': card.get('literature_suggests') or [],
            'closest_prior_gap': card.get('closest_prior_gap') or [],
            'missing_piece': card.get('missing_piece'),
            'possible_variants': card.get('possible_variants') or [],
            'academic_value': card.get('academic_value'),
            'first_probes': card.get('first_probes') or [],
            'what_counts_as_insight': card.get('what_counts_as_insight'),
            'weakness_conditions': card.get('weakness_conditions') or [],
            'kill_criteria': card.get('kill_criteria') or card.get('what_would_change_mind') or [],
            'what_would_change_mind': card.get('what_would_change_mind') or [],
            'best_fit': card.get('best_fit'),
            'why_this_ranks_here': '',
            'evidence_confidence': card.get('evidence_confidence') or 'low-medium',
            'paper_ids': pids,
            'signal_ids': card.get('signal_ids') or [],
            'anchor_reading_notes': card.get('anchor_reading_notes') or [],
            'why_prioritized': '',
            'why_not_prioritized': '',
            '_score_total': row.get('total_score'),
            '_screen_rationale': row.get('rationale'),
        }
        records.append(record)

    for idx, record in enumerate(records):
        record['why_this_ranks_here'] = _rank_reason(idx, records, record)
        record['why_prioritized'] = _prioritized_reason(record)

    leads = records[:3]
    for record in records[3:]:
        record['why_not_prioritized'] = _deferred_reason(record, leads)

    for record in records:
        record.pop('_score_total', None)
        record.pop('_screen_rationale', None)

    write_markdown(out_path, shortlist_markdown(records))
    write_jsonl(jsonl_path, records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
