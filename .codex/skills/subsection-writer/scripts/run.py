from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


_ASSET_ROOT = Path(__file__).resolve().parents[1] / 'assets'
_BOOTSTRAP_TEMPLATES_PATH = _ASSET_ROOT / 'bootstrap_paragraph_templates.json'
_LEADING_ENUM_RE = re.compile(r'^(?:\(?\d+\)?[.)]\s*)+')
_LEADING_CUE_RE = re.compile(r'(?i)^(?:however|further|furthermore|additionally|meanwhile|overall|notably|empirically|specifically|for example|in practice|then|further)\s*[:,-]\s*')
_LEADING_AUTHOR_RESULT_RE = re.compile(r'(?i)^(?:we|the authors)\s+(?:also\s+|further\s+)?(?:show|find|demonstrate|report|observe|note)\s+that\s+')
_LEADING_AUTHOR_ACTION_RE = re.compile(r'(?i)^(?:to (?:fill|address|bridge|tackle|study|understand) this gap,\s*)?(?:here,\s*)?(?:we|the authors)\s+(?:present|introduce|propose|develop|describe|provide|review|summarize|offer|open-?source|release)\b[^,]{0,120},\s*')
_TRAILING_FRAGMENT_RE = re.compile(r'(?i)(?:\.\.\.|[,;:]\s*$|\b(?:and|or|to|of|in|on|with|for|from|across|between|into|than|that|which|while|because|under|over|at|by)\.?$)')
_META_SNIPPET_RE = re.compile(r'(?i)\b(?:github\.io|project\s+page|code\s+is\s+available|open-?source|repository|website)\b')
_GENERIC_LIMIT_RE = re.compile(r'(?i)\b(?:open challenges?|future work|research directions?|provide a review|offer a quantitative comparison|summarize|review of|benchmark suite|comprehensive simulation benchmark)\b')
_LABEL_REWRITES = {
    'recent representative works': 'recent systems',
    'additional mapped works': 'other mapped systems',
    'earlier / related works': 'earlier related studies',
    'earlier and related works': 'earlier related studies',
    'mapped subset a': 'one mapped subset',
    'mapped subset b': 'another mapped subset',
    'mapped subset': 'the mapped subset',
    'mapped subset alt': 'an alternate mapped subset',
    'evaluation / benchmark-focused works': 'benchmark-driven studies',
    'evaluation and benchmark-focused works': 'benchmark-driven studies',
    'control / conditioning interfaces': 'control and conditioning schemes',
    'control and conditioning interfaces': 'control and conditioning schemes',
    'planning / reasoning loops': 'planning-centric systems',
    'planning and reasoning loops': 'planning-centric systems',
    'video / temporal generation': 'video-conditioned systems',
    'video and temporal generation': 'video-conditioned systems',
    'agent frameworks / architectures': 'agent-style systems',
    'agent frameworks and architectures': 'agent-style systems',
    'memory / retrieval augmentation': 'memory-augmented systems',
    'memory and retrieval augmentation': 'memory-augmented systems',
    'tool-use and function calling': 'tool-use systems',
    'transformer-based generators': 'transformer-based policies',
}


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding='utf-8', errors='ignore') as handle:
        data = json.load(handle)
    return data if isinstance(data, dict) else {}


_BOOTSTRAP_TEMPLATES = _load_json(_BOOTSTRAP_TEMPLATES_PATH)


def _tmpl(group: str, key: str) -> str:
    section = _BOOTSTRAP_TEMPLATES.get(group) or {}
    if not isinstance(section, dict):
        return ''
    value = section.get(key)
    if isinstance(value, list):
        options = [str(item or '').strip() for item in value if str(item or '').strip()]
        return options[0] if options else ''
    return str(value or '').strip()


def _render(group: str, key: str, **kwargs: str) -> str:
    template = _tmpl(group, key)
    if not template:
        raise KeyError(f'missing template {group}.{key}')
    return template.format(**kwargs)


