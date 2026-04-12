from __future__ import annotations

import shutil
import socket
import subprocess
import sys
import tempfile
import textwrap
import threading
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from tooling.common import resolve_pipeline_spec_path
from tooling.pipeline_spec import PipelineSpec


REPO_ROOT = Path(__file__).resolve().parents[1]


class SourceTutorialPipelineTests(unittest.TestCase):
    def test_source_tutorial_pipeline_spec_loads(self) -> None:
        path = resolve_pipeline_spec_path(repo_root=REPO_ROOT, pipeline_value="source-tutorial")
        self.assertIsNotNone(path)

        spec = PipelineSpec.load(path)
        self.assertEqual(spec.name, "source-tutorial")
        self.assertEqual(tuple(spec.stages.keys()), ("C0", "C1", "C2", "C3", "C4"))
        self.assertIn("sources/manifest.yml", spec.target_artifacts)
        self.assertIn("output/TUTORIAL.md", spec.target_artifacts)
        self.assertIn("latex/slides/main.tex", spec.target_artifacts)
        self.assertIn("video", spec.quality_contract["source_policy"]["accepted_source_kinds"])

    def test_tutorial_alias_resolves_to_source_tutorial(self) -> None:
        path = resolve_pipeline_spec_path(repo_root=REPO_ROOT, pipeline_value="tutorial")
        self.assertIsNotNone(path)
        self.assertEqual(path.name, "source-tutorial.pipeline.md")

    def test_source_manifest_script_scaffolds_and_blocks_until_sources_exist(self) -> None:
        script = REPO_ROOT / ".codex" / "skills" / "source-manifest" / "scripts" / "run.py"
        self.assertTrue(script.exists(), f"missing script: {script}")

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            (workspace / "GOAL.md").write_text("# Goal\n\nTeach robot learning from mixed sources.\n", encoding="utf-8")

            blocked = subprocess.run(
                [sys.executable, str(script), "--workspace", str(workspace)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(blocked.returncode, 0)
            manifest = workspace / "sources" / "manifest.yml"
            self.assertTrue(manifest.exists())

            manifest.write_text(
                textwrap.dedent(
                    """\
                    sources:
                      - source_id: intro-web
                        kind: webpage
                        locator: https://example.com/robot-learning
                        label: Robot Learning Intro
                        required: true
                        notes: Reader-friendly overview.
                    """
                ),
                encoding="utf-8",
            )

            ok = subprocess.run(
                [sys.executable, str(script), "--workspace", str(workspace)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(ok.returncode, 0, msg=ok.stderr or ok.stdout)

    def test_source_manifest_accepts_video_kind(self) -> None:
        script = REPO_ROOT / ".codex" / "skills" / "source-manifest" / "scripts" / "run.py"
        self.assertTrue(script.exists(), f"missing script: {script}")

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            (workspace / "sources").mkdir(parents=True, exist_ok=True)
            (workspace / "sources" / "manifest.yml").write_text(
                textwrap.dedent(
                    """\
                    sources:
                      - source_id: yt-video
                        kind: video
                        locator: https://www.youtube.com/watch?v=aircAruvnKk
                        transcript_locator: captions.vtt
                        label: YouTube Video
                        required: true
                        notes: Video source.
                    """
                ),
                encoding="utf-8",
            )

            proc = subprocess.run(
                [sys.executable, str(script), "--workspace", str(workspace)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)

    def test_source_manifest_rejects_youtube_video_without_transcript(self) -> None:
        script = REPO_ROOT / ".codex" / "skills" / "source-manifest" / "scripts" / "run.py"
        self.assertTrue(script.exists(), f"missing script: {script}")

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            (workspace / "sources").mkdir(parents=True, exist_ok=True)
            (workspace / "sources" / "manifest.yml").write_text(
                textwrap.dedent(
                    """\
                    sources:
                      - source_id: yt-video
                        kind: video
                        locator: https://www.youtube.com/watch?v=aircAruvnKk
                        label: YouTube Video
                        required: true
                        notes: Missing transcript on purpose.
                    """
                ),
                encoding="utf-8",
            )

            proc = subprocess.run(
                [sys.executable, str(script), "--workspace", str(workspace)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("transcript_locator", proc.stderr)

    def test_beamer_scaffold_generates_slides_from_tutorial(self) -> None:
        script = REPO_ROOT / ".codex" / "skills" / "beamer-scaffold" / "scripts" / "run.py"
        self.assertTrue(script.exists(), f"missing script: {script}")

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            (workspace / "output").mkdir(parents=True, exist_ok=True)
            (workspace / "output" / "TUTORIAL.md").write_text(
                textwrap.dedent(
                    """\
                    # Robot Learning Tutorial

                    ## Who This Is For
                    Early-stage robotics students.

                    ## Module 1: Behavior Cloning
                    ### Why it matters
                    Behavior cloning is the fastest way to get a first policy working.

                    ### Key idea
                    Learn a direct mapping from observations to actions.

                    ### Worked example
                    Train on a simple pick-and-place dataset.

                    ### Check yourself
                    Explain when behavior cloning fails under covariate shift.

                    ### Source notes
                    - https://example.com/robot-learning
                    """
                ),
                encoding="utf-8",
            )

            proc = subprocess.run(
                [sys.executable, str(script), "--workspace", str(workspace)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)

            tex_path = workspace / "latex" / "slides" / "main.tex"
            self.assertTrue(tex_path.exists())
            text = tex_path.read_text(encoding="utf-8")
            self.assertIn(r"\documentclass", text)
            self.assertIn("beamer", text)
            self.assertIn("Behavior Cloning", text)

    def test_latex_scaffold_prefers_tutorial_over_placeholder_draft(self) -> None:
        script = REPO_ROOT / ".codex" / "skills" / "latex-scaffold" / "scripts" / "run.py"
        self.assertTrue(script.exists(), f"missing script: {script}")

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            (workspace / "output").mkdir(parents=True, exist_ok=True)
            (workspace / "citations").mkdir(parents=True, exist_ok=True)
            (workspace / "citations" / "ref.bib").write_text("% placeholder bib\n", encoding="utf-8")
            (workspace / "output" / "DRAFT.md").write_text("# Draft (placeholder)\n\nPlaceholder only.\n", encoding="utf-8")
            (workspace / "output" / "TUTORIAL.md").write_text(
                "# Actual Tutorial\n\n## Who This Is For\nReaders.\n\n## Module 1\n### Why it matters\nReal content.\n",
                encoding="utf-8",
            )

            proc = subprocess.run(
                [sys.executable, str(script), "--workspace", str(workspace)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)
            tex = (workspace / "latex" / "main.tex").read_text(encoding="utf-8")
            self.assertIn("Actual Tutorial", tex)
            self.assertNotIn("Draft (placeholder)", tex)

    def test_tutorial_selfloop_reports_fail_without_required_sections(self) -> None:
        script = REPO_ROOT / ".codex" / "skills" / "tutorial-selfloop" / "scripts" / "run.py"
        self.assertTrue(script.exists(), f"missing script: {script}")

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            (workspace / "output").mkdir(parents=True, exist_ok=True)
            (workspace / "output" / "TUTORIAL.md").write_text("# Thin Tutorial\n\n## Module 1\nOnly one paragraph.\n", encoding="utf-8")

            proc = subprocess.run(
                [sys.executable, str(script), "--workspace", str(workspace)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(proc.returncode, 0)
            report = workspace / "output" / "TUTORIAL_SELFLOOP_TODO.md"
            self.assertTrue(report.exists())
            self.assertIn("- Status: FAIL", report.read_text(encoding="utf-8"))

    def test_source_ingest_repo_reads_readme_docs(self) -> None:
        script = REPO_ROOT / ".codex" / "skills" / "source-ingest" / "scripts" / "run.py"
        self.assertTrue(script.exists(), f"missing script: {script}")

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            repo_dir = workspace / "repo"
            docs_dir = repo_dir / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)
            (repo_dir / "README.md").write_text("# Demo Repo\n\nIntro text.\n", encoding="utf-8")
            (docs_dir / "guide.md").write_text("# Guide\n\nMore details.\n", encoding="utf-8")
            (workspace / "sources").mkdir(parents=True, exist_ok=True)
            (workspace / "sources" / "manifest.yml").write_text(
                textwrap.dedent(
                    f"""\
                    sources:
                      - source_id: repo-demo
                        kind: repo
                        locator: {repo_dir}
                        label: Demo Repo
                        required: true
                        notes: Local repo fixture.
                    """
                ),
                encoding="utf-8",
            )

            proc = subprocess.run(
                [sys.executable, str(script), "--workspace", str(workspace)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)

            index_text = (workspace / "sources" / "index.jsonl").read_text(encoding="utf-8")
            self.assertIn('"status": "success"', index_text)
            self.assertTrue((workspace / "sources" / "normalized" / "repo-demo" / "README.md").exists())

    def test_source_ingest_pdf_local_file_succeeds(self) -> None:
        script = REPO_ROOT / ".codex" / "skills" / "source-ingest" / "scripts" / "run.py"
        self.assertTrue(script.exists(), f"missing script: {script}")

        xelatex = shutil.which("xelatex")
        self.assertIsNotNone(xelatex, "xelatex is required for the local PDF fixture")

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            pdf_dir = workspace / "pdfsrc"
            pdf_dir.mkdir(parents=True, exist_ok=True)
            tex_path = pdf_dir / "mini.tex"
            tex_path.write_text(
                "\n".join(
                    [
                        r"\documentclass{article}",
                        r"\begin{document}",
                        "Robot learning starts from data, actions, and feedback.",
                        r"\end{document}",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            proc = subprocess.run(
                [xelatex, "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
                cwd=str(pdf_dir),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)
            pdf_path = pdf_dir / "mini.pdf"
            self.assertTrue(pdf_path.exists())

            (workspace / "sources").mkdir(parents=True, exist_ok=True)
            (workspace / "sources" / "manifest.yml").write_text(
                textwrap.dedent(
                    f"""\
                    sources:
                      - source_id: pdf-demo
                        kind: pdf
                        locator: {pdf_path}
                        label: Local PDF
                        required: true
                        notes: Local PDF fixture.
                    """
                ),
                encoding="utf-8",
            )

            ingest = subprocess.run(
                [sys.executable, str(script), "--workspace", str(workspace)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(ingest.returncode, 0, msg=ingest.stderr or ingest.stdout)
            text = (workspace / "sources" / "normalized" / "pdf-demo.md").read_text(encoding="utf-8")
            self.assertIn("Robot learning starts from data", text)

    def test_source_ingest_docs_site_local_server_succeeds(self) -> None:
        script = REPO_ROOT / ".codex" / "skills" / "source-ingest" / "scripts" / "run.py"
        self.assertTrue(script.exists(), f"missing script: {script}")

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            site_dir = workspace / "site"
            site_dir.mkdir(parents=True, exist_ok=True)
            (site_dir / "index.html").write_text(
                "<html><head><title>Docs Home</title></head><body><h1>Docs Home</h1><p>Intro page.</p><a href=\"guide.html\">Guide</a></body></html>",
                encoding="utf-8",
            )
            (site_dir / "guide.html").write_text(
                "<html><head><title>Guide</title></head><body><h1>Guide</h1><p>Detailed guide page.</p></body></html>",
                encoding="utf-8",
            )

            class QuietHandler(SimpleHTTPRequestHandler):
                def log_message(self, format: str, *args: object) -> None:  # noqa: A003
                    return

            cwd = Path.cwd()
            try:
                import os

                os.chdir(site_dir)
                with socket.socket() as sock:
                    sock.bind(("127.0.0.1", 0))
                    host, port = sock.getsockname()
                server = ThreadingHTTPServer(("127.0.0.1", port), QuietHandler)
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                try:
                    (workspace / "sources").mkdir(parents=True, exist_ok=True)
                    (workspace / "sources" / "manifest.yml").write_text(
                        textwrap.dedent(
                            f"""\
                            sources:
                              - source_id: docs-demo
                                kind: docs_site
                                locator: http://127.0.0.1:{port}/index.html
                                label: Local Docs Site
                                required: true
                                notes: Local docs site fixture.
                            """
                        ),
                        encoding="utf-8",
                    )

                    ingest = subprocess.run(
                        [sys.executable, str(script), "--workspace", str(workspace)],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(ingest.returncode, 0, msg=ingest.stderr or ingest.stdout)
                finally:
                    server.shutdown()
                    thread.join(timeout=2)
                    server.server_close()
            finally:
                import os

                os.chdir(cwd)

            self.assertTrue((workspace / "sources" / "normalized" / "docs-demo" / "page-01.md").exists())

    def test_source_ingest_video_with_local_transcript_succeeds(self) -> None:
        script = REPO_ROOT / ".codex" / "skills" / "source-ingest" / "scripts" / "run.py"
        self.assertTrue(script.exists(), f"missing script: {script}")

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            (workspace / "sources").mkdir(parents=True, exist_ok=True)
            transcript = workspace / "captions.vtt"
            transcript.write_text(
                textwrap.dedent(
                    """\
                    WEBVTT

                    00:00:00.000 --> 00:00:02.000
                    Reinforcement learning starts with interaction.

                    00:00:02.000 --> 00:00:05.000
                    Policies improve by trial and error.
                    """
                ),
                encoding="utf-8",
            )
            (workspace / "sources" / "manifest.yml").write_text(
                textwrap.dedent(
                    f"""\
                    sources:
                      - source_id: yt-video
                        kind: video
                        locator: https://www.youtube.com/watch?v=aircAruvnKk
                        transcript_locator: {transcript}
                        label: YouTube Video
                        required: true
                        notes: Use sidecar transcript.
                    """
                ),
                encoding="utf-8",
            )

            proc = subprocess.run(
                [sys.executable, str(script), "--workspace", str(workspace)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)
            text = (workspace / "sources" / "normalized" / "yt-video.md").read_text(encoding="utf-8")
            self.assertIn("Reinforcement learning starts with interaction.", text)

    def test_source_ingest_rejects_video_pages_as_plain_webpages(self) -> None:
        script = REPO_ROOT / ".codex" / "skills" / "source-ingest" / "scripts" / "run.py"
        self.assertTrue(script.exists(), f"missing script: {script}")

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            (workspace / "sources").mkdir(parents=True, exist_ok=True)
            (workspace / "sources" / "manifest.yml").write_text(
                textwrap.dedent(
                    """\
                    sources:
                      - source_id: yt-page
                        kind: webpage
                        locator: https://www.youtube.com/watch?v=aircAruvnKk
                        label: YouTube Page
                        required: true
                        notes: Wrong kind on purpose.
                    """
                ),
                encoding="utf-8",
            )

            proc = subprocess.run(
                [sys.executable, str(script), "--workspace", str(workspace)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(proc.returncode, 0)
            index_text = (workspace / "sources" / "index.jsonl").read_text(encoding="utf-8")
            self.assertIn('"status": "failed"', index_text)
            self.assertIn("use `kind: video`", index_text)


if __name__ == "__main__":
    unittest.main()
