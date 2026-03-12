from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows).rstrip() + ("\n" if rows else ""), encoding="utf-8")


def _load_core_set(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            title = str(row.get("title") or "").strip()
            paper_id = str(row.get("paper_id") or "").strip()
            if title and paper_id:
                rows.append(
                    {
                        "paper_id": paper_id,
                        "title": title,
                        "year": str(row.get("year") or "").strip(),
                        "url": str(row.get("url") or "").strip(),
                    }
                )
    return rows


def _binding_status(*, recommendation: str, blocking_gaps: list[str]) -> str:
    rec = str(recommendation or "").strip().lower()
    if blocking_gaps:
        return "BLOCKED"
    if rec == "decompose":
        return "PASS"
    return "REROUTE"


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

    from tooling.common import atomic_write_text, load_yaml, normalize_title_for_dedupe, parse_semicolon_list, read_jsonl, tokenize

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs) or ["papers/core_set.csv", "outline/chapter_skeleton.yml", "papers/papers_dedup.jsonl"]
    outputs = parse_semicolon_list(args.outputs) or ["outline/section_bindings.jsonl", "outline/section_binding_report.md"]
    core_path = workspace / inputs[0]
    skeleton_path = workspace / inputs[1]
    dedup_path = workspace / inputs[2] if len(inputs) > 2 else workspace / "papers/papers_dedup.jsonl"
    bindings_path = workspace / outputs[0]
    report_path = workspace / outputs[1]

    chapters = load_yaml(skeleton_path) if skeleton_path.exists() else None
    if not isinstance(chapters, list) or not chapters:
        raise SystemExit(f"Invalid chapter skeleton in {skeleton_path}")
    papers = _load_core_set(core_path)
    meta_by_key: dict[str, dict[str, Any]] = {}
    if dedup_path.exists():
        for rec in read_jsonl(dedup_path):
            if not isinstance(rec, dict):
                continue
            title = str(rec.get("title") or "").strip()
            year = str(rec.get("year") or "").strip()
            if title:
                meta_by_key[f"{normalize_title_for_dedupe(title)}::{year}"] = rec

    enriched: list[dict[str, Any]] = []
    for paper in papers:
        key = f"{normalize_title_for_dedupe(paper['title'])}::{paper['year']}"
        meta = meta_by_key.get(key) or {}
        abstract = str(meta.get("abstract") or "").strip()
        tokens = {tok for tok in tokenize(f"{paper['title']} {abstract}") if tok}
        enriched.append({**paper, "_tokens": tokens})

    rows: list[dict[str, Any]] = []
    report_lines = ["# SECTION_BINDING_REPORT", ""]
    report_lines.append("| Section | Coverage | Status | Recommendation |")
    report_lines.append("|---|---:|---|---|")

    for chapter in chapters:
        if not isinstance(chapter, dict):
            continue
        section_id = str(chapter.get("id") or "").strip()
        title = str(chapter.get("title") or "").strip()
        rationale = str(chapter.get("rationale") or "").strip()
        seeds = [str(x).strip() for x in (chapter.get("seed_topics") or []) if str(x).strip()]
        target_h3 = int(chapter.get("target_h3_count") or 3)
        section_tokens = {tok for tok in tokenize(" ".join([title, rationale, *seeds])) if tok}
        scored: list[tuple[int, str, dict[str, Any]]] = []
        for paper in enriched:
            overlap = len(section_tokens & set(paper.get("_tokens") or set()))
            score = overlap
            scored.append((score, paper["paper_id"], paper))
        scored.sort(key=lambda item: (-item[0], item[1]))
        primary_n = max(8, target_h3 * 4)
        support_n = max(4, target_h3 * 2)
        primary = [paper["paper_id"] for score, _, paper in scored[:primary_n] if score > 0]
        support = [paper["paper_id"] for score, _, paper in scored[primary_n: primary_n + support_n] if score > 0]
        coverage_count = len(primary) + len(support)
        blocking_gaps: list[str] = []
        if coverage_count < max(8, target_h3 * 4):
            blocking_gaps.append("chapter evidence is thin; reroute to retrieval expansion or merge scope")
        recommendation = "decompose" if coverage_count >= max(12, target_h3 * 5) else "hold_or_merge"
        status = _binding_status(recommendation=recommendation, blocking_gaps=blocking_gaps)
        rows.append(
            {
                "section_id": section_id,
                "section_title": title,
                "paper_ids_primary": primary,
                "paper_ids_support": support,
                "coverage_count": coverage_count,
                "status": status,
                "blocking_gaps": blocking_gaps,
                "decomposition_recommendation": recommendation,
            }
        )
        report_lines.append(f"| {section_id} {title} | {coverage_count} | {status} | {recommendation} |")

    _write_jsonl(bindings_path, rows)
    atomic_write_text(report_path, "\n".join(report_lines).rstrip() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
