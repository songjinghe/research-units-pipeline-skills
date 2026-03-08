from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from tooling.common import atomic_write_text, ensure_dir, read_jsonl


DEFAULT_IDEA_RUBRIC: list[tuple[str, float, str]] = [
    ("feasibility", 0.25, "can a small team test it in ~1 week?"),
    ("novelty_delta", 0.20, "is there a clear delta vs nearest prior work?"),
    ("evidence_traceability", 0.20, "can we anchor it to existing papers and failure modes?"),
    ("evaluation_clarity", 0.20, "does it admit a clear task/metric/baseline?"),
    ("writeability", 0.10, "can it become a coherent short paper/report?"),
    ("portfolio_diversity", 0.05, "does the shortlist cover different clusters / idea types?"),
]

OPERATOR_FAMILIES: list[str] = [
    "Counterfactual / constraint flip",
    "Failure-mode-first",
    "Evaluation protocol swap",
    "Component swap in an agent loop",
    "Combination with explicit assumptions",
    "Cross-domain analogy import",
    "Negative-result mining",
    "System/product constraints",
]

STOPWORDS = {
    "a", "an", "and", "the", "of", "to", "for", "in", "on", "with", "via", "by", "from", "or",
    "work", "works", "study", "studies", "survey", "review", "benchmarks", "benchmark", "evaluation",
    "agents", "agent", "model", "models", "llm", "large", "language", "using", "based",
}


@dataclass(frozen=True)
class IdeaCard:
    idea_id: str
    tier: str
    operator: str
    cluster: str
    idea_type: str
    gap_type: str
    problem: str
    sharp_gap: str
    why_now: str
    candidate_wedge: str
    evidence_signal: str
    key_assumption: str
    falsification: str
    paper_ids: list[str]
    opportunity_ids: list[str]


@dataclass(frozen=True)
class ScreenedIdea:
    idea_id: str
    cluster: str
    idea_type: str
    operator: str
    total_score: float
    feasibility: int
    novelty_delta: int
    evidence_traceability: int
    evaluation_clarity: int
    writeability: int
    why_now: str
    keep: str
    rationale: str



def read_core_set(path: Path) -> list[dict[str, str]]:
    import csv

    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]



def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    ensure_dir(path.parent)
    lines = [json.dumps(row, ensure_ascii=False) for row in rows]
    atomic_write_text(path, "\n".join(lines).rstrip() + ("\n" if lines else ""))



