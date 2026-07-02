# Project Telos Current State

Generated: 2026-07-02

This document is a live state packet for Project Telos. It is deliberately evidence-first: current capability, repo shape, and ambition are separated so the project can grow without turning roadmap into a false capability claim.

## Refresh Receipts

- Index public workspace map generated `2026-07-02T13:27:18-07:00`: 68 repositories, 62 public-class, 6 local-class, 10 dirty repositories, root SHA256 prefix `92ef331e0850ccf6`.
- Flagship MCP refresh on 2026-07-02 returned `MATCH` for Gather `1.5.0`, Index `2.8.0`, Forum `1.12.0`, and Crucible `1.1.0`.
- Telos MCP server manifest refresh on 2026-07-02 returned the five source-checkout launch profiles and host targets for Codex, Claude, OpenAI Agents, and OpenAI Apps.
- The active consolidation roadmap is `docs/PROJECT-TELOS-LARGE-SCALE-ROADMAP-2026-07-02.md`.
- The active documentation registry is `docs/DOCUMENTATION-CONSOLIDATION-REGISTRY-2026-07-02.md`.
- The active machine-readable documentation registry is `docs/registry/documentation-registry.json`.
- The active public-workspace documentation catalog is `docs/registry/PUBLIC-WORKSPACE-DOC-CATALOG-2026-07-02.md`, with machine data in `docs/registry/public-workspace-doc-catalog-2026-07-02.json`.
- The active Senses and Sensibility subregistry is `docs/registry/SENSES-AND-SENSIBILITY-SUBREGISTRY-2026-07-02.md`, with machine data in `docs/registry/senses-and-sensibility-subregistry-2026-07-02.json`.
- The active Build ecosystem subregistry is `docs/registry/BUILD-ECOSYSTEM-SUBREGISTRY-2026-07-02.md`, with machine data in `docs/registry/build-ecosystem-subregistry-2026-07-02.json`.
- The active proof/witnessing subregistry is `docs/registry/PROOF-WITNESSING-SUBREGISTRY-2026-07-02.md`, with machine data in `docs/registry/proof-witnessing-subregistry-2026-07-02.json`.
- The active Telos repo subregistry is `docs/registry/TELOS-REPO-SUBREGISTRY-2026-07-02.md`, with machine data in `docs/registry/telos-repo-subregistry-2026-07-02.json`.
- The active publication queue is `docs/research/PUBLICATION-QUEUE-2026-07-02.md`.
- The active frontier R&D posture is `docs/FRONTIER-RD-OPERATING-POSTURE-2026-07-02.md`.
- Gather federation validated the current Ti Morse and adjacent video source registry on 2026-07-02: 5 requested videos plus 1 Ti Morse channel catalog, seal `63a2b0cc6865791ea04bb7abdb7895db5ac4bc267c96785566e842833b9b1428`.
- Gather docs sealed the Senses and Sensibility corpus on 2026-07-02 with seal `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`; the model-facing catalog dropped 173 large corpus payloads, so the subregistry uses direct file reads for classification.
- Gather docs sealed the Telos docs surface on 2026-07-02 with seal `24b94d64f78e323245338463f79b6b87d97738bf1db489234826ff438a3d6270`; the model-facing catalog dropped 38 large payloads, so the Telos repo subregistry uses direct file reads plus Index, Forum, and Telos operator-doctor receipts.
- Latest Telos repo Index map generated `2026-07-02T13:37:49-07:00`: one public repo on `main`, head `1e0e1a1`, dirty count 3, untracked count 35, root SHA256 prefix `45e8256faa8bdc98`.
- Telos operator doctor generated `2026-07-02T20:37:50.274Z` returned `MATCH` with 14/14 checks passed across README, current state, CI, catalog, manifest, and status discoverability surfaces.
- Index workspace map: `C:\dev\public`, generated `2026-06-28T17:29:42-07:00`.
- Index public workspace `repo_count: 52`, public repos 48, local repos 4.
- Index public workspace `root_sha256_prefix: 92ef331e0850ccf6`.
- Index whole development workspace map generated `2026-06-29T00:49:59-07:00`: 124 repositories, 114 public-class, 10 local-class, 93 dirty repositories, root SHA256 prefix `99e773d965f606c9`.
- Index whole operator-profile workspace map generated `2026-06-29T00:50:16-07:00`: 207 repositories, 49 public-class, 158 local-class, 240 dirty repositories, root SHA256 prefix `b79886309f93e63a`.
- Telos repo pre-checkpoint head `2894b72`, branch `main`; latest in-turn Index/forum refresh saw the active live `--gh-run` ci-triage edits.
- Studio Engine repo current branch `feat/two-way-loop`, head `ad27b08`, public origin `https://github.com/HarperZ9/studio-engine.git`.
- Reconcile repo current head `375d1f5`, branch `main`, public origin `https://github.com/HarperZ9/reconcile.git`.
- Forum route for the expanded mandate decided `project-telos` with no escalation; related lanes remain technical-writing, function-routing, data-ml, code-review, render-pipeline, shader-effects, and deep-research.
- Gather receipts were refreshed for large-context agent memory and rendering research.
- Telos workflow returned `MATCH` for the local five-flagship workflow and reports CLI, MCP, IDE, TUI, and application workbench next actions.
- Telos catalog now presents 69 available tools across the five flagships, including `telos.context.pack`, `telos.model.foundry`, `telos.learning.forge`, `telos.learning.labs`, `telos.mcp.freshness`, `telos.ci.doctor`, `telos.ci.triage`, `telos.presentation.doctor`, `telos.accessibility.doctor`, `telos.performance.doctor`, `telos.compatibility.doctor`, `telos.operator.doctor`, `telos.research.thermodynamic`, `telos.second_level.queue`, `telos.workstation.substrate`, `telos.native.control`, `telos.browser.evidence`, `telos.showcase.scout`, `telos.proof`, `telos.proof.research`, `telos.proof.visual`, and `telos.proof.build`.
- Four proof lanes now ship in Telos through one CLI, `node demo/proof.mjs`: agent-action (`project-telos.proof-packet/v1`, `telos.proof`), research-claim (`project-telos.research-proof-packet/v1`, `telos.proof.research`), visual-truth (`project-telos.visual-proof-packet/v1`, `telos.proof.visual`), and build scientific-runtime (`project-telos.build-proof-packet/v1`, `telos.proof.build`). Each lane assembles a canonical packet, verifies it with a pure verifier that recomputes every load-bearing claim from embedded materials and can return `DRIFT` or `UNVERIFIABLE`, and exports a proof-surface shape whose `decision_summary` is derived from the overall verdict. A canned `MATCH` is structurally impossible in every lane. The full delivery-order progress ledger is `docs/PROOF-LANES.md`.
- Browser Evidence Kernel now has a cross-repo smoke receipt at `demo/research/browser-evidence-smoke.json`: Telos owns `project-telos.browser-evidence/v1`; Gather, Index, Forum, Crucible, Learn, Emet, and BuildLang consume packet refs instead of duplicating browser stacks. The model-council path stays deliberate: deterministic local gates preserve refs and hashes first, then Index and Forum route richer browser context into council/review paths when uncertainty, complexity, or operator intent justifies the overhead. The smoke receipt tracks tokens spent, council calls, artifact dereferences, route confidence, and verdict rates as the local-vs-council efficiency baseline.
- The active flagship-state goal ledger is `docs/FLAGSHIP-STATE-GOAL.md`. The latest dogfood pass records Telos compatibility `MATCH`, Gather status `MATCH`, Index maps for `C:\dev\public` (52 repos, 2 dirty), `C:\dev\opsec` (5 repos, 0 dirty), and `C:\dev\state` (4 repos, 0 dirty), Forum routing to `project-telos`, Aleph private-line MCP config `MATCH`, and Gather source launcher commit `ab959c7` with green CI run `28459724472`.
- Native background control (`telos.native.control` / `node demo/native-control.mjs`) drives the browser via the Chrome DevTools Protocol and native apps via Windows UI Automation, delivering synthetic events into each target so the operator's physical cursor and keyboard stay free. The MCP tool is the read-only capability catalog; actuation runs locally through the CLI.
- The canonical connection and distribution map now lives at `docs/PROJECT-CONNECTION-MAP.md`. It treats the five flagships as the current organs and the wider HarperZ9 public repo corpus as Telos growth tissue.
- GitHub authenticated inventory checked 77 visible HarperZ9 repos: 47 public non-forks, 4 public forks, 25 private active repos, and 1 private archived repo. Private and local-only viability stays in ignored local packets until sanitized.
- Local-only viability now has public-safe revival records for `raw-native`, `studio-libs`, and `forum-archive`: deterministic renderer verification, studio perception organ, and orchestration archive. Raw local viability notes remain ignored and are not public evidence.
- The second-level flagship queue now tracks 15 public-safe candidates and 5 private/local-only lane families through `node demo/second-level-flagship-queue.mjs` and `telos.second_level.queue`. Public candidates carry README hashes; private/local-only details stay in ignored local packets.
- The workstation substrate register now tracks two aggregate local roots, 331 repositories, 163 public-class repos, 168 local-class repos, and 8 public-safe lane families through `node demo/workstation-substrate.mjs` and `telos.workstation.substrate`; raw private paths, filenames, payloads, credentials, signing material, and runbooks are excluded.
- Crucible current-state thesis `661f7d4089347607` assessed 5 claims: 5 `MATCH`, 0 `DRIFT`, 0 `UNVERIFIABLE`. Report: `docs/verification/2026-06-28-current-state-report.md`; run record: `docs/verification/2026-06-28-current-state-run.json`.

