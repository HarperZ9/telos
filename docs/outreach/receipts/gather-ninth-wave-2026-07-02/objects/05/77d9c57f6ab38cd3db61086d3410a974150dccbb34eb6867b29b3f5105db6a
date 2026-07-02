# Ninth-Wave Bio/Medicine/Robotics Source Federation

Date: 2026-07-02

Purpose: extend the proof-carrying research lane into biology, medicine, robotics, and adjacent autonomous-science systems. This pass is source federation and paper-candidate shaping only. It does not make biomedical, clinical, robotics-safety, or protein-design truth claims.

## Summary

The ninth wave uses Gather's arXiv intake to capture four live source-lead slices:

- biomedical foundation models and clinical AI workflows
- robotics, embodied AI, and laboratory automation
- protein design and systems-biology modeling
- AI-scientist style research automation with biomedical-adjacent overlap

The result is a mixed-quality source tranche. That is useful: it shows why Telos needs an explicit source-lead demotion gate. Search terms can retrieve strong domain leads and obvious query noise in the same pass. The correct next product behavior is not to hide the noise; it is to classify it, preserve it, and route only qualified rows into official paper candidates.

## Source Intake Receipts

| Lane | Store | Retained | Dropped | Digest seal | Status |
| --- | --- | ---: | ---: | --- | --- |
| Biomedical foundation models | `docs/outreach/receipts/ninth-wave/arxiv-biomed-foundation` | 8 | 0 | `d3fe14ba9368def788557a3268fde724a605cf87a5df060af87f79c42362fbe6` | `SOURCE_LEAD` |
| Robotics and lab automation | `docs/outreach/receipts/ninth-wave/arxiv-robotics-lab` | 7 | 1 | `e5ae3b8acd8cae740d9b678e148794dd94841742a5096cd480d37355adbc4516` | `SOURCE_LEAD` |
| Protein design and systems biology | `docs/outreach/receipts/ninth-wave/arxiv-protein-design` | 8 | 0 | `c1ab2439eef86c3db3e55600bf744bbd1f084fd0c9020eb6dd474dd20a2bd91c` | `SOURCE_LEAD` |
| AI-scientist automation, biomedical-adjacent | `docs/outreach/receipts/ninth-wave/arxiv-ai-scientist-biomed` | 7 | 1 | `eadd0ca7b25db20edf82d2827d03e090c9416279ad032656b8033f3870b0d829` | `SOURCE_LEAD` |

Total retained rows: 30. The rows are arXiv metadata/source captures. They do not prove paper claims.

## Source-Lead Demotion Experiment

Receipt: `docs/outreach/receipts/ninth-wave/source-lead-demotion-gate.json`.

The demotion gate classifies every retained row before promotion:

| Class | Count | Meaning |
| --- | ---: | --- |
| `domain_lead` | 15 | Directly relevant enough for source-body review in the named lane. |
| `adjacent_lead` | 9 | Useful for tooling, governance, infrastructure, or neighboring domains, but not enough for domain claims. |
| `query_noise` | 6 | Retained by keyword overlap; cannot support domain claims without separate justification. |

Verification command:

```powershell
node -e "const fs=require('fs'); const gate=JSON.parse(fs.readFileSync('docs/outreach/receipts/ninth-wave/source-lead-demotion-gate.json','utf8')); const stores=['arxiv-biomed-foundation','arxiv-robotics-lab','arxiv-protein-design','arxiv-ai-scientist-biomed']; for (const store of stores) for (const id of fs.readFileSync('docs/outreach/receipts/ninth-wave/'+store+'/catalog.jsonl','utf8').trim().split(/\r?\n/).map(l=>JSON.parse(l).id)) if (gate.rows.filter(r=>r.store===store && r.id===id).length!==1) throw new Error(store+' '+id); console.log(gate.rows.length)"
```

The demotion gate is `PROBE_MATCH` for coverage and manual triage only. It is not a source-body review and does not prove any paper claim.

## High-Signal Leads

These rows look immediately relevant enough for the next official-paper candidate queue. They still need reading, source-body review, claim extraction, and independent checks before promotion.

| Lead | Why it matters for Telos | Proposed packet |
| --- | --- | --- |
| `2504.21336v3` UniBiomed: A Universal Foundation Model for Grounded Biomedical Image Interpretation | Biomedical model interpretation is a good fit for claim-to-source-to-evaluation packets because grounded image claims need provenance, model output, measurement, and clinician-review boundaries. | Biomedical image interpretation proof packet. |
| `2403.00868v3` SoftTiger: A Clinical Foundation Model for Healthcare Workflows | Clinical workflows require action provenance, source provenance, tool authority, and hard boundaries around clinical claims. | Clinical workflow action-receipt proof packet. |
| `2605.10877v1` Neural at ArchEHR-QA 2026 | EHR question answering is a natural testbed for evidence-state labeling, retrieval provenance, and answer-boundary checks. | EHR QA evidence-state packet. |
| `2203.13906v1` Biolink Model | A universal schema for biomedical and translational knowledge graphs is useful substrate for Telos source graph joins. | Biomed knowledge-graph source-ref adapter. |
| `2505.20503v2` Embodied AI with Foundation Models for Mobile Service Robots | Robotics foundation models need environment receipts, action receipts, safety gates, and simulator/physical-world split. | Embodied AI action-receipt packet. |
| `2511.23143v1` Automated Generation of MDPs Using Logic Programming and LLMs for Robotic Applications | MDP generation from LLMs can be checked against formal model constraints and rollout evidence. | LLM-to-MDP verification packet. |
| `2504.06806v1` Mass Balance Approximation of Unfolding Improves Potential-Like Methods for Protein Stability Predictions | Protein stability prediction can be decomposed into source, model, physical invariant, benchmark, and uncertainty receipts. | Protein-stability invariant packet. |
| `2511.04583v4` Jr. AI Scientist and Its Risk Report | Autonomous scientific exploration is directly relevant to Telos's proof-carrying research loop and risk gating. | AI-scientist risk-boundary packet. |

