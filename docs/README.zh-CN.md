🌐 [English](../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

# Personal KB

一个本地优先、代理驱动的知识库，专为 [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli) 设计。将文件放入 `inbox/`，转换为 Markdown，然后用自然语言搜索——一切都在本地完成。

## Copilot CLI 官方目录约定

仓库级自定义 agent 放在 `.github/agents/`，仓库级 skills 放在 `.github/skills/`，用户级 Copilot 资产（如 MCP 配置、个人 agents）放在 `~/.copilot/`。本项目现已按该官方约定整理。

## 功能特性

- **`/ingest`** — 使用 [markitdown](https://github.com/microsoft/markitdown) 将文件（PDF、DOCX、HTML、CSV 等）转换为可搜索的 Markdown
- **`/query`** — 使用 [ripgrep](https://github.com/BurntSushi/ripgrep) 对知识库进行全文检索
- **代理优先设计** — 基于 Copilot CLI 官方自定义能力构建：repository agent、skills 与 instructions
- **MCP 集成** — 通过外部知识源（如 Microsoft Learn）扩展能力
- **100% 本地运行** — 无需云服务、无需向量数据库、无需 Web UI

## 快速开始

### 前置依赖

- Python 3.10+
- [markitdown](https://github.com/microsoft/markitdown)：`pip install "markitdown[all]"`
- [ripgrep](https://github.com/BurntSushi/ripgrep)：`brew install ripgrep` / `apt install ripgrep`

### 安装

```bash
git clone https://github.com/haxudev/personal_kb.git
cd personal_kb
python -m venv .venv
source .venv/bin/activate
pip install "markitdown[all]"
```

### 使用方法

1. 将文件放入 `inbox/`：
   ```bash
   cp ~/Documents/report.pdf inbox/
   ```

2. 摄入文件：
   ```bash
   python scripts/ingest.py
   # 或在 Copilot CLI 中：/ingest
   ```

3. 搜索知识库：
   ```bash
   rg --type md --smart-case "搜索关键词" workmemory/
   # 或在 Copilot CLI 中：/query 搜索关键词
   ```

## 项目结构

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
│   └── preflight.sh
├── inbox/
├── workmemory/
├── tests/
├── docs/
├── LICENSE
└── .gitignore
```
## MCP 配置

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 允许你的代理访问外部知识源。本项目包含 Microsoft Learn 的配置。

### 在 Copilot CLI 中配置

1. 将 `tools/mcp.example.json` 的内容复制或合并到 `~/.copilot/mcp-config.json`
2. Microsoft Learn MCP 服务器用于访问微软文档
3. 用户级 MCP / agents / skills 默认都位于 `~/.copilot/` 下

```json
{
  "mcpServers": {
    "microsoft-learn": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-remote", "https://learn.microsoft.com/api/mcp"],
      "description": "通过 MCP 协议搜索 Microsoft Learn 文档"
    }
  }
}
```

## 运行测试

```bash
bash scripts/preflight.sh
python tests/test_all.py
```

测试覆盖：
1. 摄入单个文件
2. 摄入包含子目录的目录
3. 有匹配结果的查询
4. 无匹配结果的查询

## 参与贡献

1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 运行测试：`python tests/test_all.py`
5. 提交 Pull Request

## 许可证

[MIT](../LICENSE)
