# Standard: Home Assistant Git Sync Flow

## Principles
- Local repository is the source of truth for Home Assistant config edits.
- Configuration transfer between local and `casa` must happen via git only.
- Use `main` as the working and deployment branch.

## Rules
- Do all file edits locally on `main`, then commit to `main`.
- In iterative sessions, do one commit per completed user-requested change set and push that commit immediately.
- Push `main` to `origin` before syncing on `casa`.
- Do not accumulate multiple finished requests locally without push, unless the user explicitly asks for batching.
- Use `ssh casa` only for git operations unless explicitly requested otherwise.
- On `casa`, if there are local pending changes, commit them on `main` before pulling.
- Use `--no-gpg-sign` for commits in this environment.
- Pull `main` with fast-forward only:
  - `git pull --ff-only origin main`

## Command pattern
1. Local, on `main`:
```bash
git add <files>
git commit --no-gpg-sign -m "<message>"
git push origin main
```
2. `casa` sync:
```bash
ssh casa 'cd /docker/homeassistant-bind && git status -sb'
ssh casa 'cd /docker/homeassistant-bind && git checkout main'
ssh casa 'cd /docker/homeassistant-bind && git add -A && git commit --no-gpg-sign -m "<message>"'
ssh casa 'cd /docker/homeassistant-bind && git pull --ff-only origin main'
```

3. Validate and apply through the API after every successful sync, including syncs
   to `main`. `./sync.sh` handles Git transfer only; the agent must complete these
   steps locally using the API and token rules in `AGENTS.md`:
   - `POST /api/config/core/check_config` with `{}`. Continue only on HTTP `200`
     with `result: valid`; report errors and stop before reloading otherwise.
   - `POST /api/services/homeassistant/reload_all` with `{}`. Require HTTP `200`;
     report API failures rather than treating Git sync as a completed deployment.
   - `GET /api/` must return HTTP `200`. Verify affected automation/script entities
     and live dashboard configuration when relevant. Report validation warnings
     and any behavior or visual checks that could not be performed.

This quick reload applies supported YAML configuration without restarting Home
Assistant. If a change requires a restart, report that requirement separately;
the sync step authorizes the quick reload, not a full restart.

## Validation
- `git status -sb` is clean locally after push.
- `ssh casa 'cd /docker/homeassistant-bind && git status -sb'` shows expected branch/state after sync.
- Local and `casa` are on `main` at the expected commit.
- API validation, quick reload, and health verification succeeded after sync;
  affected runtime configuration matches the deployed change.
