---
name: home-assistant-mcp
description: Validate and troubleshoot Home Assistant MCP server connectivity, authentication, and JSON-RPC handshake for this repository's Home Assistant instance. Use when requests involve checking whether MCP is up, confirming /api/mcp behavior, testing tokens, or diagnosing MCP client connection failures.
---

# Home Assistant MCP Skill

## Endpoint and auth
- Use MCP endpoint: `https://casa.miguellobato.com/api/mcp`
- Read token from local env var: `HA_MCP_TOKEN`
- If the env var is unset, fetch it from 1Password item `HomeAssistant` in the `Employee` vault with:
  `export HA_MCP_TOKEN="$(op item get \"HomeAssistant\" --vault Employee --reveal --field password)"`
- Never write tokens to tracked files, logs, or commits.

## Validation workflow
1. Confirm base Home Assistant API access.
2. Confirm MCP route behavior.
3. Confirm JSON-RPC initialize handshake over POST.
4. Report status and likely fix path.

## Commands
```bash
BASE='https://casa.miguellobato.com'
TOKEN="$HA_MCP_TOKEN"

# 1) Base API health/auth
curl -sS -D - -o /tmp/ha_api_body.txt \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE/api/"

# 2) MCP route probe (GET should usually return 405: POST only)
curl -sS -D - -o /tmp/ha_mcp_get_body.txt \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE/api/mcp"

# 3) MCP initialize handshake (must be POST)
curl -sS -D - -o /tmp/ha_mcp_post_body.txt \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -X POST "$BASE/api/mcp" \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"codex-cli","version":"1.0.0"},"capabilities":{}}}'
```

## Result interpretation
- `GET /api/ -> 200` and `POST /api/mcp initialize -> 200`: MCP is operational.
- `/api/mcp -> 404`: MCP server integration not enabled in Home Assistant.
- `/api/mcp -> 401` or `403`: token invalid or missing permissions.
- `GET /api/mcp -> 405`: expected when endpoint is active and POST-only.

## Optional component check
Use `/api/config` and verify `mcp_server` appears in `components`.
