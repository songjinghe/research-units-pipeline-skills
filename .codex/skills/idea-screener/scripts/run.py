from __future__ import annotations

import argparse
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
    from tooling.ideation import IdeaCard, parse_idea_brief, read_jsonl, score_idea_cards, screening_table_markdown, write_jsonl, write_markdown

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ["output/IDEA_SCREENING_TABLE.md"]
    out_rel = outputs[0] if outputs else "output/IDEA_SCREENING_TABLE.md"
    out_path = workspace / out_rel
    jsonl_path = out_path.with_suffix('.jsonl')

    brief = parse_idea_brief(workspace / 'output' / 'IDEA_BRIEF.md')
    cards_path = workspace / 'output' / 'IDEA_POOL.jsonl'
    raw_cards = [r for r in read_jsonl(cards_path) if isinstance(r, dict)]
    cards = [IdeaCard(**r) for r in raw_cards]
    rows = score_idea_cards(cards, focus_clusters=brief.get('focus_clusters') or [])
    top_n = 15
    queries_path = workspace / 'queries.md'
    if queries_path.exists():
        import re
        q = queries_path.read_text(encoding='utf-8', errors='ignore')
        m = re.search(r'(?im)^-\s*idea_screen_top_n\s*:\s*"?([0-9]+)"?\s*$', q)
        if m:
            top_n = int(m.group(1))
    rows = rows[: max(12, top_n)]
    write_markdown(out_path, screening_table_markdown(rows))
    write_jsonl(jsonl_path, [r.__dict__ for r in rows])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
