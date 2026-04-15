🌐 [English](../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

# Personal KB

ローカルファースト、エージェント駆動のナレッジベース。[GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli) 向けに設計されています。ファイルを `inbox/` に入れて Markdown に変換し、自然言語で検索できます。すべてローカルで完結します。

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
├── agent.md                    # エージェント定義
├── commands/                   # スラッシュコマンド定義
│   ├── ingest.md
│   └── query.md
├── skills/                     # スキル定義
│   ├── ingest-files.md
│   └── search-local.md
├── tools/
│   └── mcp.json                # MCP サーバー設定
├── scripts/
│   ├── ingest.py               # 取り込みのコア実装
│   └── preflight.sh            # 環境チェック
├── inbox/                      # ファイルをここに配置
├── workmemory/                 # 変換された Markdown 出力
├── tests/                      # テストスイート
├── docs/                       # 多言語 README
├── .github/
│   ├── copilot-instructions.md
│   └── workflows/ci.yml
├── LICENSE                     # MIT
└── .gitignore
```

## MCP 設定

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) により、エージェントが外部知識ソースにアクセスできます。本プロジェクトには Microsoft Learn の設定が含まれています。

### Copilot CLI での設定

1. `tools/mcp.json` を Copilot CLI の MCP 設定にコピーまたは参照
2. Microsoft Learn MCP サーバーが Microsoft ドキュメントへのアクセスを提供

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
bash scripts/preflight.sh
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
