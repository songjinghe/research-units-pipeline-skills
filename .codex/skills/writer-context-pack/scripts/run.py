from __future__ import annotations

import argparse
import json
import hashlib
import re
import sys
from pathlib import Path
from typing import Any

_URL_RE = re.compile(r"https?://\S+")
_AVAILABILITY_VERB_RE = re.compile(
    r"(?i)\b(?:is|are|was|were|will\s+be|can\s+be|has\s+been)?\s*(?:publicly\s+)?(?:available|released|open-?sourced|shared)\b"
)
_LEADING_SELF_REF_RE = re.compile(
    r"(?i)^(?:to (?:address|overcome|tackle|mitigate|study|investigate|examine|understand|analyze|explore|bridge)[^,]{0,180},\s*)?"
    r"(?:(?:in|throughout)\s+(?:this|our)\s+(?:survey|paper|work|study|article),?\s*)?"
)
_LEADING_CONTEXT_RE = re.compile(
    r"(?i)^(?:building on this foundation|against this backdrop|in this context|to this end|towards this end|specifically|for example|based on this proposition|throughout [^,]{1,120}|moreover|furthermore|additionally),?\s*"
)
_LEADING_AUTHOR_FINDING_RE = re.compile(
    r"(?i)^(?:we|our\s+(?:results|analysis|study|evaluations?|experiments?))\s+"
    r"(?:show|shows|find|finds|observe|observes|demonstrate|demonstrates|quantify|quantifies|reveal|reveals|indicate|indicates)\s+that\s+"
)
_LEADING_AUTHOR_PREDICATE_RE = re.compile(
    r"(?i)^(?:we|our\s+(?:results|analysis|study|evaluations?|experiments?))\s+"
    r"(?:show|shows|find|finds|observe|observes|demonstrate|demonstrates|reveal|reveals|indicate|indicates)\s+"
)
_LEADING_AUTHOR_ACTION_RE = re.compile(
    r"(?i)^(?:here,\s*)?(?:we|our\s+(?:results|analysis|study|evaluations?|experiments?))\s+"
    r"(?:(?:also|broadly|comprehensively)\s+)?"
    r"(?:introduce|present|propose|develop|describe|compare|conduct|discuss|summarize|review|explore|analyze|evaluate|quantify|study|design|build|construct|divide)\b[^,]{0,160},\s*"
)
_LEADING_PARTICIPLE_RE = re.compile(
    r"(?i)^(?:demonstrating|showing|finding|observing|revealing|indicating|suggesting)\s+that\s+"
)
_FRAGMENT_PARTICIPLE_RE = re.compile(r"(?i)^(?:demonstrating|showing|revealing|highlighting|indicating)\b")
_PROMISSORY_SELF_NARRATION_RE = re.compile(
    r"(?i)^(?:we\s+hope|we\s+aim|our\s+(?:survey|paper|work|study)\s+aims?|this\s+(?:survey|paper|work|study)\s+aims?)\b"
)
_LEADING_DISCOURSE_RE = re.compile(r"(?i)^(?:moreover|furthermore|additionally|in addition),\s*")
_POST_ACTION_ARTIFACT_RE = re.compile(r"^([A-Z][A-Za-z0-9._-]{1,80}),\s+(.*)$")
_NAMED_ARTIFACT_RE = re.compile(
    r"(?i)^(?:here,\s*)?(?:we|the authors)\s+(?:introduce|present|propose|develop|describe)\s+([A-Z][A-Za-z0-9][^,.;:]{0,120}),\s+(.*)$"
)
_GENERIC_SELF_NARRATION_RE = re.compile(
    r"(?i)^(?:here,\s*)?(?:we|our)\s+"
    r"(?:(?:also|broadly|comprehensively)\s+)?"
    r"(?:introduce|present|propose|develop|describe|compare|conduct|discuss|summarize|review|explore|analyze|evaluate|study|design|build|construct|divide)\b"
)
_STUDY_SELF_NARRATION_RE = re.compile(r"(?i)^(?:this|our)\s+(?:survey|paper|work|study|article)\b")


def _backup_existing(path: Path) -> None:
    from tooling.common import backup_existing

    backup_existing(path)