## Moving Target Rule

Project Telos is a moving target by design. Every serious pass must rerun Index and Forum before making project-level claims.

The minimum loop is:

1. Run Index over the active workspace and any named engine-lineage repos.
2. Run Forum route over the actual request, not a remembered label.
3. Record the timestamp, repo counts, dirty repos, routed lane, and confidence.
4. Update the relevant doc, plan, or ledger if the map changed.
5. Use Crucible to distinguish `MATCH`, `DRIFT`, and `UNVERIFIABLE` claims before public presentation.

Index and Forum are not decorative. Index keeps the physical workspace visible; Forum keeps the intent and lane assignment visible. Together they prevent a stale mental map from steering the engine.

## Five Flagship Spine

The five flagship tools are the forward-facing control spine:

- Gather: perception and research intake. It produces source receipts, rights-aware source leads, arXiv catalog digests, document digests, and run records.
- Index: workspace atlas and context envelope. It maps repos, dirty state, docs, and large-codebase context packets.
- Forum: orchestration and human-facing reasoning. It routes work, summarizes ledgers, and can clarify agent prose without adding facts.
- Crucible: verification pressure. It turns falsifiable claims plus measurements into `MATCH`, `DRIFT`, or `UNVERIFIABLE`, with recheckable receipts.
- Telos: the shared room and engine surface. It reconciles flagship outputs into action receipts, context envelopes, validated context packs, loop ledgers, model-foundry packets, Learning Forge packets, creative engine manifests, research packets, measurement layers, and provider-neutral MCP contracts.
- Telos Objective Monitor: a rewardspy-inspired objective health surface. It watches proxy scores, independent quality scores, objective components, and improvement windows so an agent workflow cannot look successful merely because the easiest metric rose.
- Telos Model Foundry: a bounded model-building and self-improving daemon lane. It treats hosted frontier models, local/open-weight runtimes, post-training labs, tools, context envelopes, evals, and receipts as one system, while explicitly not claiming independent frontier-lab pretraining capacity.
- Telos Learning Forge: a receipt-backed education and research-lab lane. It treats videos and channels as source leads until Gather captures metadata and transcripts, then turns current papers, official sources, benchmarks, toy labs, failure cases, Crucible gates, and executable lab contracts into reusable learning objects.

