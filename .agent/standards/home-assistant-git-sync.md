# Standard: Home Assistant Git Sync Flow

## Principles
- Local repository is the source of truth for Home Assistant config edits.
- Configuration transfer between local and `casa` must happen via git only.
- Keep branch history clean and avoid direct `main` pushes.

## Rules
- Do all file edits locally, then commit to a non-`main` branch.
- Push local branch to origin before syncing on `casa`.
- Use `ssh casa` only for git operations unless explicitly requested otherwise.
- On `casa`, if there are local pending changes, commit them on the same branch before pulling.
- Pull with fast-forward only:
  - `git pull --ff-only origin <feature-branch>`
- Merge to `main` only after feature completion and review.

## Command pattern
1. Local:
```bash
git checkout -b <feature-branch>
git add <files>
git commit -m "<message>"
git push -u origin <feature-branch>
```
2. `casa` sync:
```bash
ssh casa 'cd /docker/homeassistant-bind && git status -sb'
ssh casa 'cd /docker/homeassistant-bind && git checkout <feature-branch>'
ssh casa 'cd /docker/homeassistant-bind && git add -A && git commit -m "<message>"'
ssh casa 'cd /docker/homeassistant-bind && git pull --ff-only origin <feature-branch>'
```

## Validation
- `git status -sb` is clean locally before final push.
- `ssh casa 'cd /docker/homeassistant-bind && git status -sb'` shows expected branch/state after sync.
- No direct push to `main` occurred for feature work.
