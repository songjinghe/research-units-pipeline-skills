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

    repo_root = Path(__file__).resolve()
    for _ in range(10):
        if (repo_root / "AGENTS.md").exists():
            break
        parent = repo_root.parent
        if parent == repo_root:
            break
        repo_root = parent
    sys.path.insert(0, str(repo_root))

    from tooling.common import load_workspace_pipeline_spec, parse_semicolon_list
    from tooling.ideation import DirectionCard, read_jsonl, resolve_idea_contract, score_direction_cards, screening_table_markdown, write_jsonl, write_markdown

    workspace = Path(args.workspace).resolve()
    if load_workspace_pipeline_spec(workspace) is None:
        raise SystemExit('Missing or invalid active pipeline contract; fix PIPELINE.lock.md and pipeline metadata before ideation C4.')
    outputs = parse_semicolon_list(args.outputs) or ["output/trace/IDEA_SCREENING_TABLE.md"]
    out_rel = outputs[0] if outputs else "output/trace/IDEA_SCREENING_TABLE.md"
    out_path = workspace / out_rel
    jsonl_path = out_path.with_suffix('.jsonl')

    try:
        contract = resolve_idea_contract(workspace)
    except Exception as exc:
        raise SystemExit(f'Invalid ideation runtime contract: {exc}')
    if not contract.get('focus_clusters'):
        raise SystemExit('Missing focus clusters; complete C2 approval before screening directions.')
    cards_path = workspace / 'output' / 'trace' / 'IDEA_DIRECTION_POOL.jsonl'
    raw_cards = [r for r in read_jsonl(cards_path) if isinstance(r, dict)]
    cards = [DirectionCard(**r) for r in raw_cards]
    rows = score_direction_cards(
        cards,
        focus_clusters=contract.get('focus_clusters') or [],
        keep_rank_max=int(contract['keep_rank_max']),
        maybe_rank_max=int(contract['maybe_rank_max']),
        score_weights=dict(contract['score_weights']),
    )

    top_n = int(contract['idea_screen_top_n'])
    rows = rows[: max(1, top_n)]
    write_markdown(out_path, screening_table_markdown(rows))
    write_jsonl(jsonl_path, [r.__dict__ for r in rows])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
