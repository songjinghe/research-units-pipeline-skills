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

    from tooling.common import load_yaml, parse_semicolon_list, write_jsonl
    from tooling.tutorial_workflows import build_module_source_coverage

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs) or ["outline/module_plan.yml"]
    outputs = parse_semicolon_list(args.outputs) or ["outline/source_coverage.jsonl"]
    plan_path = workspace / inputs[0]
    out_path = workspace / outputs[0]

    plan = load_yaml(plan_path)
    if not isinstance(plan, dict):
        raise SystemExit(f"Invalid module plan: {plan_path}")
    records = build_module_source_coverage(workspace, plan)
    write_jsonl(out_path, records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
