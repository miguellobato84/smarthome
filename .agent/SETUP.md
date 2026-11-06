# Local Setup

## Requirements
- Docker Engine with Compose support
- Running `homeassistant` container from `compose/home-assistant.yml`
- Access to host paths mounted in compose files (for example `/docker/*`)

## Environment
- Configure environment variables referenced by compose files (for example `CLOUDFLARE_TOKEN`).
- Keep secrets out of git-tracked files.
- Preserve timezone and network settings expected by the stacks (`Europe/Madrid`, external `homeassistant` network).

## Setup Steps
1. Start Home Assistant stack:
```bash
docker compose -f compose/home-assistant.yml up -d
```
2. Start optional supporting stacks as needed:
```bash
docker compose -f compose/system-management.yml up -d
docker compose -f compose/media.yml up -d
docker compose -f compose/ai.yml up -d
```
3. Confirm core container status:
```bash
docker ps --filter name=homeassistant
```

## Git-only sync workflow (`local` <-> `casa`)
- Local host is the source of truth for edits.
- Move changes to `casa` only via git (no manual file copy, no ad-hoc SSH edits).
- Use `main` as the working and deployment branch.

1. Edit and commit changes locally on `main`, then push:
```bash
git add <files>
git commit --no-gpg-sign -m "<message>"
git push origin main
```

2. Sync `main` on `casa` using SSH for git operations only:
```bash
ssh casa 'cd /docker/homeassistant-bind && git status -sb'
ssh casa 'cd /docker/homeassistant-bind && git checkout main'
```

3. If `casa` has local pending changes, commit them on `main` before pulling:
```bash
ssh casa 'cd /docker/homeassistant-bind && git add -A && git commit --no-gpg-sign -m "<message>"'
```

4. Pull `main` on `casa`:
```bash
ssh casa 'cd /docker/homeassistant-bind && git pull --ff-only origin main'
```

5. For Compose changes, apply the updated stack manually through Portainer. Git sync alone does not recreate or start containers.
6. For Home Assistant YAML and dashboard changes, follow `.agent/standards/home-assistant-git-sync.md` for API validation, reload, and runtime checks.

## Troubleshooting
- Config does not load: verify the latest synced branch on `casa`, then inspect Home Assistant logs and integration states from the UI.
- Dashboard cards missing: verify `dashboards/resources.yaml` entries and installed HACS resources.
- Integration-side failures: inspect related container logs (for example `zigbee2mqtt`, `mqtt`, `cloudflare`).
