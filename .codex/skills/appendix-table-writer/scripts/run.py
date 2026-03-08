from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


_TABLE_SEP = re.compile(r"(?m)^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$")


def _is_placeholder(text: str) -> bool:
    low = (text or "").strip().lower()
    if not low:
        return True
    if "<!-- scaffold" in low:
        return True
    if "(placeholder)" in low:
        return True
    if re.search(r"(?i)\b(?:todo|tbd|fixme)\b", low):
        return True
    if "…" in (text or ""):
        return True
    if re.search(r"(?m)\.\.\.+", text or ""):
        return True
    return False


def _md_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = ["| " + " | ".join(cell.replace("\n", " ").strip() for cell in row) + " |" for row in rows]
    return "\n".join([head, sep] + body)


def _clean(text: str, *, limit: int = 140) -> str:
    s = str(text or "").strip()
    s = s.replace("\n", " ")
    s = re.sub(r"\s+", " ", s)
    s = s.replace("|", ", ")
    s = s.strip(" \"'`")
    if len(s) <= limit:
        return s
    clipped = s[:limit].rsplit(" ", 1)[0].strip()
    return clipped if clipped else s[:limit].strip()


def _uniq(items: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        v = str(item or "").strip()
        if not v or v in seen:
            continue
        seen.add(v)
        out.append(v)
    return out


def _cite_cell(keys: list[str], *, limit: int = 4) -> str:
    keys = _uniq(keys)[:limit]
    return " ".join(f"[@{k}]" for k in keys)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not path.exists() or path.stat().st_size <= 0:
        return out
    import json

    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--unit-id", default="")
    parser.add_argument("--inputs", default="")
    parser.add_argument("--outputs", default="")
    parser.add_argument("--checkpoint", default="")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root))

    from tooling.common import atomic_write_text, ensure_dir, parse_semicolon_list
    from tooling.quality_gate import QualityIssue, check_unit_outputs, write_quality_report

    workspace = Path(args.workspace).resolve()
    unit_id = str(args.unit_id or "U0927").strip() or "U0927"

    outputs = parse_semicolon_list(args.outputs) or ["outline/tables_appendix.md", "output/TABLES_APPENDIX_REPORT.md"]
    out_rel = next((x for x in outputs if x.endswith("tables_appendix.md")), "outline/tables_appendix.md")
    report_rel = next((x for x in outputs if x.endswith("TABLES_APPENDIX_REPORT.md")), "output/TABLES_APPENDIX_REPORT.md")
    out_path = workspace / out_rel
    report_path = workspace / report_rel
    ensure_dir(out_path.parent)
    ensure_dir(report_path.parent)

    briefs = {str(r.get("sub_id") or "").strip(): r for r in _load_jsonl(workspace / "outline" / "subsection_briefs.jsonl") if str(r.get("sub_id") or "").strip()}
    packs = {str(r.get("sub_id") or "").strip(): r for r in _load_jsonl(workspace / "outline" / "evidence_drafts.jsonl") if str(r.get("sub_id") or "").strip()}
    anchors = {str(r.get("sub_id") or "").strip(): r for r in _load_jsonl(workspace / "outline" / "anchor_sheet.jsonl") if str(r.get("sub_id") or "").strip()}

    if briefs and packs:
        sub_ids = [sid for sid in briefs.keys() if sid in packs]
        sub_ids.sort(key=lambda s: [int(x) if x.isdigit() else x for x in re.split(r"([0-9]+)", s)])

        rows_a1: list[list[str]] = []
        rows_a2: list[list[str]] = []
        rows_a3: list[list[str]] = []

        for sid in sub_ids:
            brief = briefs.get(sid) or {}
            pack = packs.get(sid) or {}
            anchor_rec = anchors.get(sid) or {}
            title = str(brief.get("title") or pack.get("title") or sid).strip()
            area = f"{sid} {title}".strip()

            axes = [str(x).strip() for x in (brief.get("axes") or []) if str(x).strip()]
            comparisons = pack.get("concrete_comparisons") or []
            comp = comparisons[0] if comparisons and isinstance(comparisons[0], dict) else {}
            comp_axis = _clean(comp.get("axis") or "", limit=64)
            lens_parts = []
            if comp_axis:
                lens_parts.append(comp_axis)
            lens_parts.extend(axes[:2])
            lens = "; ".join(_uniq(lens_parts)[:3])

            highlights: list[str] = []
            ref_keys: list[str] = []
            if isinstance(comp, dict):
                a_label = _clean(comp.get("A_label") or "", limit=36)
                b_label = _clean(comp.get("B_label") or "", limit=36)
                if a_label and b_label and comp_axis:
                    highlights.append(f"{a_label} vs {b_label} on {comp_axis}")
                for hl_key in ["A_highlights", "B_highlights"]:
                    for hl in comp.get(hl_key) or []:
                        if not isinstance(hl, dict):
                            continue
                        excerpt = _clean(hl.get("excerpt") or "", limit=100)
                        if excerpt:
                            highlights.append(excerpt)
                        ref_keys.extend([str(x).strip() for x in (hl.get("citations") or []) if str(x).strip()])
            ref_keys.extend([str(x).strip() for x in (comp.get("citations") or []) if str(x).strip()])
            for rec in (anchor_rec.get("anchors") or [])[:3]:
                if not isinstance(rec, dict):
                    continue
                ref_keys.extend([str(x).strip() for x in (rec.get("citations") or []) if str(x).strip()])
            rows_a1.append([
                area,
                lens or _clean(title, limit=64),
                "<br>".join(_uniq(highlights)[:2]) or _clean((pack.get("definitions_setup") or [{}])[0].get("bullet") or "evidence-backed comparison", limit=120),
                _cite_cell(ref_keys),
            ])

            anchor_bits: list[str] = []
            anchor_keys: list[str] = []
            for rec in (anchor_rec.get("anchors") or [])[:3]:
                if not isinstance(rec, dict):
                    continue
                txt = _clean(rec.get("text") or "", limit=120)
                if txt:
                    anchor_bits.append(txt)
                anchor_keys.extend([str(x).strip() for x in (rec.get("citations") or []) if str(x).strip()])
            for rec in (pack.get("evaluation_protocol") or [])[:2]:
                if not isinstance(rec, dict):
                    continue
                txt = _clean(rec.get("bullet") or "", limit=100)
                if txt:
                    anchor_bits.append(txt)
                anchor_keys.extend([str(x).strip() for x in (rec.get("citations") or []) if str(x).strip()])
            rows_a2.append([
                area,
                "<br>".join(_uniq(anchor_bits)[:3]) or lens or _clean(title, limit=96),
                _cite_cell(anchor_keys or ref_keys),
            ])

            risk_bits: list[str] = []
            risk_keys: list[str] = []
            for rec in (pack.get("failures_limitations") or [])[:2]:
                if not isinstance(rec, dict):
                    continue
                txt = _clean(rec.get("bullet") or rec.get("excerpt") or "", limit=110)
                if txt:
                    risk_bits.append(txt)
                risk_keys.extend([str(x).strip() for x in (rec.get("citations") or []) if str(x).strip()])
            if risk_bits:
                rows_a3.append([
                    area,
                    "<br>".join(_uniq(risk_bits)[:2]),
                    _cite_cell(risk_keys or ref_keys),
                ])

        parts: list[str] = []
        parts.append("**Appendix Table A1. Reader-facing comparison lenses across the survey areas.**")
        parts.append("")
        parts.append(_md_table(["Survey area", "Comparison lens", "Representative evidence", "Key refs"], rows_a1))
        parts.append("")
        parts.append("**Appendix Table A2. Concrete evaluation anchors and protocol cues by survey area.**")
        parts.append("")
        parts.append(_md_table(["Survey area", "Anchor facts and protocol cues", "Key refs"], rows_a2))
        if rows_a3:
            parts.append("")
            parts.append("**Appendix Table A3. Recurring limitations and risk surfaces highlighted by the evidence packs.**")
            parts.append("")
            parts.append(_md_table(["Survey area", "Risk or limitation signal", "Key refs"], rows_a3))
        text = "\n".join(parts).rstrip() + "\n"
        atomic_write_text(out_path, text)

    issues = check_unit_outputs(skill="appendix-table-writer", workspace=workspace, outputs=[out_rel])
    status = "PASS" if not issues else "FAIL"
    rep_lines = [
        "# Appendix tables report",
        "",
        f"- Status: {status}",
    ]
    if issues:
        rep_lines.extend(["", "## Issues"])
        rep_lines.extend([f"- {it.message}" for it in issues])
        write_quality_report(workspace=workspace, unit_id=unit_id, skill="appendix-table-writer", issues=issues)
    else:
        text = out_path.read_text(encoding="utf-8", errors="ignore")
        rep_lines.extend([
            f"- Tables detected: {len(re.findall(_TABLE_SEP, text))}",
            f"- Output: `{out_rel}`",
        ])
    atomic_write_text(report_path, "\n".join(rep_lines).rstrip() + "\n")
    return 0 if not issues else 2


if __name__ == "__main__":
    raise SystemExit(main())
