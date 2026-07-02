"""Generate pass 0024 Telos action receipt fixture chain."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


PASS = "0024"
ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "schemas" / "telos-action-receipt-fixture-pass-0024.json"
PREV_RECEIPT_PATH = ROOT / "schemas" / "otel-recording-span-venv-pass-0023.json"
PREV_VALIDATOR_PATH = ROOT / "schemas" / "pass-0023-otel-recording-span-venv-validator-result.json"
PREV_PACKET_PATH = ROOT / "packets" / "033-otel-recording-span-venv.md"
GENESIS_CHAIN_HASH = "0" * 64


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def make_input_material(ref: str, digest: str, role: str) -> dict[str, str]:
    return {
        "ref": ref,
        "digest": f"sha256:{digest}",
        "role": role,
    }


prev_receipt = json.loads(PREV_RECEIPT_PATH.read_text(encoding="utf-8"))
prev_validator = json.loads(PREV_VALIDATOR_PATH.read_text(encoding="utf-8"))
span = prev_receipt["recording_span_fixture"]

source_artifacts = [
    {
        "path": "schemas/otel-recording-span-venv-pass-0023.json",
        "role": "upstream_span_receipt",
        "sha256": sha256_file(PREV_RECEIPT_PATH),
        "schema": prev_receipt["schema"],
        "status": prev_receipt["status"],
    },
    {
        "path": "schemas/pass-0023-otel-recording-span-venv-validator-result.json",
        "role": "upstream_validator_receipt",
        "sha256": sha256_file(PREV_VALIDATOR_PATH),
        "schema": prev_validator["schema"],
        "status": prev_validator["status"],
    },
    {
        "path": "packets/033-otel-recording-span-venv.md",
        "role": "upstream_human_packet",
        "sha256": sha256_file(PREV_PACKET_PATH),
        "schema": "MarkdownPacket/v1",
        "status": "GATHERED_IN_PASS_0023",
    },
]

contract_excerpt = {
    "schema": "project-telos.action-receipt/v1",
    "digest_references_required": True,
    "append_only_compensation_required": True,
    "receipt_is_trace_span": False,
    "links_to_trace_span": True,
    "proposed_completed_action_separation_required": True,
    "exportable_outside_trace_retention": True,
    "verification_verdicts": ["MATCH", "DRIFT", "UNVERIFIABLE"],
}
contract_digest = sha256_obj(contract_excerpt)

action_id = "act_dogfood_0024_001"
intent_id = "intent_dogfood_0024_001"
idempotency_key = "idem_dogfood_0024_001"
external_request_id = "local:dogfood-pass-0024-action-receipt-fixture"
trace_id = span["trace_id_hex"]
span_id = span["span_id_hex"]
span_ref = f"otel:trace/{trace_id}/span/{span_id}"
component_config = {
    "contract_digest": contract_digest,
    "pass": PASS,
    "generator": "tools/probe_telos_action_receipt_fixture.py",
    "upstream_receipt_seal": prev_receipt["seal"],
}
component_hash = sha256_obj(component_config)
args_hash = sha256_obj(
    {
        "action": "create-local-telos-action-receipt-fixture",
        "source_artifacts": source_artifacts,
        "span_ref": span_ref,
    }
)

input_materials = [
    make_input_material(item["path"], item["sha256"], item["role"])
    for item in source_artifacts
]
input_materials.append(
    make_input_material(
        "mcp:telos.action.receipt/project-telos.action-receipt-v1-excerpt",
        contract_digest,
        "telos_contract_excerpt",
    )
)

base_event = {
    "action_id": action_id,
    "action_intent_id": intent_id,
    "idempotency_key": idempotency_key,
    "action": {
        "kind": "file_write",
        "destination_class": "local_dogfood_artifact",
        "args_hash": f"sha256:{args_hash}",
        "risk_class": "local_research_fixture_write",
    },
    "intent_ref": "artifact:packets/033-otel-recording-span-venv.md#next-push",
    "authority_ref": "goal:019f1c75-ab64-79b0-92ba-63ecd9354d2e",
    "execution_ref": "local-command:tools/probe_telos_action_receipt_fixture.py",
    "evidence_ref": "artifact:schemas/otel-recording-span-venv-pass-0023.json",
    "review_ref": "validator:tools/validate_pass_0024_telos_action_receipt_fixture.py",
    "compensation_ref": None,
    "trace": {
        "receipt_is_trace_span": False,
        "span_ref": span_ref,
        "trace_id_hex": trace_id,
        "span_id_hex": span_id,
        "exporter_sink_hash": span["exporter_sink_hash"],
        "session_ref": "session:telos-dogfood-pass-0024",
    },
    "authority": {
        "operator_goal_ref": "goal:019f1c75-ab64-79b0-92ba-63ecd9354d2e",
        "policy_ref": "policy:dogfood-local-proof-fixture-v1",
        "capability_lease_ref": "capability:local-artifact-write/dogfood-research",
        "credential_ref": "credential-ref:none",
    },
    "actor": {
        "agent_id": "agent:codex.dogfood-research",
        "tool_id": "local:python",
        "mcp_connector_snapshot": f"sha256:{contract_digest}",
        "external_account_ref": "account:none",
        "auth_scopes_ref": "scope-ref:local-filesystem-dogfood",
    },
    "execution": {
        "external_request_id": external_request_id,
        "idempotency_key": idempotency_key,
        "terminal_status": "completed",
        "redacted_before_ref": "artifact:local-dogfood/pass-0023-state-redacted",
        "redacted_after_ref": "artifact:schemas/telos-action-receipt-fixture-pass-0024.json",
        "result_hash": f"sha256:{args_hash}",
        "result_ref": "artifact:schemas/telos-action-receipt-fixture-pass-0024.json",
    },
    "agent": {"principal": "agent:codex.dogfood-research"},
    "component": {
        "name": "telos.action.receipt.fixture",
        "version": "pass-0024",
        "config_hash": f"sha256:{component_hash}",
    },
    "input_materials": input_materials,
    "side_effect": {"class": "write", "reversible": True},
    "policy": {"decision": "allow", "ref": "policy:dogfood-local-proof-fixture-v1"},
    "verification": {
        "verdict": "MATCH",
        "ref": "validator:pass-0024-telos-action-receipt-fixture",
    },
    "retry": {"attempt": 1, "max_attempts": 1},
    "receipts": [
        {
            "kind": "upstream_span_fixture",
            "hash": f"sha256:{span['fixture_hash']}",
        },
        {
            "kind": "upstream_exporter_sink",
            "hash": f"sha256:{span['exporter_sink_hash']}",
        },
    ],
    "persistence": {
        "append_only": True,
        "storage_ref": "artifact:schemas/telos-action-receipt-fixture-pass-0024.json",
    },
}

event_specs = [
    ("evt_dogfood_0024_001_proposed", "action_proposed", "proposed", "2026-07-01T12:00:00Z"),
    ("evt_dogfood_0024_002_admitted", "action_admitted", "admitted", "2026-07-01T12:01:00Z"),
    ("evt_dogfood_0024_003_execution_completed", "execution_completed", "completed", "2026-07-01T12:02:00Z"),
    ("evt_dogfood_0024_004_verification_recorded", "verification_recorded", "completed", "2026-07-01T12:03:00Z"),
]

events: list[dict[str, object]] = []
previous_chain_hash = GENESIS_CHAIN_HASH
for event_id, event_type, result_state, created_at in event_specs:
    event = copy.deepcopy(base_event)
    event["event_id"] = event_id
    event["event_type"] = event_type
    event["result"] = {
        "state": result_state,
        "stop_reason": "completed",
        "output_ref": "artifact:schemas/telos-action-receipt-fixture-pass-0024.json",
    }
    event["created_at"] = created_at
    event["receipts"].append({"kind": "event_stage", "hash": f"sha256:{sha256_text(event_type)}"})
    finalized = finalize_event(event, previous_chain_hash)
    previous_chain_hash = finalized["persistence"]["chain_hash"]
    events.append(finalized)

record = {
    "schema": "TelosActionReceiptFixtureSet/v1",
    "pass": PASS,
    "generated_on": "2026-07-01",
    "status": "ACTION_RECEIPT_FIXTURE_MATCH",
    "source_artifacts": source_artifacts,
    "telos_contract_excerpt": contract_excerpt,
    "telos_contract_excerpt_sha256": contract_digest,
    "upstream_span": {
        "schema": "OpenTelemetryRecordingSpanFixture/v1",
        "source_pass": "0023",
        "trace_id_hex": trace_id,
        "span_id_hex": span_id,
        "span_ref": span_ref,
        "exporter_sink_hash": span["exporter_sink_hash"],
        "fixture_hash": span["fixture_hash"],
        "receipt_is_trace_span": False,
        "links_to_action_receipt": True,
    },
    "action_chain": {
        "schema": "TelosActionReceiptFixtureChain/v1",
        "action_id": action_id,
        "action_intent_id": intent_id,
        "idempotency_key": idempotency_key,
        "external_request_id": external_request_id,
        "event_count": len(events),
        "event_types": [event["event_type"] for event in events],
        "chain_head_hash": previous_chain_hash,
        "events": events,
    },
    "market_wedge": {
        "product": "agent action proof packet",
        "positioning_hypothesis": "OpenTelemetry spans become evidence inputs, while Telos receipts become the durable proof object for regulated or high-stakes agent actions.",
        "buyer": "AI infrastructure teams running multi-agent workflows with audit, policy, and provenance requirements",
        "proof_advantage": "joins source digest, command intent, action admission, trace span, verification verdict, and append-only receipt chain",
    },
    "negative_fixtures": [
        {
            "fixture_id": "negative-trace-only-receipt",
            "failure_code": "completed_action_collapsed_into_trace_span",
            "failure_mode": "The span id is stored as the only receipt and no action intent, policy, or evidence digest exists.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-action-without-command-digest",
            "failure_code": "missing_material_digest",
            "failure_mode": "The action claims a local command but does not include any digest-bound execution or args receipt.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-action-without-source-digest",
            "failure_code": "missing_material_digest",
            "failure_mode": "The receipt omits source artifact digests for the upstream OTel fixture and human packet.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-completed-without-verification",
            "failure_code": "verification_missing",
            "failure_mode": "A completed action lacks MATCH, DRIFT, or UNVERIFIABLE verification.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-policy-missing",
            "failure_code": "policy_decision_unjoined",
            "failure_mode": "The event carries no policy decision or policy reference.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-proposed-completed-collapsed",
            "failure_code": "proposed_completed_action_collapsed",
            "failure_mode": "A proposed action and completed action are represented as the same event.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-non-append-only-compensation",
            "failure_code": "non_append_only_compensation",
            "failure_mode": "A compensation or correction mutates an earlier event instead of appending a new event.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-missing-idempotency-key",
            "failure_code": "unjoinable_execution_span",
            "failure_mode": "The receipt cannot join action intent to execution because idempotency keys are missing.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-trace-span-treated-as-receipt",
            "failure_code": "completed_action_collapsed_into_trace_span",
            "failure_mode": "The fixture treats receipt_is_trace_span=true, collapsing observability evidence into the durable receipt.",
            "expected_validator_status": "REJECT",
        },
    ],
    "source_anchors": [
        {
            "source": "Telos action receipt interface",
            "url": "mcp:telos.action.receipt",
        },
        {
            "source": "Telos loop ledger contract",
            "url": "mcp:telos.loop.ledger",
        },
        {
            "source": "OpenTelemetry Python instrumentation",
            "url": "https://opentelemetry.io/docs/languages/python/instrumentation/",
        },
        {
            "source": "Pass 0023 OTel recording span packet",
            "url": "artifact:packets/033-otel-recording-span-venv.md",
        },
    ],
    "non_promotion_statement": "Pass 0024 proves only a deterministic local TelosActionReceiptFixture/v1-style chain over pass 0023 evidence. It does not prove live Telos runtime persistence, external writes, cloud trace export, buyer adoption, scientific discovery, theorem proof, or any natural law.",
}
record["negative_fixture_count"] = len(record["negative_fixtures"])
record["source_artifact_count"] = len(record["source_artifacts"])
record["event_count"] = len(events)
record["seal"] = sha256_obj({k: v for k, v in record.items() if k != "seal"})

OUT_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "path": str(OUT_PATH),
            "schema": record["schema"],
            "status": record["status"],
            "event_count": record["event_count"],
            "negative_fixture_count": record["negative_fixture_count"],
            "chain_head_hash": record["action_chain"]["chain_head_hash"],
            "seal": record["seal"],
        },
        indent=2,
        sort_keys=True,
    )
)
