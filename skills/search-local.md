# Skill: Search Local Knowledge Base

Perform full-text search across Markdown files in `workmemory/`.

## When to Use

- User runs `/query <keywords>`
- User asks a question that might be answered by local files
- User wants to find specific content in their knowledge base

## How It Works

1. **Check tool**: Verify `rg` is available; fall back to `grep -rn` if not
2. **Execute search**:
   ```bash
   rg --type md --context 3 --smart-case "<query>" workmemory/
   ```
3. **Format results**: Present as structured output with file path, line number, and context
4. **Handle no results**: Output "No results found for: <query>" with suggestions

## Fallback

If `rg` is not installed:

```bash
grep -rn --include="*.md" "<query>" workmemory/
```

This is slower but functionally equivalent.

## Tips for the Agent

- If the query is broad and returns too many results, suggest the user narrow their search
- If no results, check whether `workmemory/` is empty and suggest `/ingest`
- Use the frontmatter `source_path` to tell the user which original file the match came from
