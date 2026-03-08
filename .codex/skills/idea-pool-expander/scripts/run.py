from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


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
    from tooling.ideation import idea_pool_markdown, parse_idea_brief, read_jsonl, rows_to_idea_cards, write_jsonl, write_markdown

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ["output/IDEA_POOL.md"]
    out_rel = outputs[0] if outputs else "output/IDEA_POOL.md"
    out_path = workspace / out_rel
    jsonl_path = out_path.with_suffix('.jsonl')

    brief = parse_idea_brief(workspace / 'output' / 'IDEA_BRIEF.md')
    opp_json = workspace / 'output' / 'IDEA_OPPORTUNITY_TABLE.jsonl'
    rows = [r for r in read_jsonl(opp_json) if isinstance(r, dict)]
    if not rows:
        raise SystemExit('Missing opportunity rows; run idea-opportunity-mapper first')

    pool_max = int(brief.get('pool_max') or 80)
    pool_min = int(brief.get('pool_min') or 60)
    rep_rows = []
    seen_clusters = set()
    for row in rows:
        cluster = str(row.get('cluster') or '').strip()
        if cluster in seen_clusters:
            continue
        seen_clusters.add(cluster)
        rep_rows.append(row)

    seed_rows = list(rep_rows)
    if len(seed_rows) * 8 < pool_min:
        seen_ids = {str(r.get('opportunity_id') or '') for r in seed_rows}
        for row in rows:
            oid = str(row.get('opportunity_id') or '')
            if oid in seen_ids:
                continue
            seed_rows.append(row)
            seen_ids.add(oid)
            if len(seed_rows) * 8 >= pool_min:
                break

    cards = rows_to_idea_cards(seed_rows, focus_clusters=brief.get('focus_clusters') or [])
    cards = cards[: max(pool_min, min(pool_max, len(cards)))]
    write_markdown(out_path, idea_pool_markdown(cards))
    write_jsonl(jsonl_path, [c.__dict__ for c in cards])

    # Legacy compatibility: if asked to write IDEA_SHORTLIST.md, seed it with the pool section only.
    if out_path.name == 'IDEA_SHORTLIST.md':
        write_markdown(out_path, idea_pool_markdown(cards))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