The five flagships must stay protocol agnostic. Each should remain usable as an individual CLI tool, an MCP server, an IDE or TUI tool, a plugin or superpower, and a full application component.

## Engine Lineage

Telos Engine is larger than the website Studio demo.

- `portfolio-site` contains the public Studio Showcase and the in-flight browser engine work: graph runtime, Canonical Media IR, format adapters, render planning, effects, transforms, and Studio presentation.
- `telos` contains the flagship action contracts, tool catalog, MCP manifest, action receipts, context envelopes, loop ledger, CI doctor, creative engine manifest, measurement layers, revival registry, second-level flagship queue, and workstation substrate register.
- `studio-engine` is part of the Telos Engine lineage. Its README describes a zero-dependency creative-verification engine that emits witnessed Worlds, render programs, audio programs, timelines, and receipts.
- `reconcile` is also part of the Telos Engine lineage. Its README describes a node/browser creative-verification engine where generated artifacts are perceived, judged against independent criteria, refined, composed, choreographed, and witnessed.
- `raw-native` is now a local-only revival candidate for deterministic renderer verification: CPU G-buffer rasterization, ray-traced AO oracle checks, SSAO comparison, bounded allocation, and witnessed certificates.
- `studio-libs` is now a local-only revival candidate for the studio perception organ: nD rendering, layered sense-core readouts, and a Node-stdlib MCP surface for render, perceive, and measure operations.
- `forum-archive` is now a local-only revival candidate for orchestration archive work: supervision-tree primitives, event/task scheduling, hashing, and compatibility diffing against current Forum.
- `second-level-flagship-queue` now holds the next wave before registry promotion: Reconcile, Studio Engine, Provenance Sensorium, Proof Surface, Model Provenance Validator, Public Surface Sweeper, Agent Routing Kit, Agent Hook Pack, Coherence Membrane, Workflow Harness Lite, Accountable Engine, Accountable Surface, Anomaly Kernels, Signal Kernels, and Rewardspy concept lane.

