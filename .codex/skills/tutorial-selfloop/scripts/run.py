from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PREFACE_GROUPS = [
    ("who this is for", "受众"),
    ("prerequisites", "先修"),
    ("what you will learn", "学习目标"),
]
MODULE_REQUIREMENTS = [
    ("why it matters", "为什么重要"),
    ("key idea", "核心概念"),
    ("worked example", "示例"),
    ("check yourself", "练习"),
    ("source notes", "来源"),
]


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

    from tooling.common import atomic_write_text, ensure_dir, parse_semicolon_list

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ["output/TUTORIAL_SELFLOOP_TODO.md"]
    report_path = workspace / outputs[0]
    ensure_dir(report_path.parent)

    tutorial_path = workspace / "output" / "TUTORIAL.md"
    if not tutorial_path.exists():
        _write_report(report_path, status="FAIL", issues=["Missing `output/TUTORIAL.md`."])
        return 2

    text = tutorial_path.read_text(encoding="utf-8", errors="ignore")
    low = text.lower()
    issues: list[str] = []

    for en, zh in REQUIRED_PREFACE_GROUPS:
        if en not in low and zh not in text:
            issues.append(f"Tutorial is missing the reader-orientation section for `{en}`.")

    sections = _split_h2_sections(text)
    module_sections = [(title, body) for title, body in sections if title.lower() not in {
        "who this is for",
        "prerequisites",
        "what you will learn",
        "how to use this tutorial",
        "further reading",
    }]
    if not module_sections:
        issues.append("Tutorial has no real modules (`## ...`) beyond orientation sections.")

    for title, body in module_sections:
        block = body.lower()
        missing = [label for label, zh in MODULE_REQUIREMENTS if label not in block and zh not in body]
        if missing:
            issues.append(f"Module `{title}` is missing teaching sections: {', '.join(missing)}.")

    status = "PASS" if not issues else "FAIL"
    _write_report(report_path, status=status, issues=issues)
    return 0 if not issues else 2


def _split_h2_sections(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_title = ""
    current_lines: list[str] = []
    for line in (text or "").splitlines():
        if line.startswith("## "):
            if current_title:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = line[3:].strip()
            current_lines = []
            continue
        if current_title:
            current_lines.append(line)
    if current_title:
        sections.append((current_title, "\n".join(current_lines).strip()))
    return sections


def _write_report(path: Path, *, status: str, issues: list[str]) -> None:
    from tooling.common import atomic_write_text

    lines = [
        "# Tutorial self-loop",
        "",
        f"- Status: {status}",
        "- Deliverable: `output/TUTORIAL.md`",
        "",
        "## Summary",
        "- The tutorial gate checks whether the deliverable still reads like a teachable tutorial rather than a generic long-form article.",
        "",
        "## Remaining blockers",
    ]
    if issues:
        lines.extend([f"- {issue}" for issue in issues])
        lines.extend(["", "## Next step", "- Fix the missing teaching sections in `output/TUTORIAL.md` and rerun this unit."])
    else:
        lines.extend(["- (none)", "", "## Next step", "- Proceed to article/slides delivery."])
    atomic_write_text(path, "\n".join(lines).rstrip() + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
