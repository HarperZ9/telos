# Project Telos Integration Pack

This folder is the platform bridge. The flagship tools stay standalone; integrations mount the same CLI and MCP contracts.

## Integration Rule

Business logic lives in the tools:

- `gather` handles intake.
- `index` handles structure and context.
- `forum` handles routing and ledger orchestration.
- `crucible` handles falsifiable verification.
- `telos` handles reconciliation and the shared room.

OpenAI Apps, OpenAI Agents, Anthropic Claude, Claude Code, Codex plugins, skills, IDEs, CLIs, TUIs, and full applications should call the same MCP tool catalog or CLI JSON commands. They should not duplicate tool behavior.

## Local-First Transports

- CLI JSON: works everywhere a process can run.
- MCP stdio: local agent surfaces, Codex, Claude Code, desktop tools.
- MCP Streamable HTTP: hosted apps, OpenAI Apps SDK style deployments, remote workspaces.

## Tool Catalog

`mcp-tool-catalog.json` is the provider-neutral source of truth for tool names, CLI fallbacks, MCP names, availability status, and next actions.

`mcp-server-manifest.json` is the provider-neutral source of truth for launching the five flagship MCP servers from source checkouts or package installs. `expected_tools` is the preferred forward-facing catalog surface; `auxiliary_tools` records compatible lower-level or legacy aliases that a launched server may still expose. `../server-manifest.mjs --codex` emits Codex TOML; `../server-manifest.mjs --claude-json` emits Claude-style JSON.

`../mcp-freshness.mjs` emits `project-telos.mcp-freshness/v1`, a host-side stale-server probe contract. Hosts compare observed `serverInfo.version`, status `tool_version`, `tools/list` hashes, and declared behavior probes against the manifest before trusting a loaded MCP server. The behavior probes now cover broad Forum routing and Index context-envelope selection/freshness receipts, so a host can catch stale behavior even when version and tool-list parity look healthy. `../mcp-freshness.mjs --observed observed.json` emits `project-telos.mcp-freshness-observation/v1` with `MATCH`, `DRIFT`, or `UNVERIFIABLE` plus normalized failure codes.

`admission-telemetry-conventions.json` records the Project Telos split between an admission decision and a verification verdict, plus the negative cases that must be observable without raw prompt, raw tool-argument, or raw evidence capture.

`context-envelope-conventions.json` records the large-workspace context contract for readable agent code, source-ref compression, freshness gates, and receipt-chained unattended work.

`../context-pack.mjs` emits a runnable `project-telos.context-pack/v1` packet that validates budget, source refs, receipt joins, load-versus-relevance evidence, and raw-payload boundaries for token-efficient second-brain handoffs.

`action-receipt-conventions.json` records the enterprise receipt interface and append-only persistence contract for auditable agent actions, including digest inputs, component/config identity, policy decisions, verification verdicts, and compensation events.

`atp-adapter-validation.json` records a public/synthetic adapter-validation profile for ATP v1.2.0 transaction receipts: digest refs, component/config identity, side-effect class, policy decision, verification verdict, typed stop reason, and append-only compensation. It is a fixture profile, not a live ATP/Haystack conformance claim.

`scankii-synthetic-receipt.json` records a public/synthetic dogfood run against scankii's replayable-receipt branch. It preserves normalized replay fields and explicit drift cases from the raw scanner output; it is not a private corpus scan or a production security claim.

`agent-boundary-fixtures.json` records public/synthetic boundary fixtures for approval resume, cancellation, MCP lifecycle, and loop-guard discussions. It gives other OSS projects a small receipt-shaped corpus to compare against without requiring raw prompts, raw tool arguments, raw reasoning, private services, or live credentials.

