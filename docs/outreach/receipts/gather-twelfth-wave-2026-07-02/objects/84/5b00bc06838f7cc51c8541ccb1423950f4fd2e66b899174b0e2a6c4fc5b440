# Pass 0085 Ledger: YouTube Research Compounding Packet

Date: 2026-07-01

Status: `MATCH_YOUTUBE_RESEARCH_COMPOUNDING_PACKET`

## Purpose

Treat the supplied YouTube corpus as crucial source data for the next
Telos/Build compounding pass. This pass ingests 20 supplied URLs, rejects the
single malformed URL, verifies metadata and Gather transcript receipts for the
19 valid videos, and converts the corpus into product hypotheses without
promoting video claims as scientific proof.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_youtube_research_compounding_packet.py` | YouTube metadata, Gather video receipt, Forum, Index, and Telos receipt composer. |
| `tools/test_youtube_research_compounding_packet.py` | Focused source-count, receipt, cluster, and promotion-boundary test. |
| `tools/probe_youtube_research_compounding_packet.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0085_youtube_research_compounding_packet.py` | Independent validator for source counts, receipt counts, cluster dominance, and boundaries. |
| `schemas/youtube-research-compounding-packet-pass-0085.json` | `YouTubeResearchCompoundingPacket/v1` artifact. |
| `schemas/pass-0085-youtube-research-compounding-packet-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0085.json` | Compact YouTube, Forum, Index, Telos, compose, and test receipts. |
| `packets/095-youtube-research-compounding-packet.md` | Human-readable source-led compounding packet. |
| `briefs/095-youtube-research-compounding-brief.md` | Concise product-strategy brief. |
| `adversarial/pass-0085-youtube-research-compounding-steelman.md` | Local steelman of the video-evidence limits. |
| `crucible/pass-0085-thesis.json` | Falsifiable claims. |
| `crucible/pass-0085-measurements.json` | Measurements/evidence. |
| `crucible/pass-0085-report.md` | Crucible report. |
| `crucible/pass-0085-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Supplied URLs | 20 |
| Valid YouTube URLs | 19 |
| Invalid URLs | 1 (`https://www.youtube.com/watch?`) |
| Metadata matches | 19 |
| Gather video matches | 19 |
| Transcript receipt hashes | 19 |
| Raw transcripts stored | false |
| Research clusters | 7 |
| Compounding vectors | 7 |
| Dominant cluster | `enterprise_quantum_optimization` |
| Dominant cluster videos | 13 |
| Unsupported claims | 0 |
| Promoted natural laws | 0 |

## Corpus Clusters

| Cluster | Sources | Product Response |
| --- | ---: | --- |
| `enterprise_quantum_optimization` | 13 | Quantum optimization workflow receipts spanning problem formulation, solver branch, hardware/simulator context, calibration reference, and measured objective. |
| `molecular_ai_drug_discovery` | 1 | AI4Science packets that bind source intake, model decisions, assay handoff, verifier verdicts, and reproduction status. |
| `arc_agi_eval_and_generalization` | 1 | Eval receipt lab with replayable attempts, prompt/model boundaries, tool-use records, and benchmark authority receipts. |
| `quantitative_finance_laws` | 1 | BuildLang quant proof kernels with stress receipts, identity checks, and execution provenance. |
| `search_rl_alpha_zero` | 1 | Search-verifier loop ledger that records proposals, rollouts, verifier gates, and accepted proof states. |
| `agi_risk_scenarios` | 1 | Risk scenario proof packets with assumptions, mitigations, authority boundaries, likelihood evidence, and review status. |
| `ai_society_governance` | 1 | Societal proof-packet lane binding public claims, governance choices, model actions, and accountable review. |

## Product Finding

The corpus is skewed, and that skew is useful. Thirteen valid videos point at
quantum optimization as the fastest public proof demo: a domain where Telos can
show problem formulation, solver choice, simulator/hardware branch, calibration
reference, objective measurement, and verifier verdict as one portable packet.

The remaining single-source clusters are not weaker because they have fewer
videos; they are adapter-lane signals. They map the same proof-packet primitive
into AI4Science, ARC/AGI evaluation, BuildLang quant kernels, search-verifier
loops, AGI risk, and societal governance.

Primary next push: build a `QuantumOptimizationWorkflowReceipt/v1` demo using a
bounded optimization problem with explicit solver branch, objective value,
constraint status, calibration/reference metadata, and Crucible verdict. Pair
that with a second-pass `AI4ScienceClaimToExperimentReceipt/v1` skeleton and an
`ARCAGIEvalAttemptReceipt/v1` skeleton so the product story is visibly one
proof substrate, not a single quantum tool.

## Tool Findings

- YouTube/Gather ingestion: 19 valid videos, 19 metadata matches, 19 Gather
  video matches, and 19 transcript receipt hashes; no raw transcripts are stored.
- Forum route receipt: `MATCH`, `needs_escalation=true`, top candidates
  `deep-research`, `synthesis`, `web-intel`, then `project-telos`.
- Index context envelope: `MATCH`, schema
  `project-telos.context-envelope/v1`, graph pack SHA256
  `8ee383e19ae9a6141bee70de733fb6aa09201ff9d284ce6778ce58b06e6b68b2`.
- Telos status receipt: `MATCH`, tool version `0.1.0`.
- Gather packet receipt: SHA256
  `4a46bd08da3923d0bd515db9f62b59f0be73d9e68a7a4557eb7493eee99803fd`,
  digest seal `45cdcc207b5276facb535ee9492b888fd4050bf5806567ec90d5484d5cf9834f`.
- Gather brief receipt: SHA256
  `b0943a6d58bdaf57f64d8b8108d3751464e1cf0f0a782c6c4d0887dfffd43eb2`,
  digest seal `2d0d2bb9a045aa0652efbcb9f0645730f829ef4ac9c94fcc70c7c20e1ffc21b1`.
- Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `15db39711ac03b55`.
- Crucible assessment seal:
  `068cc60a1abbce8e8c1c96a4a05a324c292f6d26c960a4d9974a13e893a675cd`.
- Crucible registry stats after this pass: 73 theses, 598 claims, 598 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Boundaries

This pass does not claim the videos prove scientific discoveries, investment
theses, policy conclusions, quantum advantage, AGI capability, or a new natural
law. All product responses remain hypotheses until backed by executable demos,
external evidence, and verifier results.

## Verification

```powershell
python -m py_compile docs\research\dogfood\tools\compose_youtube_research_compounding_packet.py docs\research\dogfood\tools\test_youtube_research_compounding_packet.py docs\research\dogfood\tools\validate_pass_0085_youtube_research_compounding_packet.py docs\research\dogfood\tools\probe_youtube_research_compounding_packet.py
python docs\research\dogfood\tools\probe_youtube_research_compounding_packet.py
python docs\research\dogfood\tools\test_youtube_research_compounding_packet.py
python docs\research\dogfood\tools\validate_pass_0085_youtube_research_compounding_packet.py
crucible run docs\research\dogfood\crucible\pass-0085-thesis.json --measurements docs\research\dogfood\crucible\pass-0085-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0085-report.md --out docs\research\dogfood\crucible\pass-0085-run.json --json
gather docs docs\research\dogfood\packets\095-youtube-research-compounding-packet.md --json
gather docs docs\research\dogfood\briefs\095-youtube-research-compounding-brief.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Implement the first bounded demo spec from this corpus: a quantum optimization
workflow receipt with a toy objective, constraints, solver branch, measurement
packet, and Crucible verdict. Then mirror its receipt skeleton into AI4Science
and ARC/AGI eval lanes so the megatool architecture compounds across domains.
