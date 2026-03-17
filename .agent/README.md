# Agentic Coding Guide

This folder contains short, task-focused docs used by Codex in this repository.

## Documents
- `PLANS.md` - execution plan template and usage rules
- `SETUP.md` - local environment and run commands
- `TESTING.md` - config validation and runtime verification
- `CODING_STYLE.md` - YAML and structure conventions not auto-enforced
- `ARCHITECTURE.md` - boundaries and data flow
- `GLOSSARY.md` - internal terms and acronyms
- `standards/` - scoped standards used by this repo

## How to use
- Start with `AGENTS.md` at repo root.
- Open relevant `.agent/` docs based on the task.
- Load only the standards needed for the change from `standards/index.yml`.
- Follow `standards/commits.md` before creating commits.
- For Home Assistant sync/deploy flow, follow `standards/home-assistant-git-sync.md`.
- For Lovelace/UI work, follow `standards/home-assistant-dashboard-design.md`.
- When editing any file under `dashboards/*/views/`, also update the matching `dashboards/*/dashboard.yaml` timestamp comment in the same commit.
- For YAML duplication cleanup/refactors, follow `standards/home-assistant-yaml-dry.md`.
