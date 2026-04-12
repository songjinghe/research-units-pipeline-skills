from __future__ import annotations

import argparse
import re
import shutil
import subprocess
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

    from tooling.common import ensure_dir, parse_semicolon_list

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ["latex/slides/main.pdf", "output/SLIDES_BUILD_REPORT.md"]

    pdf_path = workspace / outputs[0]
    report_path = workspace / (outputs[1] if len(outputs) > 1 else "output/SLIDES_BUILD_REPORT.md")
    tex_path = workspace / "latex" / "slides" / "main.tex"
    if not tex_path.exists():
        _write_report(report_path, ok=False, message=f"Missing input: {tex_path}")
        return 0

    ensure_dir(pdf_path.parent)
    ensure_dir(report_path.parent)

    proc, engine = _compile(tex_path)
    built_pdf = tex_path.parent / "main.pdf"
    ok = proc.returncode == 0 and built_pdf.exists()
    if ok and pdf_path != built_pdf:
        shutil.copy2(built_pdf, pdf_path)

    warnings = _collect_warnings(tex_path.parent, stdout=proc.stdout, stderr=proc.stderr)
    page_count = _pdf_page_count(pdf_path if pdf_path.exists() else built_pdf)
    _write_report(
        report_path,
        ok=ok,
        message=("SUCCESS" if ok else f"{engine} failed (exit {proc.returncode})"),
        stdout=proc.stdout,
        stderr=proc.stderr,
        engine=engine,
        page_count=page_count,
        warnings=warnings,
    )
    return 0 if ok else 2


def _compile(tex_path: Path) -> tuple[subprocess.CompletedProcess[str], str]:
    latexmk = shutil.which("latexmk")
    if latexmk:
        cmd = [
            latexmk,
            "-xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            tex_path.name,
        ]
        proc = subprocess.run(cmd, cwd=str(tex_path.parent), capture_output=True, text=True)
        return proc, "latexmk -xelatex"
    xelatex = shutil.which("xelatex")
    if xelatex:
        proc = subprocess.run(
            [xelatex, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", tex_path.name],
            cwd=str(tex_path.parent),
            capture_output=True,
            text=True,
        )
        return proc, "xelatex"
    return subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="Missing tools: latexmk/xelatex"), "unavailable toolchain"


def _collect_warnings(tex_dir: Path, *, stdout: str, stderr: str) -> dict[str, int]:
    log_path = tex_dir / "main.log"
    log_text = log_path.read_text(encoding="utf-8", errors="ignore") if log_path.exists() else ""
    aux_text = "\n".join([stdout or "", stderr or ""]).strip()
    patterns = {
        "overfull_hbox": r"(?im)^Overfull \\hbox",
        "overfull_vbox": r"(?im)^Overfull \\vbox",
        "missing_character": r"(?im)^Missing character:",
        "latex_warning": r"(?im)^LaTeX Warning:",
        "annotation_out_of_page": r"(?im)^xdvipdfmx:warning:\s+Annotation out of page boundary",
    }
    counts: dict[str, int] = {}
    for key, pat in patterns.items():
        counts[key] = len(re.findall(pat, log_text + "\n" + aux_text))
    return {k: v for k, v in counts.items() if v}


def _pdf_page_count(path: Path) -> int | None:
    if not path.exists():
        return None
    pdfinfo = shutil.which("pdfinfo")
    if not pdfinfo:
        return None
    proc = subprocess.run([pdfinfo, str(path)], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return None
    m = re.search(r"(?im)^Pages:\s+(\d+)\b", proc.stdout or "")
    return int(m.group(1)) if m else None


def _write_report(
    path: Path,
    *,
    ok: bool,
    message: str,
    stdout: str = "",
    stderr: str = "",
    engine: str = "",
    page_count: int | None = None,
    warnings: dict[str, int] | None = None,
) -> None:
    from tooling.common import atomic_write_text, ensure_dir

    ensure_dir(path.parent)
    lines = [
        "# Slides build report",
        "",
        f"- Status: {'PASS' if ok else 'FAIL'}",
        f"- Engine: {engine or 'unknown'}",
        f"- Message: {message}",
        f"- Output: `latex/slides/main.pdf`",
        f"- Page count: {page_count if page_count is not None else 'unknown'}",
        "",
        "## Warning summary",
    ]
    if warnings:
        lines.extend([f"- {key}: {value}" for key, value in sorted(warnings.items())])
    else:
        lines.append("- (none)")
    lines.extend(
        [
            "",
            "## Stdout tail",
            "```text",
            "\n".join((stdout or "").splitlines()[-40:]) or "(empty)",
            "```",
            "",
            "## Stderr tail",
            "```text",
            "\n".join((stderr or "").splitlines()[-40:]) or "(empty)",
            "```",
        ]
    )
    atomic_write_text(path, "\n".join(lines).rstrip() + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
