"""Validate pass 0025 action receipt persistence and replay receipts."""

from __future__ import annotations

import copy
import hashlib
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "action-receipt-persistence-replay-pass-0025.json"
SOURCE_PATH = ROOT / "schemas" / "telos-action-receipt-fixture-pass-0024.json"
LEDGER_PATH = ROOT / "fixtures" / "telos-action-receipt-ledger-pass-0025.jsonl"
ZERO_HASH = "0" * 64


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant rejected: {value}")


def strict_loads(raw_json: str) -> tuple[object | None, list[str], str | None]:
    duplicate_keys: list[str] = []

    def hook(pairs):
        seen: defaultdict[str, int] = defaultdict(int)
        out = {}
        for key, value in pairs:
            seen[key] += 1
            if seen[key] > 1:
                duplicate_keys.append(key)
            out[key] = value
        return out

    try:
        parsed = json.loads(raw_json, object_pairs_hook=hook, parse_constant=reject_constant)
    except ValueError as exc:
        return None, duplicate_keys, str(exc)
    if duplicate_keys:
        return None, sorted(set(duplicate_keys)), "duplicate JSON object keys rejected"
    return parsed, [], None


def event_hash_body(event: dict[str, object]) -> dict[str, object]:
    body = copy.deepcopy(event)
    body.pop("event_hash", None)
    persistence = body.get("persistence")
    if isinstance(persistence, dict):
        persistence.pop("write_hash", None)
        persistence.pop("chain_hash", None)
    return body


def entry_hash_body(entry: dict[str, object]) -> dict[str, object]:
    body = copy.deepcopy(entry)
    body.pop("entry_hash", None)
    return body


def load_ledger(errors: list[str]) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for line_no, raw in enumerate(LEDGER_PATH.read_text(encoding="utf-8").splitlines(), start=1):
        require(raw == canonical_json(json.loads(raw)), errors, f"ledger line {line_no} is not canonical JSON")
        parsed, duplicates, error = strict_loads(raw)
        require(parsed is not None, errors, f"ledger line {line_no} strict load failed: {error or duplicates}")
        if isinstance(parsed, dict):
            entries.append(parsed)
    return entries


