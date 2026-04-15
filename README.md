🌐 [English](README.md) | [简体中文](docs/README.zh-CN.md) | [繁體中文](docs/README.zh-TW.md) | [日本語](docs/README.ja.md) | [한국어](docs/README.ko.md)

# Personal KB

A local-first, agent-driven knowledge base for [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli). Drop files into `inbox/`, ingest them as Markdown, and search with natural language — all on your machine.

> **Copilot CLI alignment:** repository-level custom agents live in `.github/agents/`, repository skills live in `.github/skills/`, and user-level assets live under `~/.copilot/`. This project now follows those official conventions.

## Features

- **`/ingest`** — Convert files (PDF, DOCX, HTML, CSV, etc.) to searchable Markdown using [markitdown](https://github.com/microsoft/markitdown)
- **`/query`** — Full-text search across your knowledge base using [ripgrep](https://github.com/BurntSushi/ripgrep)
- **Agent-first design** — Built around official Copilot CLI customization points: repository agents, skills, and instructions
- **MCP integration** — Extend with external knowledge sources like Microsoft Learn
- **100% local** — No cloud services, no vector databases, no web UI

## Quick Start

### Prerequisites

- Python 3.10+
- [markitdown](https://github.com/microsoft/markitdown): `pip install "markitdown[all]"`
- [ripgrep](https://github.com/BurntSushi/ripgrep): `brew install ripgrep` / `apt install ripgrep`

### Setup

**Windows CMD / PowerShell (preferred)**
```bat
git clone https://github.com/haxudev/personal_kb.git
cd personal_kb
python -m venv .venv
.venv\Scripts\activate
pip install "markitdown[all]"
```

**macOS / Linux / WSL**
```bash
git clone https://github.com/haxudev/personal_kb.git
cd personal_kb
python -m venv .venv
source .venv/bin/activate
pip install "markitdown[all]"
```

### Usage

1. Drop files into `inbox/`.

   **Windows CMD / PowerShell**
   ```bat
   copy C:\Users\you\Documents\report.pdf inbox\
   ```

   **macOS / Linux / WSL**
   ```bash
   cp ~/Documents/report.pdf inbox/
   ```

2. Ingest files (detect the current environment and use the matching command style):

   **Windows CMD / PowerShell preferred**
   ```bat
   python scripts\preflight.py
   python scripts\ingest.py
   ```

   **macOS / Linux / WSL**
   ```bash
   python scripts/preflight.py
   python scripts/ingest.py
   ```

   Or in Copilot CLI: `/ingest`

3. Search your knowledge base:
   ```bash
   rg --type md --smart-case "your query" workmemory/
   # Or in Copilot CLI: /query your query
   ```

## Official Copilot CLI Layout

```
personal_kb/
├── AGENTS.md
├── .github/
│   ├── agents/
│   │   └── personal-kb.agent.md
│   ├── skills/
│   │   ├── ingest/
│   │   │   └── SKILL.md
│   │   └── query/
│   │       └── SKILL.md
│   ├── instructions/
│   │   └── python.instructions.md
│   ├── copilot-instructions.md
│   └── workflows/ci.yml
├── tools/
│   └── mcp.example.json
├── scripts/
│   ├── ingest.py
│   └── preflight.py
├── inbox/
├── workmemory/
├── tests/
├── docs/
├── LICENSE
└── .gitignore
```
## MCP Configuration

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) lets your agent access external knowledge sources. This project includes a configuration for Microsoft Learn.

### Setup in Copilot CLI

1. Copy or merge `tools/mcp.example.json` into `~/.copilot/mcp-config.json`
2. The Microsoft Learn MCP server provides access to Microsoft's documentation
3. User-level Copilot CLI assets such as MCP config and personal agents live under `~/.copilot/`

```json
{
  "mcpServers": {
    "microsoft-learn": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-remote", "https://learn.microsoft.com/api/mcp"],
      "description": "Microsoft Learn documentation search via MCP"
    }
  }
}
```

### Adding Custom MCP Servers

Edit `tools/mcp.example.json`, then merge it into `~/.copilot/mcp-config.json`, to add your own MCP servers for additional knowledge sources.

## Running Tests

```text
# Windows CMD / PowerShell
python scripts\preflight.py
python tests\test_all.py

# macOS / Linux / WSL
python scripts/preflight.py
python tests/test_all.py
```

Tests cover:
1. Ingest single file
2. Ingest directory with subdirectories
3. Query with matching results
4. Query with no results

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python tests/test_all.py`
5. Submit a pull request

## License

[MIT](LICENSE)
