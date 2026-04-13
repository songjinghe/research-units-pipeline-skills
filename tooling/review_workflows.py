from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any

from tooling.common import atomic_write_text, load_yaml, now_iso_seconds, parse_semicolon_list, read_jsonl


CLAIM_PATTERNS = (
    "we propose",
    "we present",
    "we introduce",
    "we show",
    "we demonstrate",
    "we find",
    "our method",
    "our approach",
    "our framework",
    "our model",
    "contribution",
    "improves",
    "outperforms",
    "achieves",
)
EMPIRICAL_HINTS = (
    "%",
    "benchmark",
    "dataset",
    "metric",
    "accuracy",
    "success rate",
    "results",
    "experiment",
    "evaluation",
    "outperforms",
    "improves",
    "achieves",
)


def heading_context_sentences(text: str) -> list[dict[str, str]]:
    section = "Document"
    page = ""
    out: list[dict[str, str]] = []
    lines = (text or "").splitlines()
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            section = line.lstrip("#").strip() or section
            continue
        page_match = re.fullmatch(r"\[page\s+([0-9]+)\]", line, flags=re.IGNORECASE)
        if page_match:
            page = page_match.group(1)
            continue
        for sentence in split_sentences(line):
            if len(sentence) < 30:
                continue
            out.append(
                {
                    "section": section,
                    "page": page,
                    "sentence": sentence,
                }
            )
    return out


def split_sentences(text: str) -> list[str]:
    clean = re.sub(r"\s+", " ", str(text or "").strip())
    if not clean:
        return []
    parts = re.split(r"(?<=[.!?])\s+", clean)
    return [part.strip() for part in parts if part.strip()]


def classify_claim(sentence: str) -> str:
    low = sentence.lower()
    if any(token in low for token in EMPIRICAL_HINTS) or re.search(r"\b[0-9]+(\.[0-9]+)?\b", sentence):
        return "empirical"
    return "conceptual"


def pick_claim_candidates(text: str, *, limit: int = 8) -> list[dict[str, str]]:
    candidates = heading_context_sentences(text)
    scored: list[tuple[int, dict[str, str]]] = []
    for item in candidates:
        sent = item["sentence"]
        low = sent.lower()
        score = 0
        if any(pattern in low for pattern in CLAIM_PATTERNS):
            score += 4
        if item["section"].lower() in {"abstract", "introduction", "experiments", "results", "conclusion"}:
            score += 2
        if classify_claim(sent) == "empirical":
            score += 1
        scored.append((score, item))
    scored.sort(key=lambda pair: (-pair[0], pair[1]["section"], pair[1]["sentence"]))

    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for _, item in scored:
        sentence = item["sentence"]
        norm = re.sub(r"[^a-z0-9]+", " ", sentence.lower()).strip()
        if not norm or norm in seen:
            continue
        seen.add(norm)
        out.append(item)
        if len(out) >= limit:
            break
    return out or candidates[:limit]


