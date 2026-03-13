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
_LEADING_CUE_RE = re.compile(r'(?i)^(?:however|yet|further|furthermore|additionally|meanwhile|overall|notably|empirically|specifically|for example|in practice|then|further)\s*[:,-]\s*')
_LEADING_AUTHOR_RESULT_RE = re.compile(r'(?i)^(?:we|the authors)\s+(?:also\s+|further\s+)?(?:show|find|demonstrate|report|observe|note)\s+that\s+')
_LEADING_AUTHOR_ACTION_RE = re.compile(r'(?i)^(?:to (?:fill|address|bridge|tackle|study|understand) this gap,\s*)?(?:here,\s*)?(?:we|the authors)\s+(?:present|introduce|propose|develop|describe|provide|review|summarize|offer|open-?source|release)\b[^,]{0,120},\s*')
_TRAILING_FRAGMENT_RE = re.compile(r'(?i)(?:\.\.\.|[,;:]\s*$|\b(?:and|or|to|of|in|on|with|for|from|across|between|into|than|that|which|while|because|under|over|at|by)\.?$)')
_META_SNIPPET_RE = re.compile(r'(?i)\b(?:github\.io|project\s+page|code\s+is\s+available|open-?source|repository|website)\b')
_GENERIC_LIMIT_RE = re.compile(r'(?i)\b(?:open challenges?|future work|research directions?|provide a review|offer a quantitative comparison|summarize|review of|benchmark suite|comprehensive simulation benchmark)\b')
_LISTLIKE_EVAL_VERB_RE = re.compile(r'(?i)\b(?:compare|benchmark|evaluate|assessment?|measure|measured|metric|success|accuracy|latency|robust|generaliz|transfer|cost|throughput|real-world|simulation)\b')
_EVIDENCE_VERB_RE = re.compile(r'(?i)\b(?:is|are|was|were|becomes?|remains?|shows?|demonstrates?|reports?|finds?|observes?|argues?|indicates?|improves?|reduces?|increases?|achieves?|enables?|supports?|validates?|reveals?|suggests?|depends?|requires?|offers?|bridges?|addresses?|outperforms?|fails?|limits?|constrains?)\b')
_CONCRETE_MARKER_RE = re.compile(
    r"\b\d+(?:\.\d+)?%?\b|"
    r"\b[A-Z]{2,}(?:-[A-Z0-9]+)*\b|"
    r"\b[A-Z][a-z]+[A-Z][A-Za-z0-9-]*\b|"
    r"\b[A-Z][A-Za-z0-9]+-[A-Z0-9][A-Za-z0-9-]*\b"
)
_CONCRETE_CONTEXT_RE = re.compile(
    r"(?i)\b(?:benchmark|dataset|task|real-world|simulation|robot|robotic|policy|action|control|embod|"
    r"manipulation|navigation|transfer|generaliz|latency|cost|failure|robust|deployment|safety|baseline)\b"
)
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
    s = re.sub(r'(?i)^(?:in|throughout)\s+(?:this|our)\s+(?:thesis|paper|study|manuscript),?\s*', '', s)
    s = re.sub(r'(?i)\bour\s+', 'the ', s)
    s = re.sub(r'(?i)\bwe\s+(?:also\s+|further\s+)?(?:show|find|demonstrate|report|observe|note)\s+that\s+', '', s)
    s = re.sub(r'(?i)\bwe\s+(?:also\s+|further\s+)?can\s+', '', s)
    s = re.sub(r'(?i)\bempirically:\s*', '', s)
    s = re.sub(r'(?i)\bhowever:\s*', '', s)
    s = re.sub(r'(?i)\bthen:\s*', '', s)
    s = re.sub(r'(?i)^(?:while|but|and|yet|however|nevertheless|in contrast)\s+', '', s)
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
    if re.match(r'(?i)^[a-z-]+ing\b', s):
        return ''
    if not _EVIDENCE_VERB_RE.search(s):
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


def _has_concrete_marker(text: str) -> bool:
    s = str(text or '')
    return bool(_CONCRETE_MARKER_RE.search(s) or _CONCRETE_CONTEXT_RE.search(s))


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
    s = re.sub(r'(?i)^in\s+[^,]+,\s*', '', s)
    s = re.sub(r'(?i)^for\s+[^,]+,\s*', '', s)
    s = re.sub(r'(?i)^this\s+subsection\s+', '', s)
    s = re.sub(r'(?i)^the\s+subsection\s+', '', s)
    s = _clean(_deslash(s), limit=260)
    s = s.rstrip(' .;:')
    if s and s[0].islower():
        s = s[0].upper() + s[1:]
    return s


