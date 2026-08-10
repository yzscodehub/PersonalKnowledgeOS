#!/usr/bin/env python3
"""Synchronize created/updated fields for Markdown notes.

Usage:
    python scripts/sync_note_dates.py --staged
    python scripts/sync_note_dates.py path/to/note.md another.md

The script preserves an existing created date, fills it only when missing or blank,
and sets updated to today's local date. It does not stage files automatically.
"""

from __future__ import annotations

import argparse
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def staged_markdown() -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    paths: list[Path] = []
    for line in result.stdout.splitlines():
        path = ROOT / line
        if path.suffix.lower() == ".md" and path.exists():
            paths.append(path)
    return paths


def frontmatter_bounds(lines: list[str]) -> tuple[int, int] | None:
    if not lines or lines[0].strip() != "---":
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return 0, index
    return None


def set_scalar(lines: list[str], closing: int, key: str, value: str, *, preserve: bool) -> int:
    for index in range(1, closing):
        if lines[index].startswith(f"{key}:"):
            current = lines[index].split(":", 1)[1].strip()
            if preserve and current:
                return closing
            lines[index] = f"{key}: {value}"
            return closing
    lines.insert(closing, f"{key}: {value}")
    return closing + 1


def update(path: Path, today: str) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    bounds = frontmatter_bounds(lines)
    if bounds is None:
        return False
    _, closing = bounds
    closing = set_scalar(lines, closing, "created", today, preserve=True)
    set_scalar(lines, closing, "updated", today, preserve=False)
    updated = "\n".join(lines) + "\n"
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    print(path.relative_to(ROOT).as_posix())
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--staged", action="store_true")
    args = parser.parse_args()

    if args.staged and args.paths:
        parser.error("--staged cannot be combined with explicit paths")
    if not args.staged and not args.paths:
        parser.error("provide --staged or one or more Markdown paths")

    paths = staged_markdown() if args.staged else [ROOT / item for item in args.paths]
    today = date.today().isoformat()
    changed = sum(update(path, today) for path in paths if path.suffix.lower() == ".md")
    print(f"Updated {changed} note(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