def _pick_option(seed: str, value: Any) -> str:
    if isinstance(value, list):
        options = _ordered_options(seed, value)
        return options[0] if options else ''
    return str(value or '').strip()


def _render_seeded(group: str, key: str, *, seed: str, **kwargs: str) -> str:
    section = _BOOTSTRAP_TEMPLATES.get(group) or {}
    if not isinstance(section, dict):
        raise KeyError(f'missing template group {group}')
    template = _pick_option(seed, section.get(key))
    if not template:
        raise KeyError(f'missing template {group}.{key}')
    return template.format(**kwargs)


def _ordered_options(seed: str, value: Any) -> list[str]:
    if not isinstance(value, list):
        single = str(value or '').strip()
        return [single] if single else []
    options = [str(item or '').strip() for item in value if str(item or '').strip()]
    if not options:
        return []
    digest = hashlib.sha1(str(seed or '').encode('utf-8', errors='ignore')).hexdigest()
    idx = int(digest[:12], 16) % len(options)
    return options[idx:] + options[:idx]


def _clean(text: str, *, limit: int = 220) -> str:
    s = str(text or '').strip()
    s = s.replace('\n', ' ')
    s = re.sub(r'\s+', ' ', s)
    s = s.replace('|', ', ')
    s = s.replace('/', ' and ')
    s = s.strip(' "\'`')
    if len(s) <= limit:
        return s
    clipped = s[:limit].rsplit(' ', 1)[0].strip()
    return clipped if clipped else s[:limit].strip()


def _sentence(text: str, *, limit: int = 220) -> str:
    s = _clean(text, limit=limit).strip()
    return s.strip(' ,;:')


def _clause(text: str, *, limit: int = 220) -> str:
    s = _sentence(text, limit=limit)
    s = re.sub(r'(?i)^(?:however|moreover|furthermore|additionally|finally|in practice|notably)\s*[:,-]\s*', '', s)
    s = re.sub(r'(?i)^(?:however|moreover|furthermore|additionally|finally|in practice|notably)\s+', '', s)
    s = re.sub(r'(?i)^that\s+', '', s)
    s = re.sub(r'(?i)^there is a significant gap exists between\s+', 'a significant gap remains between ', s)
    s = s.rstrip('.')
    if not s:
        return ''
    if re.match(r'^[A-Z]{2,}\b', s) or re.match(r'^\d', s):
        return s
    return s[0].lower() + s[1:] if s[0].isalpha() else s


def _normalize_label(text: Any) -> str:
    s = _clean(_deslash(text or ''), limit=80)
    if not s:
        return ''
    low = s.lower()
    if low in _LABEL_REWRITES:
        return _LABEL_REWRITES[low]
    s = re.sub(r'(?i)\bworks\b', 'studies', s)
    s = re.sub(r'(?i)\bmethods\b', 'approaches', s)
    s = re.sub(r'(?i)\s+', ' ', s).strip(' ,;:')
    return s[0].lower() + s[1:] if s and s[0].isupper() else s


def _normalize_axis(text: Any) -> str:
    s = _clean(_deslash(text or ''), limit=90)
    if not s:
        return ''
    s = re.sub(r'(?i)\bversus\b', 'vs.', s)
    s = re.sub(r'(?i)\s+', ' ', s).strip(' ,;:')
    return s[0].lower() + s[1:] if s and s[0].isupper() else s


def _is_fragmentary(text: str) -> bool:
    s = str(text or '').strip()
    if not s:
        return True
    if len(s) < 20:
        return True
    if _META_SNIPPET_RE.search(s):
        return True
    if re.search(r'(?i)^\s*including\b', s):
        return True
    if re.search(r'(?i)^\s*by\s+\w+', s):
        return True
    if re.search(r';\s*\(\d+\)', s):
        return True
    if s.count('(') != s.count(')'):
        return True
    if _TRAILING_FRAGMENT_RE.search(s):
        return True
    return False


