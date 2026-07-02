"""Generate pass 0051 negative fixtures for agent action proof packets."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


PASS = "0051"
ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_PACKET = ROOT / "schemas" / "agent-action-proof-packet-demo-spec-pass-0050.json"
OUT_PATH = ROOT / "schemas" / "agent-action-proof-packet-negative-fixtures-pass-0051.json"
FIXTURE_PATH = ROOT / "fixtures" / "agent-action-proof-packet-negative-fixtures-pass-0051.json"
PACKET_PATH = ROOT / "packets" / "061-agent-action-proof-packet-negative-fixtures.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0051-agent-action-proof-packet-negative-fixtures-steelman.md"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def with_seal(value: dict) -> dict:
    sealed = dict(value)
    sealed["seal"] = sha256_obj(value)
    return sealed


def positive_packet() -> dict:
    packet = {
        "schema": "project-telos.agent-action-proof-packet/v0",
        "packet_id": "agent-action-proof-packet-positive-0051",
        "source_refs": [{"id": "src-demo", "uri": "repo:demo/action-receipt.mjs", "sha256": "sha256:demo-source"}],
        "workspace_context_ref": {"tool": "index", "graph_pack_sha256": "sha256:demo-graph-pack"},
        "admission_record": {
            "action_intent_id": "intent-0051-demo",
            "args_hash": "sha256:demo-args",
            "criterion_ref": "criterion:agent-action-proof-packet-demo",
            "decision": {"outcome": "allow"},
            "verification": {"verdict": "MATCH"},
        },
        "action_receipt": {
            "action_id": "act-0051-demo",
            "action_intent_id": "intent-0051-demo",
            "event_id": "evt-0051-demo",
            "receipt_hash": "sha256:demo-action-receipt",
            "trace": {"span_ref": "trace:span-0051-demo"},
        },
        "browser_evidence_ref": {
            "action_receipt_ref": "act-0051-demo",
            "artifact_hashes": ["sha256:demo-browser-state"],
            "verification": {"verdict": "MATCH"},
        },
        "loop_ledger_entry": {
            "sequence": 51,
            "previous_hash": "sha256:previous-ledger-entry",
            "entry_hash": "sha256:current-ledger-entry",
            "chain": True,
        },
        "crucible_verdict": {"status": "MATCH", "assessment_seal": "sha256:demo-assessment-seal"},
        "redaction_status": {"hashes_only": True, "raw_private_payloads_included": False},
        "exports": {"json_bundle": True, "markdown_packet": True},
    }
    packet["packet_hash"] = sha256_obj(packet)
    return packet


NEGATIVE_MUTATIONS = [
    ("missing_source_refs", "source_refs_missing", "UNVERIFIABLE", lambda p: p.pop("source_refs", None)),
    ("missing_workspace_context", "workspace_context_ref_missing", "UNVERIFIABLE", lambda p: p.pop("workspace_context_ref", None)),
    ("missing_admission_record", "admission_record_missing", "UNVERIFIABLE", lambda p: p.pop("admission_record", None)),
    ("broken_action_receipt_linkage", "action_receipt_linkage_broken", "DRIFT", lambda p: p["action_receipt"].update({"action_intent_id": "intent-mismatch"})),
    ("missing_browser_evidence", "browser_evidence_missing", "UNVERIFIABLE", lambda p: p.pop("browser_evidence_ref", None)),
    ("broken_ledger_continuity", "ledger_continuity_broken", "DRIFT", lambda p: p["loop_ledger_entry"].update({"chain": False})),
    ("missing_crucible_verdict", "crucible_verdict_missing", "UNVERIFIABLE", lambda p: p.pop("crucible_verdict", None)),
    ("raw_private_payload_leak", "private_payload_boundary_violation", "DRIFT", lambda p: p["redaction_status"].update({"raw_private_payloads_included": True})),
]


def validate_packet(packet: dict) -> dict:
    checks = [
        ("source_refs", bool(packet.get("source_refs")), "source_refs_missing", "UNVERIFIABLE"),
        ("workspace_context_ref", bool(packet.get("workspace_context_ref")), "workspace_context_ref_missing", "UNVERIFIABLE"),
        ("admission_record", bool(packet.get("admission_record")), "admission_record_missing", "UNVERIFIABLE"),
        ("action_receipt", bool(packet.get("action_receipt")), "action_receipt_missing", "UNVERIFIABLE"),
        ("browser_evidence_ref", bool(packet.get("browser_evidence_ref")), "browser_evidence_missing", "UNVERIFIABLE"),
        ("loop_ledger_entry", bool(packet.get("loop_ledger_entry")), "loop_ledger_entry_missing", "UNVERIFIABLE"),
        ("crucible_verdict", bool(packet.get("crucible_verdict")), "crucible_verdict_missing", "UNVERIFIABLE"),
    ]
    for component, ok, failure_code, verdict in checks:
        if not ok:
            return {"component": component, "failure_code": failure_code, "verdict": verdict}
    if packet["admission_record"]["action_intent_id"] != packet["action_receipt"]["action_intent_id"]:
        return {"component": "action_receipt", "failure_code": "action_receipt_linkage_broken", "verdict": "DRIFT"}
    if packet["browser_evidence_ref"]["action_receipt_ref"] != packet["action_receipt"]["action_id"]:
        return {"component": "browser_evidence_ref", "failure_code": "browser_action_ref_broken", "verdict": "DRIFT"}
    if packet["loop_ledger_entry"].get("chain") is not True:
        return {"component": "loop_ledger_entry", "failure_code": "ledger_continuity_broken", "verdict": "DRIFT"}
    if packet["crucible_verdict"].get("status") != "MATCH":
        return {"component": "crucible_verdict", "failure_code": "crucible_verdict_not_match", "verdict": "DRIFT"}
    if packet["redaction_status"].get("raw_private_payloads_included") is not False:
        return {"component": "redaction_status", "failure_code": "private_payload_boundary_violation", "verdict": "DRIFT"}
    return {"component": "packet", "failure_code": None, "verdict": "MATCH"}


def negative_fixtures(base: dict) -> list[dict]:
    rows = []
    for fixture_id, expected_failure_code, expected_verdict, mutate in NEGATIVE_MUTATIONS:
        packet = copy.deepcopy(base)
        mutate(packet)
        packet["packet_hash"] = sha256_obj({k: v for k, v in packet.items() if k != "packet_hash"})
        observed = validate_packet(packet)
        rows.append({
            "expected_failure_code": expected_failure_code,
            "expected_verdict": expected_verdict,
            "fixture_id": fixture_id,
            "observed": observed,
            "packet_hash": packet["packet_hash"],
            "status": "MATCH" if observed["failure_code"] == expected_failure_code and observed["verdict"] == expected_verdict else "DRIFT",
        })
    return rows


def render_packet(contract: dict) -> str:
    return f"""# Packet 061: Agent Action Proof Packet Negative Fixtures

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0051 defines failure cases for the public agent action proof packet demo.

