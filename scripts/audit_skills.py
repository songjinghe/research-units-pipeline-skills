from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_DIR = REPO_ROOT / ".codex" / "skills"
TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".sh",
    ".js",
    ".ts",
    ".json",
    ".yml",
    ".yaml",
    ".txt",
}
SEVERITY_ORDER = {"INFO": 10, "WARN": 20, "ERROR": 30}

GENERIC_DOMAIN_PATTERNS = (
    re.compile(r"\bLLM agents\b", re.IGNORECASE),
    re.compile(r"\bLarge language model agents?\b", re.IGNORECASE),
)
PIPELINE_VOICE_PATTERNS = (
    re.compile(r"\bthis pipeline aims\b", re.IGNORECASE),
    re.compile(r"\bacross the pipeline\b", re.IGNORECASE),
)
ELLIPSIS_PATTERNS = (
    re.compile(r"…"),
    re.compile(r"\.\.\. \([0-9]+ more\)", re.IGNORECASE),
    re.compile(r"\.\.\. \(N more\)", re.IGNORECASE),
    re.compile(r"\.\.\."),
)
SCRIPT_REFERENCE_TOKENS = (
    "scripts/",
    "run.py",
    "helper script",
    "bootstrap script",
    "quick start",
    "all options",
    "## script",
    "### script",
)


@dataclass(frozen=True)
class Finding:
    severity: str
    rule_id: str
    skill: str
    path: str
    line: int
    message: str
    excerpt: str


@dataclass(frozen=True)
class ScanStats:
    skills_scanned: int
    files_scanned: int


@dataclass(frozen=True)
class SkillSummary:
    name: str
    skill_md: Path | None
    script_files: list[Path]
    script_nonempty_lines: int


def main() -> int:
    parser = argparse.ArgumentParser(description="Static auditor for repository skills under `.codex/skills/**`.")
    parser.add_argument(
        "--skills-dir",
        default=str(DEFAULT_SKILLS_DIR),
        help="Skills root to scan (default: repo `.codex/skills`).",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default: text).",
    )
    parser.add_argument(
        "--fail-on",
        choices=("NONE", "ERROR", "WARN", "INFO"),
        default="WARN",
        help="Exit 2 if findings at or above this severity exist (default: WARN).",
    )
    parser.add_argument("--report", default="", help="Optional report output path.")
    args = parser.parse_args()

    skills_dir = Path(args.skills_dir).resolve()
    if not skills_dir.exists():
        raise SystemExit(f"Skills directory not found: {skills_dir}")

    findings, stats = audit_skills(skills_dir)
    rendered = render_report(findings=findings, stats=stats, fmt=args.format)

    if args.report:
        report_path = Path(args.report).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(rendered, encoding="utf-8")

    sys.stdout.write(rendered)
    if args.format == "text" and not rendered.endswith("\n"):
        sys.stdout.write("\n")

    threshold = str(args.fail_on).upper()
    if threshold != "NONE" and any(SEVERITY_ORDER[f.severity] >= SEVERITY_ORDER[threshold] for f in findings):
        return 2
    return 0


def audit_skills(skills_dir: Path) -> tuple[list[Finding], ScanStats]:
    findings: list[Finding] = []
    skill_dirs = [path for path in sorted(skills_dir.iterdir()) if path.is_dir() and not path.name.startswith((".", "_"))]
    files_scanned = 0

    for skill_dir in skill_dirs:
        text_files = list(iter_skill_text_files(skill_dir))
        files_scanned += len(text_files)
        for path in text_files:
            findings.extend(_audit_text_file(skill_dir.name, path, skills_dir))
        findings.extend(_audit_script_heavy_without_references(skill_dir, skills_dir))

    findings.sort(key=lambda item: (-SEVERITY_ORDER[item.severity], item.path, item.line, item.rule_id))
    stats = ScanStats(skills_scanned=len(skill_dirs), files_scanned=files_scanned)
    return findings, stats


