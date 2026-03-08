from __future__ import annotations

import argparse
import re
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


def _clean_title(title: str) -> str:
    s = str(title or '').strip()
    s = re.sub(r'\s+', ' ', s)
    return s


def _content_bridge(cur: dict[str, Any], nxt: dict[str, Any]) -> str:
    cur_title = _clean_title(cur.get('title') or 'the previous subsection')
    nxt_title = _clean_title(nxt.get('title') or 'the next subsection')
    cur_terms = [str(x).strip().replace('/', ' and ') for x in (cur.get('bridge_terms') or []) if str(x).strip()]
    nxt_terms = [str(x).strip().replace('/', ' and ') for x in (nxt.get('bridge_terms') or []) if str(x).strip()]
    hook = str(nxt.get('contrast_hook') or cur.get('contrast_hook') or '').strip()
    term_a = cur_terms[0] if cur_terms else (hook or 'the same comparison lens')
    term_b = nxt_terms[0] if nxt_terms else nxt_title.lower()
    cur_thesis = str(cur.get('thesis') or '').strip()
    nxt_thesis = str(nxt.get('thesis') or '').strip()

    if cur_thesis and nxt_thesis:
        return (
            f"{cur_title} frames the central trade-off around {term_a}, and {nxt_title.lower()} shows how that trade-off "
            f"is realized through {term_b}."
        )
    return (
        f"{cur_title} defines the core comparison lens around {term_a}, and {nxt_title.lower()} makes that lens concrete "
        f"through {term_b}."
    )


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

    from tooling.common import atomic_write_text, ensure_dir, load_yaml, parse_semicolon_list
    from tooling.quality_gate import check_unit_outputs, write_quality_report

    workspace = Path(args.workspace).resolve()
    unit_id = str(args.unit_id or 'U098').strip() or 'U098'

    inputs = parse_semicolon_list(args.inputs)
    outputs = parse_semicolon_list(args.outputs) or ['outline/transitions.md']
    out_rel = outputs[0] if outputs else 'outline/transitions.md'
    out_path = workspace / out_rel
    ensure_dir(out_path.parent)

    outline_rel = next((p for p in inputs if p.endswith('outline.yml')), 'outline/outline.yml')
    briefs_rel = next((p for p in inputs if p.endswith('subsection_briefs.jsonl')), 'outline/subsection_briefs.jsonl')

    outline = load_yaml(workspace / outline_rel) if (workspace / outline_rel).exists() else []
    briefs = {str(r.get('sub_id') or '').strip(): r for r in _load_jsonl(workspace / briefs_rel) if str(r.get('sub_id') or '').strip()}

    lines: list[str] = []
    if isinstance(outline, list):
        for sec in outline:
            if not isinstance(sec, dict):
                continue
            subs = [sub for sub in (sec.get('subsections') or []) if isinstance(sub, dict)]
            for idx in range(len(subs) - 1):
                left = subs[idx]
                right = subs[idx + 1]
                left_id = str(left.get('id') or '').strip()
                right_id = str(right.get('id') or '').strip()
                if not left_id or not right_id:
                    continue
                left_rec = briefs.get(left_id) or left
                right_rec = briefs.get(right_id) or right
                lines.append(f"- {left_id} -> {right_id}: {_content_bridge(left_rec, right_rec)}")

    atomic_write_text(out_path, '\n'.join(lines).rstrip() + ('\n' if lines else ''))

    issues = check_unit_outputs(skill='transition-weaver', workspace=workspace, outputs=[out_rel])
    if issues:
        write_quality_report(workspace=workspace, unit_id=unit_id, skill='transition-weaver', issues=issues)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
