# Packet 036: Redaction Boundary

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Pass 0026 adds a redaction-boundary proof to the action receipt chain. A
fixture raw payload is written to a temp-private local file, while the dogfood
artifacts carry only digest-bound redacted refs. The validator scans the
model-facing pass files for the raw payload and reports whether it leaked.

This is a local redaction proof. It does not prove production DLP,
cryptographic secrecy, external vault integration, live Telos runtime
integration, scientific discovery, theorem proof, or any natural law.

## Receipt Summary

Primary schema:

```text
schemas/redaction-boundary-pass-0026.json
```

Receipt seal:

```text
adcdfc1abcdb59427573760f4779182da9f9fde18553c633af5b08fc57f1816c
```

Raw payload digest:

```text
sha256 = 8c53911bf4e3763486de4c3dd43a0e1a8a587f3b172e08c322202d1b3fd66ca4
```

The raw payload value is intentionally not printed in this packet.

## Boundary

Raw payload:

```text
storage_boundary = TEMP_PRIVATE_NOT_COMMITTED
value_in_receipts = false
value_in_model_facing_artifacts = false
```

Source receipt:

```text
source = schemas/action-receipt-persistence-replay-pass-0025.json
source_sha256 = 03832d00e62c33828cbb5c6d351a10e47e5f61ac185f318044829910bdd0f293
ledger_head_hash = 6d194872068da0e9c74d95478cca7e4f2c5a447da9a82a73be3ce9b5aa44f371
```

Redacted refs:

| Ref | Path | Carries Raw Value | Carries Digest Ref |
| --- | --- | --- | --- |
| before | `fixtures/redacted-before-pass-0026.json` | `false` | `true` |
| after | `fixtures/redacted-after-pass-0026.json` | `false` | `true` |

## Action Receipt Redaction Ref

The redaction fixture binds the action receipt to digest-bearing refs:

```text
event_id = evt_dogfood_0026_redaction_boundary
redacted_before_ref = artifact:fixtures/redacted-before-pass-0026.json
redacted_after_ref = artifact:fixtures/redacted-after-pass-0026.json
raw_payload_digest = sha256:8c53911bf4e3763486de4c3dd43a0e1a8a587f3b172e08c322202d1b3fd66ca4
raw_payload_required_for_model = false
verification.verdict = MATCH
```

## Leak Scan Targets

The validator scans these model-facing surfaces:

- `schemas/redaction-boundary-pass-0026.json`;
- `fixtures/redacted-before-pass-0026.json`;
- `fixtures/redacted-after-pass-0026.json`;
- `packets/036-redaction-boundary.md`;
- `adversarial/pass-0026-redaction-boundary-steelman.md`;
- `schemas/tool-receipts-pass-0026.json`;
- `crucible/pass-0026-thesis.json`;
- `crucible/pass-0026-measurements.json`.

The expected result is:

```text
raw_payload_leak_count = 0
```

## Negative Fixtures

| Fixture | Expected Result |
| --- | --- |
| `negative-raw-payload-in-packet` | `REJECT` |
| `negative-raw-payload-in-receipt` | `REJECT` |
| `negative-redacted-ref-missing-digest` | `REJECT` |
| `negative-digest-mismatch` | `REJECT` |
| `negative-before-ref-missing` | `REJECT` |
| `negative-after-ref-missing` | `REJECT` |
| `negative-raw-path-committed` | `REJECT` |
| `negative-leak-scan-target-missing` | `REJECT` |

## Market Implication

This pass adds the privacy boundary needed for high-stakes action proof
packets:

```text
raw payload stays local
model-facing artifacts carry digest refs
redacted refs remain replayable
leak scan protects packet publication
```

For regulated AI infrastructure buyers, this is the difference between
observability logs that accidentally become data stores and proof packets that
carry verifiable evidence without exposing private payloads.

## Next Push

Pass 0027 should export a minimal verification bundle to a fresh temp directory
and replay it without relying on the dogfood repo path:

- source fixture digest;
- redacted refs;
- validator script;
- packet digest;
- Crucible measurement packet;
- no raw payload value;
- fresh-directory replay verdict.

## Natural-Law Promotion

Current promoted natural laws: none.
