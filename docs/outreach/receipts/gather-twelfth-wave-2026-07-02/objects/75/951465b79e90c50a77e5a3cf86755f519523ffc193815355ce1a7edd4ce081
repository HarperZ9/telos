# Dogfood Pass 0028 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `530faf040e421279`;
- claims: `10`;
- match: `10`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `530faf040e42127981a9d9a5b0da979426f06e562b2eee55661dadbfe4c792fe`;
- verdict seal: `5dda01f777dfe3cc0b0f8a9be63bb7250fcac53dd3b2b43861d0d5f2116f6a67`;
- measurement seal: `eb4662ab99320291f92a323fd8324feb3158a9a992218fd99226df49a0ac7320`;
- assessment seal: `fd19d4098df956a5cc52486aeae01bbb77a3debced036de5ced1b34624ad6978`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Registry stats after pass 0028:

- theses: `25`;
- claims: `216`;
- unique claims: `216`;
- assessments: `25`;
- latest assessments: `25`;
- invalid latest assessments: `0`;
- verdicts: `MATCH=216`, `DRIFT=0`, `UNVERIFIABLE=0`.

Pass theme: bind pass 0027 redacted replay refs to a redacted browser-evidence
fixture, preserving network and console capture gaps as `UNVERIFIABLE`.

No live browser collection, production browser capture, production DLP, external
vault integration, external write safety, buyer adoption signal, theorem proof,
scientific discovery, biological result, material result, medical result,
finance result, safety result, or natural law is promoted in this pass.

## Primary Receipt

Receipt schema:

```text
SourceEvidenceBindingSet/v1
```

Receipt seal:

```text
879c147a7c755ca357eaf07802a893cb6a3a92752af0664a3ea2e1ec9565337e
```

Validator result:

```text
status = MATCH
match = 1
drift = 0
source_sha256 = 00573b3ff4eb47ca7a62759b9907af0e4db7c3bd4a4a468febc7700fa39527cb
browser_evidence_sha256 = d30289cfdcaf8630e7fb7b3ba911cbac485a62f5306e3b5c37338768dbfe9e7a
manifest_sha256 = f14f6450c44b1cd2b7b070f5c0a3bb6d6d0de03ee133e6650427423e82233853
negative_fixture_count = 9
scan_target_count = 8
raw_source_sentinel_leak_count = 0
network_summary_verdict = UNVERIFIABLE
console_summary_verdict = UNVERIFIABLE
```

## Source Binding

Source receipt:

```text
path = schemas/redacted-ref-replay-pass-0027.json
sha256 = 00573b3ff4eb47ca7a62759b9907af0e4db7c3bd4a4a468febc7700fa39527cb
schema = RedactedRefReplaySet/v1
seal = da9d1c939bcc56eb33711537ab6cd491f8e9e70c91920d3e6a42572b8d985576
replay_contract_hash = 4498487ca72ca41e69ebb1fb84a9d2991855ee4537c2b24c77198d2ebc2335f9
```

## Browser Evidence

Browser evidence fixture:

```text
path = fixtures/browser-evidence-redacted-pass-0028.json
sha256 = d30289cfdcaf8630e7fb7b3ba911cbac485a62f5306e3b5c37338768dbfe9e7a
fixture_hash = ba8adef6e7b8f9795403bb85b38b87196644f75d09960aae4312cce5af134614
schema = project-telos.browser-evidence/v1
tool = telos.browser.evidence
target_ref = url:sha256:100680ad546ce6a577f42f52df33b4cfdca756859e664b8d7de329b150d09ce9
redaction_status = redacted
verification_verdict = MATCH
network_summary_verdict = UNVERIFIABLE
console_summary_verdict = UNVERIFIABLE
```

## Action Receipt Binding

Binding object:

```text
schema = ActionReceiptSourceEvidenceBinding/v1
action_id = act_dogfood_0028_source_evidence
event_id = evt_dogfood_0028_source_evidence_bound
event_type = evidence_bound
evidence_ref = artifact:fixtures/browser-evidence-redacted-pass-0028.json
evidence_digest = sha256:d30289cfdcaf8630e7fb7b3ba911cbac485a62f5306e3b5c37338768dbfe9e7a
source_replay_ref = artifact:schemas/redacted-ref-replay-pass-0027.json
source_replay_digest = sha256:00573b3ff4eb47ca7a62759b9907af0e4db7c3bd4a4a468febc7700fa39527cb
raw_source_material_required = false
raw_browser_payload_required = false
verification_verdict = MATCH
```

