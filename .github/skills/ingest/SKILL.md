---
name: ingest
description: Convert files from inbox/ to markdown in workmemory/. Use when asked to ingest files, refresh the knowledge base, or process new local source documents.
allowed-tools: execute
---

# Skill: ingest

Use this skill when the user wants to add or refresh local knowledge.

## Process

1. Run `bash scripts/preflight.sh` to verify required dependencies.
2. Run `python scripts/ingest.py`.
3. If the user requests a full refresh, run `python scripts/ingest.py --force`.
4. Report how many files were converted, skipped, or failed.

## Expected behavior

- Scan `inbox/` recursively.
- Convert supported files via `markitdown`.
- Preserve relative paths under `workmemory/`.
- Add YAML frontmatter containing `source_path` and `ingested_at`.
- Continue past single-file failures and summarize them.