def render_claims_markdown(claims: list[dict[str, str]]) -> str:
    empirical = [c for c in claims if c.get("type") == "empirical"]
    conceptual = [c for c in claims if c.get("type") == "conceptual"]
    lines = ["# Claims", ""]
    for title, bucket in (("Empirical claims", empirical), ("Conceptual claims", conceptual)):
        lines.extend([f"## {title}", ""])
        if not bucket:
            lines.append("- (none)")
            lines.append("")
            continue
        for claim in bucket:
            lines.extend(
                [
                    f"### {claim['id']}",
                    f"- Claim: {claim['claim']}",
                    f"- Type: {claim['type']}",
                    f"- Scope: {claim['scope']}",
                    f"- Source: {claim['source']}",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def parse_item_blocks(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw in (text or "").splitlines():
        line = raw.rstrip()
        if line.startswith("### "):
            if current:
                records.append(current)
            current = {"id": line[4:].strip()}
            continue
        if not current or not line.lstrip().startswith("- ") or ":" not in line:
            continue
        payload = line.lstrip()[2:]
        key, value = payload.split(":", 1)
        current[key.strip().lower().replace(" ", "_").replace("/", "_")] = value.strip()
    if current:
        records.append(current)
    return records


def load_candidate_records(workspace: Path) -> list[dict[str, Any]]:
    papers_dir = workspace / "papers"
    for path in (
        papers_dir / "papers_dedup.jsonl",
        papers_dir / "papers_raw.jsonl",
        papers_dir / "core_set.csv",
    ):
        if not path.exists():
            continue
        if path.suffix == ".jsonl":
            return [dict(rec) for rec in read_jsonl(path) if isinstance(rec, dict)]
        if path.suffix == ".csv":
            with path.open("r", encoding="utf-8", newline="") as handle:
                return [dict(row) for row in csv.DictReader(handle)]
    return []


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv_rows(path: Path, rows: list[dict[str, Any]], *, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def find_workspace_text_source(workspace: Path, *, stems: tuple[str, ...]) -> Path | None:
    candidates: list[Path] = []
    for base in (workspace / "inputs", workspace / "input", workspace):
        for stem in stems:
            for suffix in (".md", ".txt", ".pdf"):
                candidate = base / f"{stem}{suffix}"
                if candidate.exists():
                    candidates.append(candidate)
    return candidates[0] if candidates else None


def extract_pdf_text(path: Path) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception as exc:  # pragma: no cover - dependency availability differs
        raise RuntimeError(f"PDF extraction requires pypdf: {exc}") from exc

    reader = PdfReader(str(path))
    parts: list[str] = []
    for idx, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            parts.append(f"[page {idx}]\n{text.strip()}")
    return "\n\n".join(parts).strip()


def parse_protocol(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {
        "review_questions": [],
        "include_keywords": [],
        "exclude_keywords": [],
        "time_window_from": "",
        "time_window_to": "",
        "inclusion": [],
        "exclusion": [],
        "extraction_fields": [],
    }
    lines = (text or "").splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- RQ"):
            data["review_questions"].append(stripped[2:].strip())
        elif stripped.startswith("- include_keywords:"):
            data["include_keywords"] = [item.strip() for item in stripped.split(":", 1)[1].split(";") if item.strip()]
        elif stripped.startswith("- exclude_keywords:"):
            data["exclude_keywords"] = [item.strip() for item in stripped.split(":", 1)[1].split(";") if item.strip()]
        elif stripped.startswith("- time_window_from:"):
            data["time_window_from"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- time_window_to:"):
            data["time_window_to"] = stripped.split(":", 1)[1].strip()
        elif re.match(r"^- I[0-9]+:", stripped):
            code, body = stripped[2:].split(":", 1)
            data["inclusion"].append((code.strip(), body.strip()))
        elif re.match(r"^- E[0-9]+:", stripped):
            code, body = stripped[2:].split(":", 1)
            data["exclusion"].append((code.strip(), body.strip()))

    data["extraction_fields"] = parse_protocol_extraction_fields(text)
    return data


def parse_protocol_extraction_fields(text: str) -> list[dict[str, str]]:
    lines = (text or "").splitlines()
    fields: list[dict[str, str]] = []
    in_table = False
    for raw in lines:
        line = raw.strip()
        if line == "## Extraction Schema":
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("|"):
            continue
        cols = [col.strip() for col in line.strip("|").split("|")]
        if not cols or cols[0] in {"field", "---"}:
            continue
        if len(cols) < 4:
            continue
        fields.append(
            {
                "field": cols[0],
                "definition": cols[1],
                "allowed_values": cols[2],
                "notes": cols[3],
            }
        )
    return fields


def protocol_markdown(
    *,
    goal: str,
    review_questions: list[str],
    include_keywords: list[str],
    exclude_keywords: list[str],
    time_window_from: str,
    time_window_to: str,
    sources: list[str],
    extraction_fields: list[dict[str, str]],
) -> str:
    lines = [
        "# Evidence Review Protocol",
        "",
        "## Scope",
        f"- Goal: {goal or 'Review the target evidence base.'}",
        "",
        "## Review Questions",
    ]
    for idx, rq in enumerate(review_questions, start=1):
        lines.append(f"- RQ{idx}: {rq}")
    lines.extend(
        [
            "",
            "## Sources",
        ]
    )
    for source in sources:
        lines.append(f"- {source}")
    lines.extend(
        [
            "",
            "## Search Terms",
            f"- include_keywords: {'; '.join(include_keywords) if include_keywords else 'review topic'}",
            f"- exclude_keywords: {'; '.join(exclude_keywords) if exclude_keywords else 'none'}",
            f"- time_window_from: {time_window_from or '2000'}",
            f"- time_window_to: {time_window_to or 'present'}",
            f"- search_date: {now_iso_seconds()}",
            "",
            "## Inclusion Criteria",
            f"- I1: Include studies directly about {goal or 'the review topic'}.",
            "- I2: Include studies that report a concrete method, system, or evidence claim.",
            "",
            "## Exclusion Criteria",
            "- E1: Exclude studies outside the target topic boundary.",
            "- E2: Exclude records without enough title/abstract detail to judge inclusion.",
            "- E3: Exclude duplicates or near-duplicates once deduplicated upstream.",
            "",
            "## Screening Plan",
            "- Title/abstract screening first; full-text checks only if the abstract is borderline.",
            "- Every row in `papers/screening_log.csv` must include `decision`, `reason`, and `reason_codes`.",
            "",
            "## Extraction Schema",
            "| field | definition | allowed_values | notes |",
            "|---|---|---|---|",
        ]
    )
    for field in extraction_fields:
        lines.append(
            f"| {field['field']} | {field['definition']} | {field['allowed_values']} | {field['notes']} |"
        )
    lines.extend(
        [
            "",
            "## Bias Plan",
            "- Use `low|unclear|high` for each bias domain and keep notes short and specific.",
            "",
            "## Approval",
            "- HUMAN approval required before screening.",
            "",
        ]
    )
    return "\n".join(lines)


def choose_candidate_pool_path(workspace: Path) -> Path | None:
    for path in (
        workspace / "papers" / "papers_dedup.jsonl",
        workspace / "papers" / "papers_raw.jsonl",
        workspace / "papers" / "core_set.csv",
    ):
        if path.exists():
            return path
    return None


def stable_paper_id(record: dict[str, Any], *, index: int) -> str:
    value = str(record.get("paper_id") or "").strip()
    if value:
        return value
    return f"P{index:04d}"


def title_tokens(value: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", str(value or "").lower()) if len(token) >= 3}


def write_text(path: Path, text: str) -> None:
    atomic_write_text(path, text.rstrip() + "\n")


def maybe_parse_queries_md(path: Path) -> tuple[list[str], list[str], str, str]:
    if not path.exists():
        return [], [], "", ""
    keywords: list[str] = []
    exclude: list[str] = []
    time_from = ""
    time_to = ""
    mode = ""
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if line.startswith("- keywords:"):
            mode = "keywords"
            continue
        if line.startswith("- exclude:"):
            mode = "exclude"
            continue
        if line.startswith("- time_window.from:"):
            time_from = line.split(":", 1)[1].strip()
            continue
        if line.startswith("- time_window.to:"):
            time_to = line.split(":", 1)[1].strip()
            continue
        if mode in {"keywords", "exclude"} and line.startswith("- "):
            value = line[2:].strip().strip('"').strip("'")
            if value:
                (keywords if mode == "keywords" else exclude).append(value)
    return keywords, exclude, time_from, time_to


def summarize_outline(path: Path) -> tuple[list[str], list[str]]:
    if not path.exists():
        return [], []
    outline = load_yaml(path)
    sections: list[str] = []
    bullets: list[str] = []
    if not isinstance(outline, list):
        return sections, bullets
    for sec in outline:
        if not isinstance(sec, dict):
            continue
        title = str(sec.get("title") or "").strip()
        if title:
            sections.append(title)
        for bullet in sec.get("bullets") or []:
            if isinstance(bullet, str) and bullet.strip():
                bullets.append(bullet.strip())
        for sub in sec.get("subsections") or []:
            if not isinstance(sub, dict):
                continue
            for bullet in sub.get("bullets") or []:
                if isinstance(bullet, str) and bullet.strip():
                    bullets.append(bullet.strip())
    return sections, bullets