def iter_skill_text_files(skill_dir: Path) -> Iterable[Path]:
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts:
            continue
        if path.suffix == ".pyc":
            continue
        if path.name == "SKILL.md" or path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def _audit_text_file(skill_name: str, path: Path, skills_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return findings

    is_script = "scripts" in path.parts
    is_asset = "assets" in path.parts or "references" in path.parts
    rel_path = path.relative_to(REPO_ROOT).as_posix()

    for line_no, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\n")
        if not line.strip():
            continue

        for pattern in GENERIC_DOMAIN_PATTERNS:
            match = pattern.search(line)
            if match:
                findings.append(
                    Finding(
                        severity="WARN",
                        rule_id="generic_domain_hardcoding",
                        skill=skill_name,
                        path=rel_path,
                        line=line_no,
                        message=f"Hardcoded domain phrase `{match.group(0)}` reduces skill portability.",
                        excerpt=_excerpt(line),
                    )
                )
                break

        for pattern in PIPELINE_VOICE_PATTERNS:
            match = pattern.search(line)
            if match:
                findings.append(
                    Finding(
                        severity="WARN",
                        rule_id="pipeline_voice",
                        skill=skill_name,
                        path=rel_path,
                        line=line_no,
                        message=f"Pipeline/internal voice phrase `{match.group(0)}` appears in skill content.",
                        excerpt=_excerpt(line),
                    )
                )
                break

        if is_script:
            match = re.search(r"while\s+len\s*\(\s*paragraphs\s*\)\s*<", line)
            if match:
                findings.append(
                    Finding(
                        severity="ERROR",
                        rule_id="forced_paragraph_count",
                        skill=skill_name,
                        path=rel_path,
                        line=line_no,
                        message="Forced paragraph-count loop detected (`while len(paragraphs) < ...`).",
                        excerpt=_excerpt(line),
                    )
                )

        ellipsis_match = _ellipsis_match(line, is_script=is_script)
        if ellipsis_match:
            severity = "WARN" if (is_script or is_asset) else "INFO"
            findings.append(
                Finding(
                    severity=severity,
                    rule_id="reader_facing_ellipsis",
                    skill=skill_name,
                    path=rel_path,
                    line=line_no,
                    message=f"Ellipsis-like token `{ellipsis_match}` may leak into reader-facing artifacts.",
                    excerpt=_excerpt(line),
                )
            )

    return findings


def _audit_script_heavy_without_references(skill_dir: Path, skills_dir: Path) -> list[Finding]:
    skill_md = skill_dir / "SKILL.md"
    script_files = [
        path
        for path in sorted((skill_dir / "scripts").rglob("*"))
        if path.is_file() and path.suffix in {".py", ".sh", ".js", ".ts"} and "__pycache__" not in path.parts
    ]
    if not script_files:
        return []

    script_nonempty_lines = 0
    for path in script_files:
        try:
            script_nonempty_lines += sum(1 for line in path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip())
        except Exception:
            continue

    is_script_heavy = len(script_files) >= 2 or script_nonempty_lines >= 80
    if not is_script_heavy:
        return []

    if skill_md.exists():
        skill_md_text = skill_md.read_text(encoding="utf-8", errors="ignore").lower()
        has_reference = any(token in skill_md_text for token in SCRIPT_REFERENCE_TOKENS)
        if has_reference:
            return []
        path = skill_md.relative_to(REPO_ROOT).as_posix()
        return [
            Finding(
                severity="WARN",
                rule_id="script_heavy_without_references",
                skill=skill_dir.name,
                path=path,
                line=1,
                message=(
                    "Skill has substantial script logic but `SKILL.md` does not reference its scripts "
                    f"({len(script_files)} files, {script_nonempty_lines} non-empty lines)."
                ),
                excerpt=_excerpt(_first_nonempty_line(skill_md)),
            )
        ]

    path = script_files[0].relative_to(REPO_ROOT).as_posix()
    return [
        Finding(
            severity="WARN",
            rule_id="script_heavy_without_references",
            skill=skill_dir.name,
            path=path,
            line=1,
            message=(
                "Skill has substantial script logic but no `SKILL.md` reference surface was found "
                f"({len(script_files)} files, {script_nonempty_lines} non-empty lines)."
            ),
            excerpt=_excerpt(_first_nonempty_line(script_files[0])),
        )
    ]


def _ellipsis_match(line: str, *, is_script: bool) -> str | None:
    if is_script:
        return _script_ellipsis_match(line)
    for pattern in ELLIPSIS_PATTERNS:
        match = pattern.search(line)
        if match:
            return match.group(0)
    return None


def _script_ellipsis_match(line: str) -> str | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if "re.compile(" in stripped:
        return None
    if re.search(r"\bif\s+[\'\"].*(?:\.\.\.|…).*[\'\"]\s+in\s+", stripped):
        return None
    if re.search(r"tuple\[[^\]]*\.\.\.[^\]]*\]", stripped):
        return None

    for match in re.finditer(r"([\'\"])(.*?)(?<!\\)\1", stripped):
        content = match.group(2)
        for pattern in ELLIPSIS_PATTERNS:
            hit = pattern.search(content)
            if hit:
                return hit.group(0)
    return None


def _excerpt(text: str, limit: int = 160) -> str:
    compact = " ".join(str(text or "").strip().split())
    if len(compact) <= limit:
        return compact
    clipped = compact[: limit - 3].rsplit(" ", 1)[0].strip()
    return (clipped or compact[: limit - 3]).rstrip() + "..."


def _first_nonempty_line(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.strip():
                return line
    except Exception:
        return ""
    return ""


def render_report(*, findings: list[Finding], stats: ScanStats, fmt: str) -> str:
    if fmt == "json":
        payload = {
            "summary": {
                "skills_scanned": stats.skills_scanned,
                "files_scanned": stats.files_scanned,
                "findings": len(findings),
                "by_severity": _count_by_severity(findings),
                "by_rule": _count_by_rule(findings),
            },
            "findings": [asdict(item) for item in findings],
        }
        return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    lines = [
        "# Skill Audit Report",
        "",
        f"- Skills scanned: {stats.skills_scanned}",
        f"- Files scanned: {stats.files_scanned}",
        f"- Findings: {len(findings)}",
        f"- By severity: {_format_counts(_count_by_severity(findings))}",
        f"- By rule: {_format_counts(_count_by_rule(findings))}",
        "",
    ]
    if not findings:
        lines.append("No findings.")
        return "\n".join(lines) + "\n"

    for item in findings:
        lines.extend(
            [
                f"[{item.severity}] {item.rule_id} {item.path}:{item.line}",
                f"  skill: {item.skill}",
                f"  message: {item.message}",
                f"  excerpt: {item.excerpt}",
                "",
            ]
        )
    return "\n".join(lines)


def _count_by_severity(findings: Iterable[Finding]) -> dict[str, int]:
    counts = {"ERROR": 0, "WARN": 0, "INFO": 0}
    for item in findings:
        counts[item.severity] = counts.get(item.severity, 0) + 1
    return {key: value for key, value in counts.items() if value}


def _count_by_rule(findings: Iterable[Finding]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in findings:
        counts[item.rule_id] = counts.get(item.rule_id, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def _format_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "none"
    return ", ".join(f"{key}={value}" for key, value in counts.items())


if __name__ == "__main__":
    raise SystemExit(main())
