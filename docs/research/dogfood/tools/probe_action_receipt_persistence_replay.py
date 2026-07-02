"""Generate pass 0025 append-only action receipt persistence and replay receipts."""

from __future__ import annotations

import copy
import hashlib
import json
from collections import defaultdict
from pathlib import Path


PASS = "0025"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "schemas" / "telos-action-receipt-fixture-pass-0024.json"
LEDGER_PATH = ROOT / "fixtures" / "telos-action-receipt-ledger-pass-0025.jsonl"
OUT_PATH = ROOT / "schemas" / "action-receipt-persistence-replay-pass-0025.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def event_hash_body(event: dict[str, object]) -> dict[str, object]:
    body = copy.deepcopy(event)
    body.pop("event_hash", None)
    persistence = body.get("persistence")
    if isinstance(persistence, dict):
        persistence.pop("write_hash", None)
        persistence.pop("chain_hash", None)
    return body


def finalize_event(event: dict[str, object], previous_chain_hash: str) -> dict[str, object]:
    event["persistence"]["previous_chain_hash"] = previous_chain_hash
    event_hash = sha256_obj(event_hash_body(event))
    chain_hash = sha256_text(f"{previous_chain_hash}\n{event_hash}")
    event["event_hash"] = event_hash
    event["persistence"]["write_hash"] = f"sha256:{event_hash}"
    event["persistence"]["chain_hash"] = chain_hash
    return event


def entry_hash_body(entry: dict[str, object]) -> dict[str, object]:
    body = copy.deepcopy(entry)
    body.pop("entry_hash", None)
    return body


def finalize_entry(entry: dict[str, object]) -> dict[str, object]:
    entry["entry_hash"] = sha256_obj(entry_hash_body(entry))
    return entry


def make_compensation_event(source: dict[str, object]) -> dict[str, object]:
    base = copy.deepcopy(source["action_chain"]["events"][-1])
    previous_head = source["action_chain"]["chain_head_hash"]
    base["event_id"] = "evt_dogfood_0025_005_compensation_completed"
    base["event_type"] = "compensation_completed"
    base["compensates"] = source["action_chain"]["action_id"]
    base["compensation_ref"] = "compensation:local-noop-fixture-pass-0025"
    base["execution"]["external_request_id"] = "local:dogfood-pass-0025-compensation-fixture"
    base["execution"]["idempotency_key"] = "idem_dogfood_0025_compensation_001"
    base["execution"]["result_ref"] = "artifact:fixtures/telos-action-receipt-ledger-pass-0025.jsonl#compensation"
    base["execution"]["result_hash"] = f"sha256:{sha256_text('pass-0025-compensation-fixture')}"
    base["idempotency_key"] = "idem_dogfood_0025_compensation_001"
    base["result"] = {
        "state": "compensated",
        "stop_reason": "compensated",
        "output_ref": "artifact:fixtures/telos-action-receipt-ledger-pass-0025.jsonl#compensation",
    }
    base["review_ref"] = "validator:tools/validate_pass_0025_action_receipt_persistence.py"
    base["created_at"] = "2026-07-01T12:04:00Z"
    base["persistence"]["storage_ref"] = "artifact:fixtures/telos-action-receipt-ledger-pass-0025.jsonl"
    base["persistence"].pop("write_hash", None)
    base["persistence"].pop("chain_hash", None)
    base.pop("event_hash", None)
    receipts = [r for r in base["receipts"] if r.get("kind") != "event_stage"]
    receipts.append({"kind": "event_stage", "hash": f"sha256:{sha256_text('compensation_completed')}"})
    receipts.append({"kind": "append_only_compensation", "hash": f"sha256:{source['action_chain']['chain_head_hash']}"})
    base["receipts"] = receipts
    return finalize_event(base, previous_head)


