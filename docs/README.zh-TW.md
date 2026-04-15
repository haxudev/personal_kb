🌐 [English](../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

# Personal KB

一個本機優先、代理驅動的知識庫，專為 [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli) 設計。將檔案放入 `inbox/`，轉換為 Markdown，然後用自然語言搜尋——一切都在本機完成。

## 功能特色

- **`/ingest`** — 使用 [markitdown](https://github.com/microsoft/markitdown) 將檔案（PDF、DOCX、HTML、CSV 等）轉換為可搜尋的 Markdown
- **`/query`** — 使用 [ripgrep](https://github.com/BurntSushi/ripgrep) 對知識庫進行全文檢索
- **代理優先設計** — 以 Copilot CLI agent 形式建構，包含 skills、tools 和斜線命令
- **MCP 整合** — 透過外部知識來源（如 Microsoft Learn）擴展能力
- **100% 本機運行** — 無需雲端服務、無需向量資料庫、無需 Web UI

## 快速開始

### 前置需求

- Python 3.10+
- [markitdown](https://github.com/microsoft/markitdown)：`pip install "markitdown[all]"`
- [ripgrep](https://github.com/BurntSushi/ripgrep)：`brew install ripgrep` / `apt install ripgrep`

### 安裝

```bash
git clone https://github.com/haxudev/personal_kb.git
cd personal_kb
python -m venv .venv
source .venv/bin/activate
pip install "markitdown[all]"
```

### 使用方式

1. 將檔案放入 `inbox/`：
   ```bash
   cp ~/Documents/report.pdf inbox/
   ```

2. 匯入檔案：
   ```bash
   python scripts/ingest.py
   # 或在 Copilot CLI 中：/ingest
   ```

3. 搜尋知識庫：
   ```bash
   rg --type md --smart-case "搜尋關鍵字" workmemory/
   # 或在 Copilot CLI 中：/query 搜尋關鍵字
   ```

## 專案結構

```
personal_kb/
├── .github/
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
## MCP 設定

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 允許代理存取外部知識來源。本專案包含 Microsoft Learn 的設定。

### 在 Copilot CLI 中設定

1. 將 `tools/mcp.example.json` 的內容複製或合併到 `~/.copilot/mcp-config.json`
2. Microsoft Learn MCP 伺服器用於存取微軟文件
3. 使用者級 MCP / agents / skills 預設都位於 `~/.copilot/`

```json
{
  "mcpServers": {
    "microsoft-learn": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-remote", "https://learn.microsoft.com/api/mcp"],
      "description": "透過 MCP 協定搜尋 Microsoft Learn 文件"
    }
  }
}
```

## 執行測試

```bash
python scripts/preflight.py
python tests/test_all.py
```

測試涵蓋：
1. 匯入單一檔案
2. 匯入包含子目錄的目錄
3. 有匹配結果的查詢
4. 無匹配結果的查詢

## 參與貢獻

1. Fork 本專案
2. 建立功能分支
3. 提交變更
4. 執行測試：`python tests/test_all.py`
5. 提交 Pull Request

## 授權條款

[MIT](../LICENSE)


## Command Reference Matrix

| Scenario | Windows CMD / PowerShell | macOS / Linux / WSL |
|---|---|---|
| Preflight | `python scripts\preflight.py` | `python scripts/preflight.py` |
| Ingest | `python scripts\ingest.py` | `python scripts/ingest.py` |
| Ingest (force) | `python scripts\ingest.py --force` | `python scripts/ingest.py --force` |
| Query | `rg --type md --smart-case "your query" workmemory` | `rg --type md --smart-case "your query" workmemory/` |
| Query fallback | `findstr /S /N /I "your query" workmemory\*.md` | `grep -rn --include="*.md" "your query" workmemory/` |