def _normalize_evidence_text(text: Any, *, limit: int = 240) -> str:
    s = _clean(_deslash(text or ''), limit=limit)
    if not s:
        return ''
    s = _LEADING_ENUM_RE.sub('', s)
    s = _LEADING_CUE_RE.sub('', s)
    s = _LEADING_AUTHOR_RESULT_RE.sub('', s)
    s = _LEADING_AUTHOR_ACTION_RE.sub('', s)
    s = re.sub(r'(?i)\bour\s+', 'the ', s)
    s = re.sub(r'(?i)\bwe\s+(?:also\s+|further\s+)?(?:show|find|demonstrate|report|observe|note)\s+that\s+', '', s)
    s = re.sub(r'(?i)\bwe\s+(?:also\s+|further\s+)?can\s+', '', s)
    s = re.sub(r'(?i)\bempirically:\s*', '', s)
    s = re.sub(r'(?i)\bhowever:\s*', '', s)
    s = re.sub(r'(?i)\bthen:\s*', '', s)
    s = re.sub(r'(?i)\(\d+\)\s*', '', s)
    s = re.sub(r'(?i)\b(\d+)\)\s*', '', s)
    s = re.sub(r'(?i),\s*(?:supports?|enables?|provides?|including|and)\b[^.]{0,40}$', '', s)
    s = re.sub(r'\s+', ' ', s).strip(' ,;:')
    if not s:
        return ''
    if re.search(r'(?i)\b(?:we|our)\b', s):
        return ''
    if re.search(r'(?i)^is a significant gap exists\b', s):
        return ''
    if s and s[0].islower():
        s = s[0].upper() + s[1:]
    if _is_fragmentary(s):
        return ''
    return s


def _best_highlight_text(highlights: list[dict[str, Any]]) -> str:
    for item in highlights[:4]:
        excerpt = _normalize_evidence_text(item.get('excerpt') or '', limit=240)
        if excerpt:
            return excerpt
    return ''


def _valid_clause(text: str) -> str:
    clause = _clause(text, limit=280)
    if not clause or _is_fragmentary(clause):
        return ''
    return clause


def _deslash(text: str) -> str:
    s = re.sub(r'\s*/\s*', ' and ', str(text or ''))
    s = re.sub(r'\band\s+and\b', 'and', s)
    return re.sub(r'\s+', ' ', s).strip()


def _strip_title_prefix(text: str, title: str) -> str:
    s = str(text or '').strip()
    if not s:
        return ''
    title_pat = re.escape(str(title or '').strip())
    if title_pat:
        s = re.sub(rf'(?i)^in\s+{title_pat}\s*,\s*', '', s)
        s = re.sub(rf'(?i)^{title_pat}\s+highlights\s+', '', s)
    return s.strip()


def _normalize_thesis(text: str, title: str) -> str:
    s = _strip_title_prefix(text, title)
    s = re.sub(r'(?i)^this\s+subsection\s+', '', s)
    s = re.sub(r'(?i)^the\s+subsection\s+', '', s)
    s = _clean(_deslash(s), limit=260)
    if s and s[0].islower():
        s = s[0].upper() + s[1:]
    return s


def _normalize_tension(text: str, title: str) -> str:
    s = _strip_title_prefix(text, title)
    s = re.sub(r'(?i)^(?:a|the)\s+(?:central|main|recurring|key)\s+tension\s+is\s+', '', s)
    s = re.sub(r'(?i)^(?:the\s+)?main\s+interpretive\s+risk\s+is\s+that\s+', '', s)
    s = re.sub(r'(?i)^reported\s+gains\s+stay\s+readable\s+only\s+when\s+', '', s)
    return _clean(_deslash(s), limit=260)


