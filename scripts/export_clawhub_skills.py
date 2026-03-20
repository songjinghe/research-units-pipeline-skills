from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from typing import Iterable

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPO_ROOT / ".codex" / "skills"
DEST_ROOT = REPO_ROOT / "skills"
TOOLING_ROOT = REPO_ROOT / "tooling"
PIPELINES_ROOT = REPO_ROOT / "pipelines"
VALID_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

DEFAULT_EXPORT_SKILLS = [
    "agent-survey-corpus",
    "workspace-init",
    "arxiv-search",
    "dedupe-rank",
    "paper-notes",
    "citation-verifier",
    "taxonomy-builder",
    "outline-builder",
    "section-mapper",
    "subsection-briefs",
    "evidence-binder",
    "evidence-draft",
    "writer-context-pack",
    "subsection-writer",
    "front-matter-writer",
    "section-merger",
    "draft-polisher",
    "pipeline-auditor",
    "artifact-contract-auditor",
    "latex-scaffold",
    "latex-compile-qa",
]

TEXT_EXTENSIONS = {
    ".bib",
    ".csv",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".svg",
    ".toml",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}

SKIP_DIRS = {
    "__pycache__",
    ".git",
    ".idea",
    ".pytest_cache",
}

SKIP_FILE_SUFFIXES = {
    ".pyc",
}

LATEX_REQUIRED_BINS = {
    "latex-compile-qa": ["latexmk"],
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export selected repo skills into standalone Clawhub-friendly bundles under skills/."
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Specific skill to export. Repeatable. Defaults to a curated public subset.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Export every repo skill under .codex/skills, remapping invalid slugs when needed.",
    )
    parser.add_argument(
        "--version",
        default="0.1.0",
        help="Semver to write into exported SKILL.md frontmatter.",
    )
    parser.add_argument(
        "--keep-existing",
        action="store_true",
        help="Do not delete existing destination skill directories before export.",
    )
    args = parser.parse_args()

    skills = all_source_skills() if args.all else (args.skill or list(DEFAULT_EXPORT_SKILLS))
    DEST_ROOT.mkdir(parents=True, exist_ok=True)

    exported: list[tuple[str, str]] = []
    for skill_name in skills:
        dest_slug = export_slug(skill_name)
        export_skill(
            source_skill_name=skill_name,
            dest_slug=dest_slug,
            version=str(args.version).strip() or "0.1.0",
            keep_existing=bool(args.keep_existing),
        )
        exported.append((skill_name, dest_slug))

    write_index(exported)
    print(f"Exported {len(exported)} skills into {DEST_ROOT}")
    for source_name, dest_slug in exported:
        if source_name == dest_slug:
            print(f"- {dest_slug}")
        else:
            print(f"- {source_name} -> {dest_slug}")
    return 0


def export_skill(*, source_skill_name: str, dest_slug: str, version: str, keep_existing: bool) -> None:
    src_dir = SOURCE_ROOT / source_skill_name
    if not src_dir.is_dir():
        raise SystemExit(f"Source skill not found: {src_dir}")

    dest_dir = DEST_ROOT / dest_slug
    if dest_dir.exists() and not keep_existing:
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    copy_text_tree(src_dir, dest_dir, skill_name=source_skill_name)
    copy_text_tree(TOOLING_ROOT, dest_dir / "tooling", skill_name=source_skill_name)
    copy_text_tree(PIPELINES_ROOT, dest_dir / "pipelines", skill_name=source_skill_name)

    patch_exported_common(dest_dir / "tooling" / "common.py")
    patch_exported_executor(dest_dir / "tooling" / "executor.py")
    patch_exported_quality_gate(dest_dir / "tooling" / "quality_gate.py")
    write_agents_marker(dest_dir, source_skill_name=source_skill_name, dest_slug=dest_slug)
    write_clawhubignore(dest_dir)

    skill_md = dest_dir / "SKILL.md"
    if skill_md.exists():
        rewrite_skill_frontmatter(
            skill_md,
            source_skill_name=source_skill_name,
            dest_slug=dest_slug,
            version=version,
        )


