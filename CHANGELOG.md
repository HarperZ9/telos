# Changelog

All notable changes to Project Telos. Telos is a zero-dependency source demo and shared operator room; 0.2.0 adds npm packaging prep (bin entries, files allowlist, release lane) while publishing stays operator-gated.

## Unreleased

- Ship prep for 0.2.0: package version 0.2.0 across package.json, the MCP
  serverInfo, the telos.status envelope, and the server-manifest freshness
  expectations. Adds `bin` entries (`telos-mcp` for the stdio MCP server,
  `telos` as a router over the demo command surface), a `files` allowlist for
  `npm pack`, a Release workflow (`.github/workflows/release.yml`) that builds
  the npm tarball and a runnable demo zip on manual dispatch or a published
  release, RELEASING.md, draft release notes, and a Run it block in the README.
  Tagging and publishing stay operator-gated.
- Manifest: declares `index.select` as Index auxiliary compatibility surface
  (12 to 13 auxiliary tools) so the source-checkout launch gate matches the
  current Index tool surface.
- Brand gate: hero dimension check now matches the shipped flagship card canon
  (2400x1260, the 1200x630 OG card at 2x).
- Proof lanes: four sibling proof lanes now ship through one CLI,
  `node demo/proof.mjs`, each with a frozen contract, a pure verifier that
  recomputes every load-bearing claim from embedded materials and can return
  `DRIFT` or `UNVERIFIABLE`, and a proof-surface export whose `decision_summary`
  is derived from the overall verdict. Every lane treats a missing recomputable
  basis as an `UNVERIFIABLE` gap named by its path, floors an empty check set to
  `UNVERIFIABLE` rather than a silent `MATCH`, and makes a canned `MATCH`
  structurally impossible.
  - Agent-action (`project-telos.proof-packet/v1`, MCP `telos.proof`, subcommand
    `agent-action`): joins source refs, context refs, route, admission, side
    effects, and output digests, with an optional Emet coherence witness stage
    that records `unavailable` honestly. Exports to the proof-surface
    `agent-action-proof-packet/v0` contract.
  - Research-claim (`project-telos.research-proof-packet/v1`, MCP
    `telos.proof.research`, subcommand `research`): joins source provenance, a
    bounded claim, a required negative control fixture, attempt records, and a
    promotion rung; its verifier recomputes each source and negative-fixture
    digest from the embedded body, rejects a control that did not survive, and
    refuses to assert a reproduction-gated rung (`PROMOTED_DISCOVERY`,
    `LAW_CANDIDATE`) inside a single packet. Exports to
    `research-claim-proof-packet/v0`.
  - Visual-truth (`project-telos.visual-proof-packet/v1`, MCP
    `telos.proof.visual`, subcommand `visual`): recomputes every
    relative-luminance and CIE76 delta-E measurement from the artifact's own
    embedded sRGB samples with stdlib color math, rejects a non-read-only packet,
    and rejects a physical-calibration claim over a read-only surface. Exports to
    `visual-measurement-proof-packet/v0`.
  - Build scientific-runtime (`project-telos.build-proof-packet/v1`, MCP
    `telos.proof.build`, subcommand `build`): recomputes a conserved-quantity
    invariant (mean total energy) and a conservation drift (maximum relative
    energy drift) from the run's own embedded samples with stdlib math, bounds
    each tolerance to a small fraction of the metric's physical range so an
    oversized author-declared tolerance is itself `DRIFT`, and requires a
    negative fixture that must break the invariant. Exports to the proof-surface
    `conservation-proof-packet/v0` contract.

  `verify` and `export` dispatch by the packet's own schema id, so each lane is
  re-checked and exported by its own verifier and exporter and an unknown schema
  is an error rather than a silent pass. The four read-only MCP tools move the
  five-flagship catalog from 65 to 69 tools (telos from 37 to 41).