def _normalize_tension(text: str, title: str) -> str:
    s = _strip_title_prefix(text, title)
    s = re.sub(r'(?i)^(?:a|the)\s+(?:central|main|recurring|key)\s+tension\s+is\s+', '', s)
    s = re.sub(r'(?i)^(?:a|the)\s+tension\s+around\s+[^,:]+[:,-]\s*', '', s)
    s = re.sub(r'(?i)^(?:a|the)\s+tension\s+between\s+[^,:]+[:,-]\s*', '', s)
    s = re.sub(r'(?i)^(?:the\s+)?main\s+interpretive\s+risk\s+is\s+that\s+', '', s)
    s = re.sub(r'(?i)^reported\s+gains\s+stay\s+readable\s+only\s+when\s+', '', s)
    s = re.sub(r'(?i),?\s*motivating a protocol-aware synthesis rather than per-paper summaries\.?$', '', s).strip()
    if ':' in s:
        left, right = s.split(':', 1)
        right = right.strip()
        if right and _EVIDENCE_VERB_RE.search(right):
            s = right
    return _clean(_deslash(s), limit=260).rstrip(' .;:')


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


def _normalized_opener_stem(text: str, title: str) -> str:
    base = _first_sentence_no_cites(text)
    title_low = str(title or '').strip().lower()
    if title_low:
        base = re.sub(re.escape(title_low), '', base.lower())
    base = re.sub(
        r'(?i)\b(?:work on|the literature on|a stable reading of|what matters in|the most consequential contrast in)\b',
        '',
        base,
    )
    base = re.sub(r'\s+', ' ', base).strip(' ,.;:')
    return _stem(base, n_words=6)


def _opener_specificity_score(text: str) -> int:
    s = _clean(text, limit=320)
    if not s:
        return -10
    score = 0
    if _CONCRETE_MARKER_RE.search(s):
        score += 3
    if _CONCRETE_CONTEXT_RE.search(s):
        score += 2
    if re.search(r'(?i)\b(?:because|whereas|while|under|across|latency|real-world|benchmark|transfer)\b', s):
        score += 1
    if re.search(r'(?i)\b(?:only becomes comparable once|is best read through|most informative when read through)\b', s):
        score -= 2
    if re.search(r'(?i)^(?:that comparison weakens once|a recurring constraint is|the reported gains are less stable when)\b', s):
        score -= 4
    if re.search(r'(?i)^the most consequential contrast in\b', s):
        score -= 2
    return score


