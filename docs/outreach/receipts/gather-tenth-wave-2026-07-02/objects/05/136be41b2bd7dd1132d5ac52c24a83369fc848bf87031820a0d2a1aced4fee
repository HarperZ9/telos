# Pass 0124 Ledger: Agent Action Proof-Packet Factory Adapter

Date: 2026-07-01

## Objective

Advance the pass 0123 `AgentActionProofPacketFactory` from strategy into an
executable adapter fixture. The pass preserves incumbent-style trace identifiers
from OpenTelemetry, LangSmith, Langfuse, Phoenix, and Braintrust, then wraps
them with Telos proof-layer fields: source refs, workspace state, authority
scope, action admission, side-effect class, verifier verdict, stop reason,
privacy boundary, and compensation pointer.

## Result

| Field | Value |
| --- | --- |
| Artifact schema | `AgentActionProofPacketFactoryAdapter/v1` |
| Artifact | `schemas/agent-action-proof-packet-factory-adapter-pass-0124.json` |
| Status | `AGENT_ACTION_PROOF_PACKET_FACTORY_ADAPTER_MATCH` |
| Artifact sha256 | `1fa624af386e90f2bdbd1d5294efb3a36b877c92041808e096e7b16a06fe7227` |
| Artifact seal | `5be6a945b22e1c730f4fc93528321fce56bede4d750329a72c90894a9b1b5e7d` |
| Official source rows | 7 |
| Trace inputs | 5 |
| Adapted action receipts | 5 |
| Negative fixtures | 4 |
| Unsupported claim count | 0 |
| Current promoted natural laws | none |

## Source Matrix

All gap claims remain `inferred`. The source rows are official/current anchors
for trace semantics and incumbent observability products.

| Source | URL | Local Gather status |
| --- | --- | --- |
| OpenTelemetry traces | https://opentelemetry.io/docs/concepts/signals/traces/ | `GATHER_VERIFIED` |
| OpenTelemetry context propagation | https://opentelemetry.io/docs/concepts/context-propagation/ | `GATHER_VERIFIED` |
| W3C Trace Context | https://www.w3.org/TR/trace-context/ | `GATHER_VERIFIED` |
| LangSmith observability | https://docs.langchain.com/langsmith/observability | `GATHER_VERIFIED` |
| Langfuse observability | https://langfuse.com/docs/observability/overview | `GATHER_VERIFIED` |
| Phoenix tracing | https://arize.com/docs/phoenix/tracing/llm-traces | `GATHER_VERIFIED` |
| Braintrust tracing | https://www.braintrust.dev/docs/guides/tracing | `GATHER_VERIFIED` |

## Adapted Receipts

| Native system | Adapter status | Verification verdict | Side effect |
| --- | --- | --- | --- |
| OpenTelemetry | `MATCH` | `MATCH` | `local_write` |
| LangSmith | `MATCH` | `MATCH` | `local_write` |
| Langfuse | `MATCH` | `MATCH` | `local_write` |
| Phoenix | `MATCH` | `MATCH` | `local_write` |
| Braintrust | `MATCH` | `MATCH` | `local_write` |

The adapted receipts carry all 18 pass 0064 fields:

`receipt_id`, `schema`, `source_refs`, `workspace_state`, `authority_scope`,
`action_admission`, `tool_call`, `side_effect_class`, `materials_digest`,
`trace_refs`, `eval_refs`, `model_refs`, `runtime_refs`,
`verification_verdict`, `stop_reason`, `compensation_pointer`,
`privacy_boundary`, `receipt_status`.

## Rejection Fixtures

| Fixture | Status | Failures |
| --- | --- | --- |
| `missing_authority_scope` | `REJECTED` | `missing_authority_scope` |
| `missing_action_admission` | `REJECTED` | `missing_action_admission`, `write_without_admission` |
| `missing_verifier` | `REJECTED` | `invalid_or_missing_verification_verdict`, `missing_verification_verdict` |
| `external_write_and_hidden_reasoning` | `REJECTED` | `external_write_not_authorized`, `hidden_reasoning_exported` |

## Market Finding

This pass tightens the agent-ops wedge: observability traces are useful upstream
evidence, but the market-facing proof packet must also bind authority,
admission, side effects, privacy, and verifier verdict. The claim remains a
hypothesis with executable fixtures; it is not a replacement claim against
LangSmith, Langfuse, Phoenix, Braintrust, or OpenTelemetry.

## Flagship Receipts

| Tool | Status | Notes |
| --- | --- | --- |
| Gather web | `MATCH` | 7 source rows under `gather/pass-0124-agent-action-adapter-sources`. |
| Gather packet | `MATCH` | Packet hash `a8e287eef6e14371b8af356f605c1cfb3e68d228bc57d084677227821fdb1f3b`; seal `c178b7ca83dc4c1874796fc126f828650228e6d23c685a6730cf43aaeb0f475a`. |
| Gather brief | `MATCH` | Brief hash `ec9cb23a75b7ed06693c0f34d430fce00afa25f5367df80cb00bd3450e90a803`; seal `3a4c7ddf2db56f549d1ea954979c2d04794fb8dc2264042eafac947613bfec5a`. |
| Forum | `MATCH` | Route receipt captured in artifact. |
| Index | `MATCH` | Context envelope verified. |
| Telos | `MATCH` | Status receipt recorded. |
| Telos catalog | `MATCH` | Catalog summary detected. |

