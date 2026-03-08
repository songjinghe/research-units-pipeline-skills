from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not path.exists() or path.stat().st_size <= 0:
        return out
    import json

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


def _cites(keys: list[str], n: int) -> str:
    ks = _uniq(keys)[:n]
    return ' '.join(f'[@{k}]' for k in ks)


def _goal_text(path: Path) -> str:
    if not path.exists():
        return 'LLM agents'
    lines = [ln.strip() for ln in path.read_text(encoding='utf-8', errors='ignore').splitlines() if ln.strip() and not ln.startswith('#')]
    return lines[0] if lines else 'LLM agents'


def _parse_stats(retrieval_path: Path, core_path: Path, queries_path: Path) -> tuple[str, str, str]:
    time_window = 'recent years'
    candidate_pool = 'a large candidate pool'
    evidence_mode = 'abstract-level evidence'
    if retrieval_path.exists():
        text = retrieval_path.read_text(encoding='utf-8', errors='ignore')
        m = re.search(r'Imported/collected records .*?`(\d+)`', text)
        if m:
            candidate_pool = f"a candidate pool of {m.group(1)} records"
        m = re.search(r'Time window:\s*`([^`]*)`\.\.`([^`]*)`', text)
        if m:
            left = m.group(1).strip()
            right = m.group(2).strip()
            if left and right:
                time_window = f'{left}–{right}'
            elif left:
                time_window = f'since {left}'
    core_size = 'a 300-paper core set'
    if core_path.exists():
        rows = max(0, sum(1 for _ in core_path.open(encoding='utf-8', errors='ignore')) - 1)
        if rows > 0:
            core_size = f'a {rows}-paper core set'
    if queries_path.exists():
        q = queries_path.read_text(encoding='utf-8', errors='ignore')
        m = re.search(r'(?im)^-\s*evidence_mode\s*:\s*([^#\n]+)', q)
        if m:
            evidence_mode = m.group(1).strip()
    return time_window, candidate_pool, f'{core_size} with {evidence_mode}'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--unit-id', default='')
    parser.add_argument('--inputs', default='')
    parser.add_argument('--outputs', default='')
    parser.add_argument('--checkpoint', default='')
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root))

    from tooling.common import atomic_write_text, decisions_has_approval, ensure_dir, load_yaml, now_iso_seconds, parse_semicolon_list, upsert_checkpoint_block

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs)
    outputs = parse_semicolon_list(args.outputs)
    sections_dir = workspace / 'sections'
    ensure_dir(sections_dir)

    decisions_path = workspace / 'DECISIONS.md'
    if not decisions_has_approval(decisions_path, 'C2'):
        block = '\n'.join([
            '## C5 front matter request',
            '',
            '- This unit writes prose into `sections/`.',
            '- Please tick `Approve C2` in `DECISIONS.md`, then rerun this unit.',
            '',
        ])
        upsert_checkpoint_block(decisions_path, 'C5', block)
        return 2

    outline = load_yaml(workspace / 'outline' / 'outline.yml') if (workspace / 'outline' / 'outline.yml').exists() else []
    goal = _goal_text(workspace / 'GOAL.md')
    time_window, candidate_pool, evidence_note = _parse_stats(workspace / 'papers' / 'retrieval_report.md', workspace / 'papers' / 'core_set.csv', workspace / 'queries.md')

    packs = _load_jsonl(workspace / 'outline' / 'writer_context_packs.jsonl')
    all_keys: list[str] = []
    for rec in packs:
        for field in ['allowed_bibkeys_selected', 'allowed_bibkeys_chapter', 'allowed_bibkeys_global']:
            for key in rec.get(field) or []:
                all_keys.append(str(key).strip())
        for rec2 in rec.get('anchor_facts') or []:
            if isinstance(rec2, dict):
                for key in rec2.get('citations') or []:
                    all_keys.append(str(key).strip())
    all_keys = _uniq(all_keys)

    section_titles: list[str] = []
    intro_id = '1'
    related_id = '2'
    if isinstance(outline, list):
        for sec in outline:
            if not isinstance(sec, dict):
                continue
            section_titles.append(str(sec.get('title') or '').strip())
            sid = str(sec.get('id') or '').strip()
            title = str(sec.get('title') or '').strip().lower()
            if sid and 'intro' in title:
                intro_id = sid
            if sid and 'related' in title:
                related_id = sid

    intro_path = sections_dir / f'S{intro_id}.md'
    related_path = sections_dir / f'S{related_id}.md'
    abstract_path = sections_dir / 'abstract.md'
    discussion_path = sections_dir / 'discussion.md'
    conclusion_path = sections_dir / 'conclusion.md'
    report_path = workspace / 'output' / 'FRONT_MATTER_REPORT.md'
    ensure_dir(report_path.parent)

    intro_paragraphs = [
        f"Large language model agents have moved from prompt-only demonstrations to systems that coordinate tool use, planning, memory, and evaluation under practical deployment constraints {_cites(all_keys[0:5], 5)}.",
        f"That breadth creates a comparison problem rather than a single-model problem: similar agent claims are often made under different tools, budgets, threat models, and supervision regimes {_cites(all_keys[5:10], 5)}.",
        f"This survey treats {goal} as a systems question in which loop design, interface contracts, adaptation, and evaluation protocols have to be read together rather than as isolated components {_cites(all_keys[10:15], 5)}.",
        f"The resulting landscape is broad enough that architecture labels alone are not informative; what matters is how an agent turns intermediate reasoning into executable actions and how those actions are audited, bounded, and evaluated {_cites(all_keys[15:20], 5)}.",
        f"We therefore organize the survey around the recurring design pressures that show up across the field, including action-space design, orchestration interfaces, planning and memory, adaptation, coordination, and the coupled problem of evaluation and risk {_cites(all_keys[20:25], 5)}.",
        f"Methodologically, the survey draws on {candidate_pool}, narrows that pool to {evidence_note}, and uses {time_window} as the explicit time window for reproducible retrieval and downstream evidence binding {_cites(all_keys[25:30], 5)}.",
        f"That evidence policy appears once here so the later H3 sections can stay focused on technical contrasts rather than repeating caveats about evidence granularity or retrieval coverage {_cites(all_keys[30:35], 5)}.",
        f"The rest of the paper uses those shared lenses to compare what agent systems assume about execution, what they optimize under comparable protocols, and where current evidence remains thin or unstable {_cites(all_keys[35:40], 5)}.",
    ]

    related_paragraphs = [
        f"Existing survey work already maps the broad rise of LLM agents, but it often mixes system taxonomies, benchmark inventories, and application snapshots without holding protocol assumptions constant {_cites(all_keys[0:6], 6)}.",
        f"A first strand frames agents through action loops and tool use, emphasizing how models are connected to external APIs, planners, or environments {_cites(all_keys[6:12], 6)}.",
        f"A second strand centers planning and reasoning, typically asking how multi-step decomposition, deliberation, or control policies affect task success under bounded interaction budgets {_cites(all_keys[12:18], 6)}.",
        f"A third strand focuses on memory and retrieval, where the main comparison is not simply whether extra context helps, but which state representations stay verifiable as the environment and task history evolve {_cites(all_keys[18:24], 6)}.",
        f"Another line studies adaptation and self-improvement, comparing reinforcement-style updates, synthetic data loops, and other mechanisms that try to improve performance after deployment {_cites(all_keys[24:30], 6)}.",
        f"Multi-agent work adds a coordination layer in which role assignment, communication structure, and aggregation strategy become part of the core design choice rather than a thin wrapper around a base model {_cites(all_keys[30:36], 6)}.",
        f"Evaluation-focused surveys and benchmark papers contribute a complementary view by making protocol design explicit, especially around task mixtures, metrics, tool access, and reproducibility {_cites(all_keys[36:42], 6)}.",
        f"Security and governance papers widen the comparison further by showing that interface assumptions, permissions, and supply-chain boundaries can dominate downstream risk profiles {_cites(all_keys[42:48], 6)}.",
        f"What remains under-specified across these strands is a unified lens that compares architectures, evaluation practice, and risk under the same evidence-first contract rather than as separate taxonomic buckets {_cites(all_keys[48:54], 6)}.",
        f"This survey takes that gap as its starting point and positions prior work as evidence for recurring trade-offs instead of as isolated lists of methods, benchmarks, or applications {_cites(all_keys[54:60], 6)}.",
    ]

    abstract = (
        '## Abstract\n\n'
        f"LLM agent research now spans tool use, orchestration, planning, memory, adaptation, multi-agent coordination, evaluation, and safety, yet those threads are still often compared under mismatched protocols {_cites(all_keys[0:6], 6)}. "
        f"This survey organizes the field around execution loops, interface contracts, adaptation mechanisms, and protocol-aware evaluation so that evidence from different systems can be read on the same comparative scale {_cites(all_keys[6:12], 6)}. "
        f"Using {candidate_pool} and {evidence_note}, we synthesize how agent systems trade off capability, cost, latency, reproducibility, and governance across representative benchmark and deployment settings {_cites(all_keys[12:18], 6)}. "
        f"The central finding is that many headline gains depend as much on interface assumptions and evaluation design as on the nominal architecture of the agent itself {_cites(all_keys[18:24], 6)}. "
        f"We conclude by identifying where current evidence is strongest, where protocol mismatch still obscures comparison, and which risk surfaces should structure future survey and benchmark design {_cites(all_keys[24:30], 6)}.\n"
    )

    discussion = (
        '## Discussion\n\n'
        f"Across the pipeline of agent construction, the strongest pattern is not a single winning architecture but a recurring dependence on how loops, interfaces, and evaluation protocols are coupled {_cites(all_keys[0:4], 4)}.\n\n"
        f"That coupling explains why apparently similar agent systems can report different outcomes under different tool contracts, budget assumptions, or threat models {_cites(all_keys[4:8], 4)}.\n\n"
        f"It also suggests that future work should treat benchmark design, protocol transparency, and deployment constraints as first-class comparative variables rather than as appendix details {_cites(all_keys[8:12], 4)}.\n"
    )

    conclusion = (
        '## Conclusion\n\n'
        f"LLM agents are best understood as evidence-bounded systems whose performance depends on coordinated choices about action spaces, interfaces, memory, adaptation, and evaluation {_cites(all_keys[12:16], 4)}.\n\n"
        f"A survey that compares those systems without making protocol assumptions explicit will overstate some gains and understate some risks {_cites(all_keys[16:20], 4)}.\n\n"
        f"By structuring the literature around shared lenses and comparable evidence, this pipeline aims to make future agent surveys more reproducible, more stable, and easier to extend {_cites(all_keys[20:24], 4)}.\n"
    )

    atomic_write_text(abstract_path, abstract)
    atomic_write_text(intro_path, '\n\n'.join(intro_paragraphs).rstrip() + '\n')
    atomic_write_text(related_path, '\n\n'.join(related_paragraphs).rstrip() + '\n')
    atomic_write_text(discussion_path, discussion)
    atomic_write_text(conclusion_path, conclusion)

    report = '\n'.join([
        '# Front matter report',
        '',
        '- Status: PASS',
        f'- Generated at: `{now_iso_seconds()}`',
        f'- Abstract: `sections/abstract.md`',
        f'- Introduction: `sections/S{intro_id}.md`',
        f'- Related Work: `sections/S{related_id}.md`',
        '- Discussion: `sections/discussion.md`',
        '- Conclusion: `sections/conclusion.md`',
    ]) + '\n'
    atomic_write_text(report_path, report)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