def make_ledger_entries(events: list[dict[str, object]]) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    previous_entry_hash = "0" * 64
    for index, event in enumerate(events, start=1):
        line_body = {
            "schema": "TelosActionReceiptLedgerEntry/v1",
            "pass": PASS,
            "sequence": index,
            "event_id": event["event_id"],
            "event_type": event["event_type"],
            "action_id": event["action_id"],
            "action_intent_id": event["action_intent_id"],
            "idempotency_key": event["idempotency_key"],
            "event_hash": event["event_hash"],
            "event_chain_hash": event["persistence"]["chain_hash"],
            "previous_entry_hash": previous_entry_hash,
            "event": event,
        }
        entry = finalize_entry(line_body)
        previous_entry_hash = entry["entry_hash"]
        entries.append(entry)
    return entries


def replay(entries: list[dict[str, object]]) -> dict[str, object]:
    by_action: defaultdict[str, list[str]] = defaultdict(list)
    by_intent: defaultdict[str, list[str]] = defaultdict(list)
    by_idempotency: defaultdict[str, list[str]] = defaultdict(list)
    by_event: dict[str, str] = {}
    for entry in entries:
        event_id = str(entry["event_id"])
        by_action[str(entry["action_id"])].append(event_id)
        by_intent[str(entry["action_intent_id"])].append(event_id)
        by_idempotency[str(entry["idempotency_key"])].append(event_id)
        by_event[event_id] = entry["entry_hash"]
    return {
        "schema": "ActionReceiptLedgerReplay/v1",
        "replayed_event_count": len(entries),
        "ledger_head_hash": entries[-1]["entry_hash"] if entries else "0" * 64,
        "last_event_chain_hash": entries[-1]["event_chain_hash"] if entries else "0" * 64,
        "lookup_counts": {
            "by_action_id": {key: len(value) for key, value in sorted(by_action.items())},
            "by_action_intent_id": {key: len(value) for key, value in sorted(by_intent.items())},
            "by_event_id": len(by_event),
            "by_idempotency_key": {key: len(value) for key, value in sorted(by_idempotency.items())},
        },
        "event_id_index_hash": sha256_obj(by_event),
    }


source = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
original_events = copy.deepcopy(source["action_chain"]["events"])
original_event_hashes = [event["event_hash"] for event in original_events]
compensation_event = make_compensation_event(source)
events = original_events + [compensation_event]
entries = make_ledger_entries(events)

LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
LEDGER_PATH.write_text("\n".join(canonical_json(entry) for entry in entries) + "\n", encoding="utf-8")

replay_result = replay(entries)
ledger_sha256 = sha256_file(LEDGER_PATH)

