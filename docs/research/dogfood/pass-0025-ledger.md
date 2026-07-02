# Dogfood Pass 0025 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `a0ff13a2ffd88f25`;
- claims: `10`;
- match: `10`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `a0ff13a2ffd88f25e130127a32659fff5f30f64a1499ee3aba66f119f6564d35`;
- verdict seal: `b3b040750157abf29a0ba7bf4ad55d221b421bf152eda6754a272f86aeabbc80`;
- measurement seal: `b2874648e3575ec9f9a4740d19a36634bd292081049521c619a254c81aa825eb`;
- assessment seal: `00afae6a9aaef65d6d9560963fbf6e39b6db0e99b4a4769a5d6830c03b71b8f8`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Registry stats after pass 0025:

- theses: `22`;
- claims: `186`;
- unique claims: `186`;
- assessments: `22`;
- latest assessments: `22`;
- invalid latest assessments: `0`;
- verdicts: `MATCH=186`, `DRIFT=0`, `UNVERIFIABLE=0`.

Pass theme: persist pass 0024 action receipt events into an append-only JSONL
ledger, replay the ledger from disk, preserve original event hashes, and append
one compensation event without mutation.

No production database durability, distributed consensus, cryptographic signing,
external anchoring, live Telos runtime integration, external write safety, buyer
adoption signal, theorem proof, scientific discovery, biological result,
material result, medical result, finance result, safety result, or natural law
is promoted in this pass.

## Primary Receipt

Receipt schema:

```text
ActionReceiptPersistenceReplaySet/v1
```

Receipt seal:

```text
7203957ec04350756af9cdb2d244760ebbc2c00bbc3fcc048acd7c9ff2a1a177
```

Validator result:

```text
status = MATCH
match = 1
drift = 0
line_count = 5
negative_fixture_count = 11
ledger_head_hash = 6d194872068da0e9c74d95478cca7e4f2c5a447da9a82a73be3ce9b5aa44f371
compensation_event_id = evt_dogfood_0025_005_compensation_completed
```

## Ledger

Ledger file:

```text
fixtures/telos-action-receipt-ledger-pass-0025.jsonl
```

Ledger receipt:

```text
sha256 = 66a536120c2d95e2d5b1a879fbe34f8b908327dfc356bcfcf530dadc2f44dfab
line_count = 5
write_mode = append-only-jsonl
canonical_json_lines = true
ledger_head_hash = 6d194872068da0e9c74d95478cca7e4f2c5a447da9a82a73be3ce9b5aa44f371
```

Strict loader:

```text
object_pairs_hook_required = true
parse_constant_rejects_nonfinite = true
duplicate_keys_rejected = true
allow_nan_on_serialization = false
```

## Source Binding

Source fixture:

```text
schemas/telos-action-receipt-fixture-pass-0024.json
```

Source binding:

```text
source_sha256 = 9c6402f98774170311d78ea3f6983cae71a665dd38ab2ee7e88d413398990ff4
source_event_count = 4
source_chain_head_hash = 0617602eed957e0bc6c2e4a21548528f6defc542c4468433bde85df76cb51b3a
source_chain_head_preserved_at_entry_4 = true
original_event_hashes_match_source = true
```

## Append-Only Compensation

Compensation event:

```text
event_id = evt_dogfood_0025_005_compensation_completed
event_type = compensation_completed
event_hash = 85ae96fca309e5303c4ca4aba9c7058c215c70ccf928fbf384f748689ddc044f
previous_chain_hash = 0617602eed957e0bc6c2e4a21548528f6defc542c4468433bde85df76cb51b3a
chain_hash = 9e8311cf3b5cec4c3424cab1c5d7883b475fba35c70224dfb921fdacb2797a5f
```

Replay:

```text
replayed_event_count = 5
appended_event_count = 1
event_id_index_hash = 47664ad56ddceb13b4356ad4152d119f4e52ef1a67baeb1a7c93e0d6945356ca
```

## Tool Substrate Receipt

Pass 0025 refreshed the tool surfaces:

| Tool | Status | Note |
| --- | --- | --- |
| Index | `MATCH` | Version 2.8.0; status and doctor available. |
| Gather | `MATCH` | Version 1.5.0; packet 035 read verified. |
| Telos | `MATCH` | Operator doctor 14/14; action receipt and loop ledger surfaced. |
| Forum | `MATCH_WITH_SUBMIT_GAP` | Status and ledger verification work; submit is `UNVERIFIABLE` because no model executor is configured. |
| Crucible | `MATCH` | Version 1.1.0; pass 0025 assessment matched. |

Gather docs receipt for packet 035:

```text
sha256=0d9694013e0555b8249c608b327692c1d58d022c7853528770572d656476a1f5
seal=3fbf1c9cb69a4795cd1e2377f17a12a4cdb774fbbd77c07a43f86d50b1bcd663
chars=5410
```

Forum submit attempt:

```text
status=UNVERIFIABLE
error=submit needs a model executor
```

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_action_receipt_persistence_replay.py` | Append-only JSONL ledger and replay fixture generator. |
| `tools/validate_pass_0025_action_receipt_persistence.py` | Validator for strict JSONL loading, entry hashes, event hashes, replay indexes, source preservation, and compensation append. |
| `fixtures/telos-action-receipt-ledger-pass-0025.jsonl` | Append-only JSONL action receipt ledger fixture. |
| `packets/035-action-receipt-persistence-replay.md` | Human-readable persistence replay packet. |
| `adversarial/pass-0025-persistence-replay-steelman.md` | Local pass 0025 steelman. |
| `schemas/action-receipt-persistence-replay-pass-0025.json` | `ActionReceiptPersistenceReplaySet/v1` artifact. |
| `schemas/pass-0025-action-receipt-persistence-validator-result.json` | Validator receipt for pass 0025. |
| `schemas/tool-receipts-pass-0025.json` | Compact Index, Gather, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0025-thesis.json` | Falsifiable claims for the twenty-fifth pass. |
| `crucible/pass-0025-measurements.json` | Measurements/evidence for the twenty-fifth pass. |
| `crucible/pass-0025-report.md` | Crucible assessment report. |
| `crucible/pass-0025-run.json` | Crucible run record. |

## Primary Next Push

Build a redaction-boundary fixture for action receipts.

The next proof should include:

- raw payload fixture stored only in local/private fixture material;
- redacted before/after refs in action receipt events;
- raw payload digest in the receipt without raw payload exposure;
- leak scan over packet, measurements, and public-facing docs;
- replay from digest refs only;
- negative fixtures for raw payload leakage and digest mismatch.

## Natural-Law Promotion

Current promoted natural laws: none.
