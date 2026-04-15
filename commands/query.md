---
description: "Search workmemory/ for matching Markdown content using ripgrep"
---

## /query

Search your local knowledge base for relevant content.

### Steps

1. Run `bash scripts/preflight.sh` to check if `rg` is available
2. Execute `rg --type md --context 3 --smart-case "<query>" workmemory/`
3. Format results as: file path, line number, and context snippet
4. If no results found, display: "No results found for: <query>" and suggest:
   - Try different keywords
   - Check if `workmemory/` has content (run `/ingest` first if empty)

### Behavior

- Supports regex patterns (ripgrep native)
- Smart-case by default (lowercase = case-insensitive; contains uppercase = case-sensitive)
- Context of 3 lines above and below each match
- Falls back to `grep -rn` if `rg` is not available

### Usage

```
/query knowledge base
/query "Azure Functions"
/query --regex "deploy(ment|ed)"
```