def copy_text_tree(src_dir: Path, dest_dir: Path, *, skill_name: str) -> None:
    for path in sorted(src_dir.rglob("*")):
        rel = path.relative_to(src_dir)
        if should_skip(rel):
            continue

        out_path = dest_dir / rel
        if path.is_dir():
            out_path.mkdir(parents=True, exist_ok=True)
            continue

        out_path.parent.mkdir(parents=True, exist_ok=True)
        if is_text_file(path):
            text = path.read_text(encoding="utf-8")
            text = rewrite_text(text, skill_name=skill_name)
            out_path.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(path, out_path)


def should_skip(rel_path: Path) -> bool:
    for part in rel_path.parts:
        if part in SKIP_DIRS:
            return True
    return rel_path.suffix in SKIP_FILE_SUFFIXES


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    try:
        path.read_text(encoding="utf-8")
        return True
    except Exception:
        return False


def rewrite_text(text: str, *, skill_name: str) -> str:
    replacements = {
        f".codex/skills/{skill_name}/scripts/run.py": "scripts/run.py",
        f".codex/skills/{skill_name}/SKILL.md": "SKILL.md",
        f".codex/skills/{skill_name}/assets/": "assets/",
        f".codex/skills/{skill_name}/references/": "references/",
        f".codex/skills/{skill_name}/": "",
        f'repo_root / ".codex" / "skills" / "{skill_name}" / "assets"': 'repo_root / "assets"',
        f'repo_root / ".codex" / "skills" / "{skill_name}" / "references"': 'repo_root / "references"',
        f'repo_root / ".codex" / "skills" / "{skill_name}" / "scripts"': 'repo_root / "scripts"',
    }

    out = text
    for src, dst in replacements.items():
        out = out.replace(src, dst)

    out = out.replace("`python ./scripts/run.py", "`python scripts/run.py")
    out = out.replace("`./scripts/run.py", "`scripts/run.py")
    return out


def patch_exported_common(common_path: Path) -> None:
    if not common_path.exists():
        return
    text = common_path.read_text(encoding="utf-8")
    old = (
        "    try:\n"
        "        repo_root = find_repo_root(workspace)\n"
        "    except FileNotFoundError:\n"
        "        return None\n"
    )
    new = (
        "    try:\n"
        "        repo_root = find_repo_root(workspace)\n"
        "    except FileNotFoundError:\n"
        "        repo_root = Path(__file__).resolve().parents[1]\n"
    )
    if old in text:
        text = text.replace(old, new)
    common_path.write_text(text, encoding="utf-8")


def patch_exported_executor(executor_path: Path) -> None:
    if not executor_path.exists():
        return
    text = executor_path.read_text(encoding="utf-8")
    text = text.replace(
        'script_path = repo_root / ".codex" / "skills" / skill / "scripts" / "run.py"',
        'script_path = repo_root / "scripts" / "run.py"',
    )
    text = text.replace('skill_md = f".codex/skills/{skill}/SKILL.md"', 'skill_md = "SKILL.md"')
    executor_path.write_text(text, encoding="utf-8")


def patch_exported_quality_gate(quality_gate_path: Path) -> None:
    if not quality_gate_path.exists():
        return
    text = quality_gate_path.read_text(encoding="utf-8")
    text = text.replace('skill_md = f".codex/skills/{skill}/SKILL.md"', 'skill_md = "SKILL.md"')
    quality_gate_path.write_text(text, encoding="utf-8")


