# Dogfood Pass 0051 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `3363cc6e51abc319`;
- claims: `8`;
- match: `8`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `3363cc6e51abc319cc98c537a384c6443448fad1498908809372e015b6f8ae1a`;
- verdict seal: `c33304428b49e3b7e3e57dd876c3fe3e2972ed93ca647d82e313275dd092d8b2`;
- measurement seal: `cf323ad6a5b5e141cb0c118faf39b00887e43c9db4b663f743d97951a9f9862a`;
- assessment seal: `edf6060952e0c402547c220a56769af58193d7db22602e16630a9cdf88bfb3a0`.

Pass theme: negative fixtures for the agent action proof packet demo. This pass
defines what must fail before the packet composer is treated as usable.

```text
schema = AgentActionProofPacketNegativeFixturesSet/v1
status = AGENT_ACTION_PROOF_PACKET_NEGATIVE_FIXTURES_MATCH
positive_match_count = 1
negative_fixture_count = 8
negative_match_count = 8
failure_code_count = 8
uniqueness_claim_status = HYPOTHESIS_ONLY
```

The positive synthetic packet validates as `MATCH`. Each negative fixture
observes the expected `DRIFT` or `UNVERIFIABLE` verdict; no negative fixture
passes.

## Negative Fixtures

| Fixture | Expected failure | Expected verdict |
| --- | --- | --- |
| `missing_source_refs` | `source_refs_missing` | `UNVERIFIABLE` |
| `missing_workspace_context` | `workspace_context_ref_missing` | `UNVERIFIABLE` |
| `missing_admission_record` | `admission_record_missing` | `UNVERIFIABLE` |
| `broken_action_receipt_linkage` | `action_receipt_linkage_broken` | `DRIFT` |
| `missing_browser_evidence` | `browser_evidence_missing` | `UNVERIFIABLE` |
| `broken_ledger_continuity` | `ledger_continuity_broken` | `DRIFT` |
| `missing_crucible_verdict` | `crucible_verdict_missing` | `UNVERIFIABLE` |
| `raw_private_payload_leak` | `private_payload_boundary_violation` | `DRIFT` |

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_agent_action_proof_packet_negative_fixtures.py` | Negative-fixture generator for agent action proof packets. |
| `tools/validate_pass_0051_agent_action_proof_packet_negative_fixtures.py` | Validator for positive fixture, negative verdicts, failure codes, pass 0050 binding, and non-promotion controls. |
| `fixtures/agent-action-proof-packet-negative-fixtures-pass-0051.json` | Negative-fixture set and positive synthetic packet. |
| `packets/061-agent-action-proof-packet-negative-fixtures.md` | Human-readable negative-fixture packet. |
| `adversarial/pass-0051-agent-action-proof-packet-negative-fixtures-steelman.md` | Local pass 0051 steelman. |
| `schemas/agent-action-proof-packet-negative-fixtures-pass-0051.json` | `AgentActionProofPacketNegativeFixturesSet/v1` artifact. |
| `schemas/pass-0051-agent-action-proof-packet-negative-fixtures-validator-result.json` | Validator receipt for pass 0051. |
| `schemas/tool-receipts-pass-0051.json` | Compact Index, Gather, Shell, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0051-thesis.json` | Falsifiable claims for the fifty-first pass. |
| `crucible/pass-0051-measurements.json` | Measurements/evidence for the fifty-first pass. |
| `crucible/pass-0051-report.md` | Crucible report for the fifty-first pass. |
| `crucible/pass-0051-run.json` | Crucible run record for the fifty-first pass. |

## Primary Next Push

Pass 0052 should define the packet-composer build contract: input schemas,
bundle layout, one-command runner, expected public artifact tree, and the
minimum integration needed to turn these fixtures into an executable public
demo.

Current promoted natural laws: none.