These repos should converge by contract, not by a rushed copy. The shared boundary is the World/media graph/receipt model: source, transform, criterion, rendered program, measurement, verdict, and replay reference.

## Current Engine Direction

The engine is becoming a universal media and research workbench:

- Creative: generative art, retro CGI, glitch, dithering, pixel sorting, plotter paths, typography, sound, film, image/video/audio timelines, and shader graphs.
- Science and mathematics: geometry, physics, dimensions, bundle-style representations, physical constants, measurement overlays, formal checks, and reproducible demonstrations.
- Machine learning: model-foundry orchestration, large-context context envelopes, local model runtime hooks, feasible post-training labs, memory layers, retrieval receipts, uncertainty measurements, eval gates, and model-observation records.
- Security and reliability: defensive find-and-fix, release scanning, redacted IO, proof indexing, agent audit, and open-source patch demonstration packets.
- Frontier R&D: advanced computation, AI/ML, mathematics, physics, biology, medicine, robotics, cybernetics, quant, finance, color/rendering/scientific compute, nuclear and energy systems, and defense-adjacent technology when the artifact is framed as research, measurement, safety, assurance, simulation, verification, education, or accountable tooling.

The ambition is intentionally large. The delivery posture remains bounded: live, prototype, planned, promotion-ready, promotion-candidate, and quarantine-and-adapt are different labels.

The active scope update is explicit: military-adjacent and defense-adjacent
frontier R&D are not excluded by default. The publication boundary is still
strict. Public artifacts must name source basis, measured claim, non-claims,
failure condition, safety-to-publish rationale, and internal/fenced details.

## Research Receipts

Fresh Gather receipts used in this pass:

