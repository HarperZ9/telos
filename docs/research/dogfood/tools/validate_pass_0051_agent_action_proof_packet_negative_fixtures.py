"""Validate pass 0051 agent action proof-packet negative fixtures."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "agent-action-proof-packet-negative-fixtures-pass-0051.json"
FIXTURE_PATH = ROOT / "fixtures" / "agent-action-proof-packet-negative-fixtures-pass-0051.json"
PREVIOUS_PACKET = ROOT / "schemas" / "agent-action-proof-packet-demo-spec-pass-0050.json"
RESULT_PATH = ROOT / "schemas" / "pass-0051-agent-action-proof-packet-negative-fixtures-validator-result.json"


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
    negatives = contract.get("negative_fixtures", [])
    require(contract.get("schema") == "AgentActionProofPacketNegativeFixturesSet/v1", errors, "schema mismatch")
    require(contract.get("status") == "AGENT_ACTION_PROOF_PACKET_NEGATIVE_FIXTURES_MATCH", errors, "status mismatch")
    require(check_seal(contract), errors, "contract seal mismatch")
    require(check_seal(fixture), errors, "fixture seal mismatch")
    require(contract.get("previous_pass_binding", {}).get("sha256") == sha256_file(PREVIOUS_PACKET), errors, "pass0050 sha mismatch")
    require(contract.get("previous_pass_binding", {}).get("seal") == previous.get("seal"), errors, "pass0050 seal mismatch")
    require(contract.get("fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
    require(contract.get("positive_fixture_verdict", {}).get("verdict") == "MATCH", errors, "positive fixture mismatch")
    require(m.get("negative_fixture_count") == 8, errors, "negative fixture count mismatch")
    require(m.get("negative_match_count") == 8, errors, "negative match count mismatch")
    require(m.get("failure_code_count") == 8, errors, "failure code count mismatch")
    require(m.get("positive_match_count") == 1, errors, "positive match count mismatch")
    require(contract.get("uniqueness_claim_status") == "HYPOTHESIS_ONLY", errors, "uniqueness overclaimed")
    require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")
    for row in negatives:
        require(row.get("status") == "MATCH", errors, f"negative fixture drift: {row.get('fixture_id')}")
        require(row.get("observed", {}).get("failure_code") == row.get("expected_failure_code"), errors, f"failure code mismatch: {row.get('fixture_id')}")
        require(row.get("observed", {}).get("verdict") == row.get("expected_verdict"), errors, f"verdict mismatch: {row.get('fixture_id')}")
        require(row.get("observed", {}).get("verdict") != "MATCH", errors, f"negative fixture passed unexpectedly: {row.get('fixture_id')}")
    result = {
        "checks": [{
            "artifact": "AgentActionProofPacketNegativeFixturesSet",
            "errors": errors,
            "negative_fixture_count": m.get("negative_fixture_count"),
            "path": str(SCHEMA_PATH.relative_to(ROOT)),
            "status": "MATCH" if not errors else "DRIFT",
        }],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0051",
        "schema": "Pass0051AgentActionProofPacketNegativeFixturesValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT",
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