```text
positive_verdict = {contract['positive_fixture_verdict']['verdict']}
negative_fixture_count = {contract['verifier_measurements']['negative_fixture_count']}
negative_match_count = {contract['verifier_measurements']['negative_match_count']}
failure_code_count = {contract['verifier_measurements']['failure_code_count']}
```

Required failures cover missing source refs, workspace context, admission
telemetry, action receipt linkage, browser evidence, ledger continuity,
Crucible verdict, and raw private payload leakage.

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0051 Steelman: Agent Action Proof Packet Negative Fixtures

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

These fixtures prove only a local synthetic validator contract. They do not
prove the final packet composer exists, that external trace imports are
complete, or that the failure taxonomy is exhaustive. New integrations should
add more negative fixtures before promotion.
"""


def main() -> None:
    previous = read_json(PREVIOUS_PACKET)
    previous_sha = sha256_file(PREVIOUS_PACKET)
    base = positive_packet()
    positive_verdict = validate_packet(base)
    negatives = negative_fixtures(base)
    failure_codes = sorted({row["expected_failure_code"] for row in negatives})
    all_match = positive_verdict["verdict"] == "MATCH" and all(row["status"] == "MATCH" for row in negatives)
    fixture = with_seal({
        "generated_on": "2026-07-01",
        "negative_fixtures": negatives,
        "pass": PASS,
        "positive_fixture": base,
        "schema": "AgentActionProofPacketNegativeFixturesFixture/v1",
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    contract = with_seal({
        "current_promoted_natural_laws": [],
        "failure_codes": failure_codes,
        "fixture": {"path": "fixtures/agent-action-proof-packet-negative-fixtures-pass-0051.json", "schema": fixture["schema"], "seal": fixture["seal"], "sha256": fixture_sha},
        "generated_on": "2026-07-01",
        "negative_fixtures": negatives,
        "non_promotion_statement": "Pass 0051 is a synthetic negative-fixture contract. It does not prove the integrated public demo exists, product-market fit, buyer adoption, scientific truth, or any natural law.",
        "pass": PASS,
        "positive_fixture_hash": base["packet_hash"],
        "positive_fixture_verdict": positive_verdict,
        "previous_pass_binding": {"path": "schemas/agent-action-proof-packet-demo-spec-pass-0050.json", "seal": previous["seal"], "sha256": previous_sha, "source_status": previous["status"]},
        "schema": "AgentActionProofPacketNegativeFixturesSet/v1",
        "status": "AGENT_ACTION_PROOF_PACKET_NEGATIVE_FIXTURES_MATCH" if all_match else "AGENT_ACTION_PROOF_PACKET_NEGATIVE_FIXTURES_DRIFT",
        "uniqueness_claim_status": "HYPOTHESIS_ONLY",
        "verifier_measurements": {"failure_code_count": len(failure_codes), "negative_fixture_count": len(negatives), "negative_match_count": sum(1 for row in negatives if row["status"] == "MATCH"), "positive_match_count": 1 if positive_verdict["verdict"] == "MATCH" else 0},
    })
    write_json(OUT_PATH, contract)
    write_text(PACKET_PATH, render_packet(contract))
    write_text(STEELMAN_PATH, render_steelman())
    print(json.dumps({
        "negative_fixture_count": len(negatives),
        "path": str(OUT_PATH),
        "seal": contract["seal"],
        "status": contract["status"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
