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

未完アクションはステータスブロックの下に `- [ ]` で書きます。完了したアクションは削除せず `- [x]` にします。ただし**そのまま置き続けないでください**——完了エントリは、放置すると MOC の主成分になります（下記「完了ログを索引に畳む」）。

TODO 1行では背景、完了条件、依存関係、調査記録が不足する場合、所有するareaまたはproject配下にアクションサポートノートを作り、チェックボックス直下から`Details`リンクを張ります。状態、期限、次のアクションはMOCに保ち、サポートノート内では未完チェックボックスを使いません。

**既に段落化している古い起票行は、一括では畳みません**——次にその項目を触るときにノートへ剥がします。⭐ **例外は「1 つの節が MOC 全体の 3 割を超えたとき」。** そこまで育つと、次に触るのを待つ流儀では追いつきません（実測＝784 行・112,015 字まで育った MOC で、1 節が 44,580 字＝全体の 40% を占めていた。5 つの塊をノートへ移して 553 行・51,452 字へ戻した）。

**一括で畳むときは、欠落していないことを機械的に確かめてから畳みます。** 手順は「完了ログを索引に畳む」と同じ 2 段構えで、(1) 畳む前の本文から識別子・コード・数値を集合として抜く (2) 移設後の全ファイルを連結した文字列に対し、その集合が全件現れることを確かめる (3) 現れないものだけを人が読み、同義の言い換えか本当の欠落かを判定する。

- ⚠️ **強調句の字面一致では判定できません。** 受け皿のノートが同じ事実をより詳しい別の言い回しで書いていることが多く、実測では強調句 153 個中 105 個が字面一致しませんでしたが**欠落は 0** でした（識別子側は 533 種で欠落 0）。
- ⛔ **受け皿のノートが既にあるときは新しく作らないでください**（同じ話の置き場が分かれます）。既存ノートに無い事実だけを該当節へ足し、重複していた分を落とします。
- **落とすのは重複だけで、要約はしません。**

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

## 完了ログを索引に畳む

**完了した `- [x]` は、中身が他所に実在するなら「何を・いつ・どこへ」の 1 行に畳みます。** 節の見出しは「完了の記録 — 移送先の索引」のように、索引であることが分かる名前にしてください。

⛔ **畳むときに issue の状態・完了日・PR 番号は落とします。** それらは issue tracker と git が持っている情報で、MOC が二重に持つと必ず古くなります。`ISSUE-810 完了（2026-08-27・PR #821）` ではなく、**何を決めたか・現在の実装事実**を残してください。⚠️ **完了ログ節はリンクチェッカから見えません**（エントリは `- [x]` 行か引用ブロックで、多くの検査が両方を対象外にしている）ので、**ここは手順だけが防壁です。**

⚠️ **これを怠ると MOC の主成分が「もう終わったこと」になります。** 運用中の実 KB で測ったところ、完了 **193 件・88,217 字**に対して未完は **334 件・32,543 字**でした（**完了が未完の 2.7 倍**）。件数では未完のほうが多いのに総量が逆転するのは 1 件あたりの長さが違うためで、完了 424 字／未完 97 字。**完了した瞬間に「なぜそう決めたか」が書き足されて肥大する**構造になっています。

畳めるかの判定は 2 段構えです。

1. **識別子・コード・数値を集合として抜き、KB 全体と関連リポジトリに存在するかを突き合わせる。** ⚠️ **照合先を同じ area に限ると誤検知が出ます**（実測で「欠落」が 46 件 → KB 全体とリポジトリまで広げて 6 件、うち実質の欠落は 0）。
2. **散文の決定はトークンに掛かりません。** 本文を読んで移送先を確かめてください。

