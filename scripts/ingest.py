#!/usr/bin/env python3
"""Ingest files from inbox/ into workmemory/ as Markdown with frontmatter."""

import argparse
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".html", ".xml",
    ".json", ".csv", ".epub", ".ipynb", ".txt",
}


def is_supported(path: Path) -> bool:
    return path.suffix.lower() in SUPPORTED_EXTENSIONS


def make_frontmatter(source_path: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    return f"---\nsource_path: {source_path}\ningested_at: {now}\n---\n\n"


def convert_file(src: Path, dst: Path, relative_source: str) -> bool:
    """Convert a single file using markitdown. Returns True on success."""
    try:
        result = subprocess.run(
            ["markitdown", str(src)],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            print(f"FAIL: {src} — {result.stderr.strip()}", file=sys.stderr)
            return False

        dst.parent.mkdir(parents=True, exist_ok=True)
        content = make_frontmatter(relative_source) + result.stdout
        dst.write_text(content, encoding="utf-8")
        return True
    except subprocess.TimeoutExpired:
        print(f"FAIL: {src} — timeout", file=sys.stderr)
        return False
    except Exception as e:
        print(f"FAIL: {src} — {e}", file=sys.stderr)
        return False


def ingest(inbox: Path, output: Path, force: bool = False) -> dict:
    stats = {"success": 0, "failed": 0, "skipped": 0}

    if not inbox.exists():
        print(f"inbox directory not found: {inbox}", file=sys.stderr)
        return stats

    files = [f for f in inbox.rglob("*") if f.is_file() and is_supported(f)]

    if not files:
        print("inbox/ is empty or contains no supported files. Add files and try again.")
        return stats

    for src in sorted(files):
        relative = src.relative_to(inbox)
        dst = output / (str(relative) + ".md")
        relative_source = str(Path("inbox") / relative)

        if dst.exists() and not force:
            stats["skipped"] += 1
            continue

        if convert_file(src, dst, relative_source):
            stats["success"] += 1
        else:
            stats["failed"] += 1

    return stats


def main():
    parser = argparse.ArgumentParser(description="Ingest files into workmemory")
    parser.add_argument("--inbox", default="inbox", help="Source directory (default: inbox)")
    parser.add_argument("--output", default="workmemory", help="Output directory (default: workmemory)")
    parser.add_argument("--force", action="store_true", help="Re-process existing files")
    args = parser.parse_args()

    inbox = Path(args.inbox)
    output = Path(args.output)

    stats = ingest(inbox, output, force=args.force)
    total = stats["success"] + stats["failed"] + stats["skipped"]
    print(f"Ingest complete: {stats['success']} ok, {stats['failed']} failed, {stats['skipped']} skipped ({total} total)")

    if stats["failed"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
