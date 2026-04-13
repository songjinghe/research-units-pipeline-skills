from __future__ import annotations

import argparse
import sys
from pathlib import Path


GENERIC_TOKENS = {
    "what",
    "does",
    "the",
    "available",
    "evidence",
    "support",
    "target",
    "topic",
    "studies",
    "study",
    "include",
    "exclude",
    "review",
    "question",
    "questions",
    "after",
    "screening",
    "and",
    "extraction",
}


def _match_tokens(text: str) -> set[str]:
    import re

    return {token for token in re.findall(r"[a-z0-9]+", str(text or "").lower()) if len(token) >= 3 and token not in GENERIC_TOKENS}


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

    from tooling.review_workflows import choose_candidate_pool_path, load_candidate_records, parse_protocol, stable_paper_id, title_tokens, write_csv_rows
    from tooling.common import now_iso_seconds

    workspace = Path(args.workspace).resolve()
    protocol_path = workspace / "output" / "PROTOCOL.md"
    if not protocol_path.exists():
        raise SystemExit("screening-manager requires `output/PROTOCOL.md`.")

    protocol = parse_protocol(protocol_path.read_text(encoding="utf-8", errors="ignore"))
    pool_path = choose_candidate_pool_path(workspace)
    if pool_path is None:
        raise SystemExit("No candidate pool found for screening.")
    records = load_candidate_records(workspace)
    include_tokens = _match_tokens(" ".join(protocol.get("review_questions") or []) + " " + " ".join(text for _, text in protocol.get("inclusion") or []))
    exclude_tokens = _match_tokens(" ".join(text for _, text in protocol.get("exclusion") or []))
    rows = []
    for idx, record in enumerate(records, start=1):
        title = str(record.get("title") or "").strip()
        abstract = str(record.get("abstract") or "").strip()
        combined_tokens = title_tokens(title) | title_tokens(abstract)
        decision = "include" if combined_tokens & include_tokens else "exclude"
        reason_codes = "I1" if decision == "include" else "E1"
        if decision == "exclude" and exclude_tokens & combined_tokens:
            reason_codes = "E1"
        reason = (
            "Matches the topic boundary defined in the protocol."
            if decision == "include"
            else "Does not match the topic boundary strongly enough for inclusion."
        )
        rows.append(
            {
                "paper_id": stable_paper_id(record, index=idx),
                "title": title,
                "year": str(record.get("year") or ""),
                "url": str(record.get("url") or ""),
                "decision": decision,
                "reason": reason,
                "reason_codes": reason_codes,
                "reviewer": "CODEX",
                "decided_at": now_iso_seconds(),
                "notes": "",
            }
        )

    out_path = workspace / "papers" / "screening_log.csv"
    write_csv_rows(
        out_path,
        rows,
        fieldnames=["paper_id", "title", "year", "url", "decision", "reason", "reason_codes", "reviewer", "decided_at", "notes"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
