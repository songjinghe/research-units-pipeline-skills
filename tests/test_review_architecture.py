from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tooling.pipeline_spec import PipelineSpec


REPO_ROOT = Path(__file__).resolve().parents[1]


class ReviewArchitectureTests(unittest.TestCase):
    def test_review_products_expose_deliverable_contract_fields(self) -> None:
        brief = PipelineSpec.load(REPO_ROOT / "pipelines" / "research-brief.pipeline.md")
        paper = PipelineSpec.load(REPO_ROOT / "pipelines" / "paper-review.pipeline.md")
        evidence = PipelineSpec.load(REPO_ROOT / "pipelines" / "evidence-review.pipeline.md")

        self.assertEqual(brief.quality_contract["deliverable_kind"], "brief")
        self.assertEqual(brief.quality_contract["evidence_mode"], "light")
        self.assertFalse(brief.quality_contract["candidate_pool_policy"]["keep_full_deduped_pool"])

        self.assertEqual(paper.quality_contract["deliverable_kind"], "paper_review")
        self.assertEqual(paper.quality_contract["evidence_mode"], "manuscript_traceable")
        self.assertFalse(paper.quality_contract["candidate_pool_policy"]["keep_full_deduped_pool"])

        self.assertEqual(evidence.quality_contract["deliverable_kind"], "evidence_review")
        self.assertEqual(evidence.quality_contract["evidence_mode"], "protocol_driven")
        self.assertTrue(evidence.quality_contract["candidate_pool_policy"]["keep_full_deduped_pool"])

    def test_shared_review_modules_exist(self) -> None:
        import tooling.review_artifacts as review_artifacts
        import tooling.review_protocol as review_protocol
        import tooling.review_render as review_render
        import tooling.review_text as review_text

        self.assertTrue(callable(review_text.pick_claim_candidates))
        self.assertTrue(callable(review_protocol.parse_protocol))
        self.assertTrue(callable(review_artifacts.load_candidate_records))
        self.assertTrue(callable(review_render.render_claims_markdown))

    def test_review_text_claim_candidate_extraction(self) -> None:
        from tooling.review_text import pick_claim_candidates

        text = (
            "# Demo Paper\n\n"
            "## Abstract\n"
            "We propose RoboAdapt, a robot policy adaptation method.\n\n"
            "## Experiments\n"
            "We show RoboAdapt improves success rate by 12% on manipulation benchmarks.\n"
        )
        claims = pick_claim_candidates(text, limit=3)
        self.assertTrue(claims)
        self.assertIn("We propose RoboAdapt", claims[0]["sentence"])

    def test_review_protocol_parses_schema_rows(self) -> None:
        from tooling.review_protocol import parse_protocol

        text = (
            "# Protocol\n\n"
            "## Review Questions\n"
            "- RQ1: tutoring agents\n\n"
            "## Inclusion Criteria\n"
            "- I1: Include tutoring systems.\n\n"
            "## Exclusion Criteria\n"
            "- E1: Exclude non-education systems.\n\n"
            "## Extraction Schema\n"
            "| field | definition | allowed_values | notes |\n"
            "|---|---|---|---|\n"
            "| task | main task | free text | short label |\n"
        )
        parsed = parse_protocol(text)
        self.assertEqual(parsed["review_questions"], ["RQ1: tutoring agents"])
        self.assertEqual(parsed["inclusion"][0][0], "I1")
        self.assertEqual(parsed["extraction_fields"][0]["field"], "task")

    def test_research_brief_cli_smoke(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "workspaces") as tmp:
            workspace = Path(tmp)
            subprocess.run(
                [sys.executable, "scripts/pipeline.py", "init", "--workspace", str(workspace), "--pipeline", "research-brief", "--overwrite"],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            (workspace / "papers").mkdir(parents=True, exist_ok=True)
            records = []
            for idx in range(1, 6):
                records.append(
                    {
                        "title": f"Brief Paper {idx}",
                        "year": 2024,
                        "url": f"https://example.com/{idx}",
                        "abstract": "Topic overview for robotics adaptation.",
                    }
                )
            (workspace / "papers" / "papers_raw.jsonl").write_text(
                "\n".join(json.dumps(record) for record in records) + "\n",
                encoding="utf-8",
            )
            subprocess.run(
                [sys.executable, "scripts/pipeline.py", "run", "--workspace", str(workspace), "--max-steps", "2"],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [sys.executable, "scripts/pipeline.py", "mark", "--workspace", str(workspace), "--unit-id", "U010", "--status", "DONE"],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [sys.executable, "scripts/pipeline.py", "run", "--workspace", str(workspace), "--max-steps", "20", "--auto-approve", "C2"],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue((workspace / "output" / "SNAPSHOT.md").exists())
            self.assertIn("- Status: PASS", (workspace / "output" / "DELIVERABLE_SELFLOOP_TODO.md").read_text(encoding="utf-8"))
            self.assertIn("- Status: PASS", (workspace / "output" / "CONTRACT_REPORT.md").read_text(encoding="utf-8"))

    def test_paper_review_cli_smoke(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "workspaces") as tmp:
            workspace = Path(tmp)
            subprocess.run(
                [sys.executable, "scripts/pipeline.py", "init", "--workspace", str(workspace), "--pipeline", "paper-review", "--overwrite"],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            (workspace / "inputs").mkdir(parents=True, exist_ok=True)
            (workspace / "inputs" / "manuscript.md").write_text(
                "# Demo Manuscript\n\n## Abstract\nWe propose RoboAdapt.\n\n## Experiments\nWe show RoboAdapt improves success rate by 12% on robot manipulation benchmarks.\n\n## References\n- Prior Work A\n- Prior Work B\n- Prior Work C\n- Prior Work D\n- Prior Work E\n",
                encoding="utf-8",
            )
            subprocess.run(
                [sys.executable, "scripts/pipeline.py", "run", "--workspace", str(workspace), "--max-steps", "20"],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue((workspace / "output" / "REVIEW.md").exists())
            self.assertIn("- Status: PASS", (workspace / "output" / "DELIVERABLE_SELFLOOP_TODO.md").read_text(encoding="utf-8"))
            self.assertIn("- Status: PASS", (workspace / "output" / "CONTRACT_REPORT.md").read_text(encoding="utf-8"))

    def test_evidence_review_cli_smoke(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "workspaces") as tmp:
            workspace = Path(tmp)
            subprocess.run(
                [sys.executable, "scripts/pipeline.py", "init", "--workspace", str(workspace), "--pipeline", "evidence-review", "--overwrite"],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            (workspace / "GOAL.md").write_text("# Goal\n\nReview tutoring agents.\n", encoding="utf-8")
            (workspace / "queries.md").write_text("- keywords:\n  - tutoring agents\n- exclude:\n  - marketing\n", encoding="utf-8")
            subprocess.run(
                [sys.executable, "scripts/pipeline.py", "run", "--workspace", str(workspace), "--max-steps", "4", "--auto-approve", "C1"],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            (workspace / "papers").mkdir(parents=True, exist_ok=True)
            records = []
            for idx in range(1, 4):
                records.append(
                    {
                        "title": f"Tutoring Study {idx}",
                        "year": 2024,
                        "url": f"https://example.com/t{idx}",
                        "abstract": "Education tutoring agent with evaluation.",
                    }
                )
            (workspace / "papers" / "papers_raw.jsonl").write_text(
                "\n".join(json.dumps(record) for record in records) + "\n",
                encoding="utf-8",
            )
            (workspace / "papers" / "retrieval_report.md").write_text(
                "# Retrieval report\n\n- Seeded candidate pool for smoke test.\n",
                encoding="utf-8",
            )
            subprocess.run(
                [sys.executable, "scripts/pipeline.py", "mark", "--workspace", str(workspace), "--unit-id", "U025", "--status", "DONE"],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [sys.executable, "scripts/pipeline.py", "run", "--workspace", str(workspace), "--max-steps", "20"],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue((workspace / "output" / "PROTOCOL.md").exists())
            self.assertTrue((workspace / "papers" / "screening_log.csv").exists())
            self.assertTrue((workspace / "papers" / "extraction_table.csv").exists())
            self.assertTrue((workspace / "output" / "SYNTHESIS.md").exists())
            self.assertIn("- Status: PASS", (workspace / "output" / "DELIVERABLE_SELFLOOP_TODO.md").read_text(encoding="utf-8"))
            self.assertIn("- Status: PASS", (workspace / "output" / "CONTRACT_REPORT.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
