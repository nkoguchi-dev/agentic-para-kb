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

## 完了・非アクティブ化時の蒸留

project が完了した、または area が自分・チームの継続責任ではなくなった場合は、archive 前に再利用可能な知識を蒸留します。

継続中の project でも、残る作業から独立して完了判定できる作業単位には同じ蒸留手順を適用します。再利用可能な知識と継続する未完タスクを現役ファイルへ移し、固有の経緯を archive したうえで、MOCを現在地と次のアクションに絞ります。

- 安定したルール・定義 → `_core/`
- 横断的な意思決定 → `decisions/`
- 再利用可能な参照情報 → `resources/`
- 継続して残る責任領域 → `areas/`
- 残りの終了済み project / area → `archives/`

その後、MOC のリンクを更新し、`python3 tools/kb-tasks.py --write` と `python3 tools/check-links.py` を実行します。

## 完了ログを索引に畳む

蒸留は project の終わりに 1 度やるものですが、**完了した `- [x]` は動いているあいだにも溜まります。** 中身が他所に実在するなら「何を・いつ・どこへ」の 1 行へ畳んでください。

⚠️ 放置すると MOC の主成分が「もう終わったこと」になります。運用中の実 KB では、完了 193 件・88,217 字に対して未完は 334 件・32,543 字でした（**完了が未完の 2.7 倍**）。**完了した瞬間に「なぜそう決めたか」が書き足される**のが原因です。

判定は 2 段構え（識別子の照合 → 散文の決定は本文を読む）で、⛔ **畳む前に前提が今も生きているかを確かめます**。手順と落とし穴は `AGENTS.md` の「完了ログを索引に畳む」節にあります。

## 会議メモとタスク取り込み

会議メモは input record であり、タスクの正本ではありません。**アクション・決定は、議事録を作ったのと同じセッションで宛先まで書き切ります。** ただし読まずに書かないこと。

- 議事録にアクション・決定を記録する。
- **宛先ごとに、その project / area の MOC と関連する正典を実際に読む**（既存の記述・粒度・重複）。
- **既に反映済み・上書きになる・重複になるものは転記せずクローズする。** 残りを適切な粒度で書く。
- 議事録に「タスク反映先」節を作り、何をどこへ書いたか／書かなかった判断を残す。
- 議事録本文では原則 `- [ ]` を使わず、表や番号リストで記録する。
- **宛先が多くて 1 セッションで読み切れないときだけ**、残りを「反映TODO」として次セッションへ渡す（例外）。

以前は「対象の文脈を読み込んでいないセッションは直接編集せず、反映TODOを起票するに留める」というルールでしたが、**TODO を積んでも宛先を読む作業は同じだけ発生し、TODO の管理コストとタスク索引の膨張が挟まるだけ**でした。要求すべきなのは**セッションを分けることではなく、宛先を読む手順を踏むこと**です。

## 大規模KB向けの任意パターン

### ドメインprefix付き番地

大規模な業務KBやチームKBでは、JD番号の枯渇を避けるためにドメインprefix付き番地を使ってもよいです。

```text
<domain>.AC.ID-name.md
```

例:

- `dev.31.01-aws-account-structure.md`
- `org.20.03-kb-lint-policy.md`
- `hr.40.00-recruiting-index.md`
- `sec.80.00-security-requirements-index.md`

prefix は知識ドメイン、フォルダは PARA 上のライフサイクルを表します。prefix ごとに独立した番号空間を持ち、prefix/category の割当は root MOC の registry で管理します。

### 並行セッションと作業ツリー

複数のエージェントセッションを同時に走らせるなら、編集は git worktree で行い、`main` をチェックアウトしたツリーでは編集しません。`git merge` は上書き対象のファイルに未コミット変更があると中断するため、**`main` のツリーに書きかけがあるあいだ、他のセッションは自分の作業を取り込めなくなります**。手順と落とし穴は `AGENTS.md` の「作業ツリー」節にあります。

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

## ライセンス

MIT License. 詳細は [LICENSE](LICENSE) を参照してください。

テンプレートとして自由にコピー・改変して構いません。コピーや実質的な部分には著作権表示とライセンス文を残してください。

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

## Closure And Distillation

When a project is complete, or an area is no longer an ongoing responsibility for you or your team, distill reusable knowledge before archiving it.

Apply the same workflow to a work unit within an ongoing project when its completion can be determined independently from the remaining work. Move reusable knowledge and continuing open actions into active files, archive work-unit-specific history, and keep the MOC focused on current state and next actions.

- Stable rules or definitions -> `_core/`
- Cross-cutting decisions -> `decisions/`
- Reusable references -> `resources/`
- Ongoing responsibilities that remain active -> `areas/`
- Remaining completed projects or inactive areas -> `archives/`

Then update MOC links and run `python3 tools/kb-tasks.py --write` and `python3 tools/check-links.py`.

## Folding Completed Logs Into An Index

Distillation happens once, at closure. **Completed `- [x]` entries pile up while the work is still running.** Fold each into a single "what / when / where it went" line once its content exists elsewhere.

⚠️ Left alone, finished work becomes the bulk of the MOC. Measured on a real KB in daily use: 193 completed entries totalling 88,217 characters against 334 open ones totalling 32,543 — **completed work was 2.7x the volume of open work**. The cause is that **the reasoning gets appended the moment something completes**.

Deciding takes two passes (token comparison, then reading the body for prose decisions), and ⛔ **check that the entry's premise is still current before folding**. The procedure and its pitfalls are in the "Folding Completed Logs Into An Index" section of `AGENTS.md`.

## Meeting Notes And Task Intake

Meeting notes are input records, not task sources of truth. **Reflect actions and decisions into their targets in the same session that writes the meeting note** — but do not write blind.

- Record actions and decisions in the meeting note.
- **For each target, actually read that project or area MOC and the canonical pages it points to** (existing wording, granularity, duplication).
- **Close anything already reflected, superseded, or duplicated instead of copying it.** Write the rest at the right granularity.
- Add a "Reflected into" section to the meeting note recording what went where, and what you decided not to carry over.
- Avoid `- [ ]` checkboxes in meeting notes by default; use tables or numbered lists instead.
- **Only when there are too many targets to read in one session**, hand the remainder to the next session as intake TODOs (the exception, not the default).

The earlier rule required filing intake TODOs instead of editing targets directly. In practice that deferred the same reading work to a later session while adding bookkeeping and inflating the task index. **What needs to be required is reading the target, not splitting the session.**

## Optional Patterns For Larger Knowledge Bases

### Domain-Prefixed Addressing

For larger team or business knowledge bases, use domain-prefixed addresses to avoid exhausting Johnny.Decimal number ranges.

```text
<domain>.AC.ID-name.md
```

Examples:

- `dev.31.01-aws-account-structure.md`
- `org.20.03-kb-lint-policy.md`
- `hr.40.00-recruiting-index.md`
- `sec.80.00-security-requirements-index.md`

The domain prefix represents a knowledge domain. The PARA folder represents lifecycle/state. Each domain prefix has an independent number space. Maintain prefix/category assignments in the root MOC registry.

### Concurrent Sessions And Working Trees

If you run several agent sessions at once, edit in a git worktree and never edit the tree that has `main` checked out. `git merge` aborts when a file it would overwrite has uncommitted changes, so **while the `main` tree holds work in progress, no other session can land its own work**. The procedure and its pitfalls are in the "Working Trees" section of `AGENTS.md`.

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

## License

MIT License. See [LICENSE](LICENSE).

Copy and adapt this template freely. Keep the copyright notice and the license text in copies or substantial portions.
