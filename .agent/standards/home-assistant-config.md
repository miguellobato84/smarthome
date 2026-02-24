# Standard: Home Assistant YAML Patterns

## Principles
- Keep behavior explicit and traceable from file name to entity/automation alias.
- Prefer safe templates that handle unavailable states.
- Keep dashboard and automation structure modular for maintainability.

## Repo-specific rules
- Place automation definitions in `automation/` as split files, grouped by concern.
- Use snake_case names for automation files and aliases.
- Prefer explicit trigger ids and `choose` blocks when one automation handles multiple paths.
- Guard template conditions with `has_value(...)` and numeric defaults (for example `| float(0)`).
- Keep reusable/static definitions in dedicated files:
  - `templates/*.yaml` for helper entities/integration config
  - `scripts.yaml` for scripts
  - `scenes.yaml` for scenes
- Keep Lovelace in YAML mode:
  - Use `dashboards/*/dashboard.yaml` with `!include_dir_list` for view splitting.
  - Register frontend resources in `dashboards/resources.yaml`.
- Preserve existing language/wording style in entity labels and descriptions unless change is requested.

## Examples
- `automation/ac_heat_schedule.yaml` uses template triggers with ids (`heat_on`, `heat_off`) and a `choose` action.
- `automation/humidity_rise_extractor_bano.yaml` compares current humidity against a rolling average with safe casting.
- `dashboards/wallpanel/dashboard.yaml` delegates views to `dashboards/wallpanel/views/`.

## Validation
- Sync changes to `casa` using `.agent/standards/home-assistant-git-sync.md`.
- Verify affected entities/automations in Developer Tools.
- Open affected dashboard views and confirm custom cards load correctly.
- For dashboard card/layout decisions, also apply `.agent/standards/home-assistant-dashboard-design.md`.
- For duplicate logic cleanup, also apply `.agent/standards/home-assistant-yaml-dry.md`.
