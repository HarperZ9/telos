# Changelog

All notable changes to Project Telos. Telos is currently a source demo and shared operator room rather than a packaged Python or npm release.

## Unreleased

- CI: adds a GitHub Actions workflow that checks out all five flagships as siblings and runs the Telos contract, MCP runtime, room, and golden workflow gates on push and pull request.
- Forum prose humanization: catalog includes `forum.prose.humanize` as part of the shared flagship MCP surface.
- MCP server manifest: adds `project-telos.mcp-server-manifest/v1`, `node demo/server-manifest.mjs`, and `telos.server.manifest` so Codex, Claude, OpenAI Agents, IDEs, CLIs, TUIs, and app hosts can launch the same five flagship MCP servers from one source.
- Admission telemetry convention: adds `project-telos.admission-telemetry/v1`, `node demo/admission-telemetry.mjs`, and `telos.admission.telemetry` to keep admission decisions separate from verification verdicts while recording privacy-safe evidence references and negative fail-closed cases.
- Context envelope convention: adds `project-telos.context-envelope/v1`, `node demo/context-envelope.mjs`, and `telos.context.envelope` for large-workspace context packing, readability gates, and receipt-chained unattended agent work.
- Action receipt convention: adds `project-telos.action-receipt/v1`, `node demo/action-receipt.mjs`, and `telos.action.receipt` for input digests, component/config identity, side-effect class, typed stop reasons, policy decisions, verification verdicts, and append-only compensation events.
- Loop ledger convention: adds `project-telos.loop-ledger/v1`, `node demo/loop-ledger.mjs`, and `telos.loop.ledger` for first-class durable loop state, fresh-context one-action iterations, explicit `UNVERIFIABLE`, and bounded headless scheduled fires that halt as `needs_attention` when user input is required.
- Research access boundary: expands the science adapter map with lawful OA resolvers for Unpaywall, CORE, DOAJ, and PubMed Central, and marks Sci-Hub/shadow-library full text as invalid provenance.
Presentation and operator-surface housekeeping for five-flagship parity.

- README: adds the shared current-status block and consistent five-flagship navigation.
- Status payload: exposes the current operator commands, Telos MCP tool names, and 28-tool catalog summary under `native`.
- Operator room: records `status`, `doctor`, `room`, `catalog`, and `flagship-workflow` as the current front door for local operators and host integrations.
- MCP surface: records native availability for `telos.status`, `telos.doctor`, `telos.room`, `telos.catalog`, `telos.workflow`, `telos.server.manifest`, `telos.admission.telemetry`, `telos.context.envelope`, `telos.action.receipt`, and `telos.loop.ledger`.
- Catalog: keeps `demo/integrations/mcp-tool-catalog.json` as the provider-neutral source of truth for 28 available tools across Gather, Crucible, Index, Forum, and Telos.
- Research receipts: records the YouTube intake ledger under `demo/research/youtube-bgoertzel-receipts.json` as receipt-only research material, with no raw transcript text in the repository.
