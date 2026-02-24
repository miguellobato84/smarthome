# Architecture Overview

Keep this file focused on structure and data flow. Product summary lives in `AGENTS.md`.

## System boundaries
- `configuration.yaml` wires all Home Assistant includes and global options.
- `automation/` contains event/time/state-driven behavior.
- `templates/` defines entities and integration-specific config (for example Google Assistant exposure, helper entities, sensors).
- `scripts.yaml` and `scenes.yaml` provide reusable actions and scene state bundles.
- `dashboards/` defines Lovelace UI in YAML, split by dashboard and views.
- `compose/` runs Home Assistant and adjacent infrastructure services.
- `www/community/` holds frontend assets from HACS/custom cards.

## Data flow (high level)
1. Device/integration state updates -> template sensors/helpers -> automation triggers -> Home Assistant service actions (`switch.turn_on`, `climate.set_hvac_mode`, etc.).
2. User interaction in Lovelace dashboards -> card actions/navigation -> entity/service operations.
3. External services (MQTT, Zigbee2MQTT, proxy/tunnel) -> Home Assistant integrations -> entities consumed by automations and dashboards.

## Key dependencies
- Home Assistant core (`ghcr.io/home-assistant/home-assistant:stable`) is the execution engine.
- MQTT + Zigbee2MQTT provide messaging/device control for Zigbee entities.
- HACS card resources (`mushroom`, `card-mod`, `wallpanel`, `streamline-card`) are required for dashboard rendering.
- Nginx Proxy Manager and Cloudflare tunnel expose remote access paths.

## Risk areas
- Automations that affect heating/climate or always-on switches.
- Template conditions that can fail with `unknown`/`unavailable` states.
- Dashboard changes that depend on custom card resources or entity naming consistency.
- Compose-level changes impacting network bindings, credentials, or persistent volumes.