- ⛔ **畳む前に、そのエントリが前提にしている決定が今も生きているかを確かめること。** **エントリ自身が「状態の正本は◯◯」と書いていたら、必ずそこを読みます。** 実測で、**前提が 25 日前に覆っていた**のに気づかず「移送先が無いので畳めない」と誤判定しました。**索引化はエントリの棚卸しを兼ねます。**
- **移送先に無い固有分は、落とす前に該当ファイルへ上げる。** ⭐ 上げたことで別の作業が楽になることがあります（実例＝完了ログに埋もれていた配布ミラーのページ ID を各ページの「一次情報の所在」へ上げたところ、それまで名前でしか指されておらず同期のたびに探し直していたものが引けるようになった）。
- **落とすのは重複だけで、要約はしません。** **「やらないと決めた」ものも、その決定が他所にあるなら畳めます**——取り下げだから畳めない、ではありません。
- **トリガはその MOC を次に触ったとき。** ⛔ **量の閾値は置かないでください。** 量では「畳んではいけないもの」と区別できません——**畳まない判断は個別の事情によるので、その MOC 自身に理由を書きます**（機械検査に例外リストを持たせない）。
- ⚠️ **触ったときだけでは、触られない場所へ永遠に届きません。** 定期的に棚卸しの場を設けて対にしてください。**捨ててよいかの判断は自動化できない**ので、人が判断する場が要ります。

## 検証

Markdown ファイルを追加・移動・編集した後は、次を実行します。

```sh
python3 tools/kb-lint.py            # 全走査
python3 tools/kb-lint.py <path>...  # 触ったファイルだけ
python3 tools/kb-tasks.py --write
```

**エラーはコミットを止め、警告は止めません。** 日付の遅れや未使用の定義でコミットを止めると、`KB_LINT_SKIP` のような回避が常用され、**止めるべきルールごと無効化されます**。CI で厳しく見たいときは `--strict` で警告もエラー扱いにできます。

⚠️ **`index-stale-date` は `--staged` と明示パス指定のときだけ判定します**（全走査で出すと、触っていないファイルの分まで毎回並んでノイズになるため）。pre-commit hook は `--staged` で呼びます。

**検査の一覧は別に持ちません。** 指摘そのものに「なぜ駄目か」を書いてあるので、出た文面を読めば足ります（一覧を別に作ると必ず実装とずれます）。

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
- **番号空間はリポジトリ全体で 1 つ**。同じ番地を 2 つのファイルが持たないこと（`addr-duplicate` がエラーで止めます）。⚠️ **バケツごとに独立させないでください**——ファイルは project から area や `archives/` へ移動するので、バケツ別に採番すると移動した瞬間に衝突します。番号帯が足りなくなったときの逃げ道が、README の「ドメインprefix付き番地」です。
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

Unfinished actions should be written as `- [ ]` below the status block. Completed actions should become `- [x]` rather than being deleted. But **do not leave them sitting there** — completed entries become the bulk of a MOC if nothing folds them (see "Folding Completed Logs Into An Index").

When a one-line TODO lacks enough background, completion criteria, dependencies, or research history, create an action support note under the owning area or project and add an indented `Details` link below the checkbox. Keep state, due dates, and next actions in the MOC, and do not use open checkboxes in the support note.

**Do not convert old task lines that have already grown into paragraphs in bulk** — peel each one into a note the next time you touch it. ⭐ **The exception is when a single section exceeds about a third of the whole MOC.** Past that point, waiting until someone touches it never catches up (measured: a MOC had grown to 784 lines / 112,015 characters with one section accounting for 44,580 of them, 40% of the file; moving five blocks into notes brought it back to 553 lines / 51,452 characters).

**When you do convert in bulk, verify mechanically that nothing was lost before dropping anything.** The procedure is the same two-pass check as "Folding Completed Logs Into An Index": extract identifiers, code symbols and numbers from the text as a set; concatenate every file the content moved into and confirm the whole set appears; then read only the items that do not appear and decide whether each is a paraphrase or a real loss.

- ⚠️ **Matching emphasized phrases verbatim does not work as a check.** The receiving note usually states the same fact in fuller, different words: in one measurement 105 of 153 emphasized phrases had no literal match, yet **nothing had been lost** (the identifier set, 533 of them, matched completely).
- ⛔ **If a receiving note already exists, do not create another one** — it splits the same subject across two places. Add only the facts the existing note lacks, and drop what was duplicated.
- **Drop duplication only; do not summarize.**

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

## Folding Completed Logs Into An Index

**Fold a completed `- [x]` into a single "what / when / where it went" line once its content exists elsewhere.** Name the section so it reads as an index, e.g. "Completed — index of where it went".

