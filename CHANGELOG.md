# Changelog

All notable changes to Project Telos. Telos is currently a source demo and shared operator room rather than a packaged Python or npm release.

## Unreleased

- Context evidence: separates load receipts from relevance receipts, accepts load-only traces as `valid_load_receipt_not_usefulness_claim`, and gives missing relevance, over-selection, and unjoinable relevance distinct failure codes.
- ATP adapter validation: adds Haystack-style component middleware semantics with pipeline-run receipt trees, RFC 8785 canonicalization expectations, and receiver-owned independence from signing/storage backends.
- Brand renderer: adds `tools/render_flagship_heroes.py` with a standard-library `--check-existing` mode for CI and a local `--render` mode for the operator-owned Kilon/Conso font ZIPs, preserving exported PNGs without committing purchased fonts.
- MCP runtime contract: now calls Gather's live source-checkout MCP surface with inline `gather.run` config, so host-neutral run configs are verified beyond `tools/list` parity.
- Research seeds: adds bundle-theoretic differential geometry and zenzic/repeated-squaring operation seeds with lawful source receipts, explicit boundaries around unresolved "flicker" terminology, and Crucible-ready negative-test directions.
- Research intake: extends the YouTube receipt ledger with TheAIGRID's `SbafEATbfXQ` video as metadata/transcript receipts only, and adds an operator-source-leads quarantine packet for blocked Reddit and GPU-provider/render-farm discovery links.
- Rendering research: records neural-rendering/mesh-shader candidates and GPU execution-substrate leads while keeping provider pages separate from rendering-algorithm claims.
- CI: adds a Node 24 GitHub Actions workflow that checks out all five flagships as siblings and runs the Telos contract, MCP runtime, room, and golden workflow gates on push and pull request.
- CI: updates the flagship gate to current official `actions/checkout@v7`, `actions/setup-node@v6`, and `actions/setup-python@v6` majors.
- Forum prose humanization: catalog includes `forum.prose.humanize` as part of the shared flagship MCP surface.
- MCP server manifest: adds `project-telos.mcp-server-manifest/v1`, `node demo/server-manifest.mjs`, and `telos.server.manifest` so Codex, Claude, OpenAI Agents, IDEs, CLIs, TUIs, and app hosts can launch the same five flagship MCP servers from one source.
- Admission telemetry convention: adds `project-telos.admission-telemetry/v1`, `node demo/admission-telemetry.mjs`, and `telos.admission.telemetry` to keep admission decisions separate from verification verdicts while recording privacy-safe evidence references and negative fail-closed cases.
- Context envelope convention: adds `project-telos.context-envelope/v1`, `node demo/context-envelope.mjs`, and `telos.context.envelope` for large-workspace context packing, readability gates, and receipt-chained unattended agent work.
- Action receipt convention: adds `project-telos.action-receipt/v1`, `node demo/action-receipt.mjs`, and `telos.action.receipt` for input digests, component/config identity, side-effect class, typed stop reasons, policy decisions, verification verdicts, and append-only compensation events.
- Loop ledger convention: adds `project-telos.loop-ledger/v1`, `node demo/loop-ledger.mjs`, and `telos.loop.ledger` for first-class durable loop state, fresh-context one-action iterations, explicit `UNVERIFIABLE`, and bounded headless scheduled fires that halt as `needs_attention` when user input is required.
- Research seed convention: adds `project-telos.research-seed/v1`, `node demo/research-seed.mjs`, and `telos.research.seed` to turn terse operator notes like Neil Turok and Planck's Constant into lawful, source-backed research packets.
- Rendering research contract: adds `node demo/rendering-research.mjs` and `telos.rendering.research` for lawful clustered-forward rendering, Gaussian splatting, WebGPU/WGSL, SuperSplat, design-pretty gates, accessibility fallbacks, provenance, and non-evidentiary Reddit/source-lead boundaries for Telos Studio surfaces.
- Research access boundary: expands the science adapter map with lawful OA resolvers for Unpaywall, CORE, DOAJ, and PubMed Central; marks Sci-Hub/shadow-library full text as invalid provenance; and allows user-provided shadow references only as non-evidentiary source leads for lawful cross-reference.
Presentation and operator-surface housekeeping for five-flagship parity.

- README: adds the shared current-status block and consistent five-flagship navigation.
- Status payload: exposes the current operator commands, Telos MCP tool names, and 30-tool catalog summary under `native`.
- Operator room: records `status`, `doctor`, `room`, `catalog`, and `flagship-workflow` as the current front door for local operators and host integrations.
- MCP surface: records native availability for `telos.status`, `telos.doctor`, `telos.room`, `telos.catalog`, `telos.workflow`, `telos.server.manifest`, `telos.admission.telemetry`, `telos.context.envelope`, `telos.action.receipt`, `telos.loop.ledger`, `telos.research.seed`, and `telos.rendering.research`.
- Catalog: keeps `demo/integrations/mcp-tool-catalog.json` as the provider-neutral source of truth for 30 available tools across Gather, Crucible, Index, Forum, and Telos.
- Research receipts: records the YouTube intake ledger under `demo/research/youtube-bgoertzel-receipts.json` as receipt-only research material, with no raw transcript text in the repository.
