# Spec: Rendering Research Contract

## Objective

Add a receipt-backed Telos research packet for clustered forward rendering and Gaussian splatting. The packet turns the operator's rendering direction into current, lawful, source-backed implementation guidance for the Telos Studio and future UI/rendering surfaces.

## Requirements

- [x] Keep the existing fundamental physics research seed unchanged.
- [x] Add a separate `telos.rendering.research` CLI and MCP surface.
- [x] Record Gaussian splatting, clustered forward rendering, WebGPU/WGSL, SuperSplat, and current browser-splat performance work as lawful source receipts.
- [x] Preserve Reddit and shadow-library style references only as non-evidentiary source leads.
- [x] Make beauty and usability explicit acceptance gates alongside performance, accessibility, compatibility, and provenance.
- [x] Update catalog, server manifest, status, README, changelog, and tests.

## Technical Approach

Create `demo/research/rendering-pipeline-seeds.json` using the existing `project-telos.research-seed/v1` shape. Add `demo/rendering-research.mjs` to return the packet. Expose it through `demo/telos-mcp.mjs` as `telos.rendering.research`, then mirror the tool in the provider-neutral catalog and server manifest.

## Files To Modify

- `demo/research/rendering-pipeline-seeds.json` - new packet.
- `demo/rendering-research.mjs` - new CLI reader.
- `demo/rendering-research.test.mjs` - new contract test.
- `demo/telos-mcp.mjs` and tests - MCP exposure.
- `demo/integrations/mcp-tool-catalog.json` and `mcp-server-manifest.json` - host integration surface.
- `demo/status.mjs`, `README.md`, `CHANGELOG.md`, and `demo/integrations/README.md` - forward-facing presentation.

## Success Criteria

- [x] `node demo/rendering-research.test.mjs` passes.
- [x] Telos MCP lists and runs `telos.rendering.research`.
- [x] Catalog and server manifest summaries report 30 total tools.
- [x] Full Telos demo gate passes.
- [x] No source claim relies on Reddit, Sci-Hub, shadow libraries, or unverified social posts as provenance.

## Verification

- `PASS`: `node demo\rendering-research.test.mjs`
- `PASS`: `node demo\telos-mcp.test.mjs`
- `PASS`: `node demo\operator-scripts.test.mjs`
- `PASS`: `node demo\server-manifest.test.mjs`
- `PASS`: `node demo\integrations.test.mjs`
- `PASS`: `node demo\mcp-runtime-contract.test.mjs`
- `PASS`: `node demo\run.mjs`
- `PASS`: `node demo\flagship-workflow.mjs`
- `PASS`: lawful source HEAD checks returned HTTP 200 for arXiv, Inria, PlayCanvas/SuperSplat, Eurographics, GPUWeb, and W3C WGSL references.
- `PASS`: stale-language, secret-shaped, provenance-boundary, and `git diff --check` scans passed.

## Status: IMPLEMENTED
