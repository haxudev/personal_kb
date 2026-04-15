🌐 [English](../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

# Personal KB

로컬 우선, 에이전트 기반 지식 베이스. [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli)용으로 설계되었습니다. 파일을 `inbox/`에 넣고 Markdown으로 변환한 뒤 자연어로 검색하세요. 모든 것이 로컬에서 실행됩니다.

## Copilot CLI 공식 디렉터리 규칙

저장소 수준 custom agent 는 `.github/agents/`, 저장소 수준 skills 는 `.github/skills/`, 사용자 수준 Copilot 자산(MCP 설정, 개인 agents 등)은 `~/.copilot/` 아래에 둡니다. 이 프로젝트도 해당 공식 규칙에 맞게 정리했습니다.

## 기능

- **`/ingest`** — [markitdown](https://github.com/microsoft/markitdown)을 사용하여 파일(PDF, DOCX, HTML, CSV 등)을 검색 가능한 Markdown으로 변환
- **`/query`** — [ripgrep](https://github.com/BurntSushi/ripgrep)을 사용하여 지식 베이스 전문 검색
- **에이전트 우선 설계** — Copilot CLI 에이전트로 구축. skills, tools, 슬래시 커맨드 포함
- **MCP 통합** — Microsoft Learn 등 외부 지식 소스로 확장 가능
- **100% 로컬** — 클라우드 서비스 불필요, 벡터 데이터베이스 불필요, Web UI 불필요

## 빠른 시작

### 사전 요구사항

- Python 3.10+
- [markitdown](https://github.com/microsoft/markitdown): `pip install "markitdown[all]"`
- [ripgrep](https://github.com/BurntSushi/ripgrep): `brew install ripgrep` / `apt install ripgrep`

### 설치

```bash
git clone https://github.com/haxudev/personal_kb.git
cd personal_kb
python -m venv .venv
source .venv/bin/activate
pip install "markitdown[all]"
```

### 사용법

1. 파일을 `inbox/`에 배치:
   ```bash
   cp ~/Documents/report.pdf inbox/
   ```

2. 파일 수집:
   ```bash
   python scripts/ingest.py
   # 또는 Copilot CLI에서: /ingest
   ```

3. 지식 베이스 검색:
   ```bash
   rg --type md --smart-case "검색 키워드" workmemory/
   # 또는 Copilot CLI에서: /query 검색 키워드
   ```

## 프로젝트 구조

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
## MCP 설정

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)을 통해 에이전트가 외부 지식 소스에 접근할 수 있습니다. 본 프로젝트에는 Microsoft Learn 설정이 포함되어 있습니다.

### Copilot CLI에서 설정

1. `tools/mcp.example.json` 내용을 `~/.copilot/mcp-config.json` 에 복사하거나 병합합니다
2. Microsoft Learn MCP 서버를 통해 Microsoft 문서를 검색합니다
3. 사용자 수준 MCP / agents / skills 는 기본적으로 `~/.copilot/` 아래에 저장됩니다

```json
{
  "mcpServers": {
    "microsoft-learn": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-remote", "https://learn.microsoft.com/api/mcp"],
      "description": "MCP 프로토콜을 통한 Microsoft Learn 문서 검색"
    }
  }
}
```

## 테스트 실행

```bash
python scripts/preflight.py
python tests/test_all.py
```

테스트 범위:
1. 단일 파일 수집
2. 하위 디렉토리를 포함한 디렉토리 수집
3. 매칭 결과가 있는 쿼리
4. 매칭 결과가 없는 쿼리

## 기여하기

1. 리포지토리를 포크
2. 기능 브랜치 생성
3. 변경 사항 커밋
4. 테스트 실행: `python tests/test_all.py`
5. Pull Request 제출

## 라이선스

[MIT](../LICENSE)


## Command Reference Matrix

| Scenario | Windows CMD / PowerShell | macOS / Linux / WSL |
|---|---|---|
| Preflight | `python scripts\preflight.py` | `python scripts/preflight.py` |
| Ingest | `python scripts\ingest.py` | `python scripts/ingest.py` |
| Ingest (force) | `python scripts\ingest.py --force` | `python scripts/ingest.py --force` |
| Query | `rg --type md --smart-case "your query" workmemory` | `rg --type md --smart-case "your query" workmemory/` |
| Query fallback | `findstr /S /N /I "your query" workmemory\*.md` | `grep -rn --include="*.md" "your query" workmemory/` |
