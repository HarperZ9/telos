# Cross-Domain Experiment Routers For Proof-Carrying Science

Author: Project Telos

Date: 2026-07-02

Version: 0.1 official-copy working draft

Status: working paper draft

Evidence boundary: source-router architecture and local metadata receipts only. This draft does not claim new scientific laws, theorem proofs, hardware results, climate-model validation, neuroscience truth, materials discovery, or official archive acceptance.

## Abstract

Scientific AI systems increasingly retrieve papers, generate hypotheses, write code, invoke tools, and produce persuasive summaries across many fields. The hard problem is not only model capability. It is claim promotion: deciding which evidence state a claim is entitled to occupy.

This draft proposes cross-domain experiment routers. An experiment router takes a source lead and produces the smallest honest next proof packet: theorem replay, simulation receipt, benchmark packet, source-body extraction, uncertainty audit, or blocked claim. The tenth-wave Telos pass applies that pattern to quantum computing, materials and energy, climate AI, neuroscience and cognitive science, and formal verification. The result is not a solved frontier problem. It is an evidence-preserving mechanism for turning frontier ambition into verifiable subproblems.

## Evidence-State Glossary

| Term | Meaning |
| --- | --- |
| `SOURCE_LEAD` | A source or metadata row worth reading. It does not establish the source's claims. |
| `DOMAIN_LEAD` | Metadata title/lane suggests relevance to the domain. It still requires source-body review. |
| `ADJACENT_LEAD` | Useful for neighboring product or methodology work, not direct evidence for the lane. |
| `QUERY_NOISE` | Captured row that should remain visible but not promoted. |
| `EXPERIMENT_CANDIDATE` | A proposed smallest verifiable packet derived from a source lead. |
| `PROBE_MATCH` | A local bounded check matched its stated criterion. |
| `CRUCIBLE_MATCH` | A claim matched a measurement packet in Crucible. |
| `UNVERIFIABLE` | The current packet lacks enough evidence for the claim as scoped. |

## Claims Table

| Claim | Scope | Evidence state | Evidence reference | Missing evidence | Demotion trigger |
| --- | --- | --- | --- | --- | --- |
| The tenth-wave pass captured five cross-domain arXiv source stores. | Metadata/source receipt existence only. | `SOURCE_LEAD` | Five stores under `docs/outreach/receipts/tenth-wave/`. | Source-body reviews and independent relevance classification. | Missing stores, failed corpus verification, or digest mismatch. |
| The retained tenth-wave catalogs contain 39 rows and 34 unique arXiv IDs. | Local JSONL row/dedup count. | `PROBE_MATCH` | `docs/outreach/receipts/tenth-wave/source-router-demotion-gate.json` | None for the count; still missing source-body review. | Reparse count differs. |
| The demotion gate classified rows as 24 domain leads, 10 adjacent leads, and 5 query-noise rows. | Manual title metadata triage only. | `PROBE_MATCH` | `docs/outreach/receipts/tenth-wave/source-router-demotion-gate.json` | Independent reviewer, source-body classifier, false-positive/false-negative analysis. | Row coverage missing or class counts differ. |
| Cross-domain experiment routers are a useful mechanism for reducing frontier goals into verifiable packets. | Product/research thesis. | `HYPOTHESIS` | Ninth-wave source federation, tenth-wave source-router receipt, existing Telos proof-packet pipeline. | Comparative evaluation against alternatives. | A simpler workflow produces more reliable claim promotion with less evidence loss. |
| Any quantum, materials, climate, neuroscience, or theorem-proving result is established by this packet. | Domain truth. | `UNVERIFIABLE` | No source-body review, proof replay, simulation, benchmark, hardware, wet-lab, climate validation, or neuroscience evidence is attached. | Requires domain-specific evidence and verifier receipts. | Any public copy implies solved-domain results from metadata. |

## Router Pattern

The router makes one decision: what is the smallest next packet this source lead deserves?

