# Changelog

All notable changes to Project Telos. Telos is currently a source demo and shared operator room rather than a packaged Python or npm release.

## Unreleased

- Causal Research Workbench preflight: adds
  `demo/causal-workbench-proof-packet.mjs`, a deterministic toy-DAG proof
  packet, source-ledger receipts, official, working-paper, outreach, Crucible,
  and Learn prooflesson artifacts. The pass verifies `CAUSAL_DAG_FIXTURE_MATCH`
  for the local fixture while keeping causal discovery, LLM causal reasoning,
  biomedical, and BuildLang/buildc-native claims out of scope.

- TI Morse / Relentless field intake: adds
  `demo/research/youtube-ti-morse-field-receipts.json`, a bounded source-ledger
  for five metadata/transcript receipts and one channel-list receipt, plus
  official, working-paper, outreach, Crucible, and Learn prooflesson artifacts.
  The pass maps industrial science proof packets, causal research workbench,
  agentic benchmark foundry, and compute/infrastructure ledger as inferred
  megatool lanes while leaving domain correctness
  `UNVERIFIABLE_UNTIL_PRIMARY_SOURCE_OR_REPLAY`.

- Browser evidence kernel: adds `project-telos.browser-evidence/v1`,
  `node demo/browser-evidence.mjs`, and `telos.browser.evidence` as the
  local-first browser automation evidence contract for Gather/Index/Forum/
  Crucible/Learn/Emet/BuildLang pipeline consumers.

- OSS Proof Showcase: adds a fixture-first candidate scout, PR-readiness packet
  contract, read-only Telos MCP scout tool, and an optional live GitHub smoke
  command for high-star public issue discovery.
- Feedback integration: adds plain-language operator copy, standards vocabulary
  for in-toto/SBOM/AIBOM/C2PA alignment, append-only follow-up events, and
  `not_verified` packet fields for skipped checks and unobserved state.
- MCP freshness: adds Forum private-line routing and Index portable private-line
  map behavior probes, so host-loaded MCP servers must prove current routing and
  nested-workspace map behavior before Telos trusts their output.
- Learning Forge labs: adds `project-telos.learning-forge/labs/v1`,
  `node demo/learning-forge-labs.mjs`, and `telos.learning.labs` to turn the
  gathered operator research packet into seven executable lab contracts with
  source receipts, runnable commands, failure cases, measurement gates,
  expected artifacts, and Gather/Index/Forum/Crucible/Telos ownership.
- Learning Forge intake: adds `demo/research/youtube-learning-forge-receipts.json`
  for the newest video/channel seed corpus, keeping gathered video metadata,
  transcript hashes, channel-list hashes, and `UNVERIFIABLE_UNTIL_CROSS_CHECK`
  research-claim status separate from raw transcript bodies.
- Learning Forge: adds `project-telos.learning-forge/youtube-research-seed/v1`,
  `node demo/learning-forge.mjs`, and `telos.learning.forge` to turn operator-provided
  video/channel/paper/benchmark leads into receipt-backed learning labs with explicit
  YouTube `UNVERIFIABLE_UNTIL_GATHER_TRANSCRIPT` boundaries, current lawful source
  receipts, failure cases, and Gather/Index/Forum/Crucible/Telos next actions.
- CI triage: adds `project-telos.ci-triage/v1`, `node demo/ci-triage.mjs`,
  and `telos.ci.triage` to classify blocking CI failures separately from
  Node runtime migration warnings with sanitized evidence excerpts and typed
  remediation routes. The CLI now supports live read-only GitHub Actions intake
  with `--gh-run owner/repo#run_id` in addition to offline fixture packets.
- Operator doctor: adds `project-telos.operator-doctor/v1`,
  `node demo/operator-doctor.mjs`, and `telos.operator.doctor` to verify
  README quick start, status/catalog/MCP parity, CI doctor coverage,
  current-state docs, host-surface language, and next-action guidance.
- Compatibility doctor: adds `project-telos.compatibility-doctor/v1`,
  `node demo/compatibility-doctor.mjs`, and `telos.compatibility.doctor` to verify
  catalog/manifest schema parity, host exports, source/package profiles,
  expected-tool joins, CLI fallbacks, MCP availability, freshness probes, HTTPS
  sources, and private-path hygiene.
- Performance doctor: adds `project-telos.performance-doctor/v1`,
  `node demo/performance-doctor.mjs`, and `telos.performance.doctor` to verify
  static Studio byte budgets, asset budgets, approved external hosts, media
  dimensions, reduced motion, autoplay, and embedding-safe performance signals.
