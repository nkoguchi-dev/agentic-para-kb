# agentic-para-kb

PARA、ADR、MOC、軽量な agent 向け指示を組み合わせた、agent-ready な Markdown ナレッジベースフレームワーク。

このリポジトリの目的は、人間と coding agent の両方にとって扱いやすい知識ベースを作ることです。

- 人間は、plain Markdown と Git で管理できる local-first な知識ベースを持てる。
- agent は、予測可能な入口、安定したファイル名、限定されたコンテキスト、検証ツールを使える。
- リポジトリは、Git と標準的なコマンドラインツールで検査・運用できる。

## 構造

```text
agentic-para-kb/
├── AGENTS.md
├── _core/
│   ├── 00-09_index/
│   │   ├── 00.00-moc.md
│   │   ├── 00.01-kb-structure-rules.md
│   │   └── 00.02-tasks.md
│   └── 10-19_domain/
│       └── 10.01-principles-template.md
├── decisions/
├── projects/
├── areas/
├── resources/
├── archives/
└── tools/
```

## レイヤー

- `_core/`: 安定したルール、原則、ドメイン定義。
- `decisions/`: 横断的な意思決定を記録する追記型の decision records。
- `projects/`: 完了条件がある取り組み。
- `areas/`: 終わりのない継続的な責任領域。
- `resources/`: 複数の project / area から再利用される参照情報。
- `archives/`: 完了・非アクティブになった情報。agent は現在の文脈として使わない。

## Quick Start

1. このリポジトリをテンプレートとしてコピーする。
2. example project、area、resource を自分の内容に置き換える。
3. `_core/10-19_domain/10.01-principles-template.md` を更新する。
4. `python3 tools/check-links.py` を実行する。
5. `python3 tools/kb-tasks.py --write` を実行する。
6. 必要なら `bash tools/install-hooks.sh` で pre-commit hook を入れる。

## 設計メモ

このフレームワークでは、以下を意図的に分けます。

- agent が頻繁に読む「地図」: `AGENTS.md`、MOC、タスク索引。
- 必要に応じて読む「領土」: project note、area note、resource、decision。
- 安定したルールと、変化する現在の状態。

地図は薄く保ち、詳細はリンク先に置きます。

---

# agentic-para-kb

An agent-ready Markdown knowledge base framework based on PARA, ADRs, MOCs, and lightweight repository instructions.

The goal is to keep knowledge useful for both humans and coding agents:

- Humans get a durable local-first knowledge base made of plain Markdown files.
- Agents get predictable entry points, stable file names, scoped context, and validation tools.
- The repository stays inspectable with Git and standard command-line tools.

## Structure

```text
agentic-para-kb/
├── AGENTS.md
├── _core/
│   ├── 00-09_index/
│   │   ├── 00.00-moc.md
│   │   ├── 00.01-kb-structure-rules.md
│   │   └── 00.02-tasks.md
│   └── 10-19_domain/
│       └── 10.01-principles-template.md
├── decisions/
├── projects/
├── areas/
├── resources/
├── archives/
└── tools/
```

## Layers

- `_core/`: Stable rules, principles, and domain definitions.
- `decisions/`: Append-only decision records for cross-cutting decisions.
- `projects/`: Outcomes with an end condition.
- `areas/`: Ongoing responsibilities without a natural end date.
- `resources/`: Reusable reference material.
- `archives/`: Completed or inactive material. Agents should not use this as current context.

## Quick Start

1. Copy this repository as a template.
2. Replace the example project, area, and resource files.
3. Update `_core/10-19_domain/10.01-principles-template.md`.
4. Run `python3 tools/check-links.py`.
5. Run `python3 tools/kb-tasks.py --write`.
6. Optionally install the pre-commit hook with `bash tools/install-hooks.sh`.

## Design Notes

This framework intentionally separates:

- Map files that agents read often: `AGENTS.md`, MOCs, task indexes.
- Territory files that agents read on demand: project notes, area notes, resources, decisions.
- Stable rules from active state.

Keep the map small. Put details behind links.
