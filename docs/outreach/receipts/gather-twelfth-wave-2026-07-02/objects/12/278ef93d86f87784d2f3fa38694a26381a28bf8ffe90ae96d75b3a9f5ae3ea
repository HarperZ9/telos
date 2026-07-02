# Dogfood Pass 0050 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `0db250ed75fa5cf2`;
- claims: `8`;
- match: `8`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `0db250ed75fa5cf223c2f6a7251194661188aa8b29073fcbcdbbe95293f4fc2b`;
- verdict seal: `e0a7cf2791442f6c12924219486377ab71b6eff21dfc71f63ac6287560fdd515`;
- measurement seal: `c0a3eab9bed3c300351e80d346b5866593bb9820d67f27a204585c95763f4de9`;
- assessment seal: `1a973532ac137cfbe055e7a557589e9381dc79f47a6ff78e0fad4b61b4fdc470`.

Pass theme: public demo spec for the first 30-day market push. This pass maps
the agent action proof packet demo to existing local Telos contracts and marks
the missing integration seams.

```text
schema = AgentActionProofPacketDemoSpecSet/v1
status = AGENT_ACTION_PROOF_PACKET_DEMO_SPEC_MATCH
primary_market = agent_action_proof_packets
component_count = 11
summary_match_count = 3
integration_gap_count = 6
demo_flow_step_count = 10
uniqueness_claim_status = HYPOTHESIS_ONLY
```

Core architectural decision: the public demo should be a packet composer over
existing receipts, not a monolithic replacement. The pieces already present are
action receipts, admission telemetry, browser evidence, loop ledger,
workstation substrate, model foundry, flagship action envelopes, context pack,
Telos MCP/operator surfaces, and follow-on display-calibration lanes.

## Explicit Integration Gaps

| Gap | Role |
| --- | --- |
| `trace_ingest_adapter` | Import LangSmith/Langfuse/Phoenix/OpenTelemetry traces into proof packet source refs. |
| `packet_composer` | Join source refs, workspace refs, admission telemetry, action receipt, browser evidence, loop ledger, and Crucible verdict. |
| `public_demo_fixture` | Create one sanitized multi-tool action fixture with no private payloads and stable hashes. |
| `redaction_policy` | Define field-level public/private boundaries for evidence, screenshots, page state, and tool outputs. |
| `verifier_runner` | Run validator and Crucible from one command and emit a portable proof bundle. |
| `export_bundle` | Emit markdown, JSON, and small static web view for buyer review. |

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_agent_action_proof_packet_demo_spec.py` | Agent action proof-packet demo spec generator. |
| `tools/validate_pass_0050_agent_action_proof_packet_demo_spec.py` | Validator for local component mapping, summaries, gaps, pass 0049 binding, and non-promotion controls. |
| `fixtures/agent-action-proof-packet-demo-spec-pass-0050.json` | Demo spec fixture. |
| `packets/060-agent-action-proof-packet-demo-spec.md` | Human-readable demo spec packet. |
| `adversarial/pass-0050-agent-action-proof-packet-demo-spec-steelman.md` | Local pass 0050 steelman. |
| `schemas/agent-action-proof-packet-demo-spec-pass-0050.json` | `AgentActionProofPacketDemoSpecSet/v1` artifact. |
| `schemas/pass-0050-agent-action-proof-packet-demo-spec-validator-result.json` | Validator receipt for pass 0050. |
| `schemas/tool-receipts-pass-0050.json` | Compact Index, Gather, Shell, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0050-thesis.json` | Falsifiable claims for the fiftieth pass. |
| `crucible/pass-0050-measurements.json` | Measurements/evidence for the fiftieth pass. |
| `crucible/pass-0050-report.md` | Crucible report for the fiftieth pass. |
| `crucible/pass-0050-run.json` | Crucible run record for the fiftieth pass. |

## Primary Next Push

Pass 0051 should turn the spec into a negative-fixture contract: define what
must fail when a packet lacks source refs, workspace refs, admission telemetry,
action receipt linkage, browser evidence, ledger continuity, or Crucible
verdicts.

Current promoted natural laws: none.