- arXiv `2603.04428v1`, "Agent Memory Below the Prompt: Persistent Q4 KV Cache for Multi-Agent LLM Inference on Edge Devices", receipt seal `bc8b79bc308aea334c3005dd4f55047da18e8589a283b0bf9ceacac55de01093`.
- arXiv rendering digest seal `302e5fe3fc931ba06d25f527adec799cd1f59665951dab99a2d22966162eeade`, including `2308.04079v1` 3D Gaussian Splatting and `2402.13827v2` clustering unnecessary 3D Gaussians.
- Verified YouTube/Gather packet for "The Thermodynamic AI Chip - Thomas Ahle": metadata `MATCH`, transcript `MATCH`, transcript item hash `40a31546b7a391bbb016ba4e3b86a06fc4027636ab85831a0be8b8ca44d6fc56`, digest seal `77bd2c9c39aa0628238f074efe3cd2a3ef64c7d7a373cec23128845f215a59a6`. Telos records this as `telos.research.thermodynamic`, with public-source Normal Computing-adjacent integration modules and explicit no-partnership/no-private-IP boundaries.
- Learning Forge packet for the supplied AI research video/channel seed corpus: `project-telos.learning-forge/youtube-research-seed/v1` records the links as `UNVERIFIABLE_UNTIL_GATHER_TRANSCRIPT`, joins current lawful source receipts for NeurIPS education/reproducibility/evaluation, planning-agent references, reasoning and software-agent benchmark papers, MCP, and observability, and routes next actions through Gather, Index, Forum, Crucible, and Telos.
- Learning Forge Labs packet: `project-telos.learning-forge/labs/v1` binds the gathered operator research packet to seven executable lab contracts: tiny autoregressive prediction, accuracy-per-token verification, MCP action receipts, coding-agent contamination checks, explanation faithfulness, spec representation, and stochastic-compute measurement. The Gather docs receipt for the attachment is SHA256 `a022fa3b8ea3d277b97bc058444a7757c90e92b81f06bd90f233d8f2ed66ac48`, digest seal `bc983de187794519b6ab83c9d4c851e458791d9911eecf8b1445551e038f2856`.
- TI Morse / Relentless field-intake packet: `project-telos.research-intake/youtube-field-scope-receipts-v1` records five video metadata/transcript receipts and one bounded channel-list receipt under `demo/research/youtube-ti-morse-field-receipts.json`. It maps industrial science proof packets, causal research workbench, agentic benchmark foundry, and compute/infrastructure ledger as inferred megatool lanes while keeping all domain correctness claims `UNVERIFIABLE_UNTIL_PRIMARY_SOURCE_OR_REPLAY`. Crucible assessed the bounded intake claims as `MATCH`; Learn reverified the prooflesson as `VERIFIED`.
- Causal Research Workbench preflight: `project-telos.causal-workbench/proof-packet-fixture/v1` records source-ledger arXiv metadata under `demo/research/causal-workbench-source-receipts.json` and a deterministic toy-DAG proof packet under `demo/causal-workbench-proof-packet.mjs`. The fixture emits `CAUSAL_DAG_FIXTURE_MATCH`, identifies `age + baseline_health` as the exact minimal adjustment set, rejects negative controls, and keeps causal discovery, LLM causal reasoning, biomedical, and BuildLang/buildc-native claims out of scope. Crucible assessed the bounded preflight claims as `MATCH`; Learn reverified the prooflesson as `VERIFIED` with witness SHA-256 `6e358d9ea652f8e5efee0882ca7046705dc1f1c23421763d9607dd3274b6ad35`.
- Embodied Sim-to-Real preflight: `project-telos.embodied-sim2real/proof-packet-fixture/v1` records source-ledger arXiv metadata under `demo/research/embodied-sim2real-source-receipts.json` and a deterministic differential-drive proof packet under `demo/embodied-sim2real-proof-packet.mjs`. The fixture emits `EMBODIED_SIM2REAL_FIXTURE_MATCH`, checks units, command logs, predicted and observed traces, safety envelope, latency, and five negative controls, while keeping real robot safety, surgical/medical, foundation-model, large-scale sim-to-real, and BuildLang/buildc-native claims out of scope. Crucible assessed the bounded preflight claims as `MATCH`; Learn reverified the prooflesson as `VERIFIED` with witness SHA-256 `258663c0dd0d647de661602ceaeb00771a1a750a478ddb562bf21c0af71c7d6a`.
- Quantum Error-Correction preflight: `project-telos.quantum-error-correction/proof-packet-fixture/v1` records source-ledger arXiv metadata under `demo/research/quantum-error-correction-source-receipts.json` and a deterministic 3-qubit bit-flip stabilizer proof packet under `demo/quantum-error-correction-proof-packet.mjs`. The fixture emits `QEC_STABILIZER_FIXTURE_MATCH`, checks no-error and single Pauli-X recovery for both logical basis states, rejects or marks unverifiable five negative controls, and keeps surface-code, hardware QEC, fault-tolerant computation, quantum advantage, cryptographic, and BuildLang/buildc-native claims out of scope. Crucible assessed the bounded preflight claims as `MATCH`; Learn reverified the prooflesson as `VERIFIED` with witness SHA-256 `3093cea9b0746b052dba844a6745cdba1d11ae836be5468503af41f93c4702f3`.

Local research inputs used in this pass:

