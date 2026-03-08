from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _group_candidates(screen_rows: list[dict[str, Any]], *, shortlist_size: int) -> list[dict[str, Any]]:
    chosen: list[dict[str, Any]] = []
    used_clusters: set[str] = set()
    used_types: set[str] = set()
    for row in screen_rows:
        cluster = str(row.get('cluster') or '').strip()
        idea_type = str(row.get('idea_type') or '').strip()
        if len(chosen) < 3:
            if cluster not in used_clusters or idea_type not in used_types:
                chosen.append(row)
                used_clusters.add(cluster)
                used_types.add(idea_type)
                continue
            # During the diversity-forcing phase, skip rows that add neither a new cluster nor a new idea type.
            continue
        if len(chosen) < shortlist_size:
            chosen.append(row)
        if len(chosen) >= shortlist_size:
            break
    return chosen[:shortlist_size]



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
    from tooling.ideation import collect_note_index, parse_idea_brief, read_core_set, read_jsonl, uniq_keep_order, write_jsonl, write_markdown

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ["output/IDEA_SHORTLIST.md"]
    out_rel = outputs[0] if outputs else "output/IDEA_SHORTLIST.md"
    out_path = workspace / out_rel
    jsonl_path = out_path.with_suffix('.jsonl')

    brief = parse_idea_brief(workspace / 'output' / 'IDEA_BRIEF.md')
    shortlist_size = int(brief.get('shortlist_size') or 7)
    core = {r['paper_id']: r for r in read_core_set(workspace / 'papers' / 'core_set.csv') if r.get('paper_id')}
    notes = collect_note_index(workspace / 'papers' / 'paper_notes.jsonl')
    pool = {str(r.get('idea_id') or ''): r for r in read_jsonl(workspace / 'output' / 'IDEA_POOL.jsonl') if isinstance(r, dict)}
    screened = [r for r in read_jsonl(workspace / 'output' / 'IDEA_SCREENING_TABLE.jsonl') if isinstance(r, dict)]
    screened.sort(key=lambda r: (-float(r.get('total_score') or 0.0), str(r.get('idea_id') or '')))
    chosen = _group_candidates(screened, shortlist_size=shortlist_size)

    records: list[dict[str, Any]] = []
    lines: list[str] = ["# IDEA_SHORTLIST", "", "## Final Shortlist", ""]
    for idx, row in enumerate(chosen, start=1):
        pid = str(row.get('idea_id') or '')
        card = pool.get(pid) or {}
        pids = uniq_keep_order(card.get('paper_ids') or [])[:4]
        titles = [core.get(x, {}).get('title', x) for x in pids]
        gap_note = notes.get(pids[0], {}) if pids else {}
        limit = ''
        if isinstance(gap_note.get('limitations'), list) and gap_note.get('limitations'):
            limit = str(gap_note['limitations'][0]).strip()
        title = str(card.get('problem') or pid).rstrip('.')
        idea_title = title[:1].upper() + title[1:]
        why_now = str(card.get('why_now') or f"Recent papers in {row.get('cluster')} already expose a reproducible gap, but the current literature still leaves the first bounded intervention under-specified.")
        testbed = str(card.get('candidate_wedge') or f"Start with one public task family plus one stress variable tied to {row.get('cluster').lower()} (for example, protocol setting, tool ambiguity, or recovery constraint).")
        artifact = f"A minimal artifact should be a small benchmark slice, harness, evaluator, or reporting card that makes the gap in {row.get('cluster').lower()} executable within one week."
        positive = f"A strong positive signal would be a stable ranking change, a clearer diagnosis, or a measurable reliability gain tied directly to {str(card.get('sharp_gap') or row.get('cluster')).lower()}."
        negative = f"A useful negative result would still show that the proposed variable barely changes outcomes, which would narrow the true source of {str(card.get('gap_type') or 'the gap').replace('_',' ')}."
        confound = limit or 'The main confound is that benchmark engineering may dominate the observed effect if the treatment variable is not isolated cleanly.'
        kill = f"Kill the idea if the first prototype cannot isolate one controllable variable in {row.get('cluster').lower()} or if the new setup adds reporting overhead without new signal."
        record = {
            'rank': idx,
            'title': idea_title,
            'idea_id': pid,
            'cluster': row.get('cluster'),
            'idea_type': row.get('idea_type'),
            'problem': card.get('problem'),
            'sharp_gap': str(card.get('sharp_gap') or f"The current evidence around {row.get('cluster').lower()} still leaves one controllable variable under-tested, which makes comparison unstable."),
            'closest_3': pids[:3],
            'closest_3_titles': titles[:3],
            'delta': [
                f"Makes the gap in {row.get('cluster').lower()} experimentally explicit instead of leaving it as a benchmark caveat.",
                f"Uses {row.get('operator').lower()} as the organizing intervention rather than only as framing.",
            ],
            'non_delta': [
                'Not a new foundation model.',
                'Not a claim that all current benchmarks are invalid.',
            ],
            'why_now': why_now,
            'concrete_testbed': testbed,
            'minimal_artifact': artifact,
            'strong_positive_signal': positive,
            'interesting_negative_result': negative,
            'main_confound': confound,
            'kill_criterion': kill,
            'evidence_anchors': pids,
        }
        records.append(record)
        lines.extend([
            f"### Idea {idx}. {idea_title}",
            f"- Cluster: {row.get('cluster')}",
            f"- Idea type: {row.get('idea_type')}",
            f"- Problem: {card.get('problem')}",
            f"- Sharp gap: {record['sharp_gap']}",
            f"- Closest-3: " + ', '.join(f"`{x}` ({core.get(x, {}).get('title', x)})" for x in pids[:3]),
            "- Delta:",
            f"  - {record['delta'][0]}",
            f"  - {record['delta'][1]}",
            "- Non-Delta:",
            f"  - {record['non_delta'][0]}",
            f"  - {record['non_delta'][1]}",
            f"- Why now: {why_now}",
            f"- Concrete testbed: {testbed}",
            f"- Minimal artifact: {artifact}",
            f"- Strong positive signal: {positive}",
            f"- Interesting negative result: {negative}",
            f"- Main confound: {confound}",
            f"- Kill criterion: {kill}",
            f"- Evidence anchors: " + ', '.join(f"`{x}`" for x in pids),
            "",
        ])
    lines.extend([
        "## Selection Rationale",
        "",
        "- The shortlist prioritizes ideas that are bounded, evidence-anchored, and still likely to change conclusions rather than merely restating benchmark hygiene.",
        "- Diversity is enforced across clusters and idea types before the final ranking is applied.",
        "",
    ])
    write_markdown(out_path, '\n'.join(lines))
    write_jsonl(jsonl_path, records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
