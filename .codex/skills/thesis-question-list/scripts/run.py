from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    target = workspace / "codex_md" / "question_list.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text(
            "# 本轮问题单\n\n"
            "## 本轮目标\n"
            "- \n\n"
            "## 问题列表\n"
            "| 优先级 | 涉及章节/文件 | 问题 | 为什么是问题 | 修改方向 | 多 agent 讨论 | 验收标准 |\n"
            "|---|---|---|---|---|---|---|\n",
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