## Query-Noise Leads

These rows were retained by the search terms but should not be promoted into biology/medicine/robotics claims without a separate reason:

| Row | Noise reason | Proper handling |
| --- | --- | --- |
| `2607.01063v1` AutoRestTest at the SBFT 2026 Tool Competition | Software testing, not biomedical/protein/robotics despite term overlap. | Keep as agent-tooling source lead only. |
| `2604.17070v2` NTIRE 2026 Rip Current Detection and Segmentation | Vision challenge; not biomedical or protein design. | Keep only if visual-measurement tooling needs a segmentation benchmark lead. |
| `2606.03948v1` IWSLT 2026 speech translation | Audio/speech model lead, not protein design. | Demote from protein lane. |
| `2603.22728v1` Interspeech 2026 Audio Encoder Capability Challenge | Audio benchmark lead, not protein design. | Demote from protein lane. |
| `2604.11487v1` Robust AI-Generated Image Detection | AI safety / vision lead, not biomedical. | Keep only for provenance/safety lane. |
| `2601.16513v1` Competing Visions of Ethical AI | Governance lead, not biomedical. | Keep for policy lane, not biomed packet. |
| `2602.21012v1` International AI Safety Report 2026 | Safety governance lead, not biomedical. | Keep for governance and risk-boundary packets. |

## Product Implication

The market gap becomes sharper after this pass:

1. Biology/medicine/robotics research tools increasingly generate models, workflows, and candidate answers.
2. They still need evidence-state promotion rules that prevent source capture from becoming a truth claim.
3. Telos can sell the proof layer: source intake, demotion, claim extraction, model/tool action receipt, verification gate, and publication boundary.

## Megatool Integration Map

| Tool | Ninth-wave role | Product effect |
| --- | --- | --- |
| Gather | Captures arXiv source leads and hashes source metadata. | Creates source receipts instead of loose reading lists. |
| Index | Bounds the workspace context for the current Telos package. | Keeps the package re-openable by another Codex session. |
| Forum | Routes the source-federation package into the Project Telos lane. | Preserves intent and handoff context. |
| Crucible | Gates claims about the ninth-wave package against recorded measurements. | Blocks "paper truth" or "domain solved" overclaims. |
| Learn | Converts the packet into a lesson receipt that teaches the boundary. | Makes source-demotion and overclaim discipline learnable. |
| BuildLang/buildc | Future execution layer for physical, numeric, and formal subchecks. | Turns candidate claims into reproducible kernels and receipts. |
| Build Color / measurement tools | Future visual-measurement lane for biomedical image and robotics perception claims. | Separates visual output checks from domain truth. |

## Candidate Official Paper

Working title:

> Proof-Carrying Source Federation for Biology, Medicine, and Robotics

Core thesis:

> In high-stakes scientific domains, the first market need is not a larger autonomous researcher. It is a promotion discipline: every source, model claim, action, measurement, and publication boundary must carry an explicit evidence state.

Initial claims:

| Claim | Status | Evidence | Missing evidence |
| --- | --- | --- | --- |
| Telos can capture live arXiv source leads across bio/medicine/robotics-adjacent lanes. | `SOURCE_LEAD` | Four Gather stores listed above. | Source-body reading, deduplication, and relevance scoring. |
| The source tranche contains both high-signal rows and query-noise rows. | `PROBE_MATCH` | Retained row titles and manual classification in this document. | Independent reviewer classification and automated relevance gate. |
| A proof-carrying source federation paper is ready for official submission. | `UNVERIFIABLE` | No archive submission, no final claims table, no independent review. | Claims table, methods, negative controls, recheck commands, and target archive package. |

## Next Experiments

1. Add a token-free biomedical adapter path for Europe PMC or PubMed, because arXiv alone is not adequate for medicine.
2. Build a source-lead demotion gate that classifies rows as `domain_lead`, `adjacent_lead`, or `query_noise`.
3. Convert the high-signal rows into one proof-packet template each:
   - biomedical image interpretation
   - EHR QA
   - embodied robotics
   - LLM-to-MDP verification
   - protein stability invariant
4. Use Learn to create a prooflesson that teaches why source capture is not truth.
5. Only after source-body review, generate website copy and official paper copy.

## Do Not Claim

- Do not claim this pass found the latest or exhaustive academic literature.
- Do not claim Gather proved any arXiv paper's claims.
- Do not make clinical, biomedical, protein-design, or robotics-safety claims from metadata capture.
- Do not claim PubMed/Europe PMC was integrated; `gather api` currently requires `GATHER_API_TOKEN` in this environment.
- Do not claim an official paper has been submitted from this ninth-wave package.
