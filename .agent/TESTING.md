# Testing

This repository has no reliable local automated test path. Verify Home Assistant YAML and dashboards on `casa` after git sync. Apply Compose changes manually through Portainer; git sync alone does not deploy containers.

## Phases (separate and explicit)
1. **Testing phase**: update/add validation checks first when possible.
2. **Implementation phase**: edit automation/template/dashboard/config files, then execute checks.

## Fast checks
- Validate YAML consistency and changed entities manually before commit.
- Sync `main` to `casa` via `.agent/standards/home-assistant-git-sync.md` for Home Assistant YAML and dashboards.

## Full test suite
- No standalone unit-test suite was detected. Use:
  - Manual validation on `casa`
  - Manual validation in Home Assistant Developer Tools and UI
  - Runtime log inspection for touched integrations/automations

## Coverage
- Not applicable as a numeric coverage pipeline in this repo.
- Minimum expectation: every changed automation/template path must have an explicit manual verification note.

## Test validation (for higher-stakes changes)
- For critical automations (climate/heating/safety), trigger with representative states and times in Developer Tools.
- Confirm expected service calls and resulting entity states.
- Revert test state changes after validation.

## Notes
- Validate dashboard edits by opening affected Lovelace views.
- For dashboard edits, verify card rendering, navigation paths, and entity interactions on each touched view.
- For wallpanel-oriented changes, include at least one wallpanel/tablet usability check.
- For YAML refactors, run a DRY pass using `.agent/standards/home-assistant-yaml-dry.md` and verify no behavior drift.
- For Compose changes, run `docker compose -f <file> config` locally before applying the stack manually through Portainer.
- Complete YAML sanity review locally before pushing changes to `origin/main`.
- Apply Home Assistant YAML and dashboard updates on `casa` through the git sync workflow only (see `.agent/standards/home-assistant-git-sync.md`).
