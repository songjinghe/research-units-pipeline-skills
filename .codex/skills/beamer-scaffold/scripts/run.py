from __future__ import annotations

import argparse
import re
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

    from tooling.common import atomic_write_text, ensure_dir, parse_semicolon_list

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ["latex/slides/main.tex"]
    out_path = workspace / outputs[0]
    ensure_dir(out_path.parent)

    tutorial_path = workspace / "output" / "TUTORIAL.md"
    if not tutorial_path.exists():
        raise SystemExit(f"Missing input: {tutorial_path}")

    md = tutorial_path.read_text(encoding="utf-8", errors="ignore")
    title = _read_first_h1(md) or "Tutorial Slides"
    sections = _split_h2_sections(md)
    preface, modules = _partition_sections(sections)

    tex_lines = [
        r"\documentclass[aspectratio=169]{beamer}",
        r"\usetheme{Madrid}",
        r"\usepackage{fontspec}",
        r"\usepackage{newunicodechar}",
        r"\newunicodechar{π}{\ensuremath{\pi}}",
        r"\usepackage{hyperref}",
        r"\hypersetup{colorlinks=true,urlcolor=blue}",
        rf"\title{{{_escape_latex(title)}}}",
        r"\author{}",
        r"\date{\today}",
        r"\begin{document}",
        r"\frame{\titlepage}",
        r"\begin{frame}{Roadmap}",
        r"\tableofcontents",
        r"\end{frame}",
        "",
    ]

    for title, body in preface:
        tex_lines.extend(_render_frame(title, body))

    for section_title, body in modules:
        tex_lines.append(rf"\section{{{_escape_latex(section_title)}}}")
        h3_blocks = _split_h3_blocks(body)
        if not h3_blocks:
            tex_lines.extend(_render_frame(section_title, body))
            continue
        for subtitle, subbody in h3_blocks:
            tex_lines.extend(_render_frame(f"{section_title}: {subtitle}", subbody))

    tex_lines.extend([r"\end{document}", ""])
    atomic_write_text(out_path, "\n".join(tex_lines))
    return 0


def _read_first_h1(md: str) -> str:
    for line in (md or "").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def _split_h2_sections(md: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_title = ""
    current_lines: list[str] = []
    for raw in (md or "").splitlines():
        if raw.startswith("## "):
            if current_title:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = raw[3:].strip()
            current_lines = []
            continue
        if current_title:
            current_lines.append(raw)
    if current_title:
        sections.append((current_title, "\n".join(current_lines).strip()))
    return sections


def _partition_sections(sections: list[tuple[str, str]]) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    preface_titles = {"who this is for", "prerequisites", "what you will learn", "how to use this tutorial"}
    preface: list[tuple[str, str]] = []
    modules: list[tuple[str, str]] = []
    for title, body in sections:
        if title.lower() in preface_titles:
            preface.append((title, body))
        else:
            modules.append((title, body))
    return preface, modules


def _split_h3_blocks(body: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    current_title = ""
    current_lines: list[str] = []
    for raw in (body or "").splitlines():
        if raw.startswith("### "):
            if current_title:
                blocks.append((current_title, "\n".join(current_lines).strip()))
            current_title = raw[4:].strip()
            current_lines = []
            continue
        if current_title:
            current_lines.append(raw)
    if current_title:
        blocks.append((current_title, "\n".join(current_lines).strip()))
    return blocks


def _render_frame(title: str, body: str) -> list[str]:
    bullets = _body_to_bullets(body)
    if not bullets:
        bullets = ["See the tutorial article for the full explanation."]
    lines = [rf"\begin{{frame}}{{{_escape_latex(title)}}}", r"\begin{itemize}"]
    for bullet in bullets[:6]:
        lines.append(r"\item " + _convert_inline(_escape_latex(bullet)))
    lines.extend([r"\end{itemize}", r"\end{frame}", ""])
    return lines


def _body_to_bullets(body: str) -> list[str]:
    bullets: list[str] = []
    for raw in (body or "").splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("### "):
            continue
        if stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
            continue
        if stripped.startswith("Source: "):
            continue
        if len(stripped) <= 140:
            bullets.append(stripped)
            continue
        parts = re.split(r"(?<=[.!?])\s+", stripped)
        bullets.extend([part.strip() for part in parts if part.strip()])
    deduped: list[str] = []
    for bullet in bullets:
        if bullet not in deduped:
            deduped.append(bullet)
    return deduped


def _escape_latex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def _convert_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", lambda m: r"\texttt{" + m.group(1) + "}", text)
    text = re.sub(r"\*\*([^*]+)\*\*", lambda m: r"\textbf{" + m.group(1) + "}", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", lambda m: r"\emph{" + m.group(1) + "}", text)
    return text


if __name__ == "__main__":
    raise SystemExit(main())