`research-seed-conventions.json` records how terse operator notes become source-backed research seeds: the note is a lead, current lawful source receipts promote claims, and unresolved claims stay `UNVERIFIABLE`. `../rendering-research.mjs` applies the same contract to clustered-forward rendering, Gaussian splatting, WebGPU/WGSL, SuperSplat, and visual acceptance gates for Telos rendering surfaces. `rendering-capabilities.json` and `../rendering-capabilities.mjs` turn that research into a host-neutral renderer selection contract: WebGPU splat/clustered prototype, WebGL2 preview, Canvas 2D receipt renderer, then static artifact fallback. `measurement-layers.json` and `../measurement-layers.mjs` provide ten runnable meters across histogram, dither, splat, cluster, audio, flicker, curvature, interaction, uncertainty, and frame budget signals. `creative-engine-manifest.json` and `../creative-engine.mjs` present the whole Telos Creative Engine contract across generative art, sound, typography, media, math/physics, node graphs, sensor/measurement layers, verification, and revived local organs. `../creative-kernels.mjs` exposes deterministic ordered-dither, pixel-sort, harmonograph, and clustered-light kernels for reuse by CLI, MCP, browser, IDE, and app hosts. `revival-registry.json` and `../revival-registry.mjs` promote older, siloed, and frozen tools into explicit lanes with origin paths, Gather-backed README digests, risk boundaries, flagship hosts, and next actions; Context Curator Lite is the context-envelope source lane for token-efficient, lossless-by-reference large-workspace handoffs. `display-calibration.json` and `../display-calibration.mjs` promote Calibrate Pro and Quanta Color into a read-only display-calibration contract for display targets, patch sets, color metrics, artifact refs, privacy boundaries, and Crucible measurement gates. `../presentation-doctor.mjs` scans sibling flagship checkouts for README, changelog, and brand-asset parity without raw document bodies or absolute paths. `../accessibility-doctor.mjs` scans Studio HTML for language, viewport, keyboard, reduced-motion, form-label, live-region, and canvas-fallback signals without raw HTML or browser automation. `../performance-doctor.mjs` scans Studio HTML for byte budgets, asset budgets, approved external hosts, non-blocking scripts, media dimensions, reduced motion, autoplay, and embedding-safe performance signals without raw HTML or browser automation. `../compatibility-doctor.mjs` scans the catalog and server manifest for protocol schemas, transports, host exports, source/package profiles, expected-tool joins, CLI fallbacks, MCP availability, freshness probes, HTTPS sources, and private-path hygiene. `../operator-doctor.mjs` scans README, status, catalog, manifest, CI, and current-state docs for operator discoverability drift.

`../research/rendering-pipeline-seeds.json` records lawful Gaussian-splatting, clustered-forward-rendering, WebGPU/WGSL, browser-rendering, neural-rendering, mesh-shader, and rendering-provider source receipts or leads for Telos Studio rendering surfaces. Provider pages, social links, and Reddit references remain non-evidentiary source leads until repeatable benchmarks or primary technical sources promote them.

`../research/youtube-math-educator-receipts.json` records compact metadata receipts for Inigo Quilez, math/physics educator, world-model, AI-progress, and GPU-kernel video source leads. It stores no raw video and no raw transcript text.

`../research/thermodynamic-ai-chip-receipt.json` records the verified Thomas Ahle / Machine Learning Street Talk transcript packet and public-source Normal Computing-adjacent integration lane. It stores no raw transcript text, claims no partnership, and keeps external technical correctness behind future primary-source and Crucible checks.

`../research/operator-source-leads.json` records blocked, social, provider, and discovery links as quarantined leads. They can route future work, but they do not promote claims.

`../../tools/render_flagship_heroes.py --check-existing --public-root <sibling-root>` verifies the five README hero PNGs and brand receipt READMEs without private fonts or Pillow. `--render` uses the operator-owned Kilon and Conso font ZIPs plus Pillow to regenerate the artwork locally.

`../mcp-runtime-contract.test.mjs` checks the catalog against the sibling MCP runtimes so `available` means the tool is actually present in `tools/list`. `../mcp-server-launch.test.mjs` starts each `source_checkout` profile from the manifest and verifies that expected tools are present and any extra tools are declared as auxiliary compatibility surface.