- `local-download:deep-research-report1.md`, SHA256 `BA705626D31A8F157896A28381F68B97C13928582B0BD4B1E3E09639D92EC0F3`.
- `local-attachment:148000af-2094-47bc-9ca7-f11836176987/pasted-text.txt`, SHA256 `9ABF17D60018810D44CD015E733446E9FBEE301CC70CC89E4652EAE01CF9731E`.
- `local-attachment:96becef4-d943-468f-a079-ea06ea4ab6a0/pasted-text.txt`, Gather SHA256 `dc6780ba0e52f00a3e734d15082a539bb2c340a26b9c7048e967ca00c945fdc1`, digest seal `43aa038825eea817a3eb362cb8b54056a8a04ac13d00c91746e6749440ab7edd`.
- `local-attachment:773e5613-c40e-44b7-b041-3ee739b0c53c/pasted-text.txt`, Gather SHA256 `4aa65ce9bdafb9a8a5f3632b13d5085f4d5d56374398200d0c75033901192990`, digest seal `dc240ab440dd74e53f121945b52638a1630717f0570cbec38afb9a3b00600414`.
- `local-attachment:919198d0-8a63-4be7-b133-be98ec3fa74b/pasted-text.txt`, Gather SHA256 `3659d9e2fc1fd8a3ac46c0bb9534307e0aaba422f838fc4c416a09baae0b8581`, digest seal `5518523e1064ee8fa82e4c425632149a24e284a8bd9997a614ac03e110f4818d`.
- `local-attachment:80840147-31f9-47cd-845e-321223462342/pasted-text.txt`, Gather SHA256 `a022fa3b8ea3d277b97bc058444a7757c90e92b81f06bd90f233d8f2ed66ac48`, digest seal `bc983de187794519b6ab83c9d4c851e458791d9911eecf8b1445551e038f2856`.

Protocol sources already represented in the Telos MCP server manifest:

- MCP 2025-06-18 specification: https://modelcontextprotocol.io/specification/2025-06-18
- OpenAI Agents SDK MCP docs: https://openai.github.io/openai-agents-python/mcp/
- OpenAI Apps SDK MCP server guide: https://developers.openai.com/apps-sdk/build/mcp-server
- Anthropic Claude Code MCP docs: https://docs.anthropic.com/en/docs/claude-code/mcp

The MCP freshness lane turns a live dogfood failure into a host contract: a loaded MCP server can be stale even when the source tree and tests are current. Hosts should compare the manifest's status tool, expected version, expected current-status string, `tools/list` hash, and declared behavior probes before trusting tool output; `node demo/mcp-freshness.mjs --observed observed.json` returns `project-telos.mcp-freshness-observation/v1` with `MATCH`, `DRIFT`, or `UNVERIFIABLE`. The current behavior probes include broad Telos routing, private-line Telos routing, focused Index context envelopes, and portable private-line Index maps. Drift becomes `stale_mcp_server`, `tool_surface_drift`, `version_drift`, or `behavior_probe_drift`; missing probe payloads become `freshness_probe_unavailable` instead of an invisible operator surprise.

The CI doctor lane turns GitHub Actions runtime and action-major drift into a native receipt. `node demo/ci-doctor.mjs --summary` records five latest flagship CI runs, 9 workflow files, Node 24 migration markers, first-party action-major baselines, and failure routes through `telos.ci.doctor`; `node demo/ci-doctor.mjs --scan-root .. --summary` rescans local flagship workflow files into `project-telos.ci-doctor-workflow-observation/v1`. Raw logs, tokens, secrets, private paths, workflow bodies, workflow mutation, and GitHub writes are excluded.

The CI triage lane turns failed GitHub Actions logs into a native routing receipt. `node demo/ci-triage.mjs --summary` handles offline fixture packets; `node demo/ci-triage.mjs --gh-run owner/repo#run_id --summary` uses live read-only `gh run view` metadata and logs. Both modes distinguish blocking failures such as doctest/test-gate and Rust format failures from non-fatal Node runtime migration warnings, then emit `MATCH`, `DRIFT`, or `UNVERIFIABLE` as `telos.ci.triage`. Raw logs, tokens, secrets, private paths, workflow mutation, and GitHub writes are excluded; only hashes, redacted excerpts, typed failure codes, warning codes, GitHub run state, and route hints leave the triage boundary.

