# Packet 134: Agent Action Proof-Packet Factory Adapter

Date: 2026-07-01

Status: `AGENT_ACTION_PROOF_PACKET_FACTORY_ADAPTER_MATCH`

Purpose: turn the pass 0123 `AgentActionProofPacketFactory` into an executable
adapter fixture. Five incumbent-style trace inputs are preserved, then wrapped
with Telos authority, admission, side-effect, privacy, and verifier fields.

```text
source_rows = 7
trace_inputs = 5
action_receipts = 5
negative_fixtures = 4
compose_status = MATCH
test_status = MATCH
validator_status = MATCH
```

## Adapted Receipts

| Native system | Adapter status | Verdict | Side effect |
| --- | --- | --- | --- |
| opentelemetry | MATCH | MATCH | local_write |
| langsmith | MATCH | MATCH | local_write |
| langfuse | MATCH | MATCH | local_write |
| phoenix | MATCH | MATCH | local_write |
| braintrust | MATCH | MATCH | local_write |

## Rejection Fixtures

| Fixture | Status | Failures |
| --- | --- | --- |
| missing_authority_scope | REJECTED | missing_authority_scope |
| missing_action_admission | REJECTED | missing_action_admission,write_without_admission |
| missing_verifier | REJECTED | invalid_or_missing_verification_verdict,missing_verification_verdict |
| external_write_and_hidden_reasoning | REJECTED | external_write_not_authorized,hidden_reasoning_exported |

## Source Matrix

| Source | Chars | Gather status |
| --- | ---: | --- |
| Braintrust tracing | 5479 | GATHER_VERIFIED |
| Langfuse observability | 4578 | GATHER_VERIFIED |
| LangSmith observability | 2317 | GATHER_VERIFIED |
| OpenTelemetry context propagation | 16939 | GATHER_VERIFIED |
| OpenTelemetry traces | 22513 | GATHER_VERIFIED |
| Phoenix tracing | 5489 | GATHER_VERIFIED |
| W3C Trace Context | 46231 | GATHER_VERIFIED |

## Boundary

Pass 0124 is a local synthetic adapter fixture across observability trace shapes. It does not claim production ingestion, replacement of incumbents, market fit, external-write authority, scientific discovery, or a promoted natural law.
