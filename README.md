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
