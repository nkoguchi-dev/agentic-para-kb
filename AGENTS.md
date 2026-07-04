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
