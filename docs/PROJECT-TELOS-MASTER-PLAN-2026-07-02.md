# Project Telos Master Plan

Date: 2026-07-02

Objective: turn the verified research corpus into the operating system for building a frontier-grade AI model and model ecosystem.

Roadmap appendix: `docs/PROJECT-TELOS-MASTER-PLAN-ROADMAP-2026-07-02.md`

## One-Sentence Thesis

Project Telos should build the most advanced AI model stack by making the model inseparable from proof: every source, context slice, tool action, learning step, compiler/runtime result, experiment, and claim promotion becomes receipt-backed, replayable, and falsifiable.

## Strategic Correction

Do not compete only on raw pretraining scale first.

Raw scale matters, but the immediate asymmetric advantage is a model-building substrate that produces better data, better tool use, better memory, better verification, better learning loops, and safer promotion gates than ordinary chat, agent, notebook, or eval stacks.

The model should be built around a proof operating system:

```mermaid
flowchart LR
  Sources["Sources and world data"] --> Gather["Gather"]
  Workspace["Code, docs, tools, state"] --> Index["Index"]
  Gather --> Forum["Forum"]
  Index --> Forum
  Forum --> Telos["Telos"]
  Telos --> Actions["Actions, tools, labs"]
  Actions --> Crucible["Crucible"]
  Crucible --> Emet["Emet witness"]
  Crucible --> Learn["Learn"]
  Learn --> Model["Model Foundry"]
  Build["BuildLang/buildc"] --> Actions
  Model --> Telos
```

## Core Product

The product is a proof-native model operating system:

- It gathers sources instead of guessing them.
- It indexes workspace state instead of relying on stale context.
- It routes tasks through explicit lanes instead of one ambiguous agent.
- It admits actions through receipts instead of letting side effects disappear.
- It runs verification before claim promotion.
- It turns failures and misconceptions into learning data.
- It compiles and runs scientific code with source, effect, backend, and measurement receipts.
- It asks an external witness to check source/view consistency before public promotion.

## System Pillars

### Gather: Perception

Role: source intake, web/API/PDF/feed ingestion, source stores, source hashes, and source demotion.

Build:

- A source adapter SDK for scholarly graphs, preprints, college repositories, biomedical registries, code/model hubs, climate sources, materials databases, and formal proof archives.
- A source quality ladder: source lead, metadata record, full text, dataset, executable artifact, formal proof, verified measurement.
- A source-store query API that can feed model context, model training data, proof packets, and buyer-facing evidence briefs.

Rule: Gather proves what was fetched, when, from where, and with what body hash. It does not prove claim truth by itself.

### Index: Context And Memory

Role: workspace map, context envelopes, dependency surfaces, fresh-state checks, and token-efficient memory.

Build:

- Path-scoped context envelopes for each domain foundry.
- Repo and artifact graph joins across Telos, Learn, BuildLang/buildc, Emet, and sibling tools.
- Training-data context packs: code, docs, tests, receipts, and verdicts, not raw folder dumps.
- Freshness checks that detect when a model is operating on stale assumptions.

Rule: the model should read addressable memory instead of relying on conversation recall.

### Forum: Routing And Council

Role: route tasks, expose ambiguity, escalate cross-domain work, and pick the right proof lane.

Build:

- New lane taxonomy: `frontier-foundry`, `research-foundry`, `model-foundry`, `scientific-runtime`, `formal-proof`, `bio-evidence`, `robotics-control`, `visual-truth`, and `learning-forge`.
- Multi-router output: one route for product, one for domain science, one for verification, and one for implementation.
- Routing receipts that become model supervision examples.

Rule: low-confidence routing is a useful signal. It should trigger decomposition, not conceal uncertainty.

### Telos: Action And Loop OS

Role: action receipts, loop ledger, model foundry, measurement layers, objective monitor, browser evidence, native control, display calibration, and MCP surface.

Build:

- `telos proof <lane>`: one command that emits a proof packet from sources, context, action, and verifier results.
- A loop ledger that can resume long-running research and model improvement without context collapse.
- Action admission contracts for external writes, code edits, browser actions, model calls, and lab/simulation runs.
- A model foundry supervisor that records prompt, tool, context, objective, output, verifier, and promotion status.

Rule: every meaningful model action should leave a durable receipt.

### Crucible: Falsification

Role: thesis, measurement, verdict, drift, match, unverifiable, and cleanroom verification.

Build:

- Standard measurement gates for proof packets, model evaluations, compiler results, learning receipts, simulations, and display/color measurements.
- Better `UNVERIFIABLE` UX: explain exactly what evidence is missing.
- A zero-tolerance validation warning before assessment when measurements are ill-posed.
- A registry of negative fixtures that prevents overclaim regressions.

