# Skill: Ingest Files

Convert files from `inbox/` to Markdown and store in `workmemory/`.

## When to Use

- User runs `/ingest`
- User asks to "add files to the knowledge base"
- User drops files into `inbox/` and wants them processed

## How It Works

1. **Preflight check**: Verify `markitdown` is installed via `bash scripts/preflight.sh`
2. **Scan**: Recursively find all supported files in `inbox/`
3. **Convert**: For each file, run:
   ```bash
   markitdown "<input_file>"
   ```
4. **Write output**: Save to `workmemory/` preserving relative path structure
5. **Add frontmatter**: Prepend YAML frontmatter to each output file:
   ```yaml
   ---
   source_path: inbox/path/to/file.pdf
   ingested_at: 2026-04-15T08:00:00+08:00
   ---
   ```
6. **Report**: Summarize results (success/fail/skip counts)

## Error Handling

- Single file failure: log error to stderr, continue with next file
- `markitdown` not installed: abort with installation instructions
- Empty `inbox/`: inform user, no error

## Idempotency

- Skip files whose output already exists (by filename match)
- Use `FORCE=1` or `--force` to re-process all files

## Implementation

The core logic is in `scripts/ingest.py`. The agent should invoke it via:

```bash
python scripts/ingest.py [--force] [--inbox PATH] [--output PATH]
```
