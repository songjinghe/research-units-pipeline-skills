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

    from tooling.review_workflows import load_candidate_records, parse_protocol, read_csv_rows, stable_paper_id, write_csv_rows

    workspace = Path(args.workspace).resolve()
    screening_path = workspace / "papers" / "screening_log.csv"
    protocol_path = workspace / "output" / "PROTOCOL.md"
    if not screening_path.exists() or not protocol_path.exists():
        raise SystemExit("extraction-form requires `papers/screening_log.csv` and `output/PROTOCOL.md`.")

    screening_rows = read_csv_rows(screening_path)
    included = [row for row in screening_rows if str(row.get("decision") or "").strip().lower() == "include"]
    protocol = parse_protocol(protocol_path.read_text(encoding="utf-8", errors="ignore"))
    schema_fields = [field["field"] for field in protocol.get("extraction_fields") or []]
    candidate_records = load_candidate_records(workspace)
    by_key = {
        (str(rec.get("paper_id") or "").strip(), str(rec.get("title") or "").strip(), str(rec.get("url") or "").strip()): rec
        for rec in candidate_records
    }

    rows = []
    for idx, row in enumerate(included, start=1):
        rec = by_key.get((row.get("paper_id", ""), row.get("title", ""), row.get("url", "")), {})
        out = {
            "paper_id": row.get("paper_id") or stable_paper_id(rec, index=idx),
            "title": row.get("title", ""),
            "year": row.get("year", ""),
            "url": row.get("url", ""),
            "notes": "Deterministic extraction; enrich manually for deeper synthesis." if not rec else "",
        }
        for field in schema_fields:
            out[field] = str(rec.get(field) or "")
        rows.append(out)

    fieldnames = ["paper_id", "title", "year", "url", *schema_fields, "notes"]
    write_csv_rows(workspace / "papers" / "extraction_table.csv", rows, fieldnames=fieldnames)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
