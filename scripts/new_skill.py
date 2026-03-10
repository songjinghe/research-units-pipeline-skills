from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".codex" / "skills"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new reference-first skill skeleton under .codex/skills/<name>/")
    parser.add_argument("--name", required=True, help="Skill folder name (kebab-case recommended).")
    parser.add_argument("--category", default="", help="Optional category label (for humans).")
    parser.add_argument("--inputs", default="", help="Comma/semicolon-separated input artifact paths.")
    parser.add_argument("--outputs", default="", help="Comma/semicolon-separated output artifact paths.")
    parser.add_argument("--with-script", action="store_true", help="Also create scripts/run.py template.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing generated files if present.")
    args = parser.parse_args()

    name = _slug(args.name)
    if not name:
        raise SystemExit("Invalid --name (expected non-empty, kebab-case-ish).")

    inputs = _split_list(args.inputs)
    outputs = _split_list(args.outputs)

    skill_dir = SKILLS_DIR / name
    skill_dir.mkdir(parents=True, exist_ok=True)

    files: dict[Path, str] = {
        skill_dir / "SKILL.md": _render_skill_md(
            name=name,
            category=str(args.category or "").strip(),
            inputs=inputs,
            outputs=outputs,
            with_script=bool(args.with_script),
        ),
        skill_dir / "references" / "overview.md": _render_overview_md(name=name),
        skill_dir / "references" / "examples_good.md": _render_examples_good(name=name),
        skill_dir / "references" / "examples_bad.md": _render_examples_bad(name=name),
        skill_dir / "assets" / "schema.json": json.dumps(
            _render_schema(name=name, inputs=inputs, outputs=outputs),
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
    }
    if args.with_script:
        files[skill_dir / "scripts" / "run.py"] = _render_run_py(skill=name, default_inputs=inputs, default_outputs=outputs)

    for path, body in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not args.overwrite:
            raise SystemExit(f"Refusing to overwrite existing file: {path} (use --overwrite).")
        path.write_text(body, encoding="utf-8")

    print(f"Created reference-first skill skeleton: {skill_dir}")
    for path in files:
        print(f"- {path.relative_to(REPO_ROOT)}")
    print("Next: fill `references/` with domain examples/rubrics before adding semantic logic to scripts.")
    return 0


def _slug(value: str) -> str:
    value = str(value or "").strip().lower()
    value = re.sub(r"[^a-z0-9\-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value


def _split_list(value: str) -> list[str]:
    raw = str(value or "").strip()
    if not raw:
        return []
    return [p.strip() for p in re.split(r"[;,]\s*", raw) if p.strip()]


def _title(name: str) -> str:
    return " ".join([w.capitalize() for w in re.split(r"[-_]+", name) if w])


def _render_skill_md(*, name: str, category: str, inputs: list[str], outputs: list[str], with_script: bool) -> str:
    title = _title(name)
    cat_block = f"- Category: `{category}`\n" if category else ""
    inputs_lines = "\n".join([f"- `{p}`" for p in inputs]) if inputs else "- (none)"
    outputs_lines = "\n".join([f"- `{p}`" for p in outputs]) if outputs else "- (none)"
    script_note = "- `scripts/run.py` (deterministic helper; keep it thin).\n" if with_script else ""
    return f"""---
name: {name}
description: |
  <one-line summary>.
  **Trigger**: <keywords (EN/中文), comma-separated>.
  **Use when**: <when this skill is the right next step>.
  **Skip if**: <when not to use>.
  **Network**: <none|required|optional + offline fallback>.
  **Guardrail**: <invariants / block conditions / no-prose rules>.
---

# {title}

{cat_block}## Inputs

{inputs_lines}

## Outputs

{outputs_lines}

## Package layout

- `references/overview.md` (read first)
- `references/examples_good.md` (load when shaping high-quality outputs)
- `references/examples_bad.md` (load when checking anti-patterns)
- `assets/schema.json` (machine-readable contract)
{script_note}## Workflow

1. Read `references/overview.md` for the core workflow and boundaries.
2. Load `references/examples_good.md` and/or `references/examples_bad.md` only when the task is reader-facing or judgment-heavy.
3. Use `assets/schema.json` as the stable interface contract.
4. Use scripts only for deterministic work (validation, materialization, conversion), not for hidden semantic policy.

## Quality checklist

- [ ] `SKILL.md` stays lean and does not duplicate detailed domain content.
- [ ] Domain knowledge, rubrics, and examples live in `references/`.
- [ ] Templates/schemas live in `assets/`.
- [ ] Scripts remain deterministic and do not own reader-facing prose templates.
"""


def _render_overview_md(name: str) -> str:
    return f"""# Overview

This is the reference-first overview for `{name}`.

## Use this file for

- the core workflow
- decision rules
- when to block vs downgrade
- when to read more specific reference files

## Split of responsibilities

- `SKILL.md`: trigger, workflow, package navigation
- `references/`: domain knowledge, rubrics, examples, anti-patterns
- `assets/`: schemas, templates, machine-readable defaults
- `scripts/`: deterministic helpers only

## Checklist

- Keep reader-facing voice/pattern rules here, not in Python constants.
- Keep domain-specific variants in references or assets, not hard-coded in scripts.
- If you add a script, document when to run it and what it guarantees.
"""


def _render_examples_good(name: str) -> str:
    return f"""# Good examples

Use this file for concise, high-signal positive examples relevant to `{name}`.

## Example slots

- Good output shape
- Good decision rationale
- Good reader-facing wording
- Good structured sidecar
"""


def _render_examples_bad(name: str) -> str:
    return f"""# Bad examples

Use this file for anti-patterns relevant to `{name}`.

## Anti-pattern slots

- hidden domain defaults
- script-owned prose templates
- pipeline/workspace voice in reader-facing outputs
- filler text that hides missing evidence
- ellipsis / TODO / scaffold leakage
"""


def _render_schema(*, name: str, inputs: list[str], outputs: list[str]) -> dict:
    return {
        "skill_name": name,
        "mode": "reference-first",
        "inputs": inputs,
        "outputs": outputs,
        "references": [
            "references/overview.md",
            "references/examples_good.md",
            "references/examples_bad.md",
        ],
        "assets": ["assets/schema.json"],
        "script_policy": {
            "deterministic_only": True,
            "forbid_reader_facing_prose_templates": True,
            "forbid_hidden_domain_defaults": True,
        },
    }


def _render_run_py(*, skill: str, default_inputs: list[str], default_outputs: list[str]) -> str:
    ins = repr(default_inputs)
    outs = repr(default_outputs)
    return f"""from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', default='.')
    parser.add_argument('--unit-id', default='')
    parser.add_argument('--inputs', default='')
    parser.add_argument('--outputs', default='')
    parser.add_argument('--checkpoint', default='')
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()

    # Bootstrap: find repo root so we can import tooling.common
    _candidate = Path(__file__).resolve()
    for _ in range(10):
        if (_candidate / "AGENTS.md").exists():
            break
        _candidate = _candidate.parent
    sys.path.insert(0, str(_candidate))
    from tooling.common import find_repo_root, ensure_dir, parse_semicolon_list

    repo_root = find_repo_root(Path(__file__))

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs) or {ins}
    outputs = parse_semicolon_list(args.outputs) or {outs}

    manifest = {{
        'skill': {skill!r},
        'workspace': str(workspace),
        'inputs': inputs,
        'outputs': outputs,
        'strict': bool(args.strict),
    }}

    for out in outputs:
        out_path = workspace / out
        ensure_dir(out_path.parent)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
"""


if __name__ == "__main__":
    raise SystemExit(main())