The presentation doctor lane turns five-flagship README, changelog, and brand-asset parity into a native receipt. `node demo/presentation-doctor.mjs --summary` scans sibling source checkouts for shared Project Telos navigation, hero art, CI/version/license badges, operator-surface/current-status text, changelog freshness, and brand assets, then emits `MATCH`, `DRIFT`, or `UNVERIFIABLE` as `telos.presentation.doctor`. Raw document bodies, absolute paths, private paths, GitHub queries, and filesystem writes are excluded.

The accessibility doctor lane turns Studio HTML quality into a native receipt. `node demo/accessibility-doctor.mjs --summary` checks language, viewport, skip links, main/navigation landmarks, focus-visible styles, reduced-motion handling, responsive media, canvas names/fallbacks, button types, interactive state, labeled controls, and live regions, then emits `MATCH`, `DRIFT`, or `UNVERIFIABLE` as `telos.accessibility.doctor`. Raw HTML, absolute paths, browser automation, external fetches, and filesystem writes are excluded.

The performance doctor lane turns Studio efficiency and host-embedding posture into a native receipt. `node demo/performance-doctor.mjs --summary` checks HTML byte budget, inline style budget, script count, head-blocking scripts, external scripts/stylesheets, approved external hosts, font-display policy, external font budget, canvas/media dimensions, inline handlers, reduced motion, and autoplay, then emits `MATCH`, `DRIFT`, or `UNVERIFIABLE` as `telos.performance.doctor`. Raw HTML, absolute paths, browser automation, external fetches, and filesystem writes are excluded.

The compatibility doctor lane turns platform-agnostic host integration into a native receipt. `node demo/compatibility-doctor.mjs --summary` checks catalog and manifest schemas, stdio and streamable HTTP declarations, Codex/Claude/OpenAI host exports, source-checkout and package profiles, expected-tool joins, CLI fallbacks, MCP availability, freshness status tools, freshness failure codes, HTTPS protocol sources, and private-path hygiene, then emits `MATCH`, `DRIFT`, or `UNVERIFIABLE` as `telos.compatibility.doctor`. Raw catalog bodies, raw manifest bodies, absolute paths, browser automation, external fetches, and filesystem writes are excluded.

The operator doctor lane turns discoverability into a native receipt. `node demo/operator-doctor.mjs --summary` checks README quick start, status commands, catalog/MCP parity, CI doctor coverage, current-state tool counts, host-surface language, and next-action guidance, then emits `MATCH`, `DRIFT`, or `UNVERIFIABLE` as `telos.operator.doctor`. Raw docs, raw status payloads, raw catalog bodies, raw manifest bodies, absolute paths, external fetches, and filesystem writes are excluded.

## Operating Posture

The next layer is not one monolithic rewrite. It is a shared
source-to-context-to-action-to-verdict workflow:

Gather collects lawful, source-labeled inputs. Index maps the relevant code and context. Forum routes the task and keeps the operator-facing language legible. Crucible pressures the claims. Telos binds the result into receipts, ledgers, engine artifacts, and integration contracts.

The rewardspy concept now feeds back into that loop through `telos.objective.monitor`: a workflow can record proxy quality divergence, component dominance, ceiling saturation, steps since improvement, and quality variance collapse as typed signals. Forum can route those signals; Crucible can pressure them; Index can carry them by reference in context envelopes; Telos can join them to loop ledger entries.

The model-foundry lane sits one layer above that. A self-improving daemon should gather fresh evidence, index context, route one bounded improvement, admit one action, execute one patch or experiment, run Crucible, inspect objective drift, and promote only `MATCH`. `DRIFT` blocks; `UNVERIFIABLE` requests more evidence or human review. This is the shape that can improve models and model workflows without becoming blind self-training.

When the project adds a new renderer, model adapter, research source, OSS patch workflow, or creative organ, it should enter through that loop.

The consolidation layer now adds a corpus-control plane: docs, nested repo
research, scratch artifacts, local-only packets, official papers, whitepapers,
site pages, and proof demos should be classified before publication. Public
docs use the labels `public-index`, `public-official`, `public-whitepaper`,
`proof-demo`, and `paper-candidate`. Internal or risky source payloads use
`internal-source`, `quarantine-and-adapt`, or `deprecated-lineage` until a
sanitized release shape exists.