## Crucible

| Field | Value |
| --- | --- |
| Thesis id | `d25a3bcd35ff1e2d` |
| Thesis seal | `d25a3bcd35ff1e2d972a0ed664271048b65055f097c28d5587a3deefd4d348e7` |
| Verdict seal | `6057630bd37f71a695278c86270887dcdd88569b3f2078fc6c261cf66c84e362` |
| Measurement seal | `36b4215a113b9099933b72a632cc888b210fff27e7655680e65f38fd3421dc48` |
| Assessment seal | `9a3df66078655258c1d0c0a5bdb2fd872838c08e6292cb0f6bcc88ff2d41a616` |
| Counts | `MATCH 10 / DRIFT 0 / UNVERIFIABLE 0` |
| Registry after pass | 115 theses, 1026 claims, 992 unique claims, 118 assessments, 115 latest assessments, 0 invalid latest assessments |

## File Hashes

| File | SHA-256 |
| --- | --- |
| `tools/compose_agent_action_proof_packet_factory_adapter.py` | `715c0b8ff48827c5e1192b9889ce34c0c521c9c2ad8aadb0a41dea7d827349bb` |
| `tools/test_agent_action_proof_packet_factory_adapter.py` | `80469ca440c51804ecc50ddc7975e0876b1ccc1684b0b187c9f8f861416cde6a` |
| `tools/validate_pass_0124_agent_action_adapter.py` | `713ce0c5588a6b22212e06cdc75e89f9b6141cf71647f2a268614ab29ac812e9` |
| `tools/probe_agent_action_proof_packet_factory_adapter.py` | `321f78435b4896c20a37eda47907638a6ab7358501d136e7b52cc399ec298464` |
| `schemas/agent-action-proof-packet-factory-adapter-pass-0124.json` | `1fa624af386e90f2bdbd1d5294efb3a36b877c92041808e096e7b16a06fe7227` |
| `schemas/pass-0124-agent-action-adapter-validator-result.json` | `2c0eb62f1661ee913ad92087515966e3b7ff668e95b23083660a08d002181ffc` |
| `schemas/tool-receipts-pass-0124.json` | `3255d3be7d5278d6a94fd45d29e820f7af28f23e83e58b4b793178241ea1b9a6` |
| `packets/134-agent-action-proof-packet-factory-adapter.md` | `a8e287eef6e14371b8af356f605c1cfb3e68d228bc57d084677227821fdb1f3b` |
| `briefs/134-agent-action-proof-packet-factory-adapter-brief.md` | `ec9cb23a75b7ed06693c0f34d430fce00afa25f5367df80cb00bd3450e90a803` |
| `adversarial/pass-0124-agent-action-proof-packet-factory-adapter-steelman.md` | `b5d2dcd6275aa8e2b0b2f8ecaaa3d22a893cf1b16d7e0c9648bb82dc4a7b1441` |
| `crucible/pass-0124-thesis.json` | `8e66c64d55bc4aa1f4d06ec53c0f7118912764762da8351d1cc88928812c41d6` |
| `crucible/pass-0124-measurements.json` | `2f0d98ee58380780ecff06123fa48f1d47b15f2f23023ffb5e22501f2eb056f4` |
| `crucible/pass-0124-report.md` | `3a1ad85bdc64aad0475cd6e69dd62e5e2836e719bca3f0e65de53564139bc4a3` |
| `crucible/pass-0124-run.json` | `7452560b0d0e665e231328175b405d4874a137572f1d3726f01f6ad5448efb0e` |

## Verification Commands

```powershell
python -m py_compile docs\research\dogfood\tools\compose_agent_action_proof_packet_factory_adapter.py docs\research\dogfood\tools\test_agent_action_proof_packet_factory_adapter.py docs\research\dogfood\tools\validate_pass_0124_agent_action_adapter.py docs\research\dogfood\tools\probe_agent_action_proof_packet_factory_adapter.py
python docs\research\dogfood\tools\probe_agent_action_proof_packet_factory_adapter.py
python docs\research\dogfood\tools\test_agent_action_proof_packet_factory_adapter.py
python docs\research\dogfood\tools\validate_pass_0124_agent_action_adapter.py
gather docs docs\research\dogfood\packets\134-agent-action-proof-packet-factory-adapter.md --json
gather docs docs\research\dogfood\briefs\134-agent-action-proof-packet-factory-adapter-brief.md --json
crucible run docs\research\dogfood\crucible\pass-0124-thesis.json --measurements docs\research\dogfood\crucible\pass-0124-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0124-report.md --out docs\research\dogfood\crucible\pass-0124-run.json --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass Queue

1. Replace the synthetic trace refs with a local OTLP JSON export fixture and
   prove the same adapter fields are preserved.
2. Connect the adapter to a real Telos `action.receipt` output from
   `node demo/action-receipt.mjs`, then reject drift if the demo schema changes.
3. Start the second factory demo: a `pipeline-math++` theorem packet with source
   refs, failed-branch capture, verifier verdict, and formal replay boundary.
