---
name: query
description: Search local markdown content in workmemory/ with ripgrep. Use when asked to search the knowledge base, find matching documents, or answer from local KB content.
allowed-tools: execute
---

# Skill: query

Use this skill when the user wants to search local knowledge.

## Process

1. Run `bash scripts/preflight.sh` to verify `rg` is available, or note fallback to `grep`.
2. Search `workmemory/` with:
   - `rg --type md --context 3 --smart-case "<query>" workmemory/`
3. Format output with file path, matching lines, and nearby context.
4. If no results are found, say `No results found for: <query>` and suggest ingesting more content if needed.

## Expected behavior

- Prefer `rg`.
- Fall back to `grep -rn --include="*.md"` when necessary.
- Keep output concise but traceable.