| Source shape | Next packet | Evidence required before promotion |
| --- | --- | --- |
| Formal theorem/proof assistant paper | Replay packet | Proof artifact, environment, command, verifier output. |
| Quantum scheduling or error-correction paper | Assumption and simulator packet | Noise model, constraints, theorem/simulation split, reproducible script. |
| Materials discovery paper | Benchmark or wet-lab boundary packet | Dataset, split, metric, uncertainty, physical validation status. |
| Climate AI paper | Data/model/uncertainty packet | Data provenance, model version, horizon, uncertainty and scenario boundary. |
| Neuroscience/AI convergence paper | Claim-type packet | Empirical neuroscience, computational analogy, benchmark, and philosophy separated. |
| Governance/safety/media verification paper | Adjacent methodology packet | Only promoted in governance/provenance lanes, not domain-science lanes. |

## Methods

The tenth-wave intake used five Gather arXiv commands:

```powershell
gather arxiv "quantum error correction quantum networking fault tolerant computing 2026" --max-results 8 --scope "quantum,error-correction,networking,fault-tolerant,computing" --json --store docs\outreach\receipts\tenth-wave\arxiv-quantum-frontier
gather arxiv "materials discovery foundation models energy storage catalysis 2026" --max-results 8 --scope "materials,discovery,foundation,models,energy,storage,catalysis" --json --store docs\outreach\receipts\tenth-wave\arxiv-materials-energy
gather arxiv "climate modeling AI foundation model uncertainty data assimilation 2026" --max-results 8 --scope "climate,AI,foundation,model,uncertainty,data-assimilation" --json --store docs\outreach\receipts\tenth-wave\arxiv-climate-ai
gather arxiv "neuroscience AI foundation models brain cognitive science 2026" --max-results 8 --scope "neuroscience,AI,foundation,models,brain,cognitive,science" --json --store docs\outreach\receipts\tenth-wave\arxiv-neuro-ai
gather arxiv "formal verification theorem proving AI proof assistant 2026" --max-results 8 --scope "formal,verification,theorem,proving,AI,proof-assistant" --json --store docs\outreach\receipts\tenth-wave\arxiv-formal-verification-ai
```

The demotion gate is a manual title-metadata triage. It intentionally does not read source bodies or infer scientific correctness.

## Negative Controls

1. Repeated general rows such as `2512.03307v1`, `2501.02842v1`, and `2604.11487v1` are treated as duplication and adjacency controls.
2. AI safety/governance rows stay adjacent unless a governance packet is opened.
3. Media verification rows do not become theorem-proving evidence.
4. Metadata rows do not become proof, simulation, benchmark, climate, wet-lab, or neuroscience evidence.
5. The router must be allowed to return `UNVERIFIABLE` or `QUERY_NOISE`; otherwise it becomes a promotion machine instead of a scientific tool.

## First Official-Copy Candidates

| Candidate | Why it is tractable | First gate |
| --- | --- | --- |
| Formal replay micro-packet | The proof lane has clear binary replay criteria. | Reproduce one tiny proof or mark the source-body packet blocked. |
| Climate uncertainty packet | Public claims need careful scenario and uncertainty language. | Extract model/data/horizon/uncertainty from one source body. |
| Quantum scheduling toy packet | Quantum-network scheduling can be represented as a small constraint problem before hardware claims. | Encode a toy feasibility check with explicit assumptions. |
| Materials benchmark boundary packet | Materials papers often mix benchmark and physical discovery language. | Split benchmark claims from physical validation claims. |

## Recheck Commands

```powershell
gather corpus verify docs/outreach/receipts/tenth-wave/arxiv-quantum-frontier --json
gather corpus verify docs/outreach/receipts/tenth-wave/arxiv-materials-energy --json
gather corpus verify docs/outreach/receipts/tenth-wave/arxiv-climate-ai --json
gather corpus verify docs/outreach/receipts/tenth-wave/arxiv-neuro-ai --json
gather corpus verify docs/outreach/receipts/tenth-wave/arxiv-formal-verification-ai --json
node -e "const fs=require('fs'); const p='docs/outreach/receipts/tenth-wave/source-router-demotion-gate.json'; const j=JSON.parse(fs.readFileSync(p,'utf8')); console.log(j.summary)"
```

## Publication Boundary

This is an official-copy working draft, not an official submission. It becomes publication-ready only after at least one source-body lane is converted into a domain-specific proof packet with a verifier receipt and an explicit public-copy boundary.

## Revision Log

| Version | Date | Change | Evidence boundary |
| --- | --- | --- | --- |
| 0.1 | 2026-07-02 | Initial cross-domain experiment-router draft. | Metadata/source-router architecture only. |

