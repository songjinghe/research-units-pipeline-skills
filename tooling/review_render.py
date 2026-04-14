from __future__ import annotations

from collections import Counter


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


def render_gap_report_markdown(gaps: list[dict[str, str]]) -> str:
    lines = ["# Missing Evidence", ""]
    for gap in gaps:
        lines.extend(
            [
                f"### {gap['id']}",
                f"- Claim ID: {gap['claim_id']}",
                f"- Claim: {gap['claim']}",
                f"- Evidence present: {gap['evidence_present']}",
                f"- Gap / concern: {gap['gap']}",
                f"- Minimal fix: {gap['minimal_fix']}",
                f"- Severity: {gap['severity']}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_novelty_matrix_markdown(rows: list[dict[str, str]]) -> str:
    lines = [
        "# Novelty Matrix",
        "",
        "| Claim ID | Claim | Closest related work | Overlap | Delta | Evidence |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['claim_id']} | {row['claim']} | {row['related_work']} | {row['overlap']} | {row['delta']} | {row['evidence']} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def render_rubric_review_markdown(*, claim_count: int, gap_count: int, major_gaps: list[dict[str, str]], novelty_available: bool) -> str:
    recommendation = "weak_reject" if major_gaps else ("borderline" if gap_count else "weak_accept")
    novelty_note = (
        "Novelty was assessed conservatively from the available novelty matrix."
        if novelty_available
        else "Novelty matrix was unavailable; novelty is therefore conservative."
    )
    lines = [
        "# Review",
        "",
        "### Summary",
        f"- The paper claims {claim_count} main contribution(s) and is reviewed through explicit claim and gap extraction.",
        "",
        "### Novelty",
        f"- {novelty_note}",
        "",
        "### Soundness",
        f"- The review surfaced {len(major_gaps)} major and {max(0, gap_count - len(major_gaps))} minor evidence issues.",
        "",
        "### Clarity",
        "- The main clarity risk is whether each top claim states its protocol, metric, and boundary explicitly.",
        "",
        "### Impact",
        "- If the major issues are fixed, the work could become easier to compare and reproduce.",
        "",
        "### Major Concerns",
    ]
    if major_gaps:
        for gap in major_gaps:
            lines.extend(
                [
                    f"- Problem: {gap['gap']}",
                    "- Why it matters: the current evidence chain is not strong enough for a confident acceptance decision.",
                    f"- Minimal fix: {gap['minimal_fix']}",
                ]
            )
    else:
        lines.append("- (none)")
    lines.extend(["", "### Minor Comments"])
    if gap_count:
        for gap in major_gaps[:3]:
            lines.append(f"- {gap['minimal_fix']}")
        if not major_gaps:
            lines.append("- Clarify the strongest remaining evidence gaps and manuscript boundaries.")
    else:
        lines.append("- (none)")
    lines.extend(["", "### Recommendation", f"- {recommendation}"])
    return "\n".join(lines).rstrip() + "\n"


def render_research_brief_markdown(*, sections: list[str], bullets: list[str], pointers: list[str], paper_count: int) -> str:
    chosen = pointers[: min(12, len(pointers))]
    scope_bullets = bullets[:3] or [f"Focus on {sections[0]}." if sections else "Focus on the target topic."]
    theme_bullets = bullets[3:9] or bullets[:6] or [f"The literature clusters around {sections[0]}." if sections else "The literature has a small set of recurring themes."]

    lines = ["# Research Brief", "", "## Scope"]
    for idx, bullet in enumerate(scope_bullets, start=1):
        pointer = chosen[(idx - 1) % len(chosen)] if chosen else "the current core set"
        lines.append(f"- {bullet.rstrip('.')} with concrete anchors in {pointer}.")
    lines.extend(
        [
            "",
            "## Evidence policy",
            f"- This brief uses {paper_count} papers from `papers/core_set.csv` and stays pointer-heavy rather than narrative-heavy.",
            "",
            "## Taxonomy",
        ]
    )
    for title in sections[:6]:
        lines.append(f"- {title}")
    lines.extend(["", "## Key themes"])
    for idx, bullet in enumerate(theme_bullets[:6], start=1):
        if chosen:
            a = chosen[(idx - 1) % len(chosen)]
            b = chosen[idx % len(chosen)] if len(chosen) > 1 else a
            lines.append(f"- {bullet.rstrip('.')} This is easiest to contrast through {a} versus {b}.")
        else:
            lines.append(f"- {bullet.rstrip('.')}.")
    lines.extend(["", "## What to read first"])
    for pointer in chosen:
        lines.append(f"- {pointer}")
    lines.extend(
        [
            "",
            "## Open problems / risks",
            f"- The current paper set still leaves open questions around {sections[-1] if sections else 'evaluation scope'} and transferability.",
            "- Several themes need stronger benchmark alignment before they can support survey-grade claims.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_evidence_synthesis_markdown(rows: list[dict[str, str]]) -> str:
    years = [int(row["year"]) for row in rows if str(row.get("year") or "").isdigit()]
    tasks = [str(row.get("task") or "").strip() for row in rows if str(row.get("task") or "").strip()]
    rob_counts = Counter(str(row.get("rob_overall") or "unclear").strip() or "unclear" for row in rows)
    year_span = f"{min(years)}-{max(years)}" if years else "unknown"
    task_summary = ", ".join(sorted(set(tasks))) if tasks else "mixed tasks with sparse deterministic labels"

    lines = [
        "# Evidence Review Synthesis",
        "",
        "## Research questions + scope",
        "- This synthesis follows the current protocol and only reports what the extraction table supports.",
        "",
        "## Included studies summary",
        f"- Included studies: {len(rows)}",
        f"- Year span: {year_span}",
        f"- Task coverage: {task_summary}",
        "",
        "## Findings by theme",
        f"- The current extracted evidence clusters around {task_summary}.",
        "- The deterministic pass keeps findings conservative and avoids claiming effects not present in the table.",
        "",
        "## Risk of bias",
        f"- Overall RoB counts: low={rob_counts.get('low', 0)}, unclear={rob_counts.get('unclear', 0)}, high={rob_counts.get('high', 0)}.",
        "- Protocol detail and confounding control remain the main reasons to keep conclusions bounded.",
        "",
        "## Supported conclusions",
        "- The extracted evidence supports descriptive conclusions about the included study pool and its reported tasks/metrics.",
        "",
        "## Needs more evidence",
        "- Strong comparative or causal claims still need richer extraction fields, stronger protocol detail, or more complete reporting.",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"
