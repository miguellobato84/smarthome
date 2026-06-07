#!/usr/bin/env bash

set -euo pipefail

REMOTE_NAME="${REMOTE_NAME:-origin}"
CASA_HOST="${CASA_HOST:-casa}"
CASA_REPO_PATH="${CASA_REPO_PATH:-/docker/homeassistant-bind}"

main() {
  local branch
  branch="$(git branch --show-current)"

  if [[ -z "$branch" ]]; then
    echo "Error: could not detect current branch." >&2
    exit 1
  fi

  if [[ -n "$(git status --porcelain)" ]]; then
    echo "Error: local repository has uncommitted changes. Commit or stash them first." >&2
    exit 1
  fi

  ensure_local_branch_pushed "$branch"
  sync_casa_branch "$branch"
}

ensure_local_branch_pushed() {
  local branch="$1"

  if git rev-parse --abbrev-ref "${branch}@{upstream}" >/dev/null 2>&1; then
    git push "$REMOTE_NAME" "$branch"
  else
    git push -u "$REMOTE_NAME" "$branch"
  fi
}

sync_casa_branch() {
  local branch="$1"
  local remote_script

  read -r -d '' remote_script <<'EOF' || true
set -euo pipefail

branch="$1"
remote_name="$2"
repo_path="$3"

cd "$repo_path"
git fetch "$remote_name"

if git show-ref --verify --quiet "refs/heads/$branch"; then
  git checkout "$branch"
else
  git checkout -b "$branch" --track "$remote_name/$branch"
fi

if [[ -n "$(git status --porcelain)" ]]; then
  commit_msg="Sync casa local changes into ${branch} on $(date '+%Y-%m-%d %H:%M:%S %Z')"
  git add -A
  git commit --no-gpg-sign -m "$commit_msg"
  git push "$remote_name" "$branch"
fi

git pull --ff-only "$remote_name" "$branch"
git status -sb
git rev-parse --short HEAD
EOF

  ssh "$CASA_HOST" "bash -s -- $(printf '%q' "$branch") $(printf '%q' "$REMOTE_NAME") $(printf '%q' "$CASA_REPO_PATH")" <<<"$remote_script"
}

main "$@"
