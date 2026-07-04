#!/usr/bin/env python3
"""Check local Markdown links, excluding archives/."""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVES = REPO_ROOT / "archives"

INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
REFERENCE_DEF_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(\S+)")


@dataclass(frozen=True)
class BrokenLink:
    path: Path
    lineno: int
    target: str
    resolved: Path


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(REPO_ROOT.rglob("*.md")):
        if ARCHIVES in path.parents:
            continue
        files.append(path)
    return files


def is_local_file_link(target: str) -> bool:
    if not target or target.startswith("#"):
        return False
    parsed = urlparse(target)
    return not parsed.scheme and not parsed.netloc


def normalize_target(target: str) -> str:
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split("#", 1)[0]
    return unquote(target)


def resolve_target(source: Path, target: str) -> Path:
    target_path = Path(normalize_target(target))
    if target_path.is_absolute():
        return target_path
    return (source.parent / target_path).resolve()


def iter_links(path: Path) -> list[tuple[int, str]]:
    links: list[tuple[int, str]] = []
    in_fence = False

    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        ref_match = REFERENCE_DEF_RE.match(line)
        if ref_match:
            links.append((lineno, ref_match.group(1)))

        for match in INLINE_LINK_RE.finditer(line):
            links.append((lineno, match.group(1)))

    return links


def check_file(path: Path) -> list[BrokenLink]:
    broken: list[BrokenLink] = []
    for lineno, raw_target in iter_links(path):
        target = normalize_target(raw_target)
        if not is_local_file_link(target) or not target:
            continue
        resolved = resolve_target(path, target)
        if not resolved.exists():
            broken.append(BrokenLink(path=path, lineno=lineno, target=raw_target, resolved=resolved))
    return broken


def parse_args(argv: list[str]) -> list[Path]:
    if argv:
        return [(REPO_ROOT / arg).resolve() if not Path(arg).is_absolute() else Path(arg) for arg in argv]
    return markdown_files()


def main(argv: list[str]) -> int:
    files = parse_args(argv)
    broken: list[BrokenLink] = []

    for path in files:
        if not path.exists():
            print(f"File does not exist: {path}", file=sys.stderr)
            return 1
        if path.suffix != ".md":
            continue
        broken.extend(check_file(path))

    if broken:
        print("Broken Markdown links detected:", file=sys.stderr)
        for item in broken:
            try:
                rel_path = item.path.relative_to(REPO_ROOT)
            except ValueError:
                rel_path = item.path
            try:
                rel_resolved = item.resolved.relative_to(REPO_ROOT)
            except ValueError:
                rel_resolved = item.resolved
            print(f"- {rel_path}:{item.lineno} -> {item.target} ({rel_resolved})", file=sys.stderr)
        return 1

    print(f"OK: checked {len(files)} Markdown files", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
