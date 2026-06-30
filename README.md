<p align="center">
  <img src="docs/brand/telos-hero.png" alt="Project Telos, shared AI workspaces for creation, simulation, and verification">
</p>
<!-- Project mark: docs/brand/telos-mark.svg -->

# Project Telos

> Create, simulate, verify, and replay work with AI.

[Project Telos](https://harperz9.github.io) | [gather](https://github.com/HarperZ9/gather) | [crucible](https://github.com/HarperZ9/crucible) | [index](https://github.com/HarperZ9/index) | [forum](https://github.com/HarperZ9/forum) | [telos](https://github.com/HarperZ9/telos)

![node: 24 CI, 20+ registry](https://img.shields.io/badge/node-24%20CI%2C%2020%2B%20registry-blue.svg)
![CI](https://github.com/HarperZ9/telos/actions/workflows/ci.yml/badge.svg)
![version: 0.1.0](https://img.shields.io/badge/version-0.1.0-informational.svg)
![deps: none](https://img.shields.io/badge/deps-none-success.svg)
![license: fair-source](https://img.shields.io/badge/license-fair--source-blue.svg)

## Try it

Zero dependencies. Use Node 20 or newer for registry and Docker parity; CI currently runs on Node 24.

```bash
node demo/run.mjs
node demo/catalog.mjs --summary
node demo/server-manifest.mjs --summary
node demo/ci-doctor.mjs --summary
node demo/ci-triage.mjs --summary
node demo/ci-triage.mjs --gh-run HarperZ9/seed#28353077838 --summary
node demo/presentation-doctor.mjs --summary
node demo/accessibility-doctor.mjs --summary
node demo/performance-doctor.mjs --summary
node demo/compatibility-doctor.mjs --summary
node demo/operator-doctor.mjs --summary
node demo/context-envelope.mjs
node demo/context-pack.mjs
node demo/action-receipt.mjs
node demo/loop-ledger.mjs
node demo/model-foundry.mjs --summary
node demo/learning-forge.mjs
node demo/learning-forge-labs.mjs --summary
node demo/thermodynamic-ai-chip-receipt.mjs
node demo/rendering-research.mjs
node demo/rendering-capabilities.mjs --summary
node demo/measurement-layers.mjs --summary
node demo/creative-engine.mjs
node demo/creative-kernels.mjs --summary
node demo/revival-registry.mjs --summary
node demo/second-level-flagship-queue.mjs --summary
node demo/workstation-substrate.mjs --summary
node demo/display-calibration.mjs --summary
```

Open the visual certificate-loop surface at [`demo/index.html`](demo/index.html).
Use `node demo/catalog.mjs --summary` for a compact operator map of the CLI and MCP surface.
Use `node demo/server-manifest.mjs --summary` for the five-server MCP launch map.
Use `npm start` or `node demo/telos-mcp.mjs` to run the Telos stdio MCP server for registry and host introspection.
Use `node demo/mcp-freshness.mjs --observed observed.json` to turn host-loaded MCP state, including declared behavior probes, into a `MATCH`, `DRIFT`, or `UNVERIFIABLE` freshness verdict.
Use `node demo/ci-doctor.mjs --summary` for the five-flagship GitHub Actions compatibility receipt: latest CI state, Node 24 migration markers, action-major baselines, and failure routes. Use `node demo/ci-doctor.mjs --scan-root .. --summary` to rescan local flagship workflow files without raw logs, GitHub writes, or workflow mutation.
Use `node demo/ci-triage.mjs --summary` for offline CI failure routing receipts, or `node demo/ci-triage.mjs --gh-run owner/repo#run_id --summary` for live read-only GitHub Actions intake. Fatal test/format/step failures are separated from Node runtime migration warnings before remediation is chosen.
Use `node demo/presentation-doctor.mjs --summary` for the five-flagship README, changelog, and brand-asset parity receipt. It scans sibling checkouts and emits `MATCH`, `DRIFT`, or `UNVERIFIABLE` without raw document bodies or absolute paths.
Use `python tools/audit_repo_presentation.py --root C:\dev\public` for the broader public/developer README presentation audit across local forward-facing repositories.
Use `node demo/accessibility-doctor.mjs --summary` for static Studio accessibility receipts: language, viewport, skip link, focus-visible, reduced motion, labeled controls, live regions, and canvas fallbacks without raw HTML or browser automation.
Use `node demo/performance-doctor.mjs --summary` for static Studio performance and efficiency receipts: byte budgets, script/style/font budgets, approved external hosts, media dimensions, motion/autoplay controls, and embedding-safe asset checks without raw HTML or browser automation.
Use `node demo/compatibility-doctor.mjs --summary` for protocol-agnostic host receipts: catalog and manifest schemas, CLI fallback coverage, MCP availability, host exports, freshness probes, HTTPS source refs, and private-path hygiene.
Use `node demo/operator-doctor.mjs --summary` for operator UX/discoverability receipts: README quick start, status command surface, catalog/MCP parity, CI coverage, current-state docs, host-language coverage, and next-action guidance.
Use `node demo/context-pack.mjs` for a runnable, budgeted, receipt-backed context packet with validation for large-codebase handoffs.
Use `node demo/action-receipt.mjs` for the durable external-write receipt contract: proposed intent, authority, execution, redacted evidence, review, compensation, trace joins, and typed failure codes without requiring raw private payloads.
Use `node demo/model-foundry.mjs --summary` for the bounded model-foundry and self-improving daemon contract: frontier orchestration where appropriate, local/open-weight runtimes where useful, post-training labs where feasible, and crucible-gated promotion.
Use `node demo/learning-forge.mjs` for the receipt-backed education and research-lab packet that turns video/channel/paper/benchmark leads into source refs, concept modules, failure cases, and Crucible gates while keeping YouTube claims `UNVERIFIABLE` until Gather captures metadata and transcripts.
Use `node demo/learning-forge-labs.mjs --summary` for the executable Learning Forge lab contract: tiny autoregressive prediction, accuracy-per-token verification, MCP action receipts, coding-agent contamination checks, explanation faithfulness, spec representation, and stochastic-compute measurement.
Use `node demo/rendering-capabilities.mjs --summary` for the WebGPU/WebGL/canvas/static renderer selection and fallback contract.
Use `node demo/measurement-layers.mjs --summary` for ten runnable meters across histogram, dither, splat, cluster, audio, flicker, curvature, interaction, uncertainty, and frame budget signals.
Use `node demo/creative-engine.mjs --summary` for the whole creation-engine contract: raster effects, sound, typography, math/physics, node graphs, revived organs, and receipts.
Use `node demo/creative-kernels.mjs --summary` for deterministic ordered-dither, pixel-sort, harmonograph, and clustered-light kernels.
Use `node demo/revival-registry.mjs --summary` for the first promotion registry of older, siloed, and frozen tools being pulled toward flagship status.
Use `node demo/second-level-flagship-queue.mjs --summary` for the public-safe queue of second-level flagship candidates discovered during whole-workstation substrate assessment.
Use `node demo/workstation-substrate.mjs --summary` for the public-safe aggregate intake map of the operator development and profile workspaces.
Use `node demo/display-calibration.mjs --summary` for the read-only Calibrate Pro and Quanta Color display-calibration contract.

## Why it matters

The hard part of AI work is not producing an answer. It is keeping sources, workspace state,
agent routes, action boundaries, measurements, and creative artifacts close enough that a
human or another system can re-check what happened. Telos is the workbench for that: a
local MCP surface that ties gather, index, forum, crucible, and telos into receipts,
manifests, ledgers, model-foundry lanes, creative engines, and public research packets.

## Work with it

Bring a workflow where the record matters: research intake, editorial claims, agent
routing, clinical-adjacent review, design pipelines, graphics/math/science demos,
due diligence, or any loop where an honest UNVERIFIABLE is worth more than a polished
guess. The useful next pressure is verification, testing against real workflows, early
traction from people willing to inspect receipts, collaborator feedback, and modest
grassroots research funding.

## What to test first

- Pick a workflow where a model answer is not enough: source intake, codebase handoff, agent action, creative export, or math/physics demo.
- Run the closest demo or packet and ask whether the receipt preserves the state a reviewer would need tomorrow.
- If the answer is no, the most useful feedback is the missing sensor, meter, receipt field, or replay handle. Telos should grow by making real workflows more inspectable, not by adding claims the record cannot support.

## Telos Creative Engine

The Studio is now presented as a whole creation engine, not only a visual demo. `node demo/creative-engine.mjs` returns the host-neutral manifest for generative art, retro CGI, raster effects, sound, film/media, typography, math/physics, node graphs, renderer capability probes, runnable sensor/measurement layers, deterministic creative kernels, and verification. It also records the old engine organs to revive next: `demo/render-nd`, `demo/render-sound`, `demo/sense-core`, `demo/viable-viz`, the sibling `studio-engine` raster/sonify/flowfield/harmonograph/WebAudio organs, and `studio-libs/render-sound`.

Every creative action should remain receipt-backed: scene specs, hashes, replay handles, and one of `MATCH`, `DRIFT`, or `UNVERIFIABLE`. `node demo/rendering-capabilities.mjs` keeps WebGPU Gaussian-splat/clustered prototypes, WebGL2 previews, Canvas 2D receipts, and static artifact fallbacks in one selectable contract. `node demo/measurement-layers.mjs` turns pixels, dither patterns, splat fields, light clusters, and waveforms into measurable packets before crucible verdicts. `node demo/creative-kernels.mjs` gives hosts a shared deterministic core for ordered dithering, pixel sorting, plotter paths, and clustered-light bins. The public demo uses Kilon for display typography and Conso for utility text while keeping purchased font files out of the repository.

The current research queue also includes receipt-only source leads from Inigo Quilez and adjacent math, physics, AI-progress, GPU-kernel, and educator videos under [`demo/research/youtube-math-educator-receipts.json`](demo/research/youtube-math-educator-receipts.json). Those leads shape the engine toward formula-visible, perturbable demos for mathematicians, physicists, shader artists, and teachers; video metadata is not promoted to scientific or benchmark evidence until stronger sources and crucible checks exist. The newer Learning Forge seed packet is gathered under [`demo/research/youtube-learning-forge-receipts.json`](demo/research/youtube-learning-forge-receipts.json), with eight video metadata/transcript receipts and two channel-list receipts kept separate from raw transcript bodies.

`node demo/thermodynamic-ai-chip-receipt.mjs` promotes the verified Machine Learning Street Talk interview with Thomas Ahle into a transcript-backed Telos research packet. The packet turns the discussion into a public-source integration lane for Normal Computing-adjacent work: spec representation, Verilog/formal receipts, stochastic simulation, uncertainty meters, and hybrid search/check loops. It records transcript themes as `MATCH`, treats Telos integration as `INFERRED`, and keeps Normal Computing, ProgramBench, and thermodynamic-chip technical correctness `UNVERIFIABLE_FROM_THIS_PACKET` until primary sources and independent checks promote them.

## Telos Model Foundry

The true model direction is not pretending this repo can reproduce frontier-lab pretraining on a workstation. `node demo/model-foundry.mjs` defines Telos as the foundry around models: hosted frontier APIs for hard tool-heavy work when policy and privacy allow, local/open-weight models for private or cheap work, feasible post-training experiments, typed MCP tools, lossless-by-reference workspace memory, and eval gates before any promotion.

The post-training lane now has an RL scaling receipt-spine target in [`docs/research/rl-scaling-receipt-spine.md`](docs/research/rl-scaling-receipt-spine.md). It uses current THUDM/slime repository metadata as a benchmark signal while keeping Telos focused on durable rollout, verifier, reward, compute, checkpoint, and promotion receipts rather than unverified training claims.

`node demo/learning-forge.mjs` is the research-to-teaching lane. It stores the supplied AI videos and channels as source leads, joins them to current lawful sources such as NeurIPS education/reproducibility/evaluation calls, planning-agent references, reasoning and software-agent benchmark papers, MCP, and observability specs, then defines labs with failure cases and Crucible gates. It does not promote video-specific claims until Gather has metadata and transcript receipts.

`node demo/learning-forge-labs.mjs` turns that lane into seven executable lab contracts. Each lab has source refs, a runnable command, expected artifacts, failure cases, measurement metrics, and a five-flagship flow across Gather, Index, Forum, Crucible, and Telos. The attached operator research packet is represented by digest receipt only; raw video, raw transcripts, and raw attachment text stay out of the repository.

The self-improving daemon lives here as a bounded loop. It gathers fresh evidence, indexes the workspace, routes one improvement, admits one action, executes one patch or experiment, runs crucible, checks objective drift, and promotes only `MATCH`. `DRIFT` blocks; `UNVERIFIABLE` asks for evidence instead of training itself on a guess.

## Legacy Tool Revival

`node demo/revival-registry.mjs` is the first promotion registry for the older and frozen tools that should stop living as isolated experiments. It currently pulls Calibrate Pro, Quanta Color, QuantaLang/quantac, WARDEN security lineage, Agent Audit, Context Curator Lite, Secret Redact IO, Repo Proof Index, Release Surface Scanner, GPU Trace Validator, raw-native, studio-libs, and the Forum archive into explicit Telos lanes with origin paths, Gather-backed README digests, risk boundaries, flagship hosts, and next actions. The local-only entries are sanitized lane records only; raw private viability notes stay outside the repository.

`node demo/second-level-flagship-queue.mjs` is the next wave. It records 15 public-safe candidates: Reconcile, Studio Engine, Provenance Sensorium, Proof Surface, Model Provenance Validator, Public Surface Sweeper, Agent Routing Kit, Agent Hook Pack, Coherence Membrane, Workflow Harness Lite, Accountable Engine, Accountable Surface, Anomaly Kernels, Signal Kernels, and the Rewardspy concept lane. Private/local-only work is reduced to lane families. Those candidates move into the active registry only after an adapter, fixture, or crucible-verifiable claim exists.

`node demo/workstation-substrate.mjs` is the broader workstation intake register. It records aggregate Index counts for the operator development and profile roots, then reduces sensitive local material into lane families such as local-only prototypes, agent/plugin caches, temp fixtures, release assurance, creative media, research attachments, and sensitive corpora. It intentionally excludes raw private paths, filenames, payloads, credential material, signing artifacts, and runbooks.

The first rule is visibility before transplanting: a dormant tool gets a lane, a source receipt, a privacy boundary, CLI/MCP or adapter roadmap, tests, and a target host before shared code becomes a runtime dependency. Calibrate Pro and Quanta Color become the display-calibration and color-science lane for Telos measurement layers. Context Curator Lite becomes the context-envelope source for token-efficient large-workspace handoffs. QuantaLang becomes the effects-language candidate for creative kernels. WARDEN is carried forward only as defensive, authorized, good-faith find-and-fix lineage with synthetic labs and maintainer-friendly patch workflows.

`node demo/display-calibration.mjs` is the first promoted Calibrate Pro lane. It defines a read-only `project-telos.display-calibration/v1` packet for display targets, color spaces, patch sets, ICC/LUT/report artifact refs, Quanta Color metrics, privacy boundaries, and crucible measurement gates. It does not call DDC/CI, mutate monitor settings, apply LUTs, write ICC files, or require raw private device telemetry.

## Current status

- **Release:** `0.1.0` source registry package; command surface is `node demo/run.mjs`, `node demo/room.mjs`, `node demo/status.mjs`, `node demo/doctor.mjs`, `node demo/catalog.mjs`, `node demo/server-manifest.mjs`, `node demo/mcp-freshness.mjs`, `node demo/ci-doctor.mjs`, `node demo/ci-triage.mjs`, `node demo/presentation-doctor.mjs`, `node demo/accessibility-doctor.mjs`, `node demo/performance-doctor.mjs`, `node demo/compatibility-doctor.mjs`, `node demo/operator-doctor.mjs`, `node demo/admission-telemetry.mjs`, `node demo/context-envelope.mjs`, `node demo/context-pack.mjs`, `node demo/action-receipt.mjs`, `node demo/loop-ledger.mjs`, `node demo/model-foundry.mjs`, `node demo/learning-forge.mjs`, `node demo/learning-forge-labs.mjs`, `node demo/research-seed.mjs`, `node demo/thermodynamic-ai-chip-receipt.mjs`, `node demo/rendering-research.mjs`, `node demo/rendering-capabilities.mjs`, `node demo/measurement-layers.mjs`, `node demo/creative-engine.mjs`, `node demo/creative-kernels.mjs`, `node demo/revival-registry.mjs`, `node demo/second-level-flagship-queue.mjs`, `node demo/workstation-substrate.mjs`, `node demo/display-calibration.mjs`, and `node demo/flagship-workflow.mjs`.
- **Operator surface:** `node demo/telos-mcp.mjs` exposes native MCP tools: `telos.status`, `telos.doctor`, `telos.room`, `telos.catalog`, `telos.workflow`, `telos.server.manifest`, `telos.mcp.freshness`, `telos.ci.doctor`, `telos.ci.triage`, `telos.presentation.doctor`, `telos.accessibility.doctor`, `telos.performance.doctor`, `telos.compatibility.doctor`, `telos.operator.doctor`, `telos.admission.telemetry`, `telos.context.envelope`, `telos.context.pack`, `telos.action.receipt`, `telos.loop.ledger`, `telos.objective.monitor`, `telos.model.foundry`, `telos.learning.forge`, `telos.learning.labs`, `telos.research.seed`, `telos.research.thermodynamic`, `telos.rendering.research`, `telos.rendering.capabilities`, `telos.measurement.layers`, `telos.creative.engine`, `telos.creative.kernels`, `telos.revival.registry`, `telos.second_level.queue`, `telos.workstation.substrate`, `telos.display.calibration`, and `telos.native.control`.
- **Current floor:** the operator room reconciles 63 preferred tools plus 12 declared auxiliary compatibility tools across gather, crucible, index, forum, and telos, with a provider-neutral catalog, executable server manifest, MCP freshness verifier, CI doctor for GitHub Actions runtime/action drift, CI triage for separating fatal gates from runtime warnings, presentation doctor for README/changelog/brand parity, accessibility doctor for Studio host quality, performance doctor for static byte/asset/embed budgets, compatibility doctor for protocol and host parity, and operator doctor for discoverability parity across CLI, MCP, plugin, IDE, TUI, and app hosts. See [CHANGELOG.md](CHANGELOG.md).
- **Brand renderer:** `python tools/render_flagship_heroes.py --check-existing --public-root ..` verifies the five README hero PNGs and brand receipts without redistributing the operator-owned fonts.

## What it is

A language model is brilliant and forgetful in the same breath. It can reason its way through a hard problem inside one window of text, then lose the thread the moment the answer depends on something it cannot see. What changed. What is true right now. What it itself did a minute ago. It does not know, and worse, it does not know that it does not know. The confidence stays high while the accuracy quietly falls away.

Project Telos is the work of giving a model the footing it is missing: a durable memory it can read instead of guess at, real senses pointed at the world, a way to act with the brakes wired in, and underneath all of it, a way to check its own work before you are asked to trust it.

In practical terms, this is the Difference Engine / Analytical Engine idea pointed at agent work. The gears are not brass; they are ledger entries, context envelopes, admission decisions, action receipts, and replayable verification. A fresh context reads durable loop state, advances one action, writes evidence and a verdict, then stops or resumes from the ledger rather than from vibes.

## What goes wrong without it

A transformer is a function over a window of tokens. It has no live memory of state, no values it can look up, no record of the order things happened in. So it is steady on self-contained logic and blind on everything else: long-running state, and the quiet bounds that hold a system together. A depth that has to stay between zero and one. A count that cannot go negative. A buffer that did not overflow.

The expensive failure is not that the model is sometimes wrong. Everything is sometimes wrong. The failure is that its confidence does not fall when its accuracy does. A confident mistake reads exactly like a confident truth, and you find out which was which downstream, if you ever find out at all.

## The shape of the fix

You cannot train the overconfidence out of a model, so Telos does not try. It builds the missing organs around the model instead.

- A **memory** it reads from rather than recalls. An addressable store, not a fading impression.
- **Perception** that turns ground truth into bytes and pins where those bytes came from.
- **Action with impedance**, where an effect is checked against the rules before it is allowed to land.
- **A clock**, so every fact carries the time it was true.

Put together, these form a membrane between a stateless mind and a changing world. Nothing reaches the model as fact unless the store witnessed it. Nothing leaves the model as an effect unless the rules allow it. You do not verify the model, because you cannot. You verify the membrane.

## The part you can run

The trust in all of this rests on one small loop, and it is small on purpose.

```
perceive an artifact,
then recover the invariant that has to hold,
then check it against a criterion the model did not author,
then return one of three answers: MATCH, DRIFT, or UNVERIFIABLE.
```

There is no fourth answer, and there is deliberately no TRUSTED. When the loop cannot verify something, it says UNVERIFIABLE and stops, rather than hand back a guess wearing the costume of an answer. The certificate it produces re-checks from its own evidence, so you believe it by re-running it, not because it told you to.

## Run it

Zero dependencies. Use Node 20 or newer for registry and Docker parity; CI currently runs on Node 24.

```
node demo/run.mjs
```

It renders a four-dimensional cube, perceives it two independent ways, checks what it recovered against the true count of vertices and edges, and prints a certified result that re-checks. Then it does the more important thing. It feeds the loop a render too small and broken to read, and shows it returning UNVERIFIABLE instead of a confident pass. A verifier that cannot fail is not a verifier, and this one fails honestly.

```
RUN A   an honest 4-D cube render        ->  CERTIFIED      recheck = true
   criterion : 16 vertices, 32 edges         (the external truth the loop did not author)
   recovered : 16 vertices, 32 edges         (exact match)

RUN B   a render too small to read (8x8) ->  UNVERIFIABLE   recheck = true
   the two perceptions cannot agree, so the loop refuses to certify.
   it reports UNVERIFIABLE rather than lean on the reading that happens to be right.
```

## Try it in the field

The fastest test is to bring Telos a workflow where a model answer is not enough; a person needs to see what happened and re-check it later.

- **Doctor / clinical admin:** source fragments, routing decisions, and uncertainty stay visible before a summary or recommendation becomes action.
- **Artist / studio:** prompts, source assets, transforms, chosen branches, and export gates stay attached to the finished artifact.
- **Media / newsroom:** public claims map back to witnessed sources, conflict notes, and an editorial decision ledger.
- **Token economy / routing:** model calls are spent where they buy evidence, coverage, or verification, not where they merely produce confident prose.
- **Reasoning:** the model can perceive and propose; final authority belongs outside the model, in a checkable record a person can inspect.

Main site: <https://harperz9.github.io>. GitHub: <https://github.com/HarperZ9>. Flagship repos: [gather](https://github.com/HarperZ9/gather), [crucible](https://github.com/HarperZ9/crucible), [index](https://github.com/HarperZ9/index), [forum](https://github.com/HarperZ9/forum), and [the Telos engine](https://github.com/HarperZ9/telos).

I am looking for verification, testing against real workflows, early traction from people willing to inspect receipts, and possibly modest grassroots research funding or pointers.

## Why AlphaZero is the right comparison

This shape is not new, and the clearest proof of that is AlphaZero. A single neural network sits at its center, a stateless prior that guesses good moves and guesses who is winning. On its own it plays well and no better. What makes it superhuman is the search bolted on beside it, an outside process you can re-run that tests the network's guess against the actual rules of the game before it commits to a move. The network proposes. The search verifies.

Line the pieces up and Telos is the same machine, pointed at work that is not a game. The network's guess is the model's cheap output. The search is the reconcile loop. The rules of the game are the external criterion. And the way AlphaZero takes risk in proportion to what the search has actually checked is the way Telos extends trust in proportion to what re-derives.

Prof. Mihai Nica walks through this plainly in his AlphaZero Explained series, where the search is shown as a kind of visible thinking budget you can look inside, and the whole method comes down to, in David Silver's words, "three steps and literally nothing else." The plainness is the point. It is a small, legible loop, not a mystery.

## Who it is for

- People handing real work to AI agents who want a receipt for it. What changed, checked before and after, and re-checkable later, instead of trust by reputation.
- People building agent loops who want the checking step grounded in something outside the model. Self-critique with no outside standard just agrees with itself.
- Anyone who would rather hear an honest "I cannot verify this" than a confident answer that turns out to be invented.

## The bricks

The flagship is the mission. These open pieces are the bricks it is built from, and you can pick any of them up on its own. Treat the repo tests and receipts as the current evidence instead of relying on frozen maturity counts in prose.

- **[coherence-membrane](https://github.com/HarperZ9/coherence-membrane)** turns a render or a frame into MATCH, DRIFT, or UNVERIFIABLE. It is dependency-light and test-backed.
- **[accountable-surface](https://github.com/HarperZ9/accountable-surface)** is the full loop of perceive, gate, and act, with tests covering the loop behavior.
- **[EMET](https://github.com/HarperZ9/emet)** is an outside witness built on a perceptual hash and a content hash, with the same answer reproduced in two independent languages.
- **[reconcile](https://github.com/HarperZ9/reconcile)** is the bare primitive, with worked examples for novelty and structural fitness.
- **[studio-engine](https://github.com/HarperZ9/studio-engine)** generates structures to perceive, behind a small REST API.
- The **engine** the demo runs on renders, perceives, and reconciles. It is kept local for now while the five above are public.

These are open and tested on GitHub. They are not yet packaged for pip or npm.

For the full picture, read [the connection map](docs/PROJECT-CONNECTION-MAP.md), [how it works](docs/HOW-IT-WORKS.md), [the architecture](docs/ARCHITECTURE.md), and [who uses it](docs/WHO-USES-IT.md).

## What it does not claim

This is early, and it earns trust by being clear about where it stops.

- The membrane decides what the model sees, not what it believes. A strong prior from training can still talk over a quietly staged fact, which is why the seal is placed on the way out, at the point of action, and not only on the way in.
- Passing every check means tripping no named failure, which is not the same as being correct. Coverage grows one caught bug at a time. The overconfidence is reduced, never erased.
- It works on a world you can pause and replay. It is a body for recorded, steppable state, not for real time control.
- A verifier you have not verified is worse than none, because it lends a falsehood the authority of ground truth. The whole value sits in the word verified.

## Why it exists

In the author's own words, from a public comment.

> "building honest tools that keep my ADHD in check, an accountable research harness, an ecosystem of tools to help hold my work, and a model's work, to an accurate standard when my brain gets lost. The mission is to give a stateless LLM durable, verified contact with state and range."

## License

Project Telos is fair-source. The code is open to read and to run, free for nearly any use except building a competing product, and it converts to a fully open license two years after each release. The smaller bricks above are permissively open already. The aim is plain: keep the work in the open and in the hands of the people using it, while keeping the flagship able to fund the research it came from. Copyright is held by the author.

## For developers

Keep the public README, package metadata, and examples aligned with current behavior. Before opening a PR or pushing a release, run the local Node verification path.

```bash
npm install
npm test
```
