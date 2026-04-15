#!/usr/bin/env python3
"""Tests for personal_kb: ingest and query functionality."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
INGEST_SCRIPT = PROJECT_ROOT / "scripts" / "ingest.py"

passed = 0
failed = 0


def run(cmd, **kwargs):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=120, **kwargs)


def assert_true(condition, name):
    global passed, failed
    if condition:
        print(f"  ✅ {name}")
        passed += 1
    else:
        print(f"  ❌ {name}")
        failed += 1


def test_ingest_single_file():
    """Test 1: Ingest a single text file."""
    print("\n🧪 Test 1: Ingest single file")
    with tempfile.TemporaryDirectory() as tmpdir:
        inbox = Path(tmpdir) / "inbox"
        output = Path(tmpdir) / "workmemory"
        inbox.mkdir()
        shutil.copy(FIXTURES / "sample.txt", inbox / "sample.txt")

        result = run([sys.executable, str(INGEST_SCRIPT), "--inbox", str(inbox), "--output", str(output)])
        assert_true(result.returncode == 0, "ingest exits 0")

        out_file = output / "sample.txt.md"
        assert_true(out_file.exists(), "output file exists")

        content = out_file.read_text()
        assert_true("source_path:" in content, "frontmatter has source_path")
        assert_true("ingested_at:" in content, "frontmatter has ingested_at")
        assert_true("knowledge base" in content, "content is preserved")


def test_ingest_directory():
    """Test 2: Ingest a directory with multiple files including subdirectory."""
    print("\n🧪 Test 2: Ingest directory with subdirectory")
    with tempfile.TemporaryDirectory() as tmpdir:
        inbox = Path(tmpdir) / "inbox"
        output = Path(tmpdir) / "workmemory"
        inbox.mkdir()
        (inbox / "subdir").mkdir()

        shutil.copy(FIXTURES / "sample.txt", inbox / "sample.txt")
        shutil.copy(FIXTURES / "sample.html", inbox / "sample.html")
        shutil.copy(FIXTURES / "sample.csv", inbox / "sample.csv")
        shutil.copy(FIXTURES / "subdir" / "nested.txt", inbox / "subdir" / "nested.txt")

        result = run([sys.executable, str(INGEST_SCRIPT), "--inbox", str(inbox), "--output", str(output)])
        assert_true(result.returncode == 0, "ingest exits 0")
        assert_true((output / "sample.txt.md").exists(), "sample.txt.md exists")
        assert_true((output / "sample.html.md").exists(), "sample.html.md exists")
        assert_true((output / "sample.csv.md").exists(), "sample.csv.md exists")
        assert_true((output / "subdir" / "nested.txt.md").exists(), "nested file preserves path structure")

        # Test idempotency: run again without --force
        result2 = run([sys.executable, str(INGEST_SCRIPT), "--inbox", str(inbox), "--output", str(output)])
        assert_true("skipped" in result2.stdout.lower(), "second run skips existing files")


def test_query_with_results():
    """Test 3: Query workmemory with a keyword that exists."""
    print("\n🧪 Test 3: Query with results")
    with tempfile.TemporaryDirectory() as tmpdir:
        inbox = Path(tmpdir) / "inbox"
        output = Path(tmpdir) / "workmemory"
        inbox.mkdir()
        shutil.copy(FIXTURES / "sample.txt", inbox / "sample.txt")

        run([sys.executable, str(INGEST_SCRIPT), "--inbox", str(inbox), "--output", str(output)])

        # Use rg if available, else grep
        if shutil.which("rg"):
            result = run(["rg", "--type", "md", "--smart-case", "knowledge base", str(output)])
        else:
            result = run(["grep", "-rn", "--include=*.md", "knowledge base", str(output)])

        assert_true(result.returncode == 0, "rg/grep finds match")
        assert_true("knowledge base" in result.stdout.lower(), "output contains search term")


def test_query_no_results():
    """Test 4: Query workmemory with a keyword that does not exist."""
    print("\n🧪 Test 4: Query with no results")
    with tempfile.TemporaryDirectory() as tmpdir:
        inbox = Path(tmpdir) / "inbox"
        output = Path(tmpdir) / "workmemory"
        inbox.mkdir()
        output.mkdir()
        shutil.copy(FIXTURES / "sample.txt", inbox / "sample.txt")

        run([sys.executable, str(INGEST_SCRIPT), "--inbox", str(inbox), "--output", str(output)])

        if shutil.which("rg"):
            result = run(["rg", "--type", "md", "xyznonexistentkeyword99", str(output)])
        else:
            result = run(["grep", "-rn", "--include=*.md", "xyznonexistentkeyword99", str(output)])

        assert_true(result.returncode == 1, "rg/grep returns exit code 1 for no match")
        assert_true(result.stdout.strip() == "", "output is empty for no match")


if __name__ == "__main__":
    print("=" * 60)
    print("Personal KB — Test Suite")
    print("=" * 60)

    test_ingest_single_file()
    test_ingest_directory()
    test_query_with_results()
    test_query_no_results()

    print(f"\n{'=' * 60}")
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    sys.exit(1 if failed > 0 else 0)
