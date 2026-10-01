# Telos Usage

## Bounded Index compatibility probe

From the extracted Telos package or source directory, create a new synthetic
workspace in a directory whose parent already exists:

```sh
node demo/compat-fixture.mjs /absolute/path/to/new-compat-workspace
```

The helper refuses an existing target and prints PROJECT_TELOS_COMPAT_FIXTURE.
Replace that placeholder in the Index freshness probe arguments with the printed
path before calling the connected Index server. The fixture contains one tiny
repository named index and a repository marker; it has no commit history or real
user data. The probe requires bounded output, a 4,000-token budget, MATCH and no
omissions or failure codes. It tests the selection/freshness protocol on this
fixture. Full-repository budget fitness needs its own measurement. The source
integration test also rejects a real-workspace 700-token overflow and stale-source
freshness.

With the declared sibling checkouts beside the telos directory, run:

```sh
node --test demo/sibling-behavior.test.mjs
```

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

For native browser/app/device control, read the [target, focus and evidence contract](docs/native-control-contract.md).
Explicit browser matches must select one page. Omitted matches retain raw CLI
first-page selection, which is not authorization. Focus receipts can be unknown;
UIA focus/input verbs can affect the foreground window. The MCP native-control
tool returns a catalog only.

Browser evidence retains source URLs, titles and supplied context, so packets
are marked `unredacted` and should remain in private storage. Ledger verification
checks unsigned hash consistency; legacy step/result-only chains are labeled
with that limited scope. Neither check establishes task completion.

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

## Local client packages

See [the client package guide](client-plugin/README.md) for scoped skills, portable MCP configuration and same-release archives.

The current source candidate targets 0.5.0. Registry install examples above
continue to name the published baseline until release qualification finishes.