def _trim(text: str, *, max_len: int = 400) -> str:
    """Normalize whitespace and trim without adding ellipsis (avoid leakage into prose)."""

    text = re.sub(r"\s+", " ", str(text or "").strip())
    max_len = int(max_len)
    if len(text) <= max_len:
        return text

    cut = text[:max_len].rstrip()
    # Avoid cutting a token in half.
    tail = cut[-60:]
    if " " in tail:
        cut = cut.rsplit(" ", 1)[0].rstrip()
    return cut


def _is_availability_boilerplate(text: str) -> bool:
    s = re.sub(r"\s+", " ", str(text or "").strip())
    if not s:
        return True
    low = s.lower()
    has_link = bool(_URL_RE.search(s))
    mentions_artifact = bool(
        re.search(
            r"(?i)\b(?:project\s+(?:website|site|web\s*page|page)|website|site|web\s*page|repository|repo|code|dataset|data|collection|resources?)\b",
            s,
        )
    )
    if has_link and mentions_artifact:
        return True
    if re.search(r"(?i)\b(?:encourage|invite)\s+readers?\b", s) and mentions_artifact:
        return True
    if re.search(r"(?i)\b(?:view|visit|see|consult|check)\b", s) and re.search(r"(?i)\b(?:github|repository|repo|website|project\s+site)\b", s):
        return True
    if re.search(r"(?i)\bour\s+(?:living\s+)?(?:github\s+)?repository\b", s):
        return True
    if "available at" in low or "can be found at" in low:
        return mentions_artifact or has_link
    if re.search(r"(?i)\b(?:our|the)\s+(?:code|project|repository|repo|dataset|data|collection|resources?)\b", s):
        return has_link or bool(_AVAILABILITY_VERB_RE.search(s))
    if re.search(r"(?i)\b(?:code|dataset|data|collection|resources?)\b", s) and _AVAILABILITY_VERB_RE.search(s):
        return True
    return False


def _sanitize_source_sentence(text: str) -> str:
    s = re.sub(r"\s+", " ", str(text or "").strip())
    if not s:
        return ""
    if _is_availability_boilerplate(s):
        return ""

    s = _URL_RE.sub("", s)
    s = re.sub(r"\s+([,.;:])", r"\1", s)
    s = re.sub(r"\(\s*\)", "", s)
    s = re.sub(r"\s{2,}", " ", s).strip(" ,;:")
    s = _LEADING_CONTEXT_RE.sub("", s)
    s = _LEADING_DISCOURSE_RE.sub("", s)
    s = _LEADING_SELF_REF_RE.sub("", s)
    s = _LEADING_AUTHOR_FINDING_RE.sub("", s)
    s = _LEADING_AUTHOR_PREDICATE_RE.sub("", s)
    s = _LEADING_AUTHOR_ACTION_RE.sub("", s)
    s = _LEADING_PARTICIPLE_RE.sub("", s)

    if _PROMISSORY_SELF_NARRATION_RE.match(s) or _FRAGMENT_PARTICIPLE_RE.match(s):
        return ""

    m = _NAMED_ARTIFACT_RE.match(s)
    if m:
        name = re.sub(r"\s+", " ", m.group(1).strip(" ,;:"))
        rest = re.sub(r"\s+", " ", m.group(2).strip(" ,;:"))
        if rest and re.match(r"(?i)^(?:a|an|the|one|\d+)\b", rest):
            s = f"{name} is {rest}"
        elif rest:
            s = f"{name}: {rest}"
        else:
            s = name
    elif _STUDY_SELF_NARRATION_RE.match(s) or _GENERIC_SELF_NARRATION_RE.match(s):
        return ""

    artifact_match = _POST_ACTION_ARTIFACT_RE.match(s)
    if artifact_match:
        name = artifact_match.group(1).strip()
        rest = artifact_match.group(2).strip()
        if rest and re.match(r"(?i)^(?:a|an|the|one|\d+)\b", rest):
            s = f"{name} is {rest}"
        elif rest:
            s = f"{name}: {rest}"

    if s:
        s = s[:1].upper() + s[1:]
    s = re.sub(r"\s{2,}", " ", s).strip(" ,;:")
    if len(s) < 16:
        return ""
    if s[-1] not in ".!?":
        s = f"{s}."
    return s


def _sanitize_source_text(text: str) -> str:
    raw = re.sub(r"\s+", " ", str(text or "").strip())
    if not raw:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", raw)
    if not parts:
        parts = [raw]

    out: list[str] = []
    seen: set[str] = set()
    for part in parts:
        cleaned = _sanitize_source_sentence(part)
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(cleaned)
    return " ".join(out).strip()


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists() or path.stat().st_size <= 0:
        return []
    out: list[dict[str, Any]] = []
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