Rule: `UNVERIFIABLE` is a successful honesty state, not a failure to hide.

### Learn: Human And Model Learning

Role: accountable study, mastery gates, spaced repetition, retrieval practice, self-explanation, misconception tracking, and learning receipts.

Verified local evidence: `C:\dev\public\learn\README.md` reports release 1.5.0, zero dependencies, 206 tests, receipt re-verification, tutor/study workflows, and MCP advisory tools.

Build:

- Learning packets generated from proof packets.
- Model curriculum from source leads, negative fixtures, and verified explanations.
- Human-in-the-loop mastery gates for research operators and domain contributors.
- A model training/eval data format that preserves source, answer, explanation, verifier, and misconception receipt.

Rule: Learn must never let the machine take the test for the learner. It should make real mastery visible.

### BuildLang/buildc: Scientific Runtime

Role: typed effects, source digests, policy receipts, compiler/runtime receipts, verified C backend, shader outputs, and future scientific/HPC/quant/security kernels.

Verified local evidence: `C:\dev\public\pubscan\quantalang\README.md` describes BuildLang/buildc as a Rust-built compiler for typed effects, C as the production verified backend, HLSL/GLSL shader output, experimental SPIR-V/LLVM/WASM/Rust/native backends, and experimental `#[linear]` no-cloning/resource work.

Build:

- `buildc check --receipt` packets that Telos can ingest directly.
- Scientific runtime receipts: source, type/effect policy, backend, input dataset, numerical method, seed, hardware, result, tolerance, and verifier.
- Negative fixtures for numerical drift, bad constraints, resource double-use, and backend maturity mismatch.
- A Julia-replacement wedge focused on accountability for rendering, mathematics, physics, quant, finance, security, and scientific compute.

Rule: BuildLang/buildc should not claim backend or linear-type soundness beyond verified evidence.

### Emet: External Witness

Role: external witness for source/view consistency and cross-language conformance.

Verified external evidence: the public GitHub repository `HarperZ9/emet` is described as "External witness for AI source/view consistency: MATCH, DRIFT, or UNVERIFIABLE across Python, Rust, and Node conformance vectors." The repository is public at `https://github.com/HarperZ9/emet`.

Build:

- Emet witness packets for source/view consistency across Telos docs, generated packets, Python validators, Rust compiler receipts, and Node demos.
- Cross-language conformance vectors for packet schemas.
- Promotion gates that require Emet consistency for public claims.

Rule: Emet should be the outside witness, not another internal assertion.

## The Model Strategy

The target is not a plain chatbot. The target is a proof-native research and action model:

- Reads Gather source receipts.
- Requests Index context envelopes.
- Uses Forum to route uncertainty.
- Acts only through Telos admission.
- Emits Learn-compatible explanations and curricula.
- Produces BuildLang/buildc or other executable artifacts when computation matters.
- Submits claims to Crucible.
- Asks Emet to witness source/view consistency.
- Promotes only what survives the proof ladder.

## Data Flywheel

The valuable dataset is not raw scraped text. It is receipt-rich work:

- Source body plus source status.
- Context envelope plus workspace hash.
- User objective plus route decision.
- Action plan plus admission decision.
- Tool execution plus output digest.
- Explanation plus self-critique.
- Negative fixture plus failure mode.
- Crucible verdict plus missing evidence.
- Learn mastery or misconception receipt.
- Emet consistency witness.

This is a better training substrate than ordinary instruction data because it teaches the model when to act, when to verify, when to stop, and when to say `UNVERIFIABLE`.

## Training Path

1. Use frontier APIs and local/open-weight models inside Telos receipts.
2. Fine-tune and post-train smaller local models on packet production, source-grounded reasoning, verifier-aware planning, and tool-use discipline.
3. Train specialist models for source extraction, route selection, proof-target formulation, compiler/runtime receipt generation, and negative-fixture discovery.
4. Integrate a larger model with retrieval, action, learning, and proof loops as the default runtime.
5. Scale model training only after the receipt data flywheel produces enough high-quality verified examples to justify compute.

## Public Demos

The first demos are defined in the roadmap appendix:

- Agent action proof packet.
- Research proof packet.
- BuildLang scientific runtime packet.
- Learn proof lesson.
- Visual truth packet.
- Emet source/view witness.

## Positioning

Project Telos is the proof-native operating system for AI work.

The model we build should not merely answer. It should gather, remember, route, act, check, learn, compile, witness, and only then promote. That is the path to a model stack that can compound across research, science, software, learning, and real-world action without training itself on unsupported claims.
