from __future__ import annotations

import re


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


def split_sentences(text: str) -> list[str]:
    clean = re.sub(r"\s+", " ", str(text or "").strip())
    if not clean:
        return []
    parts = re.split(r"(?<=[.!?])\s+", clean)
    return [part.strip() for part in parts if part.strip()]


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
            out.append({"section": section, "page": page, "sentence": sentence})
    return out


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
        section_low = item["section"].lower()
        if section_low in {"abstract", "introduction"}:
            score += 3
        elif section_low in {"experiments", "results", "conclusion"}:
            score += 1
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


def text_tokens(value: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", str(value or "").lower()) if len(token) >= 3}


def extract_related_works(text: str) -> list[str]:
    lines = (text or "").splitlines()
    in_refs = False
    works: list[str] = []
    for raw in lines:
        line = raw.strip()
        if line.lower().startswith("## references") or line.lower().startswith("# references"):
            in_refs = True
            continue
        if in_refs and line.startswith("## "):
            break
        if in_refs and line.startswith("- "):
            works.append(line[2:].strip())
    return works
