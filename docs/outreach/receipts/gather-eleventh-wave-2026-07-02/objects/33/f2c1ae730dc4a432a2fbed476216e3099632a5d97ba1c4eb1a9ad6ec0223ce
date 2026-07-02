# Packet 038: Source Evidence Binding

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Pass 0028 binds the pass 0027 redacted-ref replay contract to a redacted
browser-evidence fixture. The evidence packet carries source URL digests,
browser text digests, redacted artifact refs, and explicit `UNVERIFIABLE`
network/console capture verdicts.

This is a local source-evidence binding proof. It does not prove live browser
collection, production browser capture, production DLP, external vault
integration, theorem proof, scientific discovery, buyer adoption, or any
natural law.

## Receipt Summary

Primary schema:

```text
schemas/source-evidence-binding-pass-0028.json
```

Receipt seal:

```text
879c147a7c755ca357eaf07802a893cb6a3a92752af0664a3ea2e1ec9565337e
```

Source binding:

```text
source = schemas/redacted-ref-replay-pass-0027.json
source_sha256 = 00573b3ff4eb47ca7a62759b9907af0e4db7c3bd4a4a468febc7700fa39527cb
source_seal = da9d1c939bcc56eb33711537ab6cd491f8e9e70c91920d3e6a42572b8d985576
replay_contract_hash = 4498487ca72ca41e69ebb1fb84a9d2991855ee4537c2b24c77198d2ebc2335f9
```

## Browser Evidence

Browser evidence fixture:

```text
path = fixtures/browser-evidence-redacted-pass-0028.json
sha256 = d30289cfdcaf8630e7fb7b3ba911cbac485a62f5306e3b5c37338768dbfe9e7a
schema = project-telos.browser-evidence/v1
tool = telos.browser.evidence
target_ref = url:sha256:100680ad546ce6a577f42f52df33b4cfdca756859e664b8d7de329b150d09ce9
redaction_status = redacted
verification_verdict = MATCH
```

Digest fields:

```text
before_url_digest = url:sha256:100680ad546ce6a577f42f52df33b4cfdca756859e664b8d7de329b150d09ce9
after_url_digest = url:sha256:100680ad546ce6a577f42f52df33b4cfdca756859e664b8d7de329b150d09ce9
after_text_digest = text:sha256:f94d9486b327090cccbeb97d67953a1f234b83d67350b7b5f60196b0a30f24db
```

Preserved gaps:

```text
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
verification.verdict = MATCH
```

The binding keeps the pass 0027 redacted before/after refs:

```text
redacted_before_ref = fixtures/redacted-before-pass-0026.json
redacted_after_ref = fixtures/redacted-after-pass-0026.json
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

Replay inputs:

```text
source replay digest
browser evidence digest
redacted before/after refs
```

## Leak Scan

The validator scans these model-facing surfaces for the raw source scanner
token:

- `schemas/source-evidence-binding-pass-0028.json`;
- `fixtures/browser-evidence-redacted-pass-0028.json`;
- `fixtures/source-evidence-replay-manifest-pass-0028.json`;
- `packets/038-source-evidence-binding.md`;
- `adversarial/pass-0028-source-evidence-steelman.md`;
- `schemas/tool-receipts-pass-0028.json`;
- `crucible/pass-0028-thesis.json`;
- `crucible/pass-0028-measurements.json`.

Expected result:

```text
raw_source_sentinel_leak_count = 0
```

## Negative Fixtures

| Fixture | Expected Result |
| --- | --- |
| `negative-source-replay-sha-drift` | `REJECT` |
| `negative-browser-evidence-omitted` | `REJECT` |
| `negative-browser-evidence-sha-drift` | `REJECT` |
| `negative-raw-source-required` | `REJECT` |
| `negative-raw-browser-payload-required` | `REJECT` |
| `negative-network-unverifiable-promoted` | `REJECT` |
| `negative-console-unverifiable-promoted` | `REJECT` |
| `negative-redaction-status-unredacted` | `REJECT` |
| `negative-source-sentinel-present` | `REJECT` |

## Market Implication

This pass adds the next product layer for proof packets:

```text
source evidence can be bound by digest
browser capture gaps remain explicitly UNVERIFIABLE
raw source material stays outside the replay path
action receipts can cite source evidence without becoming raw evidence stores
```

For research labs and regulated AI teams, this is the bridge from internal
action receipts to source-backed proof packets. It lets a reviewer inspect
where the evidence came from, what was redacted, and which capture surfaces are
still unverifiable.

## Next Push

Pass 0029 should connect source evidence binding to an executable research
claim packet:

- one small source-backed claim;
- source evidence digest;
- model/action receipt proposal;
- verifier measurement;
- explicit `UNVERIFIABLE` preservation where evidence is incomplete;
- rejection tests for unsupported claim promotion.

## Natural-Law Promotion

Current promoted natural laws: none.