⛔ **Drop issue state, completion dates and PR numbers as you fold.** The issue tracker and git already hold them, and a second copy in the MOC will go stale. Write **what was decided and what is true of the implementation now**, not `ISSUE-810 done (2026-08-27, PR #821)`. ⚠️ **Completed-log sections are invisible to link checkers** — their entries are `- [x]` lines or quote blocks, which most checks exclude — so **procedure is the only guard here.**

⚠️ **Skip this and completed work becomes the bulk of the MOC.** Measured on a real KB in daily use: **193 completed entries totalling 88,217 characters** against **334 open ones totalling 32,543** — completed work was **2.7x the volume of open work**. There were more open items by count, so the inversion comes from length: 424 characters per completed entry against 97 per open one. **The moment something completes, the reasoning behind it gets appended**, and that is what grows.

Deciding whether an entry can be folded takes two passes.

1. **Extract identifiers, code symbols and numbers as a set, and check them against the whole KB plus any related repositories.** ⚠️ **Restricting the comparison to the same area produces false positives** (measured: 46 apparent losses shrank to 6 once the whole KB and the repositories were included, of which none were real).
2. **Prose decisions do not appear as tokens.** Read the body and confirm the destination by hand.

- ⛔ **Before folding, check that the decision the entry depends on is still current.** **If the entry itself says "the source of truth for this state is X", go read X.** Measured failure: a premise had been reversed 25 days earlier, and the entry was misjudged as unfoldable "because there is no destination". **Folding an index doubles as an audit of its entries.**
- **Anything unique that has no destination must be lifted into the relevant page before it is dropped.** ⭐ Sometimes lifting it makes another job easier — in one case the page IDs of published mirrors were buried in the completed log; they had only ever been referred to by title, so every sync had to hunt for them again.
- **Drop duplication only; do not summarize.** **Something decided against can be folded too**, as long as the decision lives elsewhere — "it was abandoned" is not a reason it cannot be folded.
- **Trigger folding the next time you touch that MOC.** ⛔ **Do not set a size threshold.** Size cannot distinguish what must not be folded — **that judgment is case-specific, so record the reason in the MOC itself** rather than maintaining an exception list inside a checker.
- ⚠️ **A touch-based trigger never reaches documents nobody touches.** Pair it with a periodic review. **Deciding what is safe to discard cannot be automated**, so the review needs a human in it.

## Validation

After adding, moving, or editing Markdown files:

```sh
python3 tools/kb-lint.py            # whole repository
python3 tools/kb-lint.py <path>...  # only the files you touched
python3 tools/kb-tasks.py --write
```

**Errors block a commit; warnings do not.** Gating on a late date or an unused definition teaches people to set something like `KB_LINT_SKIP`, which turns off every rule including the ones worth keeping. Use `--strict` in CI to treat warnings as errors.

⚠️ **`index-stale-date` only runs with `--staged` or explicit paths.** On a whole-repo run it would list every file nobody touched, every time. The pre-commit hook calls it with `--staged`.

**There is no separate list of checks.** Each finding explains why it is a problem, so reading the output is enough — a list kept elsewhere would drift from the implementation.

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
- **One number space for the whole repository.** No two files share an address (`addr-duplicate` blocks the commit). ⚠️ **Do not give each bucket its own space** — files move from a project into an area or into `archives/`, so per-bucket numbering collides the moment something moves. Running out of ranges is what the domain-prefixed addressing in the README is for.
- Do not use Johnny.Decimal prefixes in `decisions/` or `archives/`.
- MOC files use `AC.00-*-moc.md`.

When using topic-scoped numbering:

- New projects should use an existing topic range by default; do not allocate a new range for each temporary initiative.
- Allocate categories to stable, long-lived topics that can serve multiple initiatives, not to temporary projects.
- Add individual research notes, designs, and procedures as `.01` through `.99` within an existing category.
- Allocate a new ten-number range only to a long-lived responsibility that does not fit an existing topic.
- After exhausting the unused `70-99` ranges and needing another range, add an explicit extension rule that permits three-digit categories. Do not use three-digit numbers before then.