- Accessibility doctor: adds `project-telos.accessibility-doctor/v1`,
  `node demo/accessibility-doctor.mjs`, and `telos.accessibility.doctor` to verify
  static Studio accessibility signals such as reduced motion, keyboard focus,
  labeled controls, live regions, and canvas fallbacks.
- Presentation doctor: adds `project-telos.presentation-doctor/v1`,
  `node demo/presentation-doctor.mjs`, and `telos.presentation.doctor` to turn
  five-flagship README, changelog, and brand-asset parity into privacy-safe
  `MATCH`, `DRIFT`, or `UNVERIFIABLE` receipts.
- Project map: adds `docs/PROJECT-CONNECTION-MAP.md` as the canonical five-flagship connection,
  distribution, adapter, hyphal-context, and promotion map, backed by Gather-digested operator
  research packets and live MCP dogfood status.
- Project map: expands the connection map from five-flagship-only to the HarperZ9 public
  repo constellation as a Telos growth layer, with verified visible/public/private/fork counts
  and a lane-record rule for public, private, and local-only revival candidates.
- Revival registry: promotes sanitized local-only lane records for raw-native, studio-libs, and
  the Forum archive, raising the registry to 13 tools while keeping raw private viability notes
  out of git.
- Second-level queue: adds `project-telos.second-level-flagship-queue/v1`,
  `node demo/second-level-flagship-queue.mjs`, and tests to track public-safe next-wave
  flagship candidates while summarizing private/local-only work as lane families.
- Action receipts: hardens `project-telos.action-receipt/v1` for external writes by separating durable receipts
  from trace spans, adding external action kinds, authority/execution/evidence/review/compensation refs,
  redacted before/after evidence, source-correction provenance, and negative cases for authority gaps,
  evidence gaps, duplicate idempotency keys, and collapsed proposed/completed action reports.
- Model foundry research: adds the RL scaling receipt-spine target for Slime-class post-training systems,
  focusing Telos on rollout, verifier, reward, compute, checkpoint, and promotion receipts rather than
  unverified frontier-training claims.
- MCP launch profiles: adds an executable source-checkout launch contract test and declares auxiliary
  Index/Forum compatibility tools separately from the 51 preferred catalog tools, so host integrations can
  distinguish the polished surface from lower-level or legacy aliases.
- MCP freshness: adds an `index.context.envelope` behavior probe that requires focused envelopes to return
  selection summaries and `index.context-envelope-freshness/v1` roots, catching stale Index MCP servers that
  still expose the old envelope shape after status/tool-list parity appears healthy.
- MCP freshness: adds `project-telos.mcp-freshness/v1`, `project-telos.mcp-freshness-observation/v1`, `node demo/mcp-freshness.mjs`, and `telos.mcp.freshness` so hosts can detect stale loaded servers by comparing `serverInfo.version`, `status.tool_version`, `tools/list` hashes, and declared behavior probes before trusting tool output, then emit `MATCH`, `DRIFT`, or `UNVERIFIABLE` with normalized failure codes from `--observed`.
- Model foundry: adds `project-telos.model-foundry/v1`, `node demo/model-foundry.mjs`, and `telos.model.foundry` to define the bounded model-building and self-improving daemon lane: frontier APIs as components, local/open-weight runtimes, feasible post-training labs, typed MCP tools, lossless-by-reference memory, objective monitoring, and Crucible-gated promotion without claiming independent frontier-lab pretraining capacity.
- Context pack surface: adds `project-telos.context-pack/v1`, `node demo/context-pack.mjs`, and `telos.context.pack` to emit a runnable, token-budgeted, lossless-by-reference context packet with source-ref joins, load/relevance receipt separation, raw-payload checks, and explicit failure codes.
- Thermodynamic AI integration lane: adds `project-telos.research-intake/youtube-verified-transcript-v1`, `node demo/thermodynamic-ai-chip-receipt.mjs`, and `telos.research.thermodynamic` to promote the verified Thomas Ahle interview into a public-source Normal Computing-adjacent lane for spec representation, Verilog/formal receipts, stochastic simulation, uncertainty meters, and hybrid search/check loops without claiming partnership or external technical correctness from the interview alone.
- Display calibration: adds `project-telos.display-calibration/v1`, `node demo/display-calibration.mjs`, and `telos.display.calibration` to promote Calibrate Pro and Quanta Color into a read-only display-calibration contract for display targets, patch sets, color metrics, ICC/LUT/report artifact refs, privacy boundaries, and Crucible measurement gates.
- Revival registry: adds `project-telos.revival-registry/v1`, `node demo/revival-registry.mjs`, and `telos.revival.registry` to begin promoting Calibrate Pro, Quanta Color, QuantaLang/quantac, WARDEN security lineage, Agent Audit, Context Curator Lite, Secret Redact IO, Repo Proof Index, Release Surface Scanner, GPU Trace Validator, raw-native, studio-libs, and the Forum archive from siloed or frozen tools into explicit flagship lanes with Gather-backed source receipts, risk boundaries, and next actions.
- Engine demo: adds a live Telos Studio effects console with retro CGI, glitch art, seeded generative fields, plotter paths, pixel sorting, poster composition, fractal recursion, Gaussian-splat stand-ins, clustered-light overlays, reduced-motion handling, and visible scene receipts.
- Effects protocol: adds a host-neutral project-telos.scene-spec/v1 scene envelope, six replayable presets, hashed action identities, chained project-telos.scene-receipt/v1 render receipts, copy/export/replay controls, and CI coverage for protocol-compatible Telos Studio embedding.
- Rendering capabilities: adds `project-telos.rendering-capabilities/v1`, `node demo/rendering-capabilities.mjs`, and `telos.rendering.capabilities` so hosts can select WebGPU Gaussian-splat/clustered prototypes, WebGL2 previews, Canvas 2D receipts, or static artifact fallbacks with privacy and verification gates.
- Measurement layers: expands `project-telos.measurement-layers/v1`, `node demo/measurement-layers.mjs`, and `telos.measurement.layers` to ten runnable meters for histogram, dither-spectrum, splat-probe, cluster-meter, audio-spectral, temporal flicker, geometry curvature, interaction trace, uncertainty budget, and frame budget signals.
- Crucible catalog parity: expands the shared MCP catalog and server manifest to the full current
  Crucible source-checkout surface, including run, measurement-gate, review, report, batch, registry,
  drift, refine, and verdicts tools.
