# Packet 035: Action Receipt Persistence Replay

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Pass 0025 takes the pass 0024 action receipt fixture out of a single JSON
object and writes it into a local append-only JSONL ledger. It then replays that
ledger from disk, rebuilds lookup indexes, preserves the original pass 0024
event hashes, and appends one compensation event without mutating history.

This is still a local persistence proof. It does not prove production database
durability, distributed consensus, cryptographic signing, external anchoring,
live Telos runtime integration, external write safety, scientific discovery,
theorem proof, or any natural law.

## Receipt Summary

Primary schema:

```text
schemas/action-receipt-persistence-replay-pass-0025.json
```

Receipt seal:

```text
7203957ec04350756af9cdb2d244760ebbc2c00bbc3fcc048acd7c9ff2a1a177
```

Validator result:

```text
schema = Pass0025ActionReceiptPersistenceValidatorRun/v1
status = MATCH
match = 1
drift = 0
line_count = 5
negative_fixture_count = 11
```

Ledger:

```text
path = fixtures/telos-action-receipt-ledger-pass-0025.jsonl
sha256 = 66a536120c2d95e2d5b1a879fbe34f8b908327dfc356bcfcf530dadc2f44dfab
ledger_head_hash = 6d194872068da0e9c74d95478cca7e4f2c5a447da9a82a73be3ce9b5aa44f371
line_count = 5
```

## Source Fixture

The ledger is bound back to pass 0024:

```text
source_fixture = schemas/telos-action-receipt-fixture-pass-0024.json
source_sha256 = 9c6402f98774170311d78ea3f6983cae71a665dd38ab2ee7e88d413398990ff4
source_chain_head_hash = 0617602eed957e0bc6c2e4a21548528f6defc542c4468433bde85df76cb51b3a
source_event_count = 4
```

Replay confirms:

```text
source_chain_head_preserved_at_entry_4 = true
original_event_hashes_match_source = true
```

That matters because pass 0025 is allowed to append. It is not allowed to edit
the pass 0024 events.

## Append-Only Replay

The replay produces:

```text
replayed_event_count = 5
appended_event_count = 1
last_event_chain_hash = 9e8311cf3b5cec4c3424cab1c5d7883b475fba35c70224dfb921fdacb2797a5f
event_id_index_hash = 47664ad56ddceb13b4356ad4152d119f4e52ef1a67baeb1a7c93e0d6945356ca
```

The appended event is:

```text
event_id = evt_dogfood_0025_005_compensation_completed
event_type = compensation_completed
event_hash = 85ae96fca309e5303c4ca4aba9c7058c215c70ccf928fbf384f748689ddc044f
previous_chain_hash = 0617602eed957e0bc6c2e4a21548528f6defc542c4468433bde85df76cb51b3a
chain_hash = 9e8311cf3b5cec4c3424cab1c5d7883b475fba35c70224dfb921fdacb2797a5f
```

The compensation event points back to the pass 0024 action id and preserves the
original completed event as an immutable prior ledger line.

## Lookup Probes

The replay builds these indexes:

| Probe | Key | Match Count |
| --- | --- | --- |
| action id | `act_dogfood_0024_001` | `5` |
| action intent id | `intent_dogfood_0024_001` | `5` |
| compensation event id | `evt_dogfood_0025_005_compensation_completed` | `1` |
| compensation idempotency key | `idem_dogfood_0025_compensation_001` | `1` |

These lookups are the minimum product requirement for a runtime receipt store:
the system must be able to find the action, intent, specific event, and
idempotency envelope after context has been compacted or restarted.

## Strict Ledger Loader

The fixture requires:

```text
canonical_json_lines = true
object_pairs_hook_required = true
parse_constant_rejects_nonfinite = true
duplicate_keys_rejected = true
allow_nan_on_serialization = false
```

This is a direct replay of the strict-runtime concern from earlier passes: a
receipt store that accepts duplicate JSON keys, NaN, Infinity, or non-canonical
lines cannot be trusted as a proof substrate.

## Negative Fixtures

| Fixture | Expected Result |
| --- | --- |
| `negative-mutate-earlier-event` | `REJECT` |
| `negative-delete-event` | `REJECT` |
| `negative-reorder-events` | `REJECT` |
| `negative-duplicate-event-id` | `REJECT` |
| `negative-idempotency-mismatch` | `REJECT` |
| `negative-append-without-previous-head` | `REJECT` |
| `negative-compensation-mutates-original` | `REJECT` |
| `negative-non-canonical-json-line` | `REJECT` |
| `negative-duplicate-json-key` | `REJECT` |
| `negative-nonfinite-json` | `REJECT` |
| `negative-replay-without-source-fixture` | `REJECT` |

## Market Implication

Pass 0025 moves the agent action proof-packet wedge one layer closer to a real
product:

```text
Trace evidence -> action receipt fixture -> append-only ledger -> fresh-context replay.
```

This is the primitive that observability and eval tools usually do not own:
the durable, replayable operational claim. A buyer can inspect a receipt after
trace retention windows, after redaction, and after agent context loss.

The next market-facing demo should show a small agent action that creates:

- an OpenTelemetry span;
- a Telos action receipt event;
- an append-only JSONL ledger line;
- a replay index;
- a compensation append;
- a Crucible verdict;
- a Gather packet digest.

## Next Push

Pass 0026 should add a redaction-boundary fixture:

- raw payload fixture stays local and out of packet text;
- redacted before/after refs are written to receipts;
- raw payload digest is verifiable without exposing the payload;
- leak scan proves the raw secret string is absent from packet, model-facing
  measurement, and public docs;
- replay still works from digest refs only.

## Natural-Law Promotion

Current promoted natural laws: none.
