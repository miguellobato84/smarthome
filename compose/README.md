# Compose Stacks

This folder defines Docker Compose stacks used by the smart home environment.

## Files
- `home-assistant.yml`: core Home Assistant, MQTT, Zigbee2MQTT, proxy, and tunnel services.
- `system-management.yml`: management and utility services (VS Code server, watchtower, backups, etc.).
- `media.yml`: media-related service stack.
- `ai.yml`: AI-related service stack.
- `portainer.yml`: Portainer stack definition.
- `index.html`: static page used by reverse proxy/site entry.