def _uniq(items: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        v = str(item or '').strip()
        if not v or v in seen:
            continue
        seen.add(v)
        out.append(v)
    return out


def _cites(keys: list[str], *, max_keys: int = 3) -> str:
    vals = _uniq(keys)[:max_keys]
    return f"[@{'; '.join(vals)}]" if vals else ''


def _first_sentence_no_cites(text: str) -> str:
    blob = re.sub(r"\[@[^\]]+\]", "", text or "")
    blob = re.sub(r"\s+", " ", blob).strip()
    if not blob:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", blob)
    return (parts[0] if parts else blob).strip()


def _stem(text: str, *, n_words: int = 4) -> str:
    words = [w for w in re.findall(r"[A-Za-z0-9']+", (text or "").lower()) if w]
    return " ".join(words[: int(n_words)])


def _render_seeded_opener(
    *,
    seed: str,
    stem_counts: dict[str, int] | None,
    max_repeats: int = 1,
    **kwargs: str,
) -> str:
    section = _BOOTSTRAP_TEMPLATES.get('paragraphs') or {}
    if not isinstance(section, dict):
        raise KeyError('missing template group paragraphs')
    options = _ordered_options(seed, section.get('opener'))
    if not options:
        raise KeyError('missing template paragraphs.opener')
    if stem_counts is None:
        return options[0].format(**kwargs)

    best_rendered = ''
    best_stem = ''
    best_count: int | None = None
    for template in options:
        rendered = template.format(**kwargs)
        stem = _stem(_first_sentence_no_cites(rendered), n_words=4)
        count = stem_counts.get(stem, 0)
        if best_count is None or count < best_count:
            best_rendered = rendered
            best_stem = stem
            best_count = count
        if stem and count < int(max_repeats):
            stem_counts[stem] = count + 1
            return rendered

    if best_rendered:
        if best_stem:
            stem_counts[best_stem] = stem_counts.get(best_stem, 0) + 1
        return best_rendered
    raise KeyError('missing template paragraphs.opener')


def _pick_text_candidate(*, seed: str, options: list[str], stem_counts: dict[str, int] | None) -> str:
    cleaned = [str(option or '').strip() for option in options if str(option or '').strip()]
    if not cleaned:
        return ''
    ordered = _ordered_options(seed, cleaned)
    if stem_counts is None:
        return ordered[0]

    best = ordered[0]
    best_stem = _stem(_first_sentence_no_cites(best), n_words=4)
    best_count = stem_counts.get(best_stem, 0) if best_stem else 0
    for option in ordered:
        stem = _stem(_first_sentence_no_cites(option), n_words=4)
        count = stem_counts.get(stem, 0) if stem else 0
        if count < best_count:
            best = option
            best_stem = stem
            best_count = count
        if stem and count == 0:
            stem_counts[stem] = 1
            return option
    if best_stem:
        stem_counts[best_stem] = stem_counts.get(best_stem, 0) + 1
    return best


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not path.exists() or path.stat().st_size <= 0:
        return out
    for raw in path.read_text(encoding='utf-8', errors='ignore').splitlines():
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


def _item_from_comp(card: dict[str, Any], title: str) -> tuple[str, list[str]]:
    axis = _normalize_axis(card.get('axis') or '') or _tmpl('fallbacks', 'comparison_axis')
    a_label = _normalize_label(card.get('A_label') or '') or _tmpl('fallbacks', 'a_label')
    b_label = _normalize_label(card.get('B_label') or '') or _tmpl('fallbacks', 'b_label')
    a_hls = [x for x in (card.get('A_highlights') or []) if isinstance(x, dict)]
    b_hls = [x for x in (card.get('B_highlights') or []) if isinstance(x, dict)]
    a_excerpt = _best_highlight_text(a_hls)
    b_excerpt = _best_highlight_text(b_hls)
    a_clause = _valid_clause(a_excerpt)
    b_clause = _valid_clause(b_excerpt)
    if not a_clause or not b_clause or a_clause == b_clause:
        return '', []
    citations: list[str] = [str(x).strip() for x in (card.get('citations') or []) if str(x).strip()]
    for pool in [a_hls, b_hls]:
        for item in pool[:2]:
            for k in item.get('citations') or []:
                citations.append(str(k).strip())
    sentence = _render_seeded(
        'items',
        'comparison',
        seed=f"comparison:{title}:{axis}:{a_label}:{b_label}",
        title_lower=title.lower(),
        axis=axis,
        a_label=a_label,
        b_label=b_label,
        a_excerpt=_clean(a_excerpt, limit=220),
        b_excerpt=_clean(b_excerpt, limit=220),
        a_clause=a_clause,
        b_clause=b_clause,
        cite_all=_cites(citations, max_keys=4),
    )
    return sentence, citations


def _item_from_anchor(anchor: dict[str, Any], title: str) -> tuple[str, list[str]]:
    text = _normalize_evidence_text(anchor.get('text') or '', limit=240)
    text_clause = _valid_clause(text)
    if not text_clause:
        return '', []
    citations = [str(x).strip() for x in (anchor.get('citations') or []) if str(x).strip()]
    sentence = _render_seeded(
        'items',
        'anchor',
        seed=f"anchor:{title}:{text}",
        title_lower=title.lower(),
        text=text,
        text_clause=text_clause,
        cite_all=_cites(citations, max_keys=4),
    )
    return sentence, citations


def _item_from_eval(item: dict[str, Any], title: str) -> tuple[str, list[str]]:
    bullet = _normalize_eval_bullet(item.get('bullet') or '') or _tmpl('fallbacks', 'evaluation_bullet')
    bullet_clause = _valid_clause(bullet)
    if not bullet_clause:
        return '', []
    citations = [str(x).strip() for x in (item.get('citations') or []) if str(x).strip()]
    sentence = _render_seeded(
        'items',
        'evaluation',
        seed=f"evaluation:{title}:{bullet}",
        title_lower=title.lower(),
        bullet=bullet,
        bullet_clause=bullet_clause,
        cite_all=_cites(citations, max_keys=4),
    )
    return sentence, citations


def _normalize_eval_bullet(value: Any) -> str:
    bullet = _sentence(_deslash(value or ''), limit=240)
    if not bullet:
        return ''
    low = bullet.lower()
    if low.startswith('evaluation mentions include:'):
        rest = bullet.split(':', 1)[1].strip().strip(' .')
        return rest
    if low.startswith('evaluation mentions include'):
        rest = bullet[len('evaluation mentions include'):].strip(' :.')
        return rest
    return _normalize_evidence_text(bullet, limit=240)


def _keep_eval_item(item: dict[str, Any]) -> bool:
    bullet = _clean(_deslash(item.get('bullet') or ''), limit=220).lower()
    if not bullet:
        return False
    blocked = (
        'when comparing results, anchor the paragraph with',
        'prefer head-to-head comparisons only when',
        'avoid underspecified model',
        'if a claim relies on a single reported number',
        'if budgets or environments differ across papers',
        'use conservative language',
    )
    if any(bullet.startswith(prefix) for prefix in blocked):
        return False
    return True


def _item_from_limit(item: dict[str, Any], title: str) -> tuple[str, list[str]]:
    raw_text = item.get('excerpt') or item.get('bullet') or ''
    if _GENERIC_LIMIT_RE.search(str(raw_text or '')):
        return '', []
    text = _normalize_evidence_text(raw_text, limit=240)
    text_clause = _valid_clause(text)
    if not text_clause:
        return '', []
    citations = [str(x).strip() for x in (item.get('citations') or []) if str(x).strip()]
    sentence = _render_seeded(
        'items',
        'limitation',
        seed=f"limitation:{title}:{text}",
        title_lower=title.lower(),
        text=text,
        text_clause=text_clause,
        cite_all=_cites(citations, max_keys=4),
    )
    return sentence, citations


def _bundle_sentences(sentences: list[str], *, target: int) -> list[str]:
    items = [str(s or '').strip() for s in sentences if str(s or '').strip()]
    if not items:
        return []
    target = max(1, min(int(target), len(items)))
    base = len(items) // target
    remainder = len(items) % target
    bundles: list[list[str]] = []
    cursor = 0
    for idx in range(target):
        size = base + (1 if idx < remainder else 0)
        if size <= 0:
            continue
        bundles.append(items[cursor: cursor + size])
        cursor += size
    while cursor < len(items):
        bundles[-1].append(items[cursor])
        cursor += 1
    return [' '.join(chunk).strip() for chunk in bundles if chunk]


def _make_paragraphs(pack: dict[str, Any], title: str, *, opener_stem_counts: dict[str, int] | None = None) -> list[str]:
    thesis = _normalize_thesis(pack.get('thesis') or '', title) or _render('fallbacks', 'thesis', title=title)
    tension = _normalize_tension(pack.get('tension_statement') or '', title) or _tmpl('fallbacks', 'tension_statement')
    rq = _clean(_deslash(pack.get('rq') or ''), limit=220) or _tmpl('fallbacks', 'rq')

    cards = [x for x in (pack.get('comparison_cards') or []) if isinstance(x, dict)]
    anchors = [x for x in (pack.get('anchor_facts') or []) if isinstance(x, dict)]
    evals = [x for x in (pack.get('evaluation_protocol') or []) if isinstance(x, dict) and _keep_eval_item(x)]
    limits = [x for x in (pack.get('limitation_hooks') or []) if isinstance(x, dict)]
    support_keys = _uniq(
        [str(x).strip() for x in (pack.get('allowed_bibkeys_selected') or []) if str(x).strip()]
        + [str(x).strip() for x in (pack.get('allowed_bibkeys_chapter') or []) if str(x).strip()]
    )

    seed_cites: list[str] = []
    for source in cards[:3]:
        seed_cites.extend([str(x).strip() for x in (source.get('citations') or []) if str(x).strip()])
    for source in anchors[:2]:
        seed_cites.extend([str(x).strip() for x in (source.get('citations') or []) if str(x).strip()])
    seed_cites = _uniq(seed_cites)
    opener_support = _ordered_options(f"opener-cites:{title}:{thesis}:{tension}", support_keys)
    opener_cites = _uniq(opener_support + seed_cites)[:6]

    opener_seed_cites = _cites(opener_cites or seed_cites, max_keys=4)
    opener_candidates: list[str] = [
        _render_seeded_opener(
            seed=f"opener:{title}:{thesis}:{tension}",
            stem_counts=None,
            title=title,
            title_lower=title.lower(),
            thesis=thesis,
            seed_cites=opener_seed_cites,
            tension=tension,
            rq=rq,
        )
    ]
    if cards:
        card0 = cards[0]
        axis = _normalize_axis(card0.get('axis') or '')
        a_label = _normalize_label(card0.get('A_label') or '')
        b_label = _normalize_label(card0.get('B_label') or '')
        if axis and a_label and b_label:
            opener_candidates.append(
                f"One recurrent split in {title.lower()} runs between {a_label} and {b_label} along {axis}. {thesis} {opener_seed_cites}."
            )
    if evals:
        eval_anchor = _normalize_eval_bullet((evals[0] or {}).get('bullet') or '')
        if eval_anchor:
            opener_candidates.append(
                f"Results in {title.lower()} only stay comparable when they are read against {eval_anchor}. {thesis} {opener_seed_cites}."
            )

    paragraphs: list[str] = []
    picked_opener = _pick_text_candidate(
        seed=f"opener-candidate:{title}:{thesis}:{tension}",
        options=opener_candidates,
        stem_counts=opener_stem_counts,
    )
    if picked_opener:
        paragraphs.append(picked_opener)

    comp_items = [_item_from_comp(card, title) for card in cards[:7]]
    anchor_items = [_item_from_anchor(anchor, title) for anchor in anchors[:10]]
    eval_items = [_item_from_eval(item, title) for item in evals[:4]]
    limit_items = [_item_from_limit(item, title) for item in limits[:8]]

    body_items: list[tuple[str, list[str]]] = []
    for idx in range(max(len(comp_items), len(anchor_items), len(eval_items), len(limit_items), 1)):
        if idx < len(comp_items):
            body_items.append(comp_items[idx])
        if idx < len(anchor_items):
            body_items.append(anchor_items[idx])
        if idx < len(eval_items):
            body_items.append(eval_items[idx])
        if idx < len(limit_items):
            body_items.append(limit_items[idx])

    deduped_items: list[tuple[str, list[str]]] = []
    seen_texts: set[str] = set()
    for text, cites in body_items:
        cleaned = re.sub(r'\s+', ' ', str(text or '').strip())
        if not cleaned:
            continue
        key = re.sub(r'[^a-z0-9]+', ' ', cleaned.lower()).strip()
        if not key or key in seen_texts:
            continue
        seen_texts.add(key)
        deduped_items.append((cleaned, cites))

    used: list[str] = opener_cites[:] or seed_cites[:]
    body_sentences: list[str] = []
    for text, cites in deduped_items[:24]:
        body_sentences.append(text)
        used.extend(cites)

    target_paragraphs = max(9, min(len(body_sentences), len(pack.get('paragraph_plan') or []) - 1 if isinstance(pack.get('paragraph_plan'), list) else 9))
    paragraphs.extend(_bundle_sentences(body_sentences, target=target_paragraphs))

    return [p.strip() for p in paragraphs if p.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--unit-id', default='')
    parser.add_argument('--inputs', default='')
    parser.add_argument('--outputs', default='')
    parser.add_argument('--checkpoint', default='')
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

    from tooling.common import atomic_write_text, backup_existing, decisions_has_approval, ensure_dir, load_yaml, now_iso_seconds, parse_semicolon_list, upsert_checkpoint_block
    from tooling.pipeline_text import slug_unit_id
    from tooling.quality_gate import check_unit_outputs, write_quality_report

    workspace = Path(args.workspace).resolve()
    unit_id = str(args.unit_id or 'U100').strip() or 'U100'
    inputs = parse_semicolon_list(args.inputs)
    outputs = parse_semicolon_list(args.outputs) or ['sections/sections_manifest.jsonl', 'sections/h3_bodies.refined.ok']

    out_rel = next((x for x in outputs if x.endswith('sections_manifest.jsonl')), 'sections/sections_manifest.jsonl')
    marker_rel = next((x for x in outputs if x.endswith('.refined.ok')), 'sections/h3_bodies.refined.ok')
    out_path = workspace / out_rel
    marker_path = workspace / marker_rel
    sections_dir = out_path.parent
    # Deprecated soft-freeze marker kept some workspaces pinned to stale prose
    # even during explicit unit reruns. Only honor the new hard-freeze marker.
    freeze_marker = sections_dir / 'h3_bodies.freeze.hard.ok'
    ensure_dir(sections_dir)

    decisions_path = workspace / 'DECISIONS.md'
    if not decisions_has_approval(decisions_path, 'C2'):
        block = '\n'.join([
            '## C5 section writing request',
            '',
            '- This unit writes prose into per-section files under `sections/`.',
            '- Please tick `Approve C2` in `DECISIONS.md`, then rerun this unit.',
            '',
        ])
        upsert_checkpoint_block(decisions_path, 'C5', block)
        return 2

    outline = load_yaml(workspace / 'outline' / 'outline.yml') if (workspace / 'outline' / 'outline.yml').exists() else []
    packs = {str(r.get('sub_id') or '').strip(): r for r in _load_jsonl(workspace / 'outline' / 'writer_context_packs.jsonl') if str(r.get('sub_id') or '').strip()}
    if not packs:
        briefs = {str(r.get('sub_id') or '').strip(): r for r in _load_jsonl(workspace / 'outline' / 'subsection_briefs.jsonl') if str(r.get('sub_id') or '').strip()}
        evidence = {str(r.get('sub_id') or '').strip(): r for r in _load_jsonl(workspace / 'outline' / 'evidence_drafts.jsonl') if str(r.get('sub_id') or '').strip()}
        for sid, brief in briefs.items():
            pack = dict(brief)
            pack.update(evidence.get(sid) or {})
            pack.setdefault('comparison_cards', pack.get('concrete_comparisons') or [])
            pack.setdefault('anchor_facts', [])
            pack.setdefault('limitation_hooks', pack.get('failures_limitations') or [])
            packs[sid] = pack

    records: list[dict[str, Any]] = []
    generated_at = now_iso_seconds()
    opener_stem_counts: dict[str, int] = {}

    def add_record(rec: dict[str, Any]) -> None:
        p = workspace / str(rec.get('path') or '')
        exists = p.exists() and p.stat().st_size > 0
        rec['exists'] = bool(exists)
        rec['generated_at'] = generated_at
        if exists:
            text = p.read_text(encoding='utf-8', errors='ignore')
            rec['citations'] = _uniq(re.findall(r'\[@([^\]]+)\]', text))
            rec['bytes'] = p.stat().st_size
        records.append(rec)

    for name, title in [('abstract', 'Abstract'), ('discussion', 'Discussion'), ('conclusion', 'Conclusion')]:
        add_record({'kind': 'global', 'id': name, 'title': title, 'path': f'sections/{name}.md'})

    if isinstance(outline, list):
        for sec in outline:
            if not isinstance(sec, dict):
                continue
            sec_id = str(sec.get('id') or '').strip()
            sec_title = str(sec.get('title') or '').strip()
            subs = [sub for sub in (sec.get('subsections') or []) if isinstance(sub, dict)]
            if subs and sec_id:
                lead_path = sections_dir / f'{slug_unit_id(sec_id)}_lead.md'
                add_record({'kind': 'h2_lead', 'id': sec_id, 'title': sec_title, 'section_id': sec_id, 'section_title': sec_title, 'path': str(lead_path.relative_to(workspace))})
            elif sec_id:
                add_record({'kind': 'h2', 'id': sec_id, 'title': sec_title, 'section_id': sec_id, 'section_title': sec_title, 'path': f'sections/{slug_unit_id(sec_id)}.md'})

            for sub in subs:
                sub_id = str(sub.get('id') or '').strip()
                title = str(sub.get('title') or '').strip()
                if not sub_id or not title:
                    continue
                path = sections_dir / f'{slug_unit_id(sub_id)}.md'
                should_write = True
                if freeze_marker.exists() and path.exists() and path.stat().st_size > 0:
                    should_write = False
                if should_write:
                    pack = packs.get(sub_id) or {'title': title}
                    text = '\n\n'.join(_make_paragraphs(pack, title, opener_stem_counts=opener_stem_counts)).rstrip() + '\n'
                    if path.exists() and path.stat().st_size > 0:
                        backup_existing(path)
                    atomic_write_text(path, text)
                add_record({'kind': 'h3', 'id': sub_id, 'title': title, 'section_id': sec_id, 'section_title': sec_title, 'path': str(path.relative_to(workspace))})

    atomic_write_text(out_path, '\n'.join(json.dumps(r, ensure_ascii=False) for r in records).rstrip() + '\n')
    atomic_write_text(marker_path, f'h3 bodies refined at {generated_at}\n')

    issues = check_unit_outputs(skill='subsection-writer', workspace=workspace, outputs=[out_rel])
    if issues:
        write_quality_report(workspace=workspace, unit_id=unit_id, skill='subsection-writer', issues=issues)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
