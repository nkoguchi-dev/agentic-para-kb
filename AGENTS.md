# AGENTS.md

このナレッジベースで作業する coding agent 向けのガイドライン。

詳細仕様の正本は [`_core/00-09_index/00.01-kb-structure-rules.md`](./_core/00-09_index/00.01-kb-structure-rules.md) にあります。このファイルは薄い地図です。

## リポジトリの目的

このリポジトリは、agent-assisted work のための Markdown ナレッジベースです。PARA、decision records、MOC、検証スクリプトを組み合わせます。

## 作業開始時

新しいタスクを始めるときは、次の順で確認します。

1. `_core/00-09_index/00.02-tasks.md` を読み、未完アクションを把握する。
2. `_core/00-09_index/00.00-moc.md` を読み、関連する area または project を選ぶ。
3. 現在のタスクに必要なリンク先だけを読む。

## ディレクトリルール

- `_core/`: 安定した定義、ルール、原則。
- `decisions/`: 追記型の decision records。過去の決定を書き換えず、新しい決定を追加するか update を追記する。
- `projects/`: 明確な完了条件がある取り組み。
- `areas/`: 継続的な責任領域。
- `resources/`: 再利用可能な参照情報。
- `archives/`: 完了・非アクティブになった情報。現在の状態として検索・引用・依存しない。

## ステータスブロック

すべての project / area MOC には、次のブロックを置きます。

```markdown
## Status (Last updated: YYYY-MM-DD)

| Task | State | Due |
|---|---|---|
| Example task | 🟡 In progress | YYYY-MM |
```

状態は次を使います。

- 🔴 Not started
- 🟡 In progress
- 🟢 Done
- ⏸ Paused

未完アクションはステータスブロックの下に `- [ ]` で書きます。完了したアクションは、強い理由がない限り削除せず `- [x]` にします。

## 完了・非アクティブ化時の蒸留

project が完了した、または area が自分・チームの継続責任ではなくなった場合は、archive 前に再利用可能な知識を蒸留します。

1. 対象 MOC の状態と最終更新日を更新する。
2. 安定したルール・定義は `_core/`、横断的な意思決定は `decisions/`、再利用可能な参照情報は `resources/`、継続して残る責任領域は `areas/` へ移す。
3. root MOC と関連 MOC のリンクを更新する。
4. 終了済み project / 非アクティブ area を `archives/` へ移動する。
5. タスク集約を再生成し、リンクチェックを実行する。

## 検証

Markdown ファイルを追加・移動・編集した後は、次を実行します。

```sh
python3 tools/check-links.py
python3 tools/kb-tasks.py --write
```

`_core/00-09_index/00.02-tasks.md` は生成物です。手で編集しないでください。

## 命名

- ファイル名は lowercase kebab-case にする。
- `_core/`、`projects/`、`areas/`、`resources/` では Johnny.Decimal 風の prefix を使う。
- `decisions/` と `archives/` では Johnny.Decimal prefix を使わない。
- MOC ファイルは `AC.00-*-moc.md` とする。

---

# AGENTS.md

Guidelines for coding agents working in this knowledge base.

Canonical details live in [`_core/00-09_index/00.01-kb-structure-rules.md`](./_core/00-09_index/00.01-kb-structure-rules.md). This file is a short map.

## Repository Purpose

This repository is a Markdown knowledge base designed for agent-assisted work. It combines PARA, decision records, MOCs, and validation scripts.

## Start Here

At the start of a new task:

1. Read `_core/00-09_index/00.02-tasks.md` to understand open actions.
2. Read `_core/00-09_index/00.00-moc.md` to choose the relevant area or project.
3. Read only the linked files needed for the current task.

## Directory Rules

- `_core/`: Stable definitions, rules, and principles.
- `decisions/`: Append-only decision records. Do not rewrite old decisions; add a new decision or append an update.
- `projects/`: Work with a clear end condition.
- `areas/`: Ongoing responsibilities.
- `resources/`: Reusable reference material.
- `archives/`: Completed or inactive material. Do not search, cite, or rely on it for current state.

## Status Blocks

Every project and area MOC should contain:

```markdown
## Status (Last updated: YYYY-MM-DD)

| Task | State | Due |
|---|---|---|
| Example task | 🟡 In progress | YYYY-MM |
```

Use these states:

- 🔴 Not started
- 🟡 In progress
- 🟢 Done
- ⏸ Paused

Unfinished actions should be written as `- [ ]` below the status block. Completed actions should become `- [x]` unless there is a strong reason to remove them.

## Closure And Distillation

When a project is complete, or an area is no longer an ongoing responsibility for you or your team, distill reusable knowledge before archiving it.

1. Update the target MOC status and last-updated date.
2. Move stable rules or definitions to `_core/`, cross-cutting decisions to `decisions/`, reusable references to `resources/`, and ongoing responsibilities that remain active to `areas/`.
3. Update the root MOC and related MOC links.
4. Move the completed project or inactive area to `archives/`.
5. Regenerate the task index and run link checks.

## Validation

After adding, moving, or editing Markdown files:

```sh
python3 tools/check-links.py
python3 tools/kb-tasks.py --write
```

`_core/00-09_index/00.02-tasks.md` is generated. Do not edit it manually.

## Naming

- Use lowercase kebab-case filenames.
- Use Johnny.Decimal-style prefixes in `_core/`, `projects/`, `areas/`, and `resources`.
- Do not use Johnny.Decimal prefixes in `decisions/` or `archives/`.
- MOC files use `AC.00-*-moc.md`.
