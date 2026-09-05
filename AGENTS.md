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

TODO 1行では背景、完了条件、依存関係、調査記録が不足する場合、所有するareaまたはproject配下にアクションサポートノートを作り、チェックボックス直下から`Details`リンクを張ります。状態、期限、次のアクションはMOCに保ち、サポートノート内では未完チェックボックスを使いません。

## 会議メモとタスク取り込み

会議メモは input record であり、タスクの正本ではありません。**アクション・決定は、議事録を作ったのと同じセッションで宛先まで書き切ります。** ただし**読まずに書かないこと**——宛先へ書くには、その既存記述・粒度・重複を把握したうえで、適切な場所に適切な粒度で書き込む必要があります。

1. 議事録にアクション・決定を記録する。
2. **宛先ごとに、その project / area の MOC と関連する正典を実際に読む**（ステータスブロック・既存の記述・粒度）。
3. **既に反映済み・上書きになる・重複になるものは転記せずクローズする。** 残りを適切な粒度で書く。
4. 議事録に「タスク反映先」節を作り、**何をどこへ書いたか／書かなかった判断**を残す。
5. 議事録本文では原則 `- [ ]` を使わず、表や番号リストで記録する。例外的に議事録自体をタスクソースにする場合だけ `<!-- kb-tasks:include -->` を使う。

**宛先が多くて 1 セッションで読み切れないときだけ**、残りを「反映TODO」として `- [ ]` に起票し、次セッションへ渡します（例外であって既定ではありません）。

> **なぜ「TODO に留める」をやめたか。** 以前は「対象の文脈を読み込んでいないセッションは直接編集せず、反映TODOを起票するに留める」というルールでした。運用した結果、**TODO を積んでも結果は「別セッションでまとめて反映して」と依頼するだけ**で、宛先を読む作業は同じだけ発生し、間に TODO の管理コストとタスク索引の膨張が挟まるだけでした。**要求すべきなのは「セッションを分けること」ではなく「宛先を読む手順を踏むこと」**です。

## 完了・非アクティブ化時の蒸留

project が完了した、または area が自分・チームの継続責任ではなくなった場合は、archive 前に再利用可能な知識を蒸留します。

継続中の project でも、残る作業から独立して完了判定できる作業単位は部分完了として蒸留します。再利用可能な知識と継続する未完タスクを現役ファイルへ移し、固有の経緯を `archives/` へ移したうえで、MOCから完了状態・完了タスク・リンクを外します。MOCは完了履歴ではなく、現在地と次のアクションの地図として薄く保ちます。

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

検証済みのまとまりになったら、こまめにコミットしてください。未コミットの変更を残して作業を終える場合は、理由と残っている変更を明示してください。

## 作業ツリー

**セッションを並行して走らせるなら、編集は worktree で行い、`main` をチェックアウトしたツリーでは 1 文字も編集しません。**

理由は「`main` のツリーが汚れていると誰もマージできなくなる」ことです。`git merge` は上書き対象のファイルに未コミット変更があると中断するので、**あるセッションが `main` のツリーに書きかけを置いている間、他のセッションは自分の作業を `main` へ入れられません**。この KB の作業は複数の MOC と正典にまたがるので、これは実際に起きます。

1. 作業ごとに `git worktree add .worktrees/<作業名> -b <branch>` で切り、そこで編集・コミットする。
2. 取り込みは `main` のツリーで `git merge --no-ff <branch>`。
3. **取り込んだら worktree とブランチを 2 つで 1 組で消す**（`git worktree remove <path>` → `git branch -d <branch>`）。`-d` は取り込み済みのときだけ成功するので、**失敗したら「まだ入っていない」というサイン**です。`-D` で強制しないでください。

- ⛔ **規模で判断しないこと。** 「小さいから直接でいい」が積み上がると必ず汚れます。閾値を置かず「`main` のツリーは誰も編集しない」を不変条件にすると、マージが他人の都合で止まらなくなります。
- ⚠️ **worktree 内のファイル操作は絶対パスで書いてください。** カレントディレクトリが次のコマンド呼び出しへ持続するかは実行環境によって違い、取り違えると `main` のツリーを編集してしまいます。
- **`main` のツリーが汚れていたら、他セッションの書きかけの可能性があります。** `git stash` / `git commit` / `git restore` のどれもせず、汚れが消えるのを待つか人間に渡してください。他人の作業を巻き上げたり消したりしないためです。
- **worktree を消してブランチだけ残すと放置ブランチが溜まります。** `git for-each-ref refs/heads/` は「他セッションが今どのブランチで作業中か」を読むための数少ない信号なので、残骸があると読めなくなります。

セッションを 1 本しか走らせないなら、この節は任意です。ただし**採用したら規模による例外は置かないでください**（上のとおり、例外を置くと必ず崩れます）。

## 命名

- ファイル名は lowercase kebab-case にする。
- `_core/`、`projects/`、`areas/`、`resources/` では Johnny.Decimal 風の prefix を使う。
- `decisions/` と `archives/` では Johnny.Decimal prefix を使わない。
- MOC ファイルは `AC.00-*-moc.md` とする。

topic-scoped numbering を採用する場合:

- 新しい project は原則として既存の主題帯を使い、一時的な取り組みごとに新しい番号帯を割り当てない。
- カテゴリは一時的な project ではなく、複数の取り組みで長期間使う安定した主題に割り当てる。
- 個別の調査・設計・手順は、既存カテゴリ内の `.01`〜`.99` を使って増やす。
- 新しい10単位の番号帯は、既存主題に分類できない長期的な責任領域に限って割り当てる。
- `70-99` の未使用帯を使い切り、さらに新しい帯が必要になった時点で3桁カテゴリを許可する拡張ルールを追加する。それまでは3桁番号を使用しない。

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

When a one-line TODO lacks enough background, completion criteria, dependencies, or research history, create an action support note under the owning area or project and add an indented `Details` link below the checkbox. Keep state, due dates, and next actions in the MOC, and do not use open checkboxes in the support note.

## Meeting Notes And Task Intake

Meeting notes are input records, not task sources of truth. **Reflect actions and decisions into their targets in the same session that writes the meeting note.** But do not write blind: reaching the right place at the right granularity requires knowing what the target already says.

1. Record actions and decisions in the meeting note.
2. **For each target, actually read that project or area MOC and the canonical pages it points to** (status block, existing wording, granularity).
3. **Close anything already reflected, superseded, or duplicated instead of copying it.** Write the rest at the right granularity.
4. Add a "Reflected into" section to the meeting note recording **what went where, and what you decided not to carry over**.
5. Avoid `- [ ]` checkboxes in meeting notes by default; use tables or numbered lists instead. Use `<!-- kb-tasks:include -->` only when the meeting note itself is intentionally a task source.

**Only when there are too many targets to read in one session**, file the remainder as intake TODOs (`- [ ]`) and hand them to the next session. That is the exception, not the default.

> **Why the intake-TODO-only rule was dropped.** The earlier rule said a session that had not loaded the target context must not edit it directly, and should only file an intake TODO. In practice, filing the TODO just deferred the same work to a later session that still had to read the target, while adding TODO bookkeeping and inflating the task index. **What needs to be required is reading the target, not splitting the session.**

## Closure And Distillation

When a project is complete, or an area is no longer an ongoing responsibility for you or your team, distill reusable knowledge before archiving it.

Within an ongoing project, treat a work unit whose completion can be determined independently from the remaining work as a partial closure. Move reusable knowledge and continuing open actions into active files, move work-unit-specific history to `archives/`, and remove completed state, completed actions, and links from the MOC. Keep the MOC thin as a map of current state and next actions, not as a completed-history log.

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

Commit frequently once a verified change is coherent. If you end work with uncommitted changes, state why and list what remains.

## Working Trees

**If you run sessions concurrently, edit in a worktree and never edit the tree that has `main` checked out.**

The reason is that a dirty `main` tree blocks everyone's merges. `git merge` aborts when a file it would overwrite has uncommitted changes, so **while one session leaves work in progress in the `main` tree, no other session can land its own work**. Work in this KB routinely spans several MOCs and canonical pages, so this happens in practice.

1. Create a worktree per unit of work: `git worktree add .worktrees/<name> -b <branch>`. Edit and commit there.
2. Land it from the `main` tree with `git merge --no-ff <branch>`.
3. **Remove the worktree and the branch together** (`git worktree remove <path>`, then `git branch -d <branch>`). `-d` only succeeds when the branch is already merged, so **a failure is the signal that it is not in yet**. Do not force with `-D`.

- ⛔ **Do not decide by size.** "This one is small enough to do directly" accumulates until the tree is dirty. Setting no threshold makes "nobody edits the `main` tree" an invariant, and merges stop depending on someone else's timing.
- ⚠️ **Use absolute paths for file operations inside a worktree.** Whether the current directory persists across command invocations depends on the runtime, and getting it wrong means editing the `main` tree by accident.
- **If the `main` tree is dirty, it may be another session's work in progress.** Do not `git stash`, `git commit`, or `git restore` it — wait for it to clear, or hand it to a human. Never sweep up or discard someone else's work.
- **Removing a worktree while leaving its branch behind accumulates stale branches.** `git for-each-ref refs/heads/` is one of the few signals for "which branch is another session working on right now", and leftovers make it unreadable.

If you only ever run one session, this section is optional. **But once you adopt it, do not add size-based exceptions** — as above, exceptions always erode it.

## Naming

- Use lowercase kebab-case filenames.
- Use Johnny.Decimal-style prefixes in `_core/`, `projects/`, `areas/`, and `resources`.
- Do not use Johnny.Decimal prefixes in `decisions/` or `archives/`.
- MOC files use `AC.00-*-moc.md`.

When using topic-scoped numbering:

- New projects should use an existing topic range by default; do not allocate a new range for each temporary initiative.
- Allocate categories to stable, long-lived topics that can serve multiple initiatives, not to temporary projects.
- Add individual research notes, designs, and procedures as `.01` through `.99` within an existing category.
- Allocate a new ten-number range only to a long-lived responsibility that does not fit an existing topic.
- After exhausting the unused `70-99` ranges and needing another range, add an explicit extension rule that permits three-digit categories. Do not use three-digit numbers before then.
