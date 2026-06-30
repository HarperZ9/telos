# Display Calibration Contract Design

## Goal

Promote Calibrate Pro from the Telos revival registry into a first-class, read-only Telos display-calibration contract that can be consumed through CLI JSON, MCP, IDEs, TUIs, apps, and Crucible measurement gates.

## Design

The first increment is a contract, not a live hardware controller. `project-telos.display-calibration/v1` will describe calibration targets, color-science dependencies, patch sets, expected artifacts, measurement gates, provenance receipts, and safety boundaries. It will cite Calibrate Pro and Quanta Color README digests from Gather, but it will not call DDC/CI, mutate monitor OSD settings, apply LUTs, write ICC profiles, or require raw private assets.

The runtime surface follows the existing Telos pattern:

- `demo/integrations/display-calibration.json` is the host-neutral contract.
- `demo/display-calibration.mjs` prints JSON by default and a compact operator summary with `--summary`.
- `telos.display.calibration` exposes the same payload through the Telos MCP server.
- The shared MCP catalog and server manifest count this as another available Telos tool.

## Data Flow

1. Gather records local source receipts for Calibrate Pro and Quanta Color.
2. The display-calibration contract references those receipts by path and SHA-256.
3. Hosts consume the contract to understand targets, patch sets, color spaces, and artifact refs.
4. Crucible receives measurement packets later and owns `MATCH`, `DRIFT`, or `UNVERIFIABLE` verdicts.

## Boundaries

- This pass is read-only and reversible by construction.
- Interop uses hashes, source refs, target specs, artifact refs, and redacted report refs.
- Raw prompts, private assets, device telemetry, live monitor controls, and generated ICC/LUT payloads are not required for interop.
- Any future live monitor mutation must be a separate local operator action with restore metadata and receipt checks.

## Success Criteria

- Tests prove the new contract exists, names Calibrate Pro and Quanta Color, includes display targets, patch sets, artifact outputs, privacy boundaries, and Crucible measurement gates.
- The CLI and MCP outputs exactly match the JSON contract.
- Telos status, catalog, server manifest, README, integration README, and changelog describe the new `telos.display.calibration` surface.
- The Telos tool count advances from 45 to 46 without breaking the existing operator tests.
