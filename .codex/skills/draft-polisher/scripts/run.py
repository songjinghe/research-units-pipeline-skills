from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def _sha1(text: str) -> str:
    return hashlib.sha1((text or "").encode("utf-8", errors="ignore")).hexdigest()


def _extract_cites(text: str) -> list[str]:
    keys: set[str] = set()
    for m in re.finditer(r"\[@([^\]]+)\]", text or ""):
        inside = (m.group(1) or "").strip()
        for key in re.findall(r"[A-Za-z0-9:_-]+", inside):
            if key:
                keys.add(key)
    return sorted(keys)


def _merge_adjacent_citation_blocks(text: str) -> str:
    pattern = re.compile(r"(?:\[@[^\]]+\]\s*){2,}")

    def repl(match: re.Match[str]) -> str:
        keys: list[str] = []
        seen: set[str] = set()
        for inside in re.findall(r"\[@([^\]]+)\]", match.group(0)):
            for key in re.findall(r"[A-Za-z0-9:_-]+", inside):
                if key and key not in seen:
                    seen.add(key)
                    keys.append(key)
        return f"[@{'; '.join(keys)}]" if keys else match.group(0)

    merged = pattern.sub(repl, text or "")
    return re.sub(r"\s+([,.;:])", r"\1", merged)


def _h3_citation_sets(md: str) -> dict[str, set[str]]:
    cur_title = ""
    cur_lines: list[str] = []
    out: dict[str, set[str]] = {}

    def flush() -> None:
        nonlocal cur_title, cur_lines
        if not cur_title:
            return
        out[cur_title] = set(_extract_cites("\n".join(cur_lines)))

    for raw in (md or "").splitlines():
        if raw.startswith("### "):
            flush()
            cur_title = raw[4:].strip()
            cur_lines = []
            continue
        if raw.startswith("## "):
            flush()
            cur_title = ""
            cur_lines = []
            continue
        if cur_title:
            cur_lines.append(raw)

    flush()
    return out


def _merge_is_pass(workspace: Path) -> bool:
    report_path = workspace / "output" / "MERGE_REPORT.md"
    if not report_path.exists() or report_path.stat().st_size <= 0:
        return False
    text = report_path.read_text(encoding="utf-8", errors="ignore")
    return "- Status: PASS" in text


def _baseline_should_refresh(*, draft_text: str, baseline_path: Path) -> bool:
    if not baseline_path.exists() or baseline_path.stat().st_size <= 0:
        return True
    expected_sha = _sha1(draft_text)
    for raw in baseline_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = json.loads(raw)
        except Exception:
            return True
        if isinstance(rec, dict) and rec.get("kind") == "meta":
            return str(rec.get("draft_sha1") or "") != expected_sha
        return True
    return True


def _load_writer_packs(path: Path) -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    if not path.exists() or path.stat().st_size <= 0:
        return out
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = json.loads(raw)
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue
        title = str(rec.get("title") or "").strip()
        if title:
            out[title] = rec
    return out


def _clean_phrase(text: str, *, limit: int = 180) -> str:
    cleaned = re.sub(r"\s+", " ", str(text or "").strip())
    cleaned = cleaned.replace("/", " and ")
    cleaned = cleaned.strip(" \"'`")
    if len(cleaned) <= limit:
        return cleaned
    clipped = cleaned[:limit].rsplit(" ", 1)[0].strip()
    return clipped if clipped else cleaned[:limit].strip()


def _cite_block(keys: list[str], limit: int = 4) -> str:
    uniq: list[str] = []
    seen: set[str] = set()
    for key in keys:
        cleaned = str(key or "").strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        uniq.append(cleaned)
        if len(uniq) >= limit:
            break
    return f"[@{'; '.join(uniq)}]" if uniq else ""


def _section_chars_without_cites(text: str) -> int:
    return len(re.sub(r"\[@[^\]]+\]", "", text or ""))


def _top_up_h3_sections(*, draft: str, packs: dict[str, dict[str, object]]) -> str:
    return draft


def _top_up_global_citations(*, draft: str, packs: dict[str, dict[str, object]], target: int = 165) -> str:
    return draft


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
    from tooling.quality_gate import check_unit_outputs, write_quality_report

    workspace = Path(args.workspace).resolve()
    unit_id = str(args.unit_id or "U110").strip() or "U110"

    outputs = parse_semicolon_list(args.outputs) or ["output/DRAFT.md"]
    out_rel = outputs[0] if outputs else "output/DRAFT.md"
    draft_path = workspace / out_rel

    if draft_path.exists() and draft_path.stat().st_size > 0:
        draft_text = draft_path.read_text(encoding="utf-8", errors="ignore")
        draft_text = _merge_adjacent_citation_blocks(draft_text)
        if draft_text != draft_path.read_text(encoding="utf-8", errors="ignore"):
            atomic_write_text(draft_path, draft_text)

    baseline_rel = "output/citation_anchors.prepolish.jsonl"
    baseline_path = workspace / baseline_rel
    if draft_path.exists() and draft_path.stat().st_size > 0:
        draft = draft_path.read_text(encoding="utf-8", errors="ignore")
        if _merge_is_pass(workspace) and not re.search(r"(?m)^TODO:\s+MISSING\s+`", draft) and _baseline_should_refresh(draft_text=draft, baseline_path=baseline_path):
            ensure_dir(baseline_path.parent)
            sets = _h3_citation_sets(draft)
            header = {
                "kind": "meta",
                "draft_rel": out_rel,
                "draft_sha1": _sha1(draft),
                "h3_count": len(sets),
            }
            records = [{"kind": "h3", "title": title, "cite_keys": sorted(keys)} for title, keys in sorted(sets.items(), key=lambda kv: kv[0].lower())]
            lines = [json.dumps(header, ensure_ascii=False)] + [json.dumps(rec, ensure_ascii=False) for rec in records]
            atomic_write_text(baseline_path, "\n".join(lines).rstrip() + "\n")

    issues = check_unit_outputs(skill="draft-polisher", workspace=workspace, outputs=[out_rel])
    if issues:
        write_quality_report(workspace=workspace, unit_id=unit_id, skill="draft-polisher", issues=issues)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
