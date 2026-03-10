# Skill Audit Rules

This document defines the Phase 0 static audit rules enforced by `scripts/audit_skills.py`.

## Goal

Catch high-signal writer/pipeline smells in `.codex/skills/**` before they spread into reader-facing outputs.

This auditor is intentionally static and heuristic-driven:
- it scans repository skill files only
- it does not execute skill scripts
- it does not judge whether a finding is acceptable for a specific skill intent
- it does provide stable rule IDs, severities, and file:line references

## Scope

Scanned paths:
- `.codex/skills/*/SKILL.md`
- `.codex/skills/*/scripts/**`
- `.codex/skills/*/assets/**`
- `.codex/skills/*/references/**`

Ignored paths:
- `__pycache__/`
- `.pyc`

## CLI

Run from repo root:

```bash
python scripts/audit_skills.py
```

Useful options:

```bash
python scripts/audit_skills.py --format json
python scripts/audit_skills.py --fail-on ERROR
python scripts/audit_skills.py --fail-on NONE --report output/skill-audit.txt
```

Exit behavior:
- `0`: no findings at or above `--fail-on`
- `2`: at least one finding at or above `--fail-on`

Default threshold:
- `--fail-on WARN`

## Finding format

Text output format:

```text
[SEVERITY] rule_id path:line
  skill: <skill-name>
  message: <human-readable explanation>
  excerpt: <trimmed line>
```

JSON output includes:
- summary counts
- one object per finding
- `severity`, `rule_id`, `skill`, `path`, `line`, `message`, `excerpt`

## Rules

### `generic_domain_hardcoding`

Default severity:
- `WARN`

What it flags:
- hardcoded generic-domain phrases such as:
  - `LLM agents`
  - `Large language model agents`

Why it matters:
- domain-specific phrasing inside reusable writer/tooling skills often leaks into unrelated outputs and reduces portability.

Detection:
- regex scan on text lines across `SKILL.md`, scripts, and assets.

Caveats:
- some skills are intentionally domain-specific; review the finding before changing it.

### `forced_paragraph_count`

Default severity:
- `ERROR`

What it flags:
- script loops that pad prose to a minimum paragraph count, specifically patterns like:
  - `while len(paragraphs) < ...`

Why it matters:
- this is a strong signal of template/filler generation rather than evidence-driven writing.

Detection:
- regex scan in script files.

Caveats:
- this rule is intentionally narrow in Phase 0; it does not yet flag every paragraph-budget smell.

### `pipeline_voice`

Default severity:
- `WARN`

What it flags:
- internal/pipeline framing phrases such as:
  - `this pipeline aims`
  - `across the pipeline`

Why it matters:
- process voice is appropriate in tooling docs, but it becomes a reader-facing smell when copied into generated prose or prompts.

Detection:
- regex scan on text lines.

Caveats:
- the auditor currently checks a small phrase family; future phases can widen this list.

### `reader_facing_ellipsis`

Default severity:
- `WARN` in scripts/assets
- `INFO` in `SKILL.md`

What it flags:
- ellipsis-like tokens that often leak into outputs:
  - `...`
  - `…`
  - `... (N more)`
  - `... (12 more)`

Why it matters:
- ellipses are often placeholders, truncation markers, or UI/debug artifacts that read badly in final outputs.

Detection:
- literal/regex scan on text lines.

Caveats:
- this is heuristic and may flag negative examples, troubleshooting examples, or explanatory docs.
- Phase 0 does not attempt semantic disambiguation.

### `script_heavy_without_references`

Default severity:
- `WARN`

What it flags:
- a skill whose `scripts/` directory is substantial, but whose `SKILL.md` does not point users to that script surface.

Current Phase 0 definition of “script-heavy”:
- `>=2` script files, or
- `>=80` non-empty script lines total

Current Phase 0 definition of “referenced”:
- `SKILL.md` contains at least one of:
  - `scripts/`
  - `run.py`
  - `helper script`
  - `bootstrap script`
  - `quick start`
  - `all options`
  - `## script`
  - `### script`

Why it matters:
- hidden script logic makes skills harder to audit, harder to use correctly, and easier to drift away from documented behavior.

Detection:
- per-skill structural check, reported against `SKILL.md:1`.

Caveats:
- this rule does not inspect whether the references are good, only whether they exist.
- a simple wrapper script with low LOC will not trigger this rule.

## Known limitations

Phase 0 intentionally stays conservative:
- no AST parsing
- no prompt-template semantic analysis
- no cross-file provenance tracing into non-skill modules like `tooling/`
- no reader-facing vs internal-text classifier beyond simple path-based severity tuning

That means:
- some acceptable domain-specific phrases may be flagged
- some prose hardcoding outside the exact phrase list will be missed
- renderer helpers called from skill scripts but implemented outside `.codex/skills/**` are out of scope for this auditor

## Future extensions

Likely Phase 1/2 additions:
- fixed section skeleton detection (`Abstract`, `Discussion`, `Conclusion`, numbered memo sections)
- fixed writer-card fields (`Why now`, `Kill criteria`, `Strong positive signal`)
- paragraph-budget literals (`6–10 paragraphs`, `10-12 paragraphs`)
- stronger pipeline-voice phrase families (`quality gate`, `evidence pack`, `writer context pack`)
- AST-aware detection for emitted hardcoded prose in Python f-strings and list joins
