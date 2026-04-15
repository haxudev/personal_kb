# AGENTS.md

This repository is optimized for GitHub Copilot CLI.

## Primary customization locations

- Repository-wide instructions: `.github/copilot-instructions.md`
- Path-specific instructions: `.github/instructions/**/*.instructions.md`
- Repository custom agent: `.github/agents/personal-kb.agent.md`
- Repository skills: `.github/skills/ingest/SKILL.md`, `.github/skills/query/SKILL.md`

## Workflow preference

1. Use `/ingest` to convert source files from `inbox/` into markdown in `workmemory/`.
2. Use `/query` to search `workmemory/`.
3. Use Microsoft Learn MCP only as a secondary source.

## Environment

- Use `.venv` for Python execution.
- Prefer project-local scripts under `scripts/`.


## Command execution preference

- Detect the user execution environment before suggesting commands.
- If the user is on Windows, prefer Windows CMD / PowerShell command syntax first for both `/ingest` and `/query`.
- Only default to POSIX shell syntax for macOS, Linux, or WSL contexts.
