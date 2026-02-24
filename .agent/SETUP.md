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
- Never push directly to `main`.

1. Create/use a feature branch locally, commit, and push:
```bash
git checkout -b <feature-branch>
git add <files>
git commit --no-gpg-sign -m "<message>"
git push -u origin <feature-branch>
```

2. Sync branch on `casa` using SSH for git operations only:
```bash
ssh casa 'cd /docker/homeassistant-bind && git status -sb'
ssh casa 'cd /docker/homeassistant-bind && git checkout <feature-branch>'
```

3. If `casa` has local pending changes, commit them on the same branch before pulling:
```bash
ssh casa 'cd /docker/homeassistant-bind && git add -A && git commit --no-gpg-sign -m "<message>"'
```

4. Pull branch updates on `casa`:
```bash
ssh casa 'cd /docker/homeassistant-bind && git pull --ff-only origin <feature-branch>'
```

5. Merge to `main` only after the feature is complete and reviewed.

## Troubleshooting
- Config does not load: verify the latest synced branch on `casa`, then inspect Home Assistant logs and integration states from the UI.
- Dashboard cards missing: verify `dashboards/resources.yaml` entries and installed HACS resources.
- Integration-side failures: inspect related container logs (for example `zigbee2mqtt`, `mqtt`, `cloudflare`).
