from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_ROOT = REPO_ROOT / "skills"
DEFAULT_STATE_DIR = REPO_ROOT / "workspaces" / "clawhub-sync-daemon"

RATE_LIMIT_RE = re.compile(
    r"(Rate limit:\s*max\s*(\d+)\s*new skills per hour|Rate limit exceeded)",
    re.IGNORECASE,
)
DRY_RUN_COUNT_RE = re.compile(r"would upload\s+(\d+)\s+skill", re.IGNORECASE)

STOP_REQUESTED = False


@dataclass
class CommandResult:
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def combined(self) -> str:
        if self.stderr:
            return f"{self.stdout}\n{self.stderr}".strip()
        return self.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Retry ClawHub sync in the background until all skills are published.")
    parser.add_argument("--skills-root", default=str(DEFAULT_SKILLS_ROOT), help="Directory that contains exported skills.")
    parser.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR), help="Directory for daemon state, logs, and pid.")
    parser.add_argument("--bump", default="patch", help="Version bump to pass to `clawhub sync`.")
    parser.add_argument(
        "--changelog",
        default="Bulk sync from research-units-pipeline-skills exports",
        help="Changelog text for updates.",
    )
    parser.add_argument("--tags", default="latest", help="Comma-separated tags to publish.")
    parser.add_argument(
        "--rate-limit-sleep-seconds",
        type=int,
        default=3660,
        help="How long to wait after a ClawHub new-skill rate limit error.",
    )
    parser.add_argument(
        "--unexpected-retry-seconds",
        type=int,
        default=600,
        help="How long to wait before retrying an unexpected failure.",
    )
    parser.add_argument(
        "--max-unexpected-failures",
        type=int,
        default=6,
        help="Stop after this many consecutive unexpected failures.",
    )
    parser.add_argument("--once", action="store_true", help="Run a single sync attempt and exit.")
    args = parser.parse_args()

    state_dir = Path(args.state_dir).resolve()
    state_dir.mkdir(parents=True, exist_ok=True)
    log_path = state_dir / "daemon.log"
    state_path = state_dir / "state.json"
    pid_path = state_dir / "daemon.pid"

    install_signal_handlers()

    pid_path.write_text(f"{os.getpid()}\n", encoding="utf-8")
    logger = Logger(log_path)
    logger.log("daemon", f"starting pid={os.getpid()} state_dir={state_dir}")

    skills_root = Path(args.skills_root).resolve()
    if not skills_root.is_dir():
        logger.log("fatal", f"skills root does not exist: {skills_root}")
        write_state(
            state_path,
            {
                "status": "fatal",
                "message": f"skills root does not exist: {skills_root}",
                "updated_at": now_iso(),
            },
        )
        return 1

    consecutive_unexpected_failures = 0
    attempt = 0

    try:
        while not STOP_REQUESTED:
            attempt += 1
            logger.log("attempt", f"starting attempt={attempt}")
            dry_run = run_sync(
                skills_root=skills_root,
                bump=str(args.bump),
                changelog=str(args.changelog),
                tags=str(args.tags),
                dry_run=True,
            )
            pending = parse_pending_count(dry_run)
            logger.log("dry-run", f"returncode={dry_run.returncode} pending={pending}")
            logger.log("dry-run-output", dry_run.combined or "(empty)")

            write_state(
                state_path,
                {
                    "status": "checking",
                    "attempt": attempt,
                    "pending": pending,
                    "dry_run_returncode": dry_run.returncode,
                    "updated_at": now_iso(),
                },
            )

            if dry_run.returncode != 0:
                consecutive_unexpected_failures += 1
                logger.log("error", f"dry-run failed; consecutive_unexpected_failures={consecutive_unexpected_failures}")
                if args.once or consecutive_unexpected_failures >= int(args.max_unexpected_failures):
                    write_state(
                        state_path,
                        {
                            "status": "failed",
                            "attempt": attempt,
                            "pending": pending,
                            "message": dry_run.combined,
                            "updated_at": now_iso(),
                        },
                    )
                    return 1
                sleep_until = datetime.now() + timedelta(seconds=int(args.unexpected_retry_seconds))
                write_state(
                    state_path,
                    {
                        "status": "sleeping-after-error",
                        "attempt": attempt,
                        "pending": pending,
                        "next_run_at": sleep_until.isoformat(timespec="seconds"),
                        "message": dry_run.combined,
                        "updated_at": now_iso(),
                    },
                )
                sleep_with_heartbeat(int(args.unexpected_retry_seconds), logger, reason="unexpected failure")
                continue

            consecutive_unexpected_failures = 0
            if pending == 0:
                logger.log("done", "no remaining skills to sync")
                write_state(
                    state_path,
                    {
                        "status": "completed",
                        "attempt": attempt,
                        "pending": 0,
                        "updated_at": now_iso(),
                    },
                )
                return 0

            sync_result = run_sync(
                skills_root=skills_root,
                bump=str(args.bump),
                changelog=str(args.changelog),
                tags=str(args.tags),
                dry_run=False,
            )
            logger.log("sync", f"returncode={sync_result.returncode}")
            logger.log("sync-output", sync_result.combined or "(empty)")

            if sync_result.returncode == 0:
                write_state(
                    state_path,
                    {
                        "status": "sync-ok",
                        "attempt": attempt,
                        "pending_before": pending,
                        "updated_at": now_iso(),
                    },
                )
                if args.once:
                    return 0
                continue

            rate_limit_match = RATE_LIMIT_RE.search(sync_result.combined)
            if rate_limit_match:
                sleep_seconds = int(args.rate_limit_sleep_seconds)
                sleep_until = datetime.now() + timedelta(seconds=sleep_seconds)
                logger.log(
                    "rate-limit",
                    f"hit rate limit after pending={pending}; sleeping until {sleep_until.isoformat(timespec='seconds')}",
                )
                write_state(
                    state_path,
                    {
                        "status": "sleeping-after-rate-limit",
                        "attempt": attempt,
                        "pending_before": pending,
                        "next_run_at": sleep_until.isoformat(timespec="seconds"),
                        "message": sync_result.combined,
                        "updated_at": now_iso(),
                    },
                )
                if args.once:
                    return 2
                sleep_with_heartbeat(sleep_seconds, logger, reason="rate limit")
                continue

            consecutive_unexpected_failures += 1
            logger.log(
                "error",
                f"sync failed unexpectedly; consecutive_unexpected_failures={consecutive_unexpected_failures}",
            )
            if args.once or consecutive_unexpected_failures >= int(args.max_unexpected_failures):
                write_state(
                    state_path,
                    {
                        "status": "failed",
                        "attempt": attempt,
                        "pending_before": pending,
                        "message": sync_result.combined,
                        "updated_at": now_iso(),
                    },
                )
                return 1

            sleep_until = datetime.now() + timedelta(seconds=int(args.unexpected_retry_seconds))
            write_state(
                state_path,
                {
                    "status": "sleeping-after-error",
                    "attempt": attempt,
                    "pending_before": pending,
                    "next_run_at": sleep_until.isoformat(timespec="seconds"),
                    "message": sync_result.combined,
                    "updated_at": now_iso(),
                },
            )
            sleep_with_heartbeat(int(args.unexpected_retry_seconds), logger, reason="unexpected sync failure")
    finally:
        if pid_path.exists():
            try:
                pid_path.unlink()
            except OSError:
                pass
        logger.log("daemon", "stopped")

    write_state(
        state_path,
        {
            "status": "stopped",
            "attempt": attempt,
            "updated_at": now_iso(),
        },
    )
    return 0