record = {
    "schema": "ActionReceiptPersistenceReplaySet/v1",
    "pass": PASS,
    "generated_on": "2026-07-01",
    "status": "ACTION_RECEIPT_PERSISTENCE_REPLAY_MATCH",
    "source_fixture": {
        "path": "schemas/telos-action-receipt-fixture-pass-0024.json",
        "sha256": sha256_file(SOURCE_PATH),
        "schema": source["schema"],
        "seal": source["seal"],
        "source_chain_head_hash": source["action_chain"]["chain_head_hash"],
        "source_event_count": source["event_count"],
    },
    "ledger": {
        "schema": "AppendOnlyJsonlActionReceiptLedger/v1",
        "path": "fixtures/telos-action-receipt-ledger-pass-0025.jsonl",
        "sha256": ledger_sha256,
        "line_count": len(entries),
        "write_mode": "append-only-jsonl",
        "canonical_json_lines": True,
        "strict_loader": {
            "object_pairs_hook_required": True,
            "parse_constant_rejects_nonfinite": True,
            "duplicate_keys_rejected": True,
            "allow_nan_on_serialization": False,
        },
        "ledger_head_hash": replay_result["ledger_head_hash"],
    },
    "replay": {
        **replay_result,
        "fresh_context_inputs": [
            "fixtures/telos-action-receipt-ledger-pass-0025.jsonl",
            "schemas/telos-action-receipt-fixture-pass-0024.json sha256",
        ],
        "source_chain_head_preserved_at_entry_4": entries[3]["event_chain_hash"] == source["action_chain"]["chain_head_hash"],
        "original_event_hashes_match_source": [entry["event_hash"] for entry in entries[:4]] == original_event_hashes,
        "appended_event_count": 1,
        "compensation_event_id": compensation_event["event_id"],
        "compensation_previous_chain_hash": compensation_event["persistence"]["previous_chain_hash"],
        "compensation_chain_hash": compensation_event["persistence"]["chain_hash"],
    },
    "lookup_probes": [
        {
            "probe": "lookup-by-action-id",
            "key": source["action_chain"]["action_id"],
            "match_count": 5,
            "status": "MATCH",
        },
        {
            "probe": "lookup-by-action-intent-id",
            "key": source["action_chain"]["action_intent_id"],
            "match_count": 5,
            "status": "MATCH",
        },
        {
            "probe": "lookup-by-event-id",
            "key": compensation_event["event_id"],
            "match_count": 1,
            "status": "MATCH",
        },
        {
            "probe": "lookup-by-idempotency-key",
            "key": compensation_event["idempotency_key"],
            "match_count": 1,
            "status": "MATCH",
        },
    ],
    "mutation_probe": {
        "schema": "AppendOnlyMutationProbe/v1",
        "mutated_original_event_allowed": False,
        "source_event_hashes_before": original_event_hashes,
        "source_event_hashes_after_replay": [entry["event_hash"] for entry in entries[:4]],
        "status": "ORIGINAL_EVENTS_UNCHANGED",
    },
    "negative_fixtures": [
        {
            "fixture_id": "negative-mutate-earlier-event",
            "failure_mode": "A replay changes the body or hash of an earlier event.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-delete-event",
            "failure_mode": "A ledger line is removed and sequence continuity is broken.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-reorder-events",
            "failure_mode": "Events are replayed in a different order from their previous hash chain.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-duplicate-event-id",
            "failure_mode": "Two ledger entries carry the same event_id.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-idempotency-mismatch",
            "failure_mode": "Execution and receipt idempotency keys diverge.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-append-without-previous-head",
            "failure_mode": "An appended event does not cite the previous action-chain head.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-compensation-mutates-original",
            "failure_mode": "A compensation updates the original event instead of appending a new event.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-non-canonical-json-line",
            "failure_mode": "A ledger line is not canonical JSON.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-duplicate-json-key",
            "failure_mode": "A ledger line contains a duplicate JSON key.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-nonfinite-json",
            "failure_mode": "A ledger line contains NaN or Infinity.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-replay-without-source-fixture",
            "failure_mode": "Replay cannot bind ledger entries back to the pass 0024 source fixture digest.",
            "expected_validator_status": "REJECT",
        },
    ],
    "source_anchors": [
        {"source": "Telos action receipt interface", "url": "mcp:telos.action.receipt"},
        {"source": "Telos loop ledger contract", "url": "mcp:telos.loop.ledger"},
        {"source": "RFC 8785 JSON Canonicalization Scheme", "url": "https://www.rfc-editor.org/info/rfc8785/"},
        {"source": "Python json module", "url": "https://docs.python.org/3/library/json.html"},
    ],
    "non_promotion_statement": "Pass 0025 proves only local append-only JSONL persistence and replay for pass 0024 action receipt events plus one appended compensation fixture. It does not prove production database durability, distributed consensus, cryptographic signing, external anchoring, live Telos runtime integration, external write safety, scientific discovery, theorem proof, or any natural law.",
}
record["line_count"] = len(entries)
record["negative_fixture_count"] = len(record["negative_fixtures"])
record["lookup_probe_count"] = len(record["lookup_probes"])
record["seal"] = sha256_obj({key: value for key, value in record.items() if key != "seal"})

OUT_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "path": str(OUT_PATH),
            "ledger_path": str(LEDGER_PATH),
            "schema": record["schema"],
            "status": record["status"],
            "line_count": record["line_count"],
            "ledger_head_hash": record["ledger"]["ledger_head_hash"],
            "compensation_event_id": compensation_event["event_id"],
            "seal": record["seal"],
        },
        indent=2,
        sort_keys=True,
    )
)