def uniq_keep_order(items: Iterable[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        value = str(item or "").strip()
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out



def slugify(text: str) -> str:
    raw = re.sub(r"[^A-Za-z0-9]+", "-", str(text or "").strip().lower())
    return raw.strip("-") or "x"



def clean_text(text: str, *, limit: int = 220) -> str:
    s = str(text or "").strip()
    s = s.replace("\n", " ")
    s = re.sub(r"\s+", " ", s)
    s = s.replace("|", ", ")
    s = s.strip(" \"'`")
    if len(s) <= limit:
        return s
    clipped = s[:limit].rsplit(" ", 1)[0].strip()
    return clipped if clipped else s[:limit].strip()



def parse_markdown_table(md: str) -> list[dict[str, str]]:
    lines = [ln.rstrip() for ln in (md or "").splitlines()]
    header: list[str] | None = None
    rows: list[dict[str, str]] = []
    for idx, ln in enumerate(lines):
        if not ln.strip().startswith("|"):
            continue
        cols = [c.strip() for c in ln.strip().strip("|").split("|")]
        if idx + 1 < len(lines):
            nxt = lines[idx + 1].strip()
            if nxt.startswith("|") and re.fullmatch(r"\|?\s*:?-{3,}:?(\s*\|\s*:?-{3,}:?)+\s*\|?", nxt):
                header = cols
                continue
        if header and len(cols) == len(header):
            rows.append({header[i]: cols[i] for i in range(len(header))})
    return rows



def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = ["| " + " | ".join(str(cell).replace("\n", " ").strip() for cell in row) + " |" for row in rows]
    return "\n".join([head, sep] + body)



def extract_goal_from_goal_md(path: Path) -> str:
    if not path.exists():
        return "research ideas"
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8", errors="ignore").splitlines() if ln.strip() and not ln.startswith("#")]
    return lines[0] if lines else "research ideas"



def parse_idea_brief(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    out: dict[str, Any] = {
        "goal": extract_goal_from_goal_md(path),
        "focus_clusters": [],
        "query_buckets": [],
        "exclusions": [],
        "pool_min": 60,
        "pool_max": 90,
        "shortlist_size": 7,
        "constraints": [],
        "targets": {},
    }
    cur = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            cur = line[3:].strip().lower()
            continue
        if cur == "goal" and line.startswith("- Topic:"):
            out["goal"] = line.split(":", 1)[1].strip()
        if cur == "focus after c2" and line.startswith("- Focus clusters:"):
            out["focus_clusters"] = [x.strip() for x in line.split(":", 1)[1].split(";") if x.strip()]
        if cur == "query buckets" and re.match(r"^\d+\.\s+", line):
            out["query_buckets"].append(re.sub(r"^\d+\.\s+", "", line).strip())
        if cur == "exclude terms" and line.startswith("- "):
            out["exclusions"].append(line[2:].strip())
        if cur == "constraints" and line.startswith("- "):
            out["constraints"].append(line[2:].strip())
        if cur == "targets" and line.startswith("- ") and ":" in line:
            key, value = line[2:].split(":", 1)
            out["targets"][key.strip().lower().replace(" ", "_")] = value.strip()
    try:
        out["pool_min"] = int(re.findall(r"\d+", str(out["targets"].get("idea_pool_size") or "60"))[0])
    except Exception:
        out["pool_min"] = 60
    try:
        nums = re.findall(r"\d+", str(out["targets"].get("idea_pool_size") or "60-90"))
        out["pool_max"] = int(nums[-1]) if nums else 90
    except Exception:
        out["pool_max"] = 90
    try:
        out["shortlist_size"] = int(re.findall(r"\d+", str(out["targets"].get("final_shortlist_size") or "7"))[0])
    except Exception:
        out["shortlist_size"] = 7
    return out



def keywords_from_cluster(name: str) -> list[str]:
    toks = [t for t in re.findall(r"[A-Za-z0-9]+", str(name or "").lower()) if t not in STOPWORDS and len(t) > 2]
    return uniq_keep_order(toks)



def score_note_to_cluster(cluster_name: str, note: dict[str, Any]) -> int:
    keys = keywords_from_cluster(cluster_name)
    blob_parts = [str(note.get("title") or "")]
    for field in ["summary_bullets", "limitations", "key_results", "method"]:
        val = note.get(field)
        if isinstance(val, list):
            blob_parts.extend([str(x) for x in val])
        elif isinstance(val, str):
            blob_parts.append(val)
    blob = " ".join(blob_parts).lower()
    return sum(1 for key in keys if key in blob)



def map_notes_to_clusters(taxonomy_path: Path, notes_path: Path) -> dict[str, list[dict[str, Any]]]:
    import yaml

    taxonomy = yaml.safe_load(taxonomy_path.read_text(encoding="utf-8", errors="ignore")) if taxonomy_path.exists() else []
    notes = [r for r in read_jsonl(notes_path) if isinstance(r, dict)]
    out: dict[str, list[dict[str, Any]]] = {}
    for top in taxonomy or []:
        if not isinstance(top, dict):
            continue
        for child in top.get("children") or []:
            if not isinstance(child, dict):
                continue
            name = str(child.get("name") or "").strip()
            if not name:
                continue
            scored: list[tuple[int, dict[str, Any]]] = []
            for note in notes:
                s = score_note_to_cluster(name, note)
                if s > 0:
                    scored.append((s, note))
            scored.sort(key=lambda x: (-x[0], str(x[1].get("paper_id") or "")))
            out[name] = [n for _, n in scored[:10]]
    return out



def build_opportunity_rows(*, cluster: str, notes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not notes:
        return rows
    limitation_bits: list[tuple[str, str]] = []
    summary_bits: list[tuple[str, str]] = []
    for note in notes:
        pid = str(note.get("paper_id") or "").strip()
        title = str(note.get("title") or pid).strip()
        for lim in note.get("limitations") or []:
            txt = clean_text(lim, limit=180)
            if txt:
                limitation_bits.append((pid, txt))
        for sm in note.get("summary_bullets") or []:
            txt = clean_text(sm, limit=180)
            if txt:
                summary_bits.append((pid, txt))
        if not note.get("limitations"):
            limitation_bits.append((pid, f"Limited evidence extracted from {title}; unresolved assumptions should be tested explicitly."))
    gap_templates = [
        ("failure_mode", "failure mode the current papers mention but do not isolate cleanly"),
        ("protocol_gap", "evaluation protocol mismatch that could flip conclusions across settings"),
        ("artifact_gap", "missing artifact or benchmark slice needed to make the comparison executable"),
        ("boundary_gap", "scope boundary that papers acknowledge but do not test directly"),
    ]
    lim_src = limitation_bits[:6]
    sum_src = summary_bits[:6]
    for idx, (gap_type, prompt) in enumerate(gap_templates, start=1):
        refs = [pid for pid, _ in (lim_src if idx % 2 else sum_src)[:3]] or [pid for pid, _ in limitation_bits[:3]]
        signal = clean_text((lim_src[idx - 1][1] if idx - 1 < len(lim_src) else sum_src[idx - 1][1] if idx - 1 < len(sum_src) else f"The current literature around {cluster.lower()} still leaves a testable gap."), limit=160)
        rows.append(
            {
                "opportunity_id": f"{slugify(cluster)[:18]}-{idx}",
                "cluster": cluster,
                "gap_type": gap_type,
                "unresolved_gap": f"{cluster}: {prompt}",
                "evidence_signal": signal,
                "why_now": f"Recent papers around {cluster.lower()} make the comparison concrete enough for a bounded test rather than a survey-level discussion.",
                "candidate_wedge": f"Build a small benchmark, protocol slice, or intervention that isolates {cluster.lower()} under one controllable variable.",
                "paper_ids": uniq_keep_order(refs),
            }
        )
    return rows



def opportunity_table_markdown(rows: list[dict[str, Any]]) -> str:
    table_rows = []
    for row in rows:
        table_rows.append([
            row.get("opportunity_id", ""),
            row.get("cluster", ""),
            row.get("gap_type", ""),
            row.get("unresolved_gap", ""),
            row.get("evidence_signal", ""),
            row.get("why_now", ""),
            row.get("candidate_wedge", ""),
            ", ".join(row.get("paper_ids", [])),
        ])
    return "\n".join(
        [
            "# IDEA_OPPORTUNITY_TABLE",
            "",
            "## Opportunity Table",
            "",
            markdown_table(
                ["Opportunity ID", "Cluster", "Gap Type", "Unresolved Gap", "Evidence Signal", "Why now", "Candidate Wedge", "Evidence pointers"],
                table_rows,
            ),
            "",
        ]
    )



def rows_to_idea_cards(rows: list[dict[str, Any]], *, focus_clusters: list[str]) -> list[IdeaCard]:
    cards: list[IdeaCard] = []
    focus_set = {x.strip() for x in focus_clusters if str(x).strip()}
    operators = OPERATOR_FAMILIES
    for idx, row in enumerate(rows):
        cluster = str(row.get("cluster") or "").strip()
        for op_idx, operator in enumerate(operators):
            tier = "Tier-1 Plausible"
            if "failure" in str(row.get("gap_type") or "") or op_idx in {1, 2}:
                tier = "Tier-2 Ready"
            elif op_idx in {5}:
                tier = "Tier-0 Wild"
            idea_type = "evaluation"
            low = cluster.lower()
            if any(k in low for k in ["safety", "security", "governance"]):
                idea_type = "safety"
            elif any(k in low for k in ["tool", "interface", "orchestration"]):
                idea_type = "system-constraint"
            elif any(k in low for k in ["memory", "retrieval"]):
                idea_type = "mechanism"
            elif any(k in low for k in ["planning", "reasoning", "loop"]):
                idea_type = "mechanism"
            elif any(k in low for k in ["adaptation", "improvement"]):
                idea_type = "adaptation"
            elif any(k in low for k in ["coordination"]):
                idea_type = "coordination"
            gap_type = str(row.get("gap_type") or "gap").strip().replace("_", " ")
            wedge = clean_text(row.get("candidate_wedge") or f"Make the gap in {cluster.lower()} executable under one controllable variable.", limit=180)
            evidence_signal = clean_text(row.get("evidence_signal") or f"Recent papers in {cluster.lower()} point to an unresolved empirical or protocol issue.", limit=180)
            why_now = clean_text(row.get("why_now") or f"Recent papers in {cluster.lower()} make the gap concrete enough for a bounded experiment.", limit=180)
            sharp_gap = clean_text(row.get("unresolved_gap") or f"{cluster}: a still-undertested {gap_type}.", limit=180)

            problem = wedge
            if operator == "Failure-mode-first":
                problem = f"Start from {gap_type} evidence in {cluster.lower()} and design an experiment that scores recovery quality, not only end-task success."
            elif operator == "Evaluation protocol swap":
                problem = f"Hold the task fixed but swap metric, budget, or observability assumptions around {sharp_gap.lower()} to test whether reported winners stay stable."
            elif operator == "System/product constraints":
                problem = f"Turn the deployment constraint behind {sharp_gap.lower()} into the main experimental variable instead of leaving it as background context."
            elif operator == "Component swap in an agent loop":
                problem = f"Hold the broader pipeline fixed and swap only one local component tied to {sharp_gap.lower()} to identify which change actually moves reliability."
            elif operator == "Counterfactual / constraint flip":
                problem = f"Invert the key assumption behind {sharp_gap.lower()} and test whether the same conclusions still hold."
            elif operator == "Combination with explicit assumptions":
                problem = f"Combine two promising fixes for {sharp_gap.lower()} but make the enabling assumptions explicit and falsifiable from the start."
            elif operator == "Cross-domain analogy import":
                problem = f"Import a control, verification, or monitoring trick that could make {sharp_gap.lower()} testable in agent settings."
            elif operator == "Negative-result mining":
                problem = f"Mine a reproducible negative result around {sharp_gap.lower()} where a popular strategy fails under realistic conditions."
            refs = row.get("paper_ids") or []
            cards.append(
                IdeaCard(
                    idea_id=f"IP-{idx+1:03d}-{op_idx+1}",
                    tier=tier,
                    operator=operator,
                    cluster=cluster,
                    idea_type=idea_type,
                    gap_type=gap_type,
                    problem=clean_text(problem, limit=180),
                    sharp_gap=sharp_gap,
                    why_now=why_now,
                    candidate_wedge=wedge,
                    evidence_signal=evidence_signal,
                    key_assumption=f"{evidence_signal} This suggests the unresolved {gap_type} in {cluster.lower()} is large enough that changing one explicit variable should expose materially different outcomes.",
                    falsification=f"If the new setup does not change diagnosis, ranking, or failure profile relative to the baseline framing for {sharp_gap.lower()}, the idea is too weak.",
                    paper_ids=uniq_keep_order(refs)[:4],
                    opportunity_ids=[str(row.get("opportunity_id") or "")],
                )
            )
    # Keep focus-aligned ideas first.
    cards.sort(key=lambda c: (0 if c.cluster in focus_set else 1, c.tier, c.cluster, c.operator, c.idea_id))
    return cards



def idea_pool_markdown(cards: list[IdeaCard]) -> str:
    rows: list[list[str]] = []
    for card in cards:
        rows.append([
            card.idea_id,
            card.tier,
            card.operator,
            card.cluster,
            card.idea_type,
            card.problem,
            card.sharp_gap,
            card.key_assumption,
            card.falsification,
            ", ".join(card.paper_ids),
            ", ".join(card.opportunity_ids),
        ])
    return "\n".join(
        [
            "# IDEA_POOL",
            "",
            "## Pool Table",
            "",
            markdown_table(
                ["Idea ID", "Tier", "Operator", "Cluster", "Idea Type", "Problem", "Sharp Gap", "Key Assumption", "How to Falsify", "Paper IDs", "Opportunity IDs"],
                rows,
            ),
            "",
        ]
    )



def score_idea_cards(cards: list[IdeaCard], *, focus_clusters: list[str]) -> list[ScreenedIdea]:
    focus_set = {x.strip() for x in focus_clusters if str(x).strip()}
    rows: list[ScreenedIdea] = []
    for idx, card in enumerate(cards):
        feasibility = 5 if card.tier == "Tier-2 Ready" else 4 if card.tier == "Tier-1 Plausible" else 2
        novelty = 4 if "swap" in card.operator.lower() or "negative" in card.operator.lower() else 3
        evidence = 5 if len(card.paper_ids) >= 3 else 4 if len(card.paper_ids) >= 2 else 2
        eval_clarity = 5 if any(k in card.problem.lower() for k in ["benchmark", "protocol", "metric", "variable", "failure", "recovery"]) else 3
        writeability = 5 if card.cluster in focus_set else 4
        why_now = "The current paper set already exposes the gap clearly enough to support a bounded first experiment."
        bonus = 0.25 if card.cluster in focus_set else 0.0
        total = feasibility * 0.25 + novelty * 0.20 + evidence * 0.20 + eval_clarity * 0.20 + writeability * 0.10 + bonus
        keep = "keep" if idx < 18 else "maybe" if idx < 30 else "drop"
        rationale = "strong fit to brief and evidence" if keep == "keep" else "interesting but weaker wedge" if keep == "maybe" else "too broad or redundant for the first shortlist"
        rows.append(
            ScreenedIdea(
                idea_id=card.idea_id,
                cluster=card.cluster,
                idea_type=card.idea_type,
                operator=card.operator,
                total_score=round(total, 2),
                feasibility=feasibility,
                novelty_delta=novelty,
                evidence_traceability=evidence,
                evaluation_clarity=eval_clarity,
                writeability=writeability,
                why_now=why_now,
                keep=keep,
                rationale=rationale,
            )
        )
    rows.sort(key=lambda r: (-r.total_score, r.keep != "keep", r.cluster, r.idea_id))
    return rows



def screening_table_markdown(rows: list[ScreenedIdea]) -> str:
    data: list[list[str]] = []
    for row in rows:
        data.append([
            row.idea_id,
            row.cluster,
            row.idea_type,
            row.operator,
            f"{row.total_score:.2f}",
            str(row.feasibility),
            str(row.novelty_delta),
            str(row.evidence_traceability),
            str(row.evaluation_clarity),
            str(row.writeability),
            row.keep,
            row.rationale,
        ])
    return "\n".join(
        [
            "# IDEA_SCREENING_TABLE",
            "",
            "## Screening Table",
            "",
            markdown_table(
                [
                    "Idea ID",
                    "Cluster",
                    "Idea Type",
                    "Operator",
                    "Total",
                    "Feasibility",
                    "Novelty",
                    "Evidence",
                    "Eval Clarity",
                    "Writeability",
                    "Keep?",
                    "Rationale",
                ],
                data,
            ),
            "",
        ]
    )



def write_markdown(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    atomic_write_text(path, text.rstrip() + "\n")



def collect_note_index(notes_path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for rec in read_jsonl(notes_path):
        if not isinstance(rec, dict):
            continue
        pid = str(rec.get("paper_id") or "").strip()
        if pid:
            out[pid] = rec
    return out
