---
name: ingest
description: Convert files from inbox/ to markdown in workmemory/. Use when asked to ingest files, refresh the knowledge base, or process new local source documents.
allowed-tools: execute
---

# Skill: ingest

Use this skill when the user wants to add or refresh local knowledge.

## Process

1. Detect the execution environment first:
   - Windows CMD / PowerShell: prefer Windows-style commands
   - macOS / Linux / WSL: use POSIX commands
2. Run `python scripts/preflight.py` to verify required dependencies.
3. Run the ingest script using the environment-appropriate Python launcher.
4. If the user requests a full refresh, append `--force`.
5. Report how many files were converted, skipped, or failed.

## Environment-specific command preference

### Windows CMD (preferred on Windows)
```bat
python scripts\preflight.py
python scripts\ingest.py
python scripts\ingest.py --force
```

### Windows PowerShell
```powershell
python .\scripts\preflight.py
python .\scripts\ingest.py
python .\scripts\ingest.py --force
```

### macOS / Linux / WSL
```bash
python scripts/preflight.py
python scripts/ingest.py
python scripts/ingest.py --force
```

## Expected behavior

- Scan `inbox/` recursively.
- Convert supported files via `markitdown`.
- Preserve relative paths under `workmemory/`.
- Add YAML frontmatter containing `source_path` and `ingested_at`.
- Continue past single-file failures and summarize them.