def rewrite_skill_frontmatter(skill_md_path: Path, *, source_skill_name: str, dest_slug: str, version: str) -> None:
    text = skill_md_path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)

    frontmatter["name"] = dest_slug
    frontmatter["version"] = version

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
    openclaw = metadata.get("openclaw")
    if not isinstance(openclaw, dict):
        openclaw = {}
    requires = openclaw.get("requires")
    if not isinstance(requires, dict):
        requires = {}

    any_bins = dedupe_strings([*as_string_list(requires.get("anyBins")), "python3", "python"])
    requires["anyBins"] = any_bins

    extra_bins = LATEX_REQUIRED_BINS.get(source_skill_name, [])
    if extra_bins:
        requires["bins"] = dedupe_strings([*as_string_list(requires.get("bins")), *extra_bins])

    openclaw["requires"] = requires
    metadata["openclaw"] = openclaw
    frontmatter["metadata"] = metadata

    rebuilt = dump_frontmatter(frontmatter, body)
    skill_md_path.write_text(rebuilt, encoding="utf-8")


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    match = re.match(r"^---\n(.*?)\n---\n?", text, flags=re.DOTALL)
    if not match:
        return {}, text
    raw = match.group(1)
    body = text[match.end() :]
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        data = {}
    return data, body


def dump_frontmatter(frontmatter: dict, body: str) -> str:
    yaml_text = yaml.safe_dump(
        frontmatter,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=120,
    ).strip()
    return f"---\n{yaml_text}\n---\n\n{body.lstrip()}"


def as_string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for item in value:
        text = str(item or "").strip()
        if text:
            out.append(text)
    return out


def dedupe_strings(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in values:
        text = str(raw or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        out.append(text)
    return out


def write_agents_marker(dest_dir: Path, *, source_skill_name: str, dest_slug: str) -> None:
    content = (
        "# AGENTS.md\n\n"
        "This exported skill uses `AGENTS.md` only as a local repo-root marker for bundled helper scripts.\n"
        f"Source skill: `{source_skill_name}` from `research-units-pipeline-skills`.\n"
        f"Export slug: `{dest_slug}`.\n"
    )
    (dest_dir / "AGENTS.md").write_text(content, encoding="utf-8")


def write_clawhubignore(dest_dir: Path) -> None:
    content = "\n".join(
        [
            "__pycache__/",
            "*.pyc",
            ".clawhub/",
            ".git/",
            "workspaces/",
            "",
        ]
    )
    (dest_dir / ".clawhubignore").write_text(content, encoding="utf-8")


def write_index(skills: list[tuple[str, str]]) -> None:
    lines = [
        "# Clawhub Exports",
        "",
        "These folders are standalone exports adapted from `.codex/skills/` for Clawhub-style upload and install.",
        "",
        "Publish examples:",
        "- `clawhub publish skills/arxiv-search`",
        "- `clawhub publish skills/taxonomy-builder`",
        "",
        "Exported skills:",
    ]
    for source_name, dest_slug in skills:
        if source_name == dest_slug:
            lines.append(f"- `{dest_slug}`")
        else:
            lines.append(f"- `{dest_slug}` (from `{source_name}`)")
    lines.extend(
        [
            "",
            "Notes:",
            "- Each exported skill bundles its own `tooling/` and `pipelines/` support files.",
            "- Repo-internal `.codex/skills/<name>/...` paths are rewritten to local package-relative paths.",
            "- Generated by `scripts/export_clawhub_skills.py`.",
            "",
        ]
    )
    (DEST_ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def all_source_skills() -> list[str]:
    return sorted(path.name for path in SOURCE_ROOT.iterdir() if path.is_dir())


def export_slug(source_skill_name: str) -> str:
    value = source_skill_name.strip().lower().replace("_", "-")
    value = re.sub(r"[^a-z0-9-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    if not value:
        raise SystemExit(f"Cannot derive Clawhub slug for skill: {source_skill_name}")
    if not VALID_SLUG_RE.match(value):
        raise SystemExit(f"Derived invalid Clawhub slug `{value}` for skill: {source_skill_name}")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
