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

`mcp-server-manifest.json` is the provider-neutral source of truth for launching the five flagship MCP servers from source checkouts or package installs. `../server-manifest.mjs --codex` emits Codex TOML; `../server-manifest.mjs --claude-json` emits Claude-style JSON.

`admission-telemetry-conventions.json` records the Project Telos split between an admission decision and a verification verdict, plus the negative cases that must be observable without raw prompt, raw tool-argument, or raw evidence capture.

`context-envelope-conventions.json` records the large-workspace context contract for readable agent code, source-ref compression, freshness gates, and receipt-chained unattended work.

`action-receipt-conventions.json` records the enterprise receipt interface and append-only persistence contract for auditable agent actions, including digest inputs, component/config identity, policy decisions, verification verdicts, and compensation events.

`../mcp-runtime-contract.test.mjs` checks the catalog against the sibling MCP runtimes so `available` means the tool is actually present in `tools/list`.

`science-research-adapters.json` is the current-source adapter map for preprints, scholarly metadata, clinical trial registries, persistent identifiers, AlphaFold, Midjourney Medical monitoring, and research graphs.
It includes a lawful full-text boundary: use Unpaywall, PubMed Central, Europe PMC, DOAJ, CORE, publisher OA links, repositories, and preprints; never use Sci-Hub or shadow-library material as provenance.

`fresh-research-policy.md` is the rule for living external claims: current evidence or `UNVERIFIABLE`.

`current-host-protocols.md` records the official host/protocol evidence used for the MCP integration shape.

Availability labels:

- `available`: a native MCP server or command exists now.
- `cli-bridge`: a CLI JSON command exists now and should be wrapped by a thin MCP adapter.
- `planned`: the tool has a stable CLI surface and needs MCP parity work.

## Packaging Targets

- Codex plugin: expose skills plus MCP servers for `gather`, `crucible`, `index`, `forum`, and Telos.
- Telos MCP: `node demo/telos-mcp.mjs` exposes `telos.status`, `telos.doctor`, `telos.room`, `telos.workflow`, `telos.catalog`, `telos.server.manifest`, `telos.admission.telemetry`, `telos.context.envelope`, `telos.action.receipt`, and `telos.loop.ledger`.
- Gather MCP: `gather mcp` exposes `gather.status`, `gather.doctor`, `gather.docs`, `gather.arxiv`, and `gather.run`.
- Crucible MCP: `crucible mcp` exposes `crucible.status`, `crucible.doctor`, `crucible.assess`, and `crucible.recheck`.
- Index MCP: `index mcp` exposes `index.map`, `index.context`, `index.status`, `index.doctor`, and the lower-level graph, focus, verify, router, and internals tools.
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
