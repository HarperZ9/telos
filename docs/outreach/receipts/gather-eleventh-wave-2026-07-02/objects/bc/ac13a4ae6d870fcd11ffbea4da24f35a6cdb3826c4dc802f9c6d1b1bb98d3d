# Packet 037: Redacted Ref Replay

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Pass 0027 takes the pass 0026 redaction-boundary artifact and replays it from a
fresh temp bundle using only redacted artifact refs, SHA-256 values, and digest
strings. The replay deliberately does not require raw payload material.

This is a local replay proof. It does not prove production DLP, cryptographic
secrecy, external vault integration, live Telos runtime integration, theorem
proof, scientific discovery, buyer adoption, or any natural law.

## Receipt Summary

Primary schema:

```text
schemas/redacted-ref-replay-pass-0027.json
```

Receipt seal:

```text
da9d1c939bcc56eb33711537ab6cd491f8e9e70c91920d3e6a42572b8d985576
```

Source binding:

```text
source = schemas/redaction-boundary-pass-0026.json
source_sha256 = cb4233fcdafb0c35fb7b87ac78dcbc6f7dbec980614049d1fd63f08595757e80
source_seal = adcdfc1abcdb59427573760f4779182da9f9fde18553c633af5b08fc57f1816c
```

## Replay Contract

Replay contract:

```text
schema = RedactedRefReplayContract/v1
action_id = act_dogfood_0024_001
event_id = evt_dogfood_0026_redaction_boundary
raw_payload_value_used = false
raw_payload_material_available_to_replay = false
fresh_replay_verdict = MATCH
redacted_ref_count = 2
contract_hash = 4498487ca72ca41e69ebb1fb84a9d2991855ee4537c2b24c77198d2ebc2335f9
```

Replay inputs:

```text
source action_receipt_redaction object
redacted before artifact
redacted after artifact
artifact SHA-256 values
digest refs
```

Redacted refs:

| Ref | Source Path | Source SHA-256 | Bundle SHA-256 | Digest Ref | Unredacted Prefix |
| --- | --- | --- | --- | --- | --- |
| before | `fixtures/redacted-before-pass-0026.json` | `32ba5ef8fcc63fb0e7bb2f3d9a84d272693971dcc524f27021fe4ad29d6dc231` | `32ba5ef8fcc63fb0e7bb2f3d9a84d272693971dcc524f27021fe4ad29d6dc231` | `true` | `false` |
| after | `fixtures/redacted-after-pass-0026.json` | `e697e1ecd32c15eec3032b001596cae71021b08808db9d597bbb4a08c6bf8c9f` | `e697e1ecd32c15eec3032b001596cae71021b08808db9d597bbb4a08c6bf8c9f` | `true` | `false` |

## Fresh Bundle

Fresh replay manifest:

```text
manifest = fixtures/redacted-ref-replay-manifest-pass-0027.json
manifest_sha256 = 47181c707049aea7573282b30cce175f51de014845ca5dd26bd1c933dd208fa3
manifest_seal = 2eb54dfc3b6974d35396c2ef597e3eec2ccb1269a88f678ceea976ad34a5f739
bundle_storage_boundary = TEMP_PRIVATE_NOT_COMMITTED
bundle_under_repo = false
file_count = 3
bundle_index_hash = 5b7ee765157d297dd17db5f61a7057c1a6a2c315bb03484346cd7d118bbdb32e
```

Manifest files:

```text
redacted-before.json
redacted-after.json
replay-contract.json
```

## Raw Material Policy

Policy:

```text
raw_payload_value_used = false
raw_payload_material_available_to_replay = false
raw_payload_value_required = false
digest_ref_required = true
redacted_refs_required = true
sentinel_prefix_allowed_in_model_facing_artifacts = false
```

The scanner token value is not written into model-facing pass 0027 artifacts.
The policy carries only a hash of that token.

## Leak Scan Targets

The validator scans these model-facing surfaces for the unredacted scanner
token:

- `schemas/redacted-ref-replay-pass-0027.json`;
- `fixtures/redacted-ref-replay-manifest-pass-0027.json`;
- `fixtures/redacted-before-pass-0026.json`;
- `fixtures/redacted-after-pass-0026.json`;
- `packets/037-redacted-ref-replay.md`;
- `adversarial/pass-0027-redacted-ref-replay-steelman.md`;
- `schemas/tool-receipts-pass-0027.json`;
- `crucible/pass-0027-thesis.json`;
- `crucible/pass-0027-measurements.json`.

Expected result:

```text
sentinel_prefix_leak_count = 0
```

## Negative Fixtures

| Fixture | Expected Result |
| --- | --- |
| `negative-raw-payload-value-required` | `REJECT` |
| `negative-missing-before-ref` | `REJECT` |
| `negative-missing-after-ref` | `REJECT` |
| `negative-before-sha-drift` | `REJECT` |
| `negative-after-sha-drift` | `REJECT` |
| `negative-digest-mismatch` | `REJECT` |
| `negative-temp-bundle-under-repo` | `REJECT` |
| `negative-unredacted-sentinel-present` | `REJECT` |
| `negative-source-seal-drift` | `REJECT` |

## Market Implication

This pass strengthens the proof-packet wedge for regulated agent and research
workflows:

```text
private material can remain outside model context
published packets can retain replayable refs
fresh-context validation can avoid raw payload dependence
action receipts can bind redaction evidence without becoming a data lake
```

That is a sharper market position than generic tracing: trace logs show what
happened, while replayable redaction refs let a buyer inspect whether a
high-stakes action packet can be verified without exposing sensitive material.

## Next Push

Pass 0028 should connect this replay boundary to a browser/source evidence
receipt:

- source URL or file evidence digest;
- redacted browser evidence snapshot;
- action receipt event that references the source evidence;
- replay from redacted refs plus source digest;
- validator rejection for source-digest drift and evidence omission.

## Natural-Law Promotion

Current promoted natural laws: none.
