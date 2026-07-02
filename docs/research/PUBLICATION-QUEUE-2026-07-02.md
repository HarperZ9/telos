# Project Telos Publication Queue

Date: 2026-07-02
Status: first publication-control pass

This queue decides what can become a credible paper, proof demo, site page, or
internal memo. It is intentionally conservative: a working demo is not a solved
field problem, and a video transcript is a source lead, not domain proof.

## Queue Rules

- A public paper candidate must state the measured claim, the evidence source,
  the negative control, the replay command, and the non-claim.
- A whitepaper can be broader than a proof demo, but it still cannot promote
  source leads into verified technical facts.
- A frontier-domain artifact can be publishable when it is framed as method,
  measurement, simulation, safety, assurance, or learning infrastructure.
- A grand-problem claim needs independent proof review and reproduced artifacts
  before the word "solved" belongs anywhere near the public copy.
- BuildLang/buildc is a strategic pillar, not the whole strategy. It should
  become the receipt-bearing compute layer for Telos proof packets.
- Research/philosophy corpus material from Senses and Sensibility is paper
  substrate until human re-derivation, provenance-ledger, citation-locator,
  live-policy, anonymization, and AI-use disclosure gates clear.
- Telos repo material is routed by
  `docs/registry/TELOS-REPO-SUBREGISTRY-2026-07-02.md`; working-tree artifacts,
  outreach copy, receipt stores, and cache payloads must not be promoted as
  shipped evidence without the matching gate.

## Tier A: Methods Papers To Push First

| Rank | Candidate | Why this leads | Evidence now | Missing gate | 7-day action | Target |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | BuildLang Scientific Runtime Receipts | It gives every domain a shared accountable compute substrate and makes BuildLang/buildc strategically central without overclaiming field results. | BuildLang docs describe `buildc`, C backend, typed effects, receipt export, invariant families, negative fixtures, and Crucible export. | Telos-side receipt import fixture and one reproduced export into Crucible. | Build `buildlang-scientific-runtime-receipt/v0` import fixture in Telos and run one small kernel receipt through Crucible. | arXiv methods paper plus proof demo |
| 2 | Causal Research Workbench | Causal claims are compact, falsifiable, and relevant to medicine, biology, economics, policy, AI evals, and research claims. | `CAUSAL_DAG_FIXTURE_MATCH` on a toy DAG with explicit negative controls. | Synthetic SCM with known treatment effect and BuildLang typed DAG. | Add SCM fixture, estimator receipts, and countergraph checks. | arXiv methods paper |
| 3 | Agent Action Proof Packets | This is the market-facing accountability wedge for AI infrastructure and high-stakes agent workflows. | Telos action receipts, browser evidence, Index context, Forum routing, Crucible verdicts, and loop ledger surfaces exist. | One external-write proof demo binding intent, state, action, evidence, and verification. | Create a no-side-effect or sandboxed external-write proof packet with browser evidence and review outcome. | whitepaper plus site demo |

## Tier B: Proof Demos To Harden

| Candidate | Evidence now | Missing gate | Next proof-demo shape | Target |
| --- | --- | --- | --- | --- |
| Quantum Error-Correction Proof Packets | Working-tree 3-qubit bit-flip stabilizer fixture emits `QEC_STABILIZER_FIXTURE_MATCH`. | Commit boundary, BuildLang typed Pauli/stabilizer runtime, surface-code toy fixture, Clifford equivalence checker. | Stabilizer-to-Clifford packet with syndrome table, decoder behavior, negative controls, and resource non-claims. | proof demo then whitepaper |
| Embodied Sim-to-Real Proof Packets | Differential-drive fixture emits `EMBODIED_SIM2REAL_FIXTURE_MATCH`. | BuildLang typed-unit replay, manipulation fixture, object pose/contact state, safety-stop gate. | Controller-stability and sim-to-real trace packet. | proof demo then whitepaper |
| Hyphal Context Benchmark | One fixture records about 98.92 percent token savings with no recorded fixture deltas. | Multi-corpus benchmark, answer-quality scoring, false-claim and missing-evidence rates. | Context-routing proof packet comparing full-context, retrieval, and hyphal receipt routing. | methods note |
| Formal PDE Replay | Finite formal/numerical preflight exists; larger PDE claims remain out of scope. | Smooth-periodic theorem boundary, BuildLang relation-invariant receipt, formal/numerical boundary table. | Paired Lean/BuildLang receipt for one finite invariant. | whitepaper |
| Color/Rendering Measurement Kit | Build Color, Calibrate Pro, Telos display calibration, Studio Engine, and Reconcile form the candidate stack. | Device/profile fixture, delta-E measurement receipt, ACES/OCIO/Calman/ColourSpace comparison matrix. | Color transform proof kit with profile hashes, display state, measured output, and render artifact hashes. | site proof demo plus market brief |

## Tier C: Source-To-Domain Expansion