- Agent-action proof lane: adds `project-telos.proof-packet/v1`, a frozen
  agent-action proof packet contract that joins source refs, context refs,
  route, admission, side effects, output digests, and an optional durable
  ledger entry by reference rather than by copied payload, composing the
  existing `project-telos.action-receipt/v1`, `project-telos.context-envelope/v1`,
  and `project-telos.loop-ledger/v1` contracts. Ships `node demo/proof.mjs`
  with `agent-action`, `verify`, and `export` subcommands, a pure verifier that
  derives `MATCH`, `DRIFT`, or `UNVERIFIABLE` from named checks (required
  fields, state-model legality, packet-hash and artifact-digest recomputation,
  admission-before-execution ordering, and compensation presence for external
  writes) so a canned verdict is structurally impossible, an optional Emet
  coherence witness stage that records `unavailable` honestly when no
  implementation is reachable and never fabricates a verdict, and a frozen
  `toProofSurfacePacket()` export to the proof-surface
  `agent-action-proof-packet/v0` contract. Registers the read-only `telos.proof`
  MCP tool that emits the fixture demo packet, moving the five-flagship catalog
  from 65 to 66 tools.

- Documentation consolidation: adds
  `docs/PROJECT-TELOS-LARGE-SCALE-ROADMAP-2026-07-02.md`,
  `docs/DOCUMENTATION-CONSOLIDATION-REGISTRY-2026-07-02.md`, and
  `docs/FRONTIER-RD-OPERATING-POSTURE-2026-07-02.md` as the new control-plane
  docs for Project Telos roadmap, corpus classification, publication gates,
  Build ecosystem integration, and broadened frontier R&D scope. The pass also
  adds `docs/registry/documentation-registry.json` and
  `docs/research/PUBLICATION-QUEUE-2026-07-02.md`, plus the cross-repo
  documentation catalog in
  `docs/registry/PUBLIC-WORKSPACE-DOC-CATALOG-2026-07-02.md` and
  `docs/registry/public-workspace-doc-catalog-2026-07-02.json`, the Senses and
  Sensibility subregistry in
  `docs/registry/SENSES-AND-SENSIBILITY-SUBREGISTRY-2026-07-02.md` and
  `docs/registry/senses-and-sensibility-subregistry-2026-07-02.json`, and the Build
  ecosystem subregistry in
  `docs/registry/BUILD-ECOSYSTEM-SUBREGISTRY-2026-07-02.md` and
  `docs/registry/build-ecosystem-subregistry-2026-07-02.json`, plus the
  proof/witnessing subregistry in
  `docs/registry/PROOF-WITNESSING-SUBREGISTRY-2026-07-02.md` and
  `docs/registry/proof-witnessing-subregistry-2026-07-02.json`, plus the Telos
  repo subregistry in
  `docs/registry/TELOS-REPO-SUBREGISTRY-2026-07-02.md` and
  `docs/registry/telos-repo-subregistry-2026-07-02.json`. It links the
  docs from `README.md` and `docs/CURRENT-STATE.md` while keeping public claims
  receipt-bound and high-risk source details fenced.

- Quantum Error-Correction preflight: adds
  `demo/quantum-error-correction-proof-packet.mjs`, a deterministic 3-qubit
  bit-flip stabilizer proof packet, source-ledger receipts, official,
  working-paper, outreach, Crucible, and Learn prooflesson artifacts. The pass
  verifies `QEC_STABILIZER_FIXTURE_MATCH` for the local fixture while keeping
  surface-code, hardware QEC, fault-tolerant computation, quantum advantage,
  cryptographic, and BuildLang/buildc-native claims out of scope.

- Embodied Sim-to-Real preflight: adds
  `demo/embodied-sim2real-proof-packet.mjs`, a deterministic
  differential-drive proof packet, source-ledger receipts, official,
  working-paper, outreach, Crucible, and Learn prooflesson artifacts. The pass
  verifies `EMBODIED_SIM2REAL_FIXTURE_MATCH` for the local fixture while
  keeping real robot safety, medical robotics, foundation-model, large-scale
  sim-to-real, and BuildLang/buildc-native claims out of scope.

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
