# Repository Guidelines

## Purpose
This repository stores Home Assistant configuration, automations, templates, dashboards, and supporting Docker Compose stacks for the home environment. Keep this file short and use the `.agent/` docs for operational details and repo conventions.

## Project overview
- What this repo does: manages Home Assistant behavior and related self-hosted services as code.
- Demo reference project for examples and good practices: `/Users/miguel.lobato/projects/others/Home-AssistantConfig`.
- Key components:
  - Home Assistant core config (`configuration.yaml`, `automation/`, `templates/`, `scripts.yaml`, `scenes.yaml`)
  - Lovelace dashboards in YAML (`dashboards/`)
  - Supporting infrastructure stacks (`compose/`)
  - Root Home Assistant state/action definitions (`scripts.yaml`, `scenes.yaml`)
- Critical flows:
  - Entity state changes and schedules trigger automations that call Home Assistant services.
  - Dashboard YAML plus HACS resources render the UI and control flows.
  - Details: see `.agent/ARCHITECTURE.md`.

## Safety and boundaries
- Never run destructive Docker, filesystem, or git commands without explicit approval.
- Never commit secrets or credentials (for example `SERVICE_ACCOUNT.json`, tokens, passwords).
- Keep changes scoped to requested behavior; avoid broad refactors unless asked.
- Transfer Home Assistant config between local and `casa` via git only.
- Never push directly to `main`; use a feature branch and merge when complete.
- Use `ssh casa` only for git operations unless explicitly requested otherwise.

## Home Assistant MCP
- MCP endpoint for this environment: `https://casa.miguellobato.com/api/mcp`
- Never store MCP bearer tokens in repository files; use local env vars (for example `HA_MCP_TOKEN`).
- For MCP checks, always validate:
  - Base API health: `GET /api/` with bearer token.
  - MCP handshake: `POST /api/mcp` with JSON-RPC `initialize`.
- Interpretation:
  - `200` on initialize = MCP server reachable and working.
  - `404` on `/api/mcp` = MCP server integration not enabled.
  - `401`/`403` = auth/permissions issue.

## Project Structure & Module Organization
- Source code: Home Assistant YAML at repository root and `automation/`, `templates/`, `dashboards/` (details: `.agent/ARCHITECTURE.md`)
- Tests: config validation and runtime checks (details: `.agent/TESTING.md`)
- Configuration: `configuration.yaml`, `compose/*.yml`
- CI/CD: not detected in-repo

## Build, Test, and Development Commands
- Build/Run: `docker compose -f compose/home-assistant.yml up -d` (details: `.agent/SETUP.md`)
- Test: no reliable local automated test command; validate after git sync on `casa` via manual human checks (details: `.agent/TESTING.md`)
- Lint/Style checks: YAML-focused review commands in `.agent/CODING_STYLE.md`
- Docs index: `.agent/README.md`

## Coding Style & Naming Conventions
- Style/lint tools: YAML syntax/shape checks and human review workflow (details: `.agent/CODING_STYLE.md`)
- Naming patterns: snake_case YAML filenames, automation aliases aligned to file purpose.
- Formatting rules not covered by tools: `.agent/CODING_STYLE.md`
- Dashboard UI/design rules: `.agent/standards/home-assistant-dashboard-design.md`
- YAML duplication/refactor rules: `.agent/standards/home-assistant-yaml-dry.md`

## Testing Guidelines
- Validation strategy: manual human verification on `casa` after git sync.
- How to run: `.agent/TESTING.md`
- Coverage expectations: verify changed automations/templates from Developer Tools and related dashboard cards.

## Commit & Pull Request Guidelines
- Commit conventions: see `.agent/standards/commits.md`
- In this repo environment, use unsigned commits (`--no-gpg-sign`) unless told otherwise.
- PR expectations: include behavior summary, impacted entities, and validation steps.
- Home Assistant git-sync workflow: see `.agent/standards/home-assistant-git-sync.md`

## Review expectations
- Run or document relevant checks for touched files.
- Summarize behavior changes and list manual verification steps.
- Call out high-risk areas explicitly (automations, climate/heating controls, external integrations).

## Planning trigger
- Use a plan for complex new features, complex refactors, or high-risk behavior changes.
- If you think you might need a plan, read `.agent/PLANS.md` for structure, storage, and commit policy.

## Deeper docs
- `.agent/README.md` - index of all agent docs
- `.agent/SETUP.md` - local setup and environment
- `.agent/TESTING.md` - test commands and expectations
- `.agent/CODING_STYLE.md` - style rules not enforced by tools
- `.agent/ARCHITECTURE.md` - system boundaries and data flow
- `.agent/GLOSSARY.md` - internal terms and acronyms

## Standards
- Load standards from `.agent/standards/index.yml` based on the task.
- When modifying any dashboard view file under `dashboards/*/views/*.yaml`, also update the matching `dashboards/*/dashboard.yaml` with a timestamp comment to ensure the dashboard change is picked up during sync/reload.

## Maintenance
- After large changes, review `AGENTS.md` and all `.agent/` docs (including standards) to keep them current.
- If updates seem necessary, ask whether to update these docs as part of the same change.

## Skills
- home-assistant-mcp: validate and troubleshoot Home Assistant MCP endpoint/auth behavior for this repo. (file: `.agent/skills/home-assistant-mcp/SKILL.md`)
