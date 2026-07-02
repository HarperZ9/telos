"""Validate pass 0050 agent action proof-packet demo spec receipts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "agent-action-proof-packet-demo-spec-pass-0050.json"
FIXTURE_PATH = ROOT / "fixtures" / "agent-action-proof-packet-demo-spec-pass-0050.json"
PREVIOUS_PACKET = ROOT / "schemas" / "wedge-budget-signal-scorecard-pass-0049.json"
RESULT_PATH = ROOT / "schemas" / "pass-0050-agent-action-proof-packet-demo-spec-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def check_seal(value: dict) -> bool:
    copy = dict(value)
    seal = copy.pop("seal", None)
    return seal == sha256_obj(copy)


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    contract = load_json(SCHEMA_PATH)
    fixture = load_json(FIXTURE_PATH)
    previous = load_json(PREVIOUS_PACKET)
    m = contract.get("verifier_measurements", {})
    require(contract.get("schema") == "AgentActionProofPacketDemoSpecSet/v1", errors, "schema mismatch")
    require(contract.get("status") == "AGENT_ACTION_PROOF_PACKET_DEMO_SPEC_MATCH", errors, "status mismatch")
    require(check_seal(contract), errors, "contract seal mismatch")
    require(check_seal(fixture), errors, "fixture seal mismatch")
    require(contract.get("previous_pass_binding", {}).get("sha256") == sha256_file(PREVIOUS_PACKET), errors, "pass0049 sha mismatch")
    require(contract.get("previous_pass_binding", {}).get("seal") == previous.get("seal"), errors, "pass0049 seal mismatch")
    require(contract.get("fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
    require(contract.get("primary_market") == "agent_action_proof_packets", errors, "primary market mismatch")
    require(m.get("component_count") == 11, errors, "component count mismatch")
    require(m.get("component_match_count") == 11, errors, "component match count mismatch")
    require(m.get("summary_match_count") == 3, errors, "summary match count mismatch")
    require(m.get("integration_gap_count") == 6, errors, "integration gap count mismatch")
    require(m.get("demo_flow_step_count") == 10, errors, "demo flow count mismatch")
    require(len(contract.get("thirty_day_acceptance_checks", [])) == 4, errors, "acceptance check count mismatch")
    require(contract.get("uniqueness_claim_status") == "HYPOTHESIS_ONLY", errors, "uniqueness overclaimed")
    require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")
    for row in contract.get("component_receipts", []):
        require(row.get("exists") is True, errors, f"missing component {row.get('component')}")
        require(row.get("schema_match") is True, errors, f"schema drift for {row.get('component')}")
    for row in contract.get("summary_receipts", []):
        require(row.get("status") == "MATCH", errors, f"summary drift for {row.get('component')}")
    result = {
        "checks": [{
            "artifact": "AgentActionProofPacketDemoSpecSet",
            "component_count": m.get("component_count"),
            "errors": errors,
            "integration_gap_count": m.get("integration_gap_count"),
            "path": str(SCHEMA_PATH.relative_to(ROOT)),
            "status": "MATCH" if not errors else "DRIFT",
        }],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0050",
        "schema": "Pass0050AgentActionProofPacketDemoSpecValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT",
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