def _bib_keys(bib_path: Path) -> set[str]:
    text = bib_path.read_text(encoding="utf-8", errors="ignore") if bib_path.exists() else ""
    return set(re.findall(r"(?im)^@\w+\s*\{\s*([^,\s]+)\s*,", text))




def _normalize_cite_keys(citations: Any, *, bibkeys: set[str]) -> list[str]:
    # Normalize citation keys to raw BibTeX keys (no @ prefix).
    # Tolerates: @Key, [@Key], Key, and semicolon/comma-separated strings.

    out: list[str] = []
    if not isinstance(citations, list):
        return out

    for c in citations:
        s = str(c or "").strip()
        if not s:
            continue
        if s.startswith("[") and s.endswith("]"):
            s = s[1:-1].strip()
        if s.startswith("@"):  # tolerate @Key
            s = s[1:].strip()

        # Split multi-key strings best-effort (e.g., "@a; @b").
        for k in re.findall(r"[A-Za-z0-9:_-]+", s.replace("@", " ")):
            k = k.strip()
            if not k:
                continue
            if bibkeys and k not in bibkeys:
                continue
            if k not in out:
                out.append(k)

    return out
def _stable_choice(key: str, options: list[str]) -> str:
    if not options:
        return ""
    digest = hashlib.sha1((key or "").encode("utf-8", errors="ignore")).hexdigest()
    return options[int(digest[:8], 16) % len(options)]


def _iter_outline_subsections(outline: Any) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    if not isinstance(outline, list):
        return out
    for sec in outline:
        if not isinstance(sec, dict):
            continue
        sec_id = str(sec.get("id") or "").strip()
        sec_title = str(sec.get("title") or "").strip()
        for sub in sec.get("subsections") or []:
            if not isinstance(sub, dict):
                continue
            sub_id = str(sub.get("id") or "").strip()
            title = str(sub.get("title") or "").strip()
            if sec_id and sec_title and sub_id and title:
                out.append({"sub_id": sub_id, "title": title, "section_id": sec_id, "section_title": sec_title})
    return out


def _draft_profile(workspace: Path) -> str:
    """Best-effort parse from `queries.md` (survey|deep)."""

    path = workspace / "queries.md"
    if not path.exists():
        return "survey"
    keys = {"draft_profile", "writing_profile", "quality_profile"}
    try:
        for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if not line.startswith("- ") or ":" not in line:
                continue
            key, value = line[2:].split(":", 1)
            key = key.strip().lower().replace(" ", "_")
            if key not in keys:
                continue
            value = value.split("#", 1)[0].strip().strip('"').strip("'").strip().lower()
            if value in {"survey", "deep"}:
                return value
            return "survey"
    except Exception:
        return "survey"
    return "survey"



def _load_voice_palette(*, workspace: Path, repo_root: Path) -> dict[str, Any]:
    """Load a paper-voice palette used by writer packs.

    Precedence (most specific first):
    - Workspace override: outline/paper_voice_palette.json
    - Repo default: .codex/skills/writer-context-pack/assets/paper_voice_palette.json

    Keep this file small and semantic: it is a rewrite guide, not a prose template.
    """

    candidates = [
        workspace / 'outline' / 'paper_voice_palette.json',
        repo_root / '.codex' / 'skills' / 'writer-context-pack' / 'assets' / 'paper_voice_palette.json',
    ]

    for p in candidates:
        try:
            if not p.exists() or p.stat().st_size <= 0:
                continue
            data = json.loads(p.read_text(encoding='utf-8', errors='ignore'))
            if isinstance(data, dict):
                return data
        except Exception:
            continue

    return {}