`science-research-adapters.json` is the current-source adapter map for preprints, scholarly metadata, clinical trial registries, persistent identifiers, AlphaFold, Midjourney Medical monitoring, and research graphs.
It includes a lawful full-text boundary: use Unpaywall, PubMed Central, Europe PMC, DOAJ, CORE, publisher OA links, repositories, and preprints; never use Sci-Hub or shadow-library material as provenance. User-provided shadow references can be retained only as non-evidentiary source leads that drive DOI/title/author/PMID/PMCID/arXiv/publisher/repository cross-reference.

`fresh-research-policy.md` is the rule for living external claims: current evidence or `UNVERIFIABLE`.

`current-host-protocols.md` records the official host/protocol evidence used for the MCP integration shape.

Availability labels:

- `available`: a native MCP server or command exists now.
- `cli-bridge`: a CLI JSON command exists now and should be wrapped by a thin MCP adapter.
- `planned`: the tool has a stable CLI surface and needs MCP parity work.

## Packaging Targets

- Codex plugin: expose skills plus MCP servers for `gather`, `crucible`, `index`, `forum`, and Telos.
- Telos MCP: `node demo/telos-mcp.mjs` exposes `telos.status`, `telos.doctor`, `telos.room`, `telos.workflow`, `telos.catalog`, `telos.server.manifest`, `telos.mcp.freshness`, `telos.ci.doctor`, `telos.presentation.doctor`, `telos.accessibility.doctor`, `telos.performance.doctor`, `telos.compatibility.doctor`, `telos.operator.doctor`, `telos.admission.telemetry`, `telos.context.envelope`, `telos.context.pack`, `telos.action.receipt`, `telos.loop.ledger`, `telos.research.seed`, `telos.research.thermodynamic`, `telos.rendering.research`, `telos.rendering.capabilities`, `telos.measurement.layers`, `telos.creative.engine`, `telos.creative.kernels`, `telos.revival.registry`, `telos.second_level.queue`, `telos.workstation.substrate`, and `telos.display.calibration`.
- Gather MCP: `gather mcp` exposes `gather.status`, `gather.doctor`, `gather.docs`, `gather.arxiv`, and `gather.run`.
- Crucible MCP: `crucible mcp` exposes `crucible.status`, `crucible.doctor`, `crucible.assess`, `crucible.measurement_gate`, `crucible.recheck`, `crucible.run`, `crucible.review`, `crucible.report`, `crucible.batch`, `crucible.registry`, `crucible.drift`, `crucible.refine`, and `crucible.verdicts`.
- Index MCP: `index mcp` exposes `index.map`, `index.context`, `index.context.envelope`, `index.status`, `index.doctor`, and the lower-level graph, focus, verify, router, and internals tools.
- Forum MCP: `forum mcp` exposes `forum.route`, `forum.status`, `forum.doctor`, `forum.ledger.summary`, and the ledger-backed submit, plan, verify, and ledger-get tools.
- Superpowers skills: add thin workflows that call the CLI/MCP catalog.
- Anthropic Claude and Claude Code: mount stdio MCP servers from the same catalog.
- OpenAI Agents and Apps: mount MCP servers and render Telos receipts in the app UI.
- IDEs, CLIs, and TUIs: call CLI JSON locally and render the same action envelope in their native surfaces.
- Full applications: call CLI JSON for local desktop and MCP Streamable HTTP for hosted or distributed setups.
- Workbench/Harness candidate: keep it as a consumer of the five flagships until the five-tool golden workflow is exceptional.
- Operator room: `node demo/room.mjs` for humans, `node demo/room.mjs --json` for hosts.

## Science And Research Domains

The first domain adapter map covers:

- Preprints and archives: arXiv, bioRxiv, medRxiv, ChemRxiv, OSF Preprints, SSRN, Research Square.
- Biomedical and clinical literature: PubMed/NCBI E-utilities, Europe PMC.
- Scholarly graphs and metadata: OpenAlex, Crossref, Semantic Scholar, DataCite, ORCID, ROR, OpenAIRE.
- Scientific model artifacts: AlphaFold Database and AlphaFold 3/server outputs.
- Emerging medical tools: Midjourney Medical as a watch-only evidence source until stronger clinical, regulatory, and API evidence exists.
