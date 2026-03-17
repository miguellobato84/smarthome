# Standard: Home Assistant Dashboard Design

## Principles
- Keep dashboards readable, fast to scan, and easy to interact with on wallpanel/tablet form factors.
- Reuse existing card patterns before introducing new visual patterns.
- Prefer maintainable YAML and template-driven composition over one-off styling.

## Card selection priority
- Prefer cards in this order unless there is a clear reason not to:
  1. `custom:streamline-card`
  2. `custom:mushroom-*` cards
  3. Built-in Home Assistant cards
- Use `card_mod` only when native card options or shared templates cannot solve the requirement.
- If you add new custom card dependencies, document them in `dashboards/resources.yaml`.

## Layout and structure rules
- Keep dashboards split by concern:
  - `dashboards/<dashboard>/dashboard.yaml` as entrypoint
  - `dashboards/<dashboard>/views/*.yaml` per view
- Keep sections compact and consistent:
  - Prefer 3-4 cards per row/section on wallpanel-oriented views.
  - Keep navigation cards and "back" actions visually consistent across views.
- For `picture-elements` views:
  - Use percentage-based positions for element placement.
  - Keep tappable elements large and uncluttered.
  - Avoid adding dense overlays that reduce usability.

## Template and naming discipline
- Reuse existing streamline templates before creating new card variants.
- Keep card `primary`/`secondary` text concise and action-oriented.
- Preserve repo language conventions in labels unless a change is requested.
- Keep entity references stable and explicit (`entity:` on interactive cards).

## Validation
- If you modify any file under `dashboards/*/views/*.yaml`, also update the matching `dashboards/*/dashboard.yaml` timestamp comment in the same change.
- Treat that timestamp comment update as required even for small follow-up UI fixes; do not defer it to a later commit.
- Sync dashboard changes to `casa` using `.agent/standards/home-assistant-git-sync.md`.
- Open every modified view and verify:
  - cards render without "Custom element doesn't exist" errors
  - navigation paths resolve correctly
  - interactive controls call the expected entity/service
- Verify modified dashboard behavior on target device class (wallpanel/tablet if applicable).