def _render_seeded_opener(
    *,
    seed: str,
    title: str,
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
    context = dict(kwargs)
    context.setdefault('title', title)
    if stem_counts is None:
        return options[0].format(**context)

    best_rendered = ''
    best_stem = ''
    best_count: int | None = None
    for template in options:
        rendered = template.format(**context)
        stem = _normalized_opener_stem(rendered, title)
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


def _pick_text_candidate(*, seed: str, title: str, options: list[str], stem_counts: dict[str, int] | None) -> str:
    cleaned = [str(option or '').strip() for option in options if str(option or '').strip()]
    if not cleaned:
        return ''
    ordered = _ordered_options(seed, cleaned)
    if stem_counts is None:
        return ordered[0]

    best = ordered[0]
    best_stem = _normalized_opener_stem(best, title)
    best_count = stem_counts.get(best_stem, 0) if best_stem else 0
    best_score = _opener_specificity_score(best)
    for option in ordered:
        stem = _normalized_opener_stem(option, title)
        count = stem_counts.get(stem, 0) if stem else 0
        score = _opener_specificity_score(option)
        if count < best_count or (count == best_count and score > best_score):
            best = option
            best_stem = stem
            best_count = count
            best_score = score
        if stem and count == 0 and score >= best_score:
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
    citations: list[str] = [str(x).strip() for x in (card.get('citations') or []) if str(x).strip()]
    for pool in [a_hls, b_hls]:
        for item in pool[:2]:
            for k in item.get('citations') or []:
                citations.append(str(k).strip())
    if not a_clause and not b_clause:
        return '', []
    if a_clause and b_clause and a_clause != b_clause:
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

    dominant_label = a_label if a_clause else b_label
    counterpart_label = b_label if a_clause else a_label
    dominant_clause = a_clause or b_clause
    sentence = (
        f"On {axis}, {dominant_label} are the better-grounded side of the current comparison: {dominant_clause}, "
        f"whereas reports for {counterpart_label} remain thinner or less directly comparable {_cites(citations, max_keys=4)}."
    )
    return sentence, citations


def _item_from_anchor(anchor: dict[str, Any], title: str) -> tuple[str, list[str]]:
    text = _normalize_evidence_text(anchor.get('text') or '', limit=240)
    text_clause = _valid_clause(text)
    if not text_clause:
        return '', []
    if not _has_concrete_marker(text_clause):
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
        return f"benchmarks and settings such as {rest}"
    if low.startswith('evaluation mentions include'):
        rest = bullet[len('evaluation mentions include'):].strip(' :.')
        return f"benchmarks and settings such as {rest}"
    return _normalize_evidence_text(bullet, limit=240)


def _keep_eval_item(item: dict[str, Any]) -> bool:
    bullet = _clean(_deslash(item.get('bullet') or ''), limit=220).lower()
    if not bullet:
        return False
    if bullet.startswith('evaluation mentions include'):
        return True
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
    tokens = [tok for tok in re.findall(r"[A-Za-z0-9-]+", bullet) if re.search(r"[A-Za-z]", tok)]
    if bullet.count(',') >= 3:
        if not _LISTLIKE_EVAL_VERB_RE.search(bullet):
            return False
        shortish = sum(1 for tok in tokens if len(tok) <= 6 or tok.isupper())
        if tokens and shortish / max(1, len(tokens)) >= 0.7:
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
    if not _has_concrete_marker(text_clause):
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

    raw_cards = [x for x in (pack.get('comparison_cards') or []) if isinstance(x, dict)]
    cards: list[dict[str, Any]] = []
    seen_pairs: set[tuple[str, str, str]] = set()
    for card in raw_cards:
        a_label = _normalize_label(card.get('A_label') or '')
        b_label = _normalize_label(card.get('B_label') or '')
        axis = _normalize_axis(card.get('axis') or '') or 'axis'
        pair = tuple(sorted([a_label or 'a', b_label or 'b'])) + (axis,)
        if pair in seen_pairs:
            continue
        seen_pairs.add(pair)
        cards.append(card)
        if len(cards) >= 6:
            break

    raw_anchors = [x for x in (pack.get('anchor_facts') or []) if isinstance(x, dict)]
    anchors: list[dict[str, Any]] = []
    seen_anchor_papers: set[str] = set()
    for anchor in raw_anchors:
        pid = str(anchor.get('paper_id') or '').strip()
        if pid and pid in seen_anchor_papers:
            continue
        if pid:
            seen_anchor_papers.add(pid)
        anchors.append(anchor)
        if len(anchors) >= 8:
            break
    evals = [x for x in (pack.get('evaluation_protocol') or []) if isinstance(x, dict) and _keep_eval_item(x)]
    raw_limits = [x for x in (pack.get('limitation_hooks') or []) if isinstance(x, dict)]
    limits: list[dict[str, Any]] = []
    seen_limit_papers: set[str] = set()
    for item in raw_limits:
        pid = str(item.get('paper_id') or '').strip()
        if pid and pid in seen_limit_papers:
            continue
        if pid:
            seen_limit_papers.add(pid)
        limits.append(item)
        if len(limits) >= 6:
            break
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
            title=title,
            stem_counts=None,
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
            comparison_openers = [
                f"The sharpest split in {title.lower()} is between {a_label} and {b_label}, because their reported gains depend on different assumptions about {axis}. {thesis} {opener_seed_cites}.",
                f"What most separates the literature on {title.lower()} is the contrast between {a_label} and {b_label}, especially once {axis} changes. {thesis} {opener_seed_cites}.",
                f"In {title.lower()}, the main divide is between {a_label} and {b_label}; that contrast only makes sense once assumptions about {axis} are stated explicitly. {thesis} {opener_seed_cites}.",
            ]
            opener_candidates.extend(comparison_openers)
    if anchors:
        anchor_sentence, _ = _item_from_anchor(anchors[0], title)
        if anchor_sentence:
            opener_candidates.append(f"{anchor_sentence} {thesis} {opener_seed_cites}.".strip())

    paragraphs: list[str] = []
    picked_opener = _pick_text_candidate(
        seed=f"opener-candidate:{title}:{thesis}:{tension}",
        title=title,
        options=opener_candidates,
        stem_counts=opener_stem_counts,
    )
    if picked_opener:
        paragraphs.append(picked_opener)

    comp_items = [('comparison',) + _item_from_comp(card, title) for card in cards[:6]]
    anchor_items = [('anchor',) + _item_from_anchor(anchor, title) for anchor in anchors[:8]]
    eval_items = [('evaluation',) + _item_from_eval(item, title) for item in evals[:4]]
    limit_items = [('limitation',) + _item_from_limit(item, title) for item in limits[:6]]

    body_items: list[tuple[str, str, list[str]]] = []
    for idx in range(max(len(comp_items), len(anchor_items), len(eval_items), len(limit_items), 1)):
        if idx < len(comp_items):
            body_items.append(comp_items[idx])
        if idx < len(anchor_items):
            body_items.append(anchor_items[idx])
        if idx < len(eval_items):
            body_items.append(eval_items[idx])
        if idx < len(limit_items):
            body_items.append(limit_items[idx])

    deduped_items: list[tuple[str, str, list[str]]] = []
    seen_texts: set[str] = set()
    for kind, text, cites in body_items:
        cleaned = re.sub(r'\s+', ' ', str(text or '').strip())
        if not cleaned:
            continue
        key = re.sub(r'[^a-z0-9]+', ' ', cleaned.lower()).strip()
        if not key or key in seen_texts:
            continue
        seen_texts.add(key)
        deduped_items.append((kind, cleaned, cites))

    plan_len = len(pack.get('paragraph_plan') or []) if isinstance(pack.get('paragraph_plan'), list) else 0
    max_items = max(14, min(20, (plan_len * 2) if plan_len else 16))
    used_cites: set[str] = set(opener_cites[:] or seed_cites[:])
    selected_types: dict[str, int] = {}
    remaining = deduped_items[:]
    chosen: list[tuple[str, str, list[str]]] = []

    def pick_best(*, only_kind: str | None = None) -> bool:
        best_idx = -1
        best_score: int | None = None
        for idx, (kind, text, cites) in enumerate(remaining):
            if only_kind and kind != only_kind:
                continue
            cite_gain = len([c for c in _uniq(cites) if c and c not in used_cites])
            type_bonus = {'comparison': 4, 'anchor': 3, 'evaluation': 2, 'limitation': 2}.get(kind, 0)
            repeat_penalty = selected_types.get(kind, 0) * 3
            score = cite_gain * 6 + type_bonus - repeat_penalty
            if _has_concrete_marker(text):
                score += 2
            if best_score is None or score > best_score:
                best_idx = idx
                best_score = score
        if best_idx < 0:
            return False
        kind, text, cites = remaining.pop(best_idx)
        chosen.append((kind, text, cites))
        selected_types[kind] = selected_types.get(kind, 0) + 1
        for cite in _uniq(cites):
            if cite:
                used_cites.add(cite)
        return True

    for kind, minimum in (('comparison', 2), ('anchor', 2), ('evaluation', 2), ('limitation', 1)):
        while len(chosen) < max_items and selected_types.get(kind, 0) < minimum:
            if not pick_best(only_kind=kind):
                break

    while remaining and len(chosen) < max_items:
        if not pick_best():
            break

    body_sentences: list[str] = []
    for _, text, cites in chosen:
        body_sentences.append(text)
    if plan_len:
        desired_paragraphs = max(6, min(10, plan_len - 1))
    else:
        desired_paragraphs = 8
    target_paragraphs = max(4, min(len(body_sentences), desired_paragraphs))
    paragraphs.extend(_bundle_sentences(body_sentences, target=target_paragraphs))

    return [p.strip() for p in paragraphs if p.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--unit-id', default='')
    parser.add_argument('--inputs', default='')
    parser.add_argument('--outputs', default='')
    parser.add_argument('--checkpoint', default='')
    parser.add_argument('--rewrite', action='store_true', help='rewrite existing H3 files instead of bootstrapping missing ones only')
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
                elif path.exists() and path.stat().st_size > 0 and not args.rewrite:
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
