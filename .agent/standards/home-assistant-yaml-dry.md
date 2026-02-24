# Standard: Home Assistant YAML DRY Verification

## Principles
- Remove duplicated YAML logic when it appears across automations, scripts, templates, or dashboards.
- Prioritize high-impact duplicates first (full blocks before small entries).
- Keep behavior identical while reducing maintenance overhead.

## Duplicate classes and priority
- Apply this priority order when analyzing duplication:
  1. `FULL_BLOCK`: duplicate full trigger/condition/action/sequence blocks
  2. `ENTRY`: duplicate list entries (single action, condition, trigger item)
  3. `INTRA`: repeated fragments inside one file/section
- Refactor the highest-level duplicate first when multiple classes overlap.

## Refactor targets in this repo
- Convert repeated action/condition groups into reusable scripts where appropriate.
- Consolidate repeated template expressions into shared template sensors/helpers when practical.
- Reuse dashboard card templates (for example streamline templates) instead of copy-paste variants.
- Keep file split-by-concern structure (`automation/`, `templates/`, `dashboards/`) after refactor.

## Workflow
1. Identify duplicate blocks and classify each finding (`FULL_BLOCK`/`ENTRY`/`INTRA`).
2. Record impacted files and entity IDs.
3. Propose minimal refactor preserving behavior.
4. Apply refactor and sync branch to `casa` for verification.
5. Manually verify impacted automations/views.

## Validation
- Changes are synced to `casa` via `.agent/standards/home-assistant-git-sync.md`.
- Refactor did not change behavior of affected entities/services.
- Dashboard/UI still renders and interactions work where templates/cards were consolidated.