## Fresh Replay

Replay manifest:

```text
manifest = fixtures/source-evidence-replay-manifest-pass-0028.json
manifest_sha256 = f14f6450c44b1cd2b7b070f5c0a3bb6d6d0de03ee133e6650427423e82233853
manifest_seal = 1e5209f5d84fd7ee77fbe4b5388d777e568d23dececdd7d48ddd18eb55c3da5f
input_ref_count = 3
network_console_unverifiable_preserved = true
raw_source_material_required = false
raw_browser_payload_required = false
replay_verdict = MATCH
```

## Leak Scan

Scan targets:

```text
schemas/source-evidence-binding-pass-0028.json
fixtures/browser-evidence-redacted-pass-0028.json
fixtures/source-evidence-replay-manifest-pass-0028.json
packets/038-source-evidence-binding.md
adversarial/pass-0028-source-evidence-steelman.md
schemas/tool-receipts-pass-0028.json
crucible/pass-0028-thesis.json
crucible/pass-0028-measurements.json
```

Negative fixtures:

```text
negative-source-replay-sha-drift
negative-browser-evidence-omitted
negative-browser-evidence-sha-drift
negative-raw-source-required
negative-raw-browser-payload-required
negative-network-unverifiable-promoted
negative-console-unverifiable-promoted
negative-redaction-status-unredacted
negative-source-sentinel-present
```

All negative fixtures expect validator status `REJECT`.

## Tool Substrate Receipt

Pass 0028 refreshed the tool surfaces:

| Tool | Status | Note |
| --- | --- | --- |
| Index | `MATCH` | Version 2.8.0; status and doctor available. |
| Gather | `MATCH` | Version 1.5.0; packet 038 read verified. |
| Telos | `MATCH` | Operator doctor 14/14; catalog, browser evidence, action receipt, and loop ledger surfaced. |
| Forum | `MATCH_WITH_SUBMIT_GAP` | Status and ledger verification work; submit is `UNVERIFIABLE` because no model executor is configured. |
| Crucible | `MATCH` | Version 1.1.0; pass 0028 assessment matched. |

Gather docs receipt for packet 038:

```text
sha256=33f2c1ae730dc4a432a2fbed476216e3099632a5d97ba1c4eb1a9ad6ec0223ce
seal=e9cf92d20156ace6be6657b714050fb9281beec1df308f9f77b8e418f304a258
chars=5389
```

Forum submit attempt:

```text
status=UNVERIFIABLE
error=submit needs a model executor
```

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_source_evidence_binding.py` | Source/browser evidence binding fixture generator. |
| `tools/validate_pass_0028_source_evidence_binding.py` | Validator for source replay binding, browser evidence digest, replay manifest, gap preservation, leak scan, and negative fixtures. |
| `fixtures/browser-evidence-redacted-pass-0028.json` | Redacted browser-evidence fixture. |
| `fixtures/source-evidence-replay-manifest-pass-0028.json` | Source evidence replay manifest. |
| `packets/038-source-evidence-binding.md` | Human-readable source evidence binding packet. |
| `adversarial/pass-0028-source-evidence-steelman.md` | Forum failure receipt plus local pass 0028 steelman. |
| `schemas/source-evidence-binding-pass-0028.json` | `SourceEvidenceBindingSet/v1` artifact. |
| `schemas/pass-0028-source-evidence-binding-validator-result.json` | Validator receipt for pass 0028. |
| `schemas/tool-receipts-pass-0028.json` | Compact Index, Gather, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0028-thesis.json` | Falsifiable claims for the twenty-eighth pass. |
| `crucible/pass-0028-measurements.json` | Measurements/evidence for the twenty-eighth pass. |
| `crucible/pass-0028-report.md` | Crucible assessment report. |
| `crucible/pass-0028-run.json` | Crucible run record. |

## Primary Next Push

Connect source evidence binding to an executable research claim packet.

The next proof should include:

- one small source-backed claim;
- source evidence digest;
- model/action receipt proposal;
- verifier measurement;
- explicit `UNVERIFIABLE` preservation where evidence is incomplete;
- rejection tests for unsupported claim promotion.

## Natural-Law Promotion

Current promoted natural laws: none.