def _assert_h3_cutover_ready(*, workspace: Path, consumer: str) -> None:
    from tooling.common import read_jsonl

    state_path = workspace / "outline" / "outline_state.jsonl"
    if not state_path.exists() or state_path.stat().st_size <= 0:
        return

    records = [rec for rec in read_jsonl(state_path) if isinstance(rec, dict)]
    if not records:
        return

    latest = records[-1]
    cutover_keys = {"structure_phase", "h3_status", "approval_status", "reroute_target", "retry_budget_remaining"}
    if not any(key in latest for key in cutover_keys):
        return

    h3_status = str(latest.get("h3_status") or "").strip().lower()
    if h3_status == "stable":
        return

    structure_phase = str(latest.get("structure_phase") or "").strip() or "unknown"
    reroute_target = str(latest.get("reroute_target") or "").strip() or "none"
    raise SystemExit(
        f"{consumer} is blocked until stable H3 ids exist: "
        f"`outline/outline_state.jsonl` reports h3_status={h3_status or 'missing'} "
        f"(structure_phase={structure_phase}, reroute_target={reroute_target})."
    )


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

    from tooling.common import ensure_dir, latest_outline_state, load_workspace_pipeline_spec, load_yaml, now_iso_seconds, parse_semicolon_list, write_jsonl
    from tooling.quality_gate import _global_citation_min_subsections

    workspace = Path(args.workspace).resolve()
    spec = load_workspace_pipeline_spec(workspace)
    if spec is not None and str(spec.structure_mode or "").strip() == "section_first":
        state = latest_outline_state(workspace)
        if not state:
            raise SystemExit("Missing outline_state.jsonl; run the section-first C2 planner pass before writer-context-pack.")
        if str(state.get("structure_phase") or "").strip() != "decomposed" or str(state.get("h3_status") or "").strip() != "stable":
            raise SystemExit("Section-first cutover not ready: `outline_state.jsonl` must report `structure_phase: decomposed` and `h3_status: stable` before writer-context-pack.")

    inputs = parse_semicolon_list(args.inputs) or [
        "outline/outline.yml",
        "outline/subsection_briefs.jsonl",
        "outline/chapter_briefs.jsonl",
        "outline/evidence_drafts.jsonl",
        "outline/anchor_sheet.jsonl",
        "outline/evidence_bindings.jsonl",
        "citations/ref.bib",
    ]
    outputs = parse_semicolon_list(args.outputs) or ["outline/writer_context_packs.jsonl"]

    outline_path = workspace / inputs[0]
    briefs_path = workspace / inputs[1]
    chapter_path = workspace / inputs[2]
    packs_path = workspace / inputs[3]
    anchors_path = workspace / inputs[4]
    bindings_path = workspace / inputs[5]
    bib_path = workspace / inputs[6]

    out_path = workspace / (outputs[0] if outputs else "outline/writer_context_packs.jsonl")
    ensure_dir(out_path.parent)

    freeze_marker = out_path.parent / "writer_context_packs.refined.ok"
    if out_path.exists() and out_path.stat().st_size > 0 and freeze_marker.exists():
        return 0
    if out_path.exists() and out_path.stat().st_size > 0:
        _backup_existing(out_path)

    _assert_h3_cutover_ready(workspace=workspace, consumer="writer-context-pack")

    outline = load_yaml(outline_path) if outline_path.exists() else []
    subsections = _iter_outline_subsections(outline)
    if not subsections:
        raise SystemExit(f"No H3 subsections found in {outline_path}")

    bibkeys = _bib_keys(bib_path)

    briefs_by_sub: dict[str, dict[str, Any]] = {}
    for rec in _load_jsonl(briefs_path):
        sid = str(rec.get("sub_id") or "").strip()
        if sid:
            briefs_by_sub[sid] = rec

    chapters_by_sec: dict[str, dict[str, Any]] = {}
    for rec in _load_jsonl(chapter_path):
        sec_id = str(rec.get("section_id") or "").strip()
        if sec_id:
            chapters_by_sec[sec_id] = rec

    packs_by_sub: dict[str, dict[str, Any]] = {}
    for rec in _load_jsonl(packs_path):
        sid = str(rec.get("sub_id") or "").strip()
        if sid:
            packs_by_sub[sid] = rec

    anchors_by_sub: dict[str, list[dict[str, Any]]] = {}
    for rec in _load_jsonl(anchors_path):
        sid = str(rec.get("sub_id") or "").strip()
        anchors = rec.get("anchors") or []
        if sid and isinstance(anchors, list):
            anchors_by_sub[sid] = [a for a in anchors if isinstance(a, dict)]

    bindings_by_sub: dict[str, dict[str, Any]] = {}
    for rec in _load_jsonl(bindings_path):
        sid = str(rec.get("sub_id") or "").strip()
        if sid:
            bindings_by_sub[sid] = rec

    # Chapter-scoped union of mapped bibkeys.
    chapter_union: dict[str, set[str]] = {}
    for sub in subsections:
        sid = sub["sub_id"]
        sec_id = sub["section_id"]
        mapped = (bindings_by_sub.get(sid) or {}).get("mapped_bibkeys") or []
        if not isinstance(mapped, list):
            continue
        bucket = chapter_union.setdefault(sec_id, set())
        for bk in mapped:
            bk = str(bk).strip()
            if bk and (not bibkeys or bk in bibkeys):
                bucket.add(bk)

    # Global bibkeys: mapped across multiple subsections (cross-cutting foundations/benchmarks/surveys).
    mapped_counts: dict[str, int] = {}
    for rec in bindings_by_sub.values():
        mapped = rec.get("mapped_bibkeys") or []
        if not isinstance(mapped, list):
            continue
        for bk in mapped:
            bk = str(bk).strip()
            if not bk:
                continue
            if bibkeys and bk not in bibkeys:
                continue
            mapped_counts[bk] = mapped_counts.get(bk, 0) + 1
    global_threshold = _global_citation_min_subsections(workspace)
    mapped_global = sorted([k for k, n in mapped_counts.items() if n >= int(global_threshold)])

    # Trim policy (avoid silent truncation; keep long enough to preserve concrete detail).
    TRIM = {
        "default": 400,
        "anchor_fact": 420,
        "highlight_excerpt": 280,
        "comparison_write_prompt": 420,
        "eval_bullet": 320,
        "limitation_excerpt": 320,
    }

    # Paper voice palette is data-driven (semantic), not hard-coded.
    # Users may override per-workspace via `outline/paper_voice_palette.json`.
    palette = _load_voice_palette(workspace=workspace, repo_root=repo_root)

    forbidden = [str(x).strip() for x in (palette.get('forbidden_pipeline_voice') or []) if str(x).strip()]
    high_risk = [str(x).strip() for x in (palette.get('high_risk_templates') or []) if str(x).strip()]

    # Back-compat: keep a single flat list for writers that expect `do_not_repeat_phrases`.
    # Treat `forbidden` as hard (must not appear). Treat `high_risk` as rewrite triggers.
    DO_NOT_REPEAT = list(dict.fromkeys(forbidden + high_risk))

    # Positive guidance (paper voice): small phrase palettes + rewrite stems.
    # Keep these semantic and short; the draft must not read like template narration.
    PAPER_VOICE_PALETTE = {
        'forbidden_pipeline_voice': forbidden,
        'high_risk_templates': high_risk,
        'opener_archetypes': palette.get('opener_archetypes') or {
            'tension-first': ['A key tension is', 'The central trade-off is', 'A recurring constraint is'],
            'decision-first': ['For system builders, the crux is', 'A practical decision is', 'One design choice is'],
            'lens-first': ['Seen through the lens of', 'From the perspective of', 'Under an interface contract,'],
        },
        'synthesis_stems': palette.get('synthesis_stems')
        or ['Across these studies,', 'Collectively,', 'In summary,', 'The evidence suggests that', 'A consistent theme is that'],
        'rewrite_rules': palette.get('rewrite_rules')
        or [
            {'avoid_stem': 'This subsection surveys', 'prefer_stem': 'A key tension is'},
            {'avoid_stem': 'In this subsection', 'prefer_stem': 'We focus on'},
            {'avoid_stem': 'Next, we move', 'prefer_stem': 'Having established'},
            {'avoid_stem': 'We now turn', 'prefer_stem': 'We then examine'},
            {'avoid_stem': 'survey comparisons should', 'prefer_stem': 'Across protocols, we observe'},
        ],
        "discourse_stem_watchlist": [str(x).strip() for x in (palette.get("discourse_stem_watchlist") or []) if str(x).strip()],
        "discourse_stem_rewrites": palette.get("discourse_stem_rewrites") or {},
        "role_cards": palette.get("role_cards") or {},
        "version": str(palette.get("version") or "").strip(),
    }

    records: list[dict[str, Any]] = []
    now = now_iso_seconds()
    draft_profile = _draft_profile(workspace)

    for sub in subsections:
        sid = sub["sub_id"]
        title = sub["title"]
        sec_id = sub["section_id"]
        sec_title = sub["section_title"]

        brief = briefs_by_sub.get(sid) or {}
        pack = packs_by_sub.get(sid) or {}
        binding = bindings_by_sub.get(sid) or {}
        chapter = chapters_by_sec.get(sec_id) or {}

        rq = str(brief.get("rq") or "").strip()
        thesis = str(brief.get("thesis") or "").strip()
        axes = [str(a).strip() for a in (brief.get("axes") or []) if str(a).strip()]
        paragraph_plan = brief.get("paragraph_plan") or []

        tension_statement = str(brief.get("tension_statement") or "").strip()
        eval_anchor = brief.get("evaluation_anchor_minimal") or {}
        if not isinstance(eval_anchor, dict):
            eval_anchor = {}

        mapped = [str(x).strip() for x in (binding.get("mapped_bibkeys") or []) if str(x).strip()]
        selected = [str(x).strip() for x in (binding.get("bibkeys") or []) if str(x).strip()]
        mapped = [k for k in mapped if (not bibkeys or k in bibkeys)]
        selected = [k for k in selected if (not bibkeys or k in bibkeys)]

        # Anchor facts (evidence hooks).
        anchors_raw = anchors_by_sub.get(sid) or []
        anchor_facts: list[dict[str, Any]] = []
        anchors_considered = 0
        anchors_dropped_no_cites = 0
        anchors_dropped_sanitized = 0

        raw_limit = 16
        keep_limit = 12 if draft_profile == "deep" else 10

        for a in anchors_raw[:raw_limit]:
            anchors_considered += 1
            cites = _normalize_cite_keys(a.get("citations") or [], bibkeys=bibkeys)
            if not cites:
                anchors_dropped_no_cites += 1
                continue
            text = _sanitize_source_text(a.get("text") or "")
            if not text:
                anchors_dropped_sanitized += 1
                continue

            anchor_facts.append(
                {
                    "hook_type": str(a.get("hook_type") or "").strip(),
                    "text": _trim(text, max_len=TRIM["anchor_fact"]),
                    "citations": cites,
                    "paper_id": str(a.get("paper_id") or "").strip(),
                    "evidence_id": str(a.get("evidence_id") or "").strip(),
                    "pointer": str(a.get("pointer") or "").strip(),
                }
            )

            if len(anchor_facts) >= keep_limit:
                break

        # Comparison cards (A-vs-B contrasts).
        raw_comparisons = pack.get("concrete_comparisons") or []
        comparisons_considered = 0
        comparisons_dropped_no_highlights = 0
        hl_dropped_no_cites = 0
        hl_dropped_sanitized = 0

        comparison_cards: list[dict[str, Any]] = []
        comp_raw_limit = 14
        comp_keep_limit = 9 if draft_profile == "deep" else 7

        for comp in (raw_comparisons or [])[:comp_raw_limit]:
            if not isinstance(comp, dict):
                continue
            comparisons_considered += 1

            cites = _normalize_cite_keys(comp.get("citations") or [], bibkeys=bibkeys)

            def _hl(side: str) -> list[dict[str, Any]]:
                nonlocal hl_dropped_no_cites, hl_dropped_sanitized
                out: list[dict[str, Any]] = []
                for hl in (comp.get(side) or [])[:3]:
                    if not isinstance(hl, dict):
                        continue
                    hcites = _normalize_cite_keys(hl.get("citations") or [], bibkeys=bibkeys)
                    if not hcites:
                        hl_dropped_no_cites += 1
                        continue
                    excerpt = _sanitize_source_text(hl.get("excerpt") or "")
                    if not excerpt:
                        hl_dropped_sanitized += 1
                        continue
                    out.append(
                        {
                            "paper_id": str(hl.get("paper_id") or "").strip(),
                            "evidence_id": str(hl.get("evidence_id") or "").strip(),
                            "excerpt": _trim(excerpt, max_len=TRIM["highlight_excerpt"]),
                            "citations": hcites,
                            "pointer": str(hl.get("pointer") or "").strip(),
                        }
                    )
                return out

            card = {
                "axis": str(comp.get("axis") or "").strip(),
                "A_label": str(comp.get("A_label") or "").strip(),
                "B_label": str(comp.get("B_label") or "").strip(),
                "citations": cites,
                "A_highlights": _hl("A_highlights"),
                "B_highlights": _hl("B_highlights"),
                "write_prompt": _trim(comp.get("write_prompt") or "", max_len=TRIM["comparison_write_prompt"]),
            }
            if card["axis"] and (card["A_highlights"] or card["B_highlights"] or card["citations"]):
                comparison_cards.append(card)
            else:
                comparisons_dropped_no_highlights += 1

            if len(comparison_cards) >= comp_keep_limit:
                break

        # Evaluation protocol bullets.
        raw_eval = pack.get("evaluation_protocol") or []
        eval_considered = 0
        eval_dropped_no_cites = 0

        eval_token_list_style = False

        eval_proto: list[dict[str, Any]] = []
        for it in (raw_eval or [])[:10]:
            if not isinstance(it, dict):
                continue
            eval_considered += 1
            cites = _normalize_cite_keys(it.get("citations") or [], bibkeys=bibkeys)
            if not cites:
                eval_dropped_no_cites += 1
                continue
            bullet = _trim(it.get("bullet") or "", max_len=TRIM["eval_bullet"])
            if re.match(r"(?i)^evaluation tokens mentioned in mapped evidence:\s*", bullet):
                eval_token_list_style = True
                bullet = re.sub(r"(?i)^evaluation tokens mentioned in mapped evidence:\s*", "Evaluation mentions include: ", bullet)
                bullet = bullet.replace(";", ",")
                bullet = re.sub(r"\s+,", ",", bullet)
                bullet = re.sub(r"\s{2,}", " ", bullet).strip()
            eval_proto.append({"bullet": bullet, "citations": cites})
            if len(eval_proto) >= 8:
                break

        # Failure/limitation hooks.
        raw_lim = pack.get("failures_limitations") or []
        lim_considered = 0
        lim_dropped_no_cites = 0
        lim_dropped_sanitized = 0

        lim_hooks: list[dict[str, Any]] = []
        for it in (raw_lim or [])[:14]:
            if not isinstance(it, dict):
                continue
            lim_considered += 1
            cites = _normalize_cite_keys(it.get("citations") or [], bibkeys=bibkeys)
            if not cites:
                lim_dropped_no_cites += 1
                continue
            # `evidence-draft` uses `bullet` (not `excerpt`) for failures/limitations.
            text = it.get("excerpt") or it.get("bullet") or it.get("text") or ""
            excerpt = _sanitize_source_text(text)
            if not excerpt:
                lim_dropped_sanitized += 1
                continue
            lim_hooks.append(
                {
                    "excerpt": _trim(excerpt, max_len=TRIM["limitation_excerpt"]),
                    "citations": cites,
                    "pointer": str(it.get("pointer") or "").strip(),
                }
            )
            if len(lim_hooks) >= (10 if draft_profile == "deep" else 8):
                break

        # Availability minima (used by gates and self-loops).
        if draft_profile == "deep":
            min_anchor = 12
            min_comp = 9
            min_lim = 3
        else:
            min_anchor = 10
            min_comp = 7
            min_lim = 3

        # Writer-executable minima: smaller than availability minima, but still forces real argument moves.
        # A150++ (survey deliverable) expects denser packs; keep the writer minima non-trivial so drafting
        # does not collapse into per-paper summaries.
        if draft_profile == "deep":
            must_anchor = 6
            must_comp = 6
            must_lim = 3
        else:
            must_anchor = 5
            must_comp = 5
            must_lim = 3

        must_use = {
            "min_anchor_facts": must_anchor,
            "min_comparison_cards": must_comp,
            "min_limitation_hooks": must_lim,
            "require_cited_numeric_if_available": True,
            "require_multi_cite_synthesis_paragraph": True,
            "thesis_required": True,
        }

        pack_warnings: list[str] = []
        if not thesis:
            pack_warnings.append(
                "Missing `thesis` in subsection briefs; fix `subsection-briefs` so the writer has a central claim to execute."
            )
        if eval_token_list_style:
            pack_warnings.append(
                "Evaluation protocol bullets are token-list style; avoid copying them as sentences. Prefer subsection-specific benchmarks/metrics from `anchor_facts` and state task/metric/constraint explicitly."
            )
        if len(anchor_facts) < min_anchor:
            pack_warnings.append(
                "Too few anchor facts after trimming; strengthen `anchor-sheet` or upstream evidence packs to avoid generic prose."
            )
        if len(comparison_cards) < min_comp:
            pack_warnings.append(
                "Too few comparison cards after trimming; strengthen `evidence-draft` (excerpt-level A-vs-B contrasts) to avoid per-paper summaries."
            )
        if len(eval_proto) < 1:
            pack_warnings.append(
                "Missing evaluation protocol bullets; strengthen `evidence-draft` so the writer can anchor comparisons to benchmarks/metrics."
            )
        if len(lim_hooks) < min_lim:
            pack_warnings.append(
                "Too few limitation hooks; strengthen `evidence-draft` so limitations are concrete (not generic future work)."
            )

        if anchors_considered and anchors_dropped_no_cites / max(1, anchors_considered) >= 0.5:
            pack_warnings.append(
                "Many anchor facts were dropped due to missing citations; ensure `anchor-sheet` records citations for each anchor."
            )

        pack_stats = {
            "anchors": {
                "raw": len(anchors_raw),
                "considered": anchors_considered,
                "kept": len(anchor_facts),
                "dropped_no_cites": anchors_dropped_no_cites,
                "dropped_sanitized": anchors_dropped_sanitized,
            },
            "comparisons": {
                "raw": len([c for c in (raw_comparisons or []) if isinstance(c, dict)]),
                "considered": comparisons_considered,
                "kept": len(comparison_cards),
                "dropped_no_highlights": comparisons_dropped_no_highlights,
                "highlights_dropped_no_cites": hl_dropped_no_cites,
                "highlights_dropped_sanitized": hl_dropped_sanitized,
            },
            "evaluation_protocol": {
                "raw": len([e for e in (raw_eval or []) if isinstance(e, dict)]),
                "considered": eval_considered,
                "kept": len(eval_proto),
                "dropped_no_cites": eval_dropped_no_cites,
            },
            "limitation_hooks": {
                "raw": len([l for l in (raw_lim or []) if isinstance(l, dict)]),
                "considered": lim_considered,
                "kept": len(lim_hooks),
                "dropped_no_cites": lim_dropped_no_cites,
                "dropped_sanitized": lim_dropped_sanitized,
            },
            "trim_policy": TRIM,
        }

        opener_mode = _stable_choice(f"opener:{sid}", ["tension-first", "decision-first", "contrast-first", "protocol-first", "lens-first"]) or "tension-first"
        opener_hint = {
            "tension-first": "Start with the subsection’s central tension/trade-off; end paragraph 1 with the thesis.",
            "decision-first": "Start with a builder/research decision; state what it depends on; end paragraph 1 with the thesis.",
            "contrast-first": "Start with an explicit A-vs-B contrast; state why it matters; end paragraph 1 with the thesis.",
            "protocol-first": "Start with comparability constraints (protocol/budget/tool access); state what they make meaningful; end paragraph 1 with the thesis.",
            "lens-first": "Start by naming the lens (interface/protocol/threat model); state what it reveals; end paragraph 1 with the thesis.",
        }.get(opener_mode, "")


        record = {
            "sub_id": sid,
            "title": title,
            "section_id": sec_id,
            "section_title": sec_title,
            "rq": rq,
            "thesis": thesis,
            "tension_statement": tension_statement,
            "evaluation_anchor_minimal": eval_anchor,
            "paper_voice_palette": PAPER_VOICE_PALETTE,
            "opener_mode": opener_mode,
            "opener_hint": opener_hint,
            "axes": axes,
            # Transition handles (NO NEW FACTS): carried from subsection briefs so writers
            # can keep connectors specific without leaking outline meta into the final draft.
            "bridge_terms": [str(x).strip() for x in (brief.get("bridge_terms") or []) if str(x).strip()],
            "contrast_hook": str(brief.get("contrast_hook") or "").strip(),
            "required_evidence_fields": [str(x).strip() for x in (brief.get("required_evidence_fields") or []) if str(x).strip()],
            "paragraph_plan": paragraph_plan,
            "chapter_throughline": chapter.get("throughline") or [],
            "chapter_key_contrasts": chapter.get("key_contrasts") or [],
            "chapter_synthesis_mode": str(chapter.get("synthesis_mode") or "").strip(),
            "allowed_bibkeys_selected": selected,
            "allowed_bibkeys_mapped": mapped,
            "allowed_bibkeys_chapter": sorted(chapter_union.get(sec_id, set())),
            "allowed_bibkeys_global": mapped_global,
            "evidence_ids": [str(e).strip() for e in (binding.get("evidence_ids") or []) if str(e).strip()],
            "anchor_facts": anchor_facts,
            "comparison_cards": comparison_cards,
            "evaluation_protocol": eval_proto,
            "limitation_hooks": lim_hooks,
            "must_use": must_use,
            "do_not_repeat_phrases": DO_NOT_REPEAT,
            "pack_warnings": pack_warnings,
            "pack_stats": pack_stats,
            "generated_at": now,
        }

        records.append(record)

    write_jsonl(out_path, records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
