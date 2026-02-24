# Coding Style

Only include rules not enforced by automatic formatters or linters.

## Linting and formatting
- Compose structure validation:
```bash
docker compose -f compose/home-assistant.yml config
```
- YAML/style validation is primarily human review in this repo; do not assume local runtime validation availability.

## Conventions
- Use snake_case for automation/template filenames and aliases.
- Keep automations split by concern under `automation/` (one primary behavior per file).
- Guard template math/comparisons with `has_value(...)` and safe casts (`| float(0)`).
- Prefer explicit `mode` in automations (existing repo uses `mode: single` frequently).
- Keep dashboard structure modular:
  - `dashboards/*/dashboard.yaml` should include views via `!include_dir_list`.
  - Shared resources stay in `dashboards/resources.yaml`.
- For dashboard composition, prefer card usage in this order:
  - `custom:streamline-card` first
  - `custom:mushroom-*` second
  - built-in HA cards last
- Use `card_mod` sparingly and only when native options/templates are insufficient.
- Keep YAML readable with consistent indentation and compact comments.
- See `.agent/standards/home-assistant-dashboard-design.md` for full dashboard UI rules.

## Examples
- `automation/ac_heat_schedule.yaml` shows trigger-id based `choose` branching.
- `automation/humidity_rise_extractor_bano.yaml` shows safe numeric template comparisons.
- `dashboards/wallpanel/dashboard.yaml` shows include-based dashboard composition.
