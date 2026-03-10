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
    from tooling.ideation import IdeaSignal, collect_note_index, direction_pool_markdown, parse_idea_brief, read_jsonl, signals_to_direction_cards, write_jsonl, write_markdown

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ["output/trace/IDEA_DIRECTION_POOL.md"]
    out_rel = outputs[0] if outputs else "output/trace/IDEA_DIRECTION_POOL.md"
    out_path = workspace / out_rel
    jsonl_path = out_path.with_suffix('.jsonl')

    brief = parse_idea_brief(workspace / 'output' / 'trace' / 'IDEA_BRIEF.md')
    signal_json = workspace / 'output' / 'trace' / 'IDEA_SIGNAL_TABLE.jsonl'
    raw_signals = [r for r in read_jsonl(signal_json) if isinstance(r, dict)]
    if not raw_signals:
        raise SystemExit('Missing signal rows; run idea-signal-mapper first')

    signals = [IdeaSignal(**row) for row in raw_signals]
    note_index = collect_note_index(workspace / 'papers' / 'paper_notes.jsonl')
    cards = signals_to_direction_cards(
        signals,
        note_index=note_index,
        focus_clusters=brief.get('focus_clusters') or [],
        pool_min=int(brief.get('direction_pool_min') or 12),
        pool_max=int(brief.get('direction_pool_max') or 24),
    )
    write_markdown(out_path, direction_pool_markdown(cards))
    write_jsonl(jsonl_path, [c.__dict__ for c in cards])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
