"""Validate pass 0024 Telos action receipt fixture chain."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "telos-action-receipt-fixture-pass-0024.json"
PREV_RECEIPT_PATH = ROOT / "schemas" / "otel-recording-span-venv-pass-0023.json"
GENESIS_CHAIN_HASH = "0" * 64
ALLOWED_VERDICTS = {"MATCH", "DRIFT", "UNVERIFIABLE"}
ALLOWED_POLICIES = {"allow", "block", "escalate", "require_review"}
ALLOWED_SIDE_EFFECTS = {"none", "read", "write", "external_call", "human_action", "mixed"}
ALLOWED_STATES = {"proposed", "admitted", "running", "completed", "failed", "cancelled", "compensated"}
REQUIRED_EVENT_FIELDS = [
    "action_id",
    "action_intent_id",
    "event_id",
    "event_type",
    "idempotency_key",
    "action",
    "intent_ref",
    "authority_ref",
    "execution_ref",
    "evidence_ref",
    "review_ref",
    "compensation_ref",
    "trace",
    "execution",
    "agent",
    "component",
    "input_materials",
    "side_effect",
    "policy",
    "verification",
    "result",
    "retry",
    "receipts",
    "persistence",
    "created_at",
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def event_hash_body(event: dict[str, object]) -> dict[str, object]:
    body = copy.deepcopy(event)
    body.pop("event_hash", None)
    persistence = body.get("persistence")
    if isinstance(persistence, dict):
        persistence.pop("write_hash", None)
        persistence.pop("chain_hash", None)
    return body


def nonzero_hex(value: object, width: int) -> bool:
    text = str(value or "")
    return len(text) == width and set(text) != {"0"} and all(char in "0123456789abcdef" for char in text)


def main() -> int:
    data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    prev = json.loads(PREV_RECEIPT_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    require(data.get("schema") == "TelosActionReceiptFixtureSet/v1", errors, "wrong schema")
    require(data.get("pass") == "0024", errors, "wrong pass")
    require(data.get("status") == "ACTION_RECEIPT_FIXTURE_MATCH", errors, "wrong status")
    expected_seal = sha256_obj({k: v for k, v in data.items() if k != "seal"})
    require(data.get("seal") == expected_seal, errors, "seal mismatch")
    require("does not prove live Telos runtime persistence" in data.get("non_promotion_statement", ""), errors, "missing runtime non-promotion")
    require("does not prove" in data.get("non_promotion_statement", ""), errors, "missing non-promotion boundary")

    artifacts = data.get("source_artifacts", [])
    require(data.get("source_artifact_count") == len(artifacts), errors, "source artifact count mismatch")
    for artifact in artifacts:
        path = ROOT / artifact.get("path", "")
        require(path.exists(), errors, f"missing source artifact {artifact.get('path')}")
        if path.exists():
            require(artifact.get("sha256") == sha256_file(path), errors, f"source artifact digest mismatch {artifact.get('path')}")

    contract = data.get("telos_contract_excerpt", {})
    require(contract.get("schema") == "project-telos.action-receipt/v1", errors, "wrong contract schema")
    require(contract.get("digest_references_required") is True, errors, "contract digest references not required")
    require(contract.get("append_only_compensation_required") is True, errors, "contract append-only compensation not required")
    require(contract.get("receipt_is_trace_span") is False, errors, "contract incorrectly treats receipt as span")
    require(contract.get("links_to_trace_span") is True, errors, "contract does not link to span")
    require(contract.get("proposed_completed_action_separation_required") is True, errors, "contract missing proposed/completed separation")
    require(data.get("telos_contract_excerpt_sha256") == sha256_obj(contract), errors, "contract digest mismatch")

    upstream = data.get("upstream_span", {})
    prev_span = prev.get("recording_span_fixture", {})
    require(upstream.get("schema") == "OpenTelemetryRecordingSpanFixture/v1", errors, "wrong upstream span schema")
    require(upstream.get("source_pass") == "0023", errors, "wrong upstream pass")
    require(upstream.get("trace_id_hex") == prev_span.get("trace_id_hex"), errors, "trace id drift from pass 0023")
    require(upstream.get("span_id_hex") == prev_span.get("span_id_hex"), errors, "span id drift from pass 0023")
    require(upstream.get("exporter_sink_hash") == prev_span.get("exporter_sink_hash"), errors, "exporter sink hash drift")
    require(upstream.get("fixture_hash") == prev_span.get("fixture_hash"), errors, "fixture hash drift")
    require(upstream.get("receipt_is_trace_span") is False, errors, "upstream treated as receipt span")
    require(upstream.get("links_to_action_receipt") is True, errors, "upstream missing action receipt link")
    require(nonzero_hex(upstream.get("trace_id_hex"), 32), errors, "upstream trace id malformed")
    require(nonzero_hex(upstream.get("span_id_hex"), 16), errors, "upstream span id malformed")
    expected_span_ref = f"otel:trace/{upstream.get('trace_id_hex')}/span/{upstream.get('span_id_hex')}"
    require(upstream.get("span_ref") == expected_span_ref, errors, "upstream span ref mismatch")

    chain = data.get("action_chain", {})
    events = chain.get("events", [])
    require(chain.get("schema") == "TelosActionReceiptFixtureChain/v1", errors, "wrong action chain schema")
    require(data.get("event_count") == len(events), errors, "event count mismatch at root")
    require(chain.get("event_count") == len(events), errors, "event count mismatch in chain")
    require(len(events) == 4, errors, "expected four receipt events")
    require(chain.get("event_types") == [event.get("event_type") for event in events], errors, "event type list mismatch")
    require(chain.get("event_types") == ["action_proposed", "action_admitted", "execution_completed", "verification_recorded"], errors, "wrong event order")

    previous_chain_hash = GENESIS_CHAIN_HASH
    seen_event_ids: set[str] = set()
    for index, event in enumerate(events):
        for field in REQUIRED_EVENT_FIELDS:
            require(field in event, errors, f"event {index} missing {field}")
        require(event.get("event_id") not in seen_event_ids, errors, f"duplicate event id {event.get('event_id')}")
        seen_event_ids.add(event.get("event_id"))
        require(event.get("action_id") == chain.get("action_id"), errors, f"event {index} action id drift")
        require(event.get("action_intent_id") == chain.get("action_intent_id"), errors, f"event {index} intent id drift")
        require(bool(event.get("idempotency_key")), errors, f"event {index} missing idempotency key")
        require(event.get("idempotency_key") == chain.get("idempotency_key"), errors, f"event {index} idempotency drift")
        require(event.get("trace", {}).get("receipt_is_trace_span") is False, errors, f"event {index} treats receipt as trace span")
        require(event.get("trace", {}).get("span_ref") == expected_span_ref, errors, f"event {index} span ref mismatch")
        require(event.get("execution", {}).get("external_request_id") == chain.get("external_request_id"), errors, f"event {index} external request id drift")
        require(event.get("execution", {}).get("idempotency_key") == chain.get("idempotency_key"), errors, f"event {index} execution idempotency drift")
        require(bool(event.get("execution", {}).get("redacted_before_ref")), errors, f"event {index} missing before ref")
        require(bool(event.get("execution", {}).get("redacted_after_ref")), errors, f"event {index} missing after ref")
        require(event.get("component", {}).get("name") == "telos.action.receipt.fixture", errors, f"event {index} wrong component")
        require(str(event.get("component", {}).get("config_hash", "")).startswith("sha256:"), errors, f"event {index} missing config hash")
        require(event.get("side_effect", {}).get("class") in ALLOWED_SIDE_EFFECTS, errors, f"event {index} invalid side effect")
        require(event.get("policy", {}).get("decision") in ALLOWED_POLICIES, errors, f"event {index} invalid policy decision")
        require(bool(event.get("policy", {}).get("ref")), errors, f"event {index} missing policy ref")
        require(event.get("verification", {}).get("verdict") in ALLOWED_VERDICTS, errors, f"event {index} invalid verdict")
        require(bool(event.get("verification", {}).get("ref")), errors, f"event {index} missing verification ref")
        require(event.get("result", {}).get("state") in ALLOWED_STATES, errors, f"event {index} invalid result state")
        require(event.get("result", {}).get("stop_reason") == "completed", errors, f"event {index} untyped stop reason")
        require(event.get("retry", {}).get("attempt") == 1, errors, f"event {index} retry attempt drift")
        require(event.get("retry", {}).get("max_attempts") == 1, errors, f"event {index} retry max drift")
        require(event.get("persistence", {}).get("append_only") is True, errors, f"event {index} not append-only")
        require(event.get("persistence", {}).get("previous_chain_hash") == previous_chain_hash, errors, f"event {index} previous chain hash mismatch")
        recomputed_event_hash = sha256_obj(event_hash_body(event))
        require(event.get("event_hash") == recomputed_event_hash, errors, f"event {index} event hash mismatch")
        recomputed_chain_hash = sha256_text(f"{previous_chain_hash}\n{recomputed_event_hash}")
        require(event.get("persistence", {}).get("chain_hash") == recomputed_chain_hash, errors, f"event {index} chain hash mismatch")
        require(event.get("persistence", {}).get("write_hash") == f"sha256:{recomputed_event_hash}", errors, f"event {index} write hash mismatch")
        materials = event.get("input_materials", [])
        require(len(materials) >= 4, errors, f"event {index} missing input materials")
        require(all(str(material.get("digest", "")).startswith("sha256:") for material in materials), errors, f"event {index} material missing digest")
        require(any(material.get("role") == "upstream_span_receipt" for material in materials), errors, f"event {index} missing span material")
        require(any(material.get("role") == "upstream_human_packet" for material in materials), errors, f"event {index} missing packet material")
        require(any(material.get("role") == "telos_contract_excerpt" for material in materials), errors, f"event {index} missing contract material")
        previous_chain_hash = recomputed_chain_hash

    require(chain.get("chain_head_hash") == previous_chain_hash, errors, "chain head hash mismatch")

    negatives = data.get("negative_fixtures", [])
    require(data.get("negative_fixture_count") == len(negatives), errors, "negative count mismatch")
    require(len(negatives) >= 9, errors, "expected at least nine negatives")
    require(all(n.get("expected_validator_status") == "REJECT" for n in negatives), errors, "negative fixture not rejected")
    failure_codes = {n.get("failure_code") for n in negatives}
    for code in [
        "completed_action_collapsed_into_trace_span",
        "missing_material_digest",
        "verification_missing",
        "policy_decision_unjoined",
        "proposed_completed_action_collapsed",
        "non_append_only_compensation",
        "unjoinable_execution_span",
    ]:
        require(code in failure_codes, errors, f"missing negative failure code {code}")

    result = {
        "schema": "Pass0024TelosActionReceiptFixtureValidatorRun/v1",
        "pass": "0024",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "TelosActionReceiptFixtureSet",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "event_count": len(events),
                "negative_fixture_count": len(negatives),
                "chain_head_hash": chain.get("chain_head_hash"),
                "trace_id_hex": upstream.get("trace_id_hex"),
                "span_id_hex": upstream.get("span_id_hex"),
                "receipt_is_trace_span": upstream.get("receipt_is_trace_span"),
                "errors": errors,
            }
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
