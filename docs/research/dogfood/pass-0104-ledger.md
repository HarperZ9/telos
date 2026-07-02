# Pass 0104 Ledger: AI4Science Claim-to-Experiment Receipt

Date: 2026-07-01

Status: `AI4SCIENCE_CLAIM_TO_EXPERIMENT_RECEIPT_MATCH`

## Purpose

Move the dogfood loop from optimization into AI4Science without overclaiming.
This pass maps official and primary AI4Science sources into a minimum
`AI4ScienceClaimToExperimentReceipt/v1` shape: source claim, agent actions,
protocol, workflow runtime, measurement, reproduction status, negative result
path, reviewer objections, and promotion verdict.

The pass does not run a biological experiment. It defines the receipt gates that
must exist before biological or drug-discovery claims can be promoted.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_ai4science_claim_to_experiment_receipt.py` | Builds source anchors, source-to-receipt map, promotion gates, and Forum/Index/Telos receipts. |
| `tools/test_ai4science_claim_to_experiment_receipt.py` | Focused TDD test for source counts, packet fields, gates, and boundaries. |
| `tools/probe_ai4science_claim_to_experiment_receipt.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0104_ai4science_claim_to_experiment_receipt.py` | Independent validator for seal, source counts, fields, gates, and boundaries. |
| `schemas/ai4science-claim-to-experiment-receipt-pass-0104.json` | `AI4ScienceClaimToExperimentReceipt/v1` artifact. |
| `schemas/pass-0104-ai4science-claim-to-experiment-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0104.json` | Compact compose, test, Forum, Index, Telos, and source-summary receipts. |
| `packets/114-ai4science-claim-to-experiment-receipt.md` | Human-readable AI4Science claim-to-experiment packet. |
| `briefs/114-ai4science-claim-to-experiment-brief.md` | Concise product-strategy brief. |
| `adversarial/pass-0104-ai4science-claim-to-experiment-steelman.md` | Local pass 0104 steelman. |
| `crucible/pass-0104-thesis.json` | Falsifiable claims. |
| `crucible/pass-0104-measurements.json` | Measurements/evidence. |
| `crucible/pass-0104-report.md` | Crucible report. |
| `crucible/pass-0104-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| YouTube source pass | 0085 |
| Roadmap pass | 0102 |
| Source anchors | 11 |
| Official or primary sources | 11 |
| YouTube AI4Science source videos | 1 |
| Minimum packet fields | 11 |
| Source-to-receipt rows | 11 |
| Next experiments | 3 |
| Gap status | `inferred` |
| Reject unmeasured discovery claim | true |
| Require reproduction status | true |
| Require human review | true |
| Unsupported claim count | 0 |
| Promoted natural laws | 0 |
| Artifact file SHA256 | `1e46530dfba2b532b5c4f4769d3d019ca45e9dd0a068a8bb04646d36fa26c844` |
| Artifact seal | `cdc127d906c82e1a485c434f2cea03c47902842a5182f7bac69e7d57205b6593` |

## Source Anchors

| Source | URL | Evidence Role |
| --- | --- | --- |
| FutureHouse | `https://www.futurehouse.org/` | Scientific-agent source anchor. |
| FutureHouse Platform | `https://www.futurehouse.org/research-announcements/launching-futurehouse-platform-ai-agents` | Scientific-agent platform source anchor. |
| Sakana AI Scientist | `https://sakana.ai/ai-scientist/` | Automated research-loop source anchor. |
| Sakana AI Scientist paper | `https://arxiv.org/abs/2408.06292` | Primary paper source anchor. |
| Microsoft Discovery blog | `https://azure.microsoft.com/en-us/blog/microsoft-discovery-advancing-agentic-rd-at-scale/` | Agentic R&D loop source anchor. |
| Microsoft Discovery product | `https://azure.microsoft.com/en-us/solutions/discovery` | Enterprise R&D platform source anchor. |
| NVIDIA BioNeMo | `https://docs.nvidia.com/bionemo-framework/latest/main/about/overview/` | Biomolecular model/workflow source anchor. |
| AlphaFold 3 Nature | `https://www.nature.com/articles/s41586-024-07487-w` | Primary biomolecular prediction paper source anchor. |
| Nextflow | `https://www.nextflow.io/` | Reproducible workflow source anchor. |
| Snakemake | `https://snakemake.readthedocs.io/` | Reproducible workflow source anchor. |
| Benchling | `https://www.benchling.com/` | Lab data/workflow source anchor. |

## Product Finding

The AI4Science wedge is not "another AI scientist." The wedge is a portable
claim-to-experiment proof packet that can sit across scientific agents,
foundation models, workflow engines, and lab-record systems. The packet must
make negative results and reviewer objections first-class, because those are
where unverified discovery claims usually fail.

## Tool Findings

- Forum route receipt: `MATCH`.
- Index context envelope: `MATCH`.
- Telos status receipt: `MATCH`, tool version `0.1.0`.
- Gather packet receipt: SHA256
  `c8dc36bad51dcc14480bf4a1f2c3533fc46df7fed1fe768e26c960877710c234`,
  digest seal `83293cca8e483dddb1777a89ac9060b194298444da461bcc0abbf950278a8042`.
- Gather brief receipt: SHA256
  `4bb052f7ffe58fcbe02020c655cde4878d522be7e594bc9fac1eb3368e29eec8`,
  digest seal `5a8d904f8f1942308301d19e6a348da538f81bd25248ee5aba987ad850743643`.
- Crucible result: 9 claims, 9 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `f674ecfdd5520582`.
- Crucible assessment seal:
  `2c314992f88142674757db033692170a0e40b352ba6b86d945963c0c81f5fb28`.
- Crucible registry stats after this pass: 93 theses, 777 claims, 777 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Boundaries

This pass does not prove biological discovery, drug efficacy, benchmark
superiority, market dominance, or a natural law. It is a source-backed schema
and gate-definition pass.

## Verification

```powershell
python docs\research\dogfood\tools\test_ai4science_claim_to_experiment_receipt.py
python -m py_compile docs\research\dogfood\tools\compose_ai4science_claim_to_experiment_receipt.py docs\research\dogfood\tools\test_ai4science_claim_to_experiment_receipt.py docs\research\dogfood\tools\validate_pass_0104_ai4science_claim_to_experiment_receipt.py docs\research\dogfood\tools\probe_ai4science_claim_to_experiment_receipt.py
python docs\research\dogfood\tools\probe_ai4science_claim_to_experiment_receipt.py
python docs\research\dogfood\tools\validate_pass_0104_ai4science_claim_to_experiment_receipt.py
crucible run docs\research\dogfood\crucible\pass-0104-thesis.json --measurements docs\research\dogfood\crucible\pass-0104-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0104-report.md --out docs\research\dogfood\crucible\pass-0104-run.json --json
gather docs docs\research\dogfood\packets\114-ai4science-claim-to-experiment-receipt.md --json
gather docs docs\research\dogfood\briefs\114-ai4science-claim-to-experiment-brief.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Implement the first minimum packet: one source claim with a protocol placeholder,
measurement receipt requirement, negative-result lane, reproduction status, and
promotion verdict that remains `UNVERIFIABLE` until evidence is attached.
