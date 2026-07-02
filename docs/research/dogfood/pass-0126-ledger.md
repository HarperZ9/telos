# Pass 0126 Ledger: Source-Lead Demotion Gate

Date: 2026-07-01

## Objective

Make the pass 0125 video-source boundary executable. Video metadata,
transcript hashes, and keyword signal counts may route experiments, but they
cannot promote a claim to fact, law, benchmark, or market-fit evidence without
independent non-video artifacts.

This pass is a guardrail before the broader `CrossFieldScientificRuntimeRouter`
begins emitting runtime branches.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_source_lead_demotion_gate.py` | Composer for source-lead policy, promotion fixtures, rejection failures, upstream bindings, and flagship receipts. |
| `tools/test_source_lead_demotion_gate.py` | Focused TDD test for gate acceptance and rejection behavior. |
| `tools/validate_pass_0126_source_lead_demotion_gate.py` | Independent validator for seal, fixture counts, rejection reasons, upstream bindings, and flagship receipts. |
| `tools/probe_source_lead_demotion_gate.py` | Packet, brief, steelman, thesis, measurement, and tool-receipt generator. |
| `schemas/source-lead-demotion-gate-pass-0126.json` | `SourceLeadDemotionGateReceipt/v1` artifact. |
| `schemas/pass-0126-source-lead-demotion-gate-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0126.json` | Compact gate, Forum, Index, Telos, catalog, compose, test, and validator receipts. |
| `packets/136-source-lead-demotion-gate.md` | Human-readable demotion gate packet. |
| `briefs/136-source-lead-demotion-gate-brief.md` | Buyer-facing demotion gate brief. |
| `adversarial/pass-0126-source-lead-demotion-gate-steelman.md` | Local pass 0126 steelman. |
| `crucible/pass-0126-thesis.json` | Falsifiable claims. |
| `crucible/pass-0126-measurements.json` | Measurements/evidence. |
| `crucible/pass-0126-report.md` | Crucible report. |
| `crucible/pass-0126-run.json` | Crucible run record. |

## Result

| Measurement | Value |
| --- | --- |
| Artifact status | `SOURCE_LEAD_DEMOTION_GATE_MATCH` |
| Artifact sha256 | `e4bc219f77998b03b4e4618647886816722c79b7ca2ff59ab8a7f7ecfe9cd9a2` |
| Artifact seal | `67b045645bb0ff265f585a2c92768684ba47e2956920030eb756191bbd737926` |
| Upstream video router pass | `0125` |
| Upstream agent-action adapter pass | `0124` |
| Source leads summarized | `4` |
| Gate fixtures | `7` |
| Accepted fixtures | `3` |
| Rejected fixtures | `4` |
| Raw transcripts exported | `false` |
| Unsupported claims | `0` |
| Current promoted natural laws | `0` |

## Gate Fixtures

| Fixture | Requested status | Gate status | Failure reason |
| --- | --- | --- | --- |
| `source_lead_only_ok` | `SOURCE_LEAD_ONLY` | `ACCEPTED` |  |
| `hypothesis_routing_ok` | `HYPOTHESIS` | `ACCEPTED` |  |
| `independent_probe_ok` | `PROBE_MATCH` | `ACCEPTED` |  |
| `video_only_fact_rejected` | `VERIFIED_FACT` | `REJECTED` | `missing_independent_evidence,video_only_promotion` |
| `video_law_rejected` | `PROMOTED_LAW` | `REJECTED` | `law_promotion_forbidden,missing_independent_evidence,video_only_promotion` |
| `raw_transcript_rejected` | `HYPOTHESIS` | `REJECTED` | `raw_transcript_included` |
| `keyword_count_as_proof_rejected` | `CRUCIBLE_MATCH` | `REJECTED` | `keyword_count_not_proof,missing_independent_evidence,video_only_promotion` |

## Policy

| Policy | Rule |
| --- | --- |
| Source-lead states | `SOURCE_LEAD_ONLY` and `HYPOTHESIS` can pass with video evidence. |
| Fact-like states | `VERIFIED_FACT`, `PROBE_MATCH`, `CRUCIBLE_MATCH`, and `LAW_CANDIDATE` require independent non-video evidence. |
| Promoted law | `PROMOTED_LAW` is rejected by this gate. |
| Raw transcripts | Packet exports with raw transcript bodies are rejected. |
| Keyword signals | Keyword counts are routing signals, not proof. |

## Gather

| Document | sha256 | seal |
| --- | --- | --- |
| `packets/136-source-lead-demotion-gate.md` | `6223c964f062071d4a08475921a0bd150c9f1b303abecf04ed9dd594293c3b6f` | `1f14500a43a2ea38ce5444b0948d3207fa4459ca5a3fc74be7c067b578ffb68b` |
| `briefs/136-source-lead-demotion-gate-brief.md` | `44f4164400ad6dd4268da6b988f9b8cad2461b3b2cc2ac73f3d025638ad41802` | `0fa4c40b6fbb04a949e0542bbbdbbe17cf146b3391f5f3b9105d3eb7c10d8798` |

## Crucible

| Measurement | Value |
| --- | --- |
| Thesis id | `e5496db163ec5f51` |
| Thesis seal | `e5496db163ec5f518d3aaac92e4243a02bfc0060f2d4d1787f10d78ee85b80cf` |
| Claims | `10` |
| MATCH | `10` |
| DRIFT | `0` |
| UNVERIFIABLE | `0` |
| Verdict seal | `9847ddd0b3d1eeb98a7d3d78d01e4cd865228edd17999a44273f4d463419ed07` |
| Measurement seal | `c07c10f3e43605e88aad53b194529019a7dd198fb221f7ddf97199b897adba24` |
| Assessment seal | `c851e1d68b24128c267786a73ba47168dd59902afa59afb80f08085c93c09633` |

Registry after pass 0126:

- theses: `117`;
- claims: `1046`;
- verdicts: `1046 MATCH`, `0 DRIFT`, `0 UNVERIFIABLE`;
- invalid latest assessments: `0`.

## File Hashes

| File | sha256 |
| --- | --- |
| `schemas/source-lead-demotion-gate-pass-0126.json` | `e4bc219f77998b03b4e4618647886816722c79b7ca2ff59ab8a7f7ecfe9cd9a2` |
| `schemas/pass-0126-source-lead-demotion-gate-validator-result.json` | `642afd9c50c041708ac0fcbfeb10afdc80ae0b04728efb4cdeed8123a21749ce` |
| `schemas/tool-receipts-pass-0126.json` | `15ae563e653f3dd36696cb2b91bb7c7e9a08223c4c001a516f6ec6dc5387047b` |
| `packets/136-source-lead-demotion-gate.md` | `6223c964f062071d4a08475921a0bd150c9f1b303abecf04ed9dd594293c3b6f` |
| `briefs/136-source-lead-demotion-gate-brief.md` | `44f4164400ad6dd4268da6b988f9b8cad2461b3b2cc2ac73f3d025638ad41802` |
| `adversarial/pass-0126-source-lead-demotion-gate-steelman.md` | `5f87cd399c4836e890bb42d56d5d07a9df8545c5335b016e936d07bd4e789ded` |
| `crucible/pass-0126-thesis.json` | `bca35dd5ce4c54b1c64f5358a5d905b205a5f7829098d9de6ebca4d77f168003` |
| `crucible/pass-0126-measurements.json` | `46794d3be3520c69f3e8008ab132d2b65ddba0befbcc3a807abc0a2039c88a46` |
| `crucible/pass-0126-report.md` | `f4fbfcc04555f0deb8f5e1299c93566f3962590d733fb494de7f23e95c8fb101` |
| `crucible/pass-0126-run.json` | `7664d6c0eacc30c6f482215fefb06eaea5360691d2c8b5b9ce3ebd0835e7e9aa` |
| `tools/compose_source_lead_demotion_gate.py` | `7b5f03f09608064dd3840983fd0629e8678fe37183dc8d3aecb7b6fc9f21ca46` |
| `tools/test_source_lead_demotion_gate.py` | `ae4c2fd1819be709bf99d43d788d0471233484e704dfc1c7d1b957884cf72e56` |
| `tools/validate_pass_0126_source_lead_demotion_gate.py` | `f4b01e60d75a2b554f20523dcacce426e5fe5777f654ee0920100537c3040a17` |
| `tools/probe_source_lead_demotion_gate.py` | `b2bbc839757f879e500e56fbf593eae86a43f655d8a34d7998ac30989f251c82` |

## Verification Commands

```powershell
python docs\research\dogfood\tools\probe_source_lead_demotion_gate.py
python docs\research\dogfood\tools\test_source_lead_demotion_gate.py
python docs\research\dogfood\tools\validate_pass_0126_source_lead_demotion_gate.py
python -m py_compile docs\research\dogfood\tools\compose_source_lead_demotion_gate.py docs\research\dogfood\tools\test_source_lead_demotion_gate.py docs\research\dogfood\tools\validate_pass_0126_source_lead_demotion_gate.py docs\research\dogfood\tools\probe_source_lead_demotion_gate.py
gather docs docs\research\dogfood\packets\136-source-lead-demotion-gate.md --json
gather docs docs\research\dogfood\briefs\136-source-lead-demotion-gate-brief.md --json
crucible run docs\research\dogfood\crucible\pass-0126-thesis.json --measurements docs\research\dogfood\crucible\pass-0126-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0126-report.md --out docs\research\dogfood\crucible\pass-0126-run.json --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

The next useful pass is the first `CrossFieldScientificRuntimeRouter` fixture:
take a source lead, route it through the demotion gate, bind it to an exact
oracle plus one executable local branch, and require the runtime receipt to keep
interpretation and market claims unpromoted.
