🌐 [English](README.md) | [简体中文](docs/README.zh-CN.md) | [繁體中文](docs/README.zh-TW.md) | [日本語](docs/README.ja.md) | [한국어](docs/README.ko.md)

# Personal KB

A local-first, agent-driven knowledge base for [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli). Drop files into `inbox/`, ingest them as Markdown, and search with natural language — all on your machine.

## Features

- **`/ingest`** — Convert files (PDF, DOCX, HTML, CSV, etc.) to searchable Markdown using [markitdown](https://github.com/microsoft/markitdown)
- **`/query`** — Full-text search across your knowledge base using [ripgrep](https://github.com/BurntSushi/ripgrep)
- **Agent-first design** — Built as a Copilot CLI agent with skills, tools, and slash commands
- **MCP integration** — Extend with external knowledge sources like Microsoft Learn
- **100% local** — No cloud services, no vector databases, no web UI

## Quick Start

### Prerequisites

- Python 3.10+
- [markitdown](https://github.com/microsoft/markitdown): `pip install "markitdown[all]"`
- [ripgrep](https://github.com/BurntSushi/ripgrep): `brew install ripgrep` / `apt install ripgrep`

### Setup

```bash
git clone https://github.com/haxudev/personal_kb.git
cd personal_kb
python -m venv .venv
source .venv/bin/activate
pip install "markitdown[all]"
```

### Usage

1. Drop files into `inbox/`:
   ```bash
   cp ~/Documents/report.pdf inbox/
   ```

2. Ingest files:
   ```bash
   python scripts/ingest.py
   # Or in Copilot CLI: /ingest
   ```

3. Search your knowledge base:
   ```bash
   rg --type md --smart-case "your query" workmemory/
   # Or in Copilot CLI: /query your query
   ```

## Project Structure

```
personal_kb/
├── agent.md                    # Agent definition
├── commands/
│   ├── ingest.md               # /ingest command spec
│   └── query.md                # /query command spec
├── skills/
│   ├── ingest-files.md         # Ingestion skill
│   └── search-local.md         # Search skill
├── tools/
│   └── mcp.json                # MCP server configuration
├── scripts/
│   ├── ingest.py               # Core ingest implementation
│   └── preflight.sh            # Environment check
├── inbox/                      # Drop files here
├── workmemory/                 # Ingested Markdown output
├── tests/                      # Test suite
├── docs/                       # Multilingual READMEs
├── .github/
│   ├── copilot-instructions.md
│   └── workflows/ci.yml
├── LICENSE                     # MIT
└── .gitignore
```

## MCP Configuration

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) lets your agent access external knowledge sources. This project includes a configuration for Microsoft Learn.

### Setup in Copilot CLI

1. Copy or reference `tools/mcp.json` in your Copilot CLI MCP configuration
2. The Microsoft Learn MCP server provides access to Microsoft's documentation

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

Edit `tools/mcp.json` to add your own MCP servers for additional knowledge sources.

## Running Tests

```bash
# Ensure dependencies are installed
bash scripts/preflight.sh

# Run all tests
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
