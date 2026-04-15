🌐 [English](../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

# Personal KB

ローカルファースト、エージェント駆動のナレッジベース。[GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli) 向けに設計されています。ファイルを `inbox/` に入れて Markdown に変換し、自然言語で検索できます。すべてローカルで完結します。

## Copilot CLI の公式ディレクトリ構成

リポジトリレベルの custom agent は `.github/agents/`、リポジトリレベルの skills は `.github/skills/`、ユーザーレベルの Copilot 資産（MCP 設定や個人 agent など）は `~/.copilot/` に配置します。本プロジェクトもこの公式構成に合わせて整理しました。

## 機能

- **`/ingest`** — [markitdown](https://github.com/microsoft/markitdown) を使って各種ファイル（PDF、DOCX、HTML、CSV など）を検索可能な Markdown に変換
- **`/query`** — [ripgrep](https://github.com/BurntSushi/ripgrep) を使ってナレッジベースを全文検索
- **エージェントファースト設計** — Copilot CLI エージェントとして構築。skills、tools、スラッシュコマンドを含む
- **MCP 統合** — Microsoft Learn などの外部知識ソースで拡張可能
- **100% ローカル** — クラウドサービス不要、ベクトルデータベース不要、Web UI 不要

## クイックスタート

### 前提条件

- Python 3.10+
- [markitdown](https://github.com/microsoft/markitdown)：`pip install "markitdown[all]"`
- [ripgrep](https://github.com/BurntSushi/ripgrep)：`brew install ripgrep` / `apt install ripgrep`

### セットアップ

```bash
git clone https://github.com/haxudev/personal_kb.git
cd personal_kb
python -m venv .venv
source .venv/bin/activate
pip install "markitdown[all]"
```

### 使い方

1. ファイルを `inbox/` に配置：
   ```bash
   cp ~/Documents/report.pdf inbox/
   ```

2. ファイルを取り込み：
   ```bash
   python scripts/ingest.py
   # または Copilot CLI で：/ingest
   ```

3. ナレッジベースを検索：
   ```bash
   rg --type md --smart-case "検索キーワード" workmemory/
   # または Copilot CLI で：/query 検索キーワード
   ```

## プロジェクト構成

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

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) により、エージェントが外部知識ソースにアクセスできます。本プロジェクトには Microsoft Learn の設定が含まれています。

### Copilot CLI での設定

1. `tools/mcp.example.json` の内容を `~/.copilot/mcp-config.json` にコピーまたはマージします
2. Microsoft Learn MCP サーバーを使って Microsoft ドキュメントを参照します
3. ユーザーレベルの MCP / agents / skills は `~/.copilot/` 配下に保存されます

```json
{
  "mcpServers": {
    "microsoft-learn": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-remote", "https://learn.microsoft.com/api/mcp"],
      "description": "MCP プロトコル経由で Microsoft Learn ドキュメントを検索"
    }
  }
}
```

## テストの実行

```bash
python scripts/preflight.py
python tests/test_all.py
```

テストカバレッジ：
1. 単一ファイルの取り込み
2. サブディレクトリを含むディレクトリの取り込み
3. マッチ結果ありのクエリ
4. マッチ結果なしのクエリ

## コントリビューション

1. リポジトリをフォーク
2. 機能ブランチを作成
3. 変更をコミット
4. テスト実行：`python tests/test_all.py`
5. Pull Request を提出

## ライセンス

[MIT](../LICENSE)


## Command Reference Matrix

| Scenario | Windows CMD / PowerShell | macOS / Linux / WSL |
|---|---|---|
| Preflight | `python scripts\preflight.py` | `python scripts/preflight.py` |
| Ingest | `python scripts\ingest.py` | `python scripts/ingest.py` |
| Ingest (force) | `python scripts\ingest.py --force` | `python scripts/ingest.py --force` |
| Query | `rg --type md --smart-case "your query" workmemory` | `rg --type md --smart-case "your query" workmemory/` |
| Query fallback | `findstr /S /N /I "your query" workmemory\*.md` | `grep -rn --include="*.md" "your query" workmemory/` |