| Candidate | Evidence now | Why it matters | Promotion gate | Target |
| --- | --- | --- | --- | --- |
| TI Morse Industrial Science Integration | Five requested videos plus Ti Morse channel catalog are captured as metadata/transcript/source-lead receipts; Gather federation seal `63a2b0cc6865791ea04bb7abdb7895db5ac4bc267c96785566e842833b9b1428`. | It expands Telos into nuclear/energy/manufacturing/drones/uranium/space/biotech/materials/supersonics as industrial R&D proof-packet lanes. | Promote one lane with primary sources, units, uncertainty, safety boundary, and replayed calculation. | methods note |
| Biology Network Intelligence | Source packet and hyphal protocol framing exist. | It can become a learning/context architecture paper without overclaiming biology. | Measure routing quality over corpora and avoid biological cognition claims. | whitepaper |
| Microscopy, Materials, Biology Instrumentation | Applied Science source lead and existing measurement-layer tools suggest instrument-aware proof packets. | It connects visual evidence, color/rendering, instrument calibration, and biological/material interpretation boundaries. | Primary source/instrument spec packet and image/video measurement fixture. | internal memo then proof demo |
| AI Scale Economics and Compute Ledger | Source leads from Molly Rocket, Ti Morse channel energy/data-center episodes, Model Foundry, and Objective Monitor. | It turns compute budgets, data center constraints, evals, and scaling claims into receipts instead of slogans. | Public-data ledger with budget, energy, latency, quality, contamination, and residual-risk fields. | whitepaper |

## Tier D: Theory And Publication-Control Corpus

| Candidate | Evidence now | Why it matters | Promotion gate | Target |
| --- | --- | --- | --- | --- |
| Senses and Sensibility / Conferred Existence corpus | `docs/registry/SENSES-AND-SENSIBILITY-SUBREGISTRY-2026-07-02.md` records 172 Markdown/RST docs, 1 preserved source `.txt`, 125 dissertation docs, 4 submission kits, and a clean local repo one commit behind. | It provides the theory vocabulary behind Telos accountability: human gate, authorship, provenance, authn/authz separation, witness discipline, and proof-before-trust. | Human re-derivation, contribution ledger, citation locator verification, live journal policy check, anonymization, and material AI-use disclosure. | theory paper candidates, ORCiD/arXiv-style research record, and Telos publication-control rubric |
| Membrane / authn-authz paper track | `dissertation/MEMBRANE-PAPER-v3.md` plus `submission/membrane-submission.md`. | Direct conceptual bridge between Telos action receipts and the is/ought category line. | Re-derive primary sources, verify journal requirements, repair references, add disclosure, and keep implementation claims separate. | philosophy/technology journal candidate after gates |
| Arity / free-will paper track | `papers/arity-gap-paper.md` plus `submission/arity-submission.md`. | Theory source for sourcehood, answerability, and human ownership without self-origination claims. | Re-derive primary sources, verify paper repair, strip provenance ledger from anonymous manuscript, and complete AI disclosure. | philosophy journal candidate after gates |
| Self-given / consciousness paper track | `papers/self-given-paper.md` plus `submission/self-given-submission.md`. | Theory source for self-givenness vs self-grounding and the seity/aseity boundary. | Reconcile sources to the bibliography, verify locators, confirm live venue rules, and clear authorship gate. | philosophy of mind journal candidate after gates |

## Primary 30-Day Market Push

Push `Project Telos Research Workbench + Build Scientific Runtime` as the
primary market motion.

The package should demonstrate:

1. Source intake through Gather.
2. Workspace/context selection through Index.
3. Lane routing through Forum.
4. A BuildLang/buildc receipt for a bounded computation.
5. A Crucible verdict.
6. A Telos action or research receipt.
7. A Learning Forge object for transfer and education.

This is the narrowest honest pitch that still preserves the full ambition:
proof-carrying research packets for scientific, industrial, and agentic work.

## Hard Boundaries

- TI Morse and other videos are source leads until primary sources or replayed
  experiments exist.
- Nuclear, biochem, medical, cyber, robotics, and defense-adjacent material can
  be scoped as research, measurement, safety, simulation, or assurance, but
  public artifacts must not become operational instructions.
- BuildLang/buildc should not be marketed as a Julia replacement on trust alone.
  The defensible claim is narrower: a receipt-bearing scientific runtime layer
  with a path toward reliability, invariants, and proof integration.
- QEC, PDE, robotics, and biology demos should say exactly which toy or bounded
  claim matched and which real-world claims remain unverifiable.

## Paper Templates Needed Next

| Template | Purpose | Required sections |
| --- | --- | --- |
| Methods paper | For BuildLang runtime, causal workbench, action packets. | Abstract, contribution, system model, artifact, evaluation, negative controls, limitations, reproducibility, ethics/risk, related work. |
| Proof-demo paper | For QEC, robotics, color/rendering, formal replay. | Claim card, fixture, command, expected output, failure cases, verifier report, non-claims. |
| Source-to-domain memo | For Ti Morse, biology, industrial R&D, AI scale economics. | Source ledger, field map, hypotheses, primary-source gaps, first safe experiment, publication boundary. |

## Immediate Backlog

1. Create `buildlang-scientific-runtime-receipt/v0` in Telos.
2. Add a causal SCM fixture and BuildLang typed DAG follow-on.
3. Add one sandboxed agent-action proof packet with browser evidence.
4. Convert the Ti Morse nuclear/manufacturing lane into a public-source,
   source-to-simulation schema without domain performance claims.
5. Add the Telos commit-boundary publication gate before README, site, or
   outreach copy says a working-tree artifact is shipped.
6. Build the receipt-index bridge over `docs/outreach/receipts` and
   `demo/research` receipts.
7. Refresh market matrices for research labs, AI infra, and visual/compiler
   tooling against this queue rather than against a single-tool framing.
8. Import the Senses human-gate and citation-locator rules into every Telos
   paper, whitepaper, and ORCiD/arXiv candidate rubric.
