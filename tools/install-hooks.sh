#!/usr/bin/env sh
set -eu

repo_root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
hook_path="$repo_root/.git/hooks/pre-commit"

if [ ! -d "$repo_root/.git" ]; then
  echo "This repository is not initialized with git yet." >&2
  exit 1
fi

cat > "$hook_path" <<'HOOK'
#!/usr/bin/env sh
set -eu

python3 tools/kb-lint.py --staged
python3 tools/kb-tasks.py --write

if ! git diff --quiet -- _core/00-09_index/00.02-tasks.md; then
  git add _core/00-09_index/00.02-tasks.md
fi
HOOK

chmod +x "$hook_path"
echo "Installed pre-commit hook: $hook_path"
