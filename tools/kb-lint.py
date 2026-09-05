#!/usr/bin/env python3
"""Structure and link checks for an agentic PARA knowledge base.

Standard library only: the pre-commit hook runs this with a bare `python3`,
so a dependency here would mean setting up a virtualenv to make commits work.

Errors block a commit. Warnings do not. That split is deliberate: gating on
soft checks (a stale date, an unused definition) teaches people to set
KB_LINT_SKIP=1, which disables every rule including the ones worth keeping.
Use --strict to promote warnings to errors in CI.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent  # not the cwd: the hook may run from anywhere

MOVABLE = ("projects/", "areas/", "resources/")
IMMOVABLE = ("_core/", "decisions/")
MAP_LAYER = "_core/00-09_index/"
ROOT_MOC = "_core/00-09_index/00.00-moc.md"
GENERATED = {"_core/00-09_index/00.02-tasks.md"}
NOT_LINKED_FROM_MAP = {"AGENTS.md", "README.md"}

ADDRESS_RE = re.compile(r"^(\d{2})\.(\d{2})(?:[-.]|$)")
LAST_UPDATED_RE = re.compile(r"Last updated:\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r"Last updated:\s*YYYY-MM-DD", re.IGNORECASE)  # unfilled template
INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
REF_DEF_RE = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s*(\S+)")
REF_USE_RE = re.compile(r"(?<!\!)\[[^\]]*\]\[([^\]]+)\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
TRACKER_KEY_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,9}-\d+\b")
TRACKER_STATE_RE = re.compile(
    r"(?:\bPR\s*#\d+|\bmerged\b|\bclosed\b|\bdone\b|\bin progress\b|\bresolved\b"
    r"|完了|クローズ|対応中|着手|マージ済)",
    re.IGNORECASE,
)


# --------------------------------------------------------------------------
# findings
# --------------------------------------------------------------------------
@dataclass
class Finding:
    severity: str  # "error" | "warning"
    code: str
    rel: str
    lineno: int | None
    message: str


@dataclass
class Report:
    items: list[Finding] = field(default_factory=list)

    def error(self, code: str, rel: str, lineno: int | None, message: str) -> None:
        self.items.append(Finding("error", code, rel, lineno, message))

    def warn(self, code: str, rel: str, lineno: int | None, message: str) -> None:
        self.items.append(Finding("warning", code, rel, lineno, message))


# --------------------------------------------------------------------------
# document model
# --------------------------------------------------------------------------
@dataclass
class Doc:
    rel: str
    lines: list[str]
    code: set[int]                              # 1-based line numbers inside fences
    headings: list[tuple[int, str]]
    inline: list[tuple[int, str]]               # (lineno, target)
    ref_defs: dict[str, tuple[int, str]]        # label -> (lineno, target)
    ref_uses: dict[str, list[int]]


def parse_doc(rel: str, text: str) -> Doc:
    lines = text.split("\n")
    code: set[int] = set()
    headings: list[tuple[int, str]] = []
    inline: list[tuple[int, str]] = []
    ref_defs: dict[str, tuple[int, str]] = {}
    ref_uses: dict[str, list[int]] = {}

    fence: str | None = None
    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if fence is None and (stripped.startswith("```") or stripped.startswith("~~~")):
            fence = stripped[:3]
            code.add(i)
            continue
        if fence is not None:
            code.add(i)
            if stripped.startswith(fence):
                fence = None
            continue

        m = HEADING_RE.match(line)
        if m:
            headings.append((i, m.group(2).strip()))

        m = REF_DEF_RE.match(line)
        if m:
            ref_defs.setdefault(m.group(1), (i, m.group(2)))
            continue  # a definition line is not a link use

        # inline code spans hide links and labels
        bare = re.sub(r"`[^`]*`", "", line)
        for lm in INLINE_LINK_RE.finditer(bare):
            inline.append((i, lm.group(1)))
        for um in REF_USE_RE.finditer(bare):
            ref_uses.setdefault(um.group(1), []).append(i)

    return Doc(rel, lines, code, headings, inline, ref_defs, ref_uses)


def slug(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    return re.sub(r"[\s]+", "-", s)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def is_local(target: str) -> bool:
    if not target or target.startswith("#"):
        return False
    p = urlparse(target)
    return not p.scheme and not p.netloc


def split_anchor(target: str) -> tuple[str, str | None]:
    t = target.strip()
    if t.startswith("<") and t.endswith(">"):
        t = t[1:-1]
    if "#" in t:
        path, anchor = t.split("#", 1)
        return unquote(path), anchor
    return unquote(t), None


def rel_of(path: Path) -> str | None:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return None


def bucket(rel: str) -> str:
    return rel.split("/", 1)[0] + "/" if "/" in rel else ""


def markdown_files() -> list[str]:
    out: list[str] = []
    for p in sorted(REPO_ROOT.rglob("*.md")):
        r = rel_of(p)
        if r is None or r.startswith("archives/") or "/.git/" in "/" + r:
            continue
        out.append(r)
    return out


def staged_files() -> list[str]:
    try:
        res = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            capture_output=True, text=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    return [ln for ln in res.stdout.split("\n") if ln.endswith(".md") and not ln.startswith("archives/")]


def owning_moc(rel: str) -> str | None:
    """The MOC that owns the directory a file lives in (projects/ and areas/ only)."""
    if not rel.startswith(("projects/", "areas/")):
        return None
    parts = rel.split("/")
    if len(parts) < 2:
        return None
    owner_dir = REPO_ROOT / parts[0] / parts[1]
    if not owner_dir.is_dir():
        return None
    for cand in sorted(owner_dir.glob("*-moc.md")):
        r = rel_of(cand)
        if r:
            return r
    return None


def last_updated_dates(doc: Doc) -> list[tuple[int, str]]:
    out = []
    for i, line in enumerate(doc.lines, 1):
        if i in doc.code:
            continue
        m = LAST_UPDATED_RE.search(line)
        if m:
            out.append((i, m.group(1)))
    return out


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------
def check_filename_nfc(rel: str, report: Report) -> None:
    if unicodedata.normalize("NFC", rel) != rel:
        report.error("nfc", rel, None,
                     "file name is not NFC-normalized; links to it break on other machines")


def check_links(doc: Doc, report: Report) -> None:
    targets: list[tuple[int, str, str]] = []  # (lineno, raw, kind)
    for lineno, raw in doc.inline:
        targets.append((lineno, raw, "link"))
    for label, (lineno, raw) in doc.ref_defs.items():
        targets.append((lineno, raw, f"definition [{label}]"))

    for lineno, raw, kind in targets:
        path_part, anchor = split_anchor(raw)
        if not is_local(path_part) or not path_part:
            continue
        resolved = (REPO_ROOT / doc.rel).parent / path_part
        r = rel_of(resolved)
        if not resolved.exists():
            report.error("broken-link", doc.rel, lineno, f"{kind} target does not exist: {raw}")
            continue
        if r and r.startswith("archives/") and not doc.rel.startswith("archives/"):
            report.error("archives-ref", doc.rel, lineno,
                         f"live document references archives/: {raw}. Archived material is excluded "
                         "from search on purpose; quoting it reintroduces stale information")
            continue
        if anchor and resolved.suffix == ".md" and r:
            try:
                target_doc = parse_doc(r, resolved.read_text(encoding="utf-8"))
            except OSError:
                continue
            anchors = {slug(h) for _, h in target_doc.headings}
            if slug(unquote(anchor)) not in anchors:
                report.warn("broken-anchor", doc.rel, lineno,
                            f"no heading matches #{anchor} in {r}")


def check_reference_labels(doc: Doc, report: Report) -> None:
    for label, linenos in doc.ref_uses.items():
        if label not in doc.ref_defs:
            report.error("ref-needs-def", doc.rel, linenos[0],
                         f"label [{label}] is used but never defined; it renders as literal text")
    for label, (lineno, _t) in doc.ref_defs.items():
        if label not in doc.ref_uses:
            report.warn("def-unused", doc.rel, lineno,
                        f"link definition [{label}] is not referenced")


def check_link_direction(doc: Doc, report: Report) -> None:
    """Immovable layers must not point at movable ones. The map layer is exempt."""
    if not doc.rel.startswith(IMMOVABLE) or doc.rel.startswith(MAP_LAYER):
        return
    seen: list[tuple[int, str]] = list(doc.inline)
    seen += [(ln, t) for ln, t in doc.ref_defs.values()]
    for lineno, raw in seen:
        path_part, _ = split_anchor(raw)
        if not is_local(path_part) or not path_part:
            continue
        r = rel_of((REPO_ROOT / doc.rel).parent / path_part)
        if r and r.startswith(MOVABLE):
            report.warn("link-direction", doc.rel, lineno,
                        f"stable layer links into a movable one: {r}. Movable files link to stable "
                        "ones, not the other way round, so moving a project cannot break _core")


def check_status_block(doc: Doc, report: Report) -> None:
    if not doc.rel.endswith("-moc.md") or not doc.rel.startswith(("projects/", "areas/")):
        return
    dates = last_updated_dates(doc)
    if not dates:
        if any(PLACEHOLDER_RE.search(ln) for ln in doc.lines):
            return  # the block is there, the date just has not been filled in yet
        report.warn("index-no-status", doc.rel, None,
                    "project/area MOC has no `Last updated: YYYY-MM-DD`; state has no owner")
        return
    head_line, head_date = dates[0]
    newest = max(d for _, d in dates)
    if head_date < newest:
        report.error("meta-date-mismatch", doc.rel, head_line,
                     f"the first `Last updated` ({head_date}) is older than {newest} later in the "
                     "file; the page date must cover every block inside it")


def check_addresses(all_md: list[str], report: Report) -> None:
    seen: dict[str, str] = {}
    for rel in all_md:
        if rel.startswith(("decisions/",)) or "/" not in rel:
            continue
        m = ADDRESS_RE.match(Path(rel).name)
        if not m:
            continue
        addr = f"{m.group(1)}.{m.group(2)}"
        if addr in seen:
            report.error("addr-duplicate", rel, None,
                         f"address {addr} is already used by {seen[addr]}; one address, one file")
        else:
            seen[addr] = rel


def check_tracker_status(targets: list[str], report: Report) -> None:
    for rel in targets:
        if not rel.endswith("-moc.md") or not rel.startswith(("projects/", "areas/")):
            continue
        try:
            doc = parse_doc(rel, (REPO_ROOT / rel).read_text(encoding="utf-8"))
        except OSError:
            continue
        for i, line in enumerate(doc.lines, 1):
            if i in doc.code or re.match(r"\s*- \[[ x]\]", line):
                continue  # the KB's own checkboxes are its state, not the tracker's
            if TRACKER_KEY_RE.search(line) and TRACKER_STATE_RE.search(line):
                report.warn("tracker-status-copied", rel, i,
                            "issue state copied into the MOC. The tracker and git own status, "
                            "assignee, completion date and PR number; a second copy goes stale")


def check_stale_dates(targets: list[str], report: Report) -> None:
    """Only for --staged or explicit paths: touching a project/area should date its MOC."""
    today = _dt.date.today().isoformat()
    by_owner: dict[str, list[str]] = {}
    for rel in targets:
        owner = owning_moc(rel)
        if owner:
            by_owner.setdefault(owner, []).append(rel)
    for owner, changed in sorted(by_owner.items()):
        try:
            doc = parse_doc(owner, (REPO_ROOT / owner).read_text(encoding="utf-8"))
        except OSError:
            continue
        dates = last_updated_dates(doc)
        if dates and dates[0][1] != today:
            names = ", ".join(Path(c).name for c in sorted(changed)[:3])
            more = f" and {len(changed) - 3} more" if len(changed) > 3 else ""
            report.warn("index-stale-date", owner, dates[0][0],
                        f"changed {names}{more} but `Last updated` is {dates[0][1]}, not {today}")


def check_orphans(all_md: list[str], report: Report) -> None:
    """Reachability from the root MOC. Whole-repo runs only."""
    if not (REPO_ROOT / ROOT_MOC).exists():
        return
    reached: set[str] = set()
    queue = [ROOT_MOC]
    while queue:
        rel = queue.pop()
        if rel in reached:
            continue
        reached.add(rel)
        try:
            doc = parse_doc(rel, (REPO_ROOT / rel).read_text(encoding="utf-8"))
        except OSError:
            continue
        outgoing = list(doc.inline) + [(ln, t) for ln, t in doc.ref_defs.values()]
        for _ln, raw in outgoing:
            path_part, _ = split_anchor(raw)
            if not is_local(path_part) or not path_part:
                continue
            r = rel_of((REPO_ROOT / rel).parent / path_part)
            if r and r.endswith(".md") and not r.startswith("archives/"):
                queue.append(r)

    for rel in all_md:
        if rel in reached or rel in GENERATED or Path(rel).name in NOT_LINKED_FROM_MAP:
            continue
        if not rel.startswith(MOVABLE + IMMOVABLE):
            continue
        report.warn("orphan", rel, None,
                    "not reachable from the root MOC; nothing links to it, so nobody will find it")


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------
def run(targets: list[str], all_md: list[str], scoped: bool) -> Report:
    report = Report()
    for rel in targets:
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        check_filename_nfc(rel, report)
        try:
            doc = parse_doc(rel, path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError) as exc:
            report.error("unreadable", rel, None, str(exc))
            continue
        check_links(doc, report)
        check_reference_labels(doc, report)
        check_link_direction(doc, report)
        check_status_block(doc, report)

    check_addresses(all_md, report)
    check_tracker_status(targets, report)
    if scoped:
        check_stale_dates(targets, report)   # noisy on a whole-repo run
    else:
        check_orphans(all_md, report)        # needs the whole graph
    return report


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Structure and link checks for the knowledge base.")
    ap.add_argument("paths", nargs="*", help="files to check (default: every tracked Markdown file)")
    ap.add_argument("--staged", action="store_true", help="check files staged for commit")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args(argv)

    all_md = markdown_files()
    if args.staged:
        targets, scoped = staged_files(), True
    elif args.paths:
        targets, scoped = [], True
        for a in args.paths:
            p = Path(a)
            p = p if p.is_absolute() else (Path.cwd() / p)
            if p.is_dir():
                targets += [r for r in all_md if r.startswith((rel_of(p) or "") + "/")]
            else:
                r = rel_of(p)
                if r:
                    targets.append(r)
    else:
        targets, scoped = all_md, False
    targets = [t for t in dict.fromkeys(targets) if t.endswith(".md") and not t.startswith("archives/")]

    report = run(targets, all_md, scoped)
    errors = [f for f in report.items if f.severity == "error"]
    warnings = [f for f in report.items if f.severity == "warning"]

    for f in sorted(report.items, key=lambda x: (x.severity != "error", x.rel, x.lineno or 0)):
        mark = "ERROR" if f.severity == "error" else "warn "
        where = f"{f.rel}:{f.lineno}" if f.lineno else f.rel
        print(f"{mark} [{f.code}] {where}  {f.message}", file=sys.stderr)

    print(f"kb-lint: {len(targets)} files checked - {len(errors)} errors / {len(warnings)} warnings",
          file=sys.stderr)
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
