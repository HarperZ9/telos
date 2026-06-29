# Quality-Tool Boundary And Revival Registry

Generated: 2026-06-28

This is the quality-tool boundary for pulling older, siloed, frozen, or local-only work back into Project Telos. The five flagships remain the public face, but high-quality older tools should share a typed boundary with at least one flagship instead of being forgotten.

## Quality-Tool Boundary

A tool can move toward flagship status only when it has:

- A clear host boundary with at least one flagship.
- CLI JSON behavior or a concrete CLI JSON plan.
- MCP adapter support or a concrete MCP adapter roadmap.
- Receipts, hashes, or replay references for important actions.
- Tests that exercise the public contract.
- Docs that separate live behavior from prototype and planned behavior.
- A privacy boundary that avoids raw private payloads, secrets, credentials, and purchased font files.
- A risk boundary that states what the tool will not do.

The promotion path is adapter-first. Tools should expose typed packets to Gather, Index, Forum, Crucible, or Telos before any code is copied into a shared runtime.

## Revival Lanes

The current Telos revival registry contains 13 older, adjacent, or local-only quality tools:

- `calibrate-pro`: display-calibration, promotion-ready. Hosts: `telos.measurement.layers`, `telos.creative.engine`, `crucible.measurement_gate`, `index.context.envelope`.
- `quanta-color`: color-science-library, promotion-ready. Hosts: Calibrate Pro, Telos measurement layers, Telos creative engine, and Crucible measurement gates.
- `quantalang`: effects-language, promotion-candidate. Hosts: `telos.creative.kernels`, `telos.creative.engine`, and `index.context.envelope`.
- `warden-security-lineage`: defensive-find-and-fix, quarantine-and-adapt. Hosts: `telos.find_fix`, `crucible.review`, `forum.ledger.summary`, and `index.context.envelope`.
- `agent-audit`: agent-quality-gate, promotion-ready. Hosts: `forum.ledger.summary`, `telos.loop.ledger`, and `crucible.assess`.
- `context-curator-lite`: context-envelope-source, promotion-ready. Hosts: `index.context.envelope`, `telos.context.envelope`, `gather.docs`, `forum.ledger.summary`, and `crucible.assess`.
- `secret-redact-io`: safe-io, promotion-ready. Hosts: Gather docs, Index context envelopes, and Telos action receipts.
- `repo-proof-index`: proof-indexing, promotion-ready. Hosts: Index context envelopes, Crucible reports, and Forum ledger summaries.
- `release-surface-scanner`: release-assurance, promotion-ready. Hosts: Crucible review, Index map, and Telos workflow.
- `gpu-trace-validator`: rendering-verification, promotion-candidate. Hosts: Telos rendering capabilities, Telos measurement layers, and Crucible measurement gates.
- `raw-native`: deterministic-renderer-verification, promotion-ready. Hosts: Telos rendering capabilities, Telos measurement layers, Telos creative engine, and Crucible measurement gates.
- `studio-libs`: studio-perception-organ, promotion-ready. Hosts: Telos creative engine, Telos rendering capabilities, Gather docs, and Crucible measurement gates.
- `forum-archive`: orchestration-archive, promotion-candidate. Hosts: Forum route, Forum ledger summaries, Telos loop ledgers, and Index context envelopes.
- `rewardspy` concept lane: proxy-objective observability, external OSS inspiration. Host: `telos.objective.monitor`. This lane watches for proxy score improvement while independent quality degrades, mirroring reward-hacking detection for agent workflows.

## Engine-Lineage Additions

`studio-engine` and `reconcile` are part of the Telos Engine lineage even though they are not in the 13-tool revival registry yet.

- `studio-engine`: creative-verification simulation engine. It contributes witnessed Worlds, strand expression algebra, GLSL render programs, audio programs, timelines, criteria, refinement, and a frontend handoff kit.
- `reconcile`: node/browser creative-verification engine. It contributes the single reconcile loop, organ abstraction, expression substrate, GLSL grounding, refinement trajectory, composition, choreography, and witnessed World receipts.

These two repos should enter the registry as engine organs with creative, science, machine learning, and verification boundaries. Their shared promotion standard should be: World packet schema, media graph package adapter, render/audio program receipt, criterion receipt, and replayable witness reference.

## Defensive And Security Boundary

The defensive find-and-fix lane matters, but it must remain maintainer-friendly and evidence-first.

Allowed shape:

- defensive analysis,
- synthetic labs,
- local fixture reproduction,
- good-faith open-source bugfix patches,
- disclosure-safe reports,
- release assurance,
- agent audit,
- proof indexing,
- redacted IO.

Excluded from the shared registry:

- live offensive automation,
- credential collection,
- stealth behavior,
- exploit publication,
- private data exfiltration,
- hidden payloads.

The security lineage becomes valuable when it improves reliability, safety, and open-source maintenance through receipts and tests.

## Creative, Science, And Machine Learning Boundary

The creative side is not a decoration. It is one of the main reasons Telos exists.

Creative lanes include sound, film, image, video, typography, poster design, plotter art, generative art, fractals, glitch, retro CGI, dithering, pixel sorting, shader graphs, Gaussian Splatting, clustered-forward rendering, WebGPU, and hardware-scaled editor surfaces.

Science lanes include physics, geometry, differential-geometry-friendly representation, physical constants, measurement overlays, biological structures, academic source receipts, reproducible experiments, and domain-specific adapters.

Machine learning lanes include large-context context envelopes, local model runtime adapters, KV cache and memory receipts, retrieval provenance, uncertainty and sensitivity maps, and readable agent-produced code.

The shared rule is the same across all lanes: if a tool changes or claims something important, it should leave a receipt that can be joined to source, action, measurement, and verdict.

## Promotion Decision Vocabulary

- `promotion-ready`: usable through a documented packet or adapter with tests and clear risk boundaries.
- `promotion-candidate`: valuable, but needs contract hardening, fixtures, or adapter work.
- `quarantine-and-adapt`: valuable lineage that must be constrained and reshaped before any shared exposure.
- `planned`: named but not implemented.
- `prototype`: runnable in a limited context, not yet a stable dependency.
- `live`: usable now through its documented interface.

`MATCH`, `DRIFT`, and `UNVERIFIABLE` remain verification verdicts. They are not marketing labels.