def install_signal_handlers() -> None:
    signal.signal(signal.SIGTERM, _handle_stop_signal)
    signal.signal(signal.SIGINT, _handle_stop_signal)


def _handle_stop_signal(signum: int, _frame: Any) -> None:
    del signum
    global STOP_REQUESTED
    STOP_REQUESTED = True


def run_sync(*, skills_root: Path, bump: str, changelog: str, tags: str, dry_run: bool) -> CommandResult:
    argv = [
        "clawhub",
        "--no-input",
        "sync",
        "--all",
        "--root",
        str(skills_root),
        "--bump",
        bump,
        "--changelog",
        changelog,
        "--tags",
        tags,
    ]
    if dry_run:
        argv.insert(3, "--dry-run")

    env = dict(os.environ)
    env.setdefault("NO_COLOR", "1")
    env.setdefault("FORCE_COLOR", "0")
    proc = subprocess.run(
        argv,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    return CommandResult(
        argv=argv,
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )


def parse_pending_count(result: CommandResult) -> int:
    text = result.combined
    match = DRY_RUN_COUNT_RE.search(text)
    if match:
        return int(match.group(1))
    if "Nothing to sync" in text:
        return 0
    if "To sync" not in text and result.returncode == 0:
        return 0
    return -1


def sleep_with_heartbeat(seconds: int, logger: "Logger", *, reason: str) -> None:
    remaining = max(0, int(seconds))
    while remaining > 0 and not STOP_REQUESTED:
        step = min(60, remaining)
        if remaining == seconds or remaining <= 60 or remaining % 600 == 0:
            logger.log("sleep", f"{reason}; remaining={remaining}s")
        time.sleep(step)
        remaining -= step


def write_state(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


class Logger:
    def __init__(self, path: Path) -> None:
        self.path = path

    def log(self, kind: str, message: str) -> None:
        line = f"[{now_iso()}] {kind}: {message}\n"
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(line)
        print(line, end="")
        sys.stdout.flush()


if __name__ == "__main__":
    raise SystemExit(main())
