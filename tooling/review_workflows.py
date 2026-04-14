from __future__ import annotations

from tooling.review_artifacts import (
    choose_candidate_pool_path,
    extract_pdf_text,
    find_workspace_text_source,
    load_candidate_records,
    read_csv_rows,
    stable_paper_id,
    summarize_outline,
    write_csv_rows,
    write_text,
)
from tooling.review_protocol import maybe_parse_queries_md, parse_protocol, parse_protocol_extraction_fields, protocol_markdown
from tooling.review_render import (
    render_claims_markdown,
    render_evidence_synthesis_markdown,
    render_gap_report_markdown,
    render_novelty_matrix_markdown,
    render_research_brief_markdown,
    render_rubric_review_markdown,
)
from tooling.review_text import (
    CLAIM_PATTERNS,
    EMPIRICAL_HINTS,
    classify_claim,
    extract_related_works,
    heading_context_sentences,
    parse_item_blocks,
    pick_claim_candidates,
    split_sentences,
    text_tokens as title_tokens,
)
