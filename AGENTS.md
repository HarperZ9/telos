# Telos Agent Instructions

## Scope

Telos is the Project Telos workbench and flagship integration surface. Changes
should improve the shared room across gather, crucible, index, forum, creative
engine lanes, model-foundry lanes, compatibility receipts, and host-agnostic MCP
integration.

## Developer Contract

- Keep demo scripts, MCP tools, README claims, and changelog entries aligned.
- Preserve receipt shapes for status, doctor, catalog, compatibility, context,
  action, loop-ledger, rendering, model-foundry, and creative-engine surfaces.
- Prefer local-first references, hashes, verdicts, and host manifests over raw
  private payloads.
- Keep README, `USAGE.md`, `CHANGELOG.md`, and operator docs current when demo
  commands or tool names change.

## Verification

Run the targeted slice for the touched surface first:

```bash
npm run test:mcp
npm run catalog
npm run manifest
npm run mcp
```

For delivery-surface changes, also run:

```bash
python -m public_surface_sweeper . --workspace --json
```