The machine-readable registry now makes that classification explicit in
`docs/registry/documentation-registry.json`, and the publication queue ranks
BuildLang scientific runtime receipts, causal research workbench, and agent
action proof packets as the first Tier-A methods pushes. QEC, embodied
sim-to-real, hyphal context, formal replay, and color/rendering remain proof
demo hardening lanes. Ti Morse industrial science, biology network
intelligence, microscopy/materials, and AI-scale economics remain source-led
domain-expansion lanes until primary sources or replayed experiments promote
one claim at a time.

The first cross-repo public-doc catalog now scans 54 top-level Git repos under
`C:\dev\public` and counts 909 Markdown/RST docs. It separates seven lanes:
research/philosophy corpus, five-flagship spine, supporting tooling,
agent-accountability organs, Build ecosystem, proof/witnessing, and
creative/rendering engine. The highest-priority subregistries are
`telos` plus the now-created `senses-and-sensibility`, `emet`/`proof-surface`,
and Build ecosystem registries.

The Senses and Sensibility research/philosophy corpus now has its own
subregistry. It records 172 Markdown/RST docs, 1 preserved `.txt` source file,
125 dissertation docs, 4 submission docs, and a clean local repo that is one
commit behind `origin/main`. The current boundary is strict: Senses can motivate
Telos vocabulary around accountability, human gates, authorship, provenance,
authn/authz separation, and proof-before-trust, but it is not a shipped tool
capability, not philosophical proof, and not publication-ready scholarship. The
subregistry also records referenced-missing curation artifacts that must be
restored or corrected before stronger publication cleanup.

The Build ecosystem now has its own subregistry. It records 10 top-level
Build-adjacent repos, 115 top-level Build docs, 131 BuildLang lineage docs
under `pubscan/quantalang`, and 11 planning rows. The current split is:
BuildLang/buildc as the receipt-bearing compute layer; Build Universe as the
alpha module and domain ledger; Build Color and Calibrate Pro as
color/rendering measurement lanes; Build Finance, Build Oracle, and Build
Engine as quant/forecasting lanes with non-advice gates; Build UI, VS Code, and
TextMate grammar as support surfaces.

The proof/witnessing layer now has its own subregistry. It records 5 repos, 112
docs, and 5 layer rows: EMET as witness, Proof Surface as validator contract,
Repo Proof Index as index, Proof Surface Report as report renderer, and
Witnessing Spine as theory corpus. The first Telos bridges are agent action
proof packets, research claim packets, visual measurement packets, and
AI4Science packets. These are planning and integration rows, not release,
compliance, safety, or product-capability approvals.

The Telos repo now has its own subregistry. It records 94 repo Markdown/RST
docs, 150 docs Markdown/JSON/RST files, 198 demo MJS/JSON/MD files, 7 official
research docs, 7 whitepaper research docs, 12 outreach docs, 61 outreach
receipt JSON files, and 13 research receipt JSON files. The split is explicit:
front-door docs are navigation and stable demo claims; control-plane docs
describe strategy with claim-state labels; research docs stay behind
publication gates; demos prove bounded fixtures only; outreach copy is not
evidence; receipt stores are cited by digest and typed packet; caches and raw
payloads remain internal or quarantined. The first Telos repo gates are the
commit-boundary publication gate, receipt-index bridge, outreach-to-official
claim gate, and cache/raw payload quarantine.

The causal workbench lane now provides the first replayable causal-claim
preflight. Its next promotion target is a synthetic SCM with known treatment
effect, estimator receipts, negative controls, Crucible gates, Learn exercises,
and a BuildLang/buildc typed DAG runtime.

The embodied sim-to-real lane now provides the first replayable robotics-claim
preflight. Its next promotion target is a BuildLang/buildc typed-unit
differential-drive replay, then a manipulation fixture with object pose, contact
state, action budget, safety envelope, negative controls, and Learn exercises.

The quantum error-correction lane now provides the first replayable
quantum-claim preflight. Its next promotion target is a BuildLang/buildc typed
Pauli/stabilizer runtime, then a small surface-code syndrome fixture and a
Clifford-circuit equivalence checker with explicit resource-estimation
non-claim gates.