- Creative engine manifest: adds `project-telos.creative-engine/v1`, `node demo/creative-engine.mjs`, and `telos.creative.engine` to present the whole creation engine across generative art, retro CGI, raster effects, sound, film/media, typography, math/physics, node graphs, verification, and revived local organs.
- Creative kernels: adds `project-telos.creative-kernels/v1`, `node demo/creative-kernels.mjs`, and `telos.creative.kernels` for deterministic ordered dithering, pixel sorting, harmonograph/plotter paths, clustered light bins, and receipt hashes.
- Sensor layers: records planned histogram, splat-probe, clustered-light, and audio spectral meters so creative work can become measurable without confusing renderer execution choices with verification verdicts.
- Math educator research intake: adds `demo/research/youtube-math-educator-receipts.json` with compact metadata receipts for Inigo Quilez, math/physics educator, world-model, AI-progress, and GPU-kernel source leads, while keeping raw video and raw transcripts out of the repo.
- Index catalog parity: adds `index.context.envelope` to the shared MCP catalog and server manifest so large-workspace, budgeted context packets are available through the same provider-neutral surface.

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
- Status payload: exposes the current operator commands, Telos MCP tool names, and 65-tool catalog summary under `native`.
- Operator room: records `status`, `doctor`, `room`, `catalog`, and `flagship-workflow` as the current front door for local operators and host integrations.
- MCP surface: records native availability for `telos.status`, `telos.doctor`, `telos.room`, `telos.catalog`, `telos.workflow`, `telos.server.manifest`, `telos.mcp.freshness`, `telos.ci.doctor`, `telos.ci.triage`, `telos.presentation.doctor`, `telos.accessibility.doctor`, `telos.performance.doctor`, `telos.compatibility.doctor`, `telos.operator.doctor`, `telos.admission.telemetry`, `telos.context.envelope`, `telos.context.pack`, `telos.action.receipt`, `telos.loop.ledger`, `telos.objective.monitor`, `telos.model.foundry`, `telos.learning.forge`, `telos.learning.labs`, `telos.research.seed`, `telos.research.thermodynamic`, `telos.rendering.research`, `telos.rendering.capabilities`, `telos.measurement.layers`, `telos.creative.engine`, `telos.creative.kernels`, `telos.revival.registry`, `telos.second_level.queue`, `telos.workstation.substrate`, `telos.display.calibration`, `telos.native.control`, and `telos.showcase.scout`.
- Catalog: keeps `demo/integrations/mcp-tool-catalog.json` as the provider-neutral source of truth for 65 available tools across Gather, Crucible, Index, Forum, and Telos.
- Research receipts: records the YouTube intake ledger under `demo/research/youtube-bgoertzel-receipts.json` as receipt-only research material, with no raw transcript text in the repository.
