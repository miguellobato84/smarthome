# SmartHome Configuration

This repository contains Home Assistant configuration and related infrastructure for the smart home setup.

## Repository structure
- `configuration.yaml`: main Home Assistant configuration entrypoint.
- `automations.yaml`: Home Assistant automation include file (routes into `automation/`).
- `automation/`: automation definitions split by behavior.
- `scripts/`: Home Assistant scripts split into one file per script.
- `scenes/`: Home Assistant scenes split into one file per scene.
- `templates/`: template entities, helpers, and integration settings.
- `dashboards/`: Lovelace YAML dashboards and views.
- `compose/`: Docker Compose stacks for Home Assistant and related services.
- `www/`: static assets served by Home Assistant.
- `.agent/`: Codex project guidance and standards.

## How configuration is wired
- `configuration.yaml` includes:
  - `automation: !include_dir_merge_list automation`
  - `script: !include_dir_merge_named scripts`
  - `scene: !include_dir_merge_list scenes`
  - template and dashboard include files/directories

## Directory documentation
Each project directory contains a local `README.md` describing its purpose and files.

## Host mount layout (casa)
- Source config directory on host: `/docker/homeassistant`
- Home Assistant container `/config` mount source: `/docker/homeassistant-bind`
- `/docker/homeassistant-bind` is provided by `bindfs` from `/docker/homeassistant`
- Persistent mount service: `homeassistant-bindfs.service` (systemd, enabled at boot)
- Why: keep writable/non-root ownership behavior for day-to-day edits while preserving host layout.
