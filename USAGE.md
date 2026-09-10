# Telos Usage

Telos is the local-first Project Telos integration workbench. It exposes the
five flagship tools, compatibility doctors, context receipts, creative-engine
lanes, model-foundry lanes, and MCP host manifests through runnable demo
surfaces.

## Install

```bash
npm install
```

Telos currently targets Node 20 or newer.

## Run

For native browser/app/device control, read the [target and focus contract](docs/native-control-contract.md).
Explicit browser matches must select one page. Omitted matches retain raw CLI
first-page selection, which is not authorization. Focus receipts can be unknown;
UIA focus/input verbs can affect the foreground window. The MCP native-control
tool returns a catalog only.

```bash
npm start
npm run catalog
npm run manifest
node demo/status.mjs --summary
node demo/doctor.mjs --summary
```

## MCP

Run the stdio MCP server with:

```bash
npm run mcp
```

Useful host-facing checks:

```bash
node demo/server-manifest.mjs --summary
node demo/mcp-freshness.mjs --observed observed.json
node demo/compatibility-doctor.mjs --summary
node demo/operator-doctor.mjs --summary
```

## Verify

```bash
npm run test:mcp
npm run catalog
npm run manifest
node demo/presentation-doctor.mjs --summary
node demo/accessibility-doctor.mjs --summary
node demo/performance-doctor.mjs --summary
```

For public/developer delivery checks:

```bash
python -m public_surface_sweeper . --workspace --json
```

## Boundary

Telos should expose runnable receipts, tool manifests, compatibility verdicts,
host references, and local artifact paths. Do not publish secrets, private
payloads, raw evidence, or operator-owned licensed font files.