def main() -> int:
    data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    source = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    require(data.get("schema") == "ActionReceiptPersistenceReplaySet/v1", errors, "wrong schema")
    require(data.get("pass") == "0025", errors, "wrong pass")
    require(data.get("status") == "ACTION_RECEIPT_PERSISTENCE_REPLAY_MATCH", errors, "wrong status")
    expected_seal = sha256_obj({key: value for key, value in data.items() if key != "seal"})
    require(data.get("seal") == expected_seal, errors, "seal mismatch")
    require("local append-only JSONL persistence" in data.get("non_promotion_statement", ""), errors, "missing non-promotion")

    source_fixture = data.get("source_fixture", {})
    require(source_fixture.get("path") == "schemas/telos-action-receipt-fixture-pass-0024.json", errors, "wrong source fixture path")
    require(source_fixture.get("sha256") == sha256_file(SOURCE_PATH), errors, "source fixture sha256 mismatch")
    require(source_fixture.get("seal") == source.get("seal"), errors, "source fixture seal mismatch")
    require(source_fixture.get("source_chain_head_hash") == source.get("action_chain", {}).get("chain_head_hash"), errors, "source chain head mismatch")
    require(source_fixture.get("source_event_count") == 4, errors, "source event count mismatch")

    ledger = data.get("ledger", {})
    require(ledger.get("path") == "fixtures/telos-action-receipt-ledger-pass-0025.jsonl", errors, "wrong ledger path")
    require(ledger.get("sha256") == sha256_file(LEDGER_PATH), errors, "ledger sha256 mismatch")
    require(ledger.get("line_count") == 5, errors, "ledger line count mismatch")
    require(ledger.get("write_mode") == "append-only-jsonl", errors, "wrong ledger write mode")
    require(ledger.get("canonical_json_lines") is True, errors, "canonical JSON not enforced")
    strict = ledger.get("strict_loader", {})
    require(strict.get("object_pairs_hook_required") is True, errors, "strict loader missing object_pairs_hook")
    require(strict.get("parse_constant_rejects_nonfinite") is True, errors, "strict loader does not reject nonfinite")
    require(strict.get("duplicate_keys_rejected") is True, errors, "strict loader does not reject duplicates")
    require(strict.get("allow_nan_on_serialization") is False, errors, "serialization allows NaN")

    entries = load_ledger(errors)
    require(len(entries) == ledger.get("line_count"), errors, "loaded entry count mismatch")

    previous_entry_hash = ZERO_HASH
    previous_event_chain_hash = None
    event_ids: set[str] = set()
    action_lookup: defaultdict[str, int] = defaultdict(int)
    intent_lookup: defaultdict[str, int] = defaultdict(int)
    idempotency_lookup: defaultdict[str, int] = defaultdict(int)
    original_hashes = [event["event_hash"] for event in source["action_chain"]["events"]]

    for index, entry in enumerate(entries, start=1):
        require(entry.get("schema") == "TelosActionReceiptLedgerEntry/v1", errors, f"entry {index} wrong schema")
        require(entry.get("pass") == "0025", errors, f"entry {index} wrong pass")
        require(entry.get("sequence") == index, errors, f"entry {index} sequence mismatch")
        require(entry.get("previous_entry_hash") == previous_entry_hash, errors, f"entry {index} previous entry hash mismatch")
        recomputed_entry_hash = sha256_obj(entry_hash_body(entry))
        require(entry.get("entry_hash") == recomputed_entry_hash, errors, f"entry {index} entry hash mismatch")
        event = entry.get("event", {})
        require(entry.get("event_id") == event.get("event_id"), errors, f"entry {index} event id drift")
        require(entry.get("event_type") == event.get("event_type"), errors, f"entry {index} event type drift")
        require(entry.get("action_id") == event.get("action_id"), errors, f"entry {index} action id drift")
        require(entry.get("action_intent_id") == event.get("action_intent_id"), errors, f"entry {index} intent id drift")
        require(entry.get("idempotency_key") == event.get("idempotency_key"), errors, f"entry {index} idempotency drift")
        require(event.get("execution", {}).get("idempotency_key") == event.get("idempotency_key"), errors, f"entry {index} execution idempotency mismatch")
        recomputed_event_hash = sha256_obj(event_hash_body(event))
        require(entry.get("event_hash") == recomputed_event_hash, errors, f"entry {index} event hash mismatch")
        require(event.get("event_hash") == recomputed_event_hash, errors, f"entry {index} nested event hash mismatch")
        event_chain_hash = event.get("persistence", {}).get("chain_hash")
        require(entry.get("event_chain_hash") == event_chain_hash, errors, f"entry {index} event chain hash mismatch")
        require(event.get("persistence", {}).get("append_only") is True, errors, f"entry {index} event not append-only")
        require(event.get("event_id") not in event_ids, errors, f"duplicate event id {event.get('event_id')}")
        event_ids.add(event.get("event_id"))
        action_lookup[str(event.get("action_id"))] += 1
        intent_lookup[str(event.get("action_intent_id"))] += 1
        idempotency_lookup[str(event.get("idempotency_key"))] += 1
        if index <= 4:
            require(entry.get("event_hash") == original_hashes[index - 1], errors, f"source event {index} mutated")
        if index == 4:
            require(entry.get("event_chain_hash") == source["action_chain"]["chain_head_hash"], errors, "source chain head not preserved at entry 4")
        if index == 5:
            require(event.get("event_type") == "compensation_completed", errors, "entry 5 is not compensation")
            require(event.get("compensates") == source["action_chain"]["action_id"], errors, "compensation target mismatch")
            require(event.get("result", {}).get("state") == "compensated", errors, "compensation state mismatch")
            require(event.get("result", {}).get("stop_reason") == "compensated", errors, "compensation stop reason mismatch")
            require(event.get("persistence", {}).get("previous_chain_hash") == source["action_chain"]["chain_head_hash"], errors, "compensation does not append from source head")
        previous_entry_hash = recomputed_entry_hash
        previous_event_chain_hash = event_chain_hash

    replay = data.get("replay", {})
    require(replay.get("replayed_event_count") == 5, errors, "replay event count mismatch")
    require(replay.get("ledger_head_hash") == previous_entry_hash, errors, "replay ledger head mismatch")
    require(ledger.get("ledger_head_hash") == previous_entry_hash, errors, "ledger head mismatch")
    require(replay.get("last_event_chain_hash") == previous_event_chain_hash, errors, "last event chain mismatch")
    require(replay.get("source_chain_head_preserved_at_entry_4") is True, errors, "source chain head not preserved flag false")
    require(replay.get("original_event_hashes_match_source") is True, errors, "original hash match flag false")
    require(replay.get("appended_event_count") == 1, errors, "appended event count mismatch")
    require(replay.get("compensation_previous_chain_hash") == source["action_chain"]["chain_head_hash"], errors, "compensation previous chain hash drift")
    require(replay.get("compensation_event_id") == "evt_dogfood_0025_005_compensation_completed", errors, "wrong compensation event id")

    lookup_counts = replay.get("lookup_counts", {})
    action_id = source["action_chain"]["action_id"]
    intent_id = source["action_chain"]["action_intent_id"]
    require(action_lookup[action_id] == 5, errors, "action lookup count mismatch")
    require(intent_lookup[intent_id] == 5, errors, "intent lookup count mismatch")
    require(lookup_counts.get("by_action_id", {}).get(action_id) == 5, errors, "recorded action lookup mismatch")
    require(lookup_counts.get("by_action_intent_id", {}).get(intent_id) == 5, errors, "recorded intent lookup mismatch")
    require(lookup_counts.get("by_event_id") == 5, errors, "recorded event id lookup count mismatch")
    require(idempotency_lookup["idem_dogfood_0025_compensation_001"] == 1, errors, "compensation idempotency lookup mismatch")

    mutation = data.get("mutation_probe", {})
    require(mutation.get("mutated_original_event_allowed") is False, errors, "mutation allowed")
    require(mutation.get("source_event_hashes_before") == original_hashes, errors, "mutation before hashes drift")
    require(mutation.get("source_event_hashes_after_replay") == original_hashes, errors, "mutation after hashes drift")
    require(mutation.get("status") == "ORIGINAL_EVENTS_UNCHANGED", errors, "mutation status mismatch")

    negatives = data.get("negative_fixtures", [])
    require(data.get("negative_fixture_count") == len(negatives), errors, "negative count mismatch")
    require(len(negatives) >= 11, errors, "expected at least 11 negatives")
    require(all(n.get("expected_validator_status") == "REJECT" for n in negatives), errors, "negative fixture not rejected")

    result = {
        "schema": "Pass0025ActionReceiptPersistenceValidatorRun/v1",
        "pass": "0025",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "ActionReceiptPersistenceReplaySet",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "line_count": len(entries),
                "ledger_head_hash": ledger.get("ledger_head_hash"),
                "last_event_chain_hash": replay.get("last_event_chain_hash"),
                "negative_fixture_count": len(negatives),
                "compensation_event_id": replay.get("compensation_event_id"),
                "errors": errors,
            }
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
