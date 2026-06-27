# Changelog

All notable changes to Project Telos. Telos is currently a source demo and shared operator room rather than a packaged Python or npm release.

## Unreleased

- OSS Proof Showcase: adds a fixture-first candidate scout, PR-readiness packet
  contract, read-only Telos MCP scout tool, and an optional live GitHub smoke
  command for high-star public issue discovery.
- Feedback integration: adds plain-language operator copy, standards vocabulary
  for in-toto/SBOM/AIBOM/C2PA alignment, append-only follow-up events, and
  `not_verified` packet fields for skipped checks and unobserved state.
- Forum prose humanization: catalog includes `forum.prose.humanize` as part of the shared flagship MCP surface.
- MCP server manifest: adds `project-telos.mcp-server-manifest/v1`, `node demo/server-manifest.mjs`, and `telos.server.manifest` so Codex, Claude, OpenAI Agents, IDEs, CLIs, TUIs, and app hosts can launch the same five flagship MCP servers from one source.
- Admission telemetry convention: adds `project-telos.admission-telemetry/v1`, `node demo/admission-telemetry.mjs`, and `telos.admission.telemetry` to keep admission decisions separate from verification verdicts while recording privacy-safe evidence references and negative fail-closed cases.
Presentation and operator-surface housekeeping for five-flagship parity.

- README: adds the shared current-status block and consistent five-flagship navigation.
- Status payload: exposes the current operator commands, Telos MCP tool names, and 26-tool catalog summary under `native`.
- Operator room: records `status`, `doctor`, `room`, `catalog`, and `flagship-workflow` as the current front door for local operators and host integrations.
- MCP surface: records native availability for `telos.status`, `telos.doctor`, `telos.room`, `telos.catalog`, `telos.workflow`, `telos.server.manifest`, `telos.admission.telemetry`, and `telos.showcase.scout`.
- Catalog: keeps `demo/integrations/mcp-tool-catalog.json` as the provider-neutral source of truth for 26 available tools across Gather, Crucible, Index, Forum, and Telos on this branch.
- Research receipts: records the YouTube intake ledger under `demo/research/youtube-bgoertzel-receipts.json` as receipt-only research material, with no raw transcript text in the repository.
